# Apply patch: 28_GWAN_Kubernetes_Production_Secrets_And_Config

Run from your repository root:

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_secrets_config_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_secrets_config_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_secrets_config_patch/README_28_APPEND.md >> hyean-gwan/simulation-integration/README.md
```

Then test:

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
kubectl kustomize k8s/overlays/local
kubectl kustomize k8s/overlays/production
```

Commit:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes secrets and config split"
git push
```
