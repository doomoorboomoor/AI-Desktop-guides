Local-First LLM Runners and All-in-One Workspaces share **CommonMark + GitHub Flavored Markdown (GFM)** for visible chat output, but they introduce an entire lower-level markup layer that cloud clients hide on remote servers: **raw model prompt templating** (Jinja2, Go templates, and special control tokens like ``<|im_start|>``), **constrained decoding grammars** (GBNF and JSON Schema), and **local RAG chunking and vector metadata schemas**.

---

## 1. Master Markup Comparison: Local-First LLM Runners & All-in-One Workspaces

| Markup Layer | LM Studio | AnythingLLM Desktop | Msty Studio | Jan | GPT4All (Nomic) | Ollama (Desktop GUI) | KoboldCpp (Desktop GUI) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Core Prose Markup** | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM (`remark-gfm`) | CommonMark + GFM | CommonMark + GFM | CommonMark + GFM + Raw HTML/CSS (Optional) |
| **Inline Math Delimiter** | `$...$` and `\(...\)` | `$...$` and `\(...\)` | `$...$` and `\(...\)` | `$...$` and `\(...\)` | `$...$` | `$...$` and `\(...\)` | `$...$` and `\(...\)` |
| **Block Math Delimiter** | `$$...$$` and `[...]` | `$$...$$` and `[...]` | `$$...$$` and `[...]` | `$$...$$` and `[...]` | `$$...$$` | `$$...$$` and `[...]` | `$$...$$` and `[...]` |
| **Math Rendering Engine** | KaTeX (`rehype-katex`) | KaTeX | KaTeX | KaTeX (`rehype-katex`) | Qt RichText / KaTeX bridge | KaTeX | KaTeX |
| **Low-Level Prompt Template Markup** | **Jinja2** (`tokenizer.chat_template` embedded in GGUF metadata) or manual prefix/suffix strings | Automatic provider/GGUF **Jinja2** template resolution + system prompt wrappers | Visual turn-template editor + GGUF **Jinja2** templates | **Jinja2** / Handlebars (`prompt_template` inside `model.yaml` or GGUF header) | **Jinja2** (`{% for message in messages %}`) stored in model metadata | **Go `text/template**` (`{{ .System }}`, `{{ .Prompt }}`, `{{ .Response }}`) inside `Modelfile` | **JSON Instruct / Jinja2** adapters (ChatML, Alpaca, Llama-3, Mistral) |
| **Special Control Token Markup** | `` `< | im_start | >```, ```< | begin_of_text | >```, ```< | eot_id | >` `` (Rendered in token inspector) |
| **Reasoning & Stream Markup** | Intercepts ``<think>...</think>`` XML tags into collapsible UI blocks; exposes `reasoning_content` in API | Intercepts ``<think>`` / ``<thought>`` XML tags into collapsible thought accordions | Automatic ``<think>`` XML detection with real-time token/sec reasoning counters | Intercepts ``<think>`` / ``<thought>`` XML blocks into collapsible UI cards | Renders ``<think>`` blocks inline or folds via Jinja2 template rules | Parses ``<think>`` XML tags into dedicated collapsible thinking sections | Folds ``<think>`` tags or exposes raw reasoning tokens for manual editing |
| **Constrained Output & Grammar Markup** | **JSON Schema** (`response_format`) compiled under the hood to `llama.cpp` **GBNF** (`root ::= ...`) | JSON Schema enforcement for agent tool calls | **JSON Schema** structured output templates | JSON Schema `response_format` via Cortex `llama.cpp` engine | Internal JSON grammar for tool/LocalDocs parsing | **JSON Schema** passed via `format` parameter (compiled to GBNF) | Direct **GBNF (GGML BNF)** grammar rules + JSON Schema |
| **Tool Call & MCP Wire Markup** | **JSON-RPC 2.0** via `~/.lmstudio/mcp.json` + OpenAI-compatible `tool_calls` JSON | **JSON-RPC 2.0** (MCP) + native `plugin.json` & Node.js `handler.js` runtime | **Msty Toolbox** (**JSON-RPC 2.0** MCP client) + local script execution | **JSON-RPC 2.0** (MCP) + OpenAI `tool_calls` JSON | Local Python/JS tool bridges (Limited MCP support) | OpenAI/Ollama JSON `tools` array (`function` schema definitions) | OpenAI-compatible `tool_calls` JSON + WebSearch JSON hooks |
| **Diagram & Sandbox Markup** | Renders ````mermaid` and HTML previews; raw code fences via Shiki | Live renders ````mermaid` diagrams and HTML/SVG blocks | Live renders ````mermaid` diagrams + **Artifacts** side-panel (HTML/JS/CSS/SVG) | Live renders ````mermaid` diagrams and syntax-highlighted code blocks | Syntax-highlighted code blocks and basic GFM tables only (No iframe sandbox) | Syntax-highlighted code fences and GFM tables (Minimalist native chat UI) | Live HTML/CSS/JS canvas rendering + Mermaid support in built-in WebUI |
| **Local RAG & Knowledge Base Markup** | Local document parser (`.md`, `.pdf`, `.txt`, `.docx`) with inline citation pills | Workspace vector chunks (LanceDB / Qdrant / Chroma) + `@agent` document citations | **Knowledge Stacks** (Folder watch, single-file or multi-chunk indexing, Jina web Markdown, reranker scores) | Local RAG attachment parser with inline source chunk citations | **LocalDocs** (SQLite + Nomic Embed) automatic folder/Markdown `.md` sync with footnote citations | Native file/image drag-and-drop context injection (No built-in persistent vector DB GUI) | World Info / Lorebook JSON keyword-triggered context injection |
| **Presets, Skills & Model Manifest Markup** | `.preset.json` (System prompt, `n_ctx`, `temperature`, sampling, and Jinja overrides) | `plugins/agent-skills/{hubId}/plugin.json` (`skill-1.0.0` schema) + `handler.js` + Slash commands | **Prompts Studio** templates (Handlebars-style `{variable}` placeholders) & Persona JSONs | `model.yaml` / `model.json` manifests inside `~/jan/models/` | `.json` model configuration cards | Declarative **`Modelfile`** (`FROM`, `PARAMETER`, `SYSTEM`, `TEMPLATE`, `ADAPTER`) | `.kcpps` (JSON settings bundle) + SillyTavern Character Card PNG/JSON metadata |
| **Local Config & Storage Markup** | JSON files in `~/.lmstudio/` (`mcp.json`, `settings.json`, conversation `.json` trees) | Local **SQLite** DB (`anythingllm.db`) + `anythingllm_mcp_servers.json` + vector store files | Local **SQLite** / LevelDB storage + JSON export bundles | Pure flat-file directory structure (`~/jan/threads/*/messages.jsonl` & `.json`) | Local **SQLite** database + `.json` preferences | Local **SQLite** chat history (`~/.ollama/`) + binary manifest blobs | Single portable `.kcpps` JSON config + local `.json` chat logs |
| **Host UI Rendering Markup** | **Electron**: Chromium HTML5 DOM + React + CSS3 | **Electron**: Chromium HTML5 DOM + React + Tailwind CSS | **Electron / Tauri Hybrid**: Chromium HTML5 DOM + multi-pane split-chat CSS grid | **Electron**: Chromium HTML5 DOM + React (`remark` / `rehype` AST pipeline) | **Qt6 / QML**: Native C++ declarative UI markup (Zero Chromium/Electron overhead) | **macOS**: Native SwiftUI; **Windows**: Native Go/WebView2 lightweight wrapper | **C++ / Python Tkinter** launcher + self-hosted Vanilla JS/HTML5 DOM client |
| **Clipboard & Export Markup** | Copies raw GFM; exports conversations as structured `.json` or `.md` | Exports workspace chats as `.md`, `.json`, `.csv`, or fine-tuning `.jsonl` datasets | Exports split-chat comparisons as `.md`, `.json`, or shareable HTML snapshots | Copies GFM; threads exist directly on disk as standard `.jsonl` / `.md` | Copies raw GFM text or exports chat logs | Copies raw GFM or code block contents | Exports full context/chat as `.json`, `.txt`, or `.md` |

---

## 2. Deep-Dive: Markup Layers Exclusive to Local-First Runners

Unlike cloud-only desktop clients where your Markdown is simply sent over HTTPS as a JSON string, local-first runners must translate human Markdown into raw tokenizer arrays and hardware-level grammar constraints on your machine.

### A. Low-Level Prompt Template Markup: Jinja2 vs. Ollama `Modelfile` Go Templates

Local GGUF/EXL2 models do not inherently understand a JSON array of messages; they only understand a single continuous string of tokens punctuated by model-specific control markup. Local desktop apps use two different templating languages to build that string:

1. **Jinja2 (`chat_template` in LM Studio, Jan, GPT4All, AnythingLLM):**
Embedded directly inside the GGUF file header (and editable in LM Studio's *Prompt Template* tab), Jinja2 loops over your Markdown messages and wraps them in the exact control tokens the model was trained on:
```jinja2
{% for message in messages %}
<|im_start|>{{ message['role'] }}
{{ message['content'] }}<|im_end|>
{% endfor %}
{% if add_generation_prompt %}
<|im_start|>assistant
{% endif %}

```


2. **Go `text/template` (Ollama `Modelfile`):**
Ollama uses a Dockerfile-inspired declarative format (`Modelfile`) paired with Go's standard `text/template` syntax rather than Jinja2:
```dockerfile
FROM llama3.3:70b
PARAMETER temperature 0.2
PARAMETER num_ctx 32768
SYSTEM """You are a precise systems engineering assistant."""
TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""

```



---

### B. Constrained Decoding Grammar Markup: GBNF (`llama.cpp` Backends)

When you ask a local model in **LM Studio**, **Ollama**, **Jan**, or **KoboldCpp** to output valid JSON or call an MCP tool, smaller quantized models can occasionally hallucinate a trailing comma or wrap the JSON in unwanted Markdown backticks.

* To prevent this mathematically at the sampling layer, these runners compile a **JSON Schema** into **GBNF (GGML Backus-Naur Form)** markup:
```ebnf
root   ::= object
value  ::= object | array | string | number | ("true" | "false" | "null") ws
object ::= "{" ws ( string ":" ws value ("," ws string ":" ws value)* )? "}" ws

```


* During token generation, the `llama.cpp` backend masks out any vocabulary token logits that violate the GBNF grammar rule, guaranteeing 100% syntactically valid JSON or XML tool markup even on 7B/8B parameter models.

---

### C. Custom Agent Skill & Preset Markup (`plugin.json` vs. `.preset.json` vs. `mcp.json`)

Each local runner uses its own configuration schema for extending capabilities:

* **AnythingLLM (`plugin.json` + `handler.js`):** In addition to standard `anythingllm_mcp_servers.json` for MCP, AnythingLLM uses a dedicated local skill manifest schema (`"schema": "skill-1.0.0"`) located in `storage/plugins/agent-skills/<hubId>/plugin.json`. This JSON file defines both the LLM tool arguments (`examples`, `params`) and the dynamic UI input fields (`setup_args`) that AnythingLLM automatically renders in its settings panel.
* **LM Studio (`mcp.json` & `.preset.json`):** Uses `~/.lmstudio/mcp.json` (following the exact same `"mcpServers"` JSON structure as Claude Desktop's `claude_desktop_config.json`) so you can symlink or copy MCP server blocks directly between Claude Desktop and LM Studio. Inference and prompt configurations are stored separately as portable `.preset.json` files.
* **Msty Studio (Knowledge Stacks & Prompts Studio):** Uses curly-brace variable interpolation (`{variable_name}`) inside reusable prompt templates, and indexes local Markdown vaults using configurable chunking strategies (including **Single-Chunk File mode**, which preserves an entire `.md` note as one undivided context unit rather than splitting mid-paragraph or mid-equation).
