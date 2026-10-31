#!/usr/bin/env python3
"""Rebuild the complete offline library from its canonical Markdown; Python 3.9+."""
from pathlib import Path
import importlib.util, json, html, re, shutil, sys
ROOT=Path(__file__).resolve().parent
ENGINE=ROOT/'Authoring/engine'
sys.path.insert(0,str(ENGINE/'vendor'))
import mistune
spec=importlib.util.spec_from_file_location('guide_engine',ENGINE/'guide_builder.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
APPS=json.loads((ROOT/'Authoring/applications.json').read_text('utf-8'))
DRIVE='https://drive.google.com/file/d/16qVAFl1TUB-T9-9idl6Qr5MdfIc6Sy1K/view?usp=sharing'
H=lambda value:html.escape(str(value),quote=True)
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(value,bytes):path.write_bytes(value)
 else:
  with path.open('w',encoding='utf-8',newline='\n') as f:f.write(value)


def tokens(source):return mistune.create_markdown(renderer='ast')(source)


def plain(token):
 if 'raw'in token:return token['raw']
 return ''.join(plain(x) for x in token.get('children',[]))


def index_entries(source,slug,name):
 seen=set();entries=[];current=None
 for t in tokens(source):
  if t['type']=='heading':
   title=plain(t);base=engine.safe_slug(title);identifier=base;i=2
   while identifier in seen:identifier=f'{base}-{i}';i+=1
   seen.add(identifier)
   current={'id':identifier,'guide':slug,'guideName':name,'heading':title,'text':title,'level':t['attrs']['level']};entries.append(current)
  elif current is not None:current['text']+=' '+plain(t)
 return entries


def master(folder,entries,stats):
 css=(ENGINE/'guide.css').read_text('utf-8')+MASTER_CSS
 distribution_path=folder/'Authoring/distribution.json'
 distribution=json.loads(distribution_path.read_text('utf-8')) if distribution_path.exists() else {'status':'current'}
 pending=distribution.get('status')!='current'
 drive_link=distribution.get('drive_url',DRIVE)
 notice='<p class="distribution-note"><strong>Confirm the download version.</strong> The saved distribution settings are not marked current. Check that the selected Drive ZIP contains this release, then update Authoring/distribution.json and rebuild. Editing a setting does not upload a ZIP.</p>' if pending else ''
 local_zip='AI-Desktop-NewPlus-Templates-All-Seven-v3.zip'
 # Downloads use the Drive URLs saved in Authoring/distribution.json.
 cards=''.join(f'<article class="guide-card"><h2><a href="{slug}.html">{H(name)}</a></h2><p>{H(description)}</p><p class="baseline">Root baseline: <code>{H(baseline)}</code></p><a class="read-link" href="{slug}.html">Read the complete guide</a></article>' for slug,name,baseline,filename,description in APPS)
 packs=''
 for slug,name,baseline,filename,description in APPS:
  pack=distribution.get('app_packs',{}).get(slug,{})
  url=pack.get('url',drive_link)
  zipname=pack.get('filename','AI-Desktop-NewPlus-Templates-All-Seven-v3.zip')
  packs+=f'<article class="pack-card"><h3>{H(name)} pack</h3><p>Three complete New+ entries: the offline HTML manual, an editable Markdown-first guide project, and an Atlas workspace using <code>{H(baseline)}</code>.</p><p class="pack-location">Separate app ZIP: <code>{H(zipname)}</code>. Extract it, then copy the three entries inside <code>NewPlus-Templates/</code> or use its included installer.</p><a href="{H(url)}" target="_blank" rel="noopener noreferrer">Download {H(name)} pack (ZIP)</a></article>'
 nav=''.join(f'<a href="{slug}.html">{H(name)}</a>' for slug,name,baseline,filename,description in APPS)
 data=json.dumps({'entries':entries,'pages':{a[0]:a[0]+'.html' for a in APPS}},ensure_ascii=False).replace('<','\\u003c')
 body=f'''<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Seven complete desktop application manuals and PowerToys New+ template packs."><title>AI Desktop Guides · Complete Library</title><style>{css}</style></head><body>
<a class="skip-link" href="#main-content">Skip to content</a><header class="topbar"><button id="menu-toggle" class="menu-button" aria-controls="sidebar" aria-expanded="false">Menu</button><a class="brand" href="index.html">AI Desktop Reference Library<small>Seven complete application manuals</small></a><div class="search-wrap"><label class="sr-only" for="guide-search">Search all seven guides</label><input type="search" id="guide-search" placeholder="Search all seven guides" aria-controls="search-results"><button id="clear-search" hidden>Clear</button></div><div class="top-actions"><button id="theme-toggle">Dark</button><button id="print-guide">Print index</button></div></header>
<div class="layout"><aside class="sidebar" id="sidebar"><nav aria-label="Library navigation"><h2>Applications</h2><div class="app-navigation">{nav}</div><div class="app-navigation"><a href="#template-packs">New+ template packs</a><a href="#using-newplus">How to use New+</a></div></nav><p class="sidebar-note">All seven manuals are complete and self-contained. Keep the HTML files together for local navigation.</p></aside><main class="main" id="main-content" tabindex="-1">
<section class="intro"><h1>AI Desktop guides</h1><p>Project instructions, markup conventions, and context management. Read a complete manual, or create a reusable guide or Atlas workspace with PowerToys New+.</p><div class="metadata"><span>7 applications</span><span>{stats['headings']} searchable sections</span><span>{stats['code_blocks']} code examples</span><span>{stats['diagrams']} diagrams</span><span>Collection updated 31 October 2026</span></div></section>
<section id="search-results" class="search-results" hidden aria-label="Search results"><div class="results-head"><h2>Search results</h2><span id="search-count" role="status" aria-live="polite"></span></div><ol id="result-list"></ol></section>
<section class="library-section" aria-labelledby="guide-list-title"><h2 id="guide-list-title">Choose an application</h2><div class="guide-grid">{cards}</div></section>
<section class="library-section" id="template-packs" aria-labelledby="packs-title"><h2 id="packs-title">New+ template packs</h2><div class="bundle-panel"><div><h3>All seven apps in one ZIP</h3><p>The combined collection includes <strong>24 New+ entries</strong>: seven complete guide HTML files, seven editable guide projects, seven Atlas workspaces, the complete reference library, a blank HTML guide, and a generic authoring project. One additional dated authoring project is optional.</p><p>Choose the complete collection here, or download one app using its separate ZIP card below. The combined ZIP also includes original sources, build tools, licenses, and validation results.</p></div><a class="primary-link" href="{H(DRIVE)}" target="_blank" rel="noopener noreferrer">Open all templates on Google Drive</a></div><div class="pack-grid">{packs}</div></section>
<section class="library-section howto" id="using-newplus" aria-labelledby="using-title"><h2 id="using-title">How to use the packs with New+</h2><ol><li><strong>Download and extract the whole ZIP.</strong> Use the complete collection link or an app's separate ZIP card, then extract to a normal folder. Do not run scripts inside a ZIP preview.</li><li><strong>Enable PowerToys New+.</strong> Open PowerToys Settings and enable New+. Reading the guides requires neither PowerToys nor Python.</li><li><strong>Install the templates.</strong> Read the extracted README, then run <code>Install-NewPlus-Templates.cmd</code>. It skips existing same-named entries. To refresh matching entries with backups, run <code>.\\Install-NewPlus-Templates.ps1 -Overwrite</code> from the extracted folder.</li><li><strong>Or copy selected entries manually.</strong> Choose <strong>New+ → Open templates</strong> in File Explorer and copy the desired items from <code>NewPlus-Templates/</code> into that folder. Copy its contents, not the enclosing directory.</li><li><strong>Create a guide or workspace.</strong> Right-click an empty area in your destination folder, choose <strong>New+</strong>, then select a complete guide, an editable source project, an Atlas workspace, or the full library. New+ creates a copy.</li><li><strong>Edit and rebuild when needed.</strong> In an editable guide project, change <code>content/guide.md</code> and <code>guide.config.json</code>, then run <code>Build-Guide.cmd</code>. Python 3.9+ is needed only for rebuilding. The full library has <code>Build-Library.cmd</code> for rebuilding every guide and the master from its saved Markdown sources.</li></ol><p><code>#Old/</code> stores previous revisions; <code>#Temp/</code> stores temporary work. They are not active source directories. Optional dated templates require New+'s filename-variable setting; variables change names, not file contents. The installer does not enable settings, sign into AI applications, or connect accounts.</p><p><a href="https://learn.microsoft.com/en-us/windows/powertoys/newplus" target="_blank" rel="noopener noreferrer">Microsoft's New+ documentation</a> · <a href="README.md">Local library maintenance guide</a></p></section>
<footer class="footer"><p>The original manuals retain their product-verification dates. This collection's HTML/build checks do not establish native app installation or account entitlement. All reading features work offline; Google Drive and external documentation require internet access.</p></footer></main></div>
<script id="library-search-data" type="application/json">{data}</script><script>{MASTER_JS}</script></body></html>'''
 body=body.replace('<h2 id="packs-title">New+ template packs</h2>','<h2 id="packs-title">New+ template packs</h2>'+notice)
 body=body.replace(H(DRIVE),H(drive_link))
 if pending:body=body.replace('Open all templates on Google Drive','Open Drive ZIP (verify version)')
 write(folder/'index.html',body)

MASTER_CSS='\n.brand{text-decoration:none}.library-section{max-width:1120px;margin:42px 0 50px;scroll-margin-top:140px}.library-section>h2{font-size:28px;color:var(--ink);letter-spacing:-.5px;margin:0 0 22px}.guide-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.guide-card{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:24px;display:flex;flex-direction:column;align-items:start;gap:12px}.guide-card h2{font-size:23px;line-height:1.3;margin:0}.guide-card h2 a{text-decoration:none}.guide-card h2 a:hover{text-decoration:underline}.guide-card p{margin:0;color:var(--muted);font-size:14px}.guide-card .baseline{font-size:12px}.read-link{margin-top:auto;font-size:14px;font-weight:650}.bundle-panel{background:var(--tint);border:1px solid var(--line);border-left:5px solid var(--accent);padding:25px;margin-bottom:22px}.bundle-panel h3{font-size:23px;color:var(--ink);margin:0 0 12px}.bundle-panel p{font-size:14px;max-width:83ch}.primary-link{display:inline-block;padding:10px 16px;border-radius:5px;background:#245bc6;color:white;font-size:14px;font-weight:650;text-decoration:none}.primary-link:hover{background:#183f90}.pack-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.pack-card{padding:22px;background:var(--paper);border:1px solid var(--line);border-radius:6px;display:flex;flex-direction:column;align-items:start}.pack-card h3{margin:0 0 12px;font-size:20px;color:var(--ink)}.pack-card p{font-size:14px;margin:0 0 14px}.pack-card .pack-location{font-size:12px;color:var(--muted)}.pack-card a{margin-top:auto;font-size:14px;font-weight:650}.howto{background:var(--paper);border:1px solid var(--line);padding:28px;border-radius:6px}.howto li{padding-left:5px;margin:15px 0;max-width:83ch}.howto p{font-size:14px;max-width:83ch}code{font-family:Consolas,monospace;overflow-wrap:anywhere}#result-list .result-app{font-size:12px;color:var(--accent)}.footer{display:block}\n@media(max-width:600px){.guide-grid,.pack-grid{grid-template-columns:1fr}.guide-card,.pack-card{padding:20px}.bundle-panel,.howto{padding:20px}.guide-card h2{font-size:22px}.library-section>h2{font-size:26px}.brand{min-width:0}.brand small{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}\n@media print{.guide-grid,.pack-grid{display:block}.guide-card,.pack-card{break-inside:avoid;margin-bottom:12px}.library-section{margin:25px 0}.bundle-panel,.howto{border:1px solid #aaa}.primary-link{color:#153c75;background:none;padding:0}.guide-card h2{font-size:15pt}.pack-card h3{font-size:13pt}.footer{display:block!important}}\n'
MASTER_JS="(()=>{const data=JSON.parse(document.getElementById('library-search-data').textContent),byId=id=>document.getElementById(id),input=byId('guide-search'),results=byId('search-results'),list=byId('result-list'),clear=byId('clear-search'),menu=byId('menu-toggle'),sidebar=byId('sidebar'),theme=byId('theme-toggle');function setTheme(mode){document.documentElement.dataset.theme=mode;theme.textContent=mode==='dark'?'Light':'Dark';theme.setAttribute('aria-label',mode==='dark'?'Switch to light theme':'Switch to dark theme');try{localStorage.setItem('newplus-guide-theme',mode);}catch{}}try{setTheme(localStorage.getItem('newplus-guide-theme')||'light');}catch{setTheme('light');}theme.addEventListener('click',()=>setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark'));function closeMenu(focus){sidebar.classList.remove('is-open');menu.setAttribute('aria-expanded','false');if(focus)menu.focus();}menu.addEventListener('click',()=>{const open=sidebar.classList.toggle('is-open');menu.setAttribute('aria-expanded',String(open));if(open)sidebar.querySelector('a')?.focus();});function search(){const q=input.value.trim().toLowerCase(),words=q.split(/\s+/).filter(Boolean);list.replaceChildren();clear.hidden=!q;results.hidden=!q;if(!q){byId('search-count').textContent='';return;}const matches=data.entries.filter(x=>words.every(w=>(x.guideName+' '+x.heading+' '+x.text).toLowerCase().includes(w)));byId('search-count').textContent=matches.length+' matching sections';for(const x of matches){const li=document.createElement('li'),a=document.createElement('a'),app=document.createElement('span'),title=document.createElement('strong'),excerpt=document.createElement('span');a.href=data.pages[x.guide]+'#'+x.id;app.className='result-app';app.textContent=x.guideName;title.textContent=x.heading;const text=x.text.replace(/\s+/g,' '),pos=Math.max(0,text.toLowerCase().indexOf(words[0]));excerpt.textContent=(pos>60?'…':'')+text.slice(Math.max(0,pos-60),pos+170)+'…';a.append(app,title,excerpt);li.append(a);list.append(li);}if(!matches.length){const li=document.createElement('li');li.textContent='No results. Try a filename, command, or fewer words.';list.append(li);}}input.addEventListener('input',search);clear.addEventListener('click',()=>{input.value='';search();input.focus();});document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();input.focus();input.select();}if(e.key==='Escape'){if(sidebar.classList.contains('is-open'))closeMenu(true);else{input.value='';search();}}});sidebar.addEventListener('click',e=>{const a=e.target.closest('a');if(a){closeMenu(false);if(a.getAttribute('href').startsWith('#')){const target=byId(a.hash.slice(1));if(target)requestAnimationFrame(()=>{target.tabIndex=-1;target.focus({preventScroll:true});});}}});byId('print-guide').addEventListener('click',()=>window.print());window.libraryReady=true;})();"

def main():
    reports=[];entries=[]
    distribution=json.loads((ROOT/'Authoring/distribution.json').read_text('utf-8'))
    for app in APPS:
        slug,name,baseline,filename,description=app
        source=ROOT/'#Source'/filename
        if not source.is_file():raise SystemExit('Missing canonical source: '+str(source))
        project=ROOT/'#Temp/library-build'/slug
        write(project/'content/guide.md',source.read_bytes())
        config=json.loads((ROOT/'Authoring/config'/(slug+'.json')).read_text('utf-8'))
        pack=distribution.get('app_packs',{}).get(slug,{})
        config['pack_url']=pack.get('url',distribution['drive_url']);config['pack_status']=distribution['status']
        config['pack_label']='Download '+name+' New+ template pack (ZIP)' if pack else 'Get all seven New+ template packs on Google Drive'
        write(project/'guide.config.json',json.dumps(config,ensure_ascii=False,indent=2)+'\n')
        shutil.copytree(ROOT/'Authoring/diagrams'/slug,project/'assets/diagrams',dirs_exist_ok=True)
        nav=[{'name':'Master index and template packs','href':'index.html'}]+[{'name':a[1],'href':a[0]+'.html'} for a in APPS if a[0]!=slug]
        output=project/'dist/index.html'
        report=engine.build(project,output,navigation=nav)
        write(ROOT/(slug+'.html'),output.read_bytes())
        reports.append(report)
        entries+=index_entries(source.read_text('utf-8'),slug,name)
    stats={'headings':sum(r['headings'] for r in reports),'code_blocks':sum(r['code_blocks'] for r in reports),'diagrams':sum(r['mermaid_blocks'] for r in reports)}
    master(ROOT,entries,stats)
    result={'applications':len(APPS),'stats':stats,'source_hashes':{app[0]:report['source_sha256'] for app,report in zip(APPS,reports)}}
    write(ROOT/'#Temp/last-build.json',json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
