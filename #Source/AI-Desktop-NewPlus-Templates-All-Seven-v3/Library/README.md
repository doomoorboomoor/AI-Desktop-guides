# Complete AI Desktop Reference Library — v3

Seven complete manuals: Claude Desktop, Claude Code, ChatGPT Desktop,
Codex Desktop, Gemini Desktop, Hermes Desktop, and OpenClaw.

Open `index.html` to browse the guides, search all seven, get the shared
Google Drive template ZIP, or read New+ usage instructions. Keep the eight
HTML files together. All reading assets are embedded; external links need internet.

## Authoring authority

Root `PROJECT.md` defines this documentation project's policy. The seven
numbered Markdown guides under `#Source/` are the canonical guide text.
Other comparison files under `#Source/` are historical research inputs,
not verified product specifications and not automatically published.

Edit guide text in `#Source/`; edit display metadata under `Authoring/config/`.
Run `Build-Library.cmd` or `./Build-Library.ps1` to rebuild every guide and
the master index. On macOS/Linux run `python3 Build-Library.py`.
Python 3.9+ is required only for rebuilding. Dependencies are bundled with licenses.
No package installation, account connection, or server is required.

Both the sidebar and the in-body Contents list regenerate from actual
headings. HTML is derived output and will be replaced by a rebuild.
Archive prior outputs in `#Old/` if needed. `#Temp/` is for temporary builds;
the builder reads explicit canonical paths, not scratch or archive folders.

Diagram SVG previews are checked against source and image hashes. When
changing Mermaid source, update its matching SVG and intentionally refresh
the manifest under `Authoring/diagrams/<app>/`. A stale preview is omitted;
the edited Mermaid code is still shown. The builder does not execute Mermaid.

## Template workflow

Use the Google Drive link on the master page for the full New+ ZIP. Extract
it completely and read the package README before running its installer.
The installer skips existing same-named templates by default; `-Overwrite`
backs up matching entries before replacement. The installer does not enable
New+ or change PowerToys settings. To install only selected entries, open
New+ > Open templates and copy the desired contents of `NewPlus-Templates/`.

After creating a copy with New+, edit that copy. Each editable single-guide
project has its own `content/guide.md` SSOT and `Build-Guide.cmd`.
It is independent of this collection's canonical sources. To update this
collection, reconcile approved Markdown into `#Source/`, then rebuild here.

Existing product-verification dates are retained; newly authored Codex and
Claude Code guides cite official documentation reviewed on 31 October 2026.
HTML validation is not proof of installation or native-account entitlements.
