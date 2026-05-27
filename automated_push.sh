#!/bin/bash
# automated_push.sh
# Run this script to push all files directly to your GitHub repository!

echo "=================================================================="
echo "PUSHING CONSTRAINED ECOLOGY v0.34 TO GITHUB..."
echo "=================================================================="

# Pre-filled credentials from your GitHub URL
gh_user="Alex2704go"
gh_repo="constrained-ecology-v0.34"

echo "GitHub Account: https://github.com/${gh_user}"
echo "Repository: ${gh_repo}"
echo "------------------------------------------------------------------"

# Prompt only for the token securely
read -s -p "Enter your GitHub Personal Access Token (PAT): " gh_token
echo ""

# Validate input
if [ -z "$gh_token" ]; then
    echo "Error: Personal Access Token (PAT) is required to authenticate."
    exit 1
fi

# Set remote origin with credentials securely and push
echo "Linking remote origin and pushing to master branch..."
git remote remove origin 2>/dev/null
git remote add origin "https://${gh_user}:${gh_token}@github.com/${gh_user}/${gh_repo}.git"
git branch -M main
git push -u origin main --force

# Clean up remote URL to avoid leaving token in git config
git remote set-url origin "https://github.com/${gh_user}/${gh_repo}.git"

echo "=================================================================="
echo "DEPOSITED SUCCESSFULLY! Your repository is now live at:"
echo "https://github.com/${gh_user}/${gh_repo}"
echo "=================================================================="
