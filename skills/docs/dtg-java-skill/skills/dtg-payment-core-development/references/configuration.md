# 支付核心配置参考

## Dubbo 配置

```yaml
dubbo:
  application:
    name: xxpay-pay
  protocol:
    port: 23020
    threads: 200
  provider:
    timeout: 5000
  consumer:
    timeout: 30000
```

## OkHttp 连接池配置

- 最大空闲连接：100
- 全局最大并发：500
- 单个三方最大并发：100
- 连接保持时间：45 秒

## 熔断器配置

使用 Resilience4j 防止故障商户拖垮通知系统。

```yaml
resilience4j:
  circuitbreaker:
    instances:
      merchantNotify:
        failure-rate-threshold: 50
        wait-duration-in-open-state: 60s
        sliding-window-size: 10
```

## 环境配置

### 环境
- `local` - 本地开发
- `dtg-stg` - 测试环境
- `dtg-prod` - 生产环境

### 关键环境变量

| 变量 | 说明 |
|------|------|
| `ZOOKEEPER` | Dubbo 注册中心地址 |
| `REDIS_HOST` / `REDIS_PASSWORD` | Redis 连接 |
| `ACTIVEMQ_BROKER` / `ACTIVEMQ_USER` / `ACTIVEMQ_PASSWORD` | ActiveMQ 连接 |
| `NODE` | 服务节点标识 |
