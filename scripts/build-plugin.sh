#!/bin/bash
# Build a distributable weseecolor.plugin zip from the repo.
#
# The zip contains exactly what Claude's plugin loader needs:
#   .claude-plugin/plugin.json     manifest (name, version, etc.)
#   skills/weseecolor-pharma/      pharma skill (incl. renderer + references)
#   skills/weseecolor-voice/       voice skill
#   README.md                      repo-level intro
#
# Skipped:
#   - .git, .DS_Store, __pycache__, prepared/ (renderer cache)
#   - Astro site code (src/, public/, package.json, etc.)
#   - assets/ (site-level, not plugin-level — plugin already has its own
#     assets under skills/weseecolor-pharma/{assets,renderer}/)
#
# Usage:
#   ./scripts/build-plugin.sh           # writes dist/weseecolor.plugin
#   ./scripts/build-plugin.sh -o /tmp   # custom output dir

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${REPO_ROOT}/dist"
while getopts "o:" opt; do
  case $opt in
    o) OUT_DIR="$OPTARG" ;;
    *) echo "Usage: $0 [-o output_dir]" >&2; exit 1 ;;
  esac
done

mkdir -p "$OUT_DIR"
OUT_FILE="$OUT_DIR/weseecolor.plugin"
rm -f "$OUT_FILE"

cd "$REPO_ROOT"

# zip the manifest, the two skills, and the readme. Exclusions inline.
# We skip the pre-rendered *_card.pdf samples (regenerable by running
# render_card.py on the .json content files) to keep the zip lean. The
# sample JSON content files and product PNGs DO ship — they're tiny and
# act as test fixtures + JSON-schema examples.
zip -r -q "$OUT_FILE" \
    .claude-plugin \
    skills/weseecolor-pharma \
    skills/weseecolor-voice \
    README.md \
    -x "*.DS_Store" \
    -x "*/__pycache__/*" \
    -x "*/prepared/*" \
    -x "*/renderer/samples/*_card.pdf" \
    -x ".git/*"

# Extract version from manifest for the success message
VERSION=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
SIZE=$(du -h "$OUT_FILE" | cut -f1)

echo "✓ Built $OUT_FILE (v$VERSION, $SIZE)"
echo ""
echo "To install in Claude Desktop:"
echo "  1. Drag the .plugin file into a Claude conversation, OR"
echo "  2. Use /plugin install /path/to/weseecolor.plugin"
echo ""
echo "To install for local development (re-installs on every \`git pull\`):"
echo "  /plugin install ${REPO_ROOT}"
