#!/usr/bin/env bash
set -euo pipefail

echo "Installing Metrics Server for local Kubernetes testing."
echo "This script is intended for local/dev clusters only. Review security flags before production use."

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Docker Desktop / kind frequently need this kubelet TLS flag for local learning environments.
kubectl -n kube-system patch deployment metrics-server --type='json' -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}
]' || true

kubectl -n kube-system rollout status deployment/metrics-server --timeout=180s
kubectl get apiservice v1beta1.metrics.k8s.io
