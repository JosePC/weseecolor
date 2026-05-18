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

Older `.plugin` zips (`v0.7.1`, `v0.7.2`, `v0.7.3`, `v0.8.0`) predate the v1.0 renderer + consolidation work. They're no longer kept on disk — git history of this repo is the canonical record of what changed when. Use `git log` and `git checkout` to inspect or restore any prior revision.

## Local-development setup (symlinked plugin)

For day-to-day work on this machine, `~/.claude/plugins/marketplaces/local-desktop-app-uploads/weseecolor` is a **symlink to this repo**. That means Claude Desktop loads its plugin definition directly from the working tree — `git pull` (or any local edit) becomes the update mechanism, no `/plugin install` needed.

To verify or rebuild the symlink:

```bash
# Confirm symlink:
ls -la ~/.claude/plugins/marketplaces/local-desktop-app-uploads/weseecolor

# Recreate if broken/missing:
rm -rf ~/.claude/plugins/marketplaces/local-desktop-app-uploads/weseecolor
ln -s /Users/josepc/GitHub/weseecolor \
      ~/.claude/plugins/marketplaces/local-desktop-app-uploads/weseecolor
```

Refresh matrix after a `git pull` or local edit:

| What changed | Action |
|---|---|
| `render_card.py`, `card_template.html.j2`, fonts, CSS | None — subprocess reads from disk on every render |
| `SKILL.md`, references, `plugin.json` | Restart Claude Desktop (`⌘Q`, reopen). Existing conversations see the new files post-restart. |

The pre-built `weseecolor.plugin` zip in this folder is for **distribution to other machines** that aren't set up with the symlink (e.g., a teammate's laptop). Local installs don't need it.
