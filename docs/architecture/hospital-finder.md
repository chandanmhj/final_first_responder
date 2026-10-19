# Hospital finder

Status: **in scope (Decided).** The data source is **Open.**

The handbook stresses transport to an *appropriate* facility, not just the nearest one:
| Emergency | Facility needs (from the handbook) |
|---|---|
| Heart attack | clot-dissolving medicine, stenting or bypass surgery |
| Cardiac arrest | ICU and cardiac catheterisation |
| Stroke | CT scan, ideally a stroke unit |
| Trauma and severe bleeding | a surgeon available |
| Snake bite | hospital immediately |
| Animal bite | rabies and tetanus vaccination centre |

Each condition in `data/scenarios/conditions.yaml` carries a `facility_requirements` text. The finder should rank hospitals by
distance **and** whether they meet that requirement.

## Open
- Where hospital locations and capabilities come from. Map services give locations but usually not capabilities
  (cath lab, stroke unit), so a curated table may be needed. See OPEN_QUESTIONS.md.
- How the user's location is obtained (browser location permission).
