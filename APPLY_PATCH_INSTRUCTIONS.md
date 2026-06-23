# Apply patch instructions: 33_GWAN_Kubernetes_Metrics_Server_And_HPA_Readiness

```bash
cd ~/Downloads
unzip hyean_gwan_kubernetes_metrics_server_hpa_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_kubernetes_metrics_server_hpa_patch/ ./
cat ~/Downloads/hyean_gwan_kubernetes_metrics_server_hpa_patch/README_33_APPEND.md >> hyean-gwan/simulation-integration/README.md

cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q

kubectl apply -k k8s/overlays/local
scripts/k8s/rollout_check.sh
scripts/k8s/hpa_check.sh
scripts/k8s/metrics_server_check.sh

cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Kubernetes metrics server and HPA readiness"
git push
```
