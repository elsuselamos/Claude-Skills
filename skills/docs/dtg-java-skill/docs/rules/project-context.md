# 项目上下文规则

本文档定义 dtg-java-skill 插件中项目上下文的结构和管理规则。

## 项目信息定义

### 基本信息

```yaml
project:
  name: "项目名称"
  description: "项目描述"
  type: "microservice"  # microservice, monolith, library
  version: "1.0.0"
```

### 技术栈

```yaml
techStack:
  java:
    version: "11"
    vendor: "Oracle JDK"

  springBoot:
    version: "2.7.18"
    profile: "stable"

  dubbo:
    version: "3.2.14"
    registry: "zookeeper"

  database:
    primary: "MySQL 8.0.33"
    cache: "Redis"

  buildTool:
    name: "maven"
    version: "3.6+"
```

---

## 架构上下文

### 微服务架构

```yaml
architecture:
  type: "microservices"
  pattern: "DDD"  # DDD, Layered, Hexagonal

  services:
    - name: "xxpay-pay"
      type: "payment-core"
      port: 3020
      dubboPort: 23020

    - name: "xxpay-manage"
      type: "admin-panel"
      port: 8193
      dubboPort: 28193

    - name: "xxpay-service"
      type: "service-provider"
      port: 8190
      dubboPort: 28190
```

### 服务边界

**限界上下文**:
- 支付核心 (Payment Core)
- 运营平台 (Management Platform)
- 商户系统 (Merchant System)
- 代理商系统 (Agent System)

**上下文映射**:
```
[支付核心] ←- [运营平台]
    ↓
[服务提供者]
    ↓
[数据库/缓存/消息队列]
```

---

## 开发上下文

### 团队配置

```yaml
team:
  size: 5
  roles:
    - name: "架构师"
      count: 1
    - name: "后端开发"
      count: 3
    - name: "前端开发"
      count: 1

  workingHours:
    start: "09:00"
    end: "18:00"
    timezone: "Asia/Shanghai"
```

### 开发流程

```yaml
process:
  methodology: "Agile/Scrum"
  sprintDuration: "2 weeks"

  branches:
    main: "main"
    develop: "develop"
    feature: "feature/*"
    release: "release/*"
    hotfix: "hotfix/*"

  codeReview:
    required: true
    approvers: 1

  testing:
    unit: true
    integration: true
    e2e: false
```

---

## 上下文管理

### 上下文加载

插件会自动检测项目上下文：

1. **检测根目录**: 查找 `pom.xml` 或 `CLAUDE.md`
2. **识别模块**: 扫描 `*/pom.xml` 或 `*/CLAUDE.md`
3. **加载配置**: 读取 `.claude/dtg-java-skill.local.md`
4. **初始化上下文**: 构建项目上下文对象

### 上下文更新

以下情况会触发上下文更新：
- 新增/删除模块
- 修改技术栈配置
- 更新服务定义
- 变更团队配置

### 上下文使用

各代理可以通过以下方式访问上下文：

```java
// 获取项目信息
ProjectInfo project = context.getProjectInfo();

// 获取服务定义
List<Service> services = context.getServices();

// 获取技术栈
TechStack techStack = context.getTechStack();
```

---

## 配置文件

### 项目级配置

`.claude/dtg-java-skill.local.md`:

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

### 模块级配置

`xxpay-pay/CLAUDE.md`:

```markdown
---
module: "xxpay-pay"
type: "payment-core"
port: 3020
dubboPort: 23020
---

支付核心模块特定配置
```

---

## 上下文验证

### 验证规则

#### 项目结构验证
- [ ] 根目录包含 `pom.xml`
- [ ] 模块目录包含 `pom.xml` 或 `CLAUDE.md`
- [ ] 配置文件完整

#### 技术栈验证
- [ ] Java 版本兼容
- [ ] Spring Boot 版本兼容
- [ ] Dubbo 版本兼容

#### 配置完整性
- [ ] 必需配置项存在
- [ ] 配置值在有效范围
- [ ] 配置格式正确

### 验证结果

```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "level": "warning",
      "message": "建议配置服务发现"
    }
  ]
}
```

---

## 上下文快照

### 生成快照

```bash
# 生成当前上下文快照
claude context snapshot

# 指定输出路径
claude context snapshot --output context-snapshot.json
```

### 快照内容

```json
{
  "timestamp": "2024-01-01T10:30:00Z",
  "project": {
    "name": "dtg-pay",
    "version": "1.0.0"
  },
  "techStack": {
    "java": "11",
    "springBoot": "2.7.18",
    "dubbo": "3.2.14"
  },
  "services": [
    {
      "name": "xxpay-pay",
      "type": "payment-core",
      "port": 3020
    }
  ]
}
```

---

## 最佳实践

### 1. 保持上下文简洁

只包含必要的信息，避免冗余：

**好的示例**:
```yaml
project:
  name: "dtg-pay"
  type: "microservices"
```

**不好的示例**:
```yaml
project:
  name: "dtg-pay"
  description: "这是一个很长的描述..."
  metadata:
    # 大量不必要的信息
```

### 2. 使用标准命名

遵循插件定义的标准命名：
- 服务名称: `xxpay-pay`, `xxpay-manage`
- 配置键: `springBootVersion`, `javaVersion`
- 模块类型: `payment-core`, `admin-panel`

### 3. 版本控制

将配置文件纳入版本控制：
```bash
git add .claude/dtg-java-skill.local.md
git commit -m "Update project context"
```

### 4. 定期更新

在以下情况下更新上下文：
- 新增/删除服务
- 升级技术栈
- 调整团队配置
- 变更架构模式

---

**相关文档**: [架构原则](architecture-principles.md) | [文档规范](documentation-criteria.md)
