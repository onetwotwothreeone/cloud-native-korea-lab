# 26_GWAN_Kubernetes_CI_With_Kind

## Purpose

This step moves Kubernetes validation from the local Mac into GitHub Actions.

Previous step:

```text
Docker Desktop Kubernetes local run
```

This step:

```text
GitHub Actions
→ create a temporary kind Kubernetes cluster
→ build the GWAN Docker image
→ load the image into kind
→ apply k8s/overlays/local
→ verify /health and /gwan/memory/db-status
```

## Why kind?

`kind` means Kubernetes IN Docker. It creates a temporary Kubernetes cluster by running Kubernetes nodes as Docker containers.

This is useful for CI because the workflow can create a clean disposable Kubernetes cluster, test manifests, and delete the cluster after the run.

## What the CI now checks

```text
Python tests
Docker image build
single-container /health smoke test
Docker Compose API + PostgreSQL integration
kind Kubernetes cluster creation
Docker image loaded into kind
kubectl apply -k k8s/overlays/local
PostgreSQL rollout
GWAN API rollout
port-forward /health
port-forward /gwan/memory/db-status
Kubernetes diagnostics on failure
kind cluster cleanup
GHCR image push on main branch
```

## Key workflow details

The workflow installs kind directly from the official release binary:

```bash
curl -Lo ./kind "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-amd64"
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Then it creates a cluster:

```bash
kind create cluster --name hyean-gwan-ci --wait 120s
```

Then it builds and loads the image:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kind load docker-image ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest --name hyean-gwan-ci
```

Then it applies the local overlay:

```bash
kubectl apply -k k8s/overlays/local
```

The local overlay is used because CI loads the image directly into kind, so Kubernetes should use the loaded local node image instead of pulling from GHCR.

## Expected result

GitHub Actions should show GWAN CI as green.

The important step names are:

```text
Create kind cluster
Build and load image into kind
Apply Kubernetes local overlay in kind
Kubernetes API health check through port-forward
Delete kind cluster
```

## Current limitation

This does not test a production overlay with private GHCR pull secrets yet.

It validates the Kubernetes manifests and local overlay inside a disposable CI Kubernetes cluster.

A later step can add production overlay validation with imagePullSecrets or a public package strategy.
