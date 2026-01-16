# Dubbo 配置指南

## [ROCKET] Apache Dubbo 3.2.14 企业级配置指南

本指南详细介绍如何在 Spring Boot 2.7 + Dubbo 3 环境中配置和使用 Dubbo 微服务框架，涵盖服务注册发现、负载均衡、容错机制、监控治理等核心功能。

## 📋 配置概览

### ai-coding-java 中的 Dubbo 集成特性
- **[AI] AI 驱动配置** - 智能推荐最优配置组合
- **[FAST] 开箱即用** - 预配置的企业级模板
- **[TOOL] 完整治理** - 服务治理、监控、熔断全集成
- **[CHART] 多协议支持** - Dubbo、HTTP、gRPC 协议支持
- **[ROCKET] 生产就绪** - 经过大规模生产环境验证的配置

## [ARCHITECTURE] 基础配置架构

### 1. 项目依赖配置

#### Maven 依赖
```xml
<dependencies>
    <!-- Dubbo 核心依赖 -->
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-spring-boot-starter</artifactId>
        <version>3.2.14</version>
    </dependency>

    <!-- 注册中心依赖 -->
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-registry-nacos</artifactId>
        <version>3.2.14</version>
    </dependency>

    <!-- 配置中心依赖 -->
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-configcenter-nacos</artifactId>
        <version>3.2.14</version>
    </dependency>

    <!-- 元数据中心依赖 -->
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-metadata-store-nacos</artifactId>
        <version>3.2.14</version>
    </dependency>

    <!-- 监控依赖 -->
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-monitor-prometheus</artifactId>
        <version>3.2.14</version>
    </dependency>

    <!-- API 网关依赖 -->
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-spring-boot-web</artifactId>
        <version>3.2.14</version>
    </dependency>
</dependencies>
```

#### 构建插件配置
```xml
<build>
    <plugins>
        <!-- Dubbo 代码生成插件 -->
        <plugin>
            <groupId>org.apache.dubbo</groupId>
            <artifactId>dubbo-maven-plugin</artifactId>
            <version>3.2.14</version>
            <executions>
                <execution>
                    <id>dubbo-compile</id>
                    <goals>
                        <goal>compile</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### 2. 应用配置文件结构
```
src/main/resources/
├── application.yml              # 主配置文件
├── application-dev.yml          # 开发环境配置
├── application-test.yml         # 测试环境配置
├── application-prod.yml         # 生产环境配置
├── dubbo-consumer.yml           # 消费者配置
├── dubbo-provider.yml           # 提供者配置
└── dubbo-admin.yml              # 管理配置
```

## ⚙️ 核心配置详解

### 1. 主应用配置 (application.yml)
```yaml
# 基础 Spring Boot 配置
server:
  port: 8080
  servlet:
    context-path: /api

spring:
  application:
    name: user-service
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

# Dubbo 基础配置
dubbo:
  application:
    name: ${spring.application.name}
    version: ${DUBBO_APPLICATION_VERSION:1.0.0}
    owner: ${DUBBO_APPLICATION_OWNER:yourcompany}
    organization: ${DUBBO_APPLICATION_ORGANIZATION:yourproject}
    logger: slf4j
    qos-enable: ${DUBBO_QOS_ENABLE:true}
    qos-accept-foreign-ip: ${DUBBO_QOS_ACCEPT_FOREIGN_IP:false}
    qos-host: ${DUBBO_QOS_HOST:localhost}
    qos-port: ${DUBBO_QOS_PORT:22222}
```

### 2. 协议配置
```yaml
dubbo:
  protocol:
    name: ${DUBBO_PROTOCOL_NAME:dubbo}
    port: ${DUBBO_PROTOCOL_PORT:20880}
    host: ${DUBBO_PROTOCOL_HOST:0.0.0.0}
    threads: ${DUBBO_PROTOCOL_THREADS:200}
    heartbeat: ${DUBBO_PROTOCOL_HEARTBEAT:60000}
    accesslog: ${DUBBO_PROTOCOL_ACCESSLOG:true}
    transporter: ${DUBBO_PROTOCOL_TRANSPORTER:netty}
    serialization: ${DUBBO_PROTOCOL_SERIALIZATION:hessian2}
    compressor: ${DUBBO_PROTOCOL_COMPRESSOR:zlib}

  # 多协议配置
  protocols:
    # Dubbo 协议配置
    dubbo:
      name: dubbo
      port: 20880
      serialization: hessian2
      optimizer: com.yourcompany.dubbo.SerializationOptimizerImpl

    # HTTP 协议配置
    http:
      name: http
      port: 8081
      server: netty

    # gRPC 协议配置
    grpc:
      name: grpc
      port: 50051
```

### 3. 注册中心配置
```yaml
dubbo:
  registry:
    # 主注册中心配置
    address: ${DUBBO_REGISTRY_ADDRESS:nacos://localhost:8848}
    protocol: ${DUBBO_REGISTRY_PROTOCOL:dubbo}
    timeout: ${DUBBO_REGISTRY_TIMEOUT:5000}
    session: ${DUBBO_REGISTRY_SESSION:60000}
    file: ${DUBBO_REGISTRY_FILE:./dubbo-registry-${spring.application.name}.cache}
    check: ${DUBBO_REGISTRY_CHECK:true}
    register: ${DUBBO_REGISTRY_REGISTER:true}
    subscribe: ${DUBBO_REGISTRY_SUBSCRIBE:true}
    group: ${DUBBO_REGISTRY_GROUP:DEFAULT_GROUP}

    # 多注册中心配置
    registries:
      # 主注册中心
      primary:
        address: nacos://nacos-primary:8848
        group: primary-group
        preferred: true

      # 备用注册中心
      backup:
        address: nacos://nacos-backup:8848
        group: backup-group
        preferred: false
```

### 4. 消费者配置 (dubbo-consumer.yml)
```yaml
dubbo:
  consumer:
    # 基础消费者配置
    check: ${DUBBO_CONSUMER_CHECK:false}
    timeout: ${DUBBO_CONSUMER_TIMEOUT:30000}
    retries: ${DUBBO_CONSUMER_RETRIES:2}
    lazy: ${DUBBO_CONSUMER_LAZY:false}
    sticky: ${DUBBO_CONSUMER_STICKY:true}
    init: ${DUBBO_CONSUMER_INIT:true}

    # 负载均衡配置
    loadbalance: ${DUBBO_CONSUMER_LOADBALANCE:roundrobin}

    # 集群容错配置
    cluster: ${DUBBO_CONSUMER_CLUSTER:failover}

    # 线程池配置
    actives: ${DUBBO_CONSUMER_ACTIVES:0}
    executes: ${DUBBO_CONSUMER_EXECUTES:0}

    # 连接配置
    connections: ${DUBBO_CONSUMER_CONNECTIONS:0}
    connect.timeout: ${DUBBO_CONSUMER_CONNECT_TIMEOUT:10000}

    # 缓存配置
    cache: ${DUBBO_CONSUMER_CACHE:lru}

    # 验证配置
    validation: ${DUBBO_CONSUMER_VALIDATION:true}

    # 版本和组配置
    version: ${DUBBO_CONSUMER_VERSION:*}
    group: ${DUBBO_CONSUMER_GROUP:*}

  # 服务引用配置
  reference:
    # 用户服务引用
    userService:
      interface: com.yourcompany.service.UserService
      version: 1.0.0
      group: user-group
      timeout: 15000
      retries: 3
      loadbalance: consistenthash

    # 订单服务引用
    orderService:
      interface: com.yourcompany.service.OrderService
      version: 1.0.0
      group: order-group
      timeout: 20000
      retries: 2
      loadbalance: leastactive
```

### 5. 提供者配置 (dubbo-provider.yml)
```yaml
dubbo:
  provider:
    # 基础提供者配置
    timeout: ${DUBBO_PROVIDER_TIMEOUT:30000}
    retries: ${DUBBO_PROVIDER_RETRIES:0}
    delay: ${DUBBO_PROVIDER_DELAY:0}
    version: ${DUBBO_PROVIDER_VERSION:1.0.0}
    group: ${DUBBO_PROVIDER_GROUP:default-group}

    # 权重配置
    weight: ${DUBBO_PROVIDER_WEIGHT:100}

    # 预热配置
    warmup: ${DUBBO_PROVIDER_WARMUP:100}
    warmup-weight: ${DUBBO_PROVIDER_WARMUP_WEIGHT:100}

    # 线程池配置
    threadpool: ${DUBBO_PROVIDER_THREADPOOL:cached}
    threads: ${DUBBO_PROVIDER_THREADS:200}
    iothreads: ${DUBBI_PROVIDER_IOTHREADS:2}
    queues: ${DUBBO_PROVIDER_QUEUES:0}
    accepts: ${DUBBO_PROVIDER_ACCEPTS:0}

    # 连接配置
    connections: ${DUBBO_PROVIDER_CONNECTIONS:0}

    # 验证配置
    validation: ${DUBBO_PROVIDER_VALIDATION:true}

    # 缓存配置
    cache: ${DUBBO_PROVIDER_CACHE:lru}

    # 令牌桶配置
    executes: ${DUBBO_PROVIDER_EXECUTES:0}
    actives: ${DUBBO_PROVIDER_ACTIVES:0}

    # 降级配置
    mock: ${DUBBO_PROVIDER_MOCK:false}

    # 动态配置
    dynamic: ${DUBBO_PROVIDER_DYNAMIC:true}

  # 服务发布配置
  service:
    # 用户服务
    userService:
      interface: com.yourcompany.service.UserService
      version: 1.0.0
      group: user-group
      ref: userServiceImpl
      timeout: 15000
      retries: 0
      weight: 100

    # 订单服务
    orderService:
      interface: com.yourcompany.service.OrderService
      version: 1.0.0
      group: order-group
      ref: orderServiceImpl
      timeout: 20000
      retries: 0
      weight: 100
```

## [TOOL] 高级配置特性

### 1. 负载均衡策略
```java
@Configuration
public class DubboLoadBalanceConfig {

    // 自定义负载均衡策略
    @Bean("customLoadBalance")
    public LoadBalance customLoadBalance() {
        return new CustomLoadBalance();
    }
}

public class CustomLoadBalance extends AbstractLoadBalance {

    @Override
    protected <T> Invoker<T> doSelect(List<Invoker<T>> invokers, URL url, Invocation invocation) {
        // 自定义负载均衡逻辑
        // 例如：基于用户ID的一致性哈希
        String userId = invocation.getAttachment("userId");
        if (userId != null) {
            int hash = userId.hashCode();
            int index = Math.abs(hash % invokers.size());
            return invokers.get(index);
        }

        // 默认随机选择
        return invokers.get(ThreadLocalRandom.current().nextInt(invokers.size()));
    }
}
```

### 2. 集群容错策略
```java
@Configuration
public class DubboClusterConfig {

    // 自定义集群策略
    @Bean("customCluster")
    public Cluster customCluster() {
        return new CustomCluster();
    }
}

public class CustomCluster extends FailoverCluster {

    @Override
    public <T> Invoker<T> join(Directory<T> directory) throws RpcException {
        return new AbstractClusterInvoker<T>(directory) {
            @Override
            protected Result doInvoke(Invocation invocation, List<Invoker<T>> invokers, LoadBalance loadbalance) throws RpcException {
                // 自定义容错逻辑
                checkInvokers(invokers, invocation);
                checkDestroy();

                // 自定义重试逻辑
                RpcException exception = null;
                for (int i = 0; i < invokers.size(); i++) {
                    Invoker<T> invoker = invokers.get(i);
                    try {
                        Result result = invoker.invoke(invocation);
                        if (exception != null) {
                            // 记录部分成功的情况
                            log.warn("部分服务调用成功，之前的错误: {}", exception.getMessage());
                        }
                        return result;
                    } catch (RpcException e) {
                        exception = e;
                        log.warn("服务调用失败: {}, 尝试下一个实例", e.getMessage());
                    }
                }

                throw exception != null ? exception : new RpcException("所有服务实例都调用失败");
            }
        };
    }
}
```

### 3. 过滤器配置
```java
// 自定义过滤器
@Activate(group = {Constants.PROVIDER, Constants.CONSUMER})
public class CustomFilter implements Filter {

    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
        long startTime = System.currentTimeMillis();

        try {
            // 前置处理
            beforeInvoke(invoker, invocation);

            // 执行调用
            Result result = invoker.invoke(invocation);

            // 后置处理
            afterInvoke(invoker, invocation, result, startTime);

            return result;
        } catch (Exception e) {
            // 异常处理
            onException(invoker, invocation, e, startTime);
            throw e;
        }
    }

    private void beforeInvoke(Invoker<?> invoker, Invocation invocation) {
        // 记录调用开始
        log.info("开始调用服务: {}.{}",
                invoker.getInterface().getSimpleName(),
                invocation.getMethodName());

        // 链路追踪
        Span span = tracer.nextSpan()
                .name("dubbo-call")
                .tag("service", invoker.getInterface().getSimpleName())
                .tag("method", invocation.getMethodName())
                .start();

        // 将 span 信息存入 attachment
        invocation.getAttachment().put("traceId", span.context().traceId());
    }

    private void afterInvoke(Invoker<?> invoker, Invocation invocation, Result result, long startTime) {
        long duration = System.currentTimeMillis() - startTime;

        log.info("服务调用完成: {}.{}, 耗时: {}ms",
                invoker.getInterface().getSimpleName(),
                invocation.getMethodName(),
                duration);

        // 记录指标
        meterRegistry.timer("dubbo.call.duration")
                .tags("service", invoker.getInterface().getSimpleName())
                .tags("method", invocation.getMethodName())
                .record(duration, TimeUnit.MILLISECONDS);
    }
}
```

### 4. 序列化配置
```java
@Configuration
public class DubboSerializationConfig {

    @Bean
    public SerializationOptimizer serializationOptimizer() {
        return new SerializationOptimizerImpl();
    }
}

public class SerializationOptimizerImpl implements SerializationOptimizer {

    @Override
    public Collection<Class<?>> getSerializableClasses() {
        List<Class<?>> classes = new LinkedList<>();

        // 添加需要序列化的类
        classes.add(com.yourcompany.dto.UserDTO.class);
        classes.add(com.yourcompany.dto.OrderDTO.class);
        classes.add(com.yourcompany.dto.PaymentDTO.class);

        return classes;
    }
}

// 自定义序列化实现
public class CustomSerialization implements Serialization {

    @Override
    public void serialize(Output output, Object obj) throws IOException {
        // 自定义序列化逻辑
        if (obj instanceof CustomObject) {
            CustomObject customObj = (CustomObject) obj;
            output.writeUTF(customObj.getId());
            output.writeUTF(customObj.getName());
            output.writeLong(customObj.getTimestamp());
        }
    }

    @Override
    public Object deserialize(Input input) throws IOException, ClassNotFoundException {
        // 自定义反序列化逻辑
        String id = input.readUTF();
        String name = input.readUTF();
        long timestamp = input.readLong();

        return new CustomObject(id, name, timestamp);
    }
}
```

## [CHART] 监控和治理

### 1. 监控配置
```yaml
dubbo:
  # 监控配置
  monitor:
    protocol: ${DUBBO_MONITOR_PROTOCOL:prometheus}
    address: ${DUBBO_MONITOR_ADDRESS:prometheus:9090}

  # 指标收集配置
  metrics:
    protocol: ${DUBBO_METRICS_PROTOCOL:prometheus}
    enabled: ${DUBBO_METRICS_ENABLED:true}
    export:
      prometheus:
        enabled: true
        step: 30s

  # 链路追踪配置
  tracing:
    enabled: ${DUBBO_TRACING_ENABLED:true}
    sampling:
      probability: ${DUBBO_TRACING_SAMPLING_PROBABILITY:0.1}
    propagation:
      type: ${DUBBO_TRACING_PROPAGATION_TYPE:b3}
```

### 2. 限流配置
```java
@Configuration
public class DubboRateLimitConfig {

    @Bean
    public RateLimiter dubboRateLimiter() {
        // 基于令牌桶的限流器
        return RateLimiter.create(1000); // 每秒1000个请求
    }

    // 限流过滤器
    @Component
    public static class RateLimitFilter implements Filter {

        @Autowired
        private RateLimiter rateLimiter;

        @Override
        public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
            if (!rateLimiter.tryAcquire()) {
                // 限流，返回限流响应
                return new RpcResult(RpcResult.ResultCode.RATE_LIMIT_EXCEEDED, "服务限流");
            }

            return invoker.invoke(invocation);
        }
    }
}
```

### 3. 熔断配置
```java
@Configuration
public class DubboCircuitBreakerConfig {

    @Bean
    public CircuitBreaker dubboCircuitBreaker() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
                .failureRateThreshold(50)  // 失败率阈值50%
                .waitDurationInOpenState(Duration.ofSeconds(30))  // 熔断器打开30秒
                .ringBufferSizeInHalfOpenState(10)  // 半开状态环状缓冲区大小
                .ringBufferSizeInClosedState(100)  // 关闭状态环状缓冲区大小
                .build();

        return CircuitBreaker.of("dubbo-service", config);
    }
}
```

## [ROCKET] 环境配置模板

### 1. 开发环境配置 (application-dev.yml)
```yaml
dubbo:
  registry:
    address: nacos://localhost:8848
    group: dev-group

  protocol:
    port: 20880

  provider:
    timeout: 60000
    threads: 50

  consumer:
    timeout: 60000
    retries: 3
    check: false

  # 开发环境特定配置
  config-center:
    address: nacos://localhost:8848
    namespace: dev
    group: dubbo-config

  # 调试配置
  qos-enable: true
  qos-accept-foreign-ip: true
```

### 2. 测试环境配置 (application-test.yml)
```yaml
dubbo:
  registry:
    address: nacos://test-nacos:8848
    group: test-group

  protocol:
    port: 20881

  provider:
    timeout: 30000
    threads: 100

  consumer:
    timeout: 30000
    retries: 2
    check: true

  # 测试环境特定配置
  config-center:
    address: nacos://test-nacos:8848
    namespace: test
    group: dubbo-config

  # 监控配置
  monitor:
    protocol: prometheus
    address: prometheus-test:9090
```

### 3. 生产环境配置 (application-prod.yml)
```yaml
dubbo:
  registry:
    address: nacos://${NACOS_HOST:nacos-cluster}:8848
    group: prod-group

  protocol:
    port: ${DUBBO_PROTOCOL_PORT:20880}

  provider:
    timeout: 15000
    threads: 200
    weight: 100

  consumer:
    timeout: 15000
    retries: 2
    check: true

  # 生产环境特定配置
  config-center:
    address: nacos://${NACOS_HOST:nacos-cluster}:8848
    namespace: prod
    group: dubbo-config

  # 安全配置
  qos-enable: false
  qos-accept-foreign-ip: false

  # 高可用配置
  cluster:
    failover:
      retries: 3
      availablecheck: true

  # 性能优化配置
  threadpool:
    type: cached
    core: 20
    max: 200
    queue: 2000
```

## [SEARCH] 故障排查指南

### 1. 常见问题诊断

#### 服务注册失败
```java
@Component
@Slf4j
public class DubboHealthChecker {

    @Scheduled(fixedRate = 30000)
    public void checkServiceRegistration() {
        try {
            // 检查注册中心连接
            Registry registry = getRegistry();
            if (registry != null) {
                boolean isRegistered = registry.isRegistered();
                log.info("服务注册状态: {}", isRegistered ? "已注册" : "未注册");
            }
        } catch (Exception e) {
            log.error("检查服务注册状态失败", e);
            // 发送告警
            alertService.sendAlert("Dubbo服务注册异常", e);
        }
    }
}
```

#### 调用超时问题
```java
@Component
public class DubboCallMonitor {

    private final MeterRegistry meterRegistry;
    private final Timer callTimer;

    public DubboCallMonitor(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.callTimer = Timer.builder("dubbo.call.duration")
                .description("Dubbo call duration")
                .register(meterRegistry);
    }

    @EventListener
    public void onCallCompleted(DubboCallCompletedEvent event) {
        callTimer.record(event.getDuration(), TimeUnit.MILLISECONDS);

        if (event.getDuration() > 1000) { // 超过1秒记录警告
            log.warn("Dubbo调用耗时过长: {}.{} 耗时: {}ms",
                    event.getServiceInterface(),
                    event.getMethodName(),
                    event.getDuration());
        }
    }
}
```

### 2. 性能调优建议

#### JVM 参数优化
```bash
# 生产环境 JVM 参数建议
-Xms2g -Xmx2g
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/dubbo/
-Ddubbo.application.logger=slf4j
-Ddubbo.protocol.name=dubbo
```

#### 线程池调优
```yaml
dubbo:
  provider:
    # 根据业务场景调整线程池大小
    threads: ${DUBBO_PROVIDER_THREADS:200}
    iothreads: ${DUBBO_PROVIDER_IOTHREADS:4}
    # 使用固定大小线程池
    threadpool: fixed
    # 设置队列大小
    queues: ${DUBBO_PROVIDER_QUEUES:1000}
    # 最大并发数
    executes: ${DUBBO_PROVIDER_EXECUTES:5000}
```

### 3. 安全配置
```yaml
dubbo:
  # 访问控制配置
  accesslog: true

  # IP 白名单配置
  accept: ${DUBBO_ACCEPT:0.0.0.0}

  # 令牌配置
  token: ${DUBBO_TOKEN:your-secret-token}

  # SSL 配置
  ssl:
    enabled: ${DUBBO_SSL_ENABLED:false}
    keystore: ${DUBBO_SSL_KEYSTORE:/path/to/keystore}
    keystorePassword: ${DUBBO_SSL_KEYSTORE_PASSWORD:password}
```

## 📋 配置检查清单

### 1. 基础配置检查
- [ ] 应用名称和版本配置正确
- [ ] 协议端口配置合适且无冲突
- [ ] 注册中心地址和分组配置正确
- [ ] 超时时间和重试次数合理设置

### 2. 高可用配置检查
- [ ] 多注册中心配置
- [ ] 集群容错策略配置
- [ ] 负载均衡策略选择合适
- [ ] 熔断和限流机制配置

### 3. 监控配置检查
- [ ] 监控协议和地址配置
- [ ] 链路追踪配置
- [ ] 指标收集配置
- [ ] 健康检查配置

### 4. 安全配置检查
- [ ] 访问控制配置
- [ ] 令牌验证配置
- [ ] SSL/TLS 配置
- [ ] IP 白名单配置

### 5. 性能配置检查
- [ ] 线程池大小配置
- [ ] 序列化配置
- [ ] 连接数配置
- [ ] 缓存配置

---

## [OK] 配置最佳实践总结

通过本指南，您已经掌握了企业级 Dubbo 3.2.14 配置的完整知识：

### [TARGET] 核心配置要素
1. **服务注册发现** - 多注册中心配置，高可用保障
2. **协议配置** - 多协议支持，性能优化
3. **负载均衡** - 智能负载，容错机制
4. **监控治理** - 全链路监控，性能指标
5. **安全防护** - 访问控制，加密传输

### [ROCKET] 配置优化建议
1. **环境差异化** - 开发、测试、生产环境分离
2. **动态配置** - 支持运行时配置变更
3. **性能调优** - 线程池、序列化、连接优化
4. **故障预防** - 熔断、限流、降级配置
5. **监控完善** - 指标、日志、链路追踪

**ai-coding-java 插件将为您提供 AI 驱动的 Dubbo 配置建议，确保配置最优、性能最佳！**