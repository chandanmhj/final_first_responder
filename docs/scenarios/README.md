# Scenarios

How the emergency flows are built. The full list is in `catalog.md` (generated).

## Why modules
Writing every scenario separately would repeat the same steps and create contradictions. Instead there are 39 modules
(for example `scene_safety`, `cpr_adult`, `aed`, `bleeding_control`, `helmet_removal`) and rules that join them.

## Examples (as you described)
| Situation | Scenario id | What it contains |
|---|---|---|
| Heart attack | `heart_attack__home` | call for help, heart attack steps, transport |
| Heart attack on the road (journey) | `heart_attack__road_journey_vehicle` | pull over safely and scene safety first, then the heart attack steps |
| Road accident, car occupant | `road_car_conscious__road_accident_scene` | road hazards, scene safety, patient placement, neck stabilisation, bleeding, transport |
| Road accident, rider with helmet | `road_bike_helmet__road_accident_scene` | scene safety, neck stabilisation, helmet removal, log roll, transport |
| Road accident, not breathing | `road_not_breathing_car__road_accident_scene` | scene safety, assessment, CPR, AED, transport |

## Roles
The same scenario gives different steps to a bystander, the patient themselves, and a trained first responder.

## What "makes sense" means here
Combinations are filtered so illogical ones are never generated:
- A condition lists only the locations where it can happen (no drowning on a railway, no road accident at home).
- Steps tagged for a group (trauma, cardiac) appear only in those scenarios (no log roll in a heart attack).
- Conflict rules remove contradictions (no recovery position in cardiac arrest, no tourniquet for a snake bite,
  no aspirin in a stroke, nothing by mouth to an unconscious person). See `data/scenarios/composition_rules.yaml`.
- A patient cannot do CPR on themselves, so those scenarios list only bystander and responder.

## Step source labels
`handbook` (with page), `adapted`, `extension` (needs expert review).
