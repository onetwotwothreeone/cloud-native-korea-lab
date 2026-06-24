# 42. GWAN Kubernetes StatefulSet Migration Plan

## Purpose

This document defines a safe migration plan for moving GWAN PostgreSQL from Deployment + PVC to StatefulSet later.

This step does not apply StatefulSet yet.

The goal is to prepare a careful migration path before changing the database workload type.

## Simple Explanation

A database is like a library archive.

The API server can be replaced easily, but the database must protect its records.

A Deployment is good for replaceable workers.

A StatefulSet is better for workloads that need stable identity and storage.

So PostgreSQL should eventually move toward StatefulSet, but only after backup, restore, rollback, and storage behavior are clearly prepared.

## Current State

GWAN currently uses:

- PostgreSQL Deployment
- postgres-data PersistentVolumeClaim
- postgres ClusterIP Service
- gwan-postgres-secret
- gwan-api-config ConfigMap
- NetworkPolicy
- ServiceAccount and RBAC
- SecurityContext
- Resource requests and limits
- PodDisruptionBudget
- HPA for GWAN API

This is the current safe local baseline.

## Migration Goal

The future goal is to migrate PostgreSQL to:

- StatefulSet
- stable Pod identity
- stable volume claim template
- predictable database service name
- clear backup and restore workflow
- rollback plan

## Migration Principles

1. Do not lose database data.
2. Do not change too many things at once.
3. Keep API connection behavior predictable.
4. Verify backup before migration.
5. Verify restore before migration.
6. Keep rollback path ready.
7. Separate local Kubernetes behavior from production behavior.

## Required Checklist Before Migration

Before converting PostgreSQL to StatefulSet, the project should confirm:

- Current PostgreSQL data can be backed up.
- Backup file can be restored into a fresh PostgreSQL instance.
- Existing PVC behavior is understood.
- StorageClass behavior is understood.
- Service name remains stable.
- Secret and ConfigMap values remain compatible.
- NetworkPolicy still allows GWAN API to access PostgreSQL.
- SecurityContext still works with PostgreSQL image permissions.
- Rollback plan is documented.

## Proposed Migration Steps

### Step 1. Backup existing PostgreSQL data

Create a database dump from the current PostgreSQL Pod.

Expected tool:

- pg_dump

### Step 2. Create StatefulSet manifest separately

Do not replace the existing Deployment immediately.

First create a draft StatefulSet manifest and test it separately.

### Step 3. Test restore into StatefulSet PostgreSQL

Start the StatefulSet in a controlled environment and restore the backup.

### Step 4. Verify GWAN API connection

Confirm that GWAN API can connect to the StatefulSet-backed PostgreSQL Service.

### Step 5. Switch traffic only after verification

Only after data and connectivity are verified, switch the active PostgreSQL workload.

### Step 6. Keep rollback plan

If StatefulSet migration fails, return to the previous Deployment + PVC baseline.

## Local vs Production Note

In local Kubernetes, this migration is for learning and architecture practice.

In production, PostgreSQL may be better managed by a cloud database service such as:

- Amazon RDS
- Google Cloud SQL
- Azure Database for PostgreSQL

Running PostgreSQL inside Kubernetes requires careful operational responsibility.

## Current Decision

Do not migrate yet.

The next recommended step is:

43_GWAN_Kubernetes_PostgreSQL_Backup_Restore_Baseline

Backup and restore should come before StatefulSet conversion.

## Portfolio Meaning

This migration plan shows that GWAN is being built with production thinking.

The project is not just adding Kubernetes objects.

It is learning how to protect data, plan migrations, and explain architecture decisions.
