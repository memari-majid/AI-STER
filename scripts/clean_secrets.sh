#!/bin/bash

# Script to automatically clean secrets from git history

echo "🧹 Git History Secret Cleaner"
echo "=============================="

# Check if git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo "Installing git-filter-repo..."
    pip install git-filter-repo
fi

# Common secret patterns to clean
cat > /tmp/secret_patterns.txt << 'EOF'
# OpenAI
regex:sk-[a-zA-Z0-9]{48}==>OPENAI_KEY_REDACTED

# GitHub
regex:ghp_[0-9a-zA-Z]{36}==>GITHUB_TOKEN_REDACTED
regex:ghs_[0-9a-zA-Z]{36}==>GITHUB_TOKEN_REDACTED
regex:github_pat_[0-9a-zA-Z_]{82}==>GITHUB_TOKEN_REDACTED

# Google
regex:AIza[0-9A-Za-z-_]{35}==>GOOGLE_KEY_REDACTED

# AWS
regex:AKIA[0-9A-Z]{16}==>AWS_KEY_REDACTED

# Generic patterns
regex:api[_-]?key\s*=\s*["'][^"']+["']==>API_KEY_REDACTED
regex:secret\s*=\s*["'][^"']+["']==>SECRET_REDACTED
regex:password\s*=\s*["'][^"']+["']==>PASSWORD_REDACTED
EOF

# Backup current state
echo "Creating backup..."
cp -r .git .git.backup

# Run git-filter-repo
echo "Cleaning secrets from history..."
git filter-repo --replace-text /tmp/secret_patterns.txt

# Clean up
rm /tmp/secret_patterns.txt

echo "✅ Complete! History has been rewritten."
echo ""
echo "⚠️  IMPORTANT: You must force-push to update remote:"
echo "    git push origin --all --force"
echo "    git push origin --tags --force"
echo ""
echo "📋 Tell your team to run:"
echo "    git fetch origin"
echo "    git reset --hard origin/main"
