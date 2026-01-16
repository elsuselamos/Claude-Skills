# AI Coding Plugin - Intelligent Spring Boot 2.7 + Dubbo 3

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-purple)](https://claude.ai/code)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot%202.7.18-2.7.18-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Apache Dubbo](https://img.shields.io/badge/Apache%20Dubbo-3.2.14-blue.svg)](https://dubbo.apache.org/)
[![AI Enhanced](https://img.shields.io/badge/AI%20Enhanced-Intelligent-green.svg)](README.md)

[AI-ENHANCED] **智能化** Spring Boot 2.7 + Dubbo 3 企业级 Java 微服务开发插件，集成 **AI 驱动的代码审查、架构分析和问题诊断** 能力，专为企业级分布式系统开发设计，提供最智能的微服务开发体验。

**[FEATURES] 核心特性**:
- [微服务架构] Spring Boot 2.7 + Dubbo 3
- [AI-代码审查] 智能架构建议和问题诊断
- [管理后台] 完整的运营管理平台
- [分布式部署] 分布式部署支持
- [智能质量门] 自动化架构分析和性能预测

## 技术栈

### 后端技术栈
| 技术 | 版本 | 用途 |
|------|------|------|
| Java | JDK 11 | 编程语言 |
| Spring Boot 2.7.18 | 2.7.18 | 应用框架 |
| Apache Dubbo | 3.2.14 | 微服务框架 |
| Lombok | 1.18.30 | 代码简化工具 |
| MySQL | 8.0.33 | 主数据库 |
| MongoDB | - | 文档数据库 |
| Redis | - | 缓存 |
| ActiveMQ | - | 消息队列 |
| MyBatis-Plus | 3.5.7 | ORM框架 |
| HikariCP | - | 连接池 |
| Zookeeper | - | 注册中心 |

### 前端技术栈
| 技术 | 版本 | 说明 |
|------|------|------|
| Layui | v2.3.0 | UI框架 |
| jQuery | 1.11.1 | JavaScript库 |
| ECharts | - | 图表库 |

## 功能特性

### 智能化 AI 代理系统
- **需求分析代理** - 智能评估分布式系统规模和确定微服务边界
- **任务执行代理** - 执行 Spring Boot 2.7 + Dubbo 3 微服务实现任务
- **智能代码审查代理** - **AI 驱动**的代码审查，集成智能架构分析和问题诊断
- **智能问题诊断代理** - **AI 驱动**的深度问题诊断，自动识别代码异味和性能瓶颈
- **智能架构分析代理** - **AI 驱动**的微服务架构评估，基于 DDD 原则和最佳实践
- **架构优化代理** - 提供微服务架构设计建议和分布式系统优化方案

### 智能分析能力
#### 智能问题诊断
  - 代码异味自动识别（长方法、大类、重复代码）
  - 性能瓶颈智能预测（数据库、内存、并发问题）
  - 安全漏洞智能扫描（SQL注入、XSS、认证授权）
  - 并发问题分析（线程安全、死锁风险）

#### 智能架构分析
  - 微服务边界合理性评估（基于 DDD 原则）
  - 架构模式识别（六边形架构、CQRS、事件驱动）
  - 性能架构评估（缓存、数据库、消息队列架构）
  - 容错架构分析（熔断、降级、重试机制）

#### 智能质量门
  - Spring Boot 2.7 + Dubbo 3 版本兼容性检查
  - 项目结构和配置文件完整性验证
  - 测试覆盖率智能评估
  - 安全配置基础检查
  - 分层架构合理性验证

### 文档模板系统
- 微服务产品需求文档模板
- 分布式系统架构决策记录（ADR）模板
- Dubbo 3 服务 API 设计文档模板
- 分布式数据库设计文档模板
- 微服务部署运维文档模板

### 开发工具集成
- Spring Boot 2.7 + Apache Dubbo 3.2.14 框架集成
- Maven 构建工具和依赖管理
- JUnit 5 + Mockito 微服务测试框架
- SonarQube 集成和代码质量监控
- Docker 容器化和 Kubernetes 部署支持
- MyBatis-Plus 数据访问层和多数据源支持
- Zookeeper 服务发现和配置中心
- Redis 缓存和 ActiveMQ 消息队列
- **Lombok 简化开发** - 自动生成样板代码，提升开发效率
- **@SneakyThrows 错误处理** - 简化异常处理代码，避免冗长的 try-catch

## 安装

```bash
# 方式1: 从 Marketplace 安装（推荐）
claude --install ai-coding-java

# 方式2: 本地安装
claude --plugin-dir /path/to/ai-coding-java
```

## 快速开发

### 环境要求
- **JDK**: 11+
- **Maven**: 3.6+
- **MySQL**: 8.0+
- **Redis**: 5.0+
- **Zookeeper**: 3.6+

## 快速开始

### 1. Spring Boot 2.7 + Dubbo 3 微服务项目初始化
```bash
# 启动 Claude Code
claude

# 使用 ai-coding-java 技能开始开发分布式微服务功能
# 通过技能内置的代理系统自动处理需求分析、代码生成和审查
```

### 2. 智能化分布式微服务开发工作流
插件提供以下智能化能力：

**[AI-AGENTS] AI 代理系统**：
- **需求分析代理** - 智能评估分布式系统规模和确定微服务边界
- **任务执行代理** - 执行 Spring Boot 2.7 + Dubbo 3 微服务实现任务
- **智能代码审查代理** - AI 驱动的代码审查，集成智能架构分析和问题诊断
- **智能问题诊断代理** - AI 驱动的深度问题诊断，自动识别代码异味和性能瓶颈
- **智能架构分析代理** - AI 驱动的微服务架构评估，基于 DDD 原则和最佳实践

### 3. 智能开发工作流示例
```bash
# 步骤1: 启动 Claude Code 并加载插件
claude

# 步骤2: 使用技能进行智能化微服务开发
# 通过对话方式描述需求，AI 代理会自动：
# - 分析需求并设计微服务架构
# - 生成符合最佳实践的代码
# - 执行智能代码审查
# - 提供优化建议

# 步骤3: 持续智能监控
# AI 代理会自动执行增强的质量门检查
```

## 详细文档

### 使用指南
- [快速开始指南](docs/guides/quickstart.md)
- [智能功能指南](docs/guides/intelligent-features.md) - **新增**
- [代理系统说明](docs/guides/agents.md)
- [最佳实践](docs/guides/best-practices.md)
- [智能架构分析](docs/guides/architecture-analysis.md) - **新增**
- [智能问题诊断](docs/guides/problem-diagnosis.md) - **新增**

### 模板参考
- [PRD 模板](docs/templates/prd.md)
- [ADR 模板](docs/templates/adr.md)
- [设计文档模板](docs/templates/design.md)
- [智能审查报告模板](docs/templates/intelligent-review.md) - **新增**

### 开发规则
- [项目上下文](docs/rules/project-context.md)
- [编码标准](docs/rules/coding-standards.md)
- [文档规范](docs/rules/documentation-criteria.md)

## 配置

插件支持个性化配置，创建 `.claude/ai-coding-java.local.md` 文件：

```markdown
---
projectName: "企业级微服务项目"
projectType: "enterprise-microservice"
springBootVersion: "2.7.x"
javaVersion: "11"
techStack: ["Spring Boot 2.7", "Apache Dubbo", "MyBatis-Plus", "MySQL", "Redis", "MongoDB", "ActiveMQ"]
buildTool: "maven"
teamSize: 5
architecture: "microservices"
database: "mysql"
cache: "redis"
messageQueue: "activemq"
containerPlatform: "docker"
---

企业级 Java 微服务项目特定配置信息
```

## 语言支持

- [中文] 简体中文
- [English] English

## 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 智能功能亮点

### AI 驱动的代码审查
- **智能架构建议**: 基于项目上下文提供微服务架构优化建议
- **自动问题诊断**: 智能识别代码异味和潜在性能问题
- **上下文感知分析**: 结合 Spring Boot 2.7 + Dubbo 3 专业知识进行深度分析
- **优先级智能排序**: 基于影响度和紧急程度对建议进行智能排序

### 智能质量保证
- **增强质量门**: 集成智能分析的前置检查，包括架构合理性验证
- **实时反馈**: 即时的智能建议和改进方案
- **持续学习**: 基于项目特点的个性化建议生成
- **企业级标准**: 符合大型企业代码质量和架构标准

### 智能化集成
- **代理协作**: 多个智能代理协同工作，提供全面分析
- **无缝集成**: 与现有工作流程完美融合
- **配置灵活**: 支持个性化的智能分析配置
- **扩展性强**: 可根据需要添加新的智能分析能力

## 使用场景

### 企业级微服务开发
- **AI 驱动开发**: 通过对话方式实现微服务需求，AI 代理自动完成架构设计、代码生成和审查
- **智能代码审查**: 自动执行包含AI驱动分析、架构评估和问题诊断的完整代码审查

### 持续集成/持续部署
- **质量门**: 增强的质量检查脚本，包含智能预分析
- **自动化检查**: Spring Boot 2.7 + Dubbo 3 版本兼容性和最佳实践验证
- **智能报告**: 详细的质量报告和改进建议

### 团队协作
- **知识共享**: 智能生成的最佳实践建议和解决方案
- **标准化**: 统一的代码质量标准和架构评估
- **技能提升**: 个性化的学习资源和改进建议

---

[AI-ENHANCED] **让 AI 成为您的微服务开发伙伴，构建更智能、更可靠的企业级应用！**

基于原始 [AI Coding Project Boilerplate](https://github.com/shinpr/ai-coding-project-boilerplate) 项目开发，现已全面智能化升级。