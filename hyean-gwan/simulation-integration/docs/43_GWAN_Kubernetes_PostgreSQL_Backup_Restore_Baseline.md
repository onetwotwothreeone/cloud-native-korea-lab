# 43. GWAN Kubernetes PostgreSQL Backup/Restore Baseline

## Purpose

This document defines the first backup and restore baseline for GWAN PostgreSQL running on Kubernetes.

This step comes before StatefulSet migration.

## Simple Explanation

A database is like the project memory box.

Before changing the box itself, we must prove that we can copy the memory out and put it back safely.

That is why backup and restore must come before StatefulSet migration.

## Current PostgreSQL State

GWAN currently uses:

- PostgreSQL Deployment
- postgres-data PersistentVolumeClaim
- postgres ClusterIP Service
- gwan-postgres-secret
- gwan-api-config ConfigMap

This is enough for local Kubernetes learning, but database safety requires backup and restore practice.

## Backup Strategy

The baseline backup uses `pg_dump`.

Expected behavior:

1. Find the running PostgreSQL Pod.
2. Run `pg_dump` inside the PostgreSQL container.
3. Save the dump file under `.local/postgres-backups`.
4. Keep backup files out of Git.

## Restore Strategy

The baseline restore check does not overwrite the main database.

Instead, it creates a temporary restore database:

- hyean_gwan_restore_check

Then it restores the dump into that temporary database.

After the check, it deletes the temporary database.

## Why Restore Check Matters

A backup is not proven until restore works.

A file that looks like a backup is not enough.

The project must verify that the backup can actually be restored.

## Safety Rule

Do not restore directly into the main database during this baseline step.

Use a temporary restore database first.

## Relationship to StatefulSet

StatefulSet migration should happen only after:

- backup works
- restore works
- rollback plan exists
- storage behavior is understood

## Next Recommended Step

44_GWAN_Kubernetes_StatefulSet_Draft_Manifest

After backup and restore are proven, the project can safely draft a StatefulSet manifest.
