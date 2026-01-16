# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

dtg-pay 是一个基于 **Spring Boot 2.7.18 + Dubbo 3.2.14** 的分布式支付网关系统，支持多币种支付、代付、分账等业务。系统采用微服务架构，各模块通过 Dubbo RPC 进行通信。

### 技术栈
- **Java**: 11
- **Spring Boot**: 2.7.18
- **Dubbo**: 3.2.14
- **数据库**: MySQL + MongoDB
- **缓存**: Redis
- **消息队列**: ActiveMQ
- **ORM**: MyBatis-Plus
- **注册中心**: Zookeeper

## 模块架构

项目采用多模块 Maven 结构，核心模块说明：

| 模块 | 端口 | 职责 |
|------|------|------|
| `xxpay-core` | - | 公共模块：实体类、DTO、Dubbo 服务接口定义、通用工具类 |
| `xxpay-service` | 8190 (Dubbo: 28190) | Dubbo 服务提供者：所有业务逻辑实现、数据库操作 |
| `xxpay-manage` | 8193 | 运营管理平台 Web 接口 |
| `xxpay-merchant` | 8191 | 商户系统 Web 接口 |
| `xxpay-agent` | 8192 | 代理商系统 Web 接口 |
| `xxpay-pay` | 3020 | 支付核心：对接三方/四方支付渠道 |
| `xxpay-task` | 8194 | 定时任务：对账、结算服务（需单节点部署） |
| `xxpay-flyway` | - | 数据库版本管理 |
| `xxpay-generator` | - | MyBatis 代码生成器 |
| `xxpay-consumer` | - | 消息消费者 |
| `rbgi` | 8195 | RBGI 相关服务 |

**依赖关系**: Web 模块 (manage/merchant/agent/pay) → 依赖 `xxpay-core` → 调用 `xxpay-service` 的 Dubbo 服务

## 编译与运行

### 编译顺序（重要）

```bash
# 1. 核心模块（必须先编译）
./mvnw -f xxpay-core clean install -Dmaven.test.skip=true

# 2. 服务层（Dubbo 提供者）
./mvnw -f xxpay-service clean package -Dmaven.test.skip=true

# 3. 各个 Web 模块
./mvnw -f xxpay-pay clean package -Dmaven.test.skip=true
./mvnw -f xxpay-task clean package -Dmaven.test.skip=true
./mvnw -f xxpay-agent clean compile -Dmaven.test.skip=true
./mvnw -f xxpay-manage clean package -Dmaven.test.skip=true
./mvnw -f xxpay-merchant clean package -Dmaven.test.skip=true
```

### 本地运行

使用 IDEA 的 `.run/` 目录下的配置：
- `8190-XxPayServiceApplication.run.xml` - xxpay-service
- `8191-XxPayMerchantApplication.run.xml` - 商户系统
- `8192-XxPayAgentApplication.run.xml` - 代理商系统
- `8193-XxPayManageApplication.run.xml` - 运营管理平台
- `8194-XxPayTaskApplication.run.xml` - 定时任务
- `3020-XxPayPayApplication.run.xml` - 支付核心

### 运行测试

```bash
# 运行单个测试类
./mvnw -f xxpay-service test -Dtest=MapperTest

# 运行指定包下的所有测试
./mvnw -f xxpay-service test -Dtest=org.xxpay.service.dao.mapper.*
```

测试基类：`xxpay-service/src/test/java/org/xxpay/service/dao/mapper/MapperTest.java`

### 环境变量

各模块通过环境变量配置不同环境：
- `spring.profiles.active`: `local` / `dtg-stg` / `dtg-prod`
- `ZOOKEEPER`: Zookeeper 地址
- `DATASOURCE_URL`, `DATASOURCE_USERNAME`, `DATASOURCE_PASSWORD`: 数据库配置
- `REDIS_HOST`, `REDIS_PASSWORD`: Redis 配置
- `MONGODB_URI`, `MONGODB_AUTHENTICATION_DATABASE`: MongoDB 配置
- `ACTIVEMQ_BROKER`, `ACTIVEMQ_USER`, `ACTIVEMQ_PASSWORD`: ActiveMQ 配置

### 时区设置

项目统一使用 `Asia/Shanghai` 时区：
- JVM: 在 `@PostConstruct` 中设置 `TimeZone.setDefault(TimeZone.getTimeZone("Asia/Shanghai"))`
- Jackson: `spring.jackson.time-zone: Asia/Shanghai`
- MySQL: `serverTimezone=GMT%2B0`（数据库存储 UTC，应用层转换）

## 核心业务架构

### Dubbo 服务调用模式

1. **服务定义**: 在 `xxpay-core/src/main/java/org/xxpay/core/service/` 中定义接口，使用 `@DubboService` 注解
2. **服务实现**: 在 `xxpay-service/src/main/java/org/xxpay/service/impl/` 中实现接口，使用 `@DubboService` 注解发布服务
3. **服务调用**: Web 模块通过 `@DubboReference` 注入服务接口进行调用

### 分润计算核心

项目包含一套完整的分润计算机制，核心组件：
- **计算器**: `ProfitSharingCalculator` - 纯内存无状态计算组件
- **上下文**: `ProfitSharingContext` - 封装订单金额、费率配置
- **层级模型**: `FeeLayer` - 抽象平台/代理/商户层级
- **结果**: `ProfitSharingResult` - 包含各方分润金额

相关设计文档：`plan.md`

### 支付渠道对接

支付渠道实现位于 `xxpay-pay/src/main/java/org/xxpay/pay/channel/`，每个渠道一个目录：
- **核心接口**:
  - `PaymentInterface`: 支付接口
  - `TransInterface`: 代付接口
  - `PayNotifyInterface`: 支付回调
  - `TransNotifyInterface`: 代付回调
- **配置类**: `*Config.java` - 渠道配置参数
- **服务实现**: `*PaymentService.java`, `*TransService.java` 等

## 开发规范

### MyBatis 代码生成

1. 修改 `xxpay-generator/resource/generatorConfig.xml`
2. 运行生成命令：`cd xxpay-generator && mvn clean install mybatis-generator:generate`
3. **重要**: 将生成的 Model 拷贝到 `xxpay-core` 项目，Mapper 拷贝到 `xxpay-service` 项目（拷贝时需比对是否有修改）

### 代码结构约定

- **Controller**: Web 接口层，各 Web 模块的 `ctrl/` 目录
- **Service**: 业务逻辑层，`xxpay-service` 的 `service/` 和 `impl/` 目录
- **DAO**: 数据访问层，`xxpay-service` 的 `dao/mapper/` 目录
- **Entity**: 实体类，`xxpay-core` 的 `entity/` 目录
- **DTO**: 数据传输对象，`xxpay-core` 的 `dto/` 目录

### Dubbo 配置要点

- **超时时间**: 统一设置为 60 秒（`timeout: 60000`）
- **重试次数**: 设置为 0（`retries: 0`），避免重复处理
- **线程池配置**:
  - Provider: `threads: 200`
  - Consumer: `threads: 100`
  - Protocol: `threads: 300`, `iothreads: 100`

### 数据库连接池配置

HikariCP 配置（基于 m7i.xlarge 实例优化）：
- `maximum-pool-size`: 150（考虑 Dubbo 200 线程）
- `minimum-idle`: 50
- `connection-timeout`: 30 秒
- `max-lifetime`: 30 分钟
- `leak-detection-threshold`: 120 秒

## 上版顺序

生产环境部署时需按以下顺序升级：
1. `xxpay-flyway` - 数据库迁移
2. `xxpay-service` - 服务层
3. `xxpay-pay` - 支付核心
4. `xxpay-task` - 定时任务
5. `xxpay-manage` - 运营平台
6. `xxpay-agent` - 代理商系统
7. `xxpay-merchant` - 商户系统

## 常见问题

### Dubbo Shutdown 错误

已知 Dubbo shutdown 时会报错（Curator NodeCache），这是 Dubbo 的已知 bug：https://github.com/apache/dubbo/issues/10150

可通过日志级别忽略：
```yaml
logging:
  level:
    org.springframework.jms.listener.DefaultMessageListenerContainer: OFF
    org.apache.curator.framework.recipes.cache.NodeCache: OFF
```

### MyBatis 一级缓存

微服务架构中已关闭一级缓存：
```yaml
mybatis-plus:
  configuration:
    localCacheScope: STATEMENT
```

### 优雅下线

配置了 15 秒的优雅下线超时：
```yaml
spring:
  lifecycle:
    timeout-per-shutdown-phase: 15s
```
