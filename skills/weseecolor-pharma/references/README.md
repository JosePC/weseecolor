# References — `weseecolor-pharma`

Materials that ground the plugin in its real-world outputs. None of these are *runtime* inputs to the renderer or the skill — they're test fixtures, source-of-truth documents, and historical context.

## Layout

```
references/
├── README.md                ← this file
├── rating-legend.md         ← the textual safety + research/data-availability rating legend
├── report-template.docx     ← blank DOCX scaffold for new Output 1 analyses
├── sample-cards/            ← 7 Canva-produced reference PDFs (5018–5024)
├── sample-reports/          ← 5 DOCX exemplars of Output 1 analyses
└── history/                 ← DO NOT READ — predecessor-workflow docs (Canva
                               template field-names, original ChatGPT prompts)
                               kept for archive only. The workflows they
                               describe no longer exist.
```

## What each piece is for

### `rating-legend.md`
The canonical textual definition of both rating scales (Safety 1–5, Research/Data Availability 1–5) with exact labels and descriptors. The runtime legend lives in `../renderer/render_card.py` as `SAFETY_LEGEND` and `RESEARCH_LEGEND` — those two **must stay in sync** with this document. If you ever change one, change the other.

### `report-template.docx`
The blank Word scaffold the team used for new Output 1 (Full Product Analysis) deliverables. Open it as a starting point when authoring a new analysis; the structure aligns with the "Required Structure" section in `../SKILL.md`.

### `sample-cards/`
The 7 original Canva-produced PDF cards that the v1.0 renderer was designed to reproduce visually. Use these as **visual regression targets** — when changing the template or renderer, open the corresponding `../renderer/samples/<sid>_card.pdf` next to the Canva original and confirm parity (typography, geometry, page-3 legend, ribbon placement).

| File | Product | Renderer counterpart |
|---|---|---|
| `5018 - …` | Hyper Skin Vitamin C Serum | `../renderer/samples/5018_card.pdf` |
| `5019 - …` | Rose Ingleton FutureBright | `../renderer/samples/5019_card.pdf` |
| `5020 - …` | Zoryve cream 0.15% — atopic dermatitis | `../renderer/samples/5020_card.pdf` |
| `5021 - …` | Zoryve foam 0.3% — seborrheic dermatitis | `../renderer/samples/5021_card.pdf` |
| `5022 - …` | Zoryve cream 0.3% — plaque psoriasis | `../renderer/samples/5022_card.pdf` |
| `5023 - …` | Zoryve foam 0.3% — plaque psoriasis | `../renderer/samples/5023_card.pdf` |
| `5024 - …` | Eucrisa — atopic dermatitis | `../renderer/samples/5024_card.pdf` |

### `sample-reports/`
DOCX exemplars of completed Output 1 (Full Product Analysis) deliverables for 5020 through 5024. Use these as **content + tone references** when writing a new analysis — depth of ingredient research, structure of the Safety Profile, how the clinical trial diversity breakdown is presented, etc.

### `history/` — DO NOT READ
Predecessor-workflow documents kept only for archival reasons:

- `canva-template.md` — the prior card-production workflow used Canva templates with named fields populated via bulk upload / MCP. The plugin no longer goes through Canva — `renderer/` produces PDFs natively. Reading this file will lead to wrong outputs (e.g., it includes a "Vegan" field that the renderer doesn't support).
- `pharma-researcher-chatgpt.md` — the predecessor prompt from the ChatGPT iteration of this work.

These describe workflows that no longer exist. They're preserved purely as context for why the active SKILL.md is shaped the way it is. **Do not use them as runtime references.**

## Regression smoke-test workflow

When the renderer or template changes, the quickest way to confirm nothing regressed:

```bash
cd ../renderer
rm -rf prepared/
for sid in 5018 5019 5020 5021 5022 5023 5024; do
  ~/miniforge3/bin/python3 render_card.py samples/${sid}.json samples/${sid}_card.pdf
done
```

Then visually compare each `samples/<sid>_card.pdf` against the matching `references/sample-cards/<sid> - … .pdf` for parity on geometry, type, and page-3 legend. All 7 must render at 3 pages and pair Inactive ingredients label with its content on the same page.
