# 63_GWAN_Kubernetes_StatefulSet_Backup_Freshness_Check

## Purpose

This document defines the Backup Freshness Check before PostgreSQL StatefulSet migration.

The goal is to confirm that a recent PostgreSQL backup exists before any real migration is considered.

## Why this matters

PostgreSQL stores important stateful data.

Before changing PostgreSQL from Deployment + PVC to StatefulSet, we must confirm that a usable backup exists.

This step protects HYEAN/GWAN from accidental data loss.

## Backup Freshness Check

The system must confirm:

- latest backup file exists
- backup age is within acceptable window
- PostgreSQL Deployment is currently available
- PostgreSQL Pod is running
- PostgreSQL PVC is Bound
- PostgreSQL Secret exists
- GWAN API ConfigMap exists
- active PostgreSQL StatefulSet does not exist yet
- real migration is still blocked
- secret values are not exported

## Current safety rule

BACKUP_MAX_AGE_SECONDS=86400

This means the latest backup must be less than or equal to 24 hours old.

## Decision state

CURRENT_DECISION=NO_GO  
APPROVED_BY_OPERATOR=false  
FINAL_DECISION=NO_GO  
BACKUP_FRESHNESS_STATUS=REVIEW_ONLY  
REAL_MIGRATION_EXECUTED=false  

## Safety result

This step does not execute real migration.

This step only checks backup freshness readiness.

## Next Recommended Step

64_GWAN_Kubernetes_StatefulSet_PreMigration_Data_Integrity_Check
