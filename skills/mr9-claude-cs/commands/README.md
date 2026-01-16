# dtg-pay 项目命令说明文档

本文档介绍 dtg-pay 项目中可用的 Claude Code 自定义命令。

## 可用命令

### `/hi` - 打招呼

**功能**: 与 Claude 打个招呼，快速开始对话。

**使用方法**:
```
/hi
```

**示例**:
```
用户: /hi
Claude: 你好！我是 dtg-pay 项目的代码助手，可以帮你处理支付网关系统的开发任务。
```

---

## 命令开发规范

### 命令文件结构

每个命令都是一个独立的 Markdown 文件，位于 `.claude/commands/` 目录下：

```markdown
---
description: 命令的简短描述
tags: [可选标签]
---

命令的具体内容和提示词
```

### 添加新命令

1. 在 `.claude/commands/` 目录下创建新的 `.md` 文件
2. 文件名即为命令名（如 `review.md` 对应 `/review` 命令）
3. 添加 YAML frontmatter（至少包含 `description`）
4. 在下方编写命令的具体内容

### 命令示例

```markdown
---
description: 代码审查
tags: [review, code-quality]
---

请审查以下代码，关注：
1. 代码规范
2. 潜在 bug
3. 性能问题
4. 安全漏洞
```

## 注意事项

- 命令文件名建议使用小写字母和连字符
- description 应简洁明了，说明命令的用途
- 命令内容可以包含复杂的提示词模板
- 同一命令可以被多次调用，每次都会展开完整内容
