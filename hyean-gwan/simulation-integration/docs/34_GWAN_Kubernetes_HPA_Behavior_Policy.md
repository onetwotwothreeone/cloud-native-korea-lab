# 34_GWAN_Kubernetes_HPA_Behavior_Policy

## Purpose

This step makes GWAN API autoscaling safer and more predictable.

The previous HPA baseline defined when GWAN API should scale based on CPU usage.
This step defines how fast GWAN API is allowed to scale up or scale down.

## Beginner Summary

HPA is like a middle manager for Pods.

Without behavior policy, HPA can react too aggressively.
With behavior policy, HPA follows controlled rules.

- scaleUp: add Pods carefully when load increases
- scaleDown: remove Pods slowly after the system becomes stable

## Current Policy

scaleUp:
  stabilizationWindowSeconds: 60
  policies:
    - type: Pods
      value: 1
      periodSeconds: 60

scaleDown:
  stabilizationWindowSeconds: 300
  policies:
    - type: Pods
      value: 1
      periodSeconds: 120

## Meaning

GWAN API may add up to 1 Pod every 60 seconds when demand increases.

GWAN API may remove up to 1 Pod every 120 seconds, but only after a 300 second stabilization window.

## Why This Matters for HYEAN/GWAN

GWAN is a decision and memory engine.
A decision engine should not be unstable.

Autoscaling must support reliability, not just speed.

## Check Commands

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/hpa_check.sh
scripts/k8s/hpa_behavior_check.sh

## Expected Result

The HPA should include:

- minReplicas: 1
- maxReplicas: 3
- averageUtilization: 70
- scaleUp behavior
- scaleDown behavior
