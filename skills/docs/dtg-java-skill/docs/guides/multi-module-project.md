# dtg-pay 多模块项目开发指南

本指南为 dtg-pay 多模块 Maven 项目提供完整的开发指导。

## 项目概述

dtg-pay 是一个基于 Spring Boot + Dubbo 分布式架构的支付系统，支持多币种、多支付渠道、多商户、多代理的商业级支付平台。系统采用微服务架构，支持分布式部署。

## 项目结构

```
dtg-pay (父项目: org.dtg:dtg-pay:1.0.0)
├── rbgi              # RBGI 银行支付网关 (8195)
├── xxpay-agent       # 代理商系统接口 (8192)
├── xxpay-consumer    # 商户通知消费者 (3120)
├── xxpay-core        # 公共方法、实体 Bean、API 接口定义
├── xxpay-flyway      # 数据库迁移
├── xxpay-manage      # 运营管理平台接口 (8193)
├── xxpay-merchant    # 商户系统接口 (8191)
├── xxpay-task        # 定时任务 (8194)
├── xxpay-pay         # 支付核心 (3020)
└── xxpay-service     # Dubbo 服务生产者 (8190)
```

## 快速开始

### 1. 环境准备

```bash
# 确保 JDK 11 已安装
java -version

# 确保 Maven 3.x 已安装
mvn -version

# 确保 MySQL 8.0+ 可用
mysql --version
```

### 2. 编译项目

```bash
# 1. 首先编译核心模块（必须先编译）
./mvnw -f xxpay-core clean install -Dmaven.test.skip=true

# 2. 编译服务层
./mvnw -f xxpay-service clean package -Dmaven.test.skip=true

# 3. 编译其他模块
./mvnw -f xxpay-pay clean package -Dmaven.test.skip=true
./mvnw -f xxpay-task clean package -Dmaven.test.skip=true
./mvnw -f xxpay-manage clean package -Dmaven.test.skip=true
./mvnw -f xxpay-agent clean package -Dmaven.test.skip=true
./mvnw -f xxpay-merchant clean package -Dmaven.test.skip=true
./mvnw -f xxpay-consumer clean package -Dmaven.test.skip=true
./mvnw -f rbgi clean package -Dmaven.test.skip=true
```

### 3. 运行单个模块

```bash
# 开发环境运行（使用 application.properties 配置）
./mvnw -f xxpay-service spring-boot:run
./mvnw -f xxpay-pay spring-boot:run
./mvnw -f xxpay-manage spring-boot:run

# 或直接运行打包后的 jar
java -jar xxpay-service/target/xxpay-service-1.0.0.jar
```

## 模块开发指南

### 根据工作目录自动切换模块

插件会根据当前工作目录自动检测并切换模块上下文：

```
工作目录: /dtg-pay/xxpay-manage
自动载入: dtg-admin-panel-development 技能
自动载入: /dtg-pay/xxpay-manage/CLAUDE.md
```

### 模块特定开发技能

| 工作目录 | 自动应用技能 | 说明 |
|---------|-------------|------|
| xxpay-service | dubbo-provider-development | Dubbo 服务提供者开发 |
| xxpay-pay | dtg-payment-core-development | 支付核心和通道开发 |
| xxpay-manage | dtg-admin-panel-development | 运营管理后台开发 |
| xxpay-agent | dtg-admin-panel-development | 代理商管理后台开发 |
| xxpay-merchant | dtg-admin-panel-development | 商户管理后台开发 |
| xxpay-task | scheduled-task-development | 定时任务开发 |
| xxpay-consumer | message-consumer-development | 消息消费者开发 |
| rbgi | bank-gateway-development | 银行网关开发 |
| xxpay-core | dtg-common-module-development | 公共模块开发 |

### 查看其他模块

使用命令查看其他模块的文档：

```
/view-module xxpay-service    # 查看 xxpay-service 模块文档
/view-module xxpay-core       # 查看 xxpay-core 公共模块文档
```

## 模块依赖关系

```
┌─────────────────────────────────────────────────────────────────┐
│                    xxpay-pay (支付核心)                          │
│                  xxpay-manage (运营平台)                         │
│                  xxpay-merchant (商户系统)                       │
│                   xxpay-agent (代理商系统)                       │
│                    xxpay-task (定时任务)                         │
│                  xxpay-consumer (通知消费)                       │
│                      rbgi (银行网关)                             │
└────────────────────────┬────────────────────────────────────────┘
                         │ 依赖
                         ↓
                  ┌──────────────┐
                  │  xxpay-core  │  (公共API、实体、常量)
                  └──────────────┘
                         │ Dubbo RPC 调用
                         ↓
                  ┌──────────────┐
                  │ xxpay-service │  (Dubbo 服务提供者)
                  └──────────────┘
                         │
                         ↓
                  MySQL + MongoDB + Redis + ActiveMQ
```

## 部署顺序

上版时必须按以下顺序发布：

1. **xxpay-flyway** - 数据库迁移
2. **xxpay-service** - 业务服务（Dubbo Provider）
3. **xxpay-pay** - 支付核心
4. **xxpay-task** - 定时任务（单节点部署）
5. **xxpay-manage** - 运营平台
6. **xxpay-agent** - 代理商系统
7. **xxpay-merchant** - 商户系统

## 服务端口

| 模块 | HTTP 端口 | Dubbo 端口 |
|------|----------|-----------|
| xxpay-service | 8190 | 28190 |
| xxpay-pay | 3020 | 23020 |
| xxpay-manage | 8193 | 28193 |
| xxpay-merchant | 8191 | 28191 |
| xxpay-agent | 8192 | 28192 |
| xxpay-task | 8194 | 28194 |
| xxpay-consumer | 3120 | 23120 |
| rbgi | 8195 | - |

## 环境配置

所有模块支持三种环境，通过环境变量 `spring.profiles.active` 切换：

- `local` - 本地开发环境
- `dtg-stg` - 测试环境
- `dtg-prod` - 生产环境

### 关键环境变量

| 变量 | 说明 |
|------|------|
| `ZOOKEEPER` | Zookeeper 注册中心地址 |
| `DATASOURCE_URL` | MySQL 数据库地址 |
| `DATASOURCE_USERNAME` | 数据库用户名 |
| `DATASOURCE_PASSWORD` | 数据库密码 |
| `REDIS_HOST` | Redis 主机地址 |
| `REDIS_PASSWORD` | Redis 密码 |
| `ACTIVEMQ_BROKER` | ActiveMQ 消息代理地址 |
| `ACTIVEMQ_USER` | ActiveMQ 用户名 |
| `ACTIVEMQ_PASSWORD` | ActiveMQ 密码 |
| `MONGODB_URI` | MongoDB 连接 URI |
| `MONGODB_AUTHENTICATION_DATABASE` | MongoDB 认证数据库 |
| `NODE` | 服务节点标识（分布式环境下需唯一）|

## 核心架构概念

### 1. Dubbo RPC 通信模型

所有服务间调用基于 `RpcBaseParam` / `RpcBaseResult` 模型：

- **RpcBaseParam**: RPC 调用入参基类
- **RpcBaseResult**: RPC 返回值基类

### 2. 服务接口定义

所有 Dubbo 服务接口定义在 `xxpay-core/src/main/java/org/xxpay/core/service/`，以 `I` 开头命名。

服务实现类在 `xxpay-service/src/main/java/org/xxpay/service/impl/`，使用 `@Service` 注解暴露为 Dubbo 服务。

### 3. 支付通道架构

支付通道采用策略模式，位于 `xxpay-pay/src/main/java/org/xxpay/pay/channel/`：

- 每个支付通道独立封装在 `channel/{channel_name}/` 目录
- 继承 `BasePayment` 实现支付下单
- 继承 `BasePayNotify` 实现回调通知

### 4. 消息队列

ActiveMQ 用于异步处理：

- `Mq4PayOrderListener` - 支付订单消息
- `Mq4MchNotify` - 商户通知（xxpay-consumer 消费）

### 5. 数据同步

xxpay-task 将 MySQL 支付订单同步到 MongoDB，用于高性能查询：

- 每 5 分钟创建时间窗口
- 首次同步每 30 秒执行
- 二次同步每 2 分钟执行
- 每天清理 7 天前的数据

## 时区设置

项目统一使用 **Asia/Shanghai** 时区：

- **应用层**: 通过 `@PostConstruct` 设置 `TimeZone.setDefault()`
- **Jackson**: `spring.jackson.time-zone: Asia/Shanghai`
- **数据库**: JDBC URL 使用 `serverTimezone=GMT%2B0`

## Git 提交规范

遵循项目规范：`EZPAY-xxx: 功能描述`

示例：
```
EZPAY-730: 计算功能优化
EZPAY-799: 优化支付通道页面
EZPAY-732: 修复 i18n 问题
```

## 常见问题

### Dubbo shutdown 报错

已知 issue: https://github.com/apache/dubbo/issues/10150

可通过配置日志级别禁用相关错误：
```yaml
logging:
  level:
    org.springframework.jms.listener.DefaultMessageListenerContainer: OFF
    org.apache.curator.framework.recipes.cache.NodeCache: OFF
```

### RPC 超时配置

- xxpay-service provider: 60 秒
- xxpay-pay consumer: 30 秒（必须 >= provider 超时）
- 其他模块 consumer: 10-60 秒

### 数据库连接池

根据 Dubbo 线程数配置：
- 生产环境: Dubbo threads (200) × 0.7 ≈ 140，设为 150
- 测试环境: 设为 200

## 各模块详细文档

每个子模块都有独立的 CLAUDE.md 文件，包含更详细的模块特定信息：

- [xxpay-core](./xxpay-core/CLAUDE.md) - 公共模块
- [xxpay-service](./xxpay-service/CLAUDE.md) - 服务层
- [xxpay-pay](./xxpay-pay/CLAUDE.md) - 支付核心
- [xxpay-manage](./xxpay-manage/CLAUDE.md) - 运营平台
- [xxpay-merchant](./xxpay-merchant/CLAUDE.md) - 商户系统
- [xxpay-agent](./xxpay-agent/CLAUDE.md) - 代理商系统
- [xxpay-task](./xxpay-task/CLAUDE.md) - 定时任务
- [xxpay-flyway](./xxpay-flyway/CLAUDE.md) - 数据库迁移
- [xxpay-consumer](./xxpay-consumer/CLAUDE.md) - 通知消费
- [rbgi](./rbgi/CLAUDE.md) - 银行网关
