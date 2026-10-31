# Editable guide project

`content/guide.md` is the complete guide-text SSOT. `guide.config.json` owns
display metadata. The generated `dist/` HTML is a derived reading copy.

1. Edit the Markdown and metadata in your text editor.
2. Run `Build-Guide.cmd` or `./Build-Guide.ps1` on Windows. Python 3.9+ is required only for rebuilding.
3. Open the generated HTML in `dist/`. No server or network is needed.
4. Use its Markdown download and compare it with the current source if checking integrity.

On macOS/Linux run `python3 scripts/guide_builder.py --root . --json-report`.
Mistune and the browser highlighter are bundled with their licenses. No pip,
npm, account connection, or application installation is performed by building.

Keep one H1 title in Markdown and H2/H3 sections. Both the sidebar and the
in-body `## Contents` list are rebuilt from actual headings, including renamed
sections. File links inside code examples remain literal examples.

Diagram source and SVG previews are separate authoring artifacts. The builder
checks `assets/diagrams/manifest.json` against both the source and SVG bytes.
After changing/reordering Mermaid, regenerate the matching SVG and intentionally
refresh the manifest. Until then, stale previews are withheld and source is shown.
The builder is not a general Mermaid renderer.

`#Old` is for superseded files; `#Temp` is for temporary work. Neither is scanned
for guide text. Keep current policy out of historical copies.

Opening the completed HTML does not execute its examples. Native app behavior
and account entitlements are distinct from HTML/browser validation. Existing
product verification dates are preserved. New+ filename variables affect names,
not placeholders inside document content.
