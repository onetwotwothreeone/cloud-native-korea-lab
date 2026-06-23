# Apply 26_GWAN_Kubernetes_CI_With_Kind patch

Run from your repository root.

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_kind_ci_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_kind_ci_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_kind_ci_patch/README_26_APPEND.md >> hyean-gwan/simulation-integration/README.md

cd hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q

cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes CI with kind"
git push
```

Then check:

```text
GitHub → Actions → GWAN CI → green check
```
