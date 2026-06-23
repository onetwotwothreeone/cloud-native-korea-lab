# Apply 30_GWAN_Kubernetes_Resource_Requests_And_Limits patch

Run from your Mac terminal:

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_resources_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_resources_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_resources_patch/README_30_APPEND.md >> hyean-gwan/simulation-integration/README.md
```

Then test:

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
```

Optional local Kubernetes check:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/resource_check.sh
```

Commit:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes resource requests and limits"
git push
```
