# 37_GWAN_Kubernetes_ServiceAccount_RBAC_Baseline

## Purpose

This step adds dedicated Kubernetes ServiceAccounts and minimal RBAC baseline for GWAN.

The goal is to avoid using the default ServiceAccount and to keep Kubernetes API permissions intentionally minimal.

## Beginner Summary

ServiceAccount is like a Pod identity card.

RBAC is like a permission table.

In this step:

- GWAN API gets its own identity: gwan-api-sa
- PostgreSQL gets its own identity: gwan-postgres-sa
- Both identities receive no extra Kubernetes API permissions
- ServiceAccount token automount is disabled

## Why This Matters

A Pod should not automatically receive unnecessary Kubernetes API access.

Even if the application is compromised, it should not easily use Kubernetes credentials.

This is a least-privilege baseline.

## HYEAN/GWAN Prevention Meaning

For HYEAN/GWAN, RBAC is preventive identity control.

It reduces the chance that one compromised workload can expand into the Kubernetes control plane.

## Current Policy

GWAN API:

- ServiceAccount: gwan-api-sa
- Role: gwan-api-minimal-role
- rules: []
- automountServiceAccountToken: false

PostgreSQL:

- ServiceAccount: gwan-postgres-sa
- Role: gwan-postgres-minimal-role
- rules: []
- automountServiceAccountToken: false

## Check Commands

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/rbac_check.sh

## Expected Result

ServiceAccounts should exist:

- gwan-api-sa
- gwan-postgres-sa

Deployments should use those ServiceAccounts.

Token automount should be false.
