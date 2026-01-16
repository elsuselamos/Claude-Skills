# 智能架构分析指南

本指南介绍如何使用 dtg-java-skill 插件进行 Spring Boot 2.7 + Dubbo 3 微服务架构分析。

## 架构分析概述

智能架构分析代理基于领域驱动设计（DDD）原则和微服务最佳实践，对您的系统进行全面评估。

### 分析维度

#### 1. 微服务边界评估
- 限界上下文划分合理性
- 业务能力映射完整性
- 服务职责单一性
- 数据一致性边界

#### 2. 架构模式识别
- 分层架构实现质量
- 六边形架构应用
- CQRS 模式使用
- 事件驱动架构

#### 3. 性能架构分析
- 缓存策略合理性
- 数据库架构评估
- 消息队列使用
- 连接池配置

#### 4. 容错架构分析
- 熔断机制
- 降级策略
- 重试机制
- 限流保护

## 使用方式

### 触发架构分析

```
"分析我的微服务架构"
"评估服务边界"
"review architecture"
```

### 分析范围

可以指定分析范围：
```
"分析 xxpay-pay 模块的架构"
"评估支付核心服务的设计"
```

## 分析报告示例

```markdown
## 架构健康度评分

- 总体架构质量: B
- 微服务合理性: 良好
- 扩展性能力: 中等
- 维护复杂度: 中等
- 技术债务指数: 45

## 微服务边界分析

### xxpay-pay (支付核心)
- 职责清晰度: 清晰
- DDD 边界: 符合
- 业务能力映射: 完整
- 改进建议: 考虑将回调处理拆分为独立服务

### xxpay-manage (运营平台)
- 职责清晰度: 部分清晰
- DDD 边界: 部分符合
- 改进建议: 报表功能建议拆分为独立服务

## 架构模式识别

- ✅ 分层架构: 实现良好
- ⚠️ 六边形架构: 部分应用
- ❌ CQRS: 未应用
- ✅ 事件驱动: 应用良好

## 性能架构评估

### 缓存架构
- 策略: 合理
- 一致性: 需要改进
- 建议: 考虑引入缓存预热机制

### 数据库架构
- 读写分离: 未实施
- 建议: 对高频查询接口实施读写分离

## 容错架构评估

- 熔断: 已实施（Resilience4j）
- 降级: 部分实施
- 建议: 为所有外部服务调用配置降级策略
```

## DDD 架构评估

### 限界上下文划分

**良好的限界上下文**:
- 清晰的业务边界
- 独立的数据模型
- 明确的团队职责
- 独立的部署单元

**评估标准**:
```
优秀: 完全符合 DDD 原则
良好: 基本符合，有小瑕疵
一般: 部分符合，需要改进
差: 不符合，需要重构
```

### 聚合设计

**聚合设计原则**:
- 聚合根是唯一的访问入口
- 聚合内保持强一致性
- 聚合间使用最终一致性
- 聚合设计小而精

**示例**:
```java
// 好的聚合设计
public class Order {
    // 聚合根
    private OrderId orderId;

    // 实体（属于聚合）
    private List<OrderItem> items;

    // 值对象
    private Money totalAmount;

    // 修改聚合状态的方法
    public void addItem(Product product, int quantity) {
        OrderItem item = new OrderItem(product, quantity);
        this.items.add(item);
        this.totalAmount = calculateTotal();
    }

    // 不直接暴露内部集合
    public List<OrderItem> getItems() {
        return Collections.unmodifiableList(items);
    }
}
```

### 领域事件

**事件设计原则**:
```java
// 领域事件
public class OrderCreatedEvent {
    private final OrderId orderId;
    private final Money totalAmount;
    private final Instant occurredOn;

    // 事件应该是不可变的
    public OrderCreatedEvent(OrderId orderId, Money totalAmount) {
        this.orderId = orderId;
        this.totalAmount = totalAmount;
        this.occurredOn = Instant.now();
    }
}

// 发布事件
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public void createOrder(Order order) {
        // 保存订单
        orderRepository.save(order);

        // 发布领域事件
        eventPublisher.publishEvent(
            new OrderCreatedEvent(order.getId(), order.getTotalAmount())
        );
    }
}
```

## 架构模式识别

### 分层架构

**标准分层**:
```
┌─────────────────────────┐
│   Presentation Layer    │  Controller + DTO
├─────────────────────────┤
│   Application Layer     │  Application Service
├─────────────────────────┤
│    Domain Layer         │  Entity + Domain Service
├─────────────────────────┤
│  Infrastructure Layer   │  Repository + External Service
└─────────────────────────┘
```

### 六边形架构

**端口和适配器**:
```java
// 端口（接口）
public interface PaymentPort {
    PaymentResult payment(PaymentRequest request);
}

// 适配器（实现）
@Component
public class AlipayAdapter implements PaymentPort {
    public PaymentResult payment(PaymentRequest request) {
        // 调用支付宝 API
    }
}
```

### CQRS 模式

**命令查询分离**:
```java
// 命令端（写）
@Component
public class OrderCommandHandler {
    public void handle(CreateOrderCommand command) {
        // 处理写操作
    }
}

// 查询端（读）
@Component
public class OrderQueryHandler {
    public OrderView handle(GetOrderQuery query) {
        // 处理读操作，可能使用不同的数据模型
    }
}
```

## 性能架构评估

### 缓存架构

**多级缓存**:
```
┌──────────────┐
│ 本地缓存     │  L1: Caffeine/Guava
├──────────────┤
│ 分布式缓存   │  L2: Redis
├──────────────┤
│   数据库     │
└──────────────┘
```

**缓存策略**:
- Cache-Aside: 旁路缓存
- Read-Through: 读穿透
- Write-Through: 写穿透
- Write-Behind: 异步写

### 数据库架构

**读写分离**:
```java
@Service
public class UserService {
    @Autowired
    private UserWriteMapper writeMapper;  // 主库

    @Autowired
    private UserReadMapper readMapper;    // 从库

    @Transactional
    public void createUser(User user) {
        writeMapper.insert(user);
    }

    public User findById(Long id) {
        return readMapper.selectById(id);
    }
}
```

## 容错架构评估

### 熔断机制

**Resilience4j 配置**:
```yaml
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        failure-rate-threshold: 50
        wait-duration-in-open-state: 60s
        sliding-window-size: 10
```

### 降级策略

**实现降级**:
```java
@Service
public class PaymentServiceFallback implements PaymentService {
    @Override
    public PaymentResult payment(PaymentRequest request) {
        // 降级逻辑：返回默认值或排队处理
        return PaymentResult.pending();
    }
}
```

### 重试机制

**重试配置**:
```java
@Retryable(
    value = {RemoteServiceException.class},
    maxAttempts = 3,
    backoff = @Backoff(delay = 1000)
)
public PaymentResult callPaymentService(PaymentRequest request) {
    // 远程调用
}
```

## 架构演进建议

### 短期优化（1-3个月）

1. **优化服务边界**
   - 重新评估服务职责
   - 拆分过大服务
   - 合并过度拆分的服务

2. **实施容错机制**
   - 添加熔断器
   - 实现降级策略
   - 配置重试机制

### 中期重构（3-6个月）

1. **引入 CQRS**
   - 分离命令和查询模型
   - 优化读写性能
   - 实现事件溯源

2. **实施事件驱动**
   - 引入消息队列
   - 实现异步通信
   - 构建事件总线

### 长期演进（6个月以上）

1. **完整 DDD 实施**
   - 建立领域模型
   - 实现聚合设计
   - 完善领域事件

2. **微服务治理**
   - 服务网格
   - 分布式追踪
   - 自动化运维

---

**相关文档**: [智能功能指南](intelligent-features.md) | [问题诊断指南](problem-diagnosis.md)
