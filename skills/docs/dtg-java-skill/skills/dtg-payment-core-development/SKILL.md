---
name: dtg-payment-core-development
description: This skill should be used when the user asks to "develop payment module", "create payment channel", "implement payment gateway", "add payment method", "payment callback", "payment integration", or mentions payment processing, payment channels, payment notification, or deposit/withdrawal implementation. Provides xxpay-pay payment core module development guidance for Spring Boot 2.7 + Dubbo 3 payment system.
version: 3.0.0
tags: ["payment", "payment-gateway", "channel-integration", "callback"]
---

# 支付核心开发技能

xxpay-pay 是 DTG 支付系统的支付处理微服务。

## 模块信息

| 属性 | 值 |
|------|-----|
| 模块名称 | xxpay-pay |
| 模块类型 | 支付核心 |
| HTTP 端口 | 3020 |
| Dubbo 端口 | 23020 |
| 主要职责 | 支付渠道对接、支付订单处理、商户通知 |

## 技术栈

| 技术 | 版本 |
|------|------|
| Java | 11 |
| Spring Boot | 2.7.18 |
| Apache Dubbo | 3.2.14 |
| MyBatis Plus | 3.5.7 |
| OkHttp | 4.12.0 |
| Resilience4j | 1.7.1 |

## 构建和运行

```bash
# 编译依赖模块
./mvnw -f ../xxpay-core clean install -Dmaven.test.skip=true

# 编译当前模块
./mvnw clean package -Dmaven.test.skip=true

# 运行
mvn spring-boot:run
# 或
java -jar target/xxpay-pay-1.0.0.jar --spring.profiles.active=dtg-prod
```

## Git 提交规范

`EZPAY-xxx: 功能描述`

示例：
```
EZPAY-730: 计算功能优化
EZPAY-799: 优化支付通道页面
```

## 参考资源

- [架构指南](references/architecture-guide.md) - 代码架构、核心接口、支付流程
- [配置参考](references/configuration.md) - Dubbo/OkHttp/熔断器配置、环境变量
