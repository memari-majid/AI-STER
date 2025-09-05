# 🔐 Complete Guide: Removing Exposed Secrets from Code and Git History

## Table of Contents
1. [🚨 Emergency Response](#emergency-response)
2. [🔍 Finding Exposed Secrets](#finding-exposed-secrets)
3. [🧹 Removing from Git History](#removing-from-git-history)
4. [🔑 Key Rotation](#key-rotation)
5. [🛡️ Prevention](#prevention)
6. [🤖 Automation Scripts](#automation-scripts)

---

## 🚨 Emergency Response

If GitHub has notified you about an exposed secret:

1. **The key is already compromised** - Assume it's been scraped by bots
2. **Rotate immediately** - Create a new key before fixing the repo
3. **Check logs** - Look for unauthorized usage in your service provider's dashboard

---

## 🔍 Finding Exposed Secrets

### Step 1: Understand the GitHub Alert

GitHub provides specific information:
```
commit: 359c79d69def96b57338ab7951a237e2890da067
path: app.py:3480
```

This tells you:
- **Commit hash**: `359c79d6...`
- **File**: `app.py`
- **Line number**: `3480`

### Step 2: Search Current Code

```bash
# Search for OpenAI keys (all start with 'sk-')
grep -R "sk-" . --exclude-dir=.git

# Search for common API key patterns
grep -rEn "(api[_-]?key|apikey|secret|token|password|pwd|pass|credential)" . \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  --exclude-dir=venv \
  --exclude-dir=__pycache__

# Search for specific patterns by service
grep -rEn "sk-[a-zA-Z0-9]{48}" .          # OpenAI
grep -rEn "AIza[0-9A-Za-z-_]{35}" .       # Google API
grep -rEn "ghp_[0-9a-zA-Z]{36}" .         # GitHub Personal Access Token
grep -rEn "ghs_[0-9a-zA-Z]{36}" .         # GitHub OAuth Access Token
grep -rEn "github_pat_[0-9a-zA-Z_]{82}" . # GitHub Fine-grained PAT
```

### Step 3: Search Git History

```bash
# Search all commits for exposed secrets
git log -p | grep -E "sk-|AIza|ghp_|ghs_|github_pat_"

# Search with context (shows 3 lines before/after)
git log -p | grep -C 3 "sk-"

# Find specific commit that introduced the secret
git log -S "sk-" --oneline

# Show all occurrences of a secret across branches
git grep "sk-" $(git rev-list --all)
```

---

## 🧹 Removing from Git History

### Method 1: Using git-filter-repo (Recommended)

```bash
# Install git-filter-repo
pip install git-filter-repo

# Create a file with secrets to replace
echo "sk-proj-YOUR_ACTUAL_KEY_HERE==>REDACTED" > replacements.txt
echo "ghp_YOUR_GITHUB_TOKEN==>REDACTED" >> replacements.txt

# Run the replacement
git filter-repo --replace-text replacements.txt

# Clean up
rm replacements.txt
```

### Method 2: Using BFG Repo-Cleaner (Alternative)

```bash
# Download BFG
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# Create passwords.txt with your exposed secrets
echo "sk-proj-YOUR_KEY_HERE" > passwords.txt

# Run BFG
java -jar bfg-1.14.0.jar --replace-text passwords.txt

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
rm passwords.txt
```

### Method 3: Interactive Rebase (For Recent Commits)

```bash
# If the secret is only in the last few commits
git rebase -i HEAD~5

# Mark commits with 'edit', then:
git show
# Edit the file to remove the secret
git add .
git commit --amend
git rebase --continue
```

### Force Push the Cleaned History

```bash
# Push to all branches
git push origin --all --force
git push origin --tags --force

# If working with a team, notify them to:
git fetch origin
git reset --hard origin/main
```

---

## 🔑 Key Rotation

### OpenAI API Keys

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Name it descriptively (e.g., "production-app-2024")
4. Save it securely
5. Delete the old compromised key

### GitHub Tokens

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Generate new token with minimal required permissions
3. Set expiration date
4. Update in your applications
5. Delete old token

### Best Practices for New Keys

```bash
# Use environment variables
export OPENAI_API_KEY="sk-proj-..."

# Or use .env files (add to .gitignore!)
echo "OPENAI_API_KEY=sk-proj-..." >> .env

# In Python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

---

## 🛡️ Prevention

### 1. Update .gitignore

```bash
# Secrets and credentials
.env
.env.*
*.pem
*.key
*.pfx
*.p12
secrets/
credentials/
config/secrets.yml
config/database.yml

# API keys patterns (as backup)
*api_key*
*apikey*
*secret*
*token*
*credential*
```

### 2. Pre-commit Hooks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Patterns to check
PATTERNS=(
    "sk-[a-zA-Z0-9]{48}"           # OpenAI
    "AIza[0-9A-Za-z-_]{35}"         # Google
    "ghp_[0-9a-zA-Z]{36}"           # GitHub PAT
    "ghs_[0-9a-zA-Z]{36}"           # GitHub OAuth
    "github_pat_[0-9a-zA-Z_]{82}"   # GitHub Fine-grained
    "xox[baprs]-[0-9a-zA-Z-]+"     # Slack
    "sq0csp-[0-9A-Za-z-_]+"         # Square
    "sk_live_[0-9a-zA-Z]+"          # Stripe
)

for pattern in "${PATTERNS[@]}"; do
    if git diff --staged | grep -E "$pattern"; then
        echo "❌ ERROR: Potential secret detected matching pattern: $pattern"
        echo "Remove the secret and try again."
        exit 1
    fi
done

echo "✅ No secrets detected"
exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### 3. GitHub Secret Scanning

Enable in repository settings:
1. Go to Settings → Security → Code security and analysis
2. Enable "Secret scanning"
3. Enable "Push protection"

---

## 🤖 Automation Scripts

### Complete Secret Scanner Script

Create `scripts/scan_secrets.py`:

```python
#!/usr/bin/env python3
"""
Comprehensive secret scanner for git repositories
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Define secret patterns
SECRET_PATTERNS = {
    'OpenAI API Key': r'sk-[a-zA-Z0-9]{48}',
    'Google API Key': r'AIza[0-9A-Za-z-_]{35}',
    'GitHub Personal Access Token': r'ghp_[0-9a-zA-Z]{36}',
    'GitHub OAuth Token': r'ghs_[0-9a-zA-Z]{36}',
    'GitHub Fine-grained PAT': r'github_pat_[0-9a-zA-Z_]{82}',
    'Slack Token': r'xox[baprs]-[0-9a-zA-Z-]+',
    'Square Access Token': r'sq0csp-[0-9A-Za-z-_]+',
    'Stripe API Key': r'sk_live_[0-9a-zA-Z]+',
    'AWS Access Key': r'AKIA[0-9A-Z]{16}',
    'Generic API Key': r'["\']?api[_-]?key["\']?\s*[:=]\s*["\'][^"\']+["\']',
    'Generic Secret': r'["\']?secret["\']?\s*[:=]\s*["\'][^"\']+["\']',
    'Private Key': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
}

def scan_file(file_path: Path) -> List[Tuple[str, int, str]]:
    """Scan a single file for secrets."""
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for secret_type, pattern in SECRET_PATTERNS.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append((secret_type, line_num, line.strip()))
    except Exception as e:
        print(f"Error scanning {file_path}: {e}")
    
    return findings

def scan_git_history() -> List[Tuple[str, str, str]]:
    """Scan git history for secrets."""
    findings = []
    
    # Get all commits
    result = subprocess.run(
        ['git', 'rev-list', '--all'],
        capture_output=True,
        text=True
    )
    
    commits = result.stdout.strip().split('\n')
    
    for commit in commits:
        # Get commit diff
        result = subprocess.run(
            ['git', 'show', commit],
            capture_output=True,
            text=True
        )
        
        for secret_type, pattern in SECRET_PATTERNS.items():
            matches = re.findall(pattern, result.stdout, re.IGNORECASE)
            if matches:
                findings.append((commit[:7], secret_type, matches[0][:20] + '...'))
    
    return findings

def main():
    """Main function to scan repository."""
    print("🔍 Scanning for secrets in current directory and git history...\n")
    
    # Scan current files
    print("📁 Scanning current files:")
    file_findings = []
    
    for file_path in Path('.').rglob('*'):
        if file_path.is_file() and '.git' not in str(file_path):
            findings = scan_file(file_path)
            if findings:
                file_findings.extend([(str(file_path), *f) for f in findings])
    
    if file_findings:
        print(f"\n❌ Found {len(file_findings)} potential secrets in current files:")
        for file_path, secret_type, line_num, content in file_findings:
            print(f"  - {file_path}:{line_num} - {secret_type}")
            print(f"    Preview: {content[:50]}...")
    else:
        print("✅ No secrets found in current files")
    
    # Scan git history
    print("\n📜 Scanning git history:")
    history_findings = scan_git_history()
    
    if history_findings:
        print(f"\n❌ Found secrets in {len(history_findings)} commits:")
        for commit, secret_type, preview in history_findings:
            print(f"  - Commit {commit}: {secret_type} - {preview}")
    else:
        print("✅ No secrets found in git history")
    
    # Exit with error if any secrets found
    if file_findings or history_findings:
        print("\n⚠️  Please remove these secrets and clean git history!")
        sys.exit(1)
    else:
        print("\n✅ Repository is clean!")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### Git History Cleaner Script

Create `scripts/clean_secrets.sh`:

```bash
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
```

Make executable:
```bash
chmod +x scripts/scan_secrets.py scripts/clean_secrets.sh
```

---

## 📚 Additional Resources

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [git-filter-repo Documentation](https://github.com/newren/git-filter-repo)
- [OWASP Secret Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [truffleHog - Secret Scanner](https://github.com/trufflesecurity/trufflehog)
- [Gitleaks - SAST for Secrets](https://github.com/gitleaks/gitleaks)

---

## 🎯 Quick Reference Checklist

- [ ] Identify exposed secret location from GitHub alert
- [ ] Search current code for the secret
- [ ] Search git history for all occurrences
- [ ] Choose removal method (git-filter-repo recommended)
- [ ] Clean git history
- [ ] Force push cleaned branches
- [ ] Rotate compromised keys/tokens
- [ ] Update code to use environment variables
- [ ] Set up pre-commit hooks
- [ ] Enable GitHub secret scanning
- [ ] Notify team members of history rewrite
- [ ] Verify repository is clean

Remember: **Speed matters!** Exposed secrets can be harvested by bots within minutes.