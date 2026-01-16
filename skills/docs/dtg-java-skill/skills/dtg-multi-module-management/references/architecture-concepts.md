# 核心架构概念

## 模块依赖关系

```
xxpay-pay, xxpay-manage, xxpay-merchant, xxpay-agent, xxpay-task, xxpay-consumer, rbgi
    ↓ 依赖
xxpay-core (公共API、实体、常量)
    ↓ Dubbo RPC 调用
xxpay-service (Dubbo 服务提供者)
    ↓
MySQL + MongoDB + Redis + ActiveMQ
```

## Dubbo RPC 通信模型

- `RpcBaseParam` - RPC 调用入参基类
- `RpcBaseResult` - RPC 返回值基类

## 服务接口定义

- Dubbo 服务接口定义在 `xxpay-core/src/main/java/org/xxpay/core/service/`
- 以 `I` 开头命名
- 服务实现在 `xxpay-service`

## 支付通道架构

- 策略模式，位于 `xxpay-pay/src/main/java/org/xxpay/pay/channel/`
- 继承 `BasePayment` 实现支付下单
- 继承 `BasePayNotify` 实现回调通知

## 消息队列

ActiveMQ 用于异步处理：
- `Mq4PayOrderListener` - 支付订单消息
- `Mq4MchNotify` - 商户通知
- `Mq4MchAgentpayNotify` - 代付通知
