#!/usr/bin/env python3
"""Offline, reproducible Markdown -> self-contained HTML guide generator.

Requires Python 3.9+ only. Mistune v3.2.1 is vendored under scripts/vendor/.
No CDN, npm, pip installation, network, or credentials required.
"""
from __future__ import annotations
import argparse, base64, datetime as dt, hashlib, html, json, mimetypes, re, sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE / "vendor"))
import mistune  # noqa: E402


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_slug(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]*>", "", value)).casefold()
    value = re.sub(r"[^\w-]+", "-", value, flags=re.UNICODE).strip("_-")
    return value[:90] or "section"


class GuideRenderer(mistune.HTMLRenderer):
    def __init__(self, project: Path):
        super().__init__(escape=True)
        self.project = project
        self.headings = []
        self.seen = set()
        self.code_count = 0
        self.mermaid_count = 0
        self.preview_count = 0
        self.messages = []

    def heading(self, text: str, level: int, **attrs) -> str:
        label = html.unescape(re.sub(r"<[^>]*>", "", text)).strip()
        base = safe_slug(label)
        name = base
        i = 2
        while name in self.seen:
            name = f"{base}-{i}"
            i += 1
        self.seen.add(name)
        self.headings.append(dict(level=level, id=name, title=label))
        return (f'<h{level} id="{html.escape(name, quote=True)}">{text}'
                f'<a class="heading-link" href="#{html.escape(name, quote=True)}" aria-label="Link to this heading">#</a>'
                f'</h{level}>\n')

    def block_code(self, code: str, info: str | None = None) -> str:
        lang = (info or "text").split(None, 1)[0].strip().lower()
        lang = re.sub(r"[^a-zA-Z0-9+_.-]", "", lang)[:35] or "text"
        self.code_count += 1
        body = html.escape(code, quote=False)
        source = (f'<div class="code-box"><div class="code-head"><span>{html.escape(lang)}</span>'
                  '<button type="button" class="copy-code" aria-label="Copy code block">Copy code</button></div>'
                  f'<pre tabindex="0"><code class="language-{lang}">{body}</code></pre></div>')
        if lang != 'mermaid':
            return source
        self.mermaid_count += 1
        diagram = self.project / 'assets' / 'diagrams' / f'diagram-{self.mermaid_count:02}.svg'
        manifest_file = self.project / 'assets' / 'diagrams' / 'manifest.json'
        snapshots = json.loads(manifest_file.read_text('utf-8')) if manifest_file.is_file() else {}
        snapshot = snapshots.get(diagram.name, {})
        valid_snapshot = diagram.is_file() and snapshot.get('source_sha256') == sha(code.encode('utf-8')) and snapshot.get('svg_sha256') == sha(diagram.read_bytes())
        if valid_snapshot:
            self.preview_count += 1
            data = base64.b64encode(diagram.read_bytes()).decode('ascii')
            return (f'<figure class="diagram"><div class="diagram-label">Diagram {self.mermaid_count}: '
                    '<span>static SVG preview, source below</span></div>'
                    f'<img class="diagram-preview" src="data:image/svg+xml;base64,{data}" '
                    f'alt="Rendered preview of Mermaid diagram {self.mermaid_count}">' 
                    f'<details class="diagram-source"><summary>View Mermaid source</summary>{source}</details></figure>')
        self.messages.append(f'Mermaid block {self.mermaid_count}: source preserved; matching current SVG snapshot missing or stale.')
        return (f'<figure class="diagram"><p class="diagram-label">Mermaid source (no SVG preview supplied)</p>'
                f'{source}</figure>')

    def image(self, text: str, url: str, title: str | None = None) -> str:
        url = html.unescape(url)
        if url.startswith('data:') or url.startswith('https://') or url.startswith('http://'):
            src = url
        elif url.startswith('/') or '..' in Path(url).parts:
            self.messages.append(f'Image reference not embedded (outside asset scope): {url}')
            src = url
        else:
            # Only dedicated assets directory is permitted for offline embedding.
            path = (self.project / url).resolve()
            assets = (self.project / 'assets').resolve()
            if path.is_file() and (assets == path.parent or assets in path.parents):
                mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
                src = f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
            else:
                self.messages.append(f'Unresolved image: {url}')
                src = url
        tag = f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(text, quote=True)}" loading="lazy"'
        if title:
            tag += f' title="{html.escape(title, quote=True)}"'
        return tag + '>'


def make_nav(headings: list[dict]) -> str:
    groups: list[dict] = []
    for h in headings:
        if h['level'] == 2:
            groups.append({'parent': h, 'children': []})
        elif h['level'] == 3 and groups:
            groups[-1]['children'].append(h)
    if not groups:
        return '<p class="muted">Add H2 headings to generate contents.</p>'
    out = []
    for idx, group in enumerate(groups):
        h = group['parent']
        out.append('<details class="toc-group"' + (' open' if idx == 0 else '') + '>')
        out.append(f'<summary>{html.escape(h["title"])}</summary>')
        out.append('<div class="toc-links">')
        out.append(f'<a class="toc-parent" href="#{html.escape(h["id"], quote=True)}">Section overview</a>')
        for c in group['children']:
            out.append(f'<a href="#{html.escape(c["id"], quote=True)}">{html.escape(c["title"])}</a>')
        out.append('</div></details>')
    return '\n'.join(out)


class CheckHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = []
        self.anchors = []
        self.urls = []
        self.imgs_missing_alt = 0
        self.tags = {}
        self.html_lang = False
        self.remote_assets = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if tag == 'html' and a.get('lang'):
            self.html_lang = True
        if a.get('id'):
            if a['id'] in self.ids:
                self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        if tag == 'a' and a.get('href', '').startswith('#') and a['href'] != '#':
            self.anchors.append(unquote(a['href'][1:]))
        if tag == 'img' and 'alt' not in a:
            self.imgs_missing_alt += 1
        if tag in ('img', 'script', 'link'):
            v = a.get('src') or a.get('href')
            if v and (v.startswith('http://') or v.startswith('https://')):
                self.remote_assets.append(v)
        if tag in ('a', 'img'):
            self.urls.append((tag, a.get('href') or a.get('src') or ''))


def validate_html(text: str, html_path: Path, project: Path) -> tuple[list[str], list[str]]:
    parser = CheckHTML()
    parser.feed(text)
    errors, warnings = [], []
    if not parser.html_lang: errors.append('HTML language attribute missing')
    if parser.tags.get('main', 0) != 1: errors.append('Exactly one main landmark is required')
    if parser.tags.get('h1', 0) != 1: errors.append('Exactly one H1 heading is required')
    if parser.duplicates: errors.append('Duplicate IDs: ' + ', '.join(parser.duplicates[:8]))
    if parser.imgs_missing_alt: errors.append(f'{parser.imgs_missing_alt} image(s) missing alt text')
    missing = sorted(set(x for x in parser.anchors if x not in parser.ids))
    if missing: errors.append('Missing anchor destinations: ' + ', '.join(missing[:12]))
    if parser.remote_assets: errors.append('Remote assets prevent standalone offline use')
    for tag, url in parser.urls:
        if not url or url.startswith(('https://', 'http://', '#', 'mailto:', 'tel:', 'data:')):
            continue
        if url.startswith(('javascript:', 'vbscript:')):
            errors.append(f'Unsafe URL in {tag}: {url}')
            continue
        if url.startswith('//'):
            warnings.append('Protocol-relative URL (may require network): ' + url)
            continue
        p = urlparse(url)
        if p.scheme:
            warnings.append('Unrecognized URL scheme: ' + url)
            continue
        # In generated stand-alone documents, only same-directory file links are valid.
        file_part = unquote(p.path)
        candidate = (html_path.parent / file_part).resolve()
        if file_part and not candidate.is_file():
            warnings.append(f'Relative {tag} reference may not work in standalone HTML: {url}')
    return errors, sorted(set(warnings))


def build(project: Path, output: Path | None = None, navigation: list | None = None) -> dict:
    cfg_path = project / 'guide.config.json'
    if not cfg_path.is_file(): raise SystemExit('Missing guide.config.json: ' + str(cfg_path))
    cfg = json.loads(cfg_path.read_text(encoding='utf-8-sig'))
    allowed = ['title', 'subtitle', 'description', 'author', 'revision', 'verified_date', 'root_baseline', 'language']
    for k in allowed:
        if k not in cfg or not isinstance(cfg[k], str):
            raise SystemExit(f'Missing or invalid config string: {k}')
    md_path = project / 'content' / 'guide.md'
    raw = md_path.read_bytes()
    markdown = raw.decode('utf-8-sig')
    r = GuideRenderer(project)
    parser = mistune.create_markdown(renderer=r, plugins=['table', 'strikethrough', 'task_lists', 'url'])
    content = parser(markdown)
    first = next((h for h in r.headings if h['level'] == 1), None)
    title_id = first['id'] if first else 'guide-title'
    if first:
        content = re.sub(r'<h1\b[^>]*>.*?</h1>\s*', '', content, count=1, flags=re.S)
    toc = '<ol class="generated-contents">' + ''.join(
        '<li><a href="#' + html.escape(h['id'], quote=True) + '">' + html.escape(re.sub(r'^\d+\.\s+', '', h['title'])) + '</a></li>'
        for h in r.headings if h['level'] == 2 and h['id'] != 'contents') + '</ol>\n'
    content = re.sub(r'(<h2 id="contents"[^>]*>.*?</h2>\s*).*?(?=<h2\b|\Z)',
                     lambda match: match.group(1) + toc, content, count=1, flags=re.S)
    css = (HERE / 'guide.css').read_text(encoding='utf-8')
    js = (HERE / 'guide.js').read_text(encoding='utf-8')
    highlighter = (HERE / 'highlight.min.js').read_text(encoding='utf-8').replace('</script', '<\\/script')
    library_nav = '<div class="app-navigation">' + ''.join('<a href="' + html.escape(x['href'], quote=True) + '">' + html.escape(x['name']) + '</a>' for x in (navigation or [])) + '</div>' if navigation else ''
    pack_url = html.escape(cfg.get('pack_url', 'https://drive.google.com/file/d/16qVAFl1TUB-T9-9idl6Qr5MdfIc6Sy1K/view?usp=sharing'), quote=True)
    pack_label = cfg.get('pack_label') or ('Get all seven New+ template packs on Google Drive' if cfg.get('pack_status') == 'current' else 'New+ template packs on Google Drive (check release version)')
    meta = {k: cfg[k] for k in allowed}
    meta['sha256'] = sha(raw)
    meta['source_filename'] = cfg.get('source_filename', 'guide.md')
    meta_json = json.dumps(meta, ensure_ascii=False).replace('<', '\\u003c')
    md_b64 = base64.b64encode(raw).decode('ascii')
    # Output path is fixed from config; it may not escape the project root.
    rel_path = cfg.get('output_file', 'dist/index.html')
    if output is None: output = project / rel_path
    output = output.resolve()
    if project.resolve() not in output.parents:
        raise SystemExit('Output path must remain inside the project directory')
    nav = make_nav(r.headings)
    escaped = lambda s: html.escape(s, quote=True)
    page = f'''<!doctype html>
<html lang="{escaped(cfg['language'])}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escaped(cfg['description'])}">
<meta name="author" content="{escaped(cfg['author'])}">
<meta name="generator" content="Offline Reference Guide Builder 3">
<meta name="source-revision" content="{escaped(cfg['revision'])}">
<title>{escaped(cfg['title'])} — Reference Guide</title>
<style>{css}</style>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="topbar">
  <button class="menu-button" id="menu-toggle" type="button" aria-label="Toggle contents" aria-expanded="false" aria-controls="sidebar">Contents</button>
  <div class="brand">AI Desktop Guides<small>{escaped(cfg['subtitle'])}</small></div>
  <div class="search-wrap"><label class="sr-only" for="guide-search">Search guide</label><input id="guide-search" type="search" placeholder="Search this guide (Ctrl+K)" aria-controls="search-results" autocomplete="off"><button id="clear-search" type="button" aria-label="Clear search" hidden>Clear</button></div>
  <div class="top-actions"><button type="button" id="theme-toggle">Dark</button><button type="button" id="download-source">Markdown</button><button type="button" id="print-guide">Print</button></div>
</header>
<div class="layout">
 <aside class="sidebar" id="sidebar">{library_nav}<nav aria-label="Table of contents"><h2>Contents</h2>{nav}</nav><p class="sidebar-note">Navigation is generated from Markdown headings. Editing content and rebuilding updates it automatically.</p></aside>
 <main class="main" id="main-content" tabindex="-1">
  <section class="intro">
   <h1 id="{escaped(title_id)}">{escaped(cfg['title'])}</h1><p>{escaped(cfg['description'])}</p>
   <div class="metadata"><span>Revision: {escaped(cfg['revision'])}</span><span>Verified: {escaped(cfg['verified_date'])}</span><span>Author: {escaped(cfg['author'])}</span><span>Root: <code>{escaped(cfg['root_baseline'])}</code></span><span>Source SHA-256: <code>{meta['sha256'][:12]}…</code></span></div>
  </section>
  <section id="search-results" class="search-results" aria-label="Search results" hidden><div class="results-head"><h2>Search results</h2><span id="search-count" role="status" aria-live="polite"></span></div><ol id="result-list"></ol></section>
  <article class="guide-content" id="guide-content">{content}</article>
  <footer class="footer"><p>Offline HTML reference guide. All styling, scripts, and Markdown source are embedded. External documentation links require an internet connection.</p><p><a href="{pack_url}" target="_blank" rel="noopener noreferrer">{pack_label}</a>. Check the package version before downloading.</p><p>Archive previous versions in <code>#Old</code> and temporary working files in <code>#Temp</code> within the authoring project.</p></footer>
 </main>
</div>
<div id="toast" class="toast" role="status" aria-live="polite" hidden></div>
<script id="guide-metadata" type="application/json">{meta_json}</script>
<script id="guide-markdown-source" type="application/octet-stream">{md_b64}</script>
<dialog id="diagram-dialog" aria-labelledby="diagram-dialog-title"><div class="dialog-bar"><h2 id="diagram-dialog-title">Diagram preview</h2><button type="button" id="close-diagram">Close</button></div><div id="dialog-art"></div></dialog>
<script>{highlighter}</script>
<script>{js}</script>
</body>
</html>
'''
    errors, warnings = validate_html(page, output, project)
    report = dict(project=str(project), output=str(output), source_sha256=sha(raw), markdown_bytes=len(raw),
                  headings=len(r.headings), code_blocks=r.code_count, mermaid_blocks=r.mermaid_count,
                  static_diagram_previews=r.preview_count,
                  validation_errors=errors, validation_warnings=warnings, notes=r.messages)
    if errors:
        print(json.dumps(report, indent=2, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(page)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default=str(ROOT), help='Project root with content/guide.md and guide.config.json')
    ap.add_argument('--output', help='Optional output HTML path within root')
    ap.add_argument('--json-report', action='store_true')
    a = ap.parse_args()
    r = build(Path(a.root).resolve(), Path(a.output) if a.output else None)
    if a.json_report: print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print('Built: ' + r['output'])
        print(f"Source: {r['markdown_bytes']} bytes; {r['headings']} headings; {r['code_blocks']} code blocks")
        if r['validation_warnings']:
            print('Warnings:')
            for w in r['validation_warnings']: print(' - ' + w)
        print('Offline HTML structure validation: PASS')

if __name__ == '__main__': main()
