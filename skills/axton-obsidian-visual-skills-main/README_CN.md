# Obsidian 可视化 Skills 套装

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)](#状态)

**[English](README.md)**

让 Claude Code 在 Obsidian 里生成 Canvas / Excalidraw / Mermaid 的可视化三件套。

## 状态

> **状态：实验性（Experimental）**
>
> - 这是公开原型，能跑通我的演示，但尚未覆盖所有输入规模与边界情况。
> - 输出质量会受模型版本、输入结构影响，结果可能波动。
> - 我的主要精力在于演示工具与系统的协作关系，而非代码维护本身。
> - 如遇到问题，请提交可复现案例（输入 + 输出文件 + 操作步骤）。

## 什么是 Skills?

Skills 是 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的提示词扩展，赋予 Claude 专业化能力。与需要复杂配置的 MCP 服务器不同，Skills 只是简单的 Markdown 文件，Claude 会按需加载。

## 包含的 Skills

### 1. Excalidraw 图表生成器

使用 Obsidian 的 Excalidraw 插件直接生成手绘风格图表。生成的 `.md` 文件包含内嵌的 Excalidraw JSON，可在 Obsidian 中原生打开。

**支持的图表类型：**

| 类型 | 适用场景 |
|------|---------|
| **流程图** | 步骤说明、工作流程、任务执行顺序 |
| **思维导图** | 概念发散、主题分类、灵感捕捉 |
| **层级图** | 组织结构、内容分级、系统拆解 |
| **关系图** | 要素之间的影响、依赖、互动 |
| **对比图** | 两种以上方案或观点的对照分析 |
| **时间线图** | 事件发展、项目进度、模型演化 |
| **矩阵图** | 双维度分类、任务优先级、定位 |
| **自由布局** | 内容零散、灵感记录、初步信息收集 |

**核心特性：**
- 自动保存为 Obsidian Excalidraw 插件可用的 `.md` 文件
- 手绘美学风格，使用 Excalifont（fontFamily: 5）
- 完美支持中文，正确处理特殊字符
- 统一的配色方案和样式规范

**触发词：** `Excalidraw`、`画图`、`流程图`、`思维导图`、`可视化`、`diagram`

### 2. Mermaid 可视化器

将文本内容转换为专业的 Mermaid 图表，适用于演示和文档。内置语法错误预防机制，避免常见陷阱。

**支持的图表类型：**
- **流程图** (graph TB/LR) - 工作流、决策树、AI Agent 架构
- **循环图** - 迭代过程、反馈循环、持续改进
- **对比图** - 前后对比、A vs B 分析、传统 vs 现代
- **思维导图** - 层级概念、知识组织
- **时序图** - 组件交互、API 调用、消息流
- **状态图** - 系统状态、状态转换、生命周期

**核心特性：**
- 内置语法错误预防（列表冲突、子图命名、特殊字符）
- 可配置布局：垂直/水平、简洁/标准/详细
- 语义化配色方案
- 兼容 Obsidian、GitHub 等 Mermaid 渲染器

**触发词：** `Mermaid`、`可视化`、`流程图`、`时序图`、`visualize`

### 3. Obsidian Canvas 创建器

创建交互式 Obsidian Canvas（`.canvas`）文件，支持思维导图和自由布局。输出有效的 JSON Canvas 格式，可直接在 Obsidian 中打开。

**布局模式：**

| 模式 | 结构 | 适用场景 |
|------|------|---------|
| **思维导图** | 从中心向外的放射状层级 | 头脑风暴、主题探索、层级内容 |
| **自由布局** | 自定义位置、灵活连接 | 复杂网络、非层级内容、自定义排列 |

**核心特性：**
- 根据内容长度智能调整节点大小
- 自动创建带标签的关系连线
- 颜色编码节点（6 种预设颜色 + 自定义 hex）
- 合理的间距算法，防止节点重叠
- 支持节点分组，增强视觉组织

**触发词：** `Canvas`、`思维导图`、`可视化图表`、`mind map`

## 安装

### 前置要求

- 已安装 [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [Obsidian](https://obsidian.md/) 及相关插件：
  - [Excalidraw 插件](https://github.com/zsviczian/obsidian-excalidraw-plugin)（用于 Excalidraw skill）

### 安装 Skills

将 skill 文件夹复制到 Claude Code 的 skills 目录：

```bash
# 克隆仓库
git clone https://github.com/axtonliu/axton-obsidian-visual-skills.git

# 复制 skills 到 Claude Code 目录
cp -r axton-obsidian-visual-skills/excalidraw-diagram ~/.claude/skills/
cp -r axton-obsidian-visual-skills/mermaid-visualizer ~/.claude/skills/
cp -r axton-obsidian-visual-skills/obsidian-canvas-creator ~/.claude/skills/
```

也可以按需只复制单个 skill。

## 使用方法

安装后，当你请求可视化内容时，Claude Code 会自动使用这些 skills：

```
# Excalidraw
"创建一个展示 CI/CD 流程的 Excalidraw 流程图"
"画一个关于机器学习概念的思维导图"
"用 Excalidraw 画一个商业模式关系图"

# Mermaid
"用 Mermaid 图表可视化这个流程"
"为 API 认证流程创建时序图"
"把这个工作流程转成 Mermaid 图表"

# Canvas
"把这篇文章转换成 Obsidian Canvas"
"创建一个项目规划的思维导图 Canvas"
"把这篇文章整理成 Canvas 思维导图"
```

## 文件结构

```
axton-obsidian-visual-skills/
├── excalidraw-diagram/
│   ├── SKILL.md              # 主 skill 定义
│   ├── assets/               # 示例输出
│   └── references/           # Excalidraw JSON schema
├── mermaid-visualizer/
│   ├── SKILL.md
│   └── references/           # 语法规则与错误预防
├── obsidian-canvas-creator/
│   ├── SKILL.md
│   ├── assets/               # 模板 canvas 文件
│   └── references/           # Canvas 规范与布局算法
├── README.md
├── README_CN.md
└── LICENSE
```

## 贡献

欢迎贡献！你可以：

- 报告 Bug，请附上可复现案例（输入 + 输出 + 步骤）
- 建议新的图表类型或功能
- 改进文档
- 提交 Pull Request

## 致谢

本项目基于以下优秀的开源工具和规范构建：

- [Excalidraw](https://excalidraw.com/) - 手绘风格白板
- [Mermaid](https://mermaid.js.org/) - 图表生成工具
- [JSON Canvas](https://jsoncanvas.org/) - 开放的无限画布文件格式（MIT 许可证）
- [Obsidian](https://obsidian.md/) - 知识库应用

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

---

## 作者

**Axton Liu** - AI 教育者与创作者

- 官网：[axtonliu.ai](https://www.axtonliu.ai)
- YouTube：[@AxtonLiu](https://youtube.com/@AxtonLiu)
- Twitter/X：[@axtonliu](https://twitter.com/axtonliu)

### 了解更多

- [AI 精英周刊](https://www.axtonliu.ai/newsletters/ai-2) - 每周 AI 洞察
- [免费 AI 课程](https://www.axtonliu.ai/axton-free-course) - 开启你的 AI 之旅

---

© AXTONLIU™ & AI 精英学院™ 版权所有
