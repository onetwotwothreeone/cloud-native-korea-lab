# Apply 20_GWAN_Docker_Image_Build_CI patch

Apply this patch from the repository root:

```bash
cd ~/Downloads
unzip hyean_gwan_docker_image_build_ci_patch_2026-06-22.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_docker_ci_patch/ ./
cat ~/Downloads/hyean_gwan_docker_ci_patch/README_20_APPEND.md >> hyean-gwan/simulation-integration/README.md
```

Run local tests:

```bash
cd ~/cloud-native-korea-lab/hyean-gwan/simulation-integration
source .venv/bin/activate
pytest -q
```

Optional local Docker check:

```bash
docker build -t hyean-gwan-simulation:local .
docker run --rm -p 8000:8000 hyean-gwan-simulation:local
```

Commit from repository root:

```bash
cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN Docker image build CI"
git push
```

Confirm in GitHub:

```text
Actions -> GWAN CI -> green check
```
