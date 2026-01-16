package com.galaxy.service.pay.thirdparty;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.galaxy.config.PaymentConfig;
import com.galaxy.enumeration.JumpMode;
import com.galaxy.model.channel.vo.ChannelMerchantAccountVo;
import com.galaxy.model.pay.dto.NotifyDto;
import com.galaxy.model.pay.dto.RechargeParameterDto;
import com.galaxy.model.pay.dto.WithdrawParameterDto;
import com.galaxy.model.pay.vo.ChannelMerchantAccountBalanceVo;
import com.galaxy.model.pay.vo.RechargeNotifyResult;
import com.galaxy.model.pay.vo.RechargeResult;
import com.galaxy.model.pay.vo.WithdrawNotifyResult;
import com.galaxy.model.pay.vo.WithdrawResultVo;
import com.galaxy.module.utils.http.HttpUtil;
import com.galaxy.service.pay.RechargeHandler;
import com.galaxy.service.pay.WithdrawHandler;
import com.galaxy.storage.rdbms.entity.ChannelMerchantAccountEntity;
import com.galaxy.utils.NotifyResultUtils;
import com.galaxy.utils.PaymentUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

import static org.apache.http.HttpHeaders.CONTENT_TYPE;
import static org.springframework.http.MediaType.APPLICATION_FORM_URLENCODED_VALUE;

/**
 * 支付渠道处理类模板
 *
 * 使用说明：
 * 1. 替换 CHANNEL_NAME 和 CHANNEL_CODE
 * 2. 根据实际需求修改常量定义
 * 3. 实现具体的业务逻辑方法
 * 4. 参考文档进行签名验证实现
 */
@Slf4j
@Service
@RequiredArgsConstructor
@SuppressWarnings("DuplicatedCode")
public class PayChannelTemplate implements RechargeHandler, WithdrawHandler {

    // ========== 渠道配置 - 请修改以下常量 ==========
    private static final String CHANNEL_NAME = "ChannelName";      // 渠道名称
    private static final String CHANNEL_CODE = "XXXX";              // 渠道编号
    private static final String LOG_PREFIX = "[" + CHANNEL_NAME + "][支付編號:" + CHANNEL_CODE + "]";

    // ========== 成功状态常量 - 根据三方API文档修改 ==========
    private static final String SUCCESS_RESPONSE_CODE = "0";        // API调用成功代码
    private static final String SUCCESS_ORDER_STATUS = "SUCCESS";  // 订单成功状态
    private static final String SUCCESS_CALLBACK_RESPONSE = "success"; // 回调成功响应

    // ========== 签名配置 - 根据三方要求修改 ==========
    private static final String SIGN_SUFFIX_WITH_API_KEY = "&key=";
    private static final Set<String> SIGN_EXCLUDE_FIELDS = Set.of("sign", "timestamp");

    // ========== HTTP配置 ==========
    private static final Map<String, String> API_HEADER = Map.of(CONTENT_TYPE, APPLICATION_FORM_URLENCODED_VALUE);

    // ========== PaymentConfig 配置 ==========
    private static final PaymentConfig PAYMENT_CONFIG = PaymentConfig.builder()
        .rechargeApiPath("/api/recharge")              // 代收API路径
        .rechargeQueryApiPath("/api/recharge/query")   // 代收查询API路径
        .rechargeNotifyPrint(SUCCESS_CALLBACK_RESPONSE) // 代收回调响应
        .queryBalanceApiPath("/api/balance")           // 余额查询API路径
        .withdrawApiPath("/api/withdraw")              // 代付API路径
        .withdrawNotifyPrint(SUCCESS_CALLBACK_RESPONSE) // 代付回调响应
        .jumpMode(JumpMode.REDIRECT)                   // 跳转模式
        .build();

    // ========== 依赖注入 ==========
    private final HttpUtil httpUtil;
    private final PaymentUtils paymentUtils;
    private final ObjectMapper objectMapper;

    @Override
    public PaymentConfig getConfig() {
        return PAYMENT_CONFIG;
    }

    // ==================== 代收功能 ====================

    @Override
    public Map<String, Object> generateRechargeRequest(RechargeParameterDto dto) throws Exception {
        log.info("{}[代收請求] 开始生成请求参数", LOG_PREFIX);

        TreeMap<String, Object> sortedMap = new TreeMap<>();

        // TODO: 根据三方API文档添加请求参数
        sortedMap.put("merchantCode", dto.getMerchantCode());
        sortedMap.put("orderNo", dto.getOrderId().toString());
        sortedMap.put("amount", paymentUtils.getValidAmount(dto.getAmount(), 0));
        sortedMap.put("currency", "TWD");
        sortedMap.put("notifyUrl", dto.getRechargeNotifyUrl());
        sortedMap.put("timestamp", System.currentTimeMillis() / 1000);

        log.info("{}[代收請求] 参数: {}", LOG_PREFIX, sortedMap);

        return buildSignedParams("代收請求", sortedMap, dto.getPrivateKey());
    }

    @Override
    public String doRechargeApi(String url, Map<String, Object> params, RechargeParameterDto dto) {
        log.info("{}[代收請求] 调用API: {}", LOG_PREFIX, url);

        String response = httpUtil.doPostForEntity(url, params, API_HEADER).getBody();

        log.info("{}[代收請求] API响应: {}", LOG_PREFIX, response);
        return response;
    }

    @Override
    public boolean handleRechargeResponse(String response, RechargeResult vo, RechargeParameterDto dto) throws Exception {
        log.info("{}[代收回應] 处理响应: {}", LOG_PREFIX, response);

        Map<String, Object> resBody = objectMapper.readValue(response, new TypeReference<>() {});

        String code = String.valueOf(resBody.get("code"));
        boolean isSuccess = SUCCESS_RESPONSE_CODE.equals(code);

        if (isSuccess) {
            // TODO: 根据三方响应格式提取跳转URL
            vo.setRedirectUrl(String.valueOf(resBody.get("redirectUrl")));
            log.info("{}[代收回應] 跳转URL: {}", LOG_PREFIX, vo.getRedirectUrl());
        } else {
            log.warn("{}[代收回應] 失败: code={}, message={}", LOG_PREFIX, code, resBody.get("message"));
        }

        return isSuccess;
    }

    @Override
    public Map<String, Object> generateRechargeQueryRequest(RechargeParameterDto dto) throws Exception {
        log.info("{}[代收查詢請求] 开始生成查询参数", LOG_PREFIX);

        TreeMap<String, Object> sortedMap = new TreeMap<>();

        // TODO: 根据三方API文档添加查询参数
        sortedMap.put("merchantCode", dto.getMerchantCode());
        sortedMap.put("orderNo", dto.getOrderId().toString());
        sortedMap.put("timestamp", System.currentTimeMillis() / 1000);

        return buildSignedParams("代收查詢請求", sortedMap, dto.getPrivateKey());
    }

    @Override
    public String doRechargeQueryApi(String url, Map<String, Object> params, RechargeParameterDto dto) {
        log.info("{}[代收查詢] 调用API: {}", LOG_PREFIX, url);
        return httpUtil.doPostForEntity(url, params, API_HEADER).getBody();
    }

    @Override
    public boolean handleRechargeQueryResponse(String response, RechargeParameterDto dto) throws Exception {
        log.info("{}[代收查詢回應] 处理响应: {}", LOG_PREFIX, response);

        Map<String, Object> resBody = objectMapper.readValue(response, new TypeReference<>() {});

        String code = String.valueOf(resBody.get("code"));
        boolean isSuccess = SUCCESS_RESPONSE_CODE.equals(code);

        if (isSuccess) {
            // TODO: 根据三方响应格式判断订单状态
            String status = String.valueOf(resBody.get("status"));
            return SUCCESS_ORDER_STATUS.equals(status);
        }

        return false;
    }

    @Override
    public boolean isValidSignOfRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
        log.info("{}[代收回調驗簽] 开始验证签名", LOG_PREFIX);
        return isValidSign("代收回調驗簽", notify.getParameters(), account.getPrivateKey());
    }

    @Override
    public RechargeNotifyResult handleRechargeNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
        log.info("{}[代收回調處理] 处理回调: {}", LOG_PREFIX, notify.getParameters());

        Map<String, String> params = notify.getParameters();
        String callbackOrderNo = params.get("orderNo");
        String status = params.get("status");
        String amountStr = params.get("amount");

        return SUCCESS_ORDER_STATUS.equals(status)
            ? NotifyResultUtils.rechargeNotifySuccess(callbackOrderNo, new BigDecimal(amountStr), BigDecimal.ZERO)
            : NotifyResultUtils.rechargeNotifyFail(callbackOrderNo, "代收失败订单状态: " + status);
    }

    @Override
    public ResponseEntity<String> responseRechargeNotify() {
        return ResponseEntity.ok(getConfig().getRechargeNotifyPrint());
    }

    // ==================== 代付功能 ====================

    @Override
    public Map<String, Object> generateWithdrawRequest(WithdrawParameterDto dto) throws JsonProcessingException {
        log.info("{}[代付請求] 开始生成请求参数", LOG_PREFIX);

        TreeMap<String, Object> sortedMap = new TreeMap<>();

        // TODO: 根据三方API文档添加代付参数
        sortedMap.put("merchantCode", dto.getChannelMerchantAccountVo().getMerchantCode());
        sortedMap.put("orderNo", dto.getOrderSubId());
        sortedMap.put("amount", paymentUtils.getValidAmount(dto.getAmount(), 0));
        sortedMap.put("bankName", dto.getBankName());
        sortedMap.put("bankCode", dto.getBankCode());
        sortedMap.put("bankAccount", dto.getCardNo());
        sortedMap.put("accountName", dto.getName());
        sortedMap.put("bankBranch", dto.getBankBranchName());
        sortedMap.put("notifyUrl", dto.getChannelMerchantAccountVo().getWithdrawNotifyUrl());
        sortedMap.put("timestamp", System.currentTimeMillis() / 1000);

        log.info("{}[代付請求] 参数: {}", LOG_PREFIX, sortedMap);

        return buildSignedParams("代付請求", sortedMap, dto.getChannelMerchantAccountVo().getPrivateKey());
    }

    @Override
    public String doWithdrawApi(String url, Map<String, Object> params, ChannelMerchantAccountVo vo) {
        log.info("{}[代付請求] 调用API: {}", LOG_PREFIX, url);

        String response = httpUtil.doPostForEntity(url, params, API_HEADER).getBody();

        log.info("{}[代付請求] API响应: {}", LOG_PREFIX, response);
        return response;
    }

    @Override
    public void handleWithdrawResponse(String response, WithdrawResultVo withdrawResultVo) throws Exception {
        log.info("{}[代付回應] 处理响应: {}", LOG_PREFIX, response);

        Map<String, Object> resBody = objectMapper.readValue(response, new TypeReference<>() {});

        String code = String.valueOf(resBody.get("code"));
        boolean isSuccess = SUCCESS_RESPONSE_CODE.equals(code);

        withdrawResultVo.setIsSuccess(isSuccess);

        if (!isSuccess) {
            withdrawResultVo.setRespCode(code);
            withdrawResultVo.setRespMessage(String.valueOf(resBody.get("message")));
            withdrawResultVo.setResData(String.valueOf(resBody.get("data")));

            log.warn("{}[代付回應] 失败: code={}, message={}", LOG_PREFIX, code, withdrawResultVo.getRespMessage());
        } else {
            log.info("{}[代付回應] 成功", LOG_PREFIX);
        }
    }

    @Override
    public boolean isValidSignOfWithdrawNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
        log.info("{}[代付回調驗簽] 开始验证签名", LOG_PREFIX);
        return isValidSign("代付回調驗簽", notify.getParameters(), account.getPrivateKey());
    }

    @Override
    public WithdrawNotifyResult handleWithdrawNotify(NotifyDto notify, ChannelMerchantAccountEntity account) {
        log.info("{}[代付回調處理] 处理回调: {}", LOG_PREFIX, notify.getParameters());

        Map<String, String> params = notify.getParameters();
        String callbackOrderNo = params.get("orderNo");
        String status = params.get("status");

        return SUCCESS_ORDER_STATUS.equals(status)
            ? NotifyResultUtils.withdrawNotifySuccess(callbackOrderNo)
            : NotifyResultUtils.withdrawNotifyFail(callbackOrderNo, "代付失败订单状态: " + status);
    }

    @Override
    public ResponseEntity<String> responseWithdrawNotify() {
        return ResponseEntity.ok(getConfig().getWithdrawNotifyPrint());
    }

    // ==================== 余额查询功能 ====================

    @Override
    public Map<String, Object> generateQueryBalanceRequest(ChannelMerchantAccountEntity channelMerchantAccountEntity) throws JsonProcessingException {
        log.info("{}[商戶餘額請求] 开始生成查询参数", LOG_PREFIX);

        TreeMap<String, Object> sortedMap = new TreeMap<>();

        // TODO: 根据三方API文档添加余额查询参数
        sortedMap.put("merchantCode", channelMerchantAccountEntity.getMerchantCode());
        sortedMap.put("timestamp", System.currentTimeMillis() / 1000);

        return buildSignedParams("商戶餘額請求", sortedMap, channelMerchantAccountEntity.getPrivateKey());
    }

    @Override
    public String doQueryBalanceApi(String url, Map<String, Object> params, ChannelMerchantAccountEntity channelMerchantAccountEntity) {
        log.info("{}[查詢餘額] 调用API: {}", LOG_PREFIX, url);
        return httpUtil.doPostForEntity(url, params, API_HEADER).getBody();
    }

    @Override
    public void handleQueryBalanceResponse(String response, ChannelMerchantAccountBalanceVo vo, ChannelMerchantAccountEntity channelMerchantAccountEntity) throws Exception {
        log.info("{}[查詢餘額回應] 处理响应: {}", LOG_PREFIX, response);

        Map<String, Object> resBody = objectMapper.readValue(response, new TypeReference<>() {});

        String code = String.valueOf(resBody.get("code"));
        boolean isSuccess = SUCCESS_RESPONSE_CODE.equals(code);

        vo.setIsSuccess(isSuccess);
        vo.setBalance("0");

        if (isSuccess) {
            // TODO: 根据三方响应格式提取余额
            vo.setBalance(String.valueOf(resBody.get("balance")));
            log.info("{}[查詢餘額回應] 余额: {}", LOG_PREFIX, vo.getBalance());
        } else {
            log.warn("{}[查詢餘額回應] 失败: code={}", LOG_PREFIX, code);
        }
    }

    // ==================== 工具方法 ====================

    /**
     * 构建带签名的参数
     */
    private TreeMap<String, Object> buildSignedParams(String functionName, TreeMap<String, Object> sortedMap, String privateKey) {
        try {
            String sign = generateSign(functionName, sortedMap, privateKey);
            sortedMap.put("sign", sign);
            log.info("{}[{}] 签名: {}", LOG_PREFIX, functionName, sign);
            return sortedMap;
        } catch (Exception e) {
            log.error("{}[{}] 签名生成失败", LOG_PREFIX, functionName, e);
            throw new RuntimeException("签名生成失败", e);
        }
    }

    /**
     * 生成签名
     * TODO: 根据三方要求实现具体的签名算法
     */
    private String generateSign(String functionName, TreeMap<String, Object> sortedMap, String privateKey) {
        try {
            // 1. 移除不需要签名的字段
            Map<String, Object> signMap = new TreeMap<>(sortedMap);
            for (String exclude : SIGN_EXCLUDE_FIELDS) {
                signMap.remove(exclude);
            }

            // 2. 转换为查询字符串
            String queryString = paymentUtils.toUrlQueryEncodedString(signMap, "&");

            // 3. 添加私钥
            String textToBeSigned = queryString + SIGN_SUFFIX_WITH_API_KEY + privateKey;

            log.info("{}[{}] 待签名字符串: {}", LOG_PREFIX, functionName, textToBeSigned);

            // 4. 生成MD5签名
            String sign = DigestUtils.md5Hex(textToBeSigned).toUpperCase();

            log.info("{}[{}] 签名结果: {}", LOG_PREFIX, functionName, sign);
            return sign;

        } catch (Exception e) {
            log.error("{}[{}] 签名生成异常", LOG_PREFIX, functionName, e);
            throw new RuntimeException("签名生成异常", e);
        }
    }

    /**
     * 验证签名
     */
    private boolean isValidSign(String functionName, Map<String, String> callbackParams, String privateKey) {
        try {
            String thirdPartySign = callbackParams.remove("sign");
            if (StringUtils.isEmpty(thirdPartySign)) {
                log.warn("{}[{}] 缺少签名参数", LOG_PREFIX, functionName);
                return false;
            }

            TreeMap<String, Object> callbackSortedParams = new TreeMap<>(callbackParams);

            String ourSign = generateSign(functionName, callbackSortedParams, privateKey);
            boolean isValid = ourSign.equals(thirdPartySign);

            log.info("{}[{}] 签名验证结果: {}, 三方签名: {}, 我方签名: {}",
                LOG_PREFIX, functionName, isValid, thirdPartySign, ourSign);

            return isValid;

        } catch (Exception e) {
            log.error("{}[{}] 签名验证异常", LOG_PREFIX, functionName, e);
            return false;
        }
    }

    // ==================== 可选功能方法 ====================

    /**
     * 获取银行名称映射（如果需要）
     */
    private String getBankName(String bankCode) {
        // TODO: 实现银行代码到银行名称的映射
        // 可以使用 assets/bank_mappings.json 中的数据
        Map<String, String> bankMapping = Map.of(
            "004", "臺灣銀行",
            "005", "土地銀行",
            "006", "合庫商銀"
            // ... 更多银行映射
        );

        return bankMapping.getOrDefault(bankCode, "未知银行");
    }

    /**
     * 数据脱敏（日志中使用）
     */
    private String maskSensitiveData(String data, int showPrefix, int showSuffix) {
        if (StringUtils.isEmpty(data) || data.length() <= showPrefix + showSuffix) {
            return "****";
        }
        return data.substring(0, showPrefix) + "****" + data.substring(data.length() - showSuffix);
    }

    /**
     * 格式化金额
     */
    private String formatAmount(BigDecimal amount) {
        return paymentUtils.getValidAmount(amount, 0);
    }
}