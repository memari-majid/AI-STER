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
            text=True,
            errors='ignore'
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
    
    # Directories to skip
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env', 'docs'}
    
    for file_path in Path('.').rglob('*'):
        # Skip certain directories and files
        if any(skip_dir in str(file_path) for skip_dir in skip_dirs):
            continue
            
        # Skip documentation and example files
        if file_path.suffix in ['.md', '.txt', '.rst', '.example']:
            continue
            
        if file_path.is_file():
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