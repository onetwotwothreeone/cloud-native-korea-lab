# 48. GWAN Kubernetes StatefulSet Migration Cutover Checklist

## Purpose

This document defines the final pre-cutover checklist before migrating GWAN PostgreSQL from Deployment + PVC to StatefulSet.

This step does not execute the real cutover.

## Simple Explanation

Cutover means switching from the old running database shape to the new database shape.

It is like moving from a temporary clinic room to a permanent operating room.

Before that move, we must check:

- the current system is healthy
- the backup exists
- restore was tested
- rollback is prepared
- the new StatefulSet draft is ready
- the migration is still not executed accidentally

## Current Active Baseline

The current active PostgreSQL workload is still:

- Deployment: `postgres`
- Service: `postgres`
- PVC: `postgres-data`
- Secret: `gwan-postgres-secret`

## Required Pre-Cutover Conditions

Before real migration, all of these must be true:

1. pytest passes
2. GitHub Actions passes
3. PostgreSQL Deployment is available
4. PostgreSQL Pod is running
5. PostgreSQL PVC is Bound
6. PostgreSQL Service exists
7. PostgreSQL Secret exists
8. ConfigMap exists
9. pg_dump backup check passed
10. temporary restore check passed
11. StatefulSet draft renders successfully
12. rollback dry run passed
13. real StatefulSet is not active yet
14. API health check passed before migration
15. migration decision is explicitly approved by the operator

## No-Go Conditions

Do not proceed to real migration if:

- pytest fails
- GitHub Actions fails
- PostgreSQL Pod is not Running
- PVC is not Bound
- backup/restore check has not passed
- rollback dry run has not passed
- StatefulSet draft does not render
- current API is already unhealthy
- data loss risk is unclear
- the operator has not explicitly approved cutover

## Cutover Safety Rule

The real migration must not happen automatically.

The operator must make a manual GO or NO-GO decision.

## What This Step Creates

This step creates:

- cutover checklist document
- cutover checklist script
- tests that protect the no-automatic-migration rule

## What This Step Does Not Do

This step does not:

- create a real StatefulSet
- delete PostgreSQL Deployment
- delete PVC
- restore into the main database
- change live database ownership
- perform real migration

## Result

After this step, the project has a final pre-cutover gate.

## Next Recommended Step

49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate
