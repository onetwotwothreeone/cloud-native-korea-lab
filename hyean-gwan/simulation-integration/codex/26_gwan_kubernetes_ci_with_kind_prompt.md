# Codex task: 26_GWAN_Kubernetes_CI_With_Kind

## Goal

Add GitHub Actions validation for Kubernetes manifests using a temporary kind cluster.

## Required workflow behavior

- Install kind in GitHub Actions.
- Create a kind cluster.
- Build the GWAN Docker image.
- Load the Docker image into kind.
- Apply `k8s/overlays/local`.
- Wait for `postgres` and `gwan-api` rollouts.
- Port-forward `svc/gwan-api`.
- Check `/health` and `/gwan/memory/db-status`.
- Dump Kubernetes diagnostics if any step fails.
- Delete the kind cluster in an `always()` cleanup step.

## Required files

```text
.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/.github/workflows/gwan-ci.yml
hyean-gwan/simulation-integration/docs/26_GWAN_Kubernetes_CI_With_Kind.md
hyean-gwan/simulation-integration/tests/test_gwan_kubernetes_kind_ci.py
```

## Success command

```bash
python -m pytest -q
```

After push, confirm that GitHub Actions shows GWAN CI as green.
