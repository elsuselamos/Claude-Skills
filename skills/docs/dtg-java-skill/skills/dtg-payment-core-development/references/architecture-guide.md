# 支付核心架构指南

## 代码架构

### 分层结构
```
Controller (ctrl/) → Service (service/) → Channel (channel/)
     ↓                   ↓                    ↓
REST API           业务逻辑          第三方支付通道适配器
```

### 核心接口和抽象类

| 类名 | 用途 |
|------|------|
| `BaseController` | 所有 Controller 的基类 |
| `BasePayNotify` | 支付回调通知的抽象基类 |
| `BasePayment` | 支付下单的抽象基类 |
| `BaseService` | 通道服务的基类 |
| `PaymentInterface` | 支付通道接口定义 |
| `TransNotifyInterface` | 代付通知接口定义 |

## 支付通道实现模式

```
channel/{channel_name}/
├── {ChannelName}Config.java        # 配置类
├── {ChannelName}DepositChannel.java # 支付通道（继承 BasePayment）
├── {ChannelName}PaymentService.java # 支付服务
├── {ChannelName}TransNotifyService.java # 代付通知服务
├── {ChannelName}SignUtils.java      # 签名工具类
└── model/                           # 请求/响应模型
```

## 支付流程

### 支付下单流程
```
1. 接收支付请求 (PayOrderController)
2. 参数验证
3. 创建支付订单
4. 调用支付通道 (BasePayment)
5. 返回支付信息
```

### 回调通知流程
```
1. 接收第三方回调 (PayNotifyController)
2. 验证回调签名
3. 查询订单状态
4. 更新订单状态
5. 发送商户通知 (ActiveMQ)
6. 返回成功响应
```

## RPC 服务调用

- 默认超时：10 秒
- 重试次数：0
- consumer 超时（30 秒）必须 >= provider 超时（60 秒）
