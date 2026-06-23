
## 30. Kubernetes resource requests and limits

This step adds baseline Kubernetes CPU and memory requests/limits for the GWAN API and PostgreSQL pods.

```text
requests = minimum resources Kubernetes should reserve
limits   = maximum resources the container should be allowed to use
```

Local check:

```bash
cd hyean-gwan/simulation-integration
python -m pytest -q

docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/resource_check.sh
```

This helps GWAN move from "it runs" to "it runs with an explicit resource baseline."
