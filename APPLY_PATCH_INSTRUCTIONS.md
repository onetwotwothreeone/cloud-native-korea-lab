# Apply 31_GWAN_Kubernetes_Namespace_ResourceQuota_And_LimitRange

Run from your repository root.

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_namespace_policy_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_namespace_policy_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_namespace_policy_patch/README_31_APPEND.md >> hyean-gwan/simulation-integration/README.md
```

Then test:

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
```

Then apply locally:

```bash
docker build -t ghcr.io/onetwotwothreeone/hyean-gwan-simulation:latest .
kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/namespace_policy_check.sh
```

Commit:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes namespace resource policies"
git push
```
