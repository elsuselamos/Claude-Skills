# Spring Boot 2.7 + Dubbo 测试配置示例

## JUnit 5 配置

### 测试环境配置 (application-test.yml)
```yaml
spring:
  datasource:
    driver-class-name: org.h2.Driver
    url: jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1
    username: sa
    password:

# MyBatis-Plus 测试配置
mybatis-plus:
  configuration:
    # 开启驼峰转换
    map-underscore-to-camel-case: true
    # 打印sql，便于测试
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  global-config:
    db-config:
      # H2 不支持自增，使用 ASSIGN_ID
      id-type: ASSIGN_ID

spring:
  redis:
    host: localhost
    port: 6379
    database: 1 # 使用不同的数据库

logging:
  level:
    com.enterprise: DEBUG
    org.springframework.web: DEBUG
```

### 测试基类
```java
// src/test/java/com/enterprise/common/AbstractIntegrationTest.java
@SpringBootTest
@ActiveProfiles("test")
@Testcontainers
@Transactional
public abstract class AbstractIntegrationTest {

    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }

    @Autowired
    protected TestRestTemplate restTemplate;

    protected HttpHeaders getHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        return headers;
    }

    protected HttpHeaders getAuthenticatedHeaders(String token) {
        HttpHeaders headers = getHeaders();
        headers.setBearerAuth(token);
        return headers;
    }
}
```

## 单元测试示例
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    void shouldCreateUser() {
        // Given
        UserCreateRequest request = UserCreateRequest.builder()
                .username("testuser")
                .email("test@example.com")
                .password("password")
                .build();

        User savedUser = User.builder()
                .id(1L)
                .username(request.getUsername())
                .email(request.getEmail())
                .status(UserStatus.ACTIVE)
                .build();

        when(userRepository.existsByUsername(request.getUsername())).thenReturn(false);
        when(userRepository.existsByEmail(request.getEmail())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // When
        UserResponse response = userService.createUser(request);

        // Then
        assertThat(response.getId()).isEqualTo(1L);
        assertThat(response.getUsername()).isEqualTo("testuser");
        verify(userRepository).save(any(User.class));
    }
}
```

## 集成测试示例
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class UserControllerIntegrationTest extends AbstractIntegrationTest {

    @Test
    void shouldCreateUserSuccessfully() {
        // Given
        UserCreateRequest request = UserCreateRequest.builder()
                .username("newuser")
                .email("newuser@example.com")
                .password("password123")
                .firstName("John")
                .lastName("Doe")
                .build();

        HttpEntity<UserCreateRequest> entity = new HttpEntity<>(request, getHeaders());

        // When
        ResponseEntity<UserResponse> response = restTemplate.exchange(
                "/api/v1/users",
                HttpMethod.POST,
                entity,
                UserResponse.class
        );

        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().getUsername()).isEqualTo("newuser");
        assertThat(response.getBody().getEmail()).isEqualTo("newuser@example.com");
    }
}
```
