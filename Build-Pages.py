#!/usr/bin/env python3
"""Build an allowlisted GitHub Pages site; keep offline exports self-contained."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SITE = ROOT / '_site'


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.urls = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate ID: ' + attrs['id'])
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.urls.append(attrs[key])


def write(name, text):
    path = SITE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(text)


def asset(text, suffix):
    name = 'assets/' + hashlib.sha256(text.encode()).hexdigest()[:16] + suffix
    write(name, text)
    return name


def optimize(text):
    text = re.sub(r'<style>(.*?)</style>', lambda m: '<link rel="stylesheet" href="' + asset(m[1], '.css') + '">', text, flags=re.S)
    # Only executable scripts are extracted; embedded source and search JSON stay intact.
    text = re.sub(r'<script>(.*?)</script>', lambda m: '<script defer src="' + asset(m[1], '.js') + '"></script>', text, flags=re.S)
    text = text.replace('href="README.md"', 'href="publishing.html"')
    text = text.replace('All styling, scripts, and Markdown source are embedded.', 'Shared styling and scripts are cached between guides. Markdown source is embedded.')
    text = text.replace('All reading features work offline;', 'For offline reading, use the standalone HTML exports;')
    return text


def validate():
    pages = {p.name: Links(p.read_text('utf-8')) for p in SITE.glob('*.html')}
    errors = []
    checked = 0
    for name, page in pages.items():
        for url in page.urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path) or name
            if path.startswith('/') or '\\' in path or '..' in Path(path).parts:
                errors.append(f'{name}: nonportable URL {url}')
                continue
            target = SITE / path
            if not target.is_file():
                errors.append(f'{name}: missing {url}')
            elif parsed.fragment and path in pages and unquote(parsed.fragment) not in pages[path].ids:
                errors.append(f'{name}: missing fragment {url}')
            checked += 1
    data_text = (SITE / 'index.html').read_text('utf-8')
    data = json.loads(re.search(r'<script id="library-search-data" type="application/json">(.*?)</script>', data_text, re.S)[1])
    for entry in data['entries']:
        target = data['pages'][entry['guide']]
        if target not in pages or entry['id'] not in pages[target].ids:
            errors.append('Invalid search destination: ' + target + '#' + entry['id'])
    if errors:
        raise SystemExit('\n'.join(errors))
    return {'html_pages': len(pages), 'local_links_checked': checked, 'search_destinations_checked': len(data['entries'])}


def main():
    subprocess.run([sys.executable, str(ROOT / 'Build-Library.py')], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # Remove only this builder's prior generated files, without recursive deletion.
    SITE.mkdir(exist_ok=True)
    for path in SITE.glob('*.html'):
        path.unlink()
    if (SITE / 'assets').exists():
        for path in (SITE / 'assets').iterdir():
            if path.is_file():
                path.unlink()
    apps = json.loads((ROOT / 'Authoring/applications.json').read_text('utf-8'))
    names = ['index.html'] + [app[0] + '.html' for app in apps]
    before = sum((ROOT / name).stat().st_size for name in names)
    for name in names:
        write(name, optimize((ROOT / name).read_text('utf-8')))
    # Retain old URLs, including their section fragments, after filename normalization.
    for old, new in {'claude-code-Desktop.html': 'claude-code.html'}.items():
        redirect = 'location.replace(' + json.dumps(new) + '+location.search+location.hash);'
        write(old, '<!doctype html><html lang="en"><meta charset="utf-8"><title>Guide moved</title><meta name="robots" content="noindex"><p>This guide has moved. <a href="' + new + '">Continue to the guide</a>.</p><script src="' + asset(redirect, '.js') + '"></script></html>')
    write('publishing.html', '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Library maintenance</title><main><h1>Library maintenance</h1><p>Edit the numbered Markdown guides in #Source, then run <code>python Build-Pages.py</code> to rebuild and validate the website. Standalone offline guides are generated in the repository root.</p><p><a href="https://github.com/doomoorboomoor/AI-Desktop-guides">Source repository and publishing instructions</a></p><p><a href="index.html">Return to the library</a></p></main></html>')
    write('404.html', '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · AI Desktop Guides</title><main><h1>Page not found</h1><p>The guide may have moved. Browse or search the library.</p><p><a href="https://doomoorboomoor.github.io/AI-Desktop-guides/">Open AI Desktop Guides</a></p></main></html>')
    write('.nojekyll', '')
    report = validate()
    after = sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())
    report.update(standalone_bytes=before, published_bytes=after, shared_assets=len(list((SITE / 'assets').iterdir())))
    (ROOT / '#Temp/pages-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
