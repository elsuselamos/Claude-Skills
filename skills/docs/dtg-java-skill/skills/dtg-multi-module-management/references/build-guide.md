# 模块构建指南

## 部署顺序

1. xxpay-flyway - 数据库迁移
2. xxpay-service - 业务服务
3. xxpay-pay - 支付核心
4. xxpay-task - 定时任务
5. xxpay-manage - 运营平台
6. xxpay-agent - 代理商系统
7. xxpay-merchant - 商户系统

## 编译命令

```bash
# 首先编译核心模块
./mvnw -f xxpay-core clean install -Dmaven.test.skip=true

# 编译服务层
./mvnw -f xxpay-service clean package -Dmaven.test.skip=true

# 编译其他模块
./mvnw -f xxpay-pay clean package -Dmaven.test.skip=true
./mvnw -f xxpay-task clean package -Dmaven.test.skip=true
./mvnw -f xxpay-manage clean package -Dmaven.test.skip=true
./mvnw -f xxpay-agent clean package -Dmaven.test.skip=true
./mvnw -f xxpay-merchant clean package -Dmaven.test.skip=true
./mvnw -f xxpay-consumer clean package -Dmaven.test.skip=true
./mvnw -f rbgi clean package -Dmaven.test.skip=true
```

## 环境配置

### 环境
- `local` - 本地开发
- `dtg-stg` - 测试环境
- `dtg-prod` - 生产环境

### 关键环境变量

| 变量 | 说明 |
|------|------|
| `ZOOKEEPER` | Zookeeper 注册中心地址 |
| `DATASOURCE_URL` | MySQL 数据库地址 |
| `REDIS_HOST` | Redis 主机地址 |
| `ACTIVEMQ_BROKER` | ActiveMQ 消息代理地址 |
| `MONGODB_URI` | MongoDB 连接 URI |
| `NODE` | 服务节点标识 |

## 时区设置

项目统一使用 **Asia/Shanghai** 时区：
- **应用层**: `TimeZone.setDefault()`
- **Jackson**: `spring.jackson.time-zone: Asia/Shanghai`
- **数据库**: `serverTimezone=GMT%2B0`

## Git 提交规范

`EZPAY-xxx: 功能描述`

示例：
```
EZPAY-730: 计算功能优化
EZPAY-799: 优化支付通道页面
```
