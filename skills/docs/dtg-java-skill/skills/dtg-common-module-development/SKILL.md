---
name: dtg-common-module-development
description: This skill should be used when the user asks to "develop common module", "create shared utilities", "define common entities", "API interfaces", "common services", or mentions shared code, common libraries, entity definitions, or API interfaces. Provides xxpay-core common module development guidance including entity beans, API interfaces, constants, and utilities.
version: 3.0.0
tags: ["common-module", "entity", "service-interface", "utilities", "constants"]
---

# xxpay-core 公共模块开发技能

xxpay-core 是 DTG-Pay 支付系统的核心公共模块。

## 模块信息

| 属性 | 值 |
|------|-----|
| 模块名称 | xxpay-core |
| 模块类型 | 公共模块 |
| 打包方式 | jar |
| 主要职责 | 实体 Bean、Dubbo 服务接口定义、常量、工具类 |

## 技术栈

| 技术 | 版本 |
|------|------|
| Java | 11 |
| Spring Boot | 2.7.18 |
| Dubbo | 3.2.14 |
| MyBatis-Plus | 3.5.7 |
| FastJSON2 | 2.0.51 |
| OkHttp | 4.12.0 |

## 构建命令

```bash
# 编译并安装到本地仓库（跳过测试）
./mvnw -f xxpay-core clean install -Dmaven.test.skip=true

# 单独编译当前模块
mvn clean install -Dmaven.test.skip=true
```

> 注意：xxpay-core 没有 main 类，作为 jar 库被其他模块依赖。

## 代码架构

### 包结构
```
org.xxpay.core/
├── common/           # 公共组件
│   ├── annotation/   # 注解 (@I18n, @MethodLog)
│   ├── constant/     # 常量定义
│   ├── domain/       # 通用领域对象 (RpcBaseParam, RpcBaseResult)
│   ├── enumm/        # 枚举类
│   ├── Exception/    # 自定义异常
│   ├── util/         # 工具类
│   └── vo/           # 值对象
├── dto/              # 数据传输对象
├── entity/           # 数据库实体
├── service/          # Dubbo服务接口定义
├── document/         # MongoDB文档定义
└── springboot/       # Spring配置
```

## 核心概念

### RPC 通信模型
- `RpcBaseParam` - RPC 调用入参基类
- `RpcBaseResult` - RPC 返回值基类

### 返回码枚举
- `RetEnum` - 业务返回码定义
- 按模块分类：公共(10xxx)、业务中心(11xxx)、商户系统(12xxx)

### 实体类特点
- `@TableName` 指定表名
- `@TableId` 指定主键（通常为 `IdType.INPUT`）
- `@TableField` 映射字段名
- 使用 Lombok 注解简化代码

### 服务接口定义
- 接口命名以 `I` 开头
- 位于 `org.xxpay.core.service` 包下
- 默认方法提供空实现，由 xxpay-service 模块实现

### 国际化支持
- 使用 `@I18n` 注解标记需要国际化的字段
- 支持 prefix 属性指定国际化 key 前缀

### 异常处理
- `ServiceException` - 业务异常
- 携带 `RetEnum` 和 `extraMsg`

## 常量定义

### MchConstant（商户相关常量）
- 商户状态：INIT(0), ACTIVE(1), STOP(2)
- 业务类型：PAY(1), AGENTPAY(2)
- 结算方式：DAILY(1), WEEKLY(2), MANUAL(3)

### PayConstant（支付相关常量）
- 支付渠道：alipay, wxpay, unionpay
- 订单状态：INIT(0), PAYING(1), SUCCESS(2), FAIL(3), REFUND(4)
- 支付方式：alipay_sdk, wxpay_sdk, fast_pay

### RedisConstant（Redis 相关常量）
- Key 前缀：`xxpay:`
- 过期时间：EXPIRE_HOUR(3600), EXPIRE_DAY(86400)

## 工具类

| 工具类 | 功能 |
|--------|------|
| `SignatureUtils` | 签名生成和验证 |
| `DateUtils` | 时间戳、流水号生成 |
| `OkHttpClientUtil` | HTTP POST 请求 |

## 开发指南

### 添加新实体
1. 在 `xxpay-generator` 生成 MyBatis 代码
2. 将 Model 拷贝到 `xxpay-core/entity`
3. 将 Mapper 拷贝到 `xxpay-service`
4. 在 `xxpay-core/service` 创建服务接口
5. 在 `xxpay-service` 创建实现类

### 添加新常量
- 支付渠道常量添加到 `PayConstant`
- 业务返回码添加到 `RetEnum`
- 商户业务类型添加到 `MchConstant`

### 添加新服务接口
1. 在 `org.xxpay.core.service` 包下创建接口
2. 接口命名以 `I` 开头
3. 定义方法签名和返回值
4. 添加 Javadoc 注释

## 时区配置

项目使用 **Asia/Shanghai** 时区：
- Spring Jackson: `spring.jackson.time-zone: "Asia/Shanghai"`
- JDBC URL: `serverTimezone=GMT%2B0`
- Java Main: 通过 `@PostConstruct` 设置 `TimeZone.setDefault()`

## 依赖配置

### Provided 依赖
- MyBatis-Plus (provided)
- MongoDB (provided)
- Redis (provided)

## 日志

使用 `@MethodLog` 注解记录方法调用日志，MDC 工具类 (`MDCs`) 用于设置 traceId。

## 部署顺序

部署时需按以下顺序发布：
1. xxpay-flyway
2. xxpay-core
3. xxpay-service
4. 其他模块

## 相关模块

xxpay-core 是以下模块的基础依赖：
- xxpay-service
- xxpay-manage
- xxpay-merchant
- xxpay-agent
- xxpay-pay
- xxpay-task
- xxpay-consumer
- rbgi
