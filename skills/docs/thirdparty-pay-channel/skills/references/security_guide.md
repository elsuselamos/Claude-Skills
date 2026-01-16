# 支付渠道安全开发指南

## 安全开发原则

### 1. 最小权限原则
- 只请求和存储必要的用户信息
- 使用最小权限的API密钥
- 限制回调URL的可访问性

### 2. 深度防御原则
- 多层验证机制（签名+时间戳+IP白名单）
- 关键操作的二次确认
- 异常情况的详细监控

### 3. 数据保护原则
- 敏感数据加密存储
- 传输过程使用HTTPS
- 日志中避免记录敏感信息

## 签名安全

### 签名算法选择

#### 推荐的签名算法（按安全等级排序）
1. **HMAC-SHA256** - 最高安全级别
2. **SHA256 + Salt** - 高安全级别
3. **MD5 + Salt** - 中等安全级别（不推荐用于新系统）
4. **MD5** - 基础安全级别（仅用于兼容老系统）

#### HMAC-SHA256实现
```java
private String generateHmacSha256Sign(String data, String secretKey) {
    try {
        Mac hmacSha256 = Mac.getInstance("HmacSHA256");
        SecretKeySpec secretKeySpec = new SecretKeySpec(secretKey.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
        hmacSha256.init(secretKeySpec);
        byte[] signedBytes = hmacSha256.doFinal(data.getBytes(StandardCharsets.UTF_8));
        return Hex.encodeHexString(signedBytes);
    } catch (Exception e) {
        throw new RuntimeException("HMAC-SHA256签名失败", e);
    }
}
```

### 签名验证最佳实践

#### 1. 参数标准化
```java
private Map<String, String> normalizeParams(Map<String, String> params) {
    Map<String, String> normalized = new TreeMap<>();

    for (Map.Entry<String, String> entry : params.entrySet()) {
        String key = entry.getKey().trim();
        String value = StringUtils.defaultString(entry.getValue()).trim();

        // 跳过空值和签名参数
        if (!"sign".equals(key) && StringUtils.isNotEmpty(value)) {
            normalized.put(key, value);
        }
    }

    return normalized;
}
```

#### 2. 时间戳验证
```java
private boolean validateTimestamp(String timestamp) {
    try {
        long ts = Long.parseLong(timestamp);
        long now = System.currentTimeMillis() / 1000;

        // 允许5分钟的时间差
        return Math.abs(now - ts) <= 300;
    } catch (NumberFormatException e) {
        return false;
    }
}
```

#### 3. 完整签名验证流程
```java
public boolean isValidSign(String functionName, Map<String, String> callbackParams, String privateKey) {
    try {
        // 1. 提取签名
        String thirdPartySign = callbackParams.remove("sign");
        if (StringUtils.isEmpty(thirdPartySign)) {
            log.warn("{}[{}] 缺少签名参数", LOG_PREFIX, functionName);
            return false;
        }

        // 2. 标准化参数
        TreeMap<String, Object> normalizedParams = new TreeMap<>(callbackParams);

        // 3. 验证必要字段
        if (!validateRequiredFields(normalizedParams)) {
            return false;
        }

        // 4. 验证时间戳
        String timestamp = String.valueOf(normalizedParams.get("timestamp"));
        if (!validateTimestamp(timestamp)) {
            log.warn("{}[{}] 时间戳验证失败", LOG_PREFIX, functionName);
            return false;
        }

        // 5. 生成我方签名
        String ourSign = generateSign(functionName, normalizedParams, privateKey);

        // 6. 比较签名（使用常量时间比较防止时序攻击）
        return MessageDigest.isEqual(
            thirdPartySign.getBytes(StandardCharsets.UTF_8),
            ourSign.getBytes(StandardCharsets.UTF_8)
        );

    } catch (Exception e) {
        log.error("{}[{}] 签名验证异常", LOG_PREFIX, functionName, e);
        return false;
    }
}
```

## 数据加密

### AES加密实现

#### 推荐的AES配置
- **算法**: AES/CBC/PKCS5Padding
- **密钥长度**: 256位 (32字节)
- **IV长度**: 128位 (16字节)
- **编码**: Base64

#### 安全的密钥派生
```java
private static byte[] deriveKey(String secretKey) throws Exception {
    // 使用SHA-256生成256位密钥
    MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
    byte[] hash = sha256.digest(secretKey.getBytes(StandardCharsets.UTF_8));
    return Arrays.copyOf(hash, 32); // 32 bytes = 256 bits
}

private static byte[] deriveIv(String secretIv) throws Exception {
    // 使用SHA-256生成128位IV
    MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
    byte[] hash = sha256.digest(secretIv.getBytes(StandardCharsets.UTF_8));
    return Arrays.copyOf(hash, 16); // 16 bytes = 128 bits
}
```

#### 安全的AES实现
```java
public static String encrypt(String plaintext, String secretKey, String secretIv) throws Exception {
    try {
        // 1. 密钥派生
        byte[] key = deriveKey(secretKey);
        byte[] iv = deriveIv(secretIv);

        // 2. 初始化Cipher
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key, "AES"), new IvParameterSpec(iv));

        // 3. 加密
        byte[] encrypted = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));

        // 4. Base64编码
        return Base64.getEncoder().encodeToString(encrypted);

    } catch (Exception e) {
        throw new RuntimeException("AES加密失败", e);
    }
}

public static String decrypt(String ciphertext, String secretKey, String secretIv) throws Exception {
    try {
        // 1. 密钥派生
        byte[] key = deriveKey(secretKey);
        byte[] iv = deriveIv(secretIv);

        // 2. Base64解码
        byte[] encrypted = Base64.getDecoder().decode(ciphertext);

        // 3. 初始化Cipher
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(key, "AES"), new IvParameterSpec(iv));

        // 4. 解密
        byte[] decrypted = cipher.doFinal(encrypted);

        return new String(decrypted, StandardCharsets.UTF_8);

    } catch (Exception e) {
        throw new RuntimeException("AES解密失败", e);
    }
}
```

## API安全

### HTTPS配置
```java
// 配置SSL验证
private CloseableHttpClient createSecureHttpClient() {
    try {
        SSLContext sslContext = SSLContextBuilder.create()
            .loadTrustMaterial(new TrustSelfSignedStrategy())
            .build();

        SSLConnectionSocketFactory sslSocketFactory = SSLConnectionSocketFactoryBuilder.create()
            .setSSLContext(sslContext)
            .setHostnameVerifier(NoopHostnameVerifier.INSTANCE)
            .build();

        return HttpClients.custom()
            .setSSLSocketFactory(sslSocketFactory)
            .build();

    } catch (Exception e) {
        throw new RuntimeException("创建安全HTTP客户端失败", e);
    }
}
```

### 请求头安全
```java
private Map<String, String> getSecureHeaders(String authToken) {
    Map<String, String> headers = new HashMap<>();
    headers.put(CONTENT_TYPE, APPLICATION_JSON_VALUE);
    headers.put(AUTHORIZATION, "Bearer " + authToken);
    headers.put("X-Request-ID", UUID.randomUUID().toString());
    headers.put("User-Agent", "PaymentService/1.0");
    return headers;
}
```

### 请求限流
```java
// 使用Redis实现分布式限流
private boolean checkRateLimit(String merchantId, int maxRequests, int timeWindowSeconds) {
    String key = "rate_limit:" + merchantId;

    // 使用滑动窗口算法
    Long currentCount = redisTemplate.opsForValue().increment(key);

    if (currentCount == 1) {
        redisTemplate.expire(key, timeWindowSeconds, TimeUnit.SECONDS);
    }

    return currentCount <= maxRequests;
}
```

## 数据库安全

### 敏感数据存储

#### 加密存储示例
```java
@Entity
public class ChannelMerchantAccountEntity {

    @Convert(converter = EncryptedStringConverter.class)
    private String privateKey;

    @Convert(converter = EncryptedStringConverter.class)
    private String publicKey;

    // 转换器实现
    @Converter
    public static class EncryptedStringConverter implements AttributeConverter<String, String> {
        @Override
        public String convertToDatabaseColumn(String attribute) {
            if (attribute == null) return null;
            try {
                return AESUtil.encrypt(attribute, getDatabaseKey());
            } catch (Exception e) {
                throw new RuntimeException("数据库字段加密失败", e);
            }
        }

        @Override
        public String convertToEntityAttribute(String dbData) {
            if (dbData == null) return null;
            try {
                return AESUtil.decrypt(dbData, getDatabaseKey());
            } catch (Exception e) {
                throw new RuntimeException("数据库字段解密失败", e);
            }
        }
    }
}
```

#### SQL注入防护
```java
// 使用参数化查询
@Query("SELECT p FROM PaymentOrder p WHERE p.orderId = :orderId AND p.merchantId = :merchantId")
PaymentOrder findByOrderIdAndMerchantId(@Param("orderId") String orderId, @Param("merchantId") String merchantId);

// 避免字符串拼接
// 错误示例：WHERE order_id = '" + orderId + "'"
// 正确示例：WHERE order_id = :orderId
```

## 日志安全

### 敏感信息脱敏
```java
public class SensitiveDataUtils {

    public static String maskCardNumber(String cardNumber) {
        if (StringUtils.isEmpty(cardNumber) || cardNumber.length() < 8) {
            return "****";
        }
        int length = cardNumber.length();
        return cardNumber.substring(0, 4) + "****" + cardNumber.substring(length - 4);
    }

    public static String maskBankAccount(String account) {
        if (StringUtils.isEmpty(account) || account.length() < 6) {
            return "****";
        }
        return account.substring(0, 3) + "****" + account.substring(account.length() - 3);
    }

    public static String maskName(String name) {
        if (StringUtils.isEmpty(name) || name.length() <= 1) {
            return "*";
        }
        return name.charAt(0) + "*".repeat(name.length() - 1);
    }
}
```

### 安全日志记录
```java
@Override
public Map<String, Object> generateWithdrawRequest(WithdrawParameterDto dto) {
    log.info("{}[代付请求] 订单号: {}, 金额: {}, 收款人: {}, 银行账号: {}",
        LOG_PREFIX,
        dto.getOrderSubId(),
        dto.getAmount(),
        SensitiveDataUtils.maskName(dto.getName()),
        SensitiveDataUtils.maskBankAccount(dto.getCardNo())
    );

    // ... 业务逻辑
}
```

## 异常处理安全

### 异常信息脱敏
```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception e) {
        // 记录详细错误到日志
        log.error("系统异常", e);

        // 返回给客户端的通用错误信息
        ErrorResponse errorResponse = new ErrorResponse();
        errorResponse.setCode("SYSTEM_ERROR");
        errorResponse.setMessage("系统处理异常，请稍后重试");

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(errorResponse);
    }
}
```

### 业务异常处理
```java
public class PaymentException extends RuntimeException {
    private final String errorCode;
    private final boolean isSensitive;

    // 构造函数和getter方法
}

// 在处理时
try {
    // 支付处理逻辑
} catch (PaymentException e) {
    log.warn("{}[{}] 支付异常: {}", LOG_PREFIX, functionName, e.getErrorCode());

    if (e.isSensitive()) {
        // 敏感异常不暴露给外部
        throw new PaymentException("PAYMENT_FAILED", false);
    } else {
        throw e;
    }
}
```

## 安全监控

### 安全事件监控
```java
@Component
public class SecurityEventMonitor {

    @EventListener
    public void handleSignVerificationFailure(SignVerificationFailureEvent event) {
        // 记录签名验证失败
        log.warn("签名验证失败 - IP: {}, 商户: {}, 时间: {}, 参数: {}",
            event.getClientIp(),
            event.getMerchantId(),
            event.getTimestamp(),
            event.getRequestParams()
        );

        // 检查是否为攻击模式
        checkAttackPattern(event);
    }

    private void checkAttackPattern(SignVerificationFailureEvent event) {
        String ip = event.getClientIp();
        String key = "failed_sign_attempts:" + ip;

        Long attempts = redisTemplate.opsForValue().increment(key);
        redisTemplate.expire(key, 3600, TimeUnit.SECONDS); // 1小时窗口

        // 如果失败次数过多，加入黑名单
        if (attempts > 10) {
            addToBlacklist(ip, "签名验证失败次数过多");
        }
    }
}
```

### 关键操作审计
```java
@Aspect
@Component
public class PaymentAuditAspect {

    @Around("@annotation(PaymentOperation)")
    public Object auditPaymentOperation(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();

        // 记录操作前状态
        String auditId = UUID.randomUUID().toString();
        log.info("审计ID: {}, 操作开始: {}, 参数: {}", auditId, methodName, maskSensitiveArgs(args));

        try {
            Object result = joinPoint.proceed();

            // 记录操作成功
            log.info("审计ID: {}, 操作成功: {}", auditId, methodName);
            return result;

        } catch (Exception e) {
            // 记录操作失败
            log.error("审计ID: {}, 操作失败: {}, 错误: {}", auditId, methodName, e.getMessage());
            throw e;
        }
    }

    private Object maskSensitiveArgs(Object[] args) {
        // 脱敏处理逻辑
        return Arrays.stream(args)
            .map(arg -> {
                if (arg instanceof WithdrawParameterDto) {
                    WithdrawParameterDto dto = (WithdrawParameterDto) arg;
                    return dto.toBuilder()
                        .cardNo(SensitiveDataUtils.maskBankAccount(dto.getCardNo()))
                        .name(SensitiveDataUtils.maskName(dto.getName()))
                        .build();
                }
                return arg;
            })
            .toArray();
    }
}
```

## 安全检查清单

### 开发阶段
- [ ] 所有API调用使用HTTPS
- [ ] 实现了签名验证机制
- [ ] 敏感数据加密存储
- [ ] 日志中敏感信息已脱敏
- [ ] 异常信息不暴露内部细节
- [ ] 实现了请求限流机制

### 测试阶段
- [ ] 签名伪造攻击测试
- [ ] 重放攻击测试
- [ ] SQL注入测试
- [ ] XSS攻击测试
- [ ] CSRF攻击测试
- [ ] 越权访问测试

### 部署阶段
- [ ] 配置了IP白名单
- [ ] 启用了安全监控
- [ ] 配置了告警机制
- [ ] 定期安全漏洞扫描
- [ ] 访问日志审计
- [ ] 密钥轮换策略

### 运维阶段
- [ ] 监控异常访问模式
- [ ] 定期更新安全补丁
- [ ] 备份和恢复测试
- [ ] 安全事件响应计划
- [ ] 员工安全培训
- [ ] 第三方安全评估