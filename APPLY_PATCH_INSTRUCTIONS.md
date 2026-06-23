# Apply patch: 23_GWAN_Kubernetes_Manifests

Apply this patch from the repository root.

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_manifests_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_manifests_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_manifests_patch/README_23_APPEND.md >> hyean-gwan/simulation-integration/README.md

cd hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
```

Then commit from the repository root.

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes manifests"
git push
```
