# Codex task: 09_GWAN_Simulation_To_Interface_Payload_Integration

## Goal

Connect GWAN simulation logic to GWAN scoring logic so that simulation output is generated from the same scoring rules used in tests.

## Required flow

```text
SimulatedGWANObject
→ GWANScoringCase
→ recommend_action()
→ GWANScoringDecision
→ GWANInterfacePayload packages
```

## Files to create or update

```text
app/services/gwan_simulation.py
app/services/gwan_scoring.py
app/api/routes_gwan.py
tests/test_gwan_simulation_integration.py
docs/09_GWAN_Simulation_To_Interface_Payload_Integration.md
README.md
```

## Required endpoint

```text
POST /gwan/simulate-integrated
```

## Required tests

- simulation generates valid interface payload
- every simulated object uses shared scoring rule
- spatial recommended_action matches scoring decision
- high-risk objects generate risk alerts
- weak-signal objects generate uncertainty records
- sidebar selects strongest non-risk candidate

## Success command

```bash
pytest -q
```
