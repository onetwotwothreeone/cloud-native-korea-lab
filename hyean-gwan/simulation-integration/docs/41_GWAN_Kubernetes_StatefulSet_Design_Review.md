# 41. GWAN Kubernetes StatefulSet Design Review

## Purpose

This document reviews whether GWAN PostgreSQL should remain as a Deployment with a PersistentVolumeClaim, or move to a StatefulSet.

At the current learning and local Kubernetes stage, GWAN uses:

- Deployment
- PersistentVolumeClaim
- ClusterIP Service
- Secret
- ConfigMap
- Resource requests and limits
- NetworkPolicy
- ServiceAccount and RBAC
- SecurityContext

This is enough for a local baseline because the goal is to learn Kubernetes persistence safely before introducing StatefulSet complexity.

## Simple Explanation

A Deployment is like a flexible worker manager.

It is good for stateless applications such as API servers.

A StatefulSet is like a hotel room assignment manager.

It gives each Pod a stable name, stable identity, and stable storage relationship.

For a database, this can be important because the database needs stable storage and predictable identity.

## Current GWAN PostgreSQL Decision

For now, GWAN PostgreSQL stays as a Deployment with a PVC.

Reason:

1. The project is still in local Kubernetes baseline stage.
2. There is only one PostgreSQL replica.
3. The main goal is to verify persistence, config, secret, security, network policy, and rollout behavior.
4. A StatefulSet migration should be done after the baseline is stable.

## When GWAN Should Move to StatefulSet

GWAN should consider StatefulSet when:

- PostgreSQL needs stable Pod identity
- Persistent data must be tied more strictly to a specific Pod identity
- database failover or replica design is introduced
- backup and restore workflow becomes part of the platform
- production-grade database architecture is designed

## Current Baseline

Current baseline:

- PostgreSQL runs as a Deployment
- PostgreSQL uses postgres-data PersistentVolumeClaim
- PostgreSQL has resource requests and limits
- PostgreSQL has SecurityContext
- PostgreSQL has NetworkPolicy
- PostgreSQL has ServiceAccount and minimal RBAC

## Future Direction

The next possible step is:

42_GWAN_Kubernetes_StatefulSet_Migration_Plan

This should not be rushed.

Before migration, the project should define:

- backup strategy
- restore strategy
- storage class behavior
- local and production differences
- whether PostgreSQL should be managed inside Kubernetes or provided by a cloud database service

## Portfolio Meaning

This step shows that the project does not blindly add Kubernetes objects.

Instead, it explains why a certain Kubernetes workload type is selected.

This is important for cloud-native portfolio quality because production architecture is not only about making things run.

It is also about explaining why the design is safe, simple, and appropriate for the current stage.
