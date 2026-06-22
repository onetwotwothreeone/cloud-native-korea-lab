# 09_GWAN_Simulation_To_Interface_Payload_Integration

## Purpose

This step connects GWAN simulation logic and GWAN scoring logic.

Before this step, the simulation could create payload data while scoring tests existed separately. That was useful, but it created a risk: simulation output and scoring rules could drift apart.

This step makes the relationship explicit:

```text
simulated object
→ GWANScoringCase
→ GWANScoringDecision
→ spatial/sidebar/alert/uncertainty/report packages
```

## Why this matters

HYEAN needs GWAN outputs that are not only valid JSON but also logically connected to scoring and decision rules.

The HYEAN Operator Interface should not receive manually guessed recommended actions. It should receive actions produced by the same scoring pathway used in tests.

## New endpoint

```text
POST /gwan/simulate-integrated
```

This endpoint returns both:

```text
payload
object_decisions
```

The `payload` is what the HYEAN Operator Interface would consume.
The `object_decisions` list is for debugging, review, and tests.

## Object flow

Each `SimulatedGWANObject` includes:

- object identity
- position
- display category
- confidence label
- data classification
- scoring inputs
- uncertainty type, if needed
- interpretation summary
- follow-up observation

Then it is converted into a `GWANScoringCase`.

The scoring rule returns:

- scores
- recommended_action
- alert_level
- reason_summary
- needs_uncertainty_record

That decision becomes the source for the final interface packages.

## Integrated simulation objects

| Object ID | Meaning | Expected action |
|---|---|---|
| candidate-resource-stable-001 | Strong low-risk resource candidate | send_micro_probe |
| risk-radiation-critical-001 | Critical radiation region | avoid |
| candidate-ice-weak-signal-001 | Weak icy candidate with uncertainty | observe_more |
| nav-reference-stable-001 | Stable navigation reference | update_survival_map |

## Payload packages generated

```text
spatial_visualization_package
sidebar_intelligence_package
alert_feed_package
uncertainty_package
decision_report_package
```

## Completion criteria

- Every simulated object is scored through the shared scoring rule.
- Spatial marker actions match scoring decisions.
- High-risk objects generate risk alerts.
- Weak-signal objects generate uncertainty records.
- The sidebar selects the strongest non-risk candidate.
- The full payload passes the GWANInterfacePayload validation model.

## Next recommended step

The next step is:

```text
10_GWAN_Memory_Map_Update_Model
```

That step should define how GWAN stores observations, scores, decisions, uncertainty, and map updates after a payload is generated.
