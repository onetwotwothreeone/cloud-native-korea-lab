# Apply 22_GWAN_GHCR_Image_Push patch

Run from your Mac terminal.

```bash
cd ~/Downloads
unzip hyean_gwan_ghcr_image_push_patch_2026-06-23.zip

cd ~/cloud-native-korea-lab
rsync -av ~/Downloads/hyean_gwan_ghcr_image_push_patch/ ./
cat ~/Downloads/hyean_gwan_ghcr_image_push_patch/README_22_APPEND.md >> hyean-gwan/simulation-integration/README.md

cd hyean-gwan/simulation-integration
source .venv/bin/activate
python -m pytest -q

cd ~/cloud-native-korea-lab
git status
git add .
git commit -m "Add GWAN GHCR image push"
git push
```

After push, open GitHub Actions and confirm `GWAN CI` is green.
Then check GitHub repository → Packages → `hyean-gwan-simulation`.
