# Security Scripts

This directory contains security-related scripts to help prevent and remove exposed secrets from your codebase.

## Available Scripts

### 🔍 `scan_secrets.py`
Scans your repository for potential exposed secrets in both current files and git history.

**Usage:**
```bash
python3 scripts/scan_secrets.py
```

**Features:**
- Detects common API key patterns (OpenAI, GitHub, AWS, Google, etc.)
- Scans current files (excluding docs and common directories)
- Scans entire git history
- Returns exit code 1 if secrets found (useful in CI/CD)

### 🧹 `clean_secrets.sh`
Automatically removes secrets from git history using git-filter-repo.

**Usage:**
```bash
./scripts/clean_secrets.sh
```

**Features:**
- Backs up `.git` directory before making changes
- Replaces common secret patterns with "REDACTED" text
- Provides instructions for force-pushing cleaned history

### 🔒 `example_secure_config.py`
Demonstrates best practices for managing secrets using environment variables.

**Usage:**
```bash
python3 scripts/example_secure_config.py
```

**Features:**
- Shows how to load secrets from `.env` files
- Validates required configuration
- Creates example `.env.example` file

## Pre-commit Hook

A pre-commit hook is installed at `.git/hooks/pre-commit` that automatically checks for secrets before each commit. This provides real-time protection against accidentally committing secrets.

## Best Practices

1. **Never hardcode secrets** - Always use environment variables
2. **Use `.env` files** - Keep them in `.gitignore`
3. **Rotate exposed keys immediately** - Assume they're compromised
4. **Enable GitHub secret scanning** - Additional layer of protection
5. **Run secret scans regularly** - Part of your security routine

## Emergency Response

If you've exposed a secret:

1. **Rotate the key immediately** at your service provider
2. **Run the cleaner script** to remove from history
3. **Force push** the cleaned branches
4. **Notify your team** about the history rewrite

See `/workspace/docs/SECURITY_SECRET_REMOVAL_GUIDE.md` for detailed instructions.