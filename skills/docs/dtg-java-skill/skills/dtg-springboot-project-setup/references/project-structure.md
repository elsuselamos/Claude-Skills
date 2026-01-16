# Spring Boot 2.7 + Dubbo 项目结构

## 推荐目录结构
```
src/
├── main/
│   ├── java/com/enterprise/
│   │   ├── Application.java           # 启动类
│   │   ├── config/                    # 配置类
│   │   │   ├── SecurityConfig.java
│   │   │   ├── WebConfig.java
│   │   │   └── RedisConfig.java
│   │   ├── controller/                # 控制器层
│   │   │   └── UserController.java
│   │   ├── service/                   # 服务层
│   │   │   ├── UserService.java
│   │   │   └── impl/
│   │   ├── repository/                # 数据访问层
│   │   │   ├── UserRepository.java
│   │   │   └── custom/
│   │   ├── entity/                    # 实体类
│   │   │   ├── User.java
│   │   │   └── BaseEntity.java
│   │   ├── dto/                       # 数据传输对象
│   │   │   ├── request/
│   │   │   ├── response/
│   │   │   └── mapper/
│   │   ├── security/                  # 安全相关
│   │   │   ├── JwtAuthenticationFilter.java
│   │   │   └── UserDetailsServiceImpl.java
│   │   ├── exception/                 # 异常处理
│   │   │   ├── GlobalExceptionHandler.java
│   │   │   └── ResourceNotFoundException.java
│   │   └── util/                      # 工具类
│   │       ├── JwtUtil.java
│   │       └── ValidationUtil.java
│   └── resources/
│       ├── application.yml
│       ├── application-dev.yml
│       ├── application-prod.yml
│       └── application-test.yml
└── test/
    └── java/com/enterprise/
        ├── common/
        │   └── AbstractIntegrationTest.java
        ├── controller/
        ├── service/
        └── repository/
```

## 分层架构设计原则
- **Controller层**: 处理HTTP请求，参数验证，调用Service层
- **Service层**: 业务逻辑处理，事务管理
- **Repository层**: 数据访问，与数据库交互
- **DTO层**: 数据传输对象，避免暴露实体
- **Utils层**: 通用工具类，可复用功能
