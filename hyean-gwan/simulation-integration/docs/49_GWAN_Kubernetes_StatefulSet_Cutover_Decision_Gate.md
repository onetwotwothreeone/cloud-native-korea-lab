# 49_GWAN_Kubernetes_StatefulSet_Cutover_Decision_Gate

## Purpose

Cutover Decision Gate

This document defines the GO / NO-GO decision gate before moving GWAN PostgreSQL from the current Deployment + PVC baseline toward a future StatefulSet migration path.

This step does not execute real StatefulSet migration.

## HYEAN/GWAN Safety Position

HYEAN is a prevention-first survival intelligence service.

GWAN must protect memory, observation continuity, and operator trust before changing infrastructure.

Because PostgreSQL is the current memory layer, the migration must remain blocked unless backup, restore, rollback, PVC, Service, Secret, ConfigMap, and operator approval conditions are all satisfied.

## Current Expected State

- PostgreSQL is still Deployment.
- PostgreSQL Pod is running.
- PostgreSQL PVC is Bound.
- PostgreSQL Service exists.
- PostgreSQL Secret exists.
- GWAN API ConfigMap exists.
- No active PostgreSQL StatefulSet exists yet.
- Real StatefulSet migration is not executed in this step.

## Required Inputs Before GO

- Backup/restore baseline exists.
- StatefulSet draft manifest exists.
- Migration dry-run document exists.
- Migration runbook exists.
- Rollback dry-run document exists.
- Cutover checklist exists.
- Operator approval template exists.
- Manual approval record exists.
- Operator approval gate exists.
- Pre-migration final check exists.

## Decision

CURRENT_DECISION=NO_GO

APPROVED_BY_OPERATOR=false

FINAL_DECISION=NO_GO

## Why NO-GO

This step is a decision gate, not an execution step.

The safe default is NO_GO until the operator manually approves the migration and all required safety records are complete.

## Safety Rule

Do not execute real migration in this step.

Do not create a live PostgreSQL StatefulSet in this step.

Do not delete the current PostgreSQL Deployment in this step.

Do not modify the existing PostgreSQL PVC in this step.

## Next Recommended Step

50_GWAN_Kubernetes_StatefulSet_Cutover_Approval_Record
