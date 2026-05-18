# WeSeeColor

This repo is the source of truth for two things, packaged together:

1. **The Claude plugin** [`weseecolor`](releases/weseecolor.plugin) — bundles two skills:
   - **`weseecolor-pharma`** — dermatology and personal care product analysis centered on Black skin and hair safety. Produces full product analyses (DOCX) and consumer-facing safety cards (3-page A4 PDF).
   - **`weseecolor-voice`** — brand voice and messaging guidance for WeSeeColor.net.
2. **The Astro site at weseecolor.net** — the public-facing advocacy site (`src/`, `public/`, `astro.config.mjs`, etc.).

The two are co-located so the visual assets stay consistent across both. They don't depend on each other.

---

## Installing the plugin

### Prerequisites (one-time per machine)

The plugin's card renderer needs two things that the plugin itself can't bundle:

| Tool | Why | Install on macOS | Install on Linux |
|---|---|---|---|
| **[uv](https://docs.astral.sh/uv/)** | Provisions the renderer's Python environment (WeasyPrint, Pillow, Jinja2) on first run. | `brew install uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Pango + Cairo** | WeasyPrint's PDF rendering engine — native libraries, not Python packages. | `brew install pango` (pulls in cairo, glib, fontconfig) | `sudo apt install libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 fontconfig` |

Both can be installed in ~2 minutes. The renderer will print clear install instructions if you skip them.

### Install the plugin

**Recommended for local development on this machine (symlink, zero copy):**

```bash
# Wire Claude Desktop's plugin directory to this repo as a symlink.
# `git pull` (or any local edit) now updates the plugin instantly.
rm -rf ~/.claude/plugins/marketplaces/local-desktop-app-uploads/weseecolor
ln -s "$(pwd)" ~/.claude/plugins/marketplaces/local-desktop-app-uploads/weseecolor
```

Then restart Claude Desktop (`⌘Q`, reopen) so it picks up the plugin manifest. Verify with `/plugin list` — should show `weseecolor 1.0.x`.

**For distribution to another machine** (e.g., a teammate's laptop), ship them the pre-built zip at [releases/weseecolor.plugin](releases/weseecolor.plugin). They install it via Claude Desktop's **Customize → Personal plugins → "+"** (Add from file).

### Update workflow after a `git pull` or local edit

| What changed | Action |
|---|---|
| `renderer/render_card.py`, `card_template.html.j2`, fonts, samples | Nothing. Subprocess reads files on every render. |
| `SKILL.md`, references, `plugin.json` | Restart Claude Desktop. |

No `/plugin install` step required when the symlink is in place.

---

## Repo layout

```
weseecolor/
├── .claude-plugin/plugin.json     ← plugin manifest (name, version)
├── releases/
│   ├── weseecolor.plugin          ← tracked-in-git, install this
│   └── README.md
├── scripts/
│   └── build-plugin.sh            ← rebuilds dist/weseecolor.plugin (+--release flag)
├── skills/
│   ├── weseecolor-pharma/         ← pharma skill + renderer + references
│   │   ├── SKILL.md
│   │   ├── renderer/              ← PDF card renderer (WeasyPrint via uv)
│   │   ├── references/            ← Canva originals, DOCX exemplars, legend
│   │   └── assets/
│   └── weseecolor-voice/          ← brand voice skill
│       └── SKILL.md
└── src/, public/, …               ← Astro site (weseecolor.net)
```

---

## Astro site (separate from the plugin)

If you also want to work on weseecolor.net:

```bash
npm install
npm run dev    # localhost:4321
```

Standard Astro commands; site is unaffected by plugin changes and vice-versa.
