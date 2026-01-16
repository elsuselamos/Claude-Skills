# 快速开始指南

## [ROCKET] ai-coding-java 快速入门

欢迎使用 ai-coding-java 插件！这是一个专为 Spring Boot 2.7 + Dubbo 3 企业级微服务开发设计的智能化插件，集成 AI 驱动的代码审查、智能架构分析和问题诊断功能。

### [TARGET] 适用场景

- **企业级微服务开发** - 快速搭建生产就绪的微服务架构
- **Spring Boot + Dubbo 项目** - 零配置集成主流微服务框架
- **代码质量提升** - AI 驱动的智能代码审查和优化建议
- **架构规范化** - 自动化架构分析和最佳实践指导

## 📋 前置要求

### 环境要求
- **Java 11+** - 推荐使用 OpenJDK 11 或更高版本
- **Maven 3.6+** - 项目构建工具
- **IDE** - IntelliJ IDEA 或 Eclipse（推荐 IntelliJ IDEA）

### 系统要求
- **内存**: 最少 4GB RAM（推荐 8GB+）
- **磁盘**: 最少 2GB 可用空间
- **网络**: 稳定的互联网连接（用于依赖下载）

## [FAST] 5分钟快速体验

### 1. 启动项目上下文注入

```bash
/ai-coding-java:project-inject
```

此命令会自动：
- [OK] 检测当前项目结构
- [OK] 注入 Spring Boot 2.7 + Dubbo 3 配置模板
- [OK] 设置企业级开发环境标准
- [OK] 激活 AI 驱动的质量门检查

### 2. 创建第一个微服务

```bash
/ai-coding-java:implement --type=new-microservice --name=user-service
```

此命令会自动：
- [ARCHITECTURE] 创建完整的微服务项目结构
- ⚙️ 配置 Spring Boot + Dubbo 集成
- 🗄️ 设置数据库连接和实体类
- 🧪 生成单元测试和集成测试
- [LIBRARY] 创建相关文档

### 3. 运行智能代码审查

```bash
/ai-coding-java:review --file=src/main/java/com/example/user/UserService.java
```

此功能会：
- [SEARCH] AI 驱动的代码质量分析
- [ARCHITECTURE] 架构合理性评估
- 🔒 安全漏洞检测
- [FAST] 性能优化建议
- [EDIT] 企业级代码规范检查

## [TOOLS] 核心功能快速指南

### 智能实现命令 `/implement`

最强大的功能，支持多种开发场景：

#### 新微服务开发
```bash
/ai-coding-java:implement 我需要创建一个订单服务，包含订单管理、支付集成和库存管理功能
```

#### 继续现有开发
```bash
/ai-coding-java:implement 继续完善用户服务的认证和权限功能
```

#### 代码质量修复
```bash
/ai-coding-java:implement 修复当前的代码质量问题，特别是性能和安全方面的
```

### 专业代理协作

插件包含 5 个专业 AI 代理：

#### [CHART] 需求分析代理 (requirement-analyzer)
```bash
/ai-coding-java:task --analyzer=requirement-analyzer 分析用户管理模块的技术需求
```

#### [ARCHITECTURE] 架构分析代理 (architecture-analyzer)
```bash
/ai-coding-java:task --analyzer=architecture-analyzer 评估当前微服务架构的合理性
```

#### [SEARCH] 智能诊断代理 (intelligent-diagnoser)
```bash
/ai-coding-java:task --analyzer=intelligent-diagnoser 诊断应用的性能瓶颈
```

#### [OK] 代码审查代理 (code-reviewer)
```bash
/ai-coding-java:task --analyzer=code-reviewer 对支付模块进行深度代码审查
```

#### [ROCKET] 任务执行代理 (task-executor)
```bash
/ai-coding-java:task --analyzer=task-executor 实现用户注册功能
```

### 质量保证系统

#### 智能质量门
```bash
/ai-coding-java:code-quality
```

自动检查：
- [OK] 编译错误和语法问题
- [OK] Spring Boot 启动测试
- [OK] Dubbo 服务注册验证
- [OK] 数据库连接测试
- [OK] 单元测试覆盖率

#### 文档质量验证
```bash
# 自动验证项目文档完整性
./hooks/scripts/documentation-validator.sh
```

## 🎨 常用开发模式

### 模式 1: 全新微服务项目
```bash
# 1. 项目初始化
/ai-coding-java:project-inject

# 2. 创建核心服务
/ai-coding-java:implement 创建用户服务，包含注册、登录和用户管理功能

# 3. 架构分析和优化
/ai-coding-java:design --microservice=user-service --analyze=architecture

# 4. 代码质量审查
/ai-coding-java:review --scope=all --depth=comprehensive
```

### 模式 2: 现有项目增强
```bash
# 1. 智能诊断现有问题
/ai-coding-java:task --analyzer=intelligent-diagnoser 分析当前项目的架构和性能问题

# 2. 基于诊断结果进行优化
/ai-coding-java:implement 根据诊断结果优化微服务间的通信和缓存策略

# 3. 全面代码审查
/ai-coding-java:review --focus=security,performance --format=detailed
```

### 模式 3: 特定功能开发
```bash
# 1. 需求分析
/ai-coding-java:task --analyzer=requirement-analyzer 设计支付集成方案

# 2. 功能实现
/ai-coding-java:implement 实现支付模块，支持多种支付方式

# 3. 质量验证
/ai-coding-java:code-quality --module=payment
```

## [TOOL] 配置快速设置

### 1. 基础配置
插件会自动创建以下配置文件：
- `application.yml` - Spring Boot 主配置
- `dubbo-consumer.yml` - Dubbo 消费者配置
- `dubbo-provider.yml` - Dubbo 提供者配置
- `logback-spring.xml` - 日志配置

### 2. 数据库配置
自动支持：
- **MySQL 8.0+** - 主要业务数据库
- **Redis** - 缓存和会话存储
- **MongoDB** - 文档存储（可选）

### 3. 消息队列配置
开箱即用：
- **ActiveMQ** - 企业级消息中间件
- **RabbitMQ** - 高性能消息队列（可选）

## 🧪 测试快速验证

### 运行所有测试
```bash
# 单元测试
mvn test

# 集成测试
mvn integration-test

# 端到端测试
mvn verify
```

### API 测试
```bash
# 健康检查
curl http://localhost:8080/actuator/health

# 应用信息
curl http://localhost:8080/actuator/info

# 服务注册状态
curl http://localhost:8080/dubbo/registry
```

## [SEARCH] 常见问题排查

### 启动失败
1. 检查 Java 版本：`java -version`
2. 检查 Maven 版本：`mvn -version`
3. 验证端口占用：`lsof -i :8080`
4. 查看详细日志：`tail -f logs/application.log`

### Dubbo 连接问题
1. 验证 Zookeeper 连接：`telnet localhost 2181`
2. 检查服务注册：`ls /dubbo/`
3. 验证服务提供者状态

### 数据库连接问题
1. 测试数据库连接：`mysql -h localhost -u root -p`
2. 检查数据库权限
3. 验证连接池配置

## [LIBRARY] 进一步学习

### 高级功能
- [微服务架构设计指南](./microservice-development.md)
- [Dubbo 高级配置](./dubbo-configuration.md)
- [数据库集成最佳实践](./database-integration.md)
- [测试策略指南](./testing-strategies.md)

### 企业级特性
- [编码规范](../rules/coding-standards.md)
- [架构原则](../rules/architecture-principles.md)
- [安全指南](../rules/security-guidelines.md)
- [性能最佳实践](../rules/performance-best-practices.md)

## 🆘 获取帮助

### 在线帮助
```bash
# 查看所有可用命令
/ai-coding-java:help

# 查看特定功能帮助
/ai-coding-java:implement --help
/ai-coding-java:review --help
```

### 社区支持
- **GitHub Issues**: 报告 bug 和功能请求
- **文档反馈**: 帮助改进文档质量
- **最佳实践分享**: 贡献开发经验和技巧

### 联系方式
- **技术支持**: dubbo-microservice-support@example.com
- **项目主页**: https://github.com/shinpr/ai-coding-java

---

## 🎉 开始您的智能微服务开发之旅！

现在您已经掌握了 ai-coding-java 插件的核心使用方法。立即开始体验智能化微服务开发的强大功能吧！

**记住**：ai-coding-java 不仅仅是一个代码生成器，更是您的智能开发伙伴，它会持续学习您的项目特点，提供越来越精准的建议和优化方案。