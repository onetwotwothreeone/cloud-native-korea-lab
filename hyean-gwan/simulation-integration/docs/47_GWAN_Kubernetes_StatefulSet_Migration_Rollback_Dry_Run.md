# 47. GWAN Kubernetes StatefulSet Migration Rollback Dry Run

## Purpose

This document defines a dry-run rollback plan for GWAN PostgreSQL StatefulSet migration.

This step does not execute the real rollback.

It only checks whether rollback preparation is clear and safe.

## Simple Explanation

Database migration is like moving a hospital medicine storage room.

Before moving, we must know how to return to the original room if something goes wrong.

Rollback dry run means:

- we do not actually move the database
- we do not delete the current database
- we do not apply StatefulSet
- we only check whether the return path is ready

## Current Safe Baseline

Current active PostgreSQL workload is:

- Deployment: `postgres`
- Service: `postgres`
- PVC: `postgres-data`
- Secret: `gwan-postgres-secret`

Current inactive draft assets are:

- StatefulSet draft
- Headless Service draft

## Rollback Dry Run Checks

The rollback dry run checks:

1. current PostgreSQL Deployment exists
2. current PostgreSQL Pod is Running
3. current PVC is Bound
4. current Service exists
5. current Secret exists
6. StatefulSet draft can render
7. active PostgreSQL StatefulSet does not exist yet
8. backup/restore baseline script exists
9. migration runbook exists
10. rollback commands are documented but not executed

## Future Real Rollback Flow

If real StatefulSet migration fails later, rollback should follow this order:

1. Stop API writes.
2. Scale down failed StatefulSet.
3. Restore PostgreSQL Deployment manifest.
4. Confirm PVC and data path.
5. Restore from backup if needed.
6. Scale PostgreSQL Deployment back up.
7. Scale API back up.
8. Verify API health.
9. Verify database connection.
10. Record incident notes.

## Commands That Must Not Run In This Step

This step must not run:

- `kubectl delete statefulset`
- `kubectl scale statefulset`
- `kubectl apply` for real migration
- `pg_restore` against the main database
- destructive PVC commands

## Stop Conditions

Stop immediately if:

- backup file is missing
- restore check has never passed
- current PVC is not Bound
- current PostgreSQL Deployment is not available
- rollback command is unclear
- API health check is failing before migration

## Safety Rule

A rollback plan is not optional.

For database migration, rollback is part of the design.

## Result

After this step:

- rollback dry run document exists
- rollback dry run script exists
- tests protect the safety rule
- real migration is still not executed

## Next Recommended Step

48_GWAN_Kubernetes_StatefulSet_Migration_Cutover_Checklist
