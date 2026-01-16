# xxpay-core 公共模块代码示例

## RPC 通信模型

### RpcBaseParam（RPC 调用入参基类）
```java
@Data
public class RpcBaseParam implements Serializable {

    /** 调用方 ID */
    private String rpcSrcSysId;

    /** 调用时间 */
    private String rpcDateTime;

    /** 随机通讯码 */
    private String rpcSeqNo;

    /** 签名方式 (0-明文, 1-SHA1) */
    private Integer rpcSignType;

    /** RPC 签名 (用于验证调用方合法性) */
    private String rpcSign;

    /** 业务流水号 (格式: 业务前缀+日期时间+6位流水号) */
    private String bizSeqNo;

    /** 业务签名 */
    private String bizSign;
}
```

### RpcBaseResult（RPC 返回值基类）
```java
@Data
public class RpcBaseResult extends RpcBaseParam implements Serializable {

    /** 返回码 (0000 表示成功) */
    private String rpcRetCode;

    /** 返回错误描述 */
    private String rpcRetMsg;

    /** 数据库错误信息 */
    private String dbErrorCode;

    /** 数据库错误消息 */
    private String dbErrorMsg;
}
```

## 返回码枚举

```java
public enum RetEnum {

    // 公共返回码 (10xxx)
    RET_COMM_SUCCESS("0000", "成功"),
    RET_COMM_FAIL("9999", "系统异常"),
    RET_COMM_OPERATE_FAIL("1001", "操作失败"),

    // 业务中心返回码 (11xxx)
    RET_SERVICE_SYSTEM_ERROR("1100", "系统错误"),

    // 商户系统返回码 (12xxx)
    RET_MCH_NOT_EXIST("1201", "商户不存在"),
    RET_MCH_STATE_STOP("1202", "商户已停用");

    private String code;
    private String message;
}
```

## 实体类示例

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@TableName("pay_order")
public class PayOrder {

    @TableId(type = IdType.INPUT)
    private String payOrderId;

    @TableField("mch_id")
    private String mchId;

    @TableField("amount")
    private Long amount;

    @TableField(value = "create_time", fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField(value = "update_time", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```

## 服务接口定义

```java
public interface IPayOrderService {

    /**
     * 根据支付订单号查询
     */
    PayOrder findByPayOrderId(String payOrderId);

    /**
     * 创建支付订单
     */
    int insert(PayOrder payOrder);

    /**
     * 更新支付订单
     */
    int update(PayOrder payOrder);
}
```

## 国际化支持

```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface I18n {
    /**
     * 国际化 key 前缀
     */
    String prefix() default "";
}

// 使用示例
public class MchInfo {
    @I18n(prefix = "mch.type")
    private Integer mchType;
}
```

## 异常处理

```java
public class ServiceException extends RuntimeException {

    private RetEnum retEnum;

    private String extraMsg;

    public ServiceException(RetEnum retEnum) {
        super(retEnum.getMessage());
        this.retEnum = retEnum;
    }

    public ServiceException(RetEnum retEnum, String extraMsg) {
        super(retEnum.getMessage() + ": " + extraMsg);
        this.retEnum = retEnum;
        this.extraMsg = extraMsg;
    }
}
```

## 常量定义

### MchConstant（商户相关常量）
```java
public class MchConstant {

    /** 商户状态 */
    public static final int MCH_STATUS_INIT = 0;
    public static final int MCH_STATUS_ACTIVE = 1;
    public static final int MCH_STATUS_STOP = 2;

    /** 业务类型 */
    public static final int MCH_BIZ_TYPE_PAY = 1;
    public static final int MCH_BIZ_TYPE_AGENTPAY = 2;

    /** 结算方式 */
    public static final int SETTLE_MODE_DAILY = 1;
    public static final int SETTLE_MODE_WEEKLY = 2;
    public static final int SETTLE_MODE_MANUAL = 3;
}
```

### PayConstant（支付相关常量）
```java
public class PayConstant {

    /** 支付渠道 */
    public static final String PAY_CHANNEL_ALIPAY = "alipay";
    public static final String PAY_CHANNEL_WECHAT = "wxpay";
    public static final String PAY_CHANNEL_UNIONPAY = "unionpay";

    /** 订单状态 */
    public static final int PAY_STATUS_INIT = 0;
    public static final int PAY_STATUS_PAYING = 1;
    public static final int PAY_STATUS_SUCCESS = 2;
    public static final int PAY_STATUS_FAIL = 3;
    public static final int PAY_STATUS_REFUND = 4;

    /** 支付方式 */
    public static final String PAY_MODE_ALIPAY_SDK = "alipay_sdk";
    public static final String PAY_MODE_WECHAT_SDK = "wxpay_sdk";
    public static final String PAY_MODE_FAST_PAY = "fast_pay";
}
```

### RedisConstant（Redis 相关常量）
```java
public class RedisConstant {

    /** Redis Key 前缀 */
    public static final String PREFIX = "xxpay:";

    /** 用户登录 Token */
    public static final String USER_TOKEN = PREFIX + "user:token:";

    /** 支付订单缓存 */
    public static final String PAY_ORDER = PREFIX + "pay:order:";

    /** 缓存过期时间（秒） */
    public static final int EXPIRE_HOUR = 3600;
    public static final int EXPIRE_DAY = 86400;
}
```

## 工具类

### 签名工具类
```java
public class SignatureUtils {

    /**
     * 生成签名
     */
    public static String generateSign(Map<String, Object> params, String secretKey) {
        // 1. 参数排序
        TreeMap<String, Object> sortedParams = new TreeMap<>(params);

        // 2. 拼接字符串
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, Object> entry : sortedParams.entrySet()) {
            if (entry.getValue() != null && !"".equals(entry.getValue())) {
                sb.append(entry.getKey()).append("=").append(entry.getValue()).append("&");
            }
        }
        sb.append("key=").append(secretKey);

        // 3. MD5 加密
        return DigestUtils.md5Hex(sb.toString());
    }

    /**
     * 验证签名
     */
    public static boolean verifySign(Map<String, Object> params, String sign, String secretKey) {
        String calculatedSign = generateSign(params, secretKey);
        return calculatedSign.equalsIgnoreCase(sign);
    }
}
```

### 日期工具类
```java
public class DateUtils {

    /**
     * 获取当前时间戳
     */
    public static long getCurrentTimestamp() {
        return System.currentTimeMillis();
    }

    /**
     * 生成业务流水号
     * 格式: 业务前缀 + 日期时间 + 6位流水号
     */
    public static String genSeqNo(String prefix) {
        String dateTime = DateFormatUtils.format(new Date(), "yyyyMMddHHmmss");
        String random = RandomStringUtils.randomNumeric(6);
        return prefix + dateTime + random;
    }
}
```

### HTTP 客户端工具类
```java
public class OkHttpClientUtil {

    private static final OkHttpClient CLIENT = new OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build();

    /**
     * POST JSON 请求
     */
    public static String doPostJson(String url, String jsonBody) {
        try {
            RequestBody body = RequestBody.create(
                MediaType.parse("application/json; charset=utf-8"),
                jsonBody
            );

            Request request = new Request.Builder()
                    .url(url)
                    .post(body)
                    .build();

            Response response = CLIENT.newCall(request).execute();

            if (response.isSuccessful() && response.body() != null) {
                return response.body().string();
            }

            return null;

        } catch (Exception e) {
            throw new RuntimeException("HTTP 请求失败", e);
        }
    }

    /**
     * POST Form 表单请求
     */
    public static String doPostFormUrlencoded(String url, Map<String, String> params) {
        try {
            FormBody.Builder builder = new FormBody.Builder();
            for (Map.Entry<String, String> entry : params.entrySet()) {
                builder.add(entry.getKey(), entry.getValue());
            }

            RequestBody body = builder.build();

            Request request = new Request.Builder()
                    .url(url)
                    .post(body)
                    .build();

            Response response = CLIENT.newCall(request).execute();

            if (response.isSuccessful() && response.body() != null) {
                return response.body().string();
            }

            return null;

        } catch (Exception e) {
            throw new RuntimeException("HTTP 请求失败", e);
        }
    }
}
```

## MongoDB 文档定义

```java
@Document(collection = "pay_order")
@Data
public class PayOrderDocument {

    @Id
    private String id;

    @Field("pay_order_id")
    @Indexed
    private String payOrderId;

    @Field("mch_id")
    @Indexed
    private String mchId;

    @Field("amount")
    private Long amount;

    @Field("status")
    @Indexed
    private Integer status;

    @Field("create_time")
    @Indexed
    private LocalDateTime createTime;

    @Field("update_time")
    private LocalDateTime updateTime;
}
```

## Spring 配置

### OkHttp 客户端工厂
```java
@Configuration
public class OkHttpConfig {

    @Bean
    public OkHttpClient okHttpClient() {
        return new OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .connectionPool(new ConnectionPool(20, 5, TimeUnit.MINUTES))
                .build();
    }
}
```
