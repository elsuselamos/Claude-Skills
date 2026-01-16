---
name: dtg-multi-module-management
description: This skill should be used when the user asks to "manage modules", "compile multiple modules", "build maven project", "module dependencies", "project structure", or mentions maven multi-module project, module compilation, or module coordination. Provides dtg-pay multi-module Maven project management guidance including module structure, dependencies, build order, and environment configuration.
version: 3.0.0
tags: ["multi-module", "maven", "project-structure", "module-detection"]
---

# dtg-pay 多模块项目管理

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

## 模块信息表

| 模块 | HTTP端口 | Dubbo端口 | 类型 | 对应技能 |
|------|----------|-----------|------|---------|
| rbgi | 8195 | - | 银行网关 | - |
| xxpay-agent | 8192 | 28192 | 代理商系统 | dtg-admin-panel-development |
| xxpay-consumer | 3120 | 23120 | 通知消费者 | - |
| xxpay-core | - | - | 公共模块 | dtg-common-module-development |
| xxpay-flyway | - | - | 数据库迁移 | - |
| xxpay-manage | 8193 | 28193 | 运营平台 | dtg-admin-panel-development |
| xxpay-merchant | 8191 | 28191 | 商户系统 | dtg-admin-panel-development |
| xxpay-task | 8194 | 28194 | 定时任务 | - |
| xxpay-pay | 3020 | 23020 | 支付核心 | dtg-payment-core-development |
| xxpay-service | 8190 | 28190 | Dubbo 服务提供者 | - |

## 参考资源

- [构建指南](references/build-guide.md) - 部署顺序、编译命令、环境配置
- [架构概念](references/architecture-concepts.md) - 模块依赖关系、Dubbo RPC、消息队列
