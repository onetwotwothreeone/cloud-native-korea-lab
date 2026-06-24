# 36_GWAN_Kubernetes_NetworkPolicy_Baseline

## Purpose

This step adds baseline Kubernetes NetworkPolicy rules for GWAN.

The goal is to reduce unnecessary Pod-to-Pod communication before it becomes an operational risk.

## Beginner Summary

NetworkPolicy is like a security gate between Pods.

Before this step, Pods may be able to talk too freely depending on the cluster network plugin.

After this step, GWAN communication becomes more intentional.

## Current Policy

GWAN API:

- allows ingress on TCP 8000
- allows egress to PostgreSQL on TCP 5432
- allows DNS egress on TCP/UDP 53

GWAN PostgreSQL:

- allows ingress only from GWAN API on TCP 5432

## HYEAN/GWAN Prevention Meaning

This is not only a security step.

For HYEAN/GWAN, NetworkPolicy is preventive infrastructure.

It reduces unnecessary communication paths before they become risk paths.

## Important Note

NetworkPolicy requires a Kubernetes network plugin that supports enforcement.

Some local environments may accept the NetworkPolicy resource but may not actually block traffic.

That is acceptable for this baseline documentation and CI check step.

## Check Commands

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/network_policy_check.sh

## Expected Result

NetworkPolicies should exist:

- gwan-api-network-policy
- gwan-postgres-network-policy
