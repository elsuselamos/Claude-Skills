---
name: soft-design
description: Opinionated full-stack engineering conventions (Spring Boot + MyBatis + MySQL + Vue 3 + TypeScript) for consistent, secure, observable delivery.
license: Internal
---

## 1. 技术栈约定

  - 后端：Spring Boot + MyBatis（建议 MyBatis-Plus 也可，但规则一致）+ MySQL
  - 前端：Vue3 + TypeScript + Vite + Pinia + Vue Router + Axios
  - 鉴权：JWT（Access Token + Refresh Token 方案优先）

## 2. 版本约束

- **Framework**: 强制使用 **Spring Boot Latest** (最新 GA 版本)。
- **JDK**: 强制 **JDK 21**，启用虚拟线程 (Virtual Threads) 提升并发性能。

## 3. 总体原则

  - **前后端完全解耦**：只通过 HTTP/JSON（或 RESTful）契约交互；禁止前端直连数据库。
  - **约定优于配置**：统一命名、目录、DTO/VO 规范、错误码、日志格式、分页规则。
  - **可观测与可回滚**：上线必须具备日志、监控、告警、灰度/回滚方案。
  - **安全默认开启**：鉴权、鉴别、审计、输入校验、防注入、防越权。
  - **SQL 离散化**: 所有的 SQL 语句**必须**编写在对应的 `Mapper.xml` 映射文件中，严禁在 Java 代码中使用 `@Select`, `@Insert` 等注解直接编写 SQL。
- **分层管理**: XML 文件应按功能模块在 `resources/mapper`。
- **分层约束**: 严格遵循 `Controller` -> `Service` -> `Mapper` 分层，禁止跨层调用。
- **对象隔离**: 严格区分 `DO` (数据库实体), `DTO` (传输对象), `VO` (视图对象)，禁止 POJO 一穿到底。
- **基建复用**: 坚持 "Don't Reinvent the Wheel"，优先使用 Hutool, Apache Commons, Guava 等成熟类库。
- **代码注释**：代码不需有中文注释 且注释逻辑清晰

## 4. 后端（SpringBoot）代码规范

### 4.1 工程目录结构

  - com.xxx.project
    - controller/：仅做入参接收、校验、鉴权注解、调用 service、返回 VO
    - service/、service/impl/：业务逻辑、事务
    - mapper/：MyBatis Mapper 接口
    - mapper/xml/：XML（若使用 XML）
    - domain/entity/：数据库实体（DO/Entity）
    - domain/dto/：入参 DTO（请求）
    - domain/vo/：出参 VO（响应）
    - common/：统一响应、异常、错误码、工具、常量
    - config/：安全、Web、MyBatis、跨域、序列化配置
    - security/：JWT 过滤器、鉴权上下文、权限判定
  - 禁止：Controller 直接操作 Mapper；Entity 直接对外返回；在 SQL 拼接用户输入。
  - 推荐分层：controller / service / repository(mapper) / domain / dto / vo / config / common
    - 规则：
        - controller 只做参数接收、校验、鉴权、调用 service、返回 VO；禁止写业务逻辑。
        - service 承载业务；事务只放 service；禁止 controller 开事务。
        - repository/mapper 仅负责数据访问；禁止拼接不安全 SQL。
        - DTO/VO 与实体分离：数据库实体（Entity/DO）不直接对外输出。

  ### 4.2 命名约定

  - 类：UserService UserController
  - 接口：IUserService（或不加 I，但全局统一）
  - 方法：动词开头：createUser getById listUsers
  - 包名全小写；常量全大写下划线。

  ### 4.3 接口设计（REST 建议）

  - URL：/api/v1/users（版本前缀统一）
  - HTTP 方法：GET 查询 / POST 新增 / PUT 更新 / DELETE 删除
  - 状态码：200/201/204/400/401/403/404/409/500 按语义使用

  ### 4.4 统一响应与错误码

  - 统一响应体（示例字段）：code message data requestId timestamp
  - 错误码：
    - 分段：如 1xxx 通用，2xxx 用户域，3xxx 订单域…
    - 业务异常用自定义异常 + 错误码；禁止直接把堆栈信息返回前端。
  - 全局异常处理：@ControllerAdvice 统一兜底，日志记录 requestId。

  ### 4.5 参数校验与序列化

  - 入参 DTO 必须 @Valid，字段用 @NotNull/@NotBlank/@Size/...
  - 日期时间统一：后端用 Instant/LocalDateTime；接口统一时区策略（建议 UTC 或明确 Asia/Shanghai），并写入规范。

  ### 4.6 事务与幂等

  - 事务：@Transactional 只加在 service；避免大事务；读写分离场景明确只读事务。
  - 幂等：对创建/支付/回调等关键接口，使用幂等键（如 Idempotency-Key）或业务唯一约束。

  ### 4.7 日志规范

  - 使用 SLF4J；禁止 System.out
  - 日志字段最少：requestId userId uri method ip cost resultCode
  - 级别：
    - INFO：关键业务动作、接口访问摘要
    - WARN：可恢复异常、参数异常、第三方超时
    - ERROR：不可恢复异常（带堆栈）
  - 禁止记录敏感信息：密码、完整身份证号、完整 Token、银行卡号等（需脱敏）。


  ## 5. 前端（Vue）规范

  ### 5.1 工程结构（示例）

  - src/api/（接口封装）
  - src/views/（页面）
  - src/components/（通用组件）
  - src/router/（路由）
  - src/store/（状态管理：Pinia/Vuex）
  - src/utils/（工具）
  - src/styles/（全局样式/变量）
  - src/types/（TS 类型）

  ### 5.2 编码与风格

  - 必须启用：ESLint + Prettier（团队统一规则）
  - 组件命名：PascalCase；文件名与组件名一致
  - 逻辑分层：页面只组装与调用；复杂逻辑下沉到 composables/hooks 或 services
  - 禁止在组件内散落重复请求代码：统一走 api 层封装与拦截器。

  ### 5.3 接口与状态

  - API 统一封装：baseURL、超时、重试策略（谨慎）、错误处理、请求取消
  - Token 存储策略明确（优先 HttpOnly Cookie；如用 localStorage 需配合 XSS 防护）
  - 路由守卫：鉴权、权限（角色/资源）控制统一实现

  ### 5.4 UI/交互规范

  - 全局 Loading、错误提示、空态、权限无权提示统一组件/规范
  - 表单校验前后端一致：前端做体验校验，后端做强制校验


  ## 6. 数据库（MySQL）规范

  ### 6.1 表与字段命名

  - 表：小写下划线：user_account
  - 主键：id（建议 bigint）
  - 通用字段（建议）：created_at updated_at deleted（软删如需要）version（乐观锁如需要）
  - 字段语义清晰：布尔用 is_xxx 或 xxx_flag（全局统一）

  ### 6.2 设计与约束

  - 必要的唯一约束/外键策略要明确（强一致可用外键；高并发场景可用逻辑约束+应用保证）。
  - 索引规范：
    - 以查询驱动建索引；复合索引遵循最左前缀；避免过度索引。
    - 大字段（TEXT/BLOB）谨慎索引。
  - 字符集与排序规则统一：建议 utf8mb4。
  - 分页必须有稳定排序字段（如 id desc）。

  ### 6.3 SQL 与迁移

  - 禁止在代码中拼接用户输入形成 SQL；使用预编译/ORM 参数绑定。
  - 数据库变更走迁移工具（Flyway/Liquibase）：每次变更有版本脚本，可回滚策略写清楚。
  - 生产变更必须评审并在低峰执行，提前评估锁表风险。



  ## 7. 接口与数据契约(必须统一)

  ### 7.1 URL 与版本

  - 前缀：/api/v1
  - 资源命名：名词复数：/users、/orders
  - 动作型：放子资源：POST /auth/login、POST /users/{id}/reset-password

  ### 7.2 统一响应体

  - 成功：

  { "code": 0, "message": "ok", "data": {}, "requestId": "..." }

  - 失败：

  { "code": 2001, "message": "USER_NOT_FOUND", "data": null, "requestId": "..." }

  ### 7.3 分页规范（推荐）

  - 请求：GET /xxx?page=1&pageSize=20&sort=id,desc
  - 响应 data：

  { "list": [], "page": 1, "pageSize": 20, "total": 100 }

  - 必须稳定排序（如 id desc），禁止无排序分页。

  ### 7.4 错误码分段（示例）

  - 0：成功
  - 1xxx：通用参数/系统（1001 参数错误、1002 资源不存在、1003 状态冲突）
  - 2xxx：鉴权/认证（2001 未登录、2002 Token 过期、2003 无权限）
  - 3xxx：用户域
  - 4xxx：订单域
    要求：错误码在 docs/error-codes.md 维护，前后端对齐。

## 8. 文档规范
- docs/ 内至少包含：
    - api.md：接口说明（Swagger）
    - db.md：表结构与变更记录
    - deploy.md：部署与回滚
    - runbook.md：常见故障处理
- 后端接口建议使用 OpenAPI：接口、模型、错误码统一对齐 
