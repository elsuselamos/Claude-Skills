# Spring Boot 2.7 + Dubbo 代码示例

## Lombok 最佳实践示例

### 实体类示例
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = false)
@TableName("users")
public class User extends BaseEntity {

    private String username;

    private String email;

    @TableField("phone_number")
    private String phoneNumber;

    @JsonIgnore
    private String password;

    @Builder.Default
    private Integer status = 1;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```

### DTO 示例
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDTO {

    private Long id;

    private String username;

    private String email;

    private String phoneNumber;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;
}
```

### 服务实现示例
```java
@Service
@Slf4j
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserMapper userMapper;

    private final RedisTemplate<String, Object> redisTemplate;

    @Override
    @Transactional
    public UserDTO createUser(CreateUserRequest request) {
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .phoneNumber(request.getPhoneNumber())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();

        userMapper.insert(user);

        log.info("Created user: {}", user.getId());

        return UserDTO.fromEntity(user);
    }

    @Override
    @SneakyThrows(DataAccessException.class)
    public UserDTO getUserById(Long id) {
        String cacheKey = "user:" + id;

        // 先从缓存获取
        UserDTO cachedUser = (UserDTO) redisTemplate.opsForValue().get(cacheKey);
        if (cachedUser != null) {
            return cachedUser;
        }

        // 从数据库获取
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new UserNotFoundException("用户不存在: " + id);
        }

        UserDTO userDTO = UserDTO.fromEntity(user);

        // 缓存结果
        redisTemplate.opsForValue().set(cacheKey, userDTO, 30, TimeUnit.MINUTES);

        return userDTO;
    }

    @Override
    @SneakyThrows
    public void deleteUser(Long id) {
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new UserNotFoundException("用户不存在: " + id);
        }

        userMapper.deleteById(id);
        redisTemplate.delete("user:" + id);

        log.info("Deleted user: {}", id);
    }
}
```

### 基础实体类
```java
@Data
public abstract class BaseEntity {

    @TableId(type = IdType.ASSIGN_ID)
    private Long id;

    @TableField(fill = FieldFill.INSERT)
    @Builder.Default
    private LocalDateTime createTime = LocalDateTime.now();

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;

    @TableField(fill = FieldFill.INSERT)
    @TableField(value = "create_by")
    private String createBy;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @TableField(value = "update_by")
    private String updateBy;
}
```

## Dubbo 服务配置示例

### Dubbo 服务接口定义
```java
@DubboService(version = "${app.dubbo.version}", group = "${app.dubbo.group}")
public interface UserService {

    /**
     * 创建用户
     */
    Result<UserResponse> createUser(UserCreateRequest request);

    /**
     * 根据ID查询用户
     */
    Result<UserResponse> getUserById(Long id);

    /**
     * 根据用户名查询用户
     */
    Result<UserResponse> getUserByUsername(String username);

    /**
     * 更新用户信息
     */
    Result<UserResponse> updateUser(Long id, UserUpdateRequest request);

    /**
     * 删除用户（逻辑删除）
     */
    Result<Void> deleteUser(Long id);

    /**
     * 分页查询用户列表
     */
    Result<PageResult<UserResponse>> listUsers(UserQueryRequest request);

    /**
     * 用户认证
     */
    Result<AuthResponse> authenticate(String username, String password);
}
```

### Dubbo 服务实现
```java
@Service
@DubboService(version = "${app.dubbo.version}", group = "${app.dubbo.group}")
@Slf4j
public class UserServiceImpl implements UserService {

    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;
    private final RedisTemplate<String, Object> redisTemplate;
    private final ApplicationEventPublisher eventPublisher;

    @Autowired
    public UserServiceImpl(UserMapper userMapper,
                           PasswordEncoder passwordEncoder,
                           RedisTemplate<String, Object> redisTemplate,
                           ApplicationEventPublisher eventPublisher) {
        this.userMapper = userMapper;
        this.passwordEncoder = passwordEncoder;
        this.redisTemplate = redisTemplate;
        this.eventPublisher = eventPublisher;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Result<UserResponse> createUser(UserCreateRequest request) {
        try {
            // 检查用户名是否已存在
            if (userMapper.existsByUsername(request.getUsername())) {
                return Result.fail(ResultCode.USER_ALREADY_EXISTS);
            }

            // 检查邮箱是否已存在
            if (userMapper.existsByEmail(request.getEmail())) {
                return Result.fail(ResultCode.EMAIL_ALREADY_EXISTS);
            }

            // 创建用户实体
            User user = User.builder()
                    .username(request.getUsername())
                    .email(request.getEmail())
                    .password(passwordEncoder.encode(request.getPassword()))
                    .firstName(request.getFirstName())
                    .lastName(request.getLastName())
                    .status(UserStatus.ACTIVE)
                    .build();

            userMapper.insert(user);

            // 发布用户创建事件
            eventPublisher.publishEvent(new UserCreatedEvent(user.getId()));

            // 清除相关缓存
            clearUserCache();

            UserResponse response = UserMapper.toResponse(user);
            return Result.success(response);

        } catch (Exception e) {
            log.error("创建用户失败", e);
            return Result.fail(ResultCode.SYSTEM_ERROR);
        }
    }

    @Override
    @Cacheable(value = "user", key = "#id", unless = "#result == null")
    public Result<UserResponse> getUserById(Long id) {
        try {
            User user = userMapper.selectById(id);
            if (user == null || user.getDeleted()) {
                return Result.fail(ResultCode.USER_NOT_FOUND);
            }

            UserResponse response = UserMapper.toResponse(user);
            return Result.success(response);

        } catch (Exception e) {
            log.error("查询用户失败, id: {}", id, e);
            return Result.fail(ResultCode.SYSTEM_ERROR);
        }
    }

    @Override
    @Cacheable(value = "user:username", key = "#username", unless = "#result == null")
    public Result<UserResponse> getUserByUsername(String username) {
        try {
            User user = userMapper.selectByUsername(username);
            if (user == null || user.getDeleted()) {
                return Result.fail(ResultCode.USER_NOT_FOUND);
            }

            UserResponse response = UserMapper.toResponse(user);
            return Result.success(response);

        } catch (Exception e) {
            log.error("根据用户名查询用户失败, username: {}", username, e);
            return Result.fail(ResultCode.SYSTEM_ERROR);
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = {"user", "user:username"}, key = "#id")
    public Result<UserResponse> updateUser(Long id, UserUpdateRequest request) {
        try {
            User user = userMapper.selectById(id);
            if (user == null || user.getDeleted()) {
                return Result.fail(ResultCode.USER_NOT_FOUND);
            }

            // 更新用户信息
            if (StringUtils.hasText(request.getFirstName())) {
                user.setFirstName(request.getFirstName());
            }
            if (StringUtils.hasText(request.getLastName())) {
                user.setLastName(request.getLastName());
            }
            if (request.getStatus() != null) {
                user.setStatus(request.getStatus());
            }

            userMapper.updateById(user);

            // 清除相关缓存
            clearUserCache();

            UserResponse response = UserMapper.toResponse(user);
            return Result.success(response);

        } catch (Exception e) {
            log.error("更新用户失败, id: {}", id, e);
            return Result.fail(ResultCode.SYSTEM_ERROR);
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    @CacheEvict(value = {"user", "user:username"}, key = "#id")
    public Result<Void> deleteUser(Long id) {
        try {
            User user = userMapper.selectById(id);
            if (user == null || user.getDeleted()) {
                return Result.fail(ResultCode.USER_NOT_FOUND);
            }

            // 逻辑删除
            user.setDeleted(LocalDateTime.now());
            userMapper.updateById(user);

            // 清除相关缓存
            clearUserCache();

            return Result.success();

        } catch (Exception e) {
            log.error("删除用户失败, id: {}", id, e);
            return Result.fail(ResultCode.SYSTEM_ERROR);
        }
    }

    @Override
    public Result<PageResult<UserResponse>> listUsers(UserQueryRequest request) {
        try {
            IPage<User> page = new Page<>(request.getPageNum(), request.getPageSize());

            QueryWrapper<User> queryWrapper = new QueryWrapper<>();
            if (StringUtils.hasText(request.getUsername())) {
                queryWrapper.like("username", request.getUsername());
            }
            if (StringUtils.hasText(request.getEmail())) {
                queryWrapper.like("email", request.getEmail());
            }
            if (request.getStatus() != null) {
                queryWrapper.eq("status", request.getStatus());
            }
            queryWrapper.eq("deleted", false);
            queryWrapper.orderByDesc("created_at");

            IPage<User> userPage = userMapper.selectPage(page, queryWrapper);

            List<UserResponse> userResponses = userPage.getRecords().stream()
                    .map(UserMapper::toResponse)
                    .collect(Collectors.toList());

            PageResult<UserResponse> pageResult = new PageResult<>(
                    userResponses,
                    userPage.getTotal(),
                    request.getPageNum(),
                    request.getPageSize()
            );

            return Result.success(pageResult);

        } catch (Exception e) {
            log.error("分页查询用户失败", e);
            return Result.fail(ResultCode.SYSTEM_ERROR);
        }
    }

    @Override
    public Result<AuthResponse> authenticate(String username, String password) {
        try {
            User user = userMapper.selectByUsername(username);
            if (user == null || user.getDeleted()) {
                return Result.fail(ResultCode.USER_NOT_FOUND);
            }

            if (!passwordEncoder.matches(password, user.getPassword())) {
                return Result.fail(ResultCode.PASSWORD_ERROR);
            }

            if (user.getStatus() != UserStatus.ACTIVE) {
                return Result.fail(ResultCode.USER_DISABLED);
            }

            // 生成JWT token
            String token = JwtUtil.generateToken(user.getId(), user.getUsername());

            AuthResponse authResponse = AuthResponse.builder()
                    .token(token)
                    .userId(user.getId())
                    .username(user.getUsername())
                    .roles(user.getRoles())
                    .build();

            return Result.success(authResponse);

        } catch (Exception e) {
            log.error("用户认证失败, username: {}", username, e);
            return Result.fail(ResultCode.SYSTEM_ERROR);
        }
    }

    private void clearUserCache() {
        // 清除用户相关缓存
        Set<String> keys = redisTemplate.keys("user:*");
        if (!keys.isEmpty()) {
            redisTemplate.delete(keys);
        }
    }
}
```

## MyBatis-Plus 实体类
```java
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@TableName("users")
public class User extends BaseEntity {

    @TableId(type = IdType.AUTO)
    private Long id;

    @TableField("username")
    @NotBlank(message = "用户名不能为空")
    private String username;

    @TableField("email")
    @Email(message = "邮箱格式不正确")
    private String email;

    @TableField("password")
    @NotBlank(message = "密码不能为空")
    private String password;

    @TableField("first_name")
    private String firstName;

    @TableField("last_name")
    private String lastName;

    @TableField("phone")
    private String phone;

    @TableField("avatar")
    private String avatar;

    @TableField("status")
    @NotNull(message = "状态不能为空")
    private UserStatus status = UserStatus.ACTIVE;

    @TableField("deleted")
    private LocalDateTime deleted;

    // 逻辑删除注解
    @TableLogic
    public LocalDateTime getDeleted() {
        return deleted;
    }

    public void setDeleted(LocalDateTime deleted) {
        this.deleted = deleted;
    }
}
```
