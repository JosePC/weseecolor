---
name: weseecolor-pharma
description: >
  Dermatology and personal care product analysis centered on Black skin and hair safety.
  Use this skill whenever the user asks to analyze a skincare, haircare, or dermatology product,
  create a product safety card, evaluate ingredients for Black skin/hair, check product safety
  ratings, review clinical trial diversity data, or anything related to WeSeeColor product reviews.
  Also trigger when the user mentions WeSeeColor, product cards, ingredient safety analysis,
  EWG/WIMJ/SkinSafe ratings, or FDA safety checks for consumer products.
  This skill produces two output types: Full Product Analysis and Product Cards.
---

# WeSeeColor Pharma Researcher

## Purpose

This skill produces structured, evidence-based analyses of dermatology and personal care products, with a specific focus on safety and efficacy for Black skin and hair. It supports the advocacy work of [WeSeeColor.net](https://weseecolor.net).

## Two Output Types

This skill produces two distinct outputs. The user will request one or the other.

### Output 1: Full Product Analysis

Triggered by: "Analyze [product]", "Product Analysis: [product]", or similar requests.

### Output 2: Product Card

Triggered by: "Create a product card", "Product card for [product]", or similar.

**CRITICAL RULE**: A Product Card can ONLY be generated if a Full Product Analysis for the same product has already been completed in the current conversation. If no prior analysis exists, respond exactly:

> "A product analysis is required before creating the product card. Please request a 'Product Analysis' first."

### Where outputs land

All deliverables and source files are saved under:

```
/Users/josepc/GitHub/weseecolor/outputs/<product-name>/
```

`<product-name>` is a short, recognizable lowercase label with spaces preserved (drop parenthetical scientific names and other noise; strip filesystem-unsafe chars `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`):

| Source product name | Folder slug |
|---|---|
| Hyper Skin — Hyper Even Brightening Dark Spot Vitamin C Serum | `hyper skin vitamin c serum` |
| ZORYVE (roflumilast) topical cream 0.15% for atopic dermatitis | `zoryve cream 0.15 atopic dermatitis` |
| Eucrisa (crisaborole) for atopic dermatitis | `eucrisa atopic dermatitis` |
| Coiff Dew Natural Shampoo | `coiff dew` |

`mkdir -p` the directory if it doesn't exist. Inside, file names mirror the folder as a prefix so individual files are self-describing when shared out of context. See [outputs/README.md](../../outputs/README.md) for the full convention.

**Always save these four files for every product** — partial output is not acceptable. The JSON is the source of truth that lets the card be regenerated; without it the work is half-finished:

| File | Contents |
|---|---|
| `<product-name>-content.json` | The full card content with **every field populated using real values** (recommendation paragraphs, full ingredient lists, every formulation-concern and research-analysis bullet, every data source). No placeholder strings, no ellipses, no "TODO". |
| `<product-name>-product.png` | The product image — transparent-background PNG, ~600px+ longest side, tightly cropped. **Optional**: when no real product image is available (user can't source one), omit this file AND remove the `image_src` field from the JSON entirely. The renderer detects the missing image and collapses the right-side slot so the layout stays tight — no empty box, no alt-text-as-placeholder. **Never** fabricate an image, fill the field with a descriptive string, or point `image_src` at a file you didn't actually save. |
| `<product-name>-card.pdf` | The rendered 3-page card produced by `render_card.py` from the JSON (+ PNG if present). |
| `<product-name>-analysis.html` | The Full Product Analysis (Output 1), in full — every section per the "Required Structure" above. **HTML, built from [references/report-template.html](references/report-template.html)** — copy that file to the output path, then replace every `[bracketed placeholder]` with real content. The template ships with print-friendly CSS (page-break rules, A4 size, URL-printing) so the file opens in any browser AND prints/exports to PDF cleanly. Do not strip the `<style>` block, do not switch to Markdown, do not invent your own HTML scaffold. |

See "Output location" under "Producing the PDF Product Card" below for the full naming convention.

---

## Rating System

The labels and descriptors for both rating scales are baked into the renderer's `SAFETY_LEGEND` and `RESEARCH_LEGEND` constants in [renderer/render_card.py](renderer/render_card.py) — the source of truth. JSON content files store only the **integer rating (1–5)**; the renderer substitutes the matching label, colored circle, and exact descriptor wording. Do not paraphrase descriptors in the Product Card source.

### Safety Rating (1–5)
- 1: Very High Risk
- 2: High Risk
- 3: Moderate Risk
- 4: Low Risk
- 5: Very Low Risk

### Research / Data Availability Rating (1–5)
- 1: None
- 2: Limited
- 3: Fair
- 4: Good
- 5: Robust

The complete visual legend (both rating scales side-by-side, plus General Considerations) renders as page 3 of every product card automatically. To see the canonical look, open page 3 of [assets/sample-product-card.pdf](assets/sample-product-card.pdf).

---

## Output 1: Full Product Analysis

### Tone and Style
- Formal, scientific, regulatory-focused.
- No conversational phrasing.
- Neutral and technical throughout.

### Required Structure (in this exact order)

The HTML built from [references/report-template.html](references/report-template.html) contains every section below. Every section is mandatory. If a section is genuinely N/A for a product, the row stays in place with "Not applicable — [one-sentence reason]" — do not silently delete sections.

### Required reading before drafting

**Read these three references first.** A thin or generic analysis is a failed run; the only way to hit the depth standard is to internalize what prior runs produced.

1. **[references/sample-reports/](references/sample-reports/)** — five completed analyses (5020–5024) covering different forms of the same molecule (roflumilast cream 0.15%, foam 0.3% sebderm, cream 0.3% psoriasis, foam 0.3% psoriasis) plus Eucrisa. Average length: ~56,000 characters. Read at least one before writing — these are the canonical **content depth standard**. Look for:
   - Per-ingredient citation URLs in the prose: "Low hazard. EWG", "Listed; use restrictions/verification substantiation required. EWG", "Cetearyl alcohol page: low irritancy. What's In My Jar"
   - Specific adverse-reaction percentages from pivotal trials (e.g., "nasopharyngitis 1.5%, nausea 1.3%, headache 1.1%")
   - Container / storage / handling specifics (temperature ranges, NDC numbers, do-not-freeze, ≤49°C warnings, pressurized-can flammability)
   - Pediatric labeling specifics (age ranges, separate strength approvals)
   - Long-term safety from open-label extension trials (durations, AE consistency)
   - Pharmacokinetics: peak-to-trough ratios, systemic exposure profile, hepatic-impairment contraindications with Child-Pugh class
   - Trial demographics by race ("11% Black and 5% Asian participants")

2. **[outputs/coiff dew/coiff_dew_report.html](../../outputs/coiff%20dew/coiff_dew_report.html)** — the **visual structure standard**. The HTML layout (Table A ratings, Table B product analysis, Table C additional analysis, 3 ingredient tables, categorized bonus track) is exactly what `references/report-template.html` reproduces as a scaffold.

3. **[references/history/pharma-researcher-chatgpt.md](references/history/pharma-researcher-chatgpt.md)** — the original CustomGPT system prompt. The 10-section "Required Structure" and the Black-participant rating heuristic both originate here. Read for any prior-art instructions that should still hold.

The template + these three references together are the contract. **If your draft is materially thinner than the sample-reports' depth on per-ingredient citations, trial-demographic breakdowns, or regulatory specifics, you have not finished the job.**

**Table A — Recommended Ratings.** Two SVG-circle ratings at the top with the exact color matching the rating value (legend colors are listed inside `report-template.html`). Each rating includes a 150–300 word rationale paragraph that names the specific drivers of the rating.

**Table B — Product Analysis** (8 sections, in order):

1. **Product Information** — Name, generic name, manufacturer, regulatory class, NDC/UPC, active strength, mechanism, US approval date, intended use, composition summary.
2. **Market Data** — Availability, package sizes, pricing (cash list + savings programs), positioning vs. named competitors, family of indications, international notes, MoCRA registration.
3. **Usage** — Verbatim FDA-approved indication in quotes, target population, application, route restrictions, contraindications, BSA from pivotal trials, actionable counseling points.
4. **Full Ingredient List** — Source-cited (FDA PI section + revision date, or product label). Actives with strengths. Inactives verbatim from label. Note explicitly-absent categories ("contains no fragrance, no dyes…").
5. **Efficacy** — Pivotal trials by name and NCT ID, design, N, primary endpoint with quantitative results (% active vs vehicle, treatment difference + 95% CI, p-value), secondary endpoints, Black-skin/Fitzpatrick IV–VI representation and subgroup data, long-term evidence (OLE trials), explicit gaps.
6. **Safety Profile** — Overall (discontinuation rate, common AEs ≥1% **with exact frequencies** verbatim from the trials section of the label — e.g. "nasopharyngitis 1.5%, nausea 1.3%, headache 1.1%", black box status, hypoallergenic claim if any, systemic exposure profile / peak-to-trough ratio if disclosed in the label, long-term safety from open-label extensions with their duration), then per-source: EWG Skin Deep (scores per active and per-key inactive, flag 4+, **with the EWG ingredient page cited inline like the sample-reports do** — "Low hazard. EWG"), WIMJ (green/yellow/red per ingredient, **inline citation** — "Cetearyl alcohol page: low irritancy. What's In My Jar"), SkinSafe (hypoallergenic status, top-allergen flags, **inline citation** — "Ingredient page present. Skin Safe Products"), FDA MedWatch (state "none as of <date>" if no signals), credible journals (authors + journal + year + PMIDs; guideline endorsements with the issuing body name).
7. **FDA and Regulatory Review** — Approval/sNDA, recalls/warning-letters/REMS (state "none" if none), drug interactions with mechanism, pregnancy/lactation, carcinogenicity, MoCRA/EU regs, per-ingredient regulatory flags (IFRA, EU Annex III, FDA §189, CosIng).
8. **Legal / Manufacturer Review** — Manufacturer identification (company, HQ city/state, public/private, ticker), litigation history with case names + court + status, FDA warning letters (state "none" if none), patent status (Hatch-Waxman, generic challenges, ANDA-related stays), manufacturing concerns, contract manufacturing site + any 483 observations, **container/handling/storage with specific numbers from the label**: storage temperature range (e.g., "20–25°C with excursions 15–30°C"), do-not-freeze rules, upright-storage rules for pressurized cans, heat exposure limits (e.g., "do not expose >49°C / 120°F"), flammability warnings for aerosol forms with propellant identities (butane/isobutane/propane), NDC numbers, container sizes.

**Table C — Additional Analysis** (4–6 rows):

- **Expanded Research** — Topic-by-topic synthesis of key clinical/mechanism studies, each cited with PMID. Black-skin-specific research called out separately if any exists.
- **Formulation Concerns** — Bulleted, priority-labeled (which is highest-priority, which is medium). Actionable, not abstract.
- **Efficacy on Black Hair and Skin** — Trial representation %, race-stratified data, formulation compatibility with Type 3/4 hair or deeply pigmented skin (ingredient-level inference), scalp/skin disease considerations (seborrheic dermatitis, scalp psoriasis, PIH, CCCA, melasma).
- **Black-Owned Business?** — Yes / No / Unconfirmed + basis.
- **Certified Cruelty-Free?** — Yes / No / Unverified + which certifying body checked.
- **Certified Vegan?** — Yes / No + named animal-origin ingredients if any.

**Ingredient tables** (three of them, all required):

- **Table 2A — Ingredient Safety Database Summary**: one row per ingredient (actives first, then inactives in label order). Columns: Ingredient | EWG Skin Deep | WIMJ Assessment | SkinSafe | FDA / Regulatory Flags. Real database values, not "consult sources."
- **Table 2B — Ingredients Grouped by INCI Category**: Solvents/Vehicles, Surfactants, Emollients, Humectants, Fragrance/Essential Oils, Preservatives, pH Adjusters, Active(s), Antioxidants, Thickeners, etc. Omit categories that don't apply.
- **Table 2C — Allergen Summary**: regulated allergens only (FDA Big 9 food, EU Annex III fragrance, IFRA-restricted sensitizers). Omit only if the formulation contains zero regulated allergens; in that case state so explicitly.

**BONUS TRACK — Sources Reviewed**: every URL cited in the analysis plus supporting references, **categorized**: Regulatory/FDA, EU Regulatory, Ingredient Databases, Clinical Research, Black Hair and Skin Research, Safety/Sensitization, Pricing/Patient Assistance, Certifications. A flat list of URLs is insufficient.

### Research Sourcing Rules
- Use up-to-date ingredient lists from official product sources when a URL is provided.
- Perform individual ingredient research across EWG, WIMJ, SkinSafe, FDA MedWatch, and credible journals.
- Do NOT rely solely on training data for ingredient or safety information.
- Prioritize structured regulatory, efficacy, and safety data — especially for underrepresented populations.
- Use web search tools to verify current ingredient lists, FDA status, and safety databases.

---

## Output 2: Product Card

### Audience and Voice
- Written for a **Black woman consumer**.
- Style: plain, respectful, practical. No jargon. No chemistry lessons.
- Tone: objective, educational. Never promotional or commercial.
- Focus on real-world safety, efficacy, and usability for Black skin and textured/protective hairstyles.

### Cardinal Rules
- No redundancy across sections.
- Short paragraphs; concise bullet points where needed.
- Links appear ONLY in the "Data Sources to Consider" section as plain-text URLs.
- Do NOT explain functional inactives unless they impact safety, tolerability, efficacy, or use.
- Center practical concerns related to lived experience with Black skin and textured/protective styles.
- **NEVER provide advice on how to use or apply the product.** Always instruct users to follow the instructions on the product label. This rule exists to keep WeSeeColor out of dosing/application guidance — the label is the authoritative source.
- **Assume the user is an adult** and assume **no prior knowledge** of clinical trials, ingredient databases, or pharmacology. Don't reference studies/trials/papers by phrases that presume the user has heard of them ("not enough Black participants were in the studies" → wrong, the user has not been told about any studies). Rephrase to be self-contained: "There is limited published research on how this product performs for Black skin."
- **Match language confidence to the rating.** WeSeeColor performs the analysis — once we assign a rating, the recommendation language must own that conclusion. Hedge words on a high rating signal we don't trust our own work.
  | Safety rating | Approved phrasing | Avoid |
  |---|---|---|
  | 5 (Very Low Risk) | "This product is safe…" | "appears to be safe", "seems safe" |
  | 4 (Low Risk) | "This product is generally safe…" | "appears to be safe", "should be safe" |
  | 3 (Moderate Risk) | "This product should be generally safe…" | "is generally safe" (overclaim), "may be unsafe" (underclaim) |
  | 2 (High Risk) | "Caution is recommended with this product…" | hedged or generic "be careful" |
  | 1 (Very High Risk) | "We do not recommend this product without medical supervision." | euphemisms |
  Same principle applies to the Safety Rating rationale paragraph in the **full analysis** (Output 1's Table A). Confidence of language tracks confidence of rating.
- **Center the Black audience in research statements.** When citing a study, the Black-skin finding is the subject of the sentence, not a parenthetical aside.
  | Wrong | Right |
  |---|---|
  | "The study found X results, including Y for Black skin." | "The study included [N] Black participants and found that Y." |
  | "Trials showed overall efficacy, with similar results in dark skin tones." | "Among participants with Fitzpatrick IV–VI skin, the trial showed Y." |
  This applies to both Output 1 (Full Product Analysis) and Output 2 (Product Card).

### Product Card Sections (in this exact order)

#### OVERVIEW
Must include all of the following, and nothing else:
- Product name
- Category
- Vehicle/form
- Skin or hair type
- Used for
- Black-owned business: Yes/No
- Certified cruelty-free: Yes/No
- Certified organic: Yes/No

No warnings or ratings in this section.

#### KEY FINDINGS
Exactly two bullets, using the legend's exact label and descriptor:
- **Safety Rating:** [Label] — [Exact descriptor from legend]
- **Research/Data Availability:** [Label] — [Exact descriptor from legend]

No added words, commentary, or explanation.

#### RECOMMENDATION
1–2 short paragraphs:
- **Paragraph 1 — Safety statement.** Paraphrase the safety rating using the **confidence-matched phrasing from the Cardinal Rules table** above. Examples by rating:
  - Rating 4 (Low Risk): "When used as directed, this product is generally safe for most people in its indicated population."
  - Rating 3 (Moderate Risk): "When used as directed, this product should be generally safe for most people, though some users may experience irritation or sensitivity."
  - Rating 2 (High Risk): "Caution is recommended with this product. It may cause irritation or an allergic reaction; talk with a healthcare provider before use."
  Follow with any specific safety issues (allergens, contraindications, flammability) phrased as actionable cautions, then remind the user to follow the label.
- **Paragraph 2 — Efficacy certainty statement.** Paraphrase the Research/Data Availability rating without assuming prior knowledge:
  - Rating 4 (Good) / 5 (Robust): "There is enough published research on this product's use in the Black community to be reasonably confident in how well it works."
  - Rating 3 (Fair): "There is a fair amount of published research on this product's use in the Black community, though some gaps remain."
  - Rating 2 (Limited): "There is limited published research on this product's use in the Black community, so it is harder to be certain about how well it works."
  - Rating 1 (None): "There is no published research on this product's use in the Black community, so its real-world performance for Black skin or hair is unknown."
- **Never** name the numeric rating in the prose (no "Safety Rating: 4", no "this scored a 3"). Paraphrase.
- **Never** assume the reader has seen the analysis. They haven't read about any studies, ingredients, or trials at this point.
- **Never** give directions for application, dosing, frequency, or technique. Tell users to follow the label.

#### FORMULATION CONCERNS (consumer)
Bulleted, actionable items only. In this priority order:
1. Contraindications and toxicities
2. Major allergens with guidance
3. Actionable safety/handling points: sting zones, acne triggers, flammability, hair buildup
4. No in-depth chemistry or routine excipient notes

#### RESEARCH AND INGREDIENT ANALYSIS (consumer)
Bulleted; insights must be plain and user-friendly:
- What the active does, expected relief timelines, application fit, special skin/hair considerations.
- Concerns for sensitive areas or pigmentation risk.
- Suitability for scalp/hair access if applicable.
- Evidence limits where relevant.
- **Clinical trial diversity breakdown** — when clinical trial data exists, break down Black-participant representation **by phase and by RCT**, with the Black participants as the subject of the sentence (per the Cardinal Rule on centering the Black audience):
  > **Good:** "Phase 3 trials included 271 Black participants across two RCTs, where the product showed a 29% improvement rate."
  > **Wrong:** "The phase 3 trials showed 32% efficacy, including some Black participants."
- **Research/Data Availability score derivation.** The rating is set by the percentage of Black participants who received the active drug (i.e., **not** placebo) across all available RCTs. The thresholds reflect that **12–15% is roughly the US Black population share** — a product properly tested for the Black community should at minimum mirror that representation:
  - **1–11%** → Rating 2 (Limited) — below the population-share floor
  - **12–15%** → Rating 3 (Fair) — at or near population share; the expected baseline
  - **>15%** → Rating 4 (Good) or 5 (Robust), depending on total study volume and consistency across trials
  - **Unknown or 0%** → Rating 1 (None) — no basis to assess

#### INGREDIENTS
- List active ingredient with strength.
- Then comma-separated inactives.
- No commentary unless it affects user behavior or safety.

#### DATA SOURCES TO CONSIDER
- 8–14 plain-text URLs only.
- Must include: FDA labels, clinical trials, skin-of-color resources, long-term safety data.
- Minimize marketing sources.

### Quality Checklist (run before delivering a Product Card)
- [ ] Ratings and descriptors match the legend EXACTLY in Key Findings
- [ ] Recommendation paraphrases results — **no numeric rating named in the prose**
- [ ] Recommendation includes both a safety statement AND an efficacy-certainty statement
- [ ] **Recommendation's confidence matches the rating.** A safety rating of 4 or 5 uses "is safe" / "is generally safe", never "appears to be safe". A rating of 3 uses "should be generally safe". Hedge words on high ratings flag a quality failure.
- [ ] **No assumed prior knowledge.** No reference to "studies", "trials", "research papers", or "ingredients" framed as if the user had previously been told about them.
- [ ] **Black audience is the subject** of any research/clinical statement, not a parenthetical aside.
- [ ] Reminder to follow the label is present; no application or dosing instructions
- [ ] No redundancy across sections
- [ ] No unnecessary chemical or mechanistic detail
- [ ] Links appear only in Data Sources to Consider
- [ ] Prior Full Product Analysis exists in conversation

### Update Rules
- Update the card if new FDA safety data or stronger/weaker evidence becomes available.
- Always center the user's lived experience and practical outcomes.
- Always assume the user is an adult.

---

## General Considerations (include when appropriate)

- Dietary supplements can have unexpected interactions with other products, drugs, or conditions. If the product is characterized as a dietary supplement, recommend starting with a small intake and monitoring for potential side or adverse effects, and consulting with a licensed professional before resuming use.
- Allergens may sometimes be listed in labels using their scientific name (e.g., "arachis hypogaea oil" for "peanut oil"). Remind users to familiarize themselves with scientific names of allergens and review labels carefully.

---

## Sample Output

The canonical visual reference is [assets/sample-product-card.pdf](assets/sample-product-card.pdf) (rendered from `renderer/samples/5021.json` — the content-densest sample card that still fits in 3 pages). Open it to see the v1.0 layout, typography, and page-3 legend that every product card produces.

Seven sample cards covering the range of product shapes and content densities live in [renderer/samples/](renderer/samples/) — `5018_card.pdf` through `5024_card.pdf` — alongside their source JSON content files and product PNGs.

---

## Producing the PDF Product Card

The renderer is self-contained inside this plugin at [renderer/](renderer/):

- **[renderer/render_card.py](renderer/render_card.py)** — the renderer. Reads a JSON content file and produces a 3-page A4 PDF via WeasyPrint (pure-Python CSS Paged Media; no browser, no HTTP server — directly deployable to a web backend).
- **[renderer/card_template.html.j2](renderer/card_template.html.j2)** — the Jinja2 HTML template. Bakes in every typographic, geometric, and page-break decision.
- **[renderer/SKELETON.md](renderer/SKELETON.md)** — the geometric and typographic contract the template draws into.
- **[renderer/fonts/](renderer/fonts/)** — embedded fonts (Montserrat for body, Biryani for section headings, Encode Sans Expanded for the footer ribbon, Saira for small annotations).
- **[renderer/pyproject.toml](renderer/pyproject.toml)** — Python dependency manifest read by `uv`. The renderer self-provisions its Python environment (WeasyPrint, Pillow, Jinja2) on first invocation.

### Prerequisites (one-time per machine)

Before invoking the renderer, confirm both of these are installed. The renderer will exit with a clear instruction message if either is missing — but it's faster to set them up once upfront:

| Tool | What it does | Install |
|---|---|---|
| **uv** | Python package + runtime manager. Provisions an isolated venv with WeasyPrint, Pillow, and Jinja2 on first run. | `brew install uv` (macOS), `pipx install uv`, or see [uv's install docs](https://docs.astral.sh/uv/getting-started/installation/) |
| **Pango / Cairo native libs** | WeasyPrint's rendering engine. Provided as system libraries (not pip packages). | **macOS:** `brew install pango` (also installs cairo, glib, fontconfig as dependencies). The renderer also auto-detects miniforge-supplied libs at `~/miniforge3/lib/` if you already have a conda environment with WeasyPrint installed. **Linux:** `sudo apt install libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 fontconfig` or your distro's equivalent. |

Before generating a card for the first time on a new machine, the agent should verify both are present:

```bash
which uv && uv --version           # expect uv 0.4+ or similar
# render_card.py probes for Pango automatically and prints install
# instructions if not found — no separate check needed
```

### Workflow

**Step 0 — Preflight (run before any analysis).** Before drafting prose or running any database lookups:

1. **Inventory the user's input.** Read the request carefully. Note:
   - What product is being analyzed (name, brand, form).
   - Any URLs the user supplied (product page, label, etc.).
   - **Any files attached to the prompt** — especially images. The user may attach a product image directly.
2. **Read the depth-standard references** (see "Required reading before drafting" above). At minimum open one of the `references/sample-reports/` DOCX files and skim the Coiff Dew HTML so you know what the bar looks like for this run. **Do not skip this step.** Skipping it is the failure mode that produces thin reports.
3. **Decide the `<product-name>` folder slug now** (see "Where outputs land"). Don't wait until after the analysis to pick a name and then re-derive paths.
4. **Create the output folder** at `/Users/josepc/GitHub/weseecolor/outputs/<product-name>/`.
5. **If the user attached a product image, save it immediately** as `<product-name>-product.png` inside that folder. Do not wait until card-generation time — save it before you start drafting the analysis. **Do not ask the user to "send the image"** when they already attached one in the original prompt.

This preflight prevents two failure modes that have already happened in production:
- The agent finishes the analysis, then asks for an image the user already attached.
- The agent writes a thin, generic analysis because it didn't study the sample-reports first.

1. Complete the **Full Product Analysis** (Output 1) in conversation. This step gathers the ingredient-by-ingredient research, FDA / EWG / WIMJ / SkinSafe lookups, clinical trial diversity data, and assigns the Safety and Research / Data Availability ratings (1–5 each). Save the rendered HTML at `outputs/<product-name>/<product-name>-analysis.html` using [references/report-template.html](references/report-template.html) as the starting point (copy the file, replace every `[bracketed placeholder]`).

2. **STOP. Confirmation gate.** Do not proceed to the card. Present the user with:

   - The path to the saved HTML (`outputs/<product-name>/<product-name>-analysis.html`).
   - A one-paragraph summary of what's inside: the two ratings, the top one or two safety flags, and the recommendation gist.
   - These three options, asked explicitly:
     > **(a)** Revise the analysis — tell me what to change.
     > **(b)** Proceed to generate the product card PDF.
     > **(c)** Export the analysis as DOCX via `references/report-template.docx`.

   Wait for the user's choice. Do not start drafting the JSON or rendering the card until the user picks (b). The DOCX export in (c) is *only* produced if the user asks for it — do not auto-generate it.

3. Once the user picks (b), distill the analysis into the **Product Card content** following the "Output 2: Product Card" structure and Cardinal Rules above. Record only the **rating integer** (1–5) in the JSON; the renderer substitutes the label / descriptor / colored circle automatically.

   Asset contract for the product image (if one was attached and saved during preflight Step 0.4):
   - **Transparent background** (real alpha channel). PNGs with a single uniform background color are auto-keyed to transparent as a safety net; PNGs with photo or multi-color backgrounds will render as-is with the background visible.
   - **At least ~600 px on the longest side** to print sharp inside the 60 mm slot at 300 DPI.
   - The product cropped reasonably tight within its frame.

   If no image was provided, **omit `image_src` from the JSON entirely** — do not fabricate a path, do not point at a file you haven't saved. The renderer collapses the right-side slot cleanly when `image_src` is absent.

4. Write the JSON content file at `outputs/<product-name>/<product-name>-content.json`. Use [renderer/samples/5021.json](renderer/samples/5021.json) as the canonical template — it exercises every field. Schema:

   ```json
   {
     "product": {
       "name":            "ZORYVE (roflumilast) topical foam 0.3%",
       "category":        "Rx, topical prescription product",
       "form":            "Foam (pressurized can)",
       "skin_hair_type":  "Suitable for diverse skin and hair types, including tightly coiled/textured hair.",
       "used_for":        "Inflammation, scaling, redness, and itch associated with seborrheic dermatitis ...",
       "black_owned":     "No",
       "cruelty_free":    "No",
       "organic":         "No",
       "image_src":       "/Users/josepc/GitHub/weseecolor/outputs/zoryve foam 0.3 seborrheic dermatitis/zoryve foam 0.3 seborrheic dermatitis-product.png"
     },
     "safety":   { "rating": 4 },
     "research": { "rating": 2 },
     "recommendation":       ["First paragraph...", "Second paragraph..."],
     "active_ingredients":   "Roflumilast 0.3% (PDE4 inhibitor).",
     "inactive_ingredients": "Ceteareth-10 phosphate; cetearyl phosphate; ...",
     "formulation_concerns": ["Bullet 1.", "Bullet 2.", "..."],
     "research_analysis":    ["Bullet 1.", "Bullet 2.", "..."],
     "data_sources":         [
       "FDA Prescribing Information (2025): https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/217242s005lbl.pdf",
       "STRATUM Phase 3 trial (PubMed): https://pubmed.ncbi.nlm.nih.gov/38253129/"
     ],
     "last_reviewed":        "September 2025"
   }
   ```

   **Field notes:**
   - `image_src` accepts an **absolute path** (recommended when working out of `outputs/`) or a path relative to the renderer's base directory (where `render_card.py` lives).
   - `data_sources` entries are `"description: URL"` strings. The renderer splits each into a two-line block: description on line 1, hyperlinked URL on line 2.
   - `safety.rating` and `research.rating` are integers 1–5. The renderer maps to label + color + descriptor from the legend tables in `render_card.py`.

5. Generate the PDF. The output filename mirrors the folder name as `outputs/<product-name>/<product-name>-card.pdf`. uv reads `renderer/pyproject.toml`, provisions a venv with the right deps on first call, and reuses it on subsequent calls:

   ```bash
   cd /Users/josepc/GitHub/weseecolor/skills/weseecolor-pharma/renderer
   uv run render_card.py \
     "/Users/josepc/GitHub/weseecolor/outputs/<product-name>/<product-name>-content.json" \
     "/Users/josepc/GitHub/weseecolor/outputs/<product-name>/<product-name>-card.pdf"
   ```

   On a fresh machine, the first invocation downloads Python 3.11+ and the three Python dependencies (~80MB cached under `~/.local/share/uv/`). Subsequent runs are immediate.

   Side effects of running the renderer:
   - Creates a `prepared/` subdirectory (cached background-keyed copies of product images that needed transparency rescue). Safe to delete; will rebuild on next run.
   - Creates a `.venv/` subdirectory (uv's environment). Gitignored.
   - Emits a stderr warning if the input product image has no real transparency and the corner-key heuristic couldn't rescue it. Non-blocking — the PDF still renders, but the product will appear with its source-PNG background visible.
   - Exits with a clear install message if Pango / Cairo native libraries can't be found — re-run after `brew install pango` (or the Linux equivalent).

6. Spot-check the output:
   - **3 pages** is the target for every product. All 7 sample cards (5018–5024) hit 3 pages, including content-dense Eucrisa with 12+ data-source URLs and a 9-bullet formulation-concerns list.
   - **4+ pages** indicates the product has unusually long content (rare). If it appears, check whether bullet lists or the data-sources list could be trimmed without losing substance.
   - Product image center aligns with the WSC logo center on the vertical axis (the renderer's geometric skeleton guarantees this for any image aspect ratio).
   - Rating circle colors match the rating numbers (1=red through 5=dark green).
   - All ratings descriptors match the legend exactly — they come from the renderer's `SAFETY_LEGEND` / `RESEARCH_LEGEND` tables, not the JSON.

### Reference + regression fixtures

- **[renderer/SKELETON.md](renderer/SKELETON.md)** — v1.0 typographic scale, geometric anchors, page-break behavior. Any future template change should land here as a one-paragraph entry describing what moved and why.
- **[references/](references/)** — visual + content regression targets and source-of-truth documents (see [references/README.md](references/README.md)):
  - `references/sample-cards/` — the 7 Canva-produced PDFs the renderer was built to reproduce. Compare against `renderer/samples/<sid>_card.pdf` for parity after any template change.
  - `references/sample-reports/` — DOCX exemplars of completed Output 1 analyses (5020–5024). Use as content + tone reference when writing new analyses.
  - `references/report-template.docx` — blank scaffold for new Output 1 deliverables.
  - `references/rating-legend.md` — textual source of truth for the rating scales. Must stay in sync with `renderer/render_card.py`'s `SAFETY_LEGEND` / `RESEARCH_LEGEND` constants.

  **Do not read `references/history/`.** That folder holds predecessor-workflow documents (the prior Canva-based card pipeline, original ChatGPT prompts) preserved only for archival purposes. They describe a workflow that no longer exists and reading them will produce wrong outputs.
