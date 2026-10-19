# 0019. Animal photo result states its confidence

- Status: Decided
- Decided by: Chandan
- Date: 2026-10-06

## Context
How the app speaks about identification.

## Decision
The app states confidence explicitly, for example: "I can say with 59% confidence that it is not venomous." It always advises a hospital visit.

## Consequences
The confidence value must be calibrated and evaluated, not made up by the model. See open question.
