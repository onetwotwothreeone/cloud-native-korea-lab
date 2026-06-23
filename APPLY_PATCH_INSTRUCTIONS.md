# Apply patch: 29_GWAN_Kubernetes_Health_Readiness_And_Observability_Baseline

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_observability_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_observability_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_observability_patch/README_29_APPEND.md >> hyean-gwan/simulation-integration/README.md

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
```

Commit:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes observability baseline"
git push
```
