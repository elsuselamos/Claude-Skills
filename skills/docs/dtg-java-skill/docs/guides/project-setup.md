# 项目设置指南

## [ARCHITECTURE] Spring Boot 2.7 + Dubbo 3 企业级项目设置

本指南将帮助您快速搭建一个生产就绪的 Spring Boot 2.7 + Dubbo 3 企业级微服务项目，集成最佳实践和企业级配置。

## 📋 项目结构规范

### 标准目录结构
```
project-root/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── yourcompany/
│   │   │           └── yourproject/
│   │   │               ├── YourApplication.java
│   │   │               ├── api/              # API 接口定义
│   │   │               ├── controller/       # REST 控制器
│   │   │               ├── service/          # 业务逻辑服务
│   │   │               ├── repository/       # 数据访问层
│   │   │               ├── entity/           # 实体类
│   │   │               ├── dto/              # 数据传输对象
│   │   │               ├── config/           # 配置类
│   │   │               ├── common/           # 公共组件
│   │   │               │   ├── exception/    # 异常处理
│   │   │               │   ├── utils/        # 工具类
│   │   │               │   └── constants/    # 常量定义
│   │   │               └── dubbo/            # Dubbo 服务
│   │   │                   ├── api/          # Dubbo 接口
│   │   │                   ├── impl/         # Dubbo 实现
│   │   │                   └── filter/       # Dubbo 过滤器
│   │   └── resources/
│   │       ├── application.yml              # 主配置文件
│   │       ├── application-dev.yml          # 开发环境配置
│   │       ├── application-test.yml         # 测试环境配置
│   │       ├── application-prod.yml         # 生产环境配置
│   │       ├── dubbo-consumer.yml           # Dubbo 消费者配置
│   │       ├── dubbo-provider.yml           # Dubbo 提供者配置
│   │       ├── logback-spring.xml           # 日志配置
│   │       ├── mapper/                      # MyBatis 映射文件
│   │       └── static/                      # 静态资源
│   └── test/                                # 测试代码
│       └── java/
│           └── com/
│               └── yourcompany/
│                   └── yourproject/
│                       ├── integration/     # 集成测试
│                       └── unit/            # 单元测试
├── docs/                                     # 项目文档
├── scripts/                                  # 构建和部署脚本
├── docker/                                   # Docker 相关文件
└── pom.xml                                   # Maven 配置
```

## [FAST] 快速项目初始化

### 1. 使用项目注入命令

```bash
/ai-coding-java:project-inject
```

此命令会自动：
- [OK] 检测当前目录结构
- [OK] 创建标准的项目目录结构
- [OK] 生成配置文件模板
- [OK] 设置企业级开发环境
- [OK] 初始化质量门检查

### 2. 手动项目创建

如果您需要手动创建项目，请按以下步骤操作：

#### 2.1 创建 Maven 项目
```bash
mvn archetype:generate \
  -DgroupId=com.yourcompany.yourproject \
  -DartifactId=your-microservice \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DinteractiveMode=false
```

#### 2.2 转换为 Spring Boot 项目
在 `pom.xml` 中添加 Spring Boot 父项目：
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.7.18</version>
    <relativePath/>
</parent>
```

## [TOOLS] 核心配置文件

### 1. Maven 依赖配置

#### 核心依赖
```xml
<dependencies>
    <!-- Spring Boot 核心依赖 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-aop</artifactId>
    </dependency>

    <!-- Dubbo 依赖 -->
    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-spring-boot-starter</artifactId>
        <version>3.2.14</version>
    </dependency>

    <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-registry-nacos</artifactId>
        <version>3.2.14</version>
    </dependency>

    <!-- 数据库依赖 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- MyBatis-Plus -->
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-boot-starter</artifactId>
        <version>3.5.7</version>
    </dependency>

    <!-- Redis -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>

    <!-- 消息队列 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-activemq</artifactId>
    </dependency>

    <!-- 工具依赖 -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>

    <dependency>
        <groupId>cn.hutool</groupId>
        <artifactId>hutool-all</artifactId>
        <version>5.8.25</version>
    </dependency>

    <!-- 测试依赖 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

#### 构建配置
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <excludes>
                    <exclude>
                        <groupId>org.projectlombok</groupId>
                        <artifactId>lombok</artifactId>
                    </exclude>
                </excludes>
            </configuration>
        </plugin>

        <!-- MyBatis-Plus 代码生成插件 -->
        <plugin>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-generator</artifactId>
            <version>3.5.7</version>
        </plugin>
    </plugins>
</build>
```

### 2. Spring Boot 主配置 (application.yml)

```yaml
server:
  port: 8080
  servlet:
    context-path: /api
  tomcat:
    max-threads: 200
    min-spare-threads: 10

spring:
  application:
    name: ${MICROSERVICE_NAME:your-microservice}
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

  # 数据源配置
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${DB_HOST:localhost}:${DB_PORT:3306}/${DB_NAME:yourdb}?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:password}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000

  # JPA 配置
  jpa:
    hibernate:
      ddl-auto: ${JPA_DDL_AUTO:none}
    show-sql: ${JPA_SHOW_SQL:false}
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL8Dialect
        format_sql: true

  # Redis 配置
  redis:
    host: ${REDIS_HOST:localhost}
    port: ${REDIS_PORT:6379}
    password: ${REDIS_PASSWORD:}
    database: 0
    timeout: 5000ms
    lettuce:
      pool:
        max-active: 8
        max-idle: 8
        min-idle: 0
        max-wait: -1ms

  # 消息队列配置
  activemq:
    broker-url: tcp://${ACTIVEMQ_HOST:localhost}:${ACTIVEMQ_PORT:61616}
    user: ${ACTIVEMQ_USER:admin}
    password: ${ACTIVEMQ_PASSWORD:admin}
    pool:
      enabled: true
      max-connections: 10

# 管理端点配置
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,dubbo
  endpoint:
    health:
      show-details: when-authorized
  metrics:
    export:
      prometheus:
        enabled: true

# 日志配置
logging:
  level:
    com.yourcompany.yourproject: ${LOG_LEVEL:INFO}
    org.apache.dubbo: ${DUBBO_LOG_LEVEL:WARN}
    org.springframework: ${SPRING_LOG_LEVEL:INFO}
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level [%logger{50}] - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level [%logger{50}] - %msg%n"
  file:
    name: logs/application.log
    max-size: 100MB
    max-history: 30
```

### 3. Dubbo 提供者配置 (dubbo-provider.yml)

```yaml
dubbo:
  application:
    name: ${dubbo.application.name:${spring.application.name}}
    version: ${dubbo.application.version:1.0.0}
    owner: ${dubbo.application.owner:yourcompany}
    organization: ${dubbo.application.organization:yourproject}

  protocol:
    name: dubbo
    port: ${dubbo.protocol.port:20880}
    threads: 200
    heartbeat: 60000

  registry:
    address: ${DUBBO_REGISTRY_ADDRESS:nacos://localhost:8848}
    timeout: 5000
    group: ${DUBBO_REGISTRY_GROUP:DEFAULT_GROUP}

  provider:
    timeout: 30000
    retries: 0
    delay: 0
    version: ${dubbo.provider.version:1.0.0}
    group: ${dubbo.provider.group:default-group}
    validation: true

  # 监控配置
  monitor:
    protocol: registry

  # 负载均衡配置
  consumer:
    check: false
    timeout: 30000
    retries: 2
    loadbalance: roundrobin
```

### 4. Dubbo 消费者配置 (dubbo-consumer.yml)

```yaml
dubbo:
  consumer:
    check: false
    timeout: 30000
    retries: 2
    version: ${dubbo.consumer.version:1.0.0}
    group: ${dubbo.consumer.group:default-group}
    loadbalance: roundrobin

  # 引用配置
  reference:
    check: false
    timeout: 30000
    retries: 2
```

## [TOOL] 开发环境配置

### 1. 开发环境配置 (application-dev.yml)

```yaml
spring:
  # 开发环境数据源
  datasource:
    url: jdbc:mysql://localhost:3306/yourdb_dev?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai

  # JPA 开发环境配置
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true

  # 开发工具配置
  devtools:
    restart:
      enabled: true
    livereload:
      enabled: true

# 日志级别
logging:
  level:
    root: INFO
    com.yourcompany.yourproject: DEBUG
    org.springframework.web: DEBUG
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE

# Dubbo 开发配置
dubbo:
  provider:
    timeout: 60000
  registry:
    address: nacos://localhost:8848
```

### 2. 测试环境配置 (application-test.yml)

```yaml
spring:
  # 测试环境数据源
  datasource:
    url: jdbc:mysql://test-db:3306/yourdb_test?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai

  # JPA 测试环境配置
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false

# 日志配置
logging:
  level:
    root: WARN
    com.yourcompany.yourproject: INFO

# Dubbo 测试配置
dubbo:
  registry:
    address: nacos://test-nacos:8848
```

### 3. 生产环境配置 (application-prod.yml)

```yaml
spring:
  # 生产环境数据源
  datasource:
    url: jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME}?useUnicode=true&characterEncoding=utf8&useSSL=true&serverTimezone=Asia/Shanghai

  # JPA 生产环境配置
  jpa:
    hibernate:
      ddl-auto: none
    show-sql: false

# 日志配置
logging:
  level:
    root: ERROR
    com.yourcompany.yourproject: WARN

# Dubbo 生产配置
dubbo:
  registry:
    address: ${DUBBO_REGISTRY_ADDRESS}
  provider:
    timeout: 10000
    retries: 3
```

## [ROCKET] 启动类配置

### 主应用类
```java
package com.yourcompany.yourproject;

import org.apache.dubbo.config.spring.context.annotation.EnableDubbo;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableDubbo
@EnableCaching
@EnableAsync
@EnableScheduling
public class YourApplication {
    public static void main(String[] args) {
        SpringApplication.run(YourApplication.class, args);
    }
}
```

## [SEARCH] 常见问题解决

### 1. 端口冲突
```bash
# 检查端口占用
lsof -i :8080
lsof -i :20880

# 杀死进程
kill -9 <PID>
```

### 2. 数据库连接失败
```bash
# 测试数据库连接
mysql -h localhost -P 3306 -u root -p

# 检查数据库服务状态
systemctl status mysql
```

### 3. Redis 连接问题
```bash
# 测试 Redis 连接
redis-cli ping

# 检查 Redis 服务状态
systemctl status redis
```

### 4. Dubbo 注册中心连接
```bash
# 测试 Nacos 连接
curl http://localhost:8848/nacos/v1/console/health

# 检查服务注册
curl http://localhost:8848/nacos/v1/ns/instance/list\?serviceName\=your-service-name
```

## 🧪 项目验证

### 1. 编译检查
```bash
mvn clean compile
```

### 2. 测试运行
```bash
mvn test
```

### 3. 应用启动
```bash
# 开发环境
mvn spring-boot:run -Dspring.profiles.active=dev

# 生产环境
java -jar target/your-microservice.jar --spring.profiles.active=prod
```

### 4. 健康检查
```bash
# 应用健康状态
curl http://localhost:8080/api/actuator/health

# 应用信息
curl http://localhost:8080/api/actuator/info

# 指标监控
curl http://localhost:8080/api/actuator/metrics
```

## [LIBRARY] 进一步配置

### 1. Docker 支持
```dockerfile
FROM openjdk:11-jre-slim

WORKDIR /app

COPY target/your-microservice.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 2. Kubernetes 部署
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: your-microservice
  template:
    metadata:
      labels:
        app: your-microservice
    spec:
      containers:
      - name: your-microservice
        image: your-registry/your-microservice:latest
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
```

---

## [OK] 配置完成！

您的企业级 Spring Boot 2.7 + Dubbo 3 项目现在已经完成基础配置。接下来可以：

1. **查看微服务开发指南** - 学习如何开发具体的业务功能
2. **配置 Dubbo 服务** - 学习微服务间的通信配置
3. **设置数据库集成** - 配置持久层和数据访问
4. **部署和监控** - 了解生产环境的部署和监控方案