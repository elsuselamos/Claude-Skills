---
name: dtg-springboot-project-setup
description: This skill should be used when the user asks to "setup Spring Boot project", "configure Spring Boot", "Spring Boot configuration", "application.yml", "environment setup", or mentions Spring Boot 2.7 setup, project configuration, or environment management. Provides Spring Boot 2.7 + Dubbo 3 enterprise-level microservice project configuration guidance.
version: 3.0.0
tags: ["spring-boot", "dubbo", "microservice", "enterprise", "java"]
---

# Spring Boot 2.7 + Dubbo 项目配置

## 配置文件

| 文件 | 路径 |
|------|------|
| Maven | `references/pom.xml` |
| 应用配置 | `references/application.yml` |
| 开发环境 | `references/application-dev.yml` |
| Lombok | `references/lombok.config` |
| 项目结构 | `references/project-structure.md` |

## 代码示例

| 类型 | 路径 |
|------|------|
| 实体/DTO | `references/code-examples.md` |
| Dubbo 服务 | `references/code-examples.md` |
| 测试 | `references/test-examples.md` |

## 技术栈

| 技术 | 版本 |
|------|------|
| Java | 11 |
| Spring Boot | 2.7.18 |
| Apache Dubbo | 3.2.14 |
| MyBatis-Plus | 3.5.7 |
| MySQL | 8.0.33 |
| Redis | 最新 |

## 快速开始

```bash
# 1. 使用 Spring Initializr 创建 Spring Boot 2.7.18 项目
#    添加依赖: Web, Security, Validation, Redis, MongoDB, ActiveMQ

# 2. 添加 Dubbo 依赖
参考 references/pom.xml

# 3. 配置应用
复制 references/application.yml 到项目

# 4. 配置 Lombok
复制 references/lombok.config 到项目根目录

# 5. 创建实体和服务
参考 references/code-examples.md
```

## 核心概念

### Dubbo 微服务
- `@DubboService` - 服务接口注解
- 注册中心: Zookeeper/Nacos
- 协议: dubbo

### 分层架构
- **Controller**: HTTP 请求处理
- **Service**: 业务逻辑
- **Repository**: 数据访问
- **DTO**: 数据传输对象
