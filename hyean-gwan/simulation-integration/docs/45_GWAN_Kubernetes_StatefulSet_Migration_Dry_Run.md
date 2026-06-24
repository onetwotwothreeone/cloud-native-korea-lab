# 45. GWAN Kubernetes StatefulSet Migration Dry Run

## Purpose

This step defines a safe dry-run process before migrating GWAN PostgreSQL from Deployment to StatefulSet.

This step does not perform the actual migration.

## Simple Explanation

A database migration is like moving a library.

You should not move the books immediately.

First, you check:

1. Where the books are now
2. Whether the backup exists
3. Whether the new shelf design is correct
4. Whether you can restore the books if something goes wrong

That is the purpose of this dry-run step.

## Current State

GWAN PostgreSQL currently runs as:

- Deployment
- Service
- Secret
- PVC

The StatefulSet draft exists, but it is not applied yet.

## Why We Do Dry Run First

PostgreSQL stores important state.

Changing it from Deployment to StatefulSet affects:

- Pod identity
- PVC naming
- rollout behavior
- backup and restore strategy
- rollback process

So the project must not apply StatefulSet directly.

## Dry Run Checks

The dry-run script checks:

- current PostgreSQL Deployment
- current PostgreSQL Pod
- current PostgreSQL PVC
- current PostgreSQL Service
- current PostgreSQL Secret
- StatefulSet draft render
- backup/restore baseline script
- whether StatefulSet already exists

## Safe Migration Rule

Before real migration:

1. Run backup/restore baseline
2. Confirm backup file exists
3. Confirm temporary restore succeeds
4. Scale down existing PostgreSQL Deployment
5. Apply StatefulSet manifest
6. Confirm PostgreSQL Pod is ready
7. Confirm GWAN API can connect
8. Keep rollback plan ready

## Not Done Yet

This step does not:

- delete the current PostgreSQL Deployment
- apply StatefulSet to the cluster
- move real data into StatefulSet PVC
- change production manifests

## Next Recommended Step

46_GWAN_Kubernetes_StatefulSet_Migration_Runbook
