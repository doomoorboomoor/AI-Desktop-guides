Autonomous Agent and Multi-Agent Desktop Workspaces share **CommonMark + GitHub Flavored Markdown (GFM)** for conversational streams and **YAML frontmatter + Markdown** (`SKILL.md`, `AGENTS.md`, `CLAUDE.md`) for portable agent instructions. However, because these applications orchestrate background subagents, isolated Git worktrees, container sandboxes, and local shell environments, they introduce four additional markup layers rarely seen in standard chat clients: **Declarative Subagent & Recipe YAML**, **Unified Diff & Search/Replace Patch blocks**, **Language Server Protocol (LSP) & Container schemas**, and **Pseudo-Terminal (PTY) ANSI escape sequences**.

---

## 1. Master Markup Comparison: Autonomous Agent & Multi-Agent Desktop Workspaces

| Markup Layer | Hermes Desktop (Nous Research) | Goose Desktop (Block) | OpenCode Desktop (SST / Anomaly) | Conductor | Sculptor (Imbue) | Nimbalyst / CodexMonitor / Vibe Kanban |
| --- | --- | --- | --- | --- | --- | --- |
| **Core Prose Markup** | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM | CommonMark + GFM | CommonMark + GFM | CommonMark + GFM + Kanban Card Markdown |
| **Inline Math Delimiter** | `$...$` and `\(...\)` | `$...$` and `\(...\)` | `$...$` | `$...$` and `\(...\)` (Depends on harness) | `$...$` and `\(...\)` | `$...$` and `\(...\)` |
| **Block Math Delimiter** | `$$...$$` and `[...]` | `$$...$$` and `[...]` | `$$...$$` | `$$...$$` and `[...]` | `$$...$$` and `[...]` | `$$...$$` and `[...]` |
| **Math Rendering Engine** | KaTeX (`rehype-katex`) | KaTeX | KaTeX / Custom WebView | KaTeX | KaTeX | KaTeX |
| **Reasoning & Stream Markup** | Intercepts inline ``<think>`` / ``<thought>`` XML tags and Nous tool-call tokens into UI accordions | Intercepts ``<think>`` XML tags + JSON-RPC stream chunks | Headless JSON stream (`opencode run --format json`) + ``<think>`` XML folding | Parses JSONL / stdout streams from parallel Claude Code, Codex, and Cursor harnesses | Parses subagent container stdout/stderr + JSON event streams | Parses multi-harness transcripts (Claude Code, Codex, OpenCode) into unified timeline nodes |
| **Tool Call, Subprocess & LSP Wire Markup** | **JSON-RPC 2.0** (MCP) + Hermes Gateway WebSocket JSON + cron schedule specs | **JSON-RPC 2.0** (MCP) + **MCP-UI** HTML/iframe extension schemas | **JSON-RPC 2.0** (MCP) + **LSP (Language Server Protocol)** JSON-RPC for real-time compiler/type diagnostics | Subprocess PTY JSONL streams (`--output-format stream-json`) + Git CLI RPC | Docker / Modal container RPC + **JSON-RPC 2.0** (MCP) + two-way filesystem sync events | Subprocess CLI JSONL bridges + Git worktree lock/status metadata |
| **Code Patching & Sandbox Markup** | Side-by-side HTML/JS/CSS/SVG **Artifact** preview + live local **Unified Diff** (`@@ -l,s +l,s @@`) | **MCP-UI** interactive DOM components + inline file-patch diffs | AST-aware `SEARCH/REPLACE` patch blocks + Split/Unified Diff views | Per-workspace isolated **Git Worktree Diff** panes + inline PR line-comment threads | Containerized **Unified Diff** viewer with branch pairing and live local IDE buffer sync | Visual Diff review panels + embedded **Monaco Editor** buffers + visual schema/mockup artifacts |
| **Diagram & Visual Artifact Markup** | Live renders ````mermaid`, ``<svg>``, and HTML in side-by-side preview pane | Live renders ````mermaid` blocks and MCP-UI visual cards | Syntax-highlighted code fences via **Shiki**; HTML preview via local server | Renders Markdown tables and diff graphs; delegates diagrams to code fences | Renders Markdown tables, container build graphs, and test-runner status trees | **Nimbalyst** natively renders ````mermaid`, data schemas, wireframes, and spreadsheets alongside code |
| **Agent Instructions & Context Markup** | `AGENTS.md`, `CLAUDE.md`, and persistent cross-session memory Markdown stores | `.goosehints` (project/global Markdown with `@file` imports) + `AGENTS.md` | `AGENTS.md`, `CLAUDE.md` (native fallback), and glob/URL `instructions` arrays | Inherits repository `CLAUDE.md`, `AGENTS.md`, and `.cursorrules` per worktree | Inherits `CLAUDE.md` and `AGENTS.md` inside each cloned container environment | Markdown **Plan Documents** (`plan.md`), `AGENTS.md`, `CLAUDE.md`, and issue-tracker Markdown |
| **Reusable Skill & Subagent Markup** | Self-authored `SKILL.md` (YAML frontmatter + GFM) or `skill.yaml` + Python/JS handler | **Goose Recipes** (`recipe.yaml` defining parallel subagents) + `SKILL.md` | `.opencode/agents/*.md` (Markdown with YAML frontmatter defining tools, model, and mode) | Executes subagent slash commands (`/add-dir`) and underlying harness `SKILL.md` files | `devcontainer.json` + `Dockerfile` + verification test-runner scripts | Harness-native `SKILL.md` + pluggable extension SDK manifests (Nimbalyst) |
| **Local Config & Ecosystem Markup** | **YAML**: `~/.hermes/config.yaml` (models, MCP servers, gateway, memory) | **YAML**: `~/.config/goose/config.yaml` (providers, extensions, MCP servers) | **JSON / JSONC**: `opencode.json` or `.opencode.json` + local **SQLite** session DB | Local SQLite state DB + JSON workspace metadata + `.env` per-worktree isolation | **JSON & Dockerfile**: `devcontainer.json`, `Dockerfile`, and Modal/Docker config YAML | Local **SQLite** / JSON project state + `.git/worktrees/` index files |
| **Terminal & Shell Stream Markup** | **ANSI / VT100 Escape Sequences** (`\x1b[...`) in integrated terminal + sandboxed Docker/SSH streams | **ANSI Escape Sequences** in collapsible shell execution blocks | **TUI / xterm.js ANSI Escape Sequences** + structured tool output blocks | Multi-pane **xterm.js ANSI** terminal streams (one PTY per Git worktree) | Container PTY **ANSI Escape Sequences** streamed from isolated Linux sandboxes | Integrated PTY **ANSI Escape Sequences** paired with per-card transcript logs |
| **Host UI Rendering Markup** | **Electron / Tauri WebView**: React HTML5 DOM + CSS3 + Monaco/CodeMirror diff views | **Electron**: React HTML5 DOM + `remark` / `rehype` AST pipeline | **Tauri (Rust + OS WebView)**: SolidJS / HTML5 DOM + **Shiki** syntax engine | **macOS Native / Electron Hybrid**: HTML5 DOM + native Git worktree diff views | **Electron**: HTML5 DOM + Docker container orchestration dashboard | **Electron / Tauri + Monaco**: HTML5 DOM + full tabbed Monaco Editor (Nimbalyst) |
| **Git & File Export Markup** | Writes raw `.md`, code files, and self-generated `SKILL.md` bundles directly to disk or Git | Direct filesystem mutation + `.yaml` recipe export + `.md` session export | Direct filesystem edits + `/undo` Git-backed state rollback + `.json` CI logs | Creates isolated Git branches (`git worktree add`), commits, and merges GitHub PRs | Syncs container branch diffs back to local Git repo or pushes PRs directly | One-click Git worktree branch merge, `.patch` export, or Markdown plan export |

---

## 2. Deep-Dive: Markup Architectures Specific to Autonomous & Multi-Agent Workspaces

Unlike first-party chat clients where markup primarily formats human-readable answers, autonomous and multi-agent desktop workspaces use markup as **executable orchestration code**.

### A. Declarative Subagent & Recipe Markup (`recipe.yaml` vs. `.opencode/agents/*.md` vs. `SKILL.md`)

Multi-agent workspaces rely on structured declarative files to spawn parallel subagents with restricted permissions, separate models, and scoped tools:

* **OpenCode Desktop (`.opencode/agents/<name>.md`):** Defines specialized agents (such as `Build`, `Plan`, `Explore`, or `Scout`) using **YAML frontmatter inside a Markdown file** committed to the repository:
```markdown
---
description: "Read-only architecture and security auditor"
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
---
You are a read-only codebase auditor. Analyze the AST and LSP diagnostics without modifying files.

```


* **Goose Desktop (`recipe.yaml` & `.goosehints`):** While Goose supports `SKILL.md`, its multi-agent **Research -> Plan -> Implement (RPI)** loop is driven by **YAML Recipes** that spawn parallel subagents (`find_files`, `analyze_code`, `find_patterns`), paired with `.goosehints` Markdown files that support `@path/to/file.md` context injection.
* **Hermes Desktop (`SKILL.md` & `skill.yaml`):** Hermes uniquely treats skill markup as **bidirectional (read/write)**. After completing a complex task, the Hermes Agent autonomously serializes its successful trajectory into a new `SKILL.md` (or `skill.yaml` + Python handler) inside your local skills directory so future sessions can reuse or refine the workflow without re-prompting.

---

### B. Multi-Agent Isolation & Environment Markup (Git Worktrees vs. `devcontainer.json`)

When running 3 to 10 autonomous coding agents simultaneously on the same repository, agents will overwrite each other's files if they share a working directory. Multi-agent desktop apps solve this using two distinct configuration and filesystem markup models:

1. **Git Worktree Metadata (`.git/worktrees/` + Per-Worktree `.env`):** Used by **Conductor**, **Nimbalyst**, **CodexMonitor**, **Vibe Kanban**, and **OpenCode Desktop**. Each agent task spawns an isolated directory linked to the repository's `.git` object database on a dedicated branch (for example, `session/refactor-dsp`). All diffs are rendered in the desktop GUI using **Unified Diff markup** (`@@ -14,6 +14,12 @@`) before being merged into `main`.
2. **Container Spec Markup (`devcontainer.json` + `Dockerfile`):** Used by **Sculptor (Imbue)** and **Hermes Desktop (Docker/Modal mode)**. Rather than sharing the host OS runtime (where parallel agents can collide on localhost ports or shared databases), Sculptor provisions each agent inside an isolated container defined by a standard **Development Container JSON (`devcontainer.json`)** manifest and syncs only approved Unified Diff hunks back to your local IDE.

---

### C. Compiler & LSP Feedback Markup (Real-Time Self-Correction)

A major architectural differentiator in **OpenCode Desktop** (and IDE-linked workspaces like **Nimbalyst**) is **Language Server Protocol (LSP) JSON-RPC integration**:

* When an agent edits a Python, Rust, or TypeScript file, OpenCode immediately queries the local language server (`pyright`, `rust-analyzer`, `tsserver`) over **JSON-RPC 2.0**.
* Compiler errors, line numbers, and type mismatches are serialized into structured diagnostic blocks and injected directly back into the agent's context window within the same turn, allowing the model to fix broken imports or type errors before rendering the final Markdown response to the user.
