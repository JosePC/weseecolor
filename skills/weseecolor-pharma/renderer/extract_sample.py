"""
One-off helper to draft a content JSON + extract the product image from a
reference sample PDF, ready for hand-curation and render.

Usage:
    ~/miniforge3/bin/python3 extract_sample.py \
        "/path/to/5018 - … product card.pdf" \
        5018

Produces:
    samples/5018_product.png   (best-guess product image)
    samples/5018.json          (draft content, may need manual cleanup)
"""

import fitz
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLES = HERE / "samples"
SAMPLES.mkdir(exist_ok=True)


def extract_product_image(pdf_path, out_path):
    """Pull the product image off page 1. Picks the largest non-logo, non-corner
    image whose bbox is in the right half of the page (product images sit there
    on these cards)."""
    doc = fitz.open(pdf_path)
    p1 = doc[0]
    pw, ph = p1.rect.width, p1.rect.height
    best = None
    best_score = 0
    for info in p1.get_image_info(xrefs=True):
        bbox = info["bbox"]
        x0, y0, x1, y1 = bbox
        w_mm = (x1 - x0) / 2.83
        h_mm = (y1 - y0) / 2.83
        cx = (x0 + x1) / 2
        # Filter to images in the right half of the page top area
        if cx < pw * 0.45 or y0 > ph * 0.55:
            continue
        # Skip extreme-corner decoration (textured circle is usually >120mm)
        if w_mm > 100 or h_mm > 100:
            continue
        # Skip the logo (aspect ~1.9, ~50mm wide, in the upper-right)
        ar = w_mm / h_mm if h_mm else 0
        if 1.7 < ar < 2.1 and y0 < ph * 0.15:
            continue
        # Score by area
        area = w_mm * h_mm
        if area > best_score:
            best_score = area
            best = info
    if best is None:
        print("  no product image candidate found", file=sys.stderr)
        return False
    xref = best["xref"]
    pix = fitz.Pixmap(doc, xref)
    pix.save(str(out_path))
    print(f"  product image: {out_path.name}  ({pix.width}x{pix.height})")
    doc.close()
    return True


def extract_text(pdf_path):
    """Return the full text content as a single string for parsing."""
    doc = fitz.open(pdf_path)
    pages = [p.get_text() for p in doc]
    doc.close()
    return pages


def find_field(label, text, multiline=False):
    """Find a label like 'Product name:' and return the value following it.

    Sample cards put each field on its own block; the value follows the label
    either on the same line or on the next block. We try to grab everything up
    to the next known label.
    """
    next_labels = [
        "Product name:", "Category:", "Skin or hair type:", "Used for:",
        "Black-owned business:", "Certified cruelty-free:", "Certified organic:",
        "Vegan:", "Vehicle/form:", "SUPPORTING DATA AND ANALYSIS",
        "Active ingredients", "KEY FINDINGS", "RECOMMENDATION",
        "Learn more", "Last reviewed", "OVERVIEW",
    ]
    next_labels = [n for n in next_labels if n != label]
    pat = re.escape(label) + r"\s*(.+?)(?=" + "|".join(re.escape(n) for n in next_labels) + r"|$)"
    m = re.search(pat, text, flags=re.DOTALL)
    if not m:
        return ""
    v = m.group(1).strip()
    # squash whitespace
    if not multiline:
        v = re.sub(r"\s+", " ", v).strip()
    else:
        v = re.sub(r"\n\s*", "\n", v).strip()
    return v


def draft_json(pdf_path, sid):
    pages = extract_text(pdf_path)
    full = "\n".join(pages)

    # Overview fields
    product = {
        "name":           find_field("Product name:", full),
        "category":       find_field("Category:", full),
        "form":           find_field("Vehicle/form:", full),
        "skin_hair_type": find_field("Skin or hair type:", full),
        "used_for":       find_field("Used for:", full),
        "black_owned":    find_field("Black-owned business:", full),
        "cruelty_free":   find_field("Certified cruelty-free:", full),
        "organic":        find_field("Certified organic:", full),
        "image_src":      f"samples/{sid}_product.png",
    }

    # Ratings — Safety + Research/Data Available
    # The card lists labels like "Low Risk", "Fair" near the SVG circles.
    safety_labels = ["Very High Risk", "High Risk", "Moderate Risk", "Low Risk", "Very Low Risk"]
    research_labels = ["None", "Limited", "Fair", "Good", "Robust"]
    safety = research = 3  # safe fallback
    for i, lbl in enumerate(safety_labels, start=1):
        # The label appears next to "SAFETY" in the original layout
        if re.search(r"SAFETY\s+" + re.escape(lbl), full) or re.search(re.escape(lbl) + r"\s+\w[^\n]{0,80}low irritancy", full, re.I):
            safety = i; break
        if "\n" + lbl + "\n" in full:
            safety = i  # tentative
    for i, lbl in enumerate(research_labels, start=1):
        if re.search(r"RESEARCH\s*/\s*DATA\s*AVAILABLE\s+" + re.escape(lbl), full, re.I):
            research = i; break

    # Recommendation: paragraphs after "RECOMMENDATION:" until next section
    rec_match = re.search(r"RECOMMENDATION:\s*(.+?)(?=SUPPORTING DATA AND ANALYSIS|Active ingredients|Vegan:|$)", full, flags=re.DOTALL)
    rec_text = rec_match.group(1).strip() if rec_match else ""
    # Split on blank lines or "There is enough", "There is a fair", etc — a heuristic for paragraph boundaries
    rec_paragraphs = [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", rec_text) if p.strip()]
    rec_paragraphs = [re.sub(r"\s+", " ", p) for p in rec_paragraphs]
    if not rec_paragraphs:
        rec_paragraphs = ["TODO: extract recommendation"]

    # Supporting data sections — these are harder, just put placeholders
    # so the human curator fills in.
    active = find_field("Active ingredients", full)
    inactive = find_field("Inactive ingredients", full)

    # Bullet lists: get content between section headers
    def bullets(heading_pattern, until_pattern):
        m = re.search(heading_pattern + r"\s*(.+?)(?=" + until_pattern + r"|$)", full, flags=re.DOTALL | re.IGNORECASE)
        if not m:
            return ["TODO"]
        chunk = m.group(1)
        # Split on lines that look like bullet starters
        parts = re.split(r"\n(?=[A-Z][^a-z\n]*[a-z])", chunk)
        out = [re.sub(r"\s+", " ", p).strip() for p in parts if p.strip()]
        return out or ["TODO"]

    formulation = bullets(r"Formulation concerns?", r"Research and ingredient analysis")
    research_an = bullets(r"Research and ingredient analysis", r"Data sources to consider")
    data_sources_raw = bullets(r"Data sources to consider", r"See the legend|Last reviewed")

    last_reviewed_m = re.search(r"Last reviewed:?\s*([A-Z][a-z]+ \d{4})", full)
    last_reviewed = last_reviewed_m.group(1) if last_reviewed_m else "October 2025"

    return {
        "product": product,
        "safety":   { "rating": safety },
        "research": { "rating": research },
        "recommendation": rec_paragraphs,
        "active_ingredients": active or "TODO",
        "inactive_ingredients": inactive or "TODO",
        "formulation_concerns": formulation,
        "research_analysis": research_an,
        "data_sources": data_sources_raw,
        "last_reviewed": last_reviewed,
    }


def main():
    pdf_path = Path(sys.argv[1])
    sid = sys.argv[2]
    print(f"Sample {sid}: {pdf_path.name}")

    out_img = SAMPLES / f"{sid}_product.png"
    extract_product_image(pdf_path, out_img)

    data = draft_json(pdf_path, sid)
    out_json = SAMPLES / f"{sid}.json"
    with out_json.open("w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  draft json:    {out_json.name}")


if __name__ == "__main__":
    main()
