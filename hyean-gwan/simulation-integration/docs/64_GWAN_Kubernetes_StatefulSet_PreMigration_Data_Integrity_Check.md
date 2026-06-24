# 64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check

## PreMigration Data Integrity Check

## Purpose

This document defines the pre-migration data integrity check before moving GWAN PostgreSQL from Deployment + PVC toward a StatefulSet-based design.

## Current Decision

CURRENT_DECISION=NO_GO
APPROVED_BY_OPERATOR=false
FINAL_DECISION=NO_GO
DATA_INTEGRITY_STATUS=REVIEW_ONLY
READ_ONLY_CHECK=true
REAL_MIGRATION_EXECUTED=false
SECRET_VALUES_EXPORTED=false

## Safety Position

This step does not execute real migration.

This step only checks whether the current PostgreSQL database can be reached, queried, and reviewed before migration.

## What This Step Checks

- PostgreSQL Deployment is available
- PostgreSQL Pod is Running
- postgres-data PVC is Bound
- PostgreSQL Service exists
- PostgreSQL Secret metadata exists
- GWAN API ConfigMap exists
- latest backup file exists
- database readiness check works
- database name can be queried
- public schema table count can be queried
- read-only integrity report can be generated
- secret values are not exported
- real migration remains blocked

## Why This Matters

A StatefulSet migration changes how PostgreSQL is managed by Kubernetes.

Before changing the workload type, we must confirm that the current database is readable and that its state is recorded.

In HYEAN/GWAN terms, this protects the memory layer before changing the memory container.

## Expected Result

- PostgreSQL remains Deployment + PVC
- no active PostgreSQL StatefulSet exists yet
- read-only database checks pass
- integrity report is created
- real migration is not executed
- next step can be planned safely

## Next Recommended Step

65_GWAN_Kubernetes_StatefulSet_PreMigration_Readiness_Summary
