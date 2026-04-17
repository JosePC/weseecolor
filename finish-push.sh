#!/bin/bash
# Run this from your Mac terminal when you have internet to complete the GitHub push.
# Creates the remote repo and pushes in one step.

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
GITHUB_TOKEN=$(security find-generic-password -a "github" -s "github-token" -w 2>/dev/null)

if [ -z "$GITHUB_TOKEN" ]; then
  echo "❌ GitHub token not found in keychain. Run setup/store-github-token.sh first."
  exit 1
fi

echo "→ Creating repo on GitHub..."
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  https://api.github.com/user/repos \
  -d '{"name":"weseecolor","description":"WeSeeColor skills and resources — evidence-based product analysis for Black skin and hair safety","private":false,"auto_init":false}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ Repo:', d.get('html_url', d.get('message','?')))"

echo "→ Pushing commits..."
git -C "$REPO_DIR" push -u origin master

echo "✅ Done! https://github.com/JosePC/weseecolor"
