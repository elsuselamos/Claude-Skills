# 支付渠道API文档参考

## 核心接口说明

### RechargeHandler 接口
代收（充值）处理接口，包含以下方法：

#### 必须实现的方法
- `PaymentConfig getConfig()` - 返回支付配置信息
- `Map<String, Object> generateRechargeRequest(RechargeParameterDto dto)` - 生成代收请求参数
- `String doRechargeApi(String url, Map<String, Object> params, RechargeParameterDto dto)` - 调用代收API
- `boolean handleRechargeResponse(String response, RechargeResult vo, RechargeParameterDto dto)` - 处理代收响应
- `RechargeNotifyResult handleRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account)` - 处理代收回调
- `ResponseEntity<String> responseRechargeNotify()` - 返回代收回调响应

#### 可选实现的方法
- `Map<String, Object> generateRechargeQueryRequest(RechargeParameterDto dto)` - 生成查询请求参数
- `String doRechargeQueryApi(String url, Map<String, Object> params, RechargeParameterDto dto)` - 调用查询API
- `boolean handleRechargeQueryResponse(String response, RechargeParameterDto dto)` - 处理查询响应
- `boolean isValidSignOfRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account)` - 验证代收回调签名

### WithdrawHandler 接口
代付（提现）处理接口，包含以下方法：

#### 必须实现的方法
- `PaymentConfig getConfig()` - 返回支付配置信息
- `Map<String, Object> generateWithdrawRequest(WithdrawParameterDto dto)` - 生成代付请求参数
- `String doWithdrawApi(String url, Map<String, Object> params, ChannelMerchantAccountVo vo)` - 调用代付API
- `void handleWithdrawResponse(String response, WithdrawResultVo withdrawResultVo)` - 处理代付响应
- `WithdrawNotifyResult handleWithdrawNotify(NotifyDto notify, ChannelMerchantAccountEntity account)` - 处理代付回调
- `ResponseEntity<String> responseWithdrawNotify()` - 返回代付回调响应

#### 可选实现的方法
- `boolean isValidSignOfWithdrawNotify(NotifyDto notify, ChannelMerchantAccountEntity account)` - 验证代付回调签名
- `Map<String, Object> generateQueryBalanceRequest(ChannelMerchantAccountEntity channelMerchantAccountEntity)` - 生成余额查询请求
- `String doQueryBalanceApi(String url, Map<String, Object> params, ChannelMerchantAccountEntity channelMerchantAccountEntity)` - 调用余额查询API
- `void handleQueryBalanceResponse(String response, ChannelMerchantAccountBalanceVo vo, ChannelMerchantAccountEntity channelMerchantAccountEntity)` - 处理余额查询响应

## PaymentConfig 配置详解

```java
private static final PaymentConfig PAYMENT_CONFIG = PaymentConfig.builder()
    .rechargeApiPath("/api/deposit")           // 代收API路径
    .rechargeQueryApiPath("/api/deposit/query")  // 代收查询API路径（可选）
    .rechargeNotifyPrint("success")             // 代收回调成功响应内容
    .queryBalanceApiPath("/api/balance")        // 余额查询API路径（可选）
    .withdrawApiPath("/api/withdraw")           // 代付API路径
    .withdrawNotifyPrint("success")             // 代付回调成功响应内容
    .jumpMode(JumpMode.REDIRECT)                // 支付跳转模式
    .build();
```

### 跳转模式说明
- `JumpMode.REDIRECT` - 重定向到支付页面
- `JumpMode.HTML` - 返回HTML内容供前端显示
- `JumpMode.IFRAME` - 在iframe中显示支付页面

## 认证方式详解

### 1. 签名认证 (Sign Authentication)

#### MD5签名
```java
private String generateSign(String functionName, TreeMap<String, Object> sortedMap, String privateKey) {
    // 1. 参数按字典序排序
    String queryString = paymentUtils.toUrlQueryEncodedString(sortedMap, StringPool.AMPERSAND);

    // 2. 拼接私钥
    String textToBeSigned = queryString + "&key=" + privateKey;

    // 3. MD5加密
    String sign = DigestUtils.md5Hex(textToBeSigned);

    // 4. 根据三方要求转换大小写
    return sign.toUpperCase(); // 或 toLowerCase()
}
```

#### SHA256+MD5双重签名
```java
private String generateSign(String functionName, Map<String, Object> parameters, String signKey, Set<String> excludedKeys) {
    // 1. 排除不需要签名的参数
    Map<String, Object> needSignParamMap = new TreeMap<>(parameters);
    for (String exclude : excludedKeys) {
        needSignParamMap.remove(exclude);
    }

    // 2. 组合参数+私钥
    String textToBeSigned = paymentUtils.convertToQueryString(needSignParamMap) + signKey;

    // 3. 先SHA256再MD5
    String sha256Hex = DigestUtils.sha256Hex(textToBeSigned);
    String signUpperCase = DigestUtils.md5Hex(sha256Hex).toUpperCase();

    return signUpperCase;
}
```

### 2. Token认证 (Token Authentication)

#### Bearer Token
```java
private Map<String, String> getApiHeaders(String bearerToken) {
    return Map.of(
        CONTENT_TYPE, APPLICATION_JSON_VALUE,
        AUTHORIZATION, BEARER + StringUtils.SPACE + bearerToken
    );
}
```

### 3. AES加密认证

#### AES/CBC/PKCS5Padding
```java
public static String decrypt(String doubleBase64Cipher, String secretKey, String secretIv) throws Exception {
    // 1. 密钥派生
    byte[] key = deriveKey(secretKey);    // 32 bytes
    byte[] iv  = deriveIv(secretIv);      // 16 bytes

    // 2. 双重Base64解码
    byte[] innerB64Bytes = Base64.getDecoder().decode(doubleBase64Cipher);
    String innerB64 = new String(innerB64Bytes, StandardCharsets.UTF_8);
    byte[] raw = Base64.getDecoder().decode(innerB64);

    // 3. AES解密
    Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
    cipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(key, "AES"), new IvParameterSpec(iv));
    byte[] plain = cipher.doFinal(raw);

    return new String(plain, StandardCharsets.UTF_8);
}
```

## 银行代码映射

### 台湾银行代码
```java
private static final Map<String, String> BANK_NAME_MAPPING = Map.of(
    "004", "臺灣銀行",
    "005", "土地銀行",
    "006", "合庫商銀",
    "007", "第一銀行",
    "008", "華南銀行",
    "009", "彰化銀行",
    "011", "上海銀行",
    "012", "台北富邦",
    "013", "國泰世華",
    // ... 更多银行代码
);
```

### 农渔会信用部
```java
// 示例：农会代码范围 500-999
bankNameMapping.put("501", "宜蘭縣蘇澳區漁會");
bankNameMapping.put("502", "宜蘭縣頭城區漁會");
bankNameMapping.put("538", "宜蘭市農會");
```

## 错误代码处理

### 常见响应状态
```java
// 成功状态
private static final String SUCCESS_RESPONSE_CODE = "0";      // API调用成功
private static final String SUCCESS_ORDER_STATUS = "SUCCESS"; // 订单成功状态

// 失败状态处理
if (!SUCCESS_RESPONSE_CODE.equals(code)) {
    withdrawResultVo.setRespCode(code);                    // 三方错误码
    withdrawResultVo.setRespMessage(String.valueOf(resBody.get("msg"))); // 错误消息
    withdrawResultVo.setResData(String.valueOf(resBody.get("data")));    // 详细错误信息
}
```

## 回调处理模式

### 1. 标准回调
```java
@Override
public RechargeNotifyResult handleRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
    Map<String, String> params = notify.getParameters();
    String callbackOrderNo = params.get("orderNo");
    String status = params.get("status");

    return SUCCESS_ORDER_STATUS.equals(status)
        ? NotifyResultUtils.rechargeNotifySuccess(callbackOrderNo, amount, fee)
        : NotifyResultUtils.rechargeNotifyFail(callbackOrderNo, "代收失败: " + status);
}
```

### 2. JSON Body回调
```java
@Override
public RechargeNotifyResult handleRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
    try {
        String rawBody = notify.getRawBodyString();
        Map<String, Object> requestBody = objectMapper.readValue(rawBody, new TypeReference<>() {});
        Map<String, String> data = objectMapper.convertValue(requestBody.get("data"), new TypeReference<>() {});

        // 处理data中的参数
        String callbackOrderNo = data.get("orderNo");
        String status = data.get("status");

        return handleOrderStatus(callbackOrderNo, status, data);
    } catch (Exception e) {
        log.error("解析回调失败", e);
        return NotifyResultUtils.rechargeNotifyFail(notify.getOrderId(), "解析错误: " + e.getMessage());
    }
}
```

### 3. 加密回调
```java
@Override
public RechargeNotifyResult handleRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
    String encrypted = notify.getParameters().get("data");

    // 解密
    Map<String, Object> decryptConfig = account.getDynamicColumnJson();
    String decrypted = decrypt(encrypted,
        decryptConfig.get("key").toString(),
        decryptConfig.get("iv").toString());

    // 解析JSON
    Map<String, String> data = objectMapper.readValue(decrypted, new TypeReference<>() {});

    return handleOrderStatus(data.get("orderNo"), data.get("status"), data);
}
```

## 安全最佳实践

### 1. 签名验证
- 始终验证回调签名
- 排除动态字段（如时间戳）不参与签名
- 记录签名验证过程用于调试

### 2. 参数验证
```java
// 金额验证
BigDecimal amount = new BigDecimal(params.get("amount"));
if (amount.compareTo(BigDecimal.ZERO) <= 0) {
    throw new IllegalArgumentException("金额必须大于0");
}

// 订单号验证
String orderNo = params.get("orderNo");
if (StringUtils.isEmpty(orderNo) || orderNo.length() > 64) {
    throw new IllegalArgumentException("订单号格式错误");
}
```

### 3. 防重放攻击
```java
// 检查时间戳
String timestamp = params.get("timestamp");
long currentTime = System.currentTimeMillis() / 1000;
long requestTime = Long.parseLong(timestamp);
if (Math.abs(currentTime - requestTime) > 300) { // 5分钟
    return false;
}

// 检查订单号是否已处理（在数据库层面实现）
```

### 4. 日志安全
```java
// 敏感信息脱敏
String maskedCardNo = dto.getCardNo().replaceAll("\\d(?=\\d{4})", "*");
log.info("处理代付请求，卡号: {}, 姓名: {}", maskedCardNo, dto.getName());

// 避免记录完整签名
log.info("签名验证结果: {}, 签名长度: {}", isValid, sign.length());
```