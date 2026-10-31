# Complete AI Desktop New+ Template Collection — v3

Seven complete application packs: Claude Desktop, Claude Code, ChatGPT Desktop,
Codex Desktop, Gemini Desktop, Hermes Desktop, and OpenClaw.

## Drive update status
The connector was denied write access to the provided Drive file. This local archive is the completed seven-app v3 release; the existing Drive URL has not yet been replaced. See DRIVE-UPDATE.md.

## Read first
Open Library/index.html for every guide and the New+ pack cards. The full
manuals, examples, source downloads, syntax highlighting, search, diagrams,
keyboard navigation, and print sources are included. All reading assets are offline.

## Install on Windows
1. Extract the complete ZIP to a normal folder.
2. In PowerToys Settings enable New+.
3. Read and run Install-NewPlus-Templates.cmd, or run ./Install-NewPlus-Templates.ps1.
4. Right-click empty space in File Explorer > New+ > select the required entry.

The installer skips existing same-named entries. Use
`./Install-NewPlus-Templates.ps1 -Overwrite` to update matching entries with
backups. `-TemplatesPath` supports a custom New+ templates folder.
For selected entries, choose New+ > Open templates and manually copy the
desired contents of NewPlus-Templates/ into that folder. Do not copy the
enclosing directory as one menu entry.

## Included entries
24 direct entries: seven complete HTML guides, seven editable source projects,
seven Atlas workspaces, the all-seven reference library, a blank HTML guide,
and a generic authoring project. The optional dated authoring project is
installed only with `-IncludeDated`. Filename variables require New+'s own
variable setting and change filenames/folder names, not document contents.

The complete HTML is repeated in each matching app's complete entry,
editable-project dist/, Atlas reference/, and the full library. Those copies
come from the same current source. Each editable project contains the full
Markdown manual, not excerpts or continuation placeholders.

## Maintain content
In an editable app project, edit content/guide.md and guide.config.json,
then run Build-Guide.cmd. In Library/, edit the canonical #Source/ files
and run Build-Library.cmd to refresh all seven manuals and the master.
Python 3.9+ is required only for rebuilding; reading HTML needs no Python.
Dependencies and licenses are bundled. Root #Old/ and #Temp/ are preserved
in every folder template and excluded from active content discovery.

The seven app HTML templates do not contain local links to missing siblings.
The all-seven library contains working links between all guides and the master.
Historical originals are stored only under Original-Uploads/ for provenance.

## Migration and scope
Earlier v2 template entries may remain installed under different names.
No obsolete entry or existing user project is automatically deleted.
After reviewing the new collection, remove only deliberate obsolete entries
through New+ > Open templates if desired. Preserve original uploads and backups.

This package copies templates; it does not install AI apps, enable New+,
change settings, connect accounts, enable hooks, or start servers. New native
guides cite documentation reviewed 31 October 2026; original five guides
retain their earlier product-verification dates. Native PowerToys GUI use
is separate from the reported build/browser/package tests.

Stable shared download: https://drive.google.com/file/d/1O7XtAEqdw9XkZerEcafWqE1GDW_oez5t/view?usp=sharing

See VALIDATION-REPORT.json for the actual checks performed for this release.
