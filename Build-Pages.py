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
import html
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = ROOT / '_site'
CONFIG = json.loads((ROOT / 'Authoring/site.json').read_text('utf-8'))
BASE = CONFIG['url']
if not BASE.startswith('https://') or not BASE.endswith('/') or urlsplit(BASE).query or urlsplit(BASE).fragment:
    raise ValueError('Authoring/site.json url must be an absolute HTTPS URL ending in /')


def crawler_metadata(text, name, app=None):
    canonical = BASE + ('' if name == 'index.html' else name)
    title = CONFIG['name'] + ' | AI Application Reference Library' if app is None else app[1] + ' Guide | ' + CONFIG['name']
    description = CONFIG['description'] if app is None else f'{app[1]} reference guide: {app[4]}. Explore project instructions, Markdown examples, context workflows, troubleshooting, and reusable templates.'
    text = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title) + '</title>', text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*">', '', text)
    tags = '<meta name="description" content="' + html.escape(description, quote=True) + '">'
    tags += '<link rel="canonical" href="' + html.escape(canonical, quote=True) + '">'
    tags += '<meta name="robots" content="index,follow">'
    tags += '<link rel="sitemap" type="application/xml" href="sitemap.xml">'
    for key, value in {'og:type': 'website' if app is None else 'article', 'og:site_name': CONFIG['name'], 'og:title': title, 'og:description': description, 'og:url': canonical}.items():
        tags += '<meta property="' + key + '" content="' + html.escape(value, quote=True) + '">'
    tags += '<meta name="twitter:card" content="summary">'
    schema = {'@context': 'https://schema.org', '@type': 'WebSite' if app is None else 'TechArticle', 'name': title, 'url': canonical, 'description': description, 'inLanguage': 'en'}
    tags += '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
    if name == 'index.html' and CONFIG.get('google_site_verification'):
        tags += '<meta name="google-site-verification" content="' + html.escape(CONFIG['google_site_verification'], quote=True) + '">'
    return text.replace('</head>', tags + '</head>', 1)


def sitemap(names):
    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', namespace)
    root = ET.Element('{' + namespace + '}urlset')
    for name in names:
        entry = ET.SubElement(root, '{' + namespace + '}url')
        ET.SubElement(entry, '{' + namespace + '}loc').text = BASE + ('' if name == 'index.html' else name)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n')
    # On a project Pages site this is a template: crawlers consult the HOST root.
    write('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: ' + BASE + 'sitemap.xml\n')


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.urls = set(), []
        self.canonicals, self.meta = [], {}
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href'))
        if tag == 'meta' and 'name' in attrs:
            self.meta[attrs['name']] = attrs.get('content', '')
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
    text = text.replace('</head>', '<link rel="icon" type="image/svg+xml" href="favicon.svg"></head>', 1)
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
    expected = [BASE] + [BASE + name for name in data['pages'].values()]
    locations = [node.text for node in ET.parse(SITE / 'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if locations != expected:
        errors.append('Sitemap must list exactly the homepage and seven canonical guides')
    for url in expected:
        name = 'index.html' if url == BASE else url.removeprefix(BASE)
        page = pages[name]
        if page.canonicals != [url] or page.meta.get('robots') != 'index,follow' or not page.meta.get('description'):
            errors.append('Invalid crawler metadata: ' + name)
        text = (SITE / name).read_text('utf-8')
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)[1])
        if schema.get('url') != url:
            errors.append('Structured data URL mismatch: ' + name)
    for name in ('404.html', 'publishing.html', 'claude-code-Desktop.html'):
        if 'noindex' not in pages[name].meta.get('robots', ''):
            errors.append('Utility page must be noindex: ' + name)
    for entry in data['entries']:
        target = data['pages'][entry['guide']]
        if target not in pages or entry['id'] not in pages[target].ids:
            errors.append('Invalid search destination: ' + target + '#' + entry['id'])
    if errors:
        raise SystemExit('\n'.join(errors))
    return {'html_pages': len(pages), 'local_links_checked': checked, 'search_destinations_checked': len(data['entries']), 'sitemap_urls_checked': len(locations)}


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
        app = next((app for app in apps if app[0] + '.html' == name), None)
        write(name, crawler_metadata(optimize((ROOT / name).read_text('utf-8')), name, app))
    sitemap(names)
    write('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#245bc6"/><path d="M15 17h15c5 0 8 2 8 5v26c-3-3-6-4-11-4H15zm34 0H38v31c3-3 6-4 11-4z" fill="white"/></svg>')
    # Retain old URLs, including their section fragments, after filename normalization.
    for old, new in {'claude-code-Desktop.html': 'claude-code.html'}.items():
        redirect = 'location.replace(' + json.dumps(new) + '+location.search+location.hash);'
        write(old, '<!doctype html><html lang="en"><meta charset="utf-8"><title>Guide moved</title><meta name="robots" content="noindex"><p>This guide has moved. <a href="' + new + '">Continue to the guide</a>.</p><script src="' + asset(redirect, '.js') + '"></script></html>')
    write('publishing.html', '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Library maintenance</title><main><h1>Library maintenance</h1><p>Edit the numbered Markdown guides in #Source, then run <code>python Build-Pages.py</code> to rebuild and validate the website. Standalone offline guides are generated in the repository root.</p><p><a href="https://github.com/doomoorboomoor/AI-Desktop-guides">Source repository and publishing instructions</a></p><p><a href="index.html">Return to the library</a></p></main></html>')
    write('404.html', '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · AI Desktop Guides</title><main><h1>Page not found</h1><p>The guide may have moved. Browse or search the library.</p><p><a href="https://doomoorboomoor.github.io/AI-Desktop-guides/">Open AI Desktop Guides</a></p></main></html>')
    write('.nojekyll', '')
    for name in ('publishing.html', '404.html'):
        path = SITE / name
        text = path.read_text('utf-8').replace('<title>', '<meta name="robots" content="noindex,follow"><title>', 1)
        write(name, text)
    report = validate()
    after = sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())
    report.update(standalone_bytes=before, published_bytes=after, shared_assets=len(list((SITE / 'assets').iterdir())))
    (ROOT / '#Temp/pages-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
