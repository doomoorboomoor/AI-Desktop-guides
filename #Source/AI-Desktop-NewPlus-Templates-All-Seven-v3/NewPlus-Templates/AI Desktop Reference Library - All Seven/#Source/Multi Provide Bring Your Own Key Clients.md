Multi-Provider "Bring Your Own Key" (BYOK) desktop clients share **CommonMark + GitHub Flavored Markdown (GFM)** as their universal base syntax, allowing a single interface to render responses simultaneously from Anthropic, OpenAI, Google, OpenRouter, and local Ollama or vLLM endpoints.

Because these clients must unify incompatible upstream model behaviors in real time, they introduce specialized markup normalization layers not found in single-provider apps: **dual-delimiter LaTeX normalization**, **multi-engine diagram fences** (`mermaid`, `plantuml`, `graphviz`), **custom artifact XML wrappers** (such as ``<lobeArtifact>``), **hybrid YAML/Markdown agent pipelines**, and **direct third-party vault synchronization** (Obsidian, Notion, and WebDAV).

---

## 1. Master Markup Comparison: Multi-Provider "Bring Your Own Key" (BYOK) Clients

| Markup Layer | Cherry Studio | LobeChat Desktop | Witsy | Chatbox | Askimo | NextChat (ChatGPT-Next-Web) | ChatWise / BoltAI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Core Prose Markup** | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM (`remark-gfm` via `@lobehub/ui`) | CommonMark + GFM (`markdown-it`) | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM (CommonMark-Kotlin / JetBrains Markdown) | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM |
| **Inline Math Delimiter** | Both `$...$` and `\(...\)` (Auto-normalized) | Both `$...$` and `\(...\)` | Both `$...$` and `\(...\)` | Both `$...$` and `\(...\)` | `$...$` and `\(...\)` | `$...$` and `\(...\)` | Both `$...$` and `\(...\)` |
| **Block Math Delimiter** | Both `$$...$$` and `[...]` | Both `$$...$$` and `[...]` | Both `$$...$$` and `[...]` | Both `$$...$$` and `[...]` | `$$...$$` and `[...]` | `$$...$$` and `[...]` | Both `$$...$$` and `[...]` |
| **Math Rendering Engine** | KaTeX (`rehype-katex`) + configurable dollar-escape toggle | KaTeX (`rehype-katex`) | KaTeX (`markdown-it-katex` / `texmath`) | KaTeX (`rehype-katex`) | Native Kotlin LaTeX / KaTeX bridge | KaTeX (`rehype-katex`) | KaTeX |
| **Reasoning & Stream Markup** | Normalizes inline ``<think>`` / ``<thought>`` XML tags AND API `reasoning_content` / `thinking` JSON deltas into unified UI accordions | Intercepts custom ``<lobeThinking>`` and ``<think>`` XML tags + provider reasoning JSON deltas | Intercepts ``<think>`` XML tags + provider-native reasoning blocks | Intercepts ``<think>`` XML blocks and API reasoning deltas into collapsible cards | Parses multi-provider reasoning deltas + live CLI agent stdout streams | Intercepts ``<think>`` XML tags into collapsible thought drawers | Normalizes ``<think>`` XML tags and OpenAI/Anthropic reasoning chunks |
| **Tool Call & MCP Wire Markup** | **JSON-RPC 2.0** (MCP `stdio`, `sse`, `streamableHttp`) + multi-provider `tool_calls` JSON adapter | **JSON-RPC 2.0** (MCP) + Lobe Plugin JSON Manifests (`openapi` / JSON Schema) | **JSON-RPC 2.0** (Universal MCP client + Smithery.ai registry integration) | OpenAI/Anthropic JSON `tool_calls` + MCP client bridge | **JSON-RPC 2.0** (MCP `stdio` & `http`, scoped globally or per project) + CLI subprocess pipes | OpenAI `tool_calls` JSON + **OpenAPI 3.0 YAML/JSON** plugin schemas | **JSON-RPC 2.0** (MCP client) + native macOS App Intents / Shortcuts (BoltAI) |
| **Interactive Sandbox & Artifact Markup** | Code-fence driven live preview (````html`, ````svg`) + dedicated **Artifacts** preview drawer | Inline XML tags: ``<lobeArtifact identifier="..." type="..." title="...">`` wrapping React, SVG, HTML, or Markdown | Scratchpad interactive Markdown/code editor + inline HTML preview | Inline **Artifact** preview pane for ````html` and ````svg` code fences | Built-in **Script Runner** executing ````python`, ````bash`, and ````javascript` directly from chat in auto-virtualenvs | Sandboxed HTML/JS iframe preview for ````html` blocks | Live side-by-side **Artifacts** sandbox for HTML, CSS, React, and SVG |
| **Diagram Markup Support** | Native live rendering for **Mermaid** (````mermaid`), **PlantUML** (````plantuml`), and **Graphviz DOT** (````dot`) | Live renders ````mermaid` and ``<svg>`` inside chat and ``<lobeArtifact>`` panels | Live renders ````mermaid` diagrams with SVG/PNG export | Live renders ````mermaid` diagrams inline with zoom/pan controls | Renders ````mermaid` diagrams and structured execution pipeline visuals | Live renders ````mermaid` code blocks inline | Full live **Mermaid** rendering with adaptive theme styling |
| **Agent, Skill & Prompt Template Markup** | **Agents** (Markdown system prompts + preset JSON parameters) | **Agent Market JSON** schemas + Markdown system instructions | **Experts** (reusable Markdown system prompts) + **AI Commands** (`{selection}` text macros) | **My Copilots** (Markdown system prompt + JSON persona metadata) | **Skills** (`SKILL.md` following the Claude Skills spec) + **Plans** (multi-step pipelines defined in **YAML**) | **Masks** (`masks.json` containing role-play multi-turn Markdown message arrays + Handlebars variables) | System prompt templates with dynamic `{variable}` placeholders |
| **Local RAG & Knowledge Base Markup** | Built-in vector knowledge bases indexing `.md`, `.pdf`, `.docx`, URLs, and Sitemap XML with inline `[1]` citation chips | Knowledge Base file chunking + vector citations (PostgreSQL / PGlite / IndexedDB) | Local RAG document repositories (`.md`, `.pdf`, `.txt`, `.docx`) with source chunk injection | File/document context attachment parser + inline reference blocks | **Hybrid BM25 + Vector Local RAG** (Lucene/jvector) indexing local folders, `.md`, and URLs | Client-side file/text attachment chunking | Local PDF/Markdown document parsing with cited text spans |
| **Local Config & Storage Markup** | Local **IndexedDB / LevelDB** + JSON backup bundles + `mcpServers` JSON configuration | **IndexedDB / PGlite** (local WebAssembly Postgres) + JSON environment/settings export | Local `.json` settings files in OS application data folder (`mcpServers`, `experts.json`) | Single local JSON storage blob (`config.json`) + IndexedDB chat history | Local **SQLite** database + `SKILL.md` folders + YAML plan definitions | LocalStorage / IndexedDB + portable JSON backup files | **ChatWise**: Local **SQLite** DB; **BoltAI**: macOS **CoreData / SQLite** + `.plist` |
| **Code Fence Extensions** | Standard GFM info strings routed to **Shiki** + instant Run/Preview/Save buttons on fences | **Shiki** syntax highlighting with file-name header metadata and diff views | `highlight.js` syntax blocks + one-click OS clipboard/insert actions | Syntax-highlighted fences with inline HTML/Mermaid toggle switches | Executable code fences (`python`, `bash`, `js`) hooked to local script runner | `prismjs` / `highlight.js` syntax blocks with copy and sandbox preview buttons | **Shiki** syntax highlighting with line numbers and diff highlighting |
| **Host UI Rendering Markup** | **Electron**: Chromium HTML5 DOM + React + Ant Design + CSS3 | **Electron**: Chromium HTML5 DOM + Next.js + React + `@lobehub/ui` | **Electron**: Chromium HTML5 DOM + Vue 3 + CSS3 | **Electron / Tauri**: Chromium/OS WebView HTML5 DOM + React | **JetBrains Compose Multiplatform**: Native Kotlin + **Skia GPU canvas** (Zero Electron/Chromium overhead) | **Tauri (Rust + OS WebView)**: Ultra-lightweight (~5 MB) HTML5 DOM + React | **ChatWise**: **Tauri** (Rust + OS WebView); **BoltAI**: Native macOS **SwiftUI / AppKit** |
| **Clipboard & Vault Export Markup** | 1-click export to **Obsidian** (`obsidian://` URI or direct vault `.md` file write), **Notion**, **Yuque**, **WebDAV**, Markdown, PNG, or SVG | Exports raw `.md`, `.json` session state, or standalone shareable images | **Prompt Anywhere** (injects generated Markdown/text directly into active OS window) or copies `.md` | Exports threads as `.md`, `.txt`, `.json`, or standalone `.html` | Exports multi-step **Plans** and chats to `.md`, **PDF**, or **Word (`.docx`)** | Exports chats as `.md`, `.json`, or PNG image snapshots | Copies clean GFM Markdown (with configurable LaTeX delimiter conversion) or exports `.md` / `.pdf` |

---

## 2. Deep-Dive: Markup Architectures Specific to Multi-Provider BYOK Clients

Because BYOK clients sit between dozens of competing model APIs and your local desktop workflow, they solve three specific markup problems that official single-provider clients ignore.

### A. Real-Time Multi-Provider Math & Reasoning Normalization

When you run a side-by-side multi-model comparison in **Cherry Studio**, **ChatWise**, or **LobeChat**—sending the exact same prompt simultaneously to `claude-sonnet-4`, `gpt-4o` / `o3`, and a local `deepseek-r1` or `qwen3` model on Ollama/vLLM—the models return incompatible markup:

* **Math Delimiter Collisions:** OpenAI models emit `\(...\)` and `[...]`, while Anthropic and local open-weights models emit `$...$` and `$$...$$`. BYOK clients run a dual-pass AST preprocessor (`remark-math` configured with both single/double dollar and escaped parenthesis/bracket tokenizers) so both styles render identically via KaTeX in the same window. Furthermore, **Cherry Studio** includes a clipboard normalizer that converts `\(...\)` into `$...$` on copy so equations paste cleanly into Obsidian.
* **Reasoning Stream Unification:** DeepSeek and Qwen models on local servers stream raw ``<think>...</think>`` XML strings inside the standard message content delta, Anthropic streams structured `thinking` content blocks, and OpenAI streams `reasoning_content` JSON fields. BYOK clients normalize all three wire formats into a single unified AST node before rendering the collapsible thought accordion.

---

### B. Polyglot Diagram Rendering & XML Artifact Protocols (`<lobeArtifact>` vs. Code Fences)

BYOK clients provide significantly broader diagram-as-code markup support than official first-party apps:

1. **Multi-Engine Diagram Fences (Cherry Studio):**
While Claude Desktop and ChatGPT only recognize Mermaid (or require a Canvas HTML wrapper), **Cherry Studio** natively parses and renders three distinct diagram markup languages directly inside the chat stream:
* ````mermaid` for flowcharts, sequence diagrams, and Gantt charts.
* ````plantuml` (`@startuml ... @enduml`) for strict UML and C4 architecture diagrams.
* ````dot` / ````graphviz` (`digraph G { ... }`) for complex network topologies and state machines.


2. **LobeChat's `<lobeArtifact>` & `<lobeThinking>` XML Protocol:**
To bring Claude-style Artifacts to models that were never trained on Anthropic's proprietary ``<antArtifact>`` tags (such as GPT-4o, Gemini, or local Llama/Qwen models), **LobeChat Desktop** injects a unified XML specification into the system prompt and intercepts two custom tags in the stream:
```xml
<lobeThinking>
Calculating SVG viewBox coordinates and Tailwind layout...
</lobeThinking>
<lobeArtifact identifier="dsp-filter-ui" type="application/lobe.artifacts.react" title="Biquad Filter Visualizer">
import React, { useState } from 'react';
export default function FilterPlot() { ... }
</lobeArtifact>

```


Supported `type` attributes include `text/markdown`, `text/html`, `image/svg+xml`, `application/lobe.artifacts.mermaid`, and `application/lobe.artifacts.react`.

---

### C. Workflow Pipelines, Portable Skills & Obsidian Vault Sync

Several BYOK desktop apps extend Markdown into local automation and note-taking pipelines:

* **Askimo's Hybrid `SKILL.md` + YAML `Plans` Architecture:**
Askimo is built natively in Kotlin/Compose (avoiding Electron RAM overhead) and combines two distinct declarative markup standards:
* **Claude-Compatible `SKILL.md`:** Reads reusable Markdown skill files (YAML frontmatter + Markdown instructions) and can execute them by spawning local `Claude Code` or `Gemini CLI` sub-processes that read/write files and stream live activity back to the GUI.
* **Declarative YAML `Plans`:** Chains multi-step AI pipelines where each step passes its structured Markdown output to the next step before compiling the final deliverable into a clean `.md`, `.pdf`, or `.docx` report.


* **Cherry Studio's Direct Obsidian & WebDAV Vault Markup:**
Instead of manual copy-pasting, Cherry Studio integrates directly with local **Obsidian vaults** (writing `.md` files with YAML frontmatter tags, timestamps, and normalized `$...$` KaTeX math directly to your vault folder or via the `obsidian://` URI protocol) and supports automated **WebDAV** state synchronization across multiple desktop machines.
