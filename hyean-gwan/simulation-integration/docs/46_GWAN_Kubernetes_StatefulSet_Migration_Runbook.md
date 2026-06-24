# 46. GWAN Kubernetes StatefulSet Migration Runbook

## Purpose

This document defines the safe migration runbook for moving GWAN PostgreSQL from Deployment + PVC to StatefulSet.

This step creates the runbook only.

It does not execute the real migration.

## Simple Explanation

Migrating PostgreSQL to StatefulSet is like moving an important library to a new building.

You should not just carry the books immediately.

You need a written plan:

1. Check the current library.
2. Make a backup.
3. Test the backup.
4. Stop new changes for a short time.
5. Move carefully.
6. Check the new place.
7. Prepare a rollback plan.

That written plan is this runbook.

## Current Architecture

Current PostgreSQL architecture:

- Deployment: `postgres`
- Service: `postgres`
- Secret: `gwan-postgres-secret`
- PVC: `postgres-data`

Current API architecture:

- Deployment: `gwan-api`
- Service: `gwan-api`
- ConfigMap: `gwan-api-config`

## Target Architecture

Target PostgreSQL architecture later:

- StatefulSet: `postgres`
- Headless Service: `postgres-headless`
- Service: `postgres`
- Secret: `gwan-postgres-secret`
- Persistent storage through StatefulSet volume claim template

## Important Decision

The current baseline keeps PostgreSQL as Deployment.

StatefulSet migration should happen only after:

- backup/restore verification passes
- StatefulSet draft is reviewed
- rollback path is ready
- API connection check is ready
- data loss risk is understood

## Migration Gates

### Gate 1. Test Gate

Required command:

    python -m pytest -q

Expected result:

    all tests passed

### Gate 2. Kubernetes Health Gate

Required commands:

    kubectl -n hyean-gwan get pods
    kubectl -n hyean-gwan get deployment postgres
    kubectl -n hyean-gwan get pvc postgres-data
    kubectl -n hyean-gwan get service postgres
    kubectl -n hyean-gwan get secret gwan-postgres-secret

Expected result:

- postgres Deployment is available
- postgres Pod is Running
- postgres PVC is Bound
- postgres Service exists
- postgres Secret exists

### Gate 3. Backup/Restore Gate

Required command:

    scripts/k8s/postgres_backup_restore_check.sh

Expected result:

- pg_dump backup succeeded
- temporary restore database was created
- backup was restored safely
- temporary restore database was cleaned up
- main database was not overwritten

### Gate 4. StatefulSet Draft Gate

Required command:

    kubectl kustomize k8s/drafts

Expected result:

- StatefulSet draft renders successfully
- Headless Service draft renders successfully
- draft is not applied to the local overlay yet

## Real Migration Plan

This is the future real migration plan.

Do not run this automatically.

### Phase 1. Announce Maintenance Window

Before migration:

- stop write-heavy tests
- avoid schema changes
- avoid manual database updates
- notify that PostgreSQL migration is in progress

### Phase 2. Final Backup

Run:

    scripts/k8s/postgres_backup_restore_check.sh

Then confirm backup file exists in:

    .local/postgres-backups/

### Phase 3. Scale Down API

Purpose:

- prevent new writes during migration

Future command:

    kubectl -n hyean-gwan scale deployment gwan-api --replicas=0

### Phase 4. Scale Down PostgreSQL Deployment

Future command:

    kubectl -n hyean-gwan scale deployment postgres --replicas=0

### Phase 5. Apply StatefulSet Manifest

Future command:

    kubectl apply -k k8s/overlays/local

This should only happen after the StatefulSet manifest is intentionally added to the local overlay.

### Phase 6. Verify PostgreSQL StatefulSet

Future commands:

    kubectl -n hyean-gwan get statefulset postgres
    kubectl -n hyean-gwan get pods -l app.kubernetes.io/name=gwan-postgres
    kubectl -n hyean-gwan get pvc

Expected result:

- StatefulSet exists
- postgres Pod is Running
- PVC is Bound

### Phase 7. Restore Data If Needed

If migration creates a new empty database, restore from the latest backup.

Future restore command must be reviewed before execution.

### Phase 8. Scale API Back Up

Future command:

    kubectl -n hyean-gwan scale deployment gwan-api --replicas=1

### Phase 9. Verify API

Future commands:

    kubectl -n hyean-gwan port-forward svc/gwan-api 8000:8000
    curl http://127.0.0.1:8000/health

Expected result:

    {"status":"ok"}

## Rollback Plan

Rollback is required before real migration.

If StatefulSet migration fails:

1. Stop API traffic.
2. Scale down or remove the failed StatefulSet.
3. Restore the previous PostgreSQL Deployment manifest.
4. Reuse the previous PVC if safe.
5. Restore from backup if data is missing.
6. Scale API back up.
7. Verify API health.

Rollback should be tested in a separate dry-run before production use.

## Stop Conditions

Stop the migration immediately if:

- backup fails
- restore verification fails
- PVC is not Bound
- StatefulSet draft does not render
- PostgreSQL Pod enters CrashLoopBackOff
- API cannot connect to PostgreSQL
- rollback command is unclear

## Safety Rule

Never do database migration without a verified backup.

## Not Done In This Step

This step does not:

- apply StatefulSet
- delete PostgreSQL Deployment
- move live data
- restore production data
- change active database workload

## Next Recommended Step

47_GWAN_Kubernetes_StatefulSet_Migration_Rollback_Dry_Run
