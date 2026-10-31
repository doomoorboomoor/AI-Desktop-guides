Every official first-party desktop client and agent application is built on a shared foundation of **CommonMark + GitHub Flavored Markdown (GFM)** for visible text tokens, **fenced code blocks with language identifiers** (`python`, `rust`, `json`, `bash`) for syntax highlighting, and **YAML frontmatter + Markdown** (`SKILL.md`, `AGENTS.md`, `CLAUDE.md`) for reusable agent instructions.

The comprehensive reference below breaks down every markup language, delimiter specification, stream protocol, and configuration format used across the seven official first-party desktop apps, arranged side-by-side to highlight their architectural similarities and differences.

---

## 1. Master Markup Comparison: Official First-Party Clients & Agent Apps

| Markup Layer | Claude Desktop (Anthropic) | Claude Code Desktop (Anthropic) | ChatGPT Desktop (OpenAI) | Codex Desktop (OpenAI) | Gemini Desktop (Google) | Microsoft Copilot (Microsoft) | Perplexity Desktop (Perplexity) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Core Prose Markup** | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM + Terminal ANSI | CommonMark + GFM | CommonMark + GFM | CommonMark + GFM | CommonMark + GFM | CommonMark + GFM + Footnote Syntax |
| **Inline Math Delimiter** | `$...$` (Pandoc / Obsidian standard) | `$...$` | `\(...\)` (Default); `$...$` (Fallback) | `\(...\)` and `$...$` | `$...$` (Strict spacing required) | `$...$` | `$...$` and `\(...\)` |
| **Block Math Delimiter** | `$$...$$` | `$$...$$` | `[...]` (Default) and `$$...$$` | `[...]` and `$$...$$` | `$$...$$` | `$$...$$` and `[...]` | `$$...$$` and `[...]` |
| **Math Rendering Engine** | KaTeX (`rehype-katex`) | KaTeX | KaTeX (macOS bridges to native TextKit) | KaTeX | KaTeX / Custom Web Components | KaTeX | KaTeX |
| **Reasoning & Stream Markup** | Inline XML tags: ``<antThinking>`` or API `thinking` content blocks | Inline XML ``<antThinking>`` + real-time JSON stream events | Out-of-band JSON SSE (`reasoning_content` delta chunks) | Out-of-band JSON SSE + execution trace logs | Out-of-band JSON stream chunks (`thought` metadata flag) | Out-of-band JSON SSE (`Deep Think` state payloads) | Out-of-band JSON SSE + ``<think>`` XML for DeepSeek/R1 models |
| **Tool Call & MCP Wire Markup** | Anthropic XML tool blocks (``<antml:function_calls>``) bridged to **JSON-RPC 2.0** (MCP) | Anthropic XML tool blocks + **JSON-RPC 2.0** (MCP) + PTY stdin/stdout | OpenAI JSON Schema `tool_calls` array + Companion App IPC JSON | OpenAI JSON Schema `tool_calls` + **JSON-RPC 2.0** (MCP) + Git worktree RPC | Protobuf / JSON `functionCall` payloads + Google Workspace API schemas | JSON Schema `tool_calls` + Windows Action / MS Graph JSON | Internal JSON search/retrieval payloads (No local tool execution) |
| **Interactive Sandbox & Artifact Markup** | Inline ``<antArtifact>`` XML wrapping HTML5, SVG, Mermaid, JSX (React + Tailwind), or Markdown | Native Split/Unified Diff AST panes + terminal **ANSI Escape Codes** (`\x1b[...`) | **Canvas** JSON state transitions wrapping React/HTML/Tailwind or Python plots | Multi-file **Unified Diff** (`@@ -l,s +l,s @@`), file-tree patches, and terminal ANSI | **Canvas / Antigravity** JSON blocks wrapping HTML5/JS/CSS or Google Docs/Sheets XML | **Copilot Pages** collaborative blocks + **Adaptive Cards JSON** for Windows UI cards | Static code blocks in chat; source web snapshots rendered in side-panel WebView |
| **Diagram Markup Support** | Live renders ````mermaid` and raw ``<svg>`` inside the Artifacts panel | Raw syntax-highlighted code for Mermaid; native visual Git diff graphs | Raw code in standard chat; live rendered only if wrapped in a **Canvas** HTML block | Raw code in chat; visual commit/worktree branch graphs in UI | Live renders charts in Canvas; raw fenced code for ````mermaid` | Raw fenced code for ````mermaid` | Raw fenced code for ````mermaid` |
| **Agent Instructions & Skill Markup** | `SKILL.md` (YAML frontmatter + Markdown) & XML-structured Project instructions | `CLAUDE.md` (hierarchical Markdown), `.claude/commands/*.md`, and `SKILL.md` | Plain-text / Markdown *Custom Instructions* + GPT Builder JSON schemas | `AGENTS.md` (root/nested Markdown) + `SKILL.md` (YAML frontmatter + Markdown) | *Gems* (Markdown system instructions) + `.idx/airules.md` / `GEMINI.md` | Declarative Agent JSON manifests + Markdown system prompts | *Spaces* instructions (Markdown system prompt + pinned local files) |
| **Local Config & MCP File Markup** | Strict **JSON**: `claude_desktop_config.json` (No comments or trailing commas) | **JSON**: `~/.claude/settings.json` and project `.mcp.json` | Cloud-synced JSON preferences + macOS `.plist` / Windows Registry | **TOML**: `~/.codex/config.toml` (Supports `#` comments, profiles, & MCP servers) | Cloud-synced JSON profile; `.gemini/settings.json` for CLI/Antigravity bridge | Windows Registry / MSIX `AppxManifest.xml` + cloud-synced JSON | Local `settings.json` + IndexedDB / SQLite local cache |
| **Code Fence Extensions** | Standard GFM info strings (````python`) routed to Shiki/Prism | Path-tagged fences + Unified Diff hunks | Standard GFM info strings + Companion App file-context badges | File-path headers + Git worktree diff metadata | Standard GFM info strings + direct export hooks to Colab / Replit / Docs | Standard GFM info strings | Standard GFM info strings |
| **Citation & Grounding Markup** | Inline JSON-backed citation spans + MCP resource URIs (`file://`, `mcp://`) | Local relative file paths (`src/main.rs:42`) clickable to IDE/buffer | Inline citation pills (`【4:0†source】` internally) rendered as hover badges | Clickable file-path and line-number anchors (`path/to/file.py#L10-L25`) | Google Search Grounding spans + Workspace `@Drive` / `@Gmail` entity chips | Numbered superscript citation badges (`[1]`) linked to Bing/Graph JSON | Native Markdown-style bracket citations (`[1]`, `[2]`) mapped to source URLs |
| **Host UI Rendering Markup** | **Electron**: Chromium HTML5 DOM + CSS3 (`remark` / `rehype` AST pipeline) | **Electron**: Chromium HTML5 DOM + `xterm.js` WebGL/Canvas terminal | **macOS**: Native SwiftUI / AppKit TextKit 2; **Windows**: WebView2 HTML5 DOM | **Electron / Native Hybrid**: HTML5 DOM + GPU-accelerated diff/terminal views | **WebView2 (Win) / WebKit-CEF (macOS)**: Lit / Material Web Components DOM | **WinUI 3 + WebView2**: XAML outer shell hosting Chromium HTML5 DOM | **Electron / Native Wrapper**: React HTML5 DOM + Tailwind CSS |
| **Clipboard & Export Markup** | Copies raw GFM (`$...$` math) or styled HTML; downloads `.md`, `.svg`, `.tsx`, `.html` | Copies raw Unified Diff patches, raw code, or commits directly to local Git | Copies GFM with `\(...\)` / `\[...\]` math; Canvas exports `.md`, `.py`, `.pdf`, `.docx` | Applies patches directly to local Git worktree or exports `.patch` / `.diff` | Copies rich HTML/Markdown; 1-click export to Google Docs (ODF/OOXML) or Gmail | Copies GFM or rich HTML; exports directly to Word (`.docx`), Excel (`.xlsx`), PowerPoint | Exports full threads as clean `.md` (with Footnote citations), `.pdf`, or share links |

---

## 2. Deep-Dive: Exact Syntax & Structural Differences

While the table above maps every layer, three specific markup differences directly affect how prompts, mathematical notes, and local configurations behave across these seven clients.

### A. Stream & Artifact Wrapping: Anthropic Inline XML vs. OpenAI/Google JSON SSE

* **Claude Desktop & Claude Code Desktop** embed structural markup directly inside the token generation stream using reserved XML namespaces:
```xml
<antThinking>
Evaluating the transfer function H(s) before generating the plot...
</antThinking>
<antArtifact identifier="bode-plot" type="application/vnd.ant.code" language="python" title="Bode Plot Generator">
import numpy as np
</antArtifact>

```


Because these tags exist in the token stream, Claude also responds exceptionally well when *you* use custom XML tags (such as `<context>`, `<constraints>`, `<input_data>`) in your user prompts.
* **ChatGPT, Codex, Gemini, and Copilot** do **not** emit XML tags inside the text stream for UI control. Instead, they emit pure GFM Markdown inside a JSON Server-Sent Event (SSE) delta stream, triggering their side panels (Canvas, Antigravity, Copilot Pages) via out-of-band JSON tool calls:
```json
{"event": "canvas.update", "type": "code/python", "content": "import numpy as np\n..."}

```



### B. Agent Instruction & Configuration Markup: `CLAUDE.md` vs. `AGENTS.md` vs. `config.toml`

First-party agent apps have converged on Markdown for project-level instructions, but their local configuration markup differs strictly:

* **Claude Desktop (`claude_desktop_config.json`) & Claude Code (`.claude/settings.json`):** Uses strict **JSON**. Even a single trailing comma or `//` comment breaks the MCP server loader. Project context is stored in `CLAUDE.md`, while reusable skills use `.claude/skills/<skill-name>/SKILL.md` (YAML frontmatter + GFM body).
* **Codex Desktop (`~/.codex/config.toml`):** Uses **TOML** for its core configuration, making it far more resilient to manual editing and inline `#` comments:
```toml
model = "o3"
approval_policy = "on-request"

[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/Workspace"]

```


For repository instructions, Codex reads hierarchical `AGENTS.md` files (from root down to subdirectories) alongside `.codex/skills/*/SKILL.md`.

### C. Mathematical & Citation Copy-Paste Behavior (Vault Compatibility)

* **Direct Obsidian / Pandoc Compatibility:** **Claude Desktop**, **Claude Code Desktop**, **Gemini Desktop**, and **Microsoft Copilot** output `$inline$` and `$$display$$` math delimiters by default. Copying a response via the built-in "Copy" button yields Markdown that renders immediately in Obsidian.
* **LaTeX Escaping Friction:** **ChatGPT Desktop** and **Codex Desktop** default to `\(...\)` for inline math and `\[...\]` for display math in their raw Markdown clipboard output (to prevent accidental math rendering when discussing dollar currency or bash variables like `$PATH`).
* **Citation Footnotes:** **Perplexity Desktop** injects bracketed numeric anchors (`[1]`, `[2]`) directly into the Markdown prose and appends a reference list at the bottom on export, whereas **ChatGPT** and **Gemini** strip or convert their hover-pill citations into standard Markdown links (`[Source](https://...)`) when copied.
