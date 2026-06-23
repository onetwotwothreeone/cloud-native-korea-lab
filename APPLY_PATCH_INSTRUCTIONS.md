# Apply patch: 27_GWAN_Kubernetes_Production_GHCR_Pull

Apply from repository root.

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_production_ghcr_pull_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_production_ghcr_pull_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_production_ghcr_pull_patch/README_27_APPEND.md >> hyean-gwan/simulation-integration/README.md
```

Run tests:

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
```

Commit and push:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes production GHCR pull"
git push
```

Check GitHub Actions:

```text
Actions → GWAN CI → green check
```
