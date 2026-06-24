# 38_GWAN_Kubernetes_SecurityContext_Baseline

## Purpose

This step adds Kubernetes SecurityContext baseline settings for GWAN.

The goal is to reduce unnecessary container privileges before they become security or operational risks.

## Beginner Summary

SecurityContext is like a safety belt for a Pod or Container.

It controls how strongly a container can act inside Linux.

## Current Baseline

GWAN API:

- runAsNonRoot: true
- runAsUser: 1000
- runAsGroup: 1000
- fsGroup: 1000
- seccompProfile: RuntimeDefault
- allowPrivilegeEscalation: false
- privileged: false
- readOnlyRootFilesystem: true
- capabilities.drop: ALL
- /tmp is mounted as emptyDir because the app may need temporary write space

PostgreSQL:

- fsGroup: 999
- seccompProfile: RuntimeDefault
- allowPrivilegeEscalation: false
- privileged: false
- readOnlyRootFilesystem: false
- capabilities.drop: ALL

## Why PostgreSQL Root Filesystem Is Not Read Only Yet

PostgreSQL is a database workload.

It needs writable storage.

For this baseline, the database keeps writable filesystem behavior while reducing unnecessary privilege escalation and Linux capabilities.

## HYEAN/GWAN Prevention Meaning

For HYEAN/GWAN, SecurityContext is preventive runtime control.

It reduces the chance that a compromised container can act with excessive Linux privileges.

## Check Commands

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/security_context_check.sh

## Expected Result

The GWAN API should run with non-root and read-only root filesystem.

PostgreSQL should run with reduced privilege escalation and RuntimeDefault seccomp.
