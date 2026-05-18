# Releases

The latest installable `weseecolor.plugin` zip lives here.

## What's tracked

- **`weseecolor.plugin`** — always the current `v$VERSION` from [.claude-plugin/plugin.json](../.claude-plugin/plugin.json). Tracked in git so a fresh clone + a single `/plugin install ./releases/weseecolor.plugin` is all anyone needs.

## How to refresh after a version bump

1. Bump `version` in [.claude-plugin/plugin.json](../.claude-plugin/plugin.json).
2. Run the build script with `--release`:

   ```bash
   ./scripts/build-plugin.sh --release
   ```

   This rebuilds the zip and copies it over `releases/weseecolor.plugin`.

3. Commit and push:

   ```bash
   git add .claude-plugin/plugin.json releases/weseecolor.plugin
   git commit -m "Release v<version> — <one-line summary>"
   git push
   ```

## Install / update locally

```
/plugin install /Users/josepc/GitHub/weseecolor/releases/weseecolor.plugin
```

Or, for live-development (re-installs on `git pull`):

```
/plugin install /Users/josepc/GitHub/weseecolor
```

## Version history

Older `.plugin` zips (`v0.7.1`, `v0.7.2`, `v0.7.3`, `v0.8.0`) are archived outside the repo at `~/Documents/Claude/Projects/_old_WeSeeColor product analysis/`. They predate the v1.0 renderer + consolidation work and are kept for historical reference only.
