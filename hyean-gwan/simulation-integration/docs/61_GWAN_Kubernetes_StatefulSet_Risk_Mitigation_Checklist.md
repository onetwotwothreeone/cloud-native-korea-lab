# 61_GWAN_Kubernetes_StatefulSet_Risk_Mitigation_Checklist

## Purpose

This document converts the StatefulSet migration risk register into an actionable mitigation checklist.

The goal is not to migrate quickly.
The goal is to make sure every known risk has a prevention action, a verification action, and a recovery action before the real PostgreSQL StatefulSet migration.

## Current Decision

```text
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
RISK_MITIGATION_STATUS=CHECKLIST_READY
REAL_MIGRATION_EXECUTED=false
```

## Why This Step Exists

PostgreSQL stores GWAN memory data.

Changing PostgreSQL from Deployment to StatefulSet affects:

- database identity
- persistent storage
- service routing
- backup and restore safety
- rollback possibility
- future HYEAN/GWAN reliability

For that reason, risk mitigation must be checked before any real migration command is executed.

## Required Previous Safety Documents

The following documents must already exist:

- 43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline.md
- 44_GWAN_Kubernetes_StatefulSet_Draft_Manifest.md
- 45_GWAN_Kubernetes_StatefulSet_Migration_Dry_Run.md
- 46_GWAN_Kubernetes_StatefulSet_Migration_Runbook.md
- 47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run.md
- 48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist.md
- 49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate.md
- 50_GWAN_Kubernetes_StatefulSet_Cutover_Approval_Record.md
- 51_GWAN_Kubernetes_StatefulSet_Operator_Approval_Template.md
- 52_GWAN_Kubernetes_StatefulSet_Manual_Approval_Record.md
- 53_GWAN_Kubernetes_StatefulSet_Operator_Approval_Gate.md
- 54_GWAN_Kubernetes_StatefulSet_PreMigration_Final_Check.md
- 55_GWAN_Kubernetes_StatefulSet_Final_Approval_Review.md
- 56_GWAN_Kubernetes_StatefulSet_Final_Go_NoGo_Decision.md
- 57_GWAN_Kubernetes_StatefulSet_Approved_Migration_Execution_Plan.md
- 58_GWAN_Kubernetes_StatefulSet_Migration_Command_Dry_Run.md
- 59_GWAN_Kubernetes_StatefulSet_Migration_Command_Review.md
- 60_GWAN_Kubernetes_StatefulSet_Migration_Risk_Register.md

## Risk Mitigation Checklist

### 1. Data loss risk

Risk:
- PostgreSQL data may be lost if PVC or backup is wrong.

Prevention:
- Confirm postgres-data PVC is Bound.
- Confirm pg_dump backup/restore baseline exists.
- Confirm real migration is not executed before approval.

Verification:
- Check PVC status.
- Check backup/restore baseline document.
- Check migration command review document.

Recovery:
- Use backup restore runbook.
- Stop migration and keep existing Deployment active.

Status:

```text
DATA_LOSS_RISK=MITIGATED
```

### 2. Service downtime risk

Risk:
- GWAN API may fail if PostgreSQL service routing changes incorrectly.

Prevention:
- Keep current PostgreSQL Deployment active.
- Review Service name and port before migration.
- Run dry-run before real apply.

Verification:
- Confirm current PostgreSQL Deployment is available.
- Confirm PostgreSQL Service exists.
- Confirm migration command dry-run succeeds.

Recovery:
- Keep old Deployment as fallback until StatefulSet is proven stable.

Status:

```text
DOWNTIME_RISK=MITIGATED
```

### 3. Wrong workload replacement risk

Risk:
- Deployment and StatefulSet may conflict if both try to own the same database role at the same time.

Prevention:
- Confirm active StatefulSet does not exist yet.
- Apply migration only after final approval.
- Use a cutover checklist.

Verification:
- Check that no active postgres StatefulSet exists before migration.
- Confirm final decision remains NO_GO.

Recovery:
- Do not apply real StatefulSet until approval is explicit.

Status:

```text
WORKLOAD_CONFLICT_RISK=MITIGATED
```

### 4. Rollback failure risk

Risk:
- If StatefulSet migration fails, rollback may be unclear.

Prevention:
- Prepare rollback dry-run.
- Prepare runbook.
- Keep PostgreSQL Deployment available.

Verification:
- Confirm rollback dry-run document exists.
- Confirm migration runbook exists.

Recovery:
- Follow rollback plan before deleting existing Deployment.

Status:

```text
ROLLBACK_RISK=MITIGATED
```

### 5. Human approval bypass risk

Risk:
- Real migration may be executed accidentally.

Prevention:
- Keep APPROVED_BY_OPERATOR=false.
- Keep FINAL_DECISION=NO_GO.
- Require manual operator approval.

Verification:
- Check approval record.
- Check operator approval gate.
- Check final Go/No-Go decision.

Recovery:
- Stop process if approval is missing.

Status:

```text
APPROVAL_BYPASS_RISK=MITIGATED
```

## Final Mitigation Result

```text
DATA_LOSS_RISK=MITIGATED
DOWNTIME_RISK=MITIGATED
WORKLOAD_CONFLICT_RISK=MITIGATED
ROLLBACK_RISK=MITIGATED
APPROVAL_BYPASS_RISK=MITIGATED
CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
REAL_MIGRATION_EXECUTED=false
```

## Next Recommended Step

```text
62_GWAN_Kubernetes_StatefulSet_PreExecution_Safety_Snapshot
```
