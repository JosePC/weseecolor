# Canva Product Card Template Reference

## Template Details
- **Name**: Claude Product Card Importer template
- **Design ID**: `DAHJeD_mmng`
- **Short link**: https://canva.link/l98e3t48qz5j7co
- **Edit URL**: https://www.canva.com/design/DAHJeD_mmng/KcSEH2Q35KQZeA6xTW_GQw/edit

## Bulk Upload / MCP Field Names

These are the exact named fields in the Canva template. Field names must match exactly when using bulk upload CSV or Canva MCP editing operations.

### Page 1 — Overview
| Field Name | Notes |
|---|---|
| `Product name` | Full product name including brand |
| `Category` | e.g., "Rx topical", "Skin care", "Hair care" |
| `Vehicle/form` | e.g., "Ointment 2%", "Serum", "Custard" |
| `Skin or hair type` | Target skin/hair type |
| `Used for` | Indication or purpose |
| `Black-owned business` | "Yes" / "No" — may include brief detail |
| `Certified cruelty-free` | "Yes" / "No" |
| `Certified organic` | "Yes" / "No" |
| `Vegan` | "Yes" / "No" (include if applicable) |

### Page 1 — Key Findings
| Field Name | Notes |
|---|---|
| Safety label | Text label: "Very High Risk" / "High Risk" / "Moderate Risk" / "Low Risk" / "Very Low Risk" |
| Safety descriptor | Exact descriptor from rating legend |
| Research label | Text label: "None" / "Limited" / "Fair" / "Good" / "Robust" |
| Research descriptor | Exact descriptor from rating legend |
| `RECommendation` | Full recommendation paragraphs (exact field name as shown in template) |

### Page 1–2 — Supporting Data and Analysis
| Field Name | Notes |
|---|---|
| `Active ingredients` | Active ingredient(s) with strength |
| `Inactive ingredients` | Comma-separated inactive ingredients |
| `Formulation concerns` | Bulleted list |
| `Research and ingredient analysis` | Bulleted list |
| `Data sources to consider` | 8–14 plain-text URLs with brief citation labels |
| `Last reviewed` | Month Year (e.g., "October 2025") |

### Page 3 — Static
Page 3 is the rating legend. It never changes and is not populated per product.

## Rating Badge Color Rules

The colored circle badges on page 1 (Key Findings) are fixed graphic elements. Color and number are inseparable — never mix them.

### Safety Rating
| Score | Label | Circle Color |
|---|---|---|
| 1 | Very High Risk | Red |
| 2 | High Risk | Orange-red |
| 3 | Moderate Risk | Amber/orange |
| 4 | Low Risk | Olive/yellow-green |
| 5 | Very Low Risk | Green |

### Research / Data Availability Rating
| Score | Label | Circle Color |
|---|---|---|
| 1 | None | Red |
| 2 | Limited | Orange-red |
| 3 | Fair | Amber/orange |
| 4 | Good | Olive/yellow-green |
| 5 | Robust | Green |

## Product Image
The product image sits in the top-right of page 1 (Overview section). It must be provided separately:
- **Via URL**: Claude can upload it directly to Canva using the MCP upload-asset-from-url tool
- **Manually**: User inserts/replaces the image in Canva after card generation

## Workflow (Canva MCP)
1. Duplicate the template using `create-design-from-candidate` or equivalent
2. Open editing transaction with `start-editing-transaction`
3. Populate all text fields via `perform-editing-operations`
4. Upload product image via `upload-asset-from-url` (if URL provided)
5. Commit with `commit-editing-transaction`
6. Export as PDF via `export-design`
