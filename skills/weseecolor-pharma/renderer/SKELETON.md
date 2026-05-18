# Card-renderer skeleton (template invariants)

This file documents the geometric model — the **invisible skeleton** — that the
HTML template draws into. The skeleton is invariant. Content (product names,
field values, image dimensions, ingredient lists) flows into it, and every
constraint here must hold no matter what content is poured in.

## Page envelope

| Constant | Value | Notes |
|---|---|---|
| Sheet size | A4 = 210 × 297 mm | |
| `@page` horizontal margin | 0 | cream `@page` background bleeds edge-to-edge |
| `@page` top margin (page 1) | 0 | so the textured corner can bleed past the top edge |
| `@page` top margin (pages 2+) | 25 mm | classic Word-like top inset |
| `@page` bottom margin | 22 mm | room for the 10.5 mm ribbon + 9 mm cream gap below + ~2.5 mm of safety |
| `.page` horizontal padding | 18 mm each side | content area is **174 mm** wide (from x=18 to x=192 in page coords) |
| Brown ribbon | `@bottom-center`, 210 mm × 10.5 mm, anchored 9 mm above page bottom | repeats on every page |

## Top-of-page-1 anchors (the most rigid block)

This is the slot the logo and the product image both reference.

| Anchor | Value | Geometry |
|---|---|---|
| `--logo-right-offset` | 11 mm | distance from `.page` content right edge to the logo's right edge |
| `--logo-width` | 63 mm | logo's rendered width |
| `--logo-top-offset` | 6 mm | distance from page top to the logo's top (was 13 mm — moved up so the logo no longer touches the OVERVIEW red divider) |
| `--logo-center-from-right` | 11 + 63/2 = **42.5 mm** | distance from `.page` content right edge to the logo's horizontal center |

The product image's center must always equal the logo's center on the X axis,
regardless of the image's own dimensions. The pattern is:

```css
.product-image {
  position: absolute;
  right: var(--logo-center-from-right);  /* same reference as the logo center */
  transform: translateX(50%);             /* shift element half its width to the right */
  /* the result: the element's CENTER is exactly at the logo center X,
     independent of its own width (translateX(50%) uses the element's own
     rendered width) */
}
```

Because both the logo and the image are anchored to the **same parent's right
edge with the same numerical offset**, any Chrome rendering quirk applies to
both identically — they will always sit on the same vertical axis.

## Typography scale

All body-style text uses the same `--font-body` (Forum) at **12.5 pt** so the
card reads with one consistent body voice. Specific exceptions:

| Use | Class | Size | Notes |
|---|---|---|---|
| Body baseline | `html, body` | 12.5 pt | inherited by Overview values, Recommendation, table data, considerations |
| Findings title (e.g. "SAFETY", "RESEARCH / DATA AVAILABLE") | `.finding-title` | 12.5 pt | Biryani, uppercase + 0.02em letter-spacing |
| Findings sub-label (e.g. "Low Risk", "Fair") | `.finding-label` | 12.5 pt | Forum, muted color |
| Findings description | `.finding-desc` | 12.5 pt | Forum, body color |
| Section headings (OVERVIEW, KEY FINDINGS…) | `.section-h` | 15 pt | Biryani 300, uppercase + 0.015em letter-spacing, **red divider above** via `border-top` |
| Rating sub-headings (SAFETY RATING, RESEARCH / DATA AVAILABILITY RATING, GENERAL CONSIDERATIONS) on the legend page | `.rating-sub` | 11.5 pt | Biryani 300, uppercase + 0.02em letter-spacing, **red divider above** via `border-top` (matches the main section style; was missing before) |
| Title "Product Review" | `.top-header h1` | 26 pt | Montserrat 300 |
| Recommendation label | `.rec-label` | 10 pt | Saira 300, uppercase + 0.04em letter-spacing |
| Brown ribbon text | `@bottom-center content` | 11 pt | Saira 300 |
| Legend intro (page 3) | `.results-intro` | 13 pt | Forum |
| Legend cell description | `.lc-desc` | 12 pt | Forum |
| General Considerations bullets | `.considerations li` | 12.5 pt | Forum, matches body |
| Last reviewed date | `.last-reviewed` | 9.5 pt | Saira 300 |

**Rule of thumb when bumping body text**: if Jose asks for "match other body
text," touch `html/body` *and* the three `.finding-*` classes *and*
`.results-intro` / `.lc-desc` / `.considerations li`. They share a font scale
but each has its own override and won't pick up `html/body` changes
automatically.

## Overview field list

The Overview field set is a **typed subset**, not arbitrary. Standard rows
(in order):

1. Product name
2. Category
3. Vehicle/form
4. Skin or hair type
5. Used for
6. Black-owned business
7. Certified cruelty-free
8. Certified organic

`Vegan` is **not** part of the standard set (the original sample cards do not
include it). If a product has additional pertinent attributes, append at the
end after Certified organic.

## Element-by-element audit

| Element | Position | Size | Content-size-independent? |
|---|---|---|---|
| `.top-header` block | top: 0 of `.page` | 174 × 50 mm | YES (fixed) |
| Title "Product Review" | bottom: 0 of `.top-header` | text auto | YES (text is fixed string) |
| `.corner-logo` (WSC) | right: `--logo-right-offset`, top: `--logo-top-offset` | width: `--logo-width` | YES (image is fixed asset) |
| `.corner-circle` (texture) | top: -39mm, right: -55mm, rotated 70° | 130 mm wide | YES (decorative bleed) |
| `.section-h` heading | natural flow, with `border-top` divider | text + padding | YES (text length variable, heading just grows) |
| Overview `.fields` sub-table | left ~60% of content area | width: 105 mm, value column auto-fills | YES (long values wrap inside 105 mm; widened from 87 mm so long values wrap to fewer lines) |
| Product image | **see "Top-of-page-1 anchors"** | max-width 58 mm, max-height 64 mm, `object-fit: contain` | YES once refactored to the `right: --logo-center-from-right; translateX(50%)` pattern |
| Key Findings cells | `<table class="findings">` 50/50 columns | each cell auto-fills 50% of content width | YES (text wraps naturally) |
| Rating circles (SVG) | inside `.c-cell` | 22 mm fixed (Key Findings) / 14.5 mm (legend) | YES (SVG is vector, color/number swapped via template) |
| Recommendation | label float-left 35 mm, body `margin-left: 38mm` | body fills remaining width | YES (paragraphs wrap + can break across pages) |
| Supporting Data table | `<table class="data">`, k-col 38 mm + v-col auto | rows + bullets variable count | YES (rows break across pages, bullets wrap) |
| End block | legend-note centered + last-reviewed right-aligned | natural text size | YES (date string variable; format consistent) |
| Page 3 legend tables | 5 × 20% columns | fixed content | YES (static page) |
| General Considerations bullets | normal flow `<ul>` | text variable | YES (text wraps, list grows) |
| Brown ribbon | `@bottom-center` margin box | 210 × 10.5 mm | YES (text is fixed string) |

**The only element NOT YET content-size-independent is the product image** —
the current `position: relative; left: 9mm` shift inside a `text-align: center`
td gets the center to a fixed X (because text-align centers regardless of
width), but the shift is hand-tuned to one image's size context, not derived
from the logo anchor. The refactor below makes the relationship explicit and
robust.

## What stress tests must pass

When the template is populated with different content, these tests should all
still render without overlap, clipping, or visible breakage:

1. **Replace the product image** with a different aspect ratio (e.g. a wide
   square 58×58 mm jar). The image's center must stay on the logo's X axis.
2. **Lengthen a field value** to wrap over 4-5 lines. The fields cell should
   stay inside its 87 mm column; the overview row's height should grow but the
   product image's vertical anchor should still align cleanly.
3. **Shorten the Recommendation** to one short sentence. Page 1 just has more
   cream space at the bottom — no layout breakage.
4. **Lengthen the Recommendation** so it can't fit on page 1. It should break
   to page 2 with the section dividers staying with their headings.
5. **Vary the number of Supporting Data bullets** by 2-3× either direction.
   The table should grow or shrink; pagination decides where to break.
6. **Change the rating numbers and circle colors** (1-5 maps to the 5 named
   colors). The SVG numbers and `fill` values are template-substituted; layout
   is unaffected.

## Renderer + template files

The card is a true generative template:

| File | Role |
|---|---|
| `card_template.html.j2` | Jinja2 HTML template with `{{ product.* }}`, `{{ safety.* }}`, `{{ research.* }}`, recommendation/bullet loops, and the static legend page |
| `render_card.py` | Renderer. Takes a JSON content file, expands rating integers (1-5) into label + color + descriptor via the embedded legend tables, renders the template, and prints to PDF via **WeasyPrint** |
| `eucrisa.json` | Example content file (sample card #5024 Eucrisa) showing the input shape |
| `sample_card.html` | The Differin baseline, hand-edited copy of the template — kept as the visual-regression reference |

To render a card (uses the conda-managed Python at `~/miniforge3/bin/python3`,
which has WeasyPrint, Pango, Cairo, Jinja2, and PyMuPDF installed):
```bash
~/miniforge3/bin/python3 render_card.py eucrisa.json eucrisa_card.pdf
```

The JSON's `safety.rating` and `research.rating` are integers 1-5. The
renderer applies the exact legend wording (label + descriptor) and the
correct fill color (`--c1`…`--c5`) automatically — never hand-write those.

### Why WeasyPrint and not headless Chrome

WeasyPrint is a pure-Python CSS Paged Media engine. Compared to the previous
Chrome-headless renderer:

- No external Chrome subprocess, no transient HTTP server.
- Web-app deployable: ships in a Python container, returns PDF bytes directly.
- Standards-compliant CSS Paged Media: `position: running()`, `@page` margin
  boxes, `page-break-inside: avoid`, table border handling all work the way
  the spec says.
- Logo + product-image anchor (`right: var(--logo-center-from-right); transform:
  translateX(50%)`) lands within **0.05 mm** of the target, vs ~13 mm off in Chrome.

The trade-off is that WeasyPrint's text engine (Pango) wraps slightly more
conservatively than Chrome's Skia. The same content takes ~1 extra line per
long paragraph. See "Page-count expectations" below.

## Page-count expectations

| Content profile | Pages | Notes |
|---|---|---|
| Standard (e.g. Differin: 2-paragraph Recommendation, 5-7 data-source URLs) | **3** | The design target. |
| Heavy (e.g. Eucrisa: 2-paragraph Recommendation that fills 8 lines on its own + 12 data-source URLs) | **4** | The Supporting Data table doesn't fit on a single page; Data sources continues onto its own page before the legend. |

**This is acceptable** — the design holds throughout, the geometric anchors
(logo / image / dividers / ribbon) remain correct, and the only difference is
that very URL-dense Data sources sections paginate to a third data page.

When evaluating a new product card, expect 3 pages if Data sources is ≤8 URLs
and Recommendation is ≤2 paragraphs of ≤300 chars each. Above that, expect 4.

To recover the strict 3-page target on heavy content would require either:
- Multi-column layout for Data sources (visual departure from the reference cards), or
- Body font drop below 10pt across the data table (compromises the readability
  bump established earlier in this design), or
- Reverting to headless Chrome (its Skia text engine wraps tighter, fitting
  Eucrisa into 3 pages — but at the cost of all the print-mode quirks that
  WeasyPrint solves cleanly).

## Stress test results (2026-05-13)

**1. Image aspect-ratio variants.** Replaced `DifferinGel.png` with three
generated test images and measured the product image's center X against the
logo's center X via PyMuPDF bbox inspection:

| Variant | Image size | Image center X | Logo center X | Δ |
|---|---|---|---|---|
| Differin (tall, 0.70:1) | 35.5 × 50.8 mm | 162.41 mm | 162.37 mm | +0.03 mm |
| Square (1:1) | 45.9 × 45.9 mm | 162.39 mm | 162.37 mm | +0.02 mm |
| Wide (2:1) | 45.9 × 23.1 mm | 162.39 mm | 162.37 mm | +0.02 mm |
| Narrow (0.40:1) | 20.1 × 50.8 mm | 162.45 mm | 162.37 mm | +0.08 mm |

All within 0.1 mm regardless of source image aspect ratio. The
`right: var(--logo-center-from-right); transform: translateX(50%)` pattern
holds.

**2. Content-length variants.**

| Variant | Pages | Notes |
|---|---|---|
| Short Recommendation (1 sentence) | 3 | Supporting Data section gains room on page 1; page-1 ribbon and last-reviewed unaffected. |
| Long Recommendation (4 full paragraphs) | 3 | Recommendation breaks mid-paragraph at the page-1 bottom and resumes at the top of page 2; section divider stays with the heading. |
| Very long field value (3-line wrap → 7 lines) | 3 | Overview row grows vertically; product image anchored at the same X; subsequent sections (Key Findings, Recommendation) just shift down accordingly. |

All three rendered the expected 3-page output with no clipping, no orphaned
dividers, and no misaligned product image.

**3. Full end-to-end test with a real second product — Eucrisa (sample #5024).**

Rendered via the new `render_card.py` + `eucrisa.json` pipeline. Different
fields, different product image (a wider-bodied ointment tube), longer
recommendation paragraphs, 12 data-source URLs (vs Differin's 7), and a
different rating descriptor (Safety 4 → "Low Risk" derived automatically
from the rating integer). Result: 3 pages, all content rendered, product
image center aligned with logo within 0.1mm.

### Bug found and fixed during this test

**End-block orphan page** — with longer Supporting Data content, Chrome
broke the `.end-block` between its two `<p>` children: "See the legend on
page 3" landed at the bottom of page 2 and "Last reviewed" was orphaned on
its own page 3, pushing the legend to page 4 (4 pages total instead of 3).

`page-break-inside: avoid` on the generic `<div class="end-block">` was
ignored. Fix: change `.end-block` to `display: flex; flex-direction: column`
and add `break-inside: avoid` alongside the legacy `page-break-inside`. Flex
containers are treated by Chrome's print engine as a single layout unit and
the rule is now honored. Internal margins were also tightened (legend-note
`margin-bottom` 3mm → 1mm, last-reviewed `margin-top` 2mm → 0) so the block
takes ~5mm less vertical space and fits more easily at the end of a packed
page-2.

This fix was applied to both the live `sample_card.html` and the
`card_template.html.j2` template.
