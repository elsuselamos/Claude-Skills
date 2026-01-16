# Spring Boot 2.7 + Dubbo 3 最佳实践

本文档总结了企业级微服务开发的最佳实践，帮助您构建高质量、可维护的系统。

## Spring Boot 最佳实践

### 1. 应用分层

遵循标准的分层架构：

```
Controller 层 (接口层)
    ↓
Service 层 (业务逻辑层)
    ↓
Repository/Mapper 层 (数据访问层)
    ↓
数据库/缓存
```

**示例**:
```java
// Controller: 处理 HTTP 请求
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;

    @GetMapping("/{id}")
    public Result<User> getUser(@PathVariable Long id) {
        return Result.success(userService.findById(id));
    }
}

// Service: 业务逻辑
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserRepository userRepository;

    @Transactional
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}

// Repository: 数据访问
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}
```

### 2. 配置管理

**多环境配置**:
```yaml
# application.yml (基础配置)
spring:
  profiles:
    active: ${SPRING_PROFILE:dev}

# application-dev.yml (开发环境)
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/dev_db

# application-prod.yml (生产环境)
spring:
  datasource:
    url: jdbc:mysql://prod-db:3306/prod_db
```

**配置属性**:
```java
@ConfigurationProperties(prefix = "app")
@Data
public class AppProperties {
    private String name;
    private String version;
    private Cache cache = new Cache();

    @Data
    public static class Cache {
        private Duration ttl = Duration.ofMinutes(30);
    }
}
```

### 3. 异常处理

**全局异常处理**:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException e) {
        return ResponseEntity.badRequest()
            .body(ErrorResponse.of(e.getCode(), e.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception e) {
        log.error("Unexpected error", e);
        return ResponseEntity.status(500)
            .body(ErrorResponse.of("SYSTEM_ERROR", "系统错误"));
    }
}
```

### 4. 日志规范

**日志级别**:
```java
// TRACE: 最详细的调试信息
log.trace("Entry: {}, Exit: {}", param1, param2);

// DEBUG: 调试信息
log.debug("User created: {}", user.getId());

// INFO: 重要业务事件
log.info("Order processed: orderId={}, amount={}", orderId, amount);

// WARN: 警告信息
log.warn("Cache miss for key: {}", key);

// ERROR: 错误信息
log.error("Payment failed: orderId={}, error={}", orderId, error, error);
```

### 5. 依赖注入

**构造器注入（推荐）**:
```java
@Service
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }
}
```

## Dubbo 3 最佳实践

### 1. 服务接口设计

**清晰的服务契约**:
```java
// 服务接口定义在 xxpay-core 模块
public interface UserService {
    /**
     * 根据用户ID查询用户
     * @param userId 用户ID
     * @return 用户信息，不存在返回 null
     */
    User findById(Long userId);

    /**
     * 创建新用户
     * @param request 用户创建请求
     * @return 创建的用户信息
     * @throws BusinessException 用户名已存在时抛出
     */
    User createUser(CreateUserRequest request) throws BusinessException;
}
```

### 2. 服务版本管理

**版本化服务**:
```java
// 服务提供者
@DubboService(version = "1.0.0")
public class UserServiceImpl implements UserService {
    // 实现代码
}

// 服务消费者
@DubboReference(version = "1.0.0")
private UserService userService;
```

### 3. 超时和重试配置

**合理的超时设置**:
```yaml
dubbo:
  provider:
    timeout: 5000  # 5秒超时
    retries: 0     # 不重试（写操作）

  consumer:
    timeout: 3000  # 3秒超时
    retries: 2     # 重试2次（读操作）
```

### 4. 负载均衡

**选择合适的负载均衡策略**:
```java
@DubboReference(loadbalance = "random")  // 随机（默认）
@DubboReference(loadbalance = "roundrobin")  // 轮询
@DubboReference(loadbalance = "leastactive")  // 最少活跃
@DubboReference(loadbalance = "consistenthash")  // 一致性哈希
```

### 5. 服务降级

**实现降级策略**:
```java
@DubboReference(mock = "return null", cluster = "failfast")
private UserService userService;

// 或使用 Mock 类
public class UserServiceMock implements UserService {
    public User findById(Long id) {
        return null;  // 降级逻辑
    }
}
```

## 数据访问最佳实践

### 1. MyBatis-Plus 使用

**Lambda 查询（类型安全）**:
```java
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    public List<User> findActiveUsers() {
        return lambdaQuery()
            .eq(User::getStatus, UserStatus.ACTIVE)
            .orderByDesc(User::getCreateTime)
            .list();
    }
}
```

### 2. 事务管理

**明确的事务边界**:
```java
@Service
public class OrderServiceImpl implements OrderService {

    @Transactional(rollbackFor = Exception.class)
    public void createOrder(Order order) {
        // 1. 创建订单
        save(order);

        // 2. 扣减库存
        inventoryService.deduct(order.getProductId(), order.getQuantity());

        // 3. 记录日志
        orderLogService.log(order.getId(), "ORDER_CREATED");
    }
}
```

### 3. 缓存策略

**Spring Cache 注解**:
```java
@Service
public class UserService {

    @Cacheable(value = "users", key = "#userId")
    public User findById(Long userId) {
        return userRepository.findById(userId).orElse(null);
    }

    @CacheEvict(value = "users", key = "#user.id")
    public void update(User user) {
        userRepository.save(user);
    }
}
```

## 安全最佳实践

### 1. 输入验证

**Bean Validation**:
```java
public class CreateUserRequest {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 50, message = "用户名长度必须在3-50之间")
    private String username;

    @Email(message = "邮箱格式不正确")
    @NotBlank(message = "邮箱不能为空")
    private String email;
}
```

### 2. 敏感数据处理

**数据脱敏**:
```java
public class UserResponse {
    private String username;

    public String getPhone() {
        return phone != null
            ? phone.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2")
            : null;
    }
}
```

### 3. 权限控制

**方法级权限**:
```java
@Service
public class OrderService {

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteOrder(Long orderId) {
        // 只有管理员可以删除订单
    }

    @PreAuthorize("#userId == authentication.principal.id")
    public User getUserProfile(Long userId) {
        // 只能查看自己的资料
    }
}
```

## 性能优化最佳实践

### 1. 数据库优化

**索引优化**:
```sql
-- 为常用查询字段添加索引
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_order_status ON `order`(status);
CREATE INDEX idx_order_user_time ON `order`(user_id, create_time);
```

### 2. 分页查询

**使用分页避免大结果集**:
```java
public Page<User> listUsers(Pageable pageable) {
    return userRepository.findAll(pageable);
}

// 调用
Page<User> users = userService.listUsers(
    PageRequest.of(0, 20, Sort.by("createTime").descending())
);
```

### 3. 异步处理

**@Async 注解**:
```java
@Service
public class NotificationService {

    @Async
    public void sendEmailAsync(String to, String subject, String content) {
        emailService.send(to, subject, content);
    }
}
```

## 测试最佳实践

### 1. 单元测试

**JUnit 5 + Mockito**:
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    void shouldReturnUserWhenExists() {
        // Given
        Long userId = 1L;
        User user = new User(userId, "test");
        when(userRepository.findById(userId)).thenReturn(Optional.of(user));

        // When
        User result = userService.findById(userId);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(userId);
    }
}
```

### 2. 集成测试

**@SpringBootTest**:
```java
@SpringBootTest
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb"
})
class UserControllerIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldReturnUserWhenExists() {
        ResponseEntity<User> response = restTemplate.getForEntity(
            "/api/users/1", User.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }
}
```

## 代码质量标准

### 1. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | 大驼峰 | UserService |
| 方法名 | 小驼峰，动词开头 | findById, createUser |
| 变量名 | 小驼峰 | userName, orderId |
| 常量名 | 全大写下划线 | MAX_RETRY_COUNT |
| 包名 | 全小写 | com.company.project.service |

### 2. 方法长度

- 推荐方法长度：10-30 行
- 最大方法长度：不超过 50 行
- 超过限制应拆分为多个小方法

### 3. 类长度

- 推荐类长度：100-300 行
- 最大类长度：不超过 500 行
- 超过限制应拆分为多个类

### 4. 注释规范

```java
/**
 * 用户服务实现类
 *
 * 提供用户管理的业务逻辑实现
 *
 * @author 开发者
 * @version 1.0.0
 * @since 2024-01-01
 */
@Service
public class UserServiceImpl implements UserService {

    /**
     * 根据用户ID查询用户
     *
     * @param userId 用户ID，不能为 null
     * @return 用户信息，不存在返回 null
     * @throws IllegalArgumentException userId 为 null 时抛出
     */
    public User findById(Long userId) {
        if (userId == null) {
            throw new IllegalArgumentException("userId cannot be null");
        }
        // 实现代码
    }
}
```

---

**参考文档**: [编码标准](../rules/coding-standards.md) | [架构原则](../rules/architecture-principles.md)
