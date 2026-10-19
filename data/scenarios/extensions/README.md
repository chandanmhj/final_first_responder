# Adding rare conditions

Use this folder to add a rare emergency without touching the core files.

1. Copy `_template_module.yaml` to `module_<id>.yaml` and write the steps. Every step must say where it comes from
   (`source`: handbook, adapted or extension), and extension steps need a reviewer.
2. Copy `_template_condition.yaml` to `condition_<id>.yaml` to say which modules it uses, which roles and locations are
   valid, what hospital it needs, and which tags it must never contain.
3. Run `python scripts/expand_scenarios.py`. It fails if the new scenario contains a forbidden tag or an unknown module.

## Rules for sensible additions (so nothing illogical is added)
- Reuse existing modules (scene safety, call for help, CPR, transport) instead of rewriting them.
- Do not add a step that contradicts a conflict rule in `composition_rules.yaml`.
- Each step must make sense for the role that sees it. A step needing a second person is not shown to the patient.
- Remove any step that does not apply to the combination (for example, no log roll for a non-trauma condition).
- No medicine doses unless a trained clinician has approved the step, and those steps are shown to responders only.
- Put the new topic in `docs/data/gaps.md` until a reviewer signs off.
