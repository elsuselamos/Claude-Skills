# 智能问题诊断指南

本指南介绍如何使用 dtg-java-skill 插件诊断 Spring Boot 2.7 + Dubbo 3 微服务系统中的问题。

## 问题诊断概述

智能问题诊断代理可以自动识别和诊断代码中的各种问题，包括代码异味、性能瓶颈、并发问题和安全漏洞。

### 诊断能力

#### 1. 代码异味识别
- 长方法检测
- 大类检测
- 重复代码检测
- 深层嵌套检测
- 参数过多检测
- 特性嫉妒检测

#### 2. 性能瓶颈诊断
- 数据库性能问题
- 内存使用分析
- 并发性能问题
- 缓存策略分析
- 网络性能问题

#### 3. 并发问题分析
- 线程安全问题
- 死锁风险识别
- 资源竞争检测
- 并发性能瓶颈

#### 4. 配置问题诊断
- 配置错误检测
- 版本兼容性检查
- 配置优化建议

## 使用方式

### 触发问题诊断

```
"诊断我的代码问题"
"分析性能瓶颈"
"diagnose problems"
"check code quality"
```

### 指定诊断范围

```
"诊断 UserService 类的性能问题"
"分析 xxpay-pay 模块的代码质量"
"检查数据库查询性能"
```

## 诊断报告示例

```markdown
## 诊断概述
- 诊断范围: xxpay-pay 模块
- 诊断时间: 2024-01-01 10:30:00
- 分析方法: 静态代码分析 + 性能模式识别

## 整体健康状况
- 代码健康指数: 72/100
- 性能风险评估: 中等
- 维护复杂度: 中等

## 发现的问题

### 🔴 高风险问题

#### 1. 长方法: OrderService.createOrder()
- 位置: OrderService.java:125
- 当前长度: 156 行
- 问题严重性: 严重
- 根本原因: 方法承担了过多职责
- 潜在影响: 难以测试、难以维护、可读性差
- 修复建议:
  将方法拆分为多个小方法：
  ```java
  public Order createOrder(CreateOrderRequest request) {
      validateRequest(request);
      Order order = buildOrder(request);
      deductInventory(request);
      saveOrder(order);
      sendNotification(order);
      return order;
  }
  ```

#### 2. N+1 查询问题: OrderItemService.listByOrderId()
- 位置: OrderItemService.java:45
- 问题严重性: 高
- 根本原因: 在循环中执行数据库查询
- 性能影响: 当订单项数量多时，性能急剧下降
- 修复建议:
  使用批量查询或 JOIN：
  ```java
  // 不推荐
  for (Order order : orders) {
      List<Item> items = itemRepository.findByOrderId(order.getId());
  }

  // 推荐
  List<Order> orders = orderRepository.findAllWithItems();
  ```

### 🟡 中风险问题

#### 3. 潜在的线程安全问题: CacheManager.get()
- 位置: CacheManager.java:23
- 问题严重性: 中等
- 根本原因: ConcurrentHashMap 的复合操作不是原子的
- 潜在影响: 缓存穿透、重复计算
- 修复建议:
  使用原子操作或加锁：
  ```java
  public Value get(Key key) {
      return cache.computeIfAbsent(key, k -> loadValue(k));
  }
  ```

### 🟢 低风险问题（优化建议）

#### 4. 魔法数字: PaymentService.process()
- 位置: PaymentService.java:89
- 优化收益: 提升可读性
- 实施难度: 低
- 优化建议:
  提取为常量：
  ```java
  private static final int MAX_RETRY_COUNT = 3;
  private static final int RETRY_DELAY_MS = 1000;
  ```

## 性能瓶颈分析

### 数据库性能
- 查询性能: 存在 N+1 问题，建议使用批量查询
- 连接池配置: 最大连接数偏小，建议增加到 50
- 索引优化: order_status 字段缺少索引

### 内存使用
- 大对象创建: OrderReportService 每次创建大对象，建议使用对象池
- 缓存配置: 缓存过期时间过短，建议延长到 1 小时

### 并发性能
- 锁竞争: PaymentService 使用 synchronized 锁，建议升级为 ReentrantLock
- 线程池配置: 核心线程数偏小，建议根据 CPU 核心数调整

## 修复方案

### 立即修复（高优先级）

1. **重构长方法**: OrderService.createOrder()
   - 步骤1: 提取验证逻辑
   - 步骤2: 提取库存扣减逻辑
   - 步骤3: 提取通知逻辑
   - 步骤4: 添加单元测试

2. **修复 N+1 查询**: OrderItemService.listByOrderId()
   - 步骤1: 修改 Mapper 使用 JOIN
   - 步骤2: 测试查询性能
   - 步骤3: 部署到测试环境验证

### 渐进式改进（中优先级）

1. **优化缓存策略**
   - 第一阶段: 调整缓存过期时间
   - 第二阶段: 引入多级缓存
   - 第三阶段: 实施缓存预热

### 长期优化（低优先级）

1. **重构支付服务**
   - 引入策略模式处理不同支付渠道
   - 实施异步处理提升性能
```

## 常见问题类型

### 1. 代码异味

#### 长方法（Long Method）

**识别标准**:
- 方法超过 50 行
- 圈复杂度 > 10
- 嵌套层级 > 3

**修复方法**:
```java
// 重构前
public void processOrder(Order order) {
    // 150 行代码...
}

// 重构后
public void processOrder(Order order) {
    validateOrder(order);
    calculatePrice(order);
    updateInventory(order);
    saveOrder(order);
    sendNotification(order);
}
```

#### 大类（Large Class）

**识别标准**:
- 类超过 500 行
- 方法数量 > 20
- 职责不单一

**修复方法**:
- 拆分为多个小类
- 提取接口
- 使用委托模式

#### 重复代码（Duplicated Code）

**识别标准**:
- 相似代码片段 > 10 行
- 重复次数 > 3

**修复方法**:
```java
// 重构前
public class UserService {
    public void createUser(User user) {
        validate(user);
        save(user);
        log(user);
    }
}

public class ProductService {
    public void createProduct(Product product) {
        validate(product);
        save(product);
        log(product);
    }
}

// 重构后
public abstract class BaseService<T> {
    public void create(T entity) {
        validate(entity);
        save(entity);
        log(entity);
    }
}
```

### 2. 性能问题

#### N+1 查询

**问题特征**:
```java
// 1 次查询获取所有订单
List<Order> orders = orderRepository.findAll();

// N 次查询获取每个订单的项
for (Order order : orders) {
    List<Item> items = itemRepository.findByOrderId(order.getId());
}
```

**解决方案**:
```java
// 使用 JOIN 一次查询
List<Order> orders = orderRepository.findAllWithItems();

// 或使用批量查询
List<Long> orderIds = orders.stream()
    .map(Order::getId)
    .collect(Collectors.toList());
Map<Long, List<Item>> itemsMap = itemRepository.findByOrderIds(orderIds);
```

#### 缓存穿透

**问题特征**:
```java
// 恶意查询不存在的 key，绕过缓存，直击数据库
User user = cache.get(userId);
if (user == null) {
    user = repository.findById(userId);  // 每次都查数据库
}
```

**解决方案**:
```java
// 使用布隆过滤器或缓存空值
User user = cache.get(userId);
if (user == null) {
    user = repository.findById(userId);
    if (user == null) {
        // 缓存空值，短时间过期
        cache.put(userId, NULL_USER, 60);
    }
}
```

### 3. 并发问题

#### 线程安全问题

**问题示例**:
```java
@Service
public class CounterService {
    private int count = 0;  // 非线程安全

    public void increment() {
        count++;  // 不是原子操作
    }
}
```

**解决方案**:
```java
@Service
public class CounterService {
    private final AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();
    }
}
```

#### 死锁风险

**问题特征**:
- 多个线程按不同顺序获取锁
- 持有锁的同时等待其他资源

**解决方案**:
- 统一锁获取顺序
- 使用定时锁
- 实施死锁检测

### 4. 配置问题

#### 连接池配置不当

**问题示例**:
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 5  # 太小
```

**建议配置**:
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 50
      minimum-idle: 10
      connection-timeout: 30000
      idle-timeout: 600000
```

#### 超时配置不当

**问题示例**:
```yaml
dubbo:
  provider:
    timeout: 60000  # 太长
```

**建议配置**:
```yaml
dubbo:
  provider:
    timeout: 5000  # 5秒

  consumer:
    timeout: 3000  # 3秒
    retries: 2     # 失败重试2次
```

## 诊断工具

### 静态代码分析

插件内置的静态分析功能：
- 代码结构分析
- 依赖关系分析
- 复杂度计算

### 性能模式识别

自动识别性能问题模式：
- 数据库查询模式
- 缓存使用模式
- 资源使用模式

### 最佳实践对比

与行业最佳实践对比：
- Spring Boot 最佳实践
- Dubbo 微服务最佳实践
- Java 编码最佳实践

## 改进建议优先级

### P0: 必须立即修复
- 安全漏洞
- 严重性能问题
- 数据丢失风险

### P1: 尽快修复
- 代码异味
- 一般性能问题
- 可维护性问题

### P2: 计划修复
- 优化建议
- 最佳实践改进
- 代码风格统一

---

**相关文档**: [智能功能指南](intelligent-features.md) | [架构分析指南](architecture-analysis.md)
