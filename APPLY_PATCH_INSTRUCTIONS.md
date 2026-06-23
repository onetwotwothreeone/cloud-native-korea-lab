# Apply 21_GWAN_Docker_Compose_CI patch

Apply this patch from the repository root:

```bash
cd ~/Downloads
unzip hyean_gwan_docker_compose_ci_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_docker_compose_ci_patch/ ./
cat ~/Downloads/hyean_gwan_docker_compose_ci_patch/README_21_APPEND.md >> hyean-gwan/simulation-integration/README.md
```

Run local tests:

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q
```

Optional local Docker Compose check:

```bash
docker compose -f docker-compose.ci.yml up -d --build
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/gwan/memory/db-status
docker compose -f docker-compose.ci.yml down -v --remove-orphans
```

Commit from repository root:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Docker Compose CI"
git push
```

Confirm in GitHub:

```text
Actions -> GWAN CI -> green check
```
