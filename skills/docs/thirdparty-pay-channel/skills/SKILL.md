---
name: thirdparty-pay-channel
description: 专业的支付渠道第三方集成开发技能，提供支付渠道处理类的快速生成、最佳实践指南、安全验证和代码模板。支持代收(Recharge)、代付(Withdraw)、余额查询等功能模块的标准化开发，包含签名验证、加密解密、银行映射等常用工具类。用于开发新的支付渠道集成、重构现有支付代码、支付安全审计、支付接口测试等场景。
---

# 支付渠道第三方集成开发技能

## 快速开始

### 创建新的支付渠道处理类
```bash
# 使用代码生成脚本
python scripts/generate_payment_handler.py --channel-name NewPay --channel-code 1270 --support-recharge --support-withdraw --auth-type sign
```

### 验证现有支付代码
```bash
# 代码质量检查
python scripts/validate_payment_handler.py --file Pay1270.java
```

## 支付渠道类型

### 认证方式分类
- **MD5签名认证**：MD5 + 私钥拼接 (如：Pay1262, Pay1266)
- **SHA256+MD5双重签名**：SHA256加密后再MD5 + 私钥 (如：Pay1269)
- **HMAC-SHA256签名**：HMAC-SHA256 + Base64 (如：Pay1260)
- **HMAC-SHA1签名**：HMAC-SHA1 + Base64 (如：Pay1271)
- **Token认证**：Bearer Token (如：Pay1260)
- **简化MD5签名**：订单号+私钥简单组合 (如：Pay1265)
- **AES加密**：AES/CBC/PKCS5Padding (如：Pay1255)
- **无认证**：直接API调用 (如：Pay1265余额查询)

### 功能支持分类
- **代收Only**：仅支持充值 (如：Pay1265)
- **代付Only**：仅支持提现 (如：Pay1268)
- **全功能**：支持代收+代付+余额查询 (如：Pay1256, Pay1266)

## 核心组件开发指南

### 1. PaymentConfig 配置
```java
private static final PaymentConfig PAYMENT_CONFIG = PaymentConfig.builder()
    .rechargeApiPath("/api/deposit")           // 代收API路径
    .rechargeQueryApiPath("/api/deposit/info")  // 代收查询API路径
    .rechargeNotifyPrint("success")             // 代收回调响应
    .queryBalanceApiPath("/api/balance")        // 余额查询API路径
    .withdrawApiPath("/api/withdraw")           // 代付API路径
    .withdrawNotifyPrint("success")             // 代付回调响应
    .jumpMode(JumpMode.REDIRECT)                // 跳转模式
    .build();
```

### 2. 签名生成模式

#### MD5签名 (最常用)
```java
private String generateSign(String functionName, TreeMap<String, Object> sortedMap, String privateKey) {
    String queryString = paymentUtils.toUrlQueryEncodedString(sortedMap, StringPool.AMPERSAND);
    String textToBeSigned = queryString + SIGN_SUFFIX_WITH_API_KEY + privateKey;
    String sign = DigestUtils.md5Hex(textToBeSigned);
    return sign.toUpperCase(); // 或小写，根据三方要求
}
```

#### MD5 + 转大写签名 (Pay1266)
```java
private String generateSign(String functionName, TreeMap<String, Object> parameters, String signKey) {
    String textToBeSigned = paymentUtils.convertMapToQueryStringIgnoreEmpty(parameters, StringPool.AMPERSAND)
        + SIGN_SUFFIX_WITH_API_KEY + signKey;

    String sign = DigestUtils.md5Hex(textToBeSigned);
    return sign.toUpperCase(); // 必须转大写
}
```

#### 简化MD5签名 (Pay1265)
```java
private String generateSimpleSign(String orderNo, String privateKey) {
    String signSource = orderNo + privateKey;
    return DigestUtils.md5Hex(signSource);
}
```

#### SHA256+MD5双重签名 (高安全)
```java
private String generateSign(String functionName, Map<String, Object> parameters, String signKey, Set<String> excludedKeys) {
    // 1. 排除指定字段
    Map<String, Object> needSignParamMap = new TreeMap<>(parameters);
    for (String exclude : excludedKeys) {
        needSignParamMap.remove(exclude);
    }

    // 2. 组合参数+私钥
    String textToBeSigned = paymentUtils.convertToQueryString(needSignParamMap) + signKey;

    // 3. SHA256然后MD5
    String sha256Hex = DigestUtils.sha256Hex(textToBeSigned);
    String signUpperCase = DigestUtils.md5Hex(sha256Hex).toUpperCase();

    return signUpperCase;
}
```

#### HMAC-SHA256签名 (Webhook)
```java
private boolean isValidHmacSign(String functionName, NotifyDto notify, String signKey) {
    String webhookId = notify.getHeaders().get("webhook-id");
    String webhookTimestamp = notify.getHeaders().get("webhook-timestamp");
    String webhookSignature = notify.getHeaders().get("webhook-signature");
    String rawBody = notify.getRawBodyString();

    String textToBeSigned = webhookId + "." + webhookTimestamp + "." + rawBody;
    byte[] hmacBytes = new HmacUtils(HmacAlgorithms.HMAC_SHA_256, signKey.getBytes())
        .hmac(textToBeSigned.getBytes(StandardCharsets.UTF_8));

    String ourSignature = Base64.getEncoder().encodeToString(hmacBytes);
    return verifySignature(webhookSignature, ourSignature);
}
```

#### HMAC-SHA1 + Base64签名 (Pay1271)
```java
private String generateSignature(String secretKey, Map<String, Object> params) {
    // 1. 过滤空值并按key排序（字典序）
    TreeMap<String, Object> sortedParams = buildSignParams(params);

    // 2. 拼接成键值对字符串
    String stringA = paymentUtils.convertToQueryString(sortedParams);

    // 3. HMAC-SHA1加密
    HmacUtils hmacUtils = new HmacUtils(HmacAlgorithms.HMAC_SHA_1,
        secretKey.getBytes(StandardCharsets.UTF_8));
    byte[] bytes = hmacUtils.hmac(stringA.getBytes(StandardCharsets.UTF_8));

    // 4. Base64编码
    return Base64.getEncoder().encodeToString(bytes);
}

private TreeMap<String, Object> buildSignParams(Map<String, Object> params) {
    TreeMap<String, Object> signParams = new TreeMap<>();
    if (params != null) {
        for (Map.Entry<String, Object> entry : params.entrySet()) {
            String key = entry.getKey();
            Object value = entry.getValue();
            // 过滤空值和sign字段
            if (value != null && StringUtils.isNotBlank(value.toString()) && !"sign".equals(key)) {
                signParams.put(key, value);
            }
        }
    }
    return signParams;
}
```

### 3. 银行名称映射
```java
private static final Map<String, String> BANK_NAME_MAPPING = Map.of(
    "004", "臺灣銀行",
    "005", "土地銀行",
    "006", "合庫商銀",
    "007", "第一銀行",
    "008", "華南銀行"
    // ... 更多银行映射
);

private String getThirdPartyBankName(String bankCode) {
    return BANK_NAME_MAPPING.getOrDefault(bankCode, "提現不支援的銀行");
}
```

### 4. 多国家支付配置 (Pay1271)
```java
/**
 * 代收国家配置
 */
private enum Pay1271RechargeCountry {
    THAILAND("THAILAND", "泰國") {
        @Override
        public void validateAndSetParams(Map<String, Object> params) {
            validateRequired(params, "bank_name", "card_no", "card_name");
        }
    },
    NEPAL("NEPAL", "尼泊爾") {
        @Override
        public void validateAndSetParams(Map<String, Object> params) {
            validateRequired(params, "card_no", "card_name");
        }
    },
    PAKISTAN("PAKISTAN", "巴基斯坦") {
        @Override
        public void validateAndSetParams(Map<String, Object> params) {
            validateRequired(params, "card_no");
            // 巴基斯坦：card_no=手機號碼
            String cardNo = (String) params.get("card_no");
            if (!isValidPhoneNumber(cardNo)) {
                throw new IllegalArgumentException("巴基斯坦支付需要有效手機號碼");
            }
        }
    };

    private final String code;
    private final String description;

    public abstract void validateAndSetParams(Map<String, Object> params);

    protected void validateRequired(Map<String, Object> params, String... fields) {
        for (String field : fields) {
            if (!params.containsKey(field) || params.get(field) == null ||
                StringUtils.isBlank(params.get(field).toString())) {
                throw new IllegalArgumentException("字段 " + field + " 不能為空");
            }
        }
    }

    public static Pay1271RechargeCountry fromCurrency(String currency) {
        if (currency.startsWith("THB")) {
            return THAILAND;
        }
        return DEFAULT;
    }
}
```

### 5. 多支付通道支持 (Pay1265)
```java
/**
 * 支付通道配置
 */
private enum Pay1265PayChannel {
    EZ_PAY("ezpay", "/api/ezpay_order_create"),      // EZ Pay通道
    ALI_PAY("alipay", "/api/alipay_order_create");  // 支付宝通道

    private final String channel;
    private final String apiUrl;

    public static Pay1265PayChannel fromDynamicColumnPayChannel(String payChannel) {
        return Arrays.stream(values())
            .filter(t -> t.channel.equals(payChannel))
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Invalid pay channel: " + payChannel));
    }
}

/**
 * 代收支付类型配置
 */
private enum Pay1265RechargeType {
    CREDIT_CARD("credit"),  // 信用卡
    ATM("atm"),            // 虚拟账号、支付宝
    CVS("cvs");            // 超商代码

    private final String type;

    public static Pay1265RechargeType fromRechargeMerchantThirdPartyCode(String code) {
        return Arrays.stream(values())
            .filter(t -> t.getType().equals(code))
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Invalid recharge type: " + code));
    }
}
```

### 6. 台湾手机号格式转换
```java
/**
 * 转换为台湾手机号格式
 */
private String toTaiwanPhoneNumber(String countryCode, String telephone) {
    return Objects.equals(countryCode, "886") ? "0" + telephone : telephone;
}

// 使用示例
String taiwanPhone = toTaiwanPhoneNumber("886", "912345678"); // 结果: "0912345678"
```

### 7. 订单号格式转换 (Pay1262)
```java
/**
 * 代付订单号格式转换：我方使用底线(-)，三方只支持下划线(_)
 */
@Override
public Map<String, Object> generateWithdrawRequest(WithdrawParameterDto dto) throws JsonProcessingException {
    // 订单号格式转换
    String convertedOrderNo = dto.getOrderSubId().replaceAll(StringPool.DASH, StringPool.UNDERSCORE);

    TreeMap<String, Object> sortedMap = new TreeMap<>();
    sortedMap.put("agent", dto.getChannelMerchantAccountVo().getMerchantCode());
    sortedMap.put("order_sn", convertedOrderNo); // 转换为下划线格式
    // ... 其他参数
}

/**
 * 代付回调订单号还原
 */
@Override
public WithdrawNotifyResult handleWithdrawNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
    Map<String, String> params = notify.getParameters();
    String callbackOrderNo = params.get("order_sn");
    // 还原订单号格式：下划线转底线
    String originalOrderNo = callbackOrderNo.replaceAll(StringPool.UNDERSCORE, StringPool.DASH);

    // ... 业务处理
}
```

### 8. 随机数防重放攻击 (Pay1266)
```java
/**
 * 余额查询使用随机数防止重放攻击
 */
@Override
public Map<String, Object> generateQueryBalanceRequest(ChannelMerchantAccountEntity channelMerchantAccountEntity) {
    TreeMap<String, Object> sortedMap = new TreeMap<>();
    sortedMap.put("appId", channelMerchantAccountEntity.getMerchantCode());
    // 使用雪花算法生成唯一随机数
    sortedMap.put("random", String.valueOf(uidGenerator.getUID()));

    String signature = this.generateSign("商戶餘額請求", sortedMap, channelMerchantAccountEntity.getPrivateKey());
    sortedMap.put("sign", signature);

    return sortedMap;
}
```

### 9. 特殊回调响应格式
```java
/**
 * 不同三方的回调响应格式要求
 */
@Override
public ResponseEntity<String> responseRechargeNotify() {
    return ResponseEntity.ok(this.getConfig().getRechargeNotifyPrint());
}

// 配置示例：
// Pay1260: "anythingIsFine"
// Pay1262: "OK"
// Pay1265: "success"
// Pay1266: "SUCCESS"
// Pay1269: "success"
// Pay1271: "ok"
```

### 10. AES加密解密
```java
public static String decrypt(String doubleBase64Cipher, String secretKey, String secretIv) throws Exception {
    byte[] key = deriveKey(secretKey);    // 32 bytes
    byte[] iv  = deriveIv(secretIv);      // 16 bytes

    byte[] innerB64Bytes = Base64.getDecoder().decode(doubleBase64Cipher);
    String innerB64 = new String(innerB64Bytes, StandardCharsets.UTF_8);
    byte[] raw = Base64.getDecoder().decode(innerB64);

    Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
    cipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(key, "AES"), new IvParameterSpec(iv));
    byte[] plain = cipher.doFinal(raw);
    return new String(plain, StandardCharsets.UTF_8);
}
```

## 错误处理最佳实践

### 1. 响应处理
```java
@Override
public void handleWithdrawResponse(String response, WithdrawResultVo withdrawResultVo) throws Exception {
    log.info("{}[代付回應] response: {}", LOG_PREFIX, response);
    Map<String, Object> resBody = objectMapper.readValue(response, new TypeReference<>() {});

    String code = String.valueOf(resBody.get("code"));
    boolean isSuccess = SUCCESS_RESPONSE_CODE.equals(code);
    withdrawResultVo.setIsSuccess(isSuccess);

    if (!isSuccess) {
        withdrawResultVo.setRespCode(code);
        withdrawResultVo.setResData(String.valueOf(resBody.get("data"))); // 保存错误详情
        withdrawResultVo.setRespMessage(String.valueOf(resBody.get("msg")));
    }
}
```

### 2. 异常处理
```java
@Override
public RechargeNotifyResult handleRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
    try {
        // 业务逻辑
        return NotifyResultUtils.rechargeNotifySuccess(callbackOrderNo, amount, fee);
    } catch (Exception e) {
        log.error("{}[代收回調處理] 失败", LOG_PREFIX, e);
        return NotifyResultUtils.rechargeNotifyFail(notify.getOrderId(), "代收失敗解析錯誤: " + e.getMessage());
    }
}
```

## 安全性检查清单

### 必须验证项目
- [ ] 签名验证逻辑正确性
- [ ] 金额精度处理（整数/小数位数）
- [ ] 订单号重复检查
- [ ] 回调IP白名单（如果支持）
- [ ] 敏感信息日志脱敏
- [ ] SQL注入防护
- [ ] 超时设置

### 推荐安全措施
- [ ] 使用枚举定义状态码和常量
- [ ] 参数验证和边界检查
- [ ] 异常信息不暴露内部错误
- [ ] 重试机制和幂等性设计
- [ ] 监控和告警设置

## 常见问题解决

### Q: 如何处理三方回调格式不统一？
A: 使用适配器模式，创建统一的回调处理接口，不同的三方实现各自的解析逻辑。

### Q: 签名验证失败怎么办？
A: 检查参数排序、编码格式、大小写、空值处理等细节，使用调试日志输出中间结果。

### Q: 如何处理银行代码映射？
A: 创建统一的银行代码映射表，支持三方不同银行代码的转换。

### Q: Webhook签名验证复杂怎么办？(Pay1260)
A: 需要从HTTP头提取webhook-id、webhook-timestamp、webhook-signature，然后使用"{webhook-id}.{webhook-timestamp}.{rawBody}"格式进行HMAC-SHA256+Base64签名验证。

### Q: 订单号格式不匹配如何处理？(Pay1262)
A: 在请求时将底线(-)转换为下划线(_)，回调时再将下划线还原为底线，确保订单号的双向正确转换。

### Q: 多国家支付字段要求不同如何处理？(Pay1271)
A: 使用国家配置枚举，为不同国家定义专门的字段验证逻辑，如泰国需要bank_name/card_no/card_name，巴基斯坦需要手机号码格式的card_no。

### Q: 回调签名只验证data字段怎么办？(Pay1271)
A: 代收和代付回调都只对data中的字段进行签名验证，不包括外层的code、message等字段。需要构建只包含data字段的参数Map进行签名。

### Q: 如何处理多签名版本验证？(Pay1260)
A: webhook-signature可能包含多个签名，需要分割后逐一比对，只要有一个匹配即可通过验证。

### Q: 支付通道动态选择如何实现？(Pay1265)
A: 根据配置动态选择不同的API端点，如EZ Pay和支付宝通道对应不同的API路径，通过枚举管理通道配置。

### Q: SHA256+MD5双重签名如何实现？(Pay1269)
A: 先对参数+私钥进行SHA256加密，再对结果进行MD5加密并转大写，支持动态排除字段配置。

## 测试模板

### 单元测试示例
```java
@Test
void testGenerateSign() {
    // Given
    TreeMap<String, Object> params = new TreeMap<>();
    params.put("amount", "1000");
    params.put("orderNo", "TEST001");

    // When
    String sign = paymentHandler.generateSign("测试", params, "testKey");

    // Then
    assertThat(sign).isNotEmpty();
    assertThat(sign).hasSize(32); // MD5 length
}
```

### 集成测试示例
```java
@Test
void testWithdrawFlow() {
    // 模拟完整的代付流程
    WithdrawParameterDto dto = createMockWithdrawDto();
    Map<String, Object> request = paymentHandler.generateWithdrawRequest(dto);
    String response = paymentHandler.doWithdrawApi(testUrl, request, dto.getChannelMerchantAccountVo());

    WithdrawResultVo resultVo = new WithdrawResultVo();
    paymentHandler.handleWithdrawResponse(response, resultVo);

    assertThat(resultVo.getIsSuccess()).isTrue();
}
```

## 参考资源

- **完整API文档**：见 [references/api_documentation.md](references/api_documentation.md)
- **安全指南**：见 [references/security_guide.md](references/security_guide.md)
- **错误代码表**：见 [references/error_codes.md](references/error_codes.md)
- **银行代码映射**：见 [assets/bank_mappings.json](assets/bank_mappings.json)
- **代码模板**：见 [assets/templates/](assets/templates/)