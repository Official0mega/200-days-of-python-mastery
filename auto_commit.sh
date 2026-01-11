# https://chatgpt.com/c/69637714-0e3c-832f-8bd7-b09574eda380
# ChatGPT Account: codeversehub@gmail.com

#!/bin/bash

# Stop if any error happens
set -e

echo "🔐 Starting SSH agent..."

# Start ssh-agent if not already running
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)"
fi

# Add SSH key (adjust path if needed)
SSH_KEY="../SSH-KEY/Official0mega_id_rsa"

if ssh-add -l >/dev/null 2>&1; then
    echo "✅ SSH key already loaded."
else
    echo "➕ Adding SSH key..."
    ssh-add "$SSH_KEY"
fi

echo "🔐 SSH authentication ready."
echo "--------------------------------"

# Read current day
DAY=$(cat day.txt)

# Safety check
if [ "$DAY" -gt 200 ]; then
    echo "✅ 200 Days Completed. Nothing left to commit."
    exit 0
fi

echo "🚀 Committing Day $DAY..."

# Stage all changes
git add .

# Check if there is anything to commit
if git diff --cached --quiet; then
    echo "⚠️ No changes detected, creating empty commit..."
    git commit --allow-empty -m "Day $DAY Completed"
else
    git commit -m "Day $DAY Completed"
fi

# Push to GitHub
git push

# Increment day
NEXT_DAY=$((DAY + 1))
echo "$NEXT_DAY" > day.txt

# Commit the updated day counter
git add day.txt
git commit -m "Prepare for Day $NEXT_DAY"
git push

echo "✅ Day $DAY pushed successfully!"
