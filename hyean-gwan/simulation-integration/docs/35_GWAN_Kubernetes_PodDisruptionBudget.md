# 35_GWAN_Kubernetes_PodDisruptionBudget

## Purpose

This step adds a PodDisruptionBudget for the GWAN API.

The goal is to protect GWAN API availability during voluntary Kubernetes disruptions.

## Beginner Summary

A PodDisruptionBudget is like a minimum staffing rule.

Even if Kubernetes is doing maintenance, moving Pods, or draining a node, this rule says:

"At least 1 GWAN API Pod should remain available."

## Current Policy

minAvailable: 1

## What This Means

GWAN API should keep at least 1 available Pod during voluntary disruption.

If there is only 1 GWAN API Pod running, Kubernetes may report:

ALLOWED DISRUPTIONS: 0

This is not an error.

It means Kubernetes is saying:

"I cannot safely evict this Pod right now because then GWAN API would have no available Pod."

## Why This Matters for HYEAN/GWAN

GWAN is the observation, scoring, decision, and memory engine.

A decision engine should not disappear during maintenance.

This PDB adds one more reliability rule:

- HPA controls how many Pods should exist.
- PDB controls how many Pods should remain available during voluntary disruption.

## Check Commands

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/pdb_check.sh

## Expected Result

The PDB should exist:

NAME           MIN AVAILABLE
gwan-api-pdb   1

If replicas are only 1, allowed disruptions may be 0.
That is expected.
