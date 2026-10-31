(() => {
'use strict';
const byId = id => document.getElementById(id);
const search = byId('guide-search');
const results = byId('search-results');
const searchCount = byId('search-count');
const resultList = byId('result-list');
const clearSearch = byId('clear-search');
const root = byId('guide-content');
const toast = byId('toast');
const sidebar = byId('sidebar');
const menu = byId('menu-toggle');
const themeButton = byId('theme-toggle');
let toastTimer;
function notice(value) { toast.textContent = value; toast.hidden = false; clearTimeout(toastTimer); toastTimer = setTimeout(() => { toast.hidden = true; }, 2500); }
function setTheme(mode) {
  document.documentElement.dataset.theme = mode;
  themeButton.textContent = mode === 'dark' ? 'Light' : 'Dark';
  themeButton.setAttribute('aria-label', mode === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  try { localStorage.setItem('newplus-guide-theme', mode); } catch (_) {}
}
let preferred = 'light';
try { preferred = localStorage.getItem('newplus-guide-theme') || 'light'; } catch (_) {}
setTheme(preferred);
themeButton.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));
byId('print-guide').addEventListener('click', () => window.print());
menu.addEventListener('click', () => { const open = sidebar.classList.toggle('is-open'); menu.setAttribute('aria-expanded', String(open)); });
sidebar.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  sidebar.classList.remove('is-open'); menu.setAttribute('aria-expanded', 'false');
  if (a.getAttribute('href').startsWith('#')) { const target = byId(decodeURIComponent(a.hash.slice(1))); if (target) requestAnimationFrame(() => { target.tabIndex=-1; target.focus({preventScroll:true}); }); }
}));
function openAnchorNav() {
  if (!location.hash) return;
  const id = decodeURIComponent(location.hash.slice(1));
  for (const a of sidebar.querySelectorAll('a[href^="#"]')) {
    if (a.getAttribute('href') === '#' + id) { a.closest('details')?.setAttribute('open', ''); break; }
  }
}
window.addEventListener('hashchange', openAnchorNav);
openAnchorNav();
// Tables are wide on small screens; wrappers are inserted without altering their contents.
for (const table of root.querySelectorAll('table')) {
  if (table.parentElement.classList.contains('table-wrap')) continue;
  const wrap = document.createElement('div'); wrap.className = 'table-wrap'; wrap.tabIndex = 0; wrap.setAttribute('role','region'); wrap.setAttribute('aria-label','Reference table; scroll horizontally if needed');
  table.parentNode.insertBefore(wrap, table); wrap.appendChild(table);
}
const sections = [];
const nodes = Array.from(root.children);
for (let i = 0; i < nodes.length; i++) {
  const h = nodes[i];
  if (!/^H[23]$/.test(h.tagName)) continue;
  const level = Number(h.tagName.slice(1));
  let text = h.textContent.replace(/#$/, '').trim() + ' ';
  for (let j = i + 1; j < nodes.length; j++) {
    const el = nodes[j];
    if (/^H[1-6]$/.test(el.tagName) && Number(el.tagName.slice(1)) <= level) break;
    text += ' ' + el.textContent;
  }
  sections.push({ id: h.id, title: h.textContent.replace(/#$/, '').trim(), content: text.replace(/\s+/g, ' ').trim() });
}
function appendMarked(parent, value, terms) {
  if (!terms.length) { parent.textContent = value; return; }
  const regex = new RegExp('(' + [...new Set(terms)].map(v => v.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'ig');
  let last = 0;
  for (const match of value.matchAll(regex)) {
    parent.append(document.createTextNode(value.slice(last, match.index)));
    const mark = document.createElement('mark'); mark.textContent = match[0]; parent.append(mark);
    last = match.index + match[0].length;
  }
  parent.append(document.createTextNode(value.slice(last)));
}
function runSearch() {
  const query = search.value.trim().toLocaleLowerCase();
  const terms = query.split(/\s+/).filter(Boolean);
  clearSearch.hidden = !query;
  results.hidden = !query;
  resultList.replaceChildren();
  if (!query) { searchCount.textContent = ''; return; }
  const hits = sections.filter(s => terms.every(t => s.content.toLocaleLowerCase().includes(t)));
  searchCount.textContent = hits.length + ' matching section' + (hits.length === 1 ? '' : 's');
  for (const item of hits) {
    const li = document.createElement('li'), link = document.createElement('a');
    link.href = '#' + item.id;
    const title = document.createElement('strong'), excerpt = document.createElement('span');
    appendMarked(title, item.title, terms);
    const lower = item.content.toLocaleLowerCase();
    let first = terms.reduce((best, t) => { const idx = lower.indexOf(t); return idx >= 0 && (best < 0 || idx < best) ? idx : best; }, -1);
    if (first < 0) first = 0;
    const start = Math.max(0, first - 54), end = Math.min(item.content.length, first + 155);
    appendMarked(excerpt, (start ? '…' : '') + item.content.slice(start, end) + (end < item.content.length ? '…' : ''), terms);
    link.append(title, excerpt); li.append(link); resultList.append(li);
  }
  if (!hits.length) { const li = document.createElement('li'); li.textContent = 'No results. Try fewer words.'; li.className = 'no-results'; resultList.append(li); }
}
search.addEventListener('input', runSearch);
clearSearch.addEventListener('click', () => { search.value = ''; runSearch(); search.focus(); });
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); search.focus(); search.select(); }
  if (e.key === 'Escape' && !byId('diagram-dialog').open) {
    if (sidebar.classList.contains('is-open')) { sidebar.classList.remove('is-open'); menu.setAttribute('aria-expanded','false'); menu.focus(); }
    else if (document.activeElement === search) { search.value=''; runSearch(); }
  }
});
async function copyText(value) {
  try { if (!navigator.clipboard) throw Error('Clipboard API unavailable'); await navigator.clipboard.writeText(value); return true; }
  catch (_) {
    const field = document.createElement('textarea'); field.value = value; field.style.position = 'fixed'; field.style.left = '-9999px';
    document.body.append(field); field.select(); let success = false;
    try { success = document.execCommand('copy'); } catch (_) {} field.remove(); return success;
  }
}
root.querySelectorAll('.copy-code').forEach(btn => btn.addEventListener('click', async () => {
  const code = btn.closest('.code-box').querySelector('code');
  notice(await copyText(code.textContent) ? 'Code copied' : 'Copy unavailable; select the code manually');
}));
byId('download-source').addEventListener('click', () => {
  try {
    const cfg = JSON.parse(byId('guide-metadata').textContent);
    const encoded = byId('guide-markdown-source').textContent.trim();
    const binary = atob(encoded); const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    const file = new Blob([bytes], {type:'text/markdown;charset=utf-8'});
    const link = document.createElement('a'); link.href = URL.createObjectURL(file);
    link.download = String(cfg.source_filename || 'guide.md').replace(/[\\/:*?"<>|]/g, '-');
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    notice('Markdown source download started');
  } catch (_) { notice('Markdown download unavailable in this browser'); }
});

for (const code of root.querySelectorAll('pre code')) {
  const language=[...code.classList].find(x=>x.startsWith('language-'))?.slice(9);
  if (window.hljs && language && hljs.getLanguage(language)) hljs.highlightElement(code);
}
const diagramDialog=byId('diagram-dialog'), dialogArt=byId('dialog-art'); let diagramTrigger=null, printSources=null;
function closeDiagram() { if(diagramDialog.open) diagramDialog.close(); dialogArt.replaceChildren(); if(diagramTrigger?.isConnected) diagramTrigger.focus({preventScroll:true}); diagramTrigger=null; }
byId('close-diagram').addEventListener('click',closeDiagram);
diagramDialog.addEventListener('close',()=>{dialogArt.replaceChildren(); if(diagramTrigger?.isConnected) diagramTrigger.focus({preventScroll:true}); diagramTrigger=null;});
for (const image of root.querySelectorAll('.diagram-preview')) {
  const button=document.createElement('button'); button.type='button'; button.className='expand-diagram'; button.textContent='Expand diagram';
  image.closest('.diagram').querySelector('.diagram-label').append(button);
  const expand=()=>{diagramTrigger=button; const full=image.cloneNode(true); full.className='expanded-preview';dialogArt.replaceChildren(full);diagramDialog.showModal();byId('close-diagram').focus();};
  button.addEventListener('click',expand); image.addEventListener('click',expand);
}
window.addEventListener('beforeprint',()=>{closeDiagram(); if(!printSources)printSources=[...document.querySelectorAll('.diagram-source')].map(e=>[e,e.open]); printSources.forEach(([e])=>{e.open=true;});});
window.addEventListener('afterprint',()=>{printSources?.forEach(([e,open])=>{e.open=open;});printSources=null;});
window.guideReady=true;
})();
