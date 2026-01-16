# 快速开始指南

欢迎使用 dtg-java-skill 插件！本指南将帮助您快速上手 Spring Boot 2.7 + Dubbo 3 微服务开发。

## 前置要求

在开始之前，请确保您的开发环境满足以下要求：

### 必需环境
- **JDK**: 11 或更高版本
- **Maven**: 3.6 或更高版本
- **MySQL**: 8.0 或更高版本
- **Redis**: 5.0 或更高版本
- **Zookeeper**: 3.6 或更高版本

### 可选环境
- **MongoDB**: 用于文档存储
- **ActiveMQ**: 用于消息队列
- **Docker**: 用于容器化部署

## 5 分钟快速启动

### 步骤 1: 安装插件

```bash
# 从 Marketplace 安装（推荐）
claude --install dtg-java-skill

# 或使用本地安装
claude --plugin-dir /path/to/dtg-java-skill
```

### 步骤 2: 创建新项目

```bash
# 启动 Claude Code
claude

# 通过对话创建项目
"帮我创建一个新的 Spring Boot 2.7 + Dubbo 3 微服务项目"
```

### 步骤 3: 使用智能功能

```bash
# 代码审查
"请审查我的代码"

# 架构分析
"分析我的微服务架构"

# 问题诊断
"诊断我的代码问题"
```

## 主要功能介绍

### 1. 智能代码审查

自动执行全面的代码审查，包括：
- Spring Boot 2.7 最佳实践检查
- Dubbo 3 微服务架构评估
- 安全漏洞扫描
- 性能问题识别

### 2. 智能架构分析

基于 DDD 原则评估微服务架构：
- 服务边界合理性分析
- 架构模式识别
- 性能架构评估
- 容错能力分析

### 3. 智能问题诊断

自动识别代码问题：
- 代码异味检测
- 性能瓶颈分析
- 并发问题识别
- 配置问题诊断

## 快速参考

### 常用命令

| 任务 | 命令 |
|------|------|
| 代码审查 | "code review" 或 "审查代码" |
| 架构分析 | "analyze architecture" 或 "分析架构" |
| 问题诊断 | "diagnose" 或 "诊断问题" |
| 创建服务 | "create service" 或 "创建服务" |
| 生成代码 | "generate code" 或 "生成代码" |

### 技能触发

插件包含以下智能技能：

| 技能 | 触发词 |
|------|--------|
| dtg-code-review | "code review", "审查代码" |
| dtg-intelligent-architecture-analysis | "analyze architecture", "分析架构" |
| dtg-springboot-project-setup | "setup Spring Boot", "配置 Spring Boot" |
| dtg-payment-core-development | "develop payment", "开发支付模块" |
| dtg-admin-panel-development | "develop admin panel", "开发管理后台" |
| dtg-common-module-development | "develop common module", "开发公共模块" |
| dtg-multi-module-management | "manage modules", "管理模块" |

## 常见问题

### Q: 插件支持哪些 Spring Boot 版本？

A: 当前支持 Spring Boot 2.7.18。

### Q: 支持哪些数据库？

A: 主要支持 MySQL 8.0+，也支持 MongoDB 作为文档数据库。

### Q: 如何配置 Dubbo 注册中心？

A: 插件会自动配置 Zookeeper 作为注册中心。您可以在 application.yml 中自定义配置。

### Q: 生成的代码可以直接使用吗？

A: 是的，生成的代码符合企业级标准，可以直接用于生产环境。

### Q: 如何获取更多帮助？

A: 请查阅详细的 [使用指南](../guides/) 或参考 [最佳实践](best-practices.md)。

## 下一步

- 阅读 [智能功能指南](intelligent-features.md) 了解 AI 代理系统
- 查看 [代理系统说明](agents.md) 了解代理协作流程
- 学习 [最佳实践](best-practices.md) 提升代码质量
- 探索 [架构分析](architecture-analysis.md) 深入理解微服务架构

---

**需要更多帮助？** 请访问 [GitHub Issues](https://github.com/shinpr/dtg-java-skill/issues) 提问。
