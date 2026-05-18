# Outputs

This directory is where the `weseecolor-pharma` skill writes its deliverables — one subfolder per product.

## Convention

```
outputs/
└── <product-name>/
    ├── <product-name>-content.json     ← JSON content file passed to the card renderer
    ├── <product-name>-product.png      ← the product image (transparent-background PNG)
    ├── <product-name>-card.pdf         ← rendered 3-page A4 card (Output 2)
    └── <product-name>-analysis.html      ← Full Product Analysis (Output 1), if produced
                                            (.docx export optional via references/report-template.docx)
```

### Folder naming

`<product-name>` is **lowercase, spaces preserved**, dropping parenthetical scientific names and other noise. The goal is a short, human-recognizable label:

| Source product name | Folder name |
|---|---|
| Hyper Skin — Hyper Even Brightening Dark Spot Vitamin C Serum | `hyper skin vitamin c serum` |
| ZORYVE (roflumilast) topical cream 0.15% for atopic dermatitis | `zoryve cream 0.15 atopic dermatitis` |
| Eucrisa (crisaborole) for atopic dermatitis | `eucrisa atopic dermatitis` |
| Coiff Dew Natural Shampoo | `coiff dew` |

Filesystem-unsafe characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) get dropped or replaced with hyphens. Trailing punctuation gets trimmed.

### File naming inside the folder

Mirror the folder name as a prefix so a single file shared out of context is still recognizable. E.g., `outputs/coiff dew/coiff dew-card.pdf` exports as a self-describing `coiff dew-card.pdf`.

## Why outputs/ isn't tracked in git

Generated cards and analyses are personal work products, not source. They can be large (5MB+ each for a PDF, multi-MB for DOCX), they may contain in-progress drafts you don't want under public history, and they're fully regenerable from the source JSON content file plus the renderer.

`outputs/` is in `.gitignore`. Only this `README.md` is tracked, to keep the directory present in the repo structure.

If you ever want to share a specific deliverable, copy the file out of `outputs/` to wherever you want it distributed. If you want to start tracking outputs in git for a specific project, edit the root `.gitignore` to remove the `outputs/` rule.
