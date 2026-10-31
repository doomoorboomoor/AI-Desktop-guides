# Complete AI Desktop Reference Library — v3

## Publish on GitHub Pages

For crawler metadata, sitemap submission, and Google Search Console verification,
see [Search engine setup](SEARCH-ENGINE-SETUP.md). SEO settings live in
`Authoring/site.json`; indexing is separate from publishing.

Run `python Build-Pages.py` from this folder. It rebuilds the seven manuals
from canonical Markdown, validates local links and every search destination,
and writes the website to `_site/`. Python 3.9+ is required; dependencies
are bundled. No npm installation is needed.

Preview with `python -m http.server 8000 --directory _site`, then open
<http://localhost:8000>. Stop the preview with Ctrl+C.

Commit and push the source changes to `main`. In the GitHub repository,
open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
The included `.github/workflows/pages.yml` builds and validates pull requests;
pushes to `main` also publish the validated `_site` artifact. The expected URL is
<https://doomoorboomoor.github.io/AI-Desktop-guides/> once deployment succeeds.
You can also run the workflow manually from the Actions tab.

The publishing layout is:

```text
#Source/                 Canonical guide Markdown and historical inputs
Authoring/               Metadata, diagram previews, and bundled build engine
Build-Library.py         Standalone offline HTML build
Build-Pages.py           Optimized website build and link validation
.github/workflows/       GitHub Pages build and deployment
_site/                   Generated website only (ignored by Git)
  index.html             Library navigation and full-text search
  <app-slug>.html         Seven complete manuals with lowercase URLs
  assets/                Shared, content-hashed CSS and JavaScript
  404.html               Missing-page recovery
```

Only generated pages and their shared assets are published. Scratch folders,
archives, authoring projects, and original uploads are excluded from the
deployment artifact. Guide text, source downloads, diagrams, template download
links, and the existing mobile and print layouts are retained. The published
pages share cacheable assets; the root HTML exports remain self-contained.
Keep the entire `_site` folder together when copying the website.

Links are relative, so navigation and assets work beneath the repository's
GitHub Pages path. The 404 recovery URL and repository link in Build-Pages.py
are specific to this repository; update them if you fork it. Historical
`claude-code-Desktop.html` links redirect with their section fragments.
Use the canonical lowercase `chatgpt-desktop.html` when sharing links.

The validation report is saved to `#Temp/pages-validation.json`. Publishing
does not update the separate Google Drive ZIPs. For workflow details, see
[GitHub's custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

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

## Separate app downloads

Each app card and guide footer links to its own three-entry ZIP. The combined collection remains available. `Authoring/distribution.json` stores the seven app URLs and the combined URL; `Build-Library.cmd` preserves this mapping. See `DOWNLOADS.md`.
