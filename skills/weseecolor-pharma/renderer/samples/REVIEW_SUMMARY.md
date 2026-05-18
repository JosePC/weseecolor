# Product card renderer v1.0 — smoke-test results

The renderer ([render_card.py](../render_card.py)) now produces the v1.0 format natively from each sample JSON, with no per-card tweaks and no ad-hoc CSS overrides. One command per card:

```bash
~/miniforge3/bin/python3 render_card.py samples/<sid>.json samples/<sid>_card.pdf
```

## Page counts (all 7 cards, native v1.0 render)

| ID | Product | Pages | Notes |
|---|---|:-:|---|
| 5018 | Hyper Skin — Hyper Even Brightening Dark Spot Vitamin C Serum | **3** | Clean |
| 5019 | Rose Ingleton — FutureBright Dark Spot Vitamin C Serum | **3** | Clean |
| 5020 | ZORYVE (roflumilast) cream 0.15% — atopic dermatitis | **3** | Clean |
| 5021 | ZORYVE (roflumilast) foam 0.3% — seborrheic dermatitis | **3** | Was 4p pre-v1.0 — now fits |
| 5022 | ZORYVE (roflumilast) cream 0.3% — plaque psoriasis | **3** | Clean |
| 5023 | ZORYVE (roflumilast) foam 0.3% — plaque psoriasis | **3** | Clean |
| 5024 | Eucrisa (crisaborole) — atopic dermatitis | **3** | Was 4p pre-v1.0 — now fits |

**Every card now fits the 3-page target.** Previously, the two content-densest cards (Eucrisa and the Zoryve sebderm foam) overflowed to 4 pages. The v1.0 typographic system has enough headroom to absorb their content without compromising the standard cards.

## What changed in v1.0 (vs the prior baseline)

All changes live in [card_template.html.j2](../card_template.html.j2). No callsite changes — `render_card.py` is unchanged.

### Type system

- **Body font:** Forum (serif, single-weight) → **Montserrat** (sans, real 300/400/500/700 weights). One font family for the entire body voice across all pages.
- **Sizes** (scaled via Jose's tested Forum 9 ≈ Montserrat 8 ratio):
  - body root: 12.5pt → 11pt
  - Overview table: 10.5pt → 9.5pt
  - Recommendation paragraphs: 11pt → 9pt
  - Rec label, data table rows, legend intro, considerations bullets: all unified at **9pt**
  - Legend rating-card descriptors: 10.5pt → **8pt** (narrower cells, more wrapping)
  - KEY FINDINGS finding-label ("Low Risk", etc.): 12.5pt → 11pt
  - KEY FINDINGS finding-desc: 10.5pt → 9pt
- **Weights:**
  - Overview labels (`td.k`): Regular → **Medium 500** — real glyphs, no synthesis
  - Recommendation label: Saira/Helios → Montserrat **Regular**
  - Data table headers ("Key Area" / "Findings"): Biryani 600 → Montserrat **Bold 700**

### Geometry

- **`--logo-right-offset`:** 11mm → **-6mm** (logo shifted ~17mm rightward, per Jose's "50 px" using the codebase's 1mm = 3px convention).
- **Product image** automatically follows because it's anchored to `--logo-center-from-right`, which is a `calc()` of the right-offset.
- **Overview value column:** `td.fields` width 105mm → **139mm** (with matching max-width — the original had a `max-width: 105mm` that silently clamped any `width` override). The label column stays nowrap and keeps its content width; the entire +34mm flows to the value column.

### Legend page spacing

- **`.rating-sub` margin-top:** 2mm → **6mm**, including the first-of-type override on SAFETY RATING (previously 0mm). All three sub-headings (SAFETY / RESEARCH / GENERAL CONSIDERATIONS) now have matched breathing room above their red dividers.

### What's intentionally unchanged

- Biryani 300 for section headings (OVERVIEW, KEY FINDINGS, SUPPORTING DATA AND ANALYSIS, and the legend's UNDERSTANDING YOUR RESULTS / SAFETY RATING / RESEARCH RATING / GENERAL CONSIDERATIONS). Still uppercase + letter-spacing.
- Saira (`--font-helios`) for the small `.legend-note` ("See the legend on the last page") and `.last-reviewed` annotations on page 2.
- Encode Sans Expanded for the brown ribbon footer.
- Montserrat **300** for the page title ("Product Review").
- Geometric skeleton (the `--logo-*` variables that keep the product image centered on the logo's vertical axis regardless of source image dimensions).

## Files

```
card-renderer/
  render_card.py                — unchanged
  card_template.html.j2         — v1.0 styling baked in
  fonts/
    Montserrat-{300,400,500,700}.ttf   — all real TTFs from Google Fonts gstatic CDN
    Biryani-{300,400,600}.ttf
    EncodeSansExpanded-{300,400,700}.ttf
    Saira-{300,400}.ttf
  samples/
    {5018..5024}.json            — content payloads
    {5018..5024}_product.png     — product images
    {5018..5024}_card.pdf        — rendered v1.0 PDFs (all 3 pages)
```

The previous helper scripts `demo_montserrat.py` and `demo_heavier_labels.py` were deleted — their CSS is now part of the canonical template.

Last rendered: 2026-05-14
