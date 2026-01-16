# 架构原则

## 🏛️ Spring Boot 2.7 + Dubbo 3 企业级微服务架构原则

本文档定义了 ai-coding-java 项目中微服务架构的核心原则和最佳实践，确保系统的可扩展性、可维护性和高可用性。

## [TARGET] 核心架构原则

### 1. 单一职责原则 (Single Responsibility Principle)
每个微服务应该专注于单一业务领域，保持服务边界的清晰性。

```java
// [OK] 正确 - 用户服务专注用户管理
@Service
public class UserService {
    // 用户注册、登录、信息管理
}

// [OK] 正确 - 订单服务专注订单处理
@Service
public class OrderService {
    // 订单创建、支付、状态跟踪
}

// [X] 错误 - 混合职责
@Service
public class UserAndOrderService {
    // 既处理用户管理，又处理订单处理
}
```

### 2. 高内聚低耦合 (High Cohesion, Low Coupling)
服务内部组件高度内聚，服务之间通过明确的接口进行松耦合通信。

```java
// [OK] 正确 - 明确的服务接口定义
@DubboService(version = "1.0.0")
public class UserServiceImpl implements UserService {
    // 实现用户相关业务逻辑，不直接依赖其他服务
}

// [OK] 正确 - 通过 Dubbo 接口调用其他服务
@DubboReference(version = "1.0.0")
private PaymentService paymentService;
```

### 3. 领域驱动设计 (Domain Driven Design)
基于业务领域进行服务划分，每个服务对应一个明确的业务领域。

```java
// 用户聚合根
@Entity
@Table(name = "users")
public class User {
    private Long id;
    private String username;
    private String email;
    // 用户相关属性和方法
}

// 订单聚合根
@Entity
@Table(name = "orders")
public class Order {
    private Long id;
    private String orderNumber;
    private BigDecimal amount;
    // 订单相关属性和方法
}
```

## [ARCHITECTURE] 微服务设计原则

### 1. 服务边界划分

#### 业务能力边界
```
用户服务 (User Service)
├── 用户注册和认证
├── 用户信息管理
├── 权限和角色管理
└── 用户偏好设置

订单服务 (Order Service)
├── 订单创建和管理
├── 订单状态跟踪
├── 订单查询和统计
└── 订单取消和退款

支付服务 (Payment Service)
├── 支付方式管理
├── 支付处理
├── 退款处理
└── 支付记录查询

库存服务 (Inventory Service)
├── 商品库存管理
├── 库存预留和释放
├── 库存预警
└── 库存统计
```

#### 数据一致性边界
```java
// [OK] 正确 - 每个服务管理自己的数据
@Service
@Transactional
public class OrderService {
    @Autowired
    private OrderRepository orderRepository; // 订单数据

    // 通过服务调用操作其他服务的数据
    @DubboReference
    private InventoryService inventoryService;

    @DubboReference
    private PaymentService paymentService;
}

// [X] 错误 - 跨服务直接访问数据库
@Service
public class OrderService {
    @Autowired
    private InventoryRepository inventoryRepository; // 不应该直接访问其他服务的数据
}
```

### 2. API 设计原则

#### RESTful API 设计
```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @GetMapping("/{userId}")
    public UserResponse getUser(@PathVariable Long userId) {
        // GET /api/v1/users/123 - 获取用户信息
    }

    @PostMapping
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        // POST /api/v1/users - 创建用户
    }

    @PutMapping("/{userId}")
    public UserResponse updateUser(@PathVariable Long userId,
                                  @Valid @RequestBody UpdateUserRequest request) {
        // PUT /api/v1/users/123 - 更新用户信息
    }

    @DeleteMapping("/{userId}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long userId) {
        // DELETE /api/v1/users/123 - 删除用户
    }
}
```

#### Dubbo 服务接口设计
```java
// [OK] 正确 - 明确的服务接口定义
public interface UserService {

    /**
     * 创建用户
     * @param request 创建用户请求
     * @return 用户信息
     */
    UserResponse createUser(UserRequest request);

    /**
     * 根据ID获取用户
     * @param userId 用户ID
     * @return 用户信息，不存在时返回null
     */
    UserResponse getUserById(Long userId);

    /**
     * 验证用户凭证
     * @param username 用户名
     * @param password 密码
     * @return 验证结果
     */
    AuthResult authenticate(String username, String password);
}
```

## [TOOL] 技术架构原则

### 1. 分层架构
```
┌─────────────────────────────────────┐
│           API Layer                 │  <- REST API, Dubbo Service
├─────────────────────────────────────┤
│         Application Layer           │  <- 业务编排, 事务管理
├─────────────────────────────────────┤
│          Domain Layer               │  <- 业务逻辑, 领域模型
├─────────────────────────────────────┤
│       Infrastructure Layer          │  <- 数据访问, 外部服务
└─────────────────────────────────────┘
```

### 2. 依赖注入原则
```java
@Service
public class UserServiceImpl implements UserService {

    // [OK] 正确 - 依赖接口而不是具体实现
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final NotificationService notificationService;

    // [OK] 正确 - 构造函数注入
    public UserServiceImpl(UserRepository userRepository,
                          PasswordEncoder passwordEncoder,
                          NotificationService notificationService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.notificationService = notificationService;
    }

    // [OK] 正确 - 遵循单一职责
    public UserResponse createUser(UserRequest request) {
        // 业务逻辑编排
        validateRequest(request);
        User user = buildUser(request);
        User savedUser = userRepository.save(user);
        notificationService.sendWelcomeEmail(savedUser);
        return convertToResponse(savedUser);
    }
}
```

### 3. 配置外部化
```java
@ConfigurationProperties(prefix = "app.user")
@Data
public class UserConfigProperties {
    private int maxLoginAttempts = 3;
    private Duration sessionTimeout = Duration.ofMinutes(30);
    private boolean emailVerificationRequired = true;
}

@Service
public class UserService {

    @Autowired
    private UserConfigProperties config;

    public void authenticateUser(String username, String password) {
        // 使用外部化配置
        if (loginAttempts >= config.getMaxLoginAttempts()) {
            lockAccount(username);
        }
    }
}
```

## 🔄 通信架构原则

### 1. 同步通信
```java
@Service
public class OrderService {

    // [OK] 正确 - 同步调用，适用于需要立即响应的场景
    @DubboReference(version = "1.0.0", timeout = 5000)
    private PaymentService paymentService;

    @Transactional
    public OrderResponse createOrder(OrderRequest request) {
        // 创建订单
        Order order = buildOrder(request);
        order = orderRepository.save(order);

        // 同步支付处理
        PaymentResult paymentResult = paymentService.processPayment(
            PaymentRequest.builder()
                .orderId(order.getId())
                .amount(order.getAmount())
                .build()
        );

        // 更新订单状态
        if (paymentResult.isSuccess()) {
            order.setStatus(OrderStatus.PAID);
            orderRepository.save(order);
        }

        return convertToResponse(order);
    }
}
```

### 2. 异步通信
```java
@Service
public class OrderService {

    // [OK] 正确 - 异步事件，适用于不需要立即处理的场景
    @Autowired
    private ApplicationEventPublisher eventPublisher;

    @Transactional
    public OrderResponse createOrder(OrderRequest request) {
        Order order = buildOrder(request);
        order = orderRepository.save(order);

        // 异步发送订单创建事件
        eventPublisher.publishEvent(
            OrderCreatedEvent.builder()
                .orderId(order.getId())
                .userId(order.getUserId())
                .amount(order.getAmount())
                .build()
        );

        return convertToResponse(order);
    }
}

@Component
public class OrderEventHandler {

    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 异步处理库存扣减
        inventoryService.reserveInventory(event);

        // 异步发送确认邮件
        emailService.sendOrderConfirmation(event);
    }
}
```

### 3. 消息驱动架构
```java
@Component
public class OrderMessageHandler {

    @JmsListener(destination = "order.created")
    public void handleOrderCreated(OrderCreatedMessage message) {
        // 处理订单创建消息
        processOrderCreation(message);
    }

    @JmsListener(destination = "payment.completed")
    public void handlePaymentCompleted(PaymentCompletedMessage message) {
        // 处理支付完成消息
        updateOrderStatus(message);
    }
}
```

## [CHART] 数据架构原则

### 1. 数据库分离
```yaml
# 每个服务使用独立的数据库
spring:
  datasource:
    url: jdbc:mysql://user-db:3306/user_service?useUnicode=true&characterEncoding=utf8
    username: ${DB_USERNAME:user_service}
    password: ${DB_PASSWORD:password}
```

### 2. 数据一致性策略

#### 最终一致性
```java
@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @DubboReference
    private InventoryService inventoryService;

    @DubboReference
    private NotificationService notificationService;

    @Transactional
    public OrderResponse createOrder(OrderRequest request) {
        // 1. 创建订单（本地事务）
        Order order = buildOrder(request);
        order = orderRepository.save(order);

        // 2. 预留库存（远程调用，可能失败）
        try {
            inventoryService.reserveInventory(
                InventoryReserveRequest.builder()
                    .productId(request.getProductId())
                    .quantity(request.getQuantity())
                    .orderId(order.getId())
                    .build()
            );
        } catch (Exception e) {
            // 记录补偿任务，后续重试
            compensationService.scheduleInventoryReserve(order);
        }

        // 3. 发送异步通知
        notificationService.sendOrderCreatedNotification(order);

        return convertToResponse(order);
    }
}
```

#### Saga 模式实现
```java
@Component
public class OrderSaga {

    @SagaOrchestrationStart
    public void startCreateOrderSaga(OrderRequest request) {
        OrderSagaData sagaData = new OrderSagaData();
        sagaData.setRequest(request);

        // 步骤1：创建订单
        sagaManager.addStep(
            new CreateOrderStep(),
            sagaData,
            compensation -> new CancelOrderStep()
        );

        // 步骤2：预留库存
        sagaManager.addStep(
            new ReserveInventoryStep(),
            sagaData,
            compensation -> new ReleaseInventoryStep()
        );

        // 步骤3：处理支付
        sagaManager.addStep(
            new ProcessPaymentStep(),
            sagaData,
            compensation -> new RefundPaymentStep()
        );

        sagaManager.start(sagaData);
    }
}
```

### 3. 缓存策略
```java
@Service
public class UserService {

    // [OK] 正确 - 多级缓存策略
    @Cacheable(value = "users", key = "#userId")
    public User getUserById(Long userId) {
        return userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId));
    }

    // [OK] 正确 - 缓存预热
    @PostConstruct
    public void warmUpCache() {
        List<User> activeUsers = userRepository.findActiveUsers();
        activeUsers.forEach(user ->
            cacheManager.getCache("users").put(user.getId(), user)
        );
    }

    // [OK] 正确 - 缓存失效策略
    @CacheEvict(value = "users", key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
}
```

## 🔒 安全架构原则

### 1. API 安全
```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @GetMapping("/{userId}")
    @PreAuthorize("hasRole('USER') or #userId == authentication.principal.userId")
    public UserResponse getUser(@PathVariable Long userId) {
        // 用户只能查看自己的信息或需要管理员权限
    }

    @PostMapping
    @RateLimiter(name = "createUser", fallbackMethod = "createUserFallback")
    @PreAuthorize("hasRole('ADMIN')")
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        // 需要管理员权限且限流保护
    }
}
```

### 2. 服务间认证
```java
@Configuration
public class DubboSecurityConfig {

    @Bean
    public Filter registrationFilter() {
        return new ConsumerContextFilter();
    }

    @Bean
    public Filter invokeFilter() {
        return new AuthenticationFilter();
    }
}
```

## 📈 可扩展性原则

### 1. 水平扩展
```yaml
# 应用配置支持多实例部署
server:
  port: ${SERVER_PORT:8080}

# Dubbo 配置支持集群部署
dubbo:
  protocol:
    port: ${DUBBO_PORT:20880}
  registry:
    address: nacos://nacos-cluster:8848
```

### 2. 数据库扩展
```java
// [OK] 正确 - 读写分离
@Configuration
public class DatabaseConfig {

    @Bean
    @Primary
    public DataSource masterDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean
    public DataSource slaveDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean
    public DataSource routingDataSource() {
        RoutingDataSource routingDataSource = new RoutingDataSource();
        Map<Object, Object> dataSourceMap = new HashMap<>();
        dataSourceMap.put("master", masterDataSource());
        dataSourceMap.put("slave", slaveDataSource());
        routingDataSource.setTargetDataSources(dataSourceMap);
        routingDataSource.setDefaultTargetDataSource(masterDataSource());
        return routingDataSource;
    }
}
```

### 3. 服务发现与负载均衡
```java
@Configuration
public class DubboConfig {

    @Bean
    public LoadBalance loadBalance() {
        return new RoundRobinLoadBalance(); // 轮询负载均衡
    }

    @Bean
    public Cluster cluster() {
        return new FailoverCluster(); // 失败重试
    }
}
```

## [SEARCH] 监控与治理原则

### 1. 健康检查
```java
@Component
public class CustomHealthIndicator implements HealthIndicator {

    @Autowired
    private DatabaseHealthChecker databaseHealthChecker;

    @Override
    public Health health() {
        try {
            boolean isHealthy = databaseHealthChecker.check();
            if (isHealthy) {
                return Health.up()
                    .withDetail("database", "Available")
                    .build();
            } else {
                return Health.down()
                    .withDetail("database", "Unavailable")
                    .build();
            }
        } catch (Exception e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

### 2. 链路追踪
```java
@Component
public class TracingInterceptor {

    @Autowired
    private Tracer tracer;

    @Around("@annotation(org.apache.dubbo.config.annotation.DubboReference)")
    public Object traceDubboCall(ProceedingJoinPoint joinPoint) throws Throwable {
        Span span = tracer.nextSpan()
            .name("dubbo-call")
            .tag("service", joinPoint.getSignature().getName())
            .start();

        try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
            return joinPoint.proceed();
        } finally {
            span.end();
        }
    }
}
```

## 📋 架构审查检查清单

### 1. 服务设计
- [ ] 服务边界清晰，遵循单一职责原则
- [ ] 接口设计合理，版本管理完善
- [ ] 数据一致性策略明确
- [ ] 错误处理和降级方案完整

### 2. 技术选型
- [ ] 框架版本兼容性良好
- [ ] 第三方依赖管理规范
- [ ] 性能指标满足业务需求
- [ ] 安全策略实施到位

### 3. 可扩展性
- [ ] 支持水平扩展
- [ ] 数据库分片策略合理
- [ ] 缓存策略有效
- [ ] 消息队列设计适当

### 4. 运维支持
- [ ] 监控指标完善
- [ ] 日志记录规范
- [ ] 配置管理集中化
- [ ] 部署流程自动化

---

## [OK] 遵循本架构原则

遵循本架构原则将确保：

1. **业务价值最大化** - 技术架构支撑业务发展
2. **系统可维护性** - 清晰的服务边界和接口定义
3. **技术先进性** - 采用成熟可靠的技术栈
4. **团队协作效率** - 统一的架构标准和规范
5. **长期演进能力** - 支持业务的持续发展和技术升级

请架构师和开发团队严格遵循本原则，并在项目设计和实施过程中作为重要指导。