# 58_GWAN_Kubernetes_StatefulSet_Migration_Command_Dry_Run

## Purpose

Migration Command Dry Run

This document defines a dry-run command plan for a future PostgreSQL Deployment to StatefulSet migration.

This step does not execute real migration.

This step only validates that the migration commands are prepared, ordered, and safe to review.

## HYEAN/GWAN Safety Principle

HYEAN is a prevention-first survival intelligence service.

GWAN must protect memory, continuity, and operator trust.

A database migration must never be executed by surprise.

Before any real migration, commands must be reviewed in dry-run form.

## Current Decision State

CURRENT_DECISION=NO_GO

APPROVED_BY_OPERATOR=false

FINAL_DECISION=NO_GO

## Current Workload State

- PostgreSQL is still running as Deployment.
- PostgreSQL Pod is running.
- PostgreSQL PVC exists and is Bound.
- PostgreSQL Service exists.
- PostgreSQL Secret exists.
- GWAN API ConfigMap exists.
- No active PostgreSQL StatefulSet exists yet.

## Dry-Run Command Plan

The future migration should be reviewed in this order:

1. Confirm current PostgreSQL health.
2. Confirm backup/restore baseline.
3. Render StatefulSet draft.
4. Dry-run StatefulSet draft apply.
5. Confirm approval gate.
6. Confirm execution plan.

## Dry-Run Commands

kubectl -n hyean-gwan get deployment postgres

kubectl -n hyean-gwan get pods -l app.kubernetes.io/name=gwan-postgres

kubectl -n hyean-gwan get pvc postgres-data

kubectl -n hyean-gwan get svc postgres

kubectl -n hyean-gwan get secret gwan-postgres-secret

scripts/k8s/postgres_backup_restore_check.sh

kubectl kustomize k8s/drafts

kubectl apply --dry-run=client -f k8s/drafts/postgres-headless-service-draft.yaml

kubectl apply --dry-run=client -f k8s/drafts/postgres-statefulset-draft.yaml

scripts/k8s/statefulset_operator_approval_gate_check.sh

scripts/k8s/statefulset_final_go_nogo_decision_check.sh

scripts/k8s/statefulset_approved_migration_execution_plan_check.sh

## Explicit Non-Goals

Do not execute real migration in this step.

Do not create a live PostgreSQL StatefulSet in this step.

Do not delete the current PostgreSQL Deployment in this step.

Do not modify the existing PostgreSQL PVC in this step.

Do not switch database traffic in this step.

## Result

The migration command dry-run plan is documented.

The system remains safe.

The current final decision remains NO_GO.

## Next Recommended Step

59_GWAN_Kubernetes_StatefulSet_Migration_Command_Review
