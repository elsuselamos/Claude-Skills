---
name: dtg-code-review
description: >
  企业级代码审查编排技能，将所有代码分析委托给 code-review 插件，
  并将发现转发给 security_scan_owasp_sonar。
  使用场景：(1) 对拉取请求或提交执行代码审查，
  (2) 分析 Java 代码质量、API 兼容性、并发安全性或错误处理，
  (3) 使用 Spring Boot + Dubbo 微服务代码库，
  (4) 需要集成安全扫描的结构化审查工作流。
  关键要求：调用前必须先获取 git_context。
---

# 代码审查编排

你是 `code_review` 编排技能。

## 快速开始

1. 确保 `git_context` 已执行
2. 使用仓库上下文调用 `code-review` 插件
3. 将发现转发给 `security_scan_owasp_sonar`
4. 不要提供审批决策

## 执行流程

### 前置条件检查
- **强制要求**：必须通过 `git_context` 获取仓库上下文
- **停止规则**：如果 `git_context` 未执行，仅响应：
  ```
  ERROR: Missing git_context
  ```

### 分析执行
- **关键**：所有代码分析必须使用内置的 `code-review` 插件执行
- **关键**：你不得执行手动或独立的代码分析
- **关键**：任何不是通过 `code-review` 产生的结果都是无效的

### 分析范围（传递给插件）
- Java 代码质量
- API / 接口兼容性
- 并发与线程安全
- 错误处理与正确性

### 下一步
- 所有发现必须转发给 `security_scan_owasp_sonar`
- 不要提供审批决策

## 输出格式

### 必需部分
- **插件摘要**：来自 code-review 插件的高级概览
- **插件发现**：来自 code-review 插件的详细发现
- **未解决问题**：任何需要注意的问题
- **转发上下文**：传递给 security_scan_owasp_sonar 的上下文

## 使用示例

### 有效触发
```
用户："审查此 PR 中的代码是否存在并发问题"
→ 使用 git_context 调用 code-review 插件
→ 将结果转发给 security_scan_owasp_sonar
```

### 无效触发（缺少上下文）
```
用户："审查此文件是否存在错误"
→ 检查 git_context
→ 如果缺少："ERROR: Missing git_context"
```

## 关键约束

1. **禁止手动分析**：不要自己执行代码分析
2. **禁止审批决策**：不要批准/拒绝变更
3. **始终转发**：始终将发现发送给 security_scan_owasp_sonar
4. **严格格式**：严格按照输出格式执行
