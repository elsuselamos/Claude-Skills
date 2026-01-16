# 支付渠道错误代码参考

## 通用错误代码

### API调用错误 (1xxx)
| 错误代码 | 描述 | 解决方案 |
|---------|------|----------|
| 1001 | 网络连接超时 | 检查网络连接，增加超时时间 |
| 1002 | HTTP连接失败 | 检查URL配置和防火墙设置 |
| 1003 | 响应解析异常 | 验证三方API响应格式 |
| 1004 | SSL证书验证失败 | 检查证书配置和有效期 |
| 1005 | 请求频率过高 | 实现请求限流和重试机制 |

### 参数错误 (2xxx)
| 错误代码 | 描述 | 解决方案 |
|---------|------|----------|
| 2001 | 必填参数缺失 | 检查请求参数完整性 |
| 2002 | 参数格式错误 | 验证参数类型和格式 |
| 2003 | 参数值超出范围 | 检查参数取值范围 |
| 2004 | 商户信息无效 | 验证商户配置 |
| 2005 | 银行信息不匹配 | 检查银行代码和名称映射 |

### 签名验证错误 (3xxx)
| 错误代码 | 描述 | 解决方案 |
|---------|------|----------|
| 3001 | 签名验证失败 | 检查签名算法和密钥配置 |
| 3002 | 签名参数缺失 | 确认签名参数传递正确 |
| 3003 | 时间戳超时 | 调整时间窗口配置 |
| 3004 | 签名顺序错误 | 检查参数排序逻辑 |
| 3005 | 密钥格式错误 | 验证密钥编码格式 |

### 业务逻辑错误 (4xxx)
| 错误代码 | 描述 | 解决方案 |
|---------|------|----------|
| 4001 | 订单不存在 | 验证订单号有效性 |
| 4002 | 订单状态异常 | 检查订单状态流转 |
| 4003 | 重复订单请求 | 实现幂等性检查 |
| 4004 | 余额不足 | 提示用户充值或联系商户 |
| 4005 | 超出单笔限额 | 调整交易金额或申请提升限额 |

### 三方平台错误 (5xxx)
| 错误代码 | 描述 | 解决方案 |
|---------|------|----------|
| 5001 | 三方系统维护 | 暂停交易，等待恢复 |
| 5002 | 三方风控拦截 | 联系三方客服处理 |
| 5003 | 银行通道繁忙 | 稍后重试或更换通道 |
| 5004 | 三方余额不足 | 提示三方充值 |
| 5005 | 三方配置错误 | 联系技术支持处理 |

## 常见三方平台错误代码

### FP Pay (1256)
| 三方错误码 | 描述 | 我方处理 |
|-----------|------|----------|
| 0 | 成功 | 标记为成功 |
| 1001 | 商户不存在 | 返回商户配置错误 |
| 1002 | 签名错误 | 记录安全事件 |
| 2001 | 订单重复 | 返回重复订单错误 |
| 3001 | 余额不足 | 返回余额不足错误 |

### AUY Pay (1265, 1268)
| 三方错误码 | 描述 | 我方处理 |
|-----------|------|----------|
| success | 成功 | 标记为成功 |
| failed | 失败 | 记录失败原因 |
| insufficient_balance | 余额不足 | 返回余额不足错误 |
| invalid_bank | 银行不支持 | 提示更换银行 |

### SC Pay (1258, 1262)
| 三方错误码 | 描述 | 我方处理 |
|-----------|------|----------|
| 1 | 成功 | 标记为成功 |
| 1001 | 参数错误 | 返回参数错误 |
| 1002 | 签名错误 | 记录安全事件 |
| 2001 | 订单不存在 | 返回订单不存在错误 |

### 58 Pay (1266)
| 三方错误码 | 描述 | 我方处理 |
|-----------|------|----------|
| 1 | 成功 | 标记为成功 |
| 1001 | 商户号错误 | 返回商户配置错误 |
| 1002 | 签名验证失败 | 记录安全事件 |
| 2001 | 通道不可用 | 暂停该通道使用 |

### Tendoor Pay (1260)
| HTTP状态码 | 描述 | 我方处理 |
|-----------|------|----------|
| 200 | 成功 | 解析响应体处理 |
| 400 | 请求参数错误 | 返回参数错误 |
| 401 | 认证失败 | 检查Token配置 |
| 403 | 权限不足 | 联系三方开通权限 |
| 429 | 请求过频 | 实现限流机制 |

## 错误处理最佳实践

### 1. 错误分类处理
```java
public enum ErrorCategory {
    NETWORK_ERROR("网络错误", 1000),
    PARAMETER_ERROR("参数错误", 2000),
    SIGNATURE_ERROR("签名错误", 3000),
    BUSINESS_ERROR("业务错误", 4000),
    THIRD_PARTY_ERROR("三方错误", 5000);

    private final String description;
    private final int codePrefix;
}
```

### 2. 错误响应标准化
```java
@Data
@AllArgsConstructor
public class ErrorResponse {
    private String code;
    private String message;
    private String details;
    private long timestamp;

    public static ErrorResponse of(ErrorCategory category, String specificCode, String message) {
        return new ErrorResponse(
            category.getCodePrefix() + specificCode,
            category.getDescription() + ": " + message,
            message,
            System.currentTimeMillis()
        );
    }
}
```

### 3. 错误重试策略
```java
@Component
public class PaymentRetryService {

    @Retryable(
        value = {NetworkException.class, TemporaryServiceException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 1000, multiplier = 2)
    )
    public String doPaymentWithRetry(String url, Map<String, Object> params) {
        // 执行支付请求
        return httpUtil.doPostForEntity(url, params, headers).getBody();
    }

    @Recover
    public String recover(Exception ex, String url, Map<String, Object> params) {
        log.error("支付请求重试失败，最终失败", ex);
        throw new PermanentFailureException("支付请求最终失败", ex);
    }
}
```

### 4. 错误监控
```java
@Component
public class ErrorMonitorService {

    private final MeterRegistry meterRegistry;

    public void recordError(ErrorCategory category, String errorCode, String message) {
        // 记录错误指标
        meterRegistry.counter("payment.errors",
            "category", category.name(),
            "code", errorCode
        ).increment();

        // 记录错误日志
        log.error("支付错误 - 类别: {}, 代码: {}, 消息: {}",
            category.getDescription(), errorCode, message);

        // 关键错误告警
        if (isCriticalError(category, errorCode)) {
            sendAlert(category, errorCode, message);
        }
    }

    private boolean isCriticalError(ErrorCategory category, String errorCode) {
        return category == ErrorCategory.SIGNATURE_ERROR ||
               category == ErrorCategory.BUSINESS_ERROR;
    }

    private void sendAlert(ErrorCategory category, String errorCode, String message) {
        // 发送告警通知
        alertService.sendAlert(
            String.format("支付系统关键错误: %s - %s",
                category.getDescription(), errorCode),
            message
        );
    }
}
```

## 错误代码映射

### 我方错误码设计
```
格式: E + 业务线 + 错误类别 + 具体错误
示例: E10_3001
- E: 错误前缀
- 1: 支付业务线
- 0: 渠道类型
- 3001: 具体错误代码
```

### 错误映射配置
```java
@ConfigurationProperties(prefix = "payment.error-mapping")
@Data
public class ErrorMappingConfig {

    private Map<String, String> thirdPartyMapping = Map.of(
        // FP Pay映射
        "1256_0", "SUCCESS",
        "1256_1001", "E10_4004",
        "1256_1002", "E10_3001",

        // AUY Pay映射
        "1265_success", "SUCCESS",
        "1265_failed", "E10_4001",
        "1265_insufficient_balance", "E10_4004",

        // 通用映射
        "timeout", "E10_1001",
        "connection_failed", "E10_1002",
        "parse_error", "E10_1003"
    );
}
```

### 错误转换服务
```java
@Service
public class ErrorMappingService {

    private final ErrorMappingConfig errorMappingConfig;

    public String mapThirdPartyError(String channelId, String thirdPartyCode) {
        String mappingKey = channelId + "_" + thirdPartyCode;
        String mappedError = errorMappingConfig.getThirdPartyMapping().get(mappingKey);

        if (mappedError == null) {
            // 未知错误映射为通用三方错误
            mappedError = "E10_5000";
            log.warn("未知三方错误码: {}", mappingKey);
        }

        return mappedError;
    }

    public ErrorResponse createErrorResponse(String channelId, String thirdPartyCode, String message) {
        String ourErrorCode = mapThirdPartyError(channelId, thirdPartyCode);
        ErrorCategory category = determineErrorCategory(ourErrorCode);

        return ErrorResponse.of(category, ourErrorCode.substring(4), message);
    }

    private ErrorCategory determineErrorCategory(String errorCode) {
        int codePrefix = Integer.parseInt(errorCode.substring(4, 5));
        return Arrays.stream(ErrorCategory.values())
            .filter(category -> category.getCodePrefix() / 1000 == codePrefix)
            .findFirst()
            .orElse(ErrorCategory.THIRD_PARTY_ERROR);
    }
}
```

## 用户友好错误消息

### 代收错误消息
```java
public static final Map<String, String> RECHARGE_ERROR_MESSAGES = Map.of(
    "E10_2001", "支付信息不完整，请重新填写",
    "E10_2002", "支付信息格式错误，请检查后重试",
    "E10_3001", "支付验证失败，请重新尝试",
    "E10_4001", "订单已过期，请重新下单",
    "E10_4004", "账户余额不足，请充值后重试",
    "E10_5001", "支付系统维护中，请稍后重试"
);
```

### 代付错误消息
```java
public static final Map<String, String> WITHDRAW_ERROR_MESSAGES = Map.of(
    "E10_2001", "提现信息不完整，请重新填写",
    "E10_2002", "银行信息错误，请检查后重试",
    "E10_3001", "提现验证失败，请联系客服",
    "E10_4001", "提现订单不存在，请重新申请",
    "E10_4004", "商户余额不足，请充值后提现",
    "E10_5002", "银行通道繁忙，请稍后重试"
);
```

## 错误恢复策略

### 自动恢复场景
1. **网络超时**: 自动重试3次，指数退避
2. **三方维护**: 切换备用通道
3. **临时限流**: 延迟后重试
4. **余额检查**: 定时任务自动恢复

### 手动干预场景
1. **签名错误**: 需要技术支持检查配置
2. **权限问题**: 需要联系三方开通权限
3. **风控拦截**: 需要人工审核处理
4. **大额交易**: 需要人工确认

### 错误恢复通知
```java
@Service
public class ErrorRecoveryService {

    @EventListener
    public void handleErrorResolved(ErrorResolvedEvent event) {
        // 发送恢复通知
        notificationService.sendRecoveryNotification(
            event.getErrorType(),
            event.getRecoveryAction(),
            event.getAffectedOrders()
        );

        // 更新系统状态
        systemStatusService.updateComponentStatus(
            event.getComponentId(),
            ComponentStatus.NORMAL
        );
    }
}
```