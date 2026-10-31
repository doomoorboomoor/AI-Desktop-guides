# Live website audit — 31 October 2026

Site: https://doomoorboomoor.github.io/AI-Desktop-guides/

## Passed

- All 11 generated HTML URLs return HTTP 200 (index, seven guides, maintenance,
  explicit 404 page, and legacy Claude Code redirect).
- All discovered same-origin linked resources load successfully, including
  seven distinct shared assets and the favicon.
- All 1,012 checked internal section-link occurrences resolve.
- All 466 library search destinations resolve to existing guide headings.
- Search works on the index and all seven guides; result navigation,
  no-result handling, and clearing were exercised in a browser.
- All seven Markdown download buttons generate successful downloads. Embedded
  downloadable bytes match canonical source SHA-256 hashes for every guide.
- Mobile menus, theme switching, and 390px-wide layouts pass on the index
  and seven guides, without document-level horizontal overflow.
- All 14 diagram previews load with alternative text. Expansion and closing,
  Ctrl+K search focus, and code copying were exercised on each guide.
- No application JavaScript exceptions occurred during the page/control checks.
- Legacy Claude Code navigation preserves the section fragment.
- A deliberately missing URL returns HTTP 404 with the custom recovery page.
- 153 of 161 distinct external URLs return HTTP 200. These are HTTP
  availability checks; external-page section fragments and content accuracy
  were not exhaustively verified.
- The public combined template ZIP downloads anonymously: 8,155,257 bytes,
  810 entries, and no corrupt archive entry detected by ZIP integrity checking.

## Outstanding public-access problems

1. All seven individual app-pack Google Drive URLs return HTTP 401 when
   accessed anonymously. A browser visit to the Claude Desktop pack redirects
   to Google sign-in. These downloads are not currently verified as publicly
   accessible. The combined ZIP is accessible.
2. The maintenance page links to the source repository, which returns HTTP 404
   anonymously because the repository is private (confirmed through the
   authenticated GitHub CLI). The public maintenance link should instead point
   to public instructions, or clearly identify the repository as restricted.

The seven restricted URLs are recorded in Authoring/distribution.json under
`app_packs`. Making those files public changes their sharing permissions;
repository visibility and Drive permissions were not changed during this audit.

## Scope

This audit checked the deployed site in a browser and used unauthenticated HTTP
requests for external links and the combined ZIP download. Successful HTTP
responses alone do not prove the accuracy of third-party documentation. The
individual restricted ZIP contents could not be downloaded anonymously, so
their archive integrity and contents remain unverified. No live content or
cloud sharing settings were changed.
