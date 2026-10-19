# data/scenarios/

The emergency knowledge is built from small reusable **modules** (a list of steps), joined into **scenarios** by rules.

```
data/scenarios/
├── modules/              one YAML per module (steps, roles, source, page, tags, quick-reply hints)
├── conditions.yaml       condition -> modules, roles, valid locations, facility needs, forbidden tags
├── locations.yaml        location -> hazard and scene-safety modules added first
├── composition_rules.yaml  ordering, role filtering and the conflict rules
├── extensions/           your additions for rare situations (see extensions/README.md)
└── generated/scenarios.yaml  all expanded scenarios (generated, do not edit)
```

A scenario id is `<condition>__<location>`, for example `heart_attack__road_journey_vehicle`
or `road_not_breathing_car__road_accident_scene`.

## Roles
- **B** bystander, **S** self (the patient), **R** first responder (trained). Each step lists the roles that see it.
- Pulse checks, rescue breaths, bag valve mask and medication steps are for **R** only.

## Step source labels
- `handbook`: taken from the handbook (page number given).
- `adapted`: based on the handbook but reworded or restructured for the app (for example for a role).
- `extension`: not in the handbook. **Needs expert review before use.**

## Regenerating
```
python scripts/expand_scenarios.py
```
This validates every scenario (unknown modules, forbidden tags) and rebuilds `generated/scenarios.yaml`,
`docs/scenarios/catalog.md` and `media/manifest.yaml`. `media/replace.md` is only rebuilt with `--overwrite-replace`,
because it holds your ticks.
