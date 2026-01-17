#!/bin/bash
set -e

echo "🧠 Micro Commit Mode Started"
echo "--------------------------------"

CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
  echo "⚠️ No changes detected. Nothing to commit."
  exit 0
fi

echo "📦 Staging current changes..."
git add .

TIMESTAMP=$(date +"%H:%M:%S")

echo "✍️ Creating micro commit..."
git commit -m "Progress update at $TIMESTAMP"

echo "🌍 Pushing to GitHub..."
# git push
git push https://Official0mega@github.com/Official0mega/200-days-of-python-mastery.git 

echo "✅ Micro commit pushed successfully"
