# Apply 25_GWAN_Kubernetes_Overlays_Local_And_Production patch

Run from your Mac terminal:

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_overlays_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_overlays_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_overlays_patch/README_25_APPEND.md >> hyean-gwan/simulation-integration/README.md

cd hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
```

Recommended local Kubernetes check:

```bash
kubectl kustomize k8s/overlays/local
scripts/k8s/apply_local.sh
scripts/k8s/status.sh
scripts/k8s/port_forward_health_check.sh
```

Then commit from the repository root:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes local and production overlays"
git push
```
