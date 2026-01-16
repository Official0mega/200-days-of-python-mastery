# # https://chatgpt.com/c/69637714-0e3c-832f-8bd7-b09574eda380
# # ChatGPT Account: codeversehub@gmail.com
# # 🔹 ONE-TIME Windows cleanup (recommended)
# # Run this once to stop CRLF/LF warnings forever:
# git config --global core.autocrlf true


#!/bin/bash
set -e

echo "🚀 Auto Git Commit Started"
echo "--------------------------------"

# Ensure day.txt exists
if [ ! -f day.txt ]; then
    echo "❌ day.txt not found. Create it and put the starting day inside."
    exit 1
fi

# Read current day
DAY=$(cat day.txt)

# Validate day value
if ! [[ "$DAY" =~ ^[0-9]+$ ]]; then
    echo "❌ Invalid day value in day.txt"
    exit 1
fi

# Safety check
if [ "$DAY" -gt 200 ]; then
    echo "🎉 200 Days Completed. Challenge finished!"
    exit 0
fi

# Prevent duplicate commits
if git log --oneline | grep -q "Day $DAY Completed"; then
    echo "⚠️ Day $DAY already committed. Skipping."
    exit 0
fi

echo "📦 Staging files..."
git add .

echo "✍️ Committing Day $DAY..."

if git diff --cached --quiet; then
    echo "⚠️ No changes detected — creating empty commit."
    git commit --allow-empty -m "Day $DAY Completed"
else
    git commit -m "Day $DAY Completed"
fi

echo "🌍 Pushing to GitHub..."
git push

# Increment day
NEXT_DAY=$((DAY + 1))
echo "$NEXT_DAY" > day.txt

echo "🗓️ Preparing for Day $NEXT_DAY..."
git add day.txt
git commit -m "Prepare for Day $NEXT_DAY"
git push

echo "--------------------------------"
echo "✅ Day $DAY successfully committed & pushed!"
echo "📅 Ready for Day $NEXT_DAY"




































# #!/bin/bash

# # Exit immediately if a command fails
# set -e

# echo "🔐 Initializing SSH authentication..."

# # Always start ssh-agent (safe on Windows Git Bash)
# eval "$(ssh-agent -s)" >/dev/null

# # SSH key path (relative to repo)
# SSH_KEY="../SSH-KEY/Official0mega_id_rsa"

# # Add SSH key silently (ignore if already added)
# ssh-add "$SSH_KEY" >/dev/null 2>&1 || true

# echo "✅ SSH authentication ready."
# echo "--------------------------------"

# # Ensure day.txt exists
# if [ ! -f day.txt ]; then
#     echo "❌ day.txt not found. Create it and put the starting day inside."
#     exit 1
# fi

# # Read current day
# DAY=$(cat day.txt)

# # Validate day is a number
# if ! [[ "$DAY" =~ ^[0-9]+$ ]]; then
#     echo "❌ Invalid day value in day.txt"
#     exit 1
# fi

# # Safety check
# if [ "$DAY" -gt 200 ]; then
#     echo "🎉 200 Days Completed. Challenge finished!"
#     exit 0
# fi

# # Prevent duplicate Day commits
# if git log --oneline | grep -q "Day $DAY Completed"; then
#     echo "⚠️ Day $DAY already committed. Skipping."
#     exit 0
# fi

# echo "🚀 Committing Day $DAY..."

# # Stage all changes
# git add .

# # Commit changes (or empty commit if no changes)
# if git diff --cached --quiet; then
#     echo "⚠️ No changes detected — creating empty commit."
#     git commit --allow-empty -m "Day $DAY Completed"
# else
#     git commit -m "Day $DAY Completed"
# fi

# # Push Day commit
# git push

# # Increment day
# NEXT_DAY=$((DAY + 1))
# echo "$NEXT_DAY" > day.txt

# # Commit day counter update
# git add day.txt
# git commit -m "Prepare for Day $NEXT_DAY"
# git push

# echo "✅ Day $DAY successfully committed and pushed!"
# echo "📅 Ready for Day $NEXT_DAY"










































# #!/bin/bash

# # Stop if any error happens
# set -e

# echo "🔐 Starting SSH agent..."

# # Start ssh-agent if not already running
# if [ -z "$SSH_AUTH_SOCK" ]; then
#     eval "$(ssh-agent -s)"
# fi

# # Add SSH key (adjust path if needed)
# SSH_KEY="../SSH-KEY/Official0mega_id_rsa"

# if ssh-add -l >/dev/null 2>&1; then
#     echo "✅ SSH key already loaded."
# else
#     echo "➕ Adding SSH key..."
#     ssh-add "$SSH_KEY"
# fi

# echo "🔐 SSH authentication ready."
# echo "--------------------------------"

# # Read current day
# DAY=$(cat day.txt)

# # Safety check
# if [ "$DAY" -gt 200 ]; then
#     echo "✅ 200 Days Completed. Nothing left to commit."
#     exit 0
# fi

# echo "🚀 Committing Day $DAY..."

# # Stage all changes
# git add .

# # Check if there is anything to commit
# if git diff --cached --quiet; then
#     echo "⚠️ No changes detected, creating empty commit..."
#     git commit --allow-empty -m "Day $DAY Completed"
# else
#     git commit -m "Day $DAY Completed"
# fi

# # Push to GitHub
# git push

# # Increment day
# NEXT_DAY=$((DAY + 1))
# echo "$NEXT_DAY" > day.txt

# # Commit the updated day counter
# git add day.txt
# git commit -m "Prepare for Day $NEXT_DAY"
# git push

# echo "✅ Day $DAY pushed successfully!"
