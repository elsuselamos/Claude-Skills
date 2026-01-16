# 编码规范

## 📋 Spring Boot 2.7 + Dubbo 3 企业级编码规范

本文档定义了 ai-coding-java 项目中的编码标准和最佳实践，确保代码质量、可维护性和团队协作效率。

## [TARGET] 核心原则

### 1. 可读性优先
- 代码应该易于理解和维护
- 清晰的命名和注释
- 逻辑简单，避免过度优化

### 2. 一致性
- 遵循团队统一的编码风格
- 使用相同的设计模式
- 保持代码结构的一致性

### 3. 可测试性
- 编写可单元测试的代码
- 依赖注入和面向接口编程
- 避免硬编码和静态依赖

## [EDIT] 命名规范

### 1. 包命名
```java
// [OK] 正确 - 全小写，用点号分隔
package com.company.project.module.service.impl;

// [X] 错误 - 首字母大写或使用下划线
package com.Company.Project.Module.Service;
package com.company.project.module.service_impl;
```

### 2. 类命名
```java
// [OK] 正确 - 大驼峰命名法
public class UserService {}
public class OrderRepositoryImpl {}
public class PaymentController {}

// [X] 错误 - 小驼峰或下划线
public class userService {}
public class order_repository_impl {}
```

### 3. 方法和变量命名
```java
public class UserService {

    // [OK] 正确 - 小驼峰命名法
    private UserRepository userRepository;
    private String userName;
    private List<Order> orderList;

    // [OK] 正确 - 动词开头，表达明确的操作
    public User createUser(CreateUserRequest request) {}
    public boolean validateUserCredentials(String username, String password) {}
    public List<User> findActiveUsersByDepartment(String departmentId) {}

    // [X] 错误 - 名词开头或含义不明
    public User user(CreateUserRequest request) {}
    public boolean check(String username, String password) {}
    public List<User> get(String departmentId) {}
}
```

### 4. 常量命名
```java
public class OrderConstants {

    // [OK] 正确 - 全大写，下划线分隔
    public static final int MAX_ORDER_AMOUNT = 10000;
    public static final String DEFAULT_STATUS = "PENDING";
    public static final long TOKEN_EXPIRE_TIME = 3600L;

    // [X] 错误 - 小驼峰或混合大小写
    public static final int maxOrderAmount = 10000;
    public static final String defaultStatus = "PENDING";
}
```

## [BOOK] 注释规范

### 1. 类注释
```java
/**
 * 用户服务实现类
 *
 * 提供用户管理相关的业务逻辑实现，包括用户注册、登录、信息更新等功能。
 * 支持分布式部署，通过 Dubbo 提供服务接口。
 *
 * @author 开发者姓名
 * @version 1.0.0
 * @since 2023-12-07
 */
@Service
@Transactional
public class UserServiceImpl implements UserService {

}
```

### 2. 方法注释
```java
/**
 * 创建新用户
 *
 * 根据提供的用户信息创建新用户账户，包括：
 * - 基本信息验证和存储
 * - 密码加密
 * - 默认角色分配
 * - 审计信息记录
 *
 * @param request 用户创建请求，包含用户基本信息
 * @return 创建成功的用户信息，不包含敏感数据
 * @throws BusinessException 当用户名已存在时抛出
 * @throws ValidationException 当请求数据验证失败时抛出
 */
@Transactional(rollbackFor = Exception.class)
public UserResponse createUser(CreateUserRequest request) {
    // 实现逻辑
}
```

### 3. 复杂逻辑注释
```java
public Order calculateOrderTotal(Order order) {
    BigDecimal totalAmount = BigDecimal.ZERO;

    // 计算商品总价
    for (OrderItem item : order.getItems()) {
        // 商品单价 × 数量 - 促销折扣
        BigDecimal itemTotal = item.getUnitPrice()
            .multiply(new BigDecimal(item.getQuantity()))
            .subtract(item.getDiscountAmount());
        totalAmount = totalAmount.add(itemTotal);
    }

    // 应用订单级优惠券折扣
    if (order.getCouponCode() != null) {
        Coupon coupon = couponService.getByCode(order.getCouponCode());
        if (coupon != null && coupon.isValid()) {
            totalAmount = totalAmount.subtract(coupon.getDiscountAmount());
        }
    }

    // 检查最小订单金额限制
    if (totalAmount.compareTo(BigDecimal.valueOf(10)) < 0) {
        throw new BusinessException("订单金额不能小于10元");
    }

    return totalAmount;
}
```

## [ARCHITECTURE] 代码结构规范

### 1. 类结构顺序
```java
public class UserService {

    // 1. 静态常量
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    // 2. 实例变量（按访问级别排序：private -> protected -> public）
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    // 3. 构造方法
    public UserService() {}

    @Autowired
    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    // 4. 公共方法（按业务逻辑分组）
    public User createUser(CreateUserRequest request) {}
    public User updateUser(Long userId, UpdateUserRequest request) {}
    public void deleteUser(Long userId) {}

    // 5. 受保护方法
    protected void validateUserRequest(CreateUserRequest request) {}

    // 6. 私有方法
    private String encryptPassword(String rawPassword) {}
    private UserResponse convertToResponse(User user) {}

    // 7. 静态方法
    public static boolean isValidEmail(String email) {}
}
```

### 2. 方法长度控制
```java
// [OK] 正确 - 单一职责，长度适中
public UserResponse createUser(CreateUserRequest request) {
    // 验证请求参数
    validateCreateUserRequest(request);

    // 检查用户名是否已存在
    if (userRepository.existsByUsername(request.getUsername())) {
        throw new BusinessException("用户名已存在");
    }

    // 创建用户实体
    User user = buildUserFromRequest(request);

    // 保存用户
    User savedUser = userRepository.save(user);

    // 发送欢迎邮件（异步）
    sendWelcomeEmail(savedUser);

    return convertToResponse(savedUser);
}

// [X] 错误 - 方法过长，职责不清
public UserResponse createUser(CreateUserRequest request) {
    // 100+ 行代码包含验证、业务逻辑、数据转换、通知等
}
```

## 🔐 异常处理规范

### 1. 自定义异常类
```java
// 业务异常基类
public class BusinessException extends RuntimeException {
    private final String errorCode;

    public BusinessException(String message) {
        super(message);
        this.errorCode = "BUSINESS_ERROR";
    }

    public BusinessException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
}

// 具体业务异常
public class UserNotFoundException extends BusinessException {
    public UserNotFoundException(String username) {
        super("USER_NOT_FOUND", "用户不存在: " + username);
    }
}
```

### 2. 异常处理策略
```java
@Service
public class UserService {

    public User createUser(CreateUserRequest request) {
        try {
            // 业务逻辑
            return userRepository.save(user);
        } catch (DataIntegrityViolationException e) {
            // 数据完整性约束异常
            throw new BusinessException("USER_ALREADY_EXISTS", "用户已存在");
        } catch (Exception e) {
            // 其他未知异常
            logger.error("创建用户失败", e);
            throw new BusinessException("SYSTEM_ERROR", "系统错误，请稍后重试");
        }
    }
}
```

### 3. 全局异常处理
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException e) {
        ErrorResponse error = ErrorResponse.builder()
            .code(e.getErrorCode())
            .message(e.getMessage())
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(ValidationException e) {
        ErrorResponse error = ErrorResponse.builder()
            .code("VALIDATION_ERROR")
            .message(e.getMessage())
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.badRequest().body(error);
    }
}
```

## 🧪 测试规范

### 1. 单元测试
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("创建用户成功")
    void shouldCreateUserSuccessfully() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
            .username("testuser")
            .email("test@example.com")
            .password("password123")
            .build();

        User savedUser = User.builder()
            .id(1L)
            .username("testuser")
            .email("test@example.com")
            .password("encryptedPassword")
            .build();

        when(userRepository.existsByUsername("testuser")).thenReturn(false);
        when(passwordEncoder.encode("password123")).thenReturn("encryptedPassword");
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // When
        UserResponse response = userService.createUser(request);

        // Then
        assertThat(response.getUsername()).isEqualTo("testuser");
        assertThat(response.getEmail()).isEqualTo("test@example.com");
        verify(userRepository).save(any(User.class));
    }

    @Test
    @DisplayName("用户名已存在时抛出异常")
    void shouldThrowExceptionWhenUsernameExists() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
            .username("existinguser")
            .build();

        when(userRepository.existsByUsername("existinguser")).thenReturn(true);

        // When & Then
        assertThatThrownBy(() -> userService.createUser(request))
            .isInstanceOf(BusinessException.class)
            .hasMessage("用户名已存在");
    }
}
```

### 2. 集成测试
```java
@SpringBootTest
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
class UserControllerIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldCreateUserSuccessfully() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
            .username("testuser")
            .email("test@example.com")
            .password("password123")
            .build();

        // When
        ResponseEntity<UserResponse> response = restTemplate.postForEntity(
            "/api/users", request, UserResponse.class);

        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().getUsername()).isEqualTo("testuser");
    }
}
```

## [TOOL] 配置规范

### 1. 配置类
```java
@Configuration
@EnableConfigurationProperties({RedisProperties.class, DatabaseProperties.class})
public class AppConfig {

    @Bean
    @ConditionalOnProperty(name = "cache.enabled", havingValue = "true")
    public CacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(30))
            .serializeKeysWith(RedisSerializationContext.SerializationPair.fromSerializer(new StringRedisSerializer()))
            .serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(new GenericJackson2JsonRedisSerializer()));

        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
    }
}
```

### 2. 配置属性
```java
@ConfigurationProperties(prefix = "app")
@Data
public class AppConfigProperties {

    private String name;
    private String version;
    private Cache cache = new Cache();

    @Data
    public static class Cache {
        private boolean enabled = true;
        private Duration ttl = Duration.ofMinutes(30);
        private int maxSize = 1000;
    }
}
```

## [CHART] 性能优化规范

### 1. 数据库访问优化
```java
// [OK] 正确 - 使用分页查询
public Page<User> findUsersByPage(UserQuery query, Pageable pageable) {
    return userRepository.findByConditions(
        query.getUsername(),
        query.getEmail(),
        query.getStatus(),
        pageable
    );
}

// [X] 错误 - 一次性加载大量数据
public List<User> findAllUsers() {
    return userRepository.findAll(); // 可能导致内存溢出
}
```

### 2. 缓存使用规范
```java
@Service
public class UserService {

    @Cacheable(value = "users", key = "#userId")
    public User getUserById(Long userId) {
        return userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId));
    }

    @CacheEvict(value = "users", key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
}
```

### 3. 异步处理
```java
@Service
public class NotificationService {

    @Async
    public void sendEmailAsync(String to, String subject, String content) {
        try {
            emailService.send(to, subject, content);
        } catch (Exception e) {
            logger.error("发送邮件失败: to={}, subject={}", to, subject, e);
        }
    }
}
```

## 🔒 安全编码规范

### 1. 输入验证
```java
public class CreateUserRequest {

    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 50, message = "用户名长度必须在3-50个字符之间")
    @Pattern(regexp = "^[a-zA-Z0-9_]+$", message = "用户名只能包含字母、数字和下划线")
    private String username;

    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;

    @NotBlank(message = "密码不能为空")
    @Size(min = 8, message = "密码长度不能少于8位")
    @Pattern(regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]",
             message = "密码必须包含大小写字母、数字和特殊字符")
    private String password;
}
```

### 2. 敏感信息处理
```java
public class UserResponse {

    private Long id;
    private String username;
    private String email;

    // [X] 不要在响应中包含敏感信息
    // private String password;
    // private String creditCardNumber;

    // [OK] 使用数据脱敏
    public String getPhone() {
        return phone != null ? phone.replaceAll("(\\d{3})\\d{4}(\\d{4})", "$1****$2") : null;
    }
}
```

### 3. SQL 注入防护
```java
// [OK] 正确 - 使用参数化查询
@Query("SELECT u FROM User u WHERE u.username = :username AND u.status = :status")
List<User> findByUsernameAndStatus(@Param("username") String username, @Param("status") String status);

// [X] 错误 - 字符串拼接容易导致 SQL 注入
// @Query("SELECT u FROM User u WHERE u.username = '" + username + "'")
```

## 📋 代码审查检查清单

### 1. 命名和可读性
- [ ] 类名、方法名、变量名符合命名规范
- [ ] 常量使用全大写下划线分隔
- [ ] 代码自文档化，必要时有注释
- [ ] 复杂逻辑有详细注释说明

### 2. 异常处理
- [ ] 业务异常使用自定义异常类
- [ ] 异常信息清晰明确
- [ ] 有全局异常处理机制
- [ ] 日志记录恰当，不泄露敏感信息

### 3. 安全性
- [ ] 输入参数验证完整
- [ ] 敏感信息不记录到日志
- [ ] SQL 注入防护到位
- [ ] 权限控制正确实现

### 4. 性能考虑
- [ ] 避免不必要的数据库查询
- [ ] 合理使用缓存
- [ ] 大数据量操作使用分页
- [ ] 及时释放资源

### 5. 测试覆盖
- [ ] 单元测试覆盖核心业务逻辑
- [ ] 边界条件测试完整
- [ ] 异常场景测试覆盖
- [ ] 集成测试验证端到端流程

---

## [OK] 遵循本规范

遵循本编码规范将有助于：

1. **提高代码质量** - 统一的编码标准减少错误
2. **增强可维护性** - 清晰的命名和结构便于理解和修改
3. **促进团队协作** - 统一的风格减少沟通成本
4. **保证系统稳定性** - 规范的异常处理和安全防护
5. **提升开发效率** - 标准化的开发和测试流程

请所有开发人员严格遵循本规范，并在代码审查中作为重要参考标准。