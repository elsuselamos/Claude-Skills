# Obsidian Visual Skills Pack

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)](#status)

**[中文文档](README_CN.md)**

Visual Skills Pack for Obsidian: generate Canvas, Excalidraw, and Mermaid diagrams from text with Claude Code.

## Status

> **Status: Experimental**
>
> - This is a public prototype that works for my demos, but does not yet cover all input scales and edge cases.
> - Output quality varies based on model version and input structure; results may fluctuate.
> - My primary focus is demonstrating how tools and systems work together, not maintaining this codebase.
> - If you encounter issues, please submit a reproducible case (input + output file + steps to reproduce).

## What Are Skills?

Skills are prompt-based extensions for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that give Claude specialized capabilities. Unlike MCP servers that require complex setup, skills are simple markdown files that Claude loads on demand.

## Included Skills

### 1. Excalidraw Diagram Generator

Generate hand-drawn style diagrams directly in Obsidian using the Excalidraw plugin. Creates `.md` files with embedded Excalidraw JSON that opens natively in Obsidian.

**Supported Diagram Types:**

| Type | Best For |
|------|----------|
| **Flowchart** | Step-by-step processes, workflows, task sequences |
| **Mind Map** | Concept expansion, topic categorization, brainstorming |
| **Hierarchy** | Org charts, content levels, system decomposition |
| **Relationship** | Dependencies, influences, interactions between elements |
| **Comparison** | Side-by-side analysis of approaches or options |
| **Timeline** | Event progression, project milestones, evolution |
| **Matrix** | 2D categorization, priority grids, positioning |
| **Freeform** | Scattered ideas, initial exploration, free-form notes |

**Key Features:**
- Auto-saves `.md` files ready for Obsidian Excalidraw plugin
- Hand-drawn aesthetic with Excalifont (fontFamily: 5)
- Full Chinese text support with proper character handling
- Consistent color palette and styling guidelines

**Trigger words:** `Excalidraw`, `diagram`, `flowchart`, `mind map`, `画图`, `流程图`, `思维导图`, `可视化`

### 2. Mermaid Visualizer

Transform text content into professional Mermaid diagrams optimized for presentations and documentation. Includes built-in syntax error prevention for common pitfalls.

**Supported Diagram Types:**
- **Process Flow** (graph TB/LR) - Workflows, decision trees, AI agent architectures
- **Circular Flow** - Cyclic processes, feedback loops, continuous improvement
- **Comparison Diagram** - Before/after, A vs B analysis, traditional vs modern
- **Mindmap** - Hierarchical concepts, knowledge organization
- **Sequence Diagram** - Component interactions, API calls, message flows
- **State Diagram** - System states, status transitions, lifecycle stages

**Key Features:**
- Built-in syntax error prevention (list conflicts, subgraph naming, special characters)
- Configurable layouts: vertical/horizontal, simple/standard/detailed
- Professional color schemes with semantic meaning
- Compatible with Obsidian, GitHub, and other Mermaid renderers

**Trigger words:** `Mermaid`, `visualize`, `flowchart`, `sequence diagram`, `可视化`

### 3. Obsidian Canvas Creator

Create interactive Obsidian Canvas (`.canvas`) files with MindMap or freeform layouts. Outputs valid JSON Canvas format that opens directly in Obsidian.

**Layout Modes:**

| Mode | Structure | Best For |
|------|-----------|----------|
| **MindMap** | Radial hierarchy from center | Brainstorming, topic exploration, hierarchical content |
| **Freeform** | Custom positioning, flexible connections | Complex networks, non-hierarchical content, custom arrangements |

**Key Features:**
- Smart node sizing based on content length
- Automatic edge creation with labeled relationships
- Color-coded nodes (6 preset colors + custom hex)
- Proper spacing algorithms to prevent overlap
- Group nodes for visual organization

**Trigger words:** `Canvas`, `mind map`, `visual diagram`, `思维导图`

## Installation

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- [Obsidian](https://obsidian.md/) with relevant plugins:
  - [Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin) (for Excalidraw skill)

### Install Skills

Copy the skill folders to your Claude Code skills directory:

```bash
# Clone the repository
git clone https://github.com/axtonliu/axton-obsidian-visual-skills.git

# Copy skills to Claude Code directory
cp -r axton-obsidian-visual-skills/excalidraw-diagram ~/.claude/skills/
cp -r axton-obsidian-visual-skills/mermaid-visualizer ~/.claude/skills/
cp -r axton-obsidian-visual-skills/obsidian-canvas-creator ~/.claude/skills/
```

Or copy individual skills as needed.

## Usage

Once installed, Claude Code will automatically use these skills when you ask for visualizations:

```
# Excalidraw
"Create an Excalidraw flowchart showing the CI/CD pipeline"
"Draw a mind map about machine learning concepts"
"用 Excalidraw 画一个商业模式关系图"

# Mermaid
"Visualize this process as a Mermaid diagram"
"Create a sequence diagram for the API authentication flow"
"把这个工作流程转成 Mermaid 图表"

# Canvas
"Turn this article into an Obsidian Canvas"
"Create a mind map canvas for project planning"
"把这篇文章整理成 Canvas 思维导图"
```

## File Structure

```
axton-obsidian-visual-skills/
├── excalidraw-diagram/
│   ├── SKILL.md              # Main skill definition
│   ├── assets/               # Example outputs
│   └── references/           # Excalidraw JSON schema
├── mermaid-visualizer/
│   ├── SKILL.md
│   └── references/           # Syntax rules & error prevention
├── obsidian-canvas-creator/
│   ├── SKILL.md
│   ├── assets/               # Template canvas files
│   └── references/           # Canvas spec & layout algorithms
├── README.md
├── README_CN.md
└── LICENSE
```

## Contributing

Contributions are welcome! Feel free to:

- Report bugs with reproducible cases (input + output + steps)
- Suggest new diagram types or features
- Improve documentation
- Submit pull requests

## Acknowledgments

This project builds upon these excellent open-source tools and specifications:

- [Excalidraw](https://excalidraw.com/) - Hand-drawn style whiteboard
- [Mermaid](https://mermaid.js.org/) - Diagram and chart generation
- [JSON Canvas](https://jsoncanvas.org/) - Open file format for infinite canvas (MIT License)
- [Obsidian](https://obsidian.md/) - Knowledge base application

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Author

**Axton Liu** - AI Educator & Creator

- Website: [axtonliu.ai](https://www.axtonliu.ai)
- YouTube: [@AxtonLiu](https://youtube.com/@AxtonLiu)
- Twitter/X: [@axtonliu](https://twitter.com/axtonliu)

### Learn More

- [AI Elite Weekly Newsletter](https://www.axtonliu.ai/newsletters/ai-2) - Weekly AI insights
- [Free AI Course](https://www.axtonliu.ai/axton-free-course) - Get started with AI

---

© AXTONLIU™ & AI 精英学院™ 版权所有
