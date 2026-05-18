"""
WeSeeColor product card renderer.

Takes a JSON content file describing one product analysis and produces a 3-page
A4 PDF using the geometric skeleton documented in SKELETON.md. PDF rendering
uses WeasyPrint (pure-Python CSS Paged Media engine) — no Chrome subprocess,
no HTTP server, web-app deployable.

Input JSON shape (see eucrisa.json for an example):

  {
    "product": {
      "name":            "Eucrisa (crisaborole)",
      "category":        "Rx, topical nonsteroidal phosphodiesterase-4 inhibitor for atopic dermatitis",
      "form":            "Ointment 2%",
      "skin_hair_type":  "...",
      "used_for":        "...",
      "black_owned":     "No",
      "cruelty_free":    "No",
      "organic":         "No",
      "image_src":       "eucrisa_product.png"
    },
    "safety": { "rating": 4 },              # 1-5; label / color / descriptor derived from the legend
    "research": { "rating": 3 },            # same shape
    "recommendation": [
        "First paragraph...",
        "Second paragraph..."
    ],
    "active_ingredients": "Crisaborole 2%",
    "inactive_ingredients": "White petrolatum, propylene glycol, ...",
    "formulation_concerns":  [ "Bullet 1", "Bullet 2", ... ],
    "research_analysis":     [ "Bullet 1", "Bullet 2", ... ],
    "data_sources":          [ "Bullet 1", "Bullet 2", ... ],
    "last_reviewed":         "October 2025"
  }

Usage:
  python3 render_card.py eucrisa.json eucrisa_card.pdf
"""

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from PIL import Image, ImageDraw
from weasyprint import HTML

HERE = Path(__file__).resolve().parent
PREPARED_DIR = HERE / "prepared"
PREPARED_DIR.mkdir(exist_ok=True)

# Legend bindings — must match the exact wording in references/rating-legend.md.
# Index 0 is unused; ratings are 1-5.
SAFETY_LEGEND = [
    None,
    ("Very High Risk", "#DC4538", "Caution. Strong likelihood that this product may cause irritation and/or an allergic reaction. Seek medical attention if exposed."),
    ("High Risk",      "#E67E22", "This product may cause irritation and/or an allergic reaction. Be careful and consult your physician."),
    ("Moderate Risk",  "#F2C94C", "In certain situations, this product may cause irritation or an allergic reaction. Speak with your physician to learn more."),
    ("Low Risk",       "#82B23A", "Generally safe. Product ingredients have low irritancy or allergy potential."),
    ("Very Low Risk",  "#2E9D5C", "Safe to use on most occasions. Product ingredients have negligible irritancy or allergy potential."),
]

RESEARCH_LEGEND = [
    None,
    ("None",    "#DC4538", "There is no data on this product or ingredients used in the Black community."),
    ("Limited", "#E67E22", "There is limited published data on this product or ingredients used in the Black community."),
    ("Fair",    "#F2C94C", "There is a fair amount of published data or documented usage in the Black community."),
    ("Good",    "#82B23A", "Product or its ingredients have been studied extensively or used extensively in the Black community."),
    ("Robust",  "#2E9D5C", "This product or its ingredients have been studied extensively, used extensively, and known in the Black community."),
]


def expand_rating(rating_int, legend):
    """Given a 1-5 integer rating + a legend table, return the dict the template expects."""
    if not (isinstance(rating_int, int) and 1 <= rating_int <= 5):
        raise ValueError(f"Rating must be an integer 1-5, got {rating_int!r}")
    label, color, descriptor = legend[rating_int]
    return {"rating": rating_int, "label": label, "color": color, "descriptor": descriptor}


def prepare_product_image(src_path: Path) -> Path:
    """Return a path to a product image that renders cleanly on the card.

    Two cases:

      1. The input already has real transparency (alpha channel with any
         non-opaque pixels). Trust it — pass through unchanged.

      2. The input is effectively opaque (no alpha, or alpha is all 255).
         Run a flood-fill from each of the four corners, replacing the
         connected similar-color region with transparency. This handles:
           - Uniform backgrounds (white, black, cream) — all four floods
             cover the same region, removing the whole backdrop.
           - Composite/screenshot images with different backgrounds in
             different corners (5022 has light grey at the top half and
             pure black at the bottom half — each corner's flood removes
             its own connected region independently).
           - Backgrounds with mild compression noise — the per-channel
             tolerance lets near-uniform pixels also flood.

    Flood-fill is connectivity-aware: a product element in the middle of
    the image with the same color as the background is NOT removed unless
    it's spatially connected to a corner. Safer than a global color-key.

    None of this is infallible — a photo background, a gradient, or a
    backdrop that wraps around the product without ever reaching a corner
    will not be removed. Those cases trigger the soft-validation warning
    in _warn_if_opaque() and need to be fixed at the asset-source layer.
    """
    im = Image.open(src_path)
    rgba = im.convert("RGBA")

    # Case 1 — has real transparency already; trust the user's asset.
    alpha = rgba.split()[-1]
    if alpha.getextrema() != (255, 255):
        return src_path

    # Case 2 — flood-fill from each corner. Tolerance of 15 lets us catch
    # JPEG-style compression artifacts and slightly-non-uniform light-grey
    # backdrops (5022's top-corner pair was 226 vs 213 in the grey channel,
    # within 15).
    w, h = rgba.size
    corner_xys = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    tolerance = 15

    for xy in corner_xys:
        r, g, b, a = rgba.getpixel(xy)
        if a == 0:
            # Already transparent — either an earlier corner's flood
            # reached this one, or the corner happened to be transparent.
            continue
        # Replace the connected similar-color region with the same RGB
        # but alpha=0. PIL compares each visited pixel against the SEED
        # color (the corner) with the given threshold, so the alpha
        # transition from 255 to 0 in already-filled pixels doesn't break
        # the traversal.
        ImageDraw.floodfill(rgba, xy, (r, g, b, 0), thresh=tolerance)

    out = PREPARED_DIR / f"{src_path.stem}_keyed.png"
    rgba.save(out, "PNG", optimize=True)
    return out


def _warn_if_opaque(prepared_path: Path, original_path: Path) -> None:
    """Soft-validate that the prepared image has actual transparency.

    We trust the user to provide a PNG with a transparent background.
    `prepare_product_image()` rescues common failure cases (a non-alpha
    PNG with uniform corners gets color-keyed), but if the input has a
    photo background or non-uniform-color backdrop, the prepared image
    will render *with* that background showing — visibly wrong on the
    cream card.

    This emits a non-blocking warning so the renderer still produces a
    PDF (the broken background is obvious in the output, which is itself
    useful feedback), but the issue gets surfaced in logs so it can be
    fixed at the asset-source layer.
    """
    im = Image.open(prepared_path)
    if im.mode not in ("RGBA", "LA"):
        print(
            f"⚠ {original_path.name}: no alpha channel and corner key-out did not trigger. "
            f"Image will render with whatever background is in the PNG. "
            f"Please re-export with a transparent background.",
            file=sys.stderr,
        )
        return
    # Has an alpha channel — confirm it carries actual transparency.
    alpha = im.split()[-1]
    if alpha.getextrema() == (255, 255):
        print(
            f"⚠ {original_path.name}: alpha channel is fully opaque. "
            f"Image will render with whatever background is in the PNG. "
            f"Please re-export with a transparent background.",
            file=sys.stderr,
        )


def split_data_source(entry):
    """Parse a `"description: https://url"` string into {description, url}.

    Each data-source entry in the JSON is a single string of the form
    "<descriptive lead-in>: <URL>" (a few are URL-only or description-only).
    The template wants them rendered as two visual lines: the description,
    then the URL on a new line, hyperlinked and clickable in the PDF.
    """
    if isinstance(entry, dict):
        return {"description": entry.get("description", ""), "url": entry.get("url", "")}
    s = str(entry).strip()
    # Find the URL — earliest occurrence of "http://" or "https://"
    for marker in ("https://", "http://"):
        idx = s.find(marker)
        if idx >= 0:
            description = s[:idx].rstrip().rstrip(":").rstrip()
            url = s[idx:].rstrip()
            return {"description": description, "url": url}
    return {"description": s, "url": ""}


def render(content_path: Path, out_pdf: Path):
    # Load content
    with content_path.open() as f:
        data = json.load(f)

    # Expand rating integers into label / color / descriptor
    data["safety"]   = expand_rating(data["safety"]["rating"],   SAFETY_LEGEND)
    data["research"] = expand_rating(data["research"]["rating"], RESEARCH_LEGEND)

    # Auto-fix product image: ensure transparent / color-keyed background.
    # The template renders into a fixed 60×60mm slot, so no per-product
    # height computation is needed — the slot takes whatever PNG we hand it
    # and fits it via object-fit: contain.
    img_rel = data.get("product", {}).get("image_src")
    if img_rel:
        src = HERE / img_rel
        if src.exists():
            cleaned = prepare_product_image(src)
            data["product"]["image_src"] = cleaned.relative_to(HERE).as_posix()
            _warn_if_opaque(cleaned, src)
        # If it doesn't exist, leave the path as-is — the renderer will surface the broken-image obviously.

    # Split data-source strings into {description, url} for the template
    data["data_sources"] = [split_data_source(e) for e in data.get("data_sources", [])]

    # Render the Jinja template
    env = Environment(
        loader=FileSystemLoader(str(HERE)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("card_template.html.j2")
    html = template.render(**data)

    # Hand the rendered HTML to WeasyPrint. `base_url` lets it resolve the
    # relative paths to fonts/, the product image, and the corner assets.
    HTML(string=html, base_url=str(HERE)).write_pdf(str(out_pdf))
    print(f"wrote {out_pdf}")


def main():
    ap = argparse.ArgumentParser(description="Render a WeSeeColor product card PDF from a JSON content file.")
    ap.add_argument("content", type=Path, help="Path to the JSON content file.")
    ap.add_argument("output",  type=Path, help="Path to write the PDF.")
    args = ap.parse_args()
    render(args.content, args.output)


if __name__ == "__main__":
    main()
