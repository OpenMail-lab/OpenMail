#!/bin/bash
echo "🔹 Packaging OpenMail Helm Chart..."
helm package helm/
mv openmail-chart-1.0.0.tgz charts/

echo "🔹 Indexing Helm repository..."
helm repo index charts/

echo "🔹 Pushing to GitHub..."
git add charts/index.yaml charts/openmail-chart-1.0.0.tgz
git commit -m "Auto-updating Helm repository"
git push origin main
