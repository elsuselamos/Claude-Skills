# 微服务开发指南

## [ARCHITECTURE] Spring Boot 2.7 + Dubbo 3 企业级微服务开发指南

本指南详细介绍如何使用 ai-coding-java 插件进行企业级微服务开发，涵盖微服务设计、实现、测试和部署的完整生命周期。

## [TARGET] 微服务开发概述

### 什么是微服务架构
微服务架构是一种将应用程序构建为一组小型、独立服务的方法，每个服务都运行在自己的进程中，通过轻量级通信机制进行交互。

### ai-coding-java 微服务特性
- **[AI] AI 驱动开发** - 智能代码生成和优化建议
- **[FAST] 快速启动** - 5分钟创建生产就绪的微服务
- **[TOOL] 企业级配置** - 开箱即用的 Spring Boot 2.7 + Dubbo 3 集成
- **[CHART] 质量保证** - 内置代码审查和架构分析
- **[ROCKET] 一键部署** - 支持 Docker 和 Kubernetes 部署

## [ROCKET] 快速创建微服务

### 1. 使用 AI 实现命令创建微服务

```bash
# 基础微服务创建
/ai-coding-java:implement --type=microservice --name=user-service --module=user-management

# 复杂微服务创建（包含完整业务功能）
/ai-coding-java:implement 创建订单服务，包含订单管理、支付集成、库存管理和通知功能
```

### 2. 手动微服务创建步骤

#### 2.1 项目初始化
```bash
# 创建微服务项目结构
mkdir order-service && cd order-service

# 使用 ai-coding-java 项目注入
/ai-coding-java:project-inject

# 创建标准的 Maven 项目结构
```

#### 2.2 核心配置文件设置
```yaml
# application.yml
server:
  port: 8082
  servlet:
    context-path: /order-service

spring:
  application:
    name: order-service
  profiles:
    active: dev

# Dubbo 配置
dubbo:
  application:
    name: order-service
    version: 1.0.0
  protocol:
    name: dubbo
    port: 20882
  registry:
    address: nacos://localhost:8848
```

## 🏛️ 微服务架构设计

### 1. 服务边界划分

#### 单一职责原则
```java
// [OK] 正确 - 每个服务专注于单一业务领域
@Service
public class OrderService {
    // 专注于订单相关业务逻辑
    public Order createOrder(CreateOrderRequest request) {}
    public Order updateOrderStatus(Long orderId, OrderStatus status) {}
    public List<Order> findOrdersByUser(Long userId) {}
}

@Service
public class PaymentService {
    // 专注于支付相关业务逻辑
    public PaymentResult processPayment(PaymentRequest request) {}
    public RefundResult processRefund(RefundRequest request) {}
}

// [X] 错误 - 服务职责混合
@Service
public class OrderAndPaymentService {
    // 既处理订单逻辑又处理支付逻辑，违反单一职责原则
}
```

#### 领域驱动设计
```java
// 订单聚合根
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "order_number", unique = true, nullable = false)
    private String orderNumber;

    @Column(name = "user_id", nullable = false)
    private Long userId;

    @Column(name = "total_amount", nullable = false)
    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private OrderStatus status;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<OrderItem> items;

    // 领域方法
    public void addItem(OrderItem item) {
        items.add(item);
        recalculateTotal();
    }

    public void markAsPaid() {
        if (status != OrderStatus.PENDING) {
            throw new OrderStateException("只有待支付状态的订单才能标记为已支付");
        }
        status = OrderStatus.PAID;
    }

    private void recalculateTotal() {
        totalAmount = items.stream()
            .map(OrderItem::getTotalPrice)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}

// 订单项实体
@Entity
@Table(name = "order_items")
public class OrderItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @Column(name = "product_id", nullable = false)
    private Long productId;

    @Column(name = "quantity", nullable = false)
    private Integer quantity;

    @Column(name = "unit_price", nullable = false)
    private BigDecimal unitPrice;

    public BigDecimal getTotalPrice() {
        return unitPrice.multiply(new BigDecimal(quantity));
    }
}
```

### 2. 服务间通信设计

#### Dubbo 服务接口定义
```java
// 订单服务接口
@DubboService(version = "1.0.0", timeout = 5000)
public interface OrderService {

    /**
     * 创建订单
     * @param request 创建订单请求
     * @return 订单响应
     * @throws BusinessException 业务异常
     */
    OrderResponse createOrder(CreateOrderRequest request) throws BusinessException;

    /**
     * 根据ID获取订单
     * @param orderId 订单ID
     * @return 订单响应，不存在时返回null
     */
    OrderResponse getOrderById(Long orderId);

    /**
     * 更新订单状态
     * @param orderId 订单ID
     * @param status 新状态
     * @return 是否更新成功
     */
    boolean updateOrderStatus(Long orderId, OrderStatus status);

    /**
     * 根据用户ID查询订单列表
     * @param userId 用户ID
     * @param pageable 分页参数
     * @return 订单列表
     */
    Page<OrderResponse> findOrdersByUserId(Long userId, Pageable pageable);
}
```

#### 服务实现
```java
@Service
@DubboService(version = "1.0.0", timeout = 5000, retries = 2)
@Transactional
public class OrderServiceImpl implements OrderService {

    private final OrderRepository orderRepository;
    private final OrderItemRepository orderItemRepository;
    private final IdGeneratorService idGeneratorService;
    private final InventoryService inventoryService;
    private final PaymentService paymentService;

    @Override
    public OrderResponse createOrder(CreateOrderRequest request) {
        // 1. 参数验证
        validateCreateOrderRequest(request);

        // 2. 生成订单号
        String orderNumber = generateOrderNumber();

        // 3. 检查库存
        checkInventoryAvailability(request.getItems());

        // 4. 创建订单
        Order order = buildOrder(request, orderNumber);
        order = orderRepository.save(order);

        // 5. 创建订单项
        List<OrderItem> orderItems = createOrderItems(order.getId(), request.getItems());
        orderItemRepository.saveAll(orderItems);

        // 6. 预留库存
        reserveInventory(order);

        // 7. 创建支付记录
        createPaymentRecord(order);

        return convertToResponse(order, orderItems);
    }

    @Override
    public OrderResponse getOrderById(Long orderId) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        List<OrderItem> items = orderItemRepository.findByOrderId(orderId);

        return convertToResponse(order, items);
    }

    private void validateCreateOrderRequest(CreateOrderRequest request) {
        if (request.getUserId() == null) {
            throw new ValidationException("用户ID不能为空");
        }

        if (request.getItems() == null || request.getItems().isEmpty()) {
            throw new ValidationException("订单项不能为空");
        }

        request.getItems().forEach(this::validateOrderItem);
    }

    private void checkInventoryAvailability(List<OrderItemRequest> items) {
        Map<Long, Integer> productQuantities = items.stream()
            .collect(Collectors.toMap(
                OrderItemRequest::getProductId,
                OrderItemRequest::getQuantity,
                Integer::sum
            ));

        InventoryCheckResult result = inventoryService.checkAvailability(
            new InventoryCheckRequest(productQuantities)
        );

        if (!result.isAvailable()) {
            throw new InventoryNotAvailableException(result.getUnavailableProducts());
        }
    }
}
```

## 🔄 数据一致性处理

### 1. Saga 模式实现

#### Saga 协调器
```java
@Component
public class OrderSagaOrchestrator {

    @Autowired
    private SagaManager sagaManager;

    public void executeOrderCreationSaga(CreateOrderRequest request) {
        OrderSagaData sagaData = new OrderSagaData();
        sagaData.setOriginalRequest(request);

        // 定义 Saga 步骤
        SagaDefinition<OrderSagaData> sagaDefinition = SagaDefinition
            .<OrderSagaData>create()
            // 步骤1：创建订单
            .step("createOrder")
                .invoke(this::createOrderStep)
                .compensate(this::cancelOrderStep)
            // 步骤2：预留库存
            .step("reserveInventory")
                .invoke(this::reserveInventoryStep)
                .compensate(this::releaseInventoryStep)
            // 步骤3：处理支付
            .step("processPayment")
                .invoke(this::processPaymentStep)
                .compensate(this::refundPaymentStep)
            // 步骤4：发送通知
            .step("sendNotification")
                .invoke(this::sendNotificationStep)
                .build();

        // 执行 Saga
        sagaManager.execute(sagaDefinition, sagaData);
    }

    private OrderSagaData createOrderStep(OrderSagaData data) {
        // 创建订单逻辑
        Order order = orderService.createOrderWithoutInventoryCheck(data.getOriginalRequest());
        data.setOrder(order);
        return data;
    }

    private OrderSagaData cancelOrderStep(OrderSagaData data) {
        // 取消订单补偿逻辑
        if (data.getOrder() != null) {
            orderService.cancelOrder(data.getOrder().getId());
        }
        return data;
    }

    private OrderSagaData reserveInventoryStep(OrderSagaData data) {
        // 预留库存逻辑
        inventoryService.reserveInventory(buildInventoryRequest(data));
        data.setInventoryReserved(true);
        return data;
    }

    private OrderSagaData releaseInventoryStep(OrderSagaData data) {
        // 释放库存补偿逻辑
        if (data.isInventoryReserved()) {
            inventoryService.releaseInventory(buildInventoryRequest(data));
        }
        return data;
    }
}
```

### 2. 事件驱动架构

#### 事件发布
```java
@Service
public class OrderEventPublisher {

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public void publishOrderCreatedEvent(Order order, List<OrderItem> items) {
        OrderCreatedEvent event = OrderCreatedEvent.builder()
            .orderId(order.getId())
            .orderNumber(order.getOrderNumber())
            .userId(order.getUserId())
            .totalAmount(order.getTotalAmount())
            .items(convertToItemEventList(items))
            .createdAt(Instant.now())
            .build();

        eventPublisher.publishEvent(event);
    }

    public void publishOrderStatusChangedEvent(Order order, OrderStatus oldStatus, OrderStatus newStatus) {
        OrderStatusChangedEvent event = OrderStatusChangedEvent.builder()
            .orderId(order.getId())
            .orderNumber(order.getOrderNumber())
            .userId(order.getUserId())
            .oldStatus(oldStatus)
            .newStatus(newStatus)
            .changedAt(Instant.now())
            .build();

        eventPublisher.publishEvent(event);
    }
}
```

#### 事件处理
```java
@Component
@Slf4j
public class OrderEventHandler {

    @Autowired
    private NotificationService notificationService;

    @Autowired
    private ReportService reportService;

    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        log.info("处理订单创建事件: orderId={}", event.getOrderId());

        try {
            // 发送订单确认邮件
            notificationService.sendOrderConfirmation(event);

            // 更新用户购买统计
            reportService.updateUserPurchaseStats(event.getUserId(), event.getTotalAmount());

        } catch (Exception e) {
            log.error("处理订单创建事件失败: orderId={}", event.getOrderId(), e);
            // 发送告警通知
            notificationService.sendErrorAlert("订单创建事件处理失败", e);
        }
    }

    @EventListener
    @Async
    public void handleOrderStatusChanged(OrderStatusChangedEvent event) {
        log.info("处理订单状态变更事件: orderId={}, {} -> {}",
                event.getOrderId(), event.getOldStatus(), event.getNewStatus());

        // 发送状态变更通知
        if (shouldSendNotification(event.getNewStatus())) {
            notificationService.sendStatusChangeNotification(event);
        }

        // 更新报表数据
        reportService.updateOrderStatusStats(event);
    }

    private boolean shouldSendNotification(OrderStatus status) {
        return status == OrderStatus.PAID ||
               status == OrderStatus.SHIPPED ||
               status == OrderStatus.DELIVERED ||
               status == OrderStatus.CANCELLED;
    }
}
```

## [TOOL] 微服务配置管理

### 1. 配置中心集成
```yaml
# bootstrap.yml
spring:
  application:
    name: order-service
  cloud:
    nacos:
      config:
        server-addr: ${NACOS_SERVER_URL:localhost:8848}
        namespace: ${NACOS_NAMESPACE:dev}
        group: ${NACOS_GROUP:DEFAULT_GROUP}
        file-extension: yaml
        refresh-enabled: true
      discovery:
        server-addr: ${NACOS_SERVER_URL:localhost:8848}
        namespace: ${NACOS_NAMESPACE:dev}
        group: ${NACOS_GROUP:DEFAULT_GROUP}
```

### 2. 动态配置刷新
```java
@Component
@RefreshScope
@ConfigurationProperties(prefix = "order.service")
@Data
public class OrderServiceConfig {

    private int maxOrderAmount = 50000;
    private Duration orderTimeout = Duration.ofMinutes(30);
    private boolean autoCancelEnabled = true;
    private Duration autoCancelDelay = Duration.ofHours(2);

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    @EventListener
    public void handleRefreshEvent(RefreshRemoteApplicationEvent event) {
        log.info("配置已刷新，新的配置: {}", this);

        // 发布配置变更事件
        eventPublisher.publishEvent(new ConfigRefreshedEvent(this));
    }
}
```

### 3. 环境配置管理
```java
@Component
public class EnvironmentConfigManager {

    @Value("${spring.profiles.active}")
    private String activeProfile;

    @Value("${order.service.timeout:30s}")
    private Duration defaultTimeout;

    @Value("${order.service.max-retry:3}")
    private int maxRetry;

    public boolean isProductionEnvironment() {
        return "prod".equalsIgnoreCase(activeProfile);
    }

    public boolean isDevelopmentEnvironment() {
        return "dev".equalsIgnoreCase(activeProfile);
    }

    public Duration getTimeout() {
        if (isProductionEnvironment()) {
            return defaultTimeout.multipliedBy(2); // 生产环境超时时间加倍
        }
        return defaultTimeout;
    }
}
```

## 🧪 微服务测试策略

### 1. 单元测试
```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private OrderItemRepository orderItemRepository;

    @Mock
    private InventoryService inventoryService;

    @Mock
    private PaymentService paymentService;

    @Mock
    private IdGeneratorService idGeneratorService;

    @InjectMocks
    private OrderServiceImpl orderService;

    @Test
    @DisplayName("创建订单成功")
    void shouldCreateOrderSuccessfully() {
        // Given
        CreateOrderRequest request = CreateOrderRequest.builder()
            .userId(123L)
            .items(Arrays.asList(
                OrderItemRequest.builder()
                    .productId(1L)
                    .quantity(2)
                    .unitPrice(new BigDecimal("100.00"))
                    .build()
            ))
            .build();

        Order savedOrder = Order.builder()
            .id(1L)
            .orderNumber("ORD20231207001")
            .userId(123L)
            .totalAmount(new BigDecimal("200.00"))
            .status(OrderStatus.PENDING)
            .build();

        when(idGeneratorService.generateOrderNumber()).thenReturn("ORD20231207001");
        when(orderRepository.save(any(Order.class))).thenReturn(savedOrder);
        when(inventoryService.checkAvailability(any())).thenReturn(
            InventoryCheckResult.builder().available(true).build()
        );

        // When
        OrderResponse response = orderService.createOrder(request);

        // Then
        assertThat(response.getOrderNumber()).isEqualTo("ORD20231207001");
        assertThat(response.getTotalAmount()).isEqualTo(new BigDecimal("200.00"));
        assertThat(response.getStatus()).isEqualTo(OrderStatus.PENDING);

        verify(orderRepository).save(any(Order.class));
        verify(inventoryService).checkAvailability(any());
    }

    @Test
    @DisplayName("库存不足时抛出异常")
    void shouldThrowExceptionWhenInventoryNotAvailable() {
        // Given
        CreateOrderRequest request = CreateOrderRequest.builder()
            .userId(123L)
            .items(Arrays.asList(
                OrderItemRequest.builder()
                    .productId(1L)
                    .quantity(10)
                    .unitPrice(new BigDecimal("100.00"))
                    .build()
            ))
            .build();

        when(inventoryService.checkAvailability(any())).thenReturn(
            InventoryCheckResult.builder()
                .available(false)
                .unavailableProducts(Collections.singletonMap(1L, 5))
                .build()
        );

        // When & Then
        assertThatThrownBy(() -> orderService.createOrder(request))
            .isInstanceOf(InventoryNotAvailableException.class)
            .hasMessageContaining("库存不足");
    }
}
```

### 2. 集成测试
```java
@SpringBootTest
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1",
    "spring.jpa.hibernate.ddl-auto=create-drop",
    "dubbo.registry.address=nacos://localhost:8848"
})
@Transactional
class OrderServiceIntegrationTest {

    @Autowired
    private OrderService orderService;

    @Autowired
    private TestDubboConsumerService testDubboConsumer;

    @Test
    @DisplayName("完整订单创建流程测试")
    void shouldCompleteOrderCreationFlow() {
        // Given
        CreateOrderRequest request = CreateOrderRequest.builder()
            .userId(1L)
            .items(Arrays.asList(
                OrderItemRequest.builder()
                    .productId(1L)
                    .quantity(2)
                    .unitPrice(new BigDecimal("100.00"))
                    .build()
            ))
            .build();

        // When
        OrderResponse response = orderService.createOrder(request);

        // Then
        assertThat(response.getId()).isNotNull();
        assertThat(response.getOrderNumber()).isNotBlank();
        assertThat(response.getStatus()).isEqualTo(OrderStatus.PENDING);

        // 验证数据库中的数据
        OrderResponse savedOrder = orderService.getOrderById(response.getId());
        assertThat(savedOrder.getOrderNumber()).isEqualTo(response.getOrderNumber());

        // 验证 Dubbo 服务调用
        OrderResponse dubboResponse = testDubboConsumer.getOrderById(response.getId());
        assertThat(dubboResponse.getOrderNumber()).isEqualTo(response.getOrderNumber());
    }
}
```

### 3. 端到端测试
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.profiles.active=test"
})
class OrderServiceE2ETest {

    @Autowired
    private TestRestTemplate restTemplate;

    @LocalServerPort
    private int port;

    @Test
    @DisplayName("完整API流程测试")
    void shouldCompleteApiFlow() {
        String baseUrl = "http://localhost:" + port + "/order-service";

        // 1. 创建订单
        CreateOrderRequest createRequest = CreateOrderRequest.builder()
            .userId(1L)
            .items(Arrays.asList(
                OrderItemRequest.builder()
                    .productId(1L)
                    .quantity(2)
                    .unitPrice(new BigDecimal("100.00"))
                    .build()
            ))
            .build();

        ResponseEntity<OrderResponse> createResponse = restTemplate.postForEntity(
            baseUrl + "/api/orders", createRequest, OrderResponse.class);

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        OrderResponse order = createResponse.getBody();
        assertThat(order).isNotNull();

        // 2. 查询订单
        ResponseEntity<OrderResponse> getResponse = restTemplate.getForEntity(
            baseUrl + "/api/orders/" + order.getId(), OrderResponse.class);

        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(getResponse.getBody().getOrderNumber()).isEqualTo(order.getOrderNumber());

        // 3. 更新订单状态
        UpdateOrderStatusRequest updateRequest = UpdateOrderStatusRequest.builder()
            .status(OrderStatus.PAID)
            .build();

        restTemplate.put(
            baseUrl + "/api/orders/" + order.getId() + "/status", updateRequest);

        // 4. 验证状态更新
        ResponseEntity<OrderResponse> updatedResponse = restTemplate.getForEntity(
            baseUrl + "/api/orders/" + order.getId(), OrderResponse.class);

        assertThat(updatedResponse.getBody().getStatus()).isEqualTo(OrderStatus.PAID);
    }
}
```

## [ROCKET] 微服务部署

### 1. Docker 部署
```dockerfile
# Dockerfile
FROM openjdk:11-jre-slim

LABEL maintainer="your-team@company.com"
LABEL version="1.0.0"
LABEL description="Order Service Microservice"

# 设置工作目录
WORKDIR /app

# 创建应用用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 复制应用文件
COPY target/order-service-*.jar app.jar

# 设置文件权限
RUN chown -R appuser:appuser /app

# 切换到应用用户
USER appuser

# 暴露端口
EXPOSE 8082 20882

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8082/order-service/actuator/health || exit 1

# 启动应用
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
```

### 2. Docker Compose 部署
```yaml
# docker-compose.yml
version: '3.8'

services:
  order-service:
    build: .
    ports:
      - "8082:8082"
      - "20882:20882"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - DB_HOST=mysql
      - REDIS_HOST=redis
      - NACOS_SERVER_URL=nacos:8848
    depends_on:
      - mysql
      - redis
      - nacos
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8082/order-service/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: order_service
      MYSQL_USER: orderuser
      MYSQL_PASSWORD: orderpass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nacos:
    image: nacos/nacos-server:v2.2.3
    environment:
      MODE: standalone
      SPRING_DATASOURCE_PLATFORM: mysql
      MYSQL_SERVICE_HOST: mysql
      MYSQL_SERVICE_DB_NAME: nacos
      MYSQL_SERVICE_USER: root
      MYSQL_SERVICE_PASSWORD: rootpassword
    ports:
      - "8848:8848"
    depends_on:
      - mysql
    restart: unless-stopped

volumes:
  mysql_data:
  redis_data:
```

### 3. Kubernetes 部署
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: microservices
  labels:
    app: order-service
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
        version: v1
    spec:
      containers:
      - name: order-service
        image: your-registry/order-service:1.0.0
        ports:
        - containerPort: 8082
          name: http
        - containerPort: 20882
          name: dubbo
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "k8s"
        - name: DB_HOST
          value: "mysql-service"
        - name: REDIS_HOST
          value: "redis-service"
        - name: NACOS_SERVER_URL
          value: "nacos-service:8848"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /order-service/actuator/health
            port: 8082
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /order-service/actuator/health
            port: 8082
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: microservices
spec:
  selector:
    app: order-service
  ports:
  - name: http
    port: 8082
    targetPort: 8082
  - name: dubbo
    port: 20882
    targetPort: 20882
  type: LoadBalancer
```

## [CHART] 微服务监控

### 1. 健康检查
```java
@Component
public class OrderServiceHealthIndicator implements HealthIndicator {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private InventoryService inventoryService;

    @Override
    public Health health() {
        try {
            // 检查数据库连接
            long orderCount = orderRepository.count();

            // 检查依赖服务
            boolean inventoryServiceHealthy = inventoryService.healthCheck();

            if (inventoryServiceHealthy) {
                return Health.up()
                    .withDetail("database", "Connected")
                    .withDetail("orderCount", orderCount)
                    .withDetail("inventoryService", "Available")
                    .build();
            } else {
                return Health.down()
                    .withDetail("database", "Connected")
                    .withDetail("inventoryService", "Unavailable")
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

### 2. 指标收集
```java
@Component
public class OrderServiceMetrics {

    private final MeterRegistry meterRegistry;
    private final Counter orderCreatedCounter;
    private final Timer orderProcessingTimer;
    private final Gauge activeOrdersGauge;

    public OrderServiceMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.orderCreatedCounter = Counter.builder("orders.created")
            .description("Total number of orders created")
            .register(meterRegistry);
        this.orderProcessingTimer = Timer.builder("orders.processing.time")
            .description("Order processing time")
            .register(meterRegistry);
        this.activeOrdersGauge = Gauge.builder("orders.active")
            .description("Number of active orders")
            .register(meterRegistry);
    }

    public void recordOrderCreated() {
        orderCreatedCounter.increment();
    }

    public Timer.Sample startOrderProcessing() {
        return Timer.start(meterRegistry);
    }

    public void recordOrderProcessingTime(Timer.Sample sample) {
        sample.stop(orderProcessingTimer);
    }

    public void updateActiveOrdersCount(int count) {
        activeOrdersGauge.set(count);
    }
}
```

## [TOOL] 常见问题解决

### 1. 服务发现失败
```java
@Component
@Slf4j
public class ServiceDiscoveryHealthCheck {

    @Scheduled(fixedRate = 30000) // 每30秒检查一次
    public void checkServiceDiscovery() {
        try {
            // 检查 Nacos 连接
            String nacosUrl = "http://localhost:8848/nacos/v1/console/health";
            RestTemplate restTemplate = new RestTemplate();
            ResponseEntity<String> response = restTemplate.getForEntity(nacosUrl, String.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                log.info("服务发现正常");
            } else {
                log.error("服务发现异常: {}", response.getStatusCode());
            }
        } catch (Exception e) {
            log.error("服务发现检查失败", e);
            // 发送告警
            alertService.sendAlert("服务发现连接失败", e);
        }
    }
}
```

### 2. 数据库连接问题
```java
@Component
public class DatabaseConnectionPoolMonitor {

    @Autowired
    private DataSource dataSource;

    @EventListener
    public void handleApplicationReady(ApplicationReadyEvent event) {
        try {
            HikariDataSource hikariDataSource = (HikariDataSource) dataSource;
            HikariPoolMXBean poolProxy = hikariDataSource.getHikariPoolMXBean();

            log.info("数据库连接池状态:");
            log.info("  - 活跃连接数: {}", poolProxy.getActiveConnections());
            log.info("  - 空闲连接数: {}", poolProxy.getIdleConnections());
            log.info("  - 总连接数: {}", poolProxy.getTotalConnections());
            log.info("  - 等待线程数: {}", poolProxy.getThreadsAwaitingConnection());

        } catch (Exception e) {
            log.error("获取数据库连接池状态失败", e);
        }
    }
}
```

## [LIBRARY] 进阶主题

### 1. API 版本管理
```java
@RestController
@RequestMapping("/api/v1")
public class OrderControllerV1 {
    // V1 版本API
}

@RestController
@RequestMapping("/api/v2")
public class OrderControllerV2 {
    // V2 版本API，向后兼容V1
}

@RestController
@RequestMapping("/api")
public class OrderController {

    @GetMapping("/orders")
    public ResponseEntity<?> getOrders(
            @RequestHeader(value = "API-Version", defaultValue = "v1") String version) {

        switch (version) {
            case "v1":
                return ResponseEntity.ok(orderServiceV1.getOrders());
            case "v2":
                return ResponseEntity.ok(orderServiceV2.getOrders());
            default:
                return ResponseEntity.badRequest().body("不支持的API版本: " + version);
        }
    }
}
```

### 2. 限流和熔断
```java
@Component
public class OrderServiceCircuitBreaker {

    @Autowired
    private InventoryService inventoryService;

    private final CircuitBreaker inventoryCircuitBreaker;

    public OrderServiceCircuitBreaker() {
        this.inventoryCircuitBreaker = CircuitBreaker.ofDefaults("inventoryService");

        // 配置熔断策略
        inventoryCircuitBreaker.getEventPublisher()
            .onStateTransition(event ->
                log.info("库存服务熔断状态变更: {} -> {}",
                        event.getStateTransition().getFromState(),
                        event.getStateTransition().getToState()));
    }

    public InventoryCheckResult checkInventoryWithCircuitBreaker(InventoryCheckRequest request) {
        Supplier<InventoryCheckResult> decoratedSupplier = CircuitBreaker
            .decorateSupplier(inventoryCircuitBreaker, () -> inventoryService.checkAvailability(request));

        try {
            return decoratedSupplier.get();
        } catch (CallNotPermittedException e) {
            log.warn("库存服务熔断，使用默认处理");
            return InventoryCheckResult.builder()
                .available(false)
                .fallbackReason("库存服务暂时不可用")
                .build();
        }
    }
}
```

---

## [OK] 微服务开发最佳实践总结

通过本指南，您已经掌握了使用 ai-coding-java 插件进行企业级微服务开发的完整流程：

### [TARGET] 关键成功要素
1. **清晰的服务边界** - 遵循单一职责原则和DDD设计
2. **完善的数据一致性** - 使用Saga模式和事件驱动架构
3. **可靠的通信机制** - 合理使用Dubbo同步和异步通信
4. **全面的测试策略** - 单元测试、集成测试、端到端测试
5. **完善的监控体系** - 健康检查、指标收集、日志管理

### [ROCKET] 下一步行动
1. **实践项目开发** - 使用指南创建实际微服务项目
2. **深入高级特性** - 学习API版本管理、限流熔断等
3. **性能优化** - 优化数据库查询、缓存策略
4. **运维部署** - 掌握容器化和Kubernetes部署

**ai-coding-java 插件将伴随您的微服务开发之旅，提供AI驱动的智能支持和最佳实践指导！**