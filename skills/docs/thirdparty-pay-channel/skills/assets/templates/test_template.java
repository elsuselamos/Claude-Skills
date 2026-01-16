package com.galaxy.service.pay.thirdparty;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.galaxy.model.channel.vo.ChannelMerchantAccountVo;
import com.galaxy.model.pay.dto.NotifyDto;
import com.galaxy.model.pay.dto.RechargeParameterDto;
import com.galaxy.model.pay.dto.WithdrawParameterDto;
import com.galaxy.model.pay.vo.RechargeResult;
import com.galaxy.model.pay.vo.WithdrawResultVo;
import com.galaxy.module.utils.http.HttpUtil;
import com.galaxy.storage.rdbms.entity.ChannelMerchantAccountEntity;
import com.galaxy.utils.PaymentUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * 支付渠道处理类测试模板
 *
 * 使用说明：
 * 1. 将 PayChannelTest 替换为实际的类名
 * 2. 修改导入的包名
 * 3. 根据实际业务逻辑调整测试用例
 * 4. 添加更多的边界测试和异常测试
 */
@ExtendWith(MockitoExtension.class)
class PayChannelTest {

    // Mock依赖
    @Mock
    private HttpUtil httpUtil;

    @Mock
    private PaymentUtils paymentUtils;

    @Mock
    private ObjectMapper objectMapper;

    // 被测试的类
    @InjectMocks
    private PayChannelTemplate payChannel;

    // 测试数据
    private RechargeParameterDto rechargeDto;
    private WithdrawParameterDto withdrawDto;
    private ChannelMerchantAccountVo channelMerchantAccountVo;
    private ChannelMerchantAccountEntity accountEntity;

    @BeforeEach
    void setUp() {
        // 初始化测试数据
        rechargeDto = createMockRechargeDto();
        withdrawDto = createMockWithdrawDto();
        channelMerchantAccountVo = createMockChannelMerchantAccountVo();
        accountEntity = createMockChannelMerchantAccountEntity();
    }

    // ==================== 代收功能测试 ====================

    @Test
    void testGenerateRechargeRequest() throws Exception {
        // Given
        when(paymentUtils.getValidAmount(any(BigDecimal.class), anyInt())).thenReturn("1000");

        // When
        Map<String, Object> result = payChannel.generateRechargeRequest(rechargeDto);

        // Then
        assertNotNull(result);
        assertTrue(result.containsKey("merchantCode"));
        assertTrue(result.containsKey("orderNo"));
        assertTrue(result.containsKey("amount"));
        assertTrue(result.containsKey("sign"));

        assertEquals("MERCHANT001", result.get("merchantCode"));
        assertEquals("12345", result.get("orderNo"));
        assertEquals("1000", result.get("amount"));

        verify(paymentUtils).getValidAmount(BigDecimal.valueOf(1000), 0);
    }

    @Test
    void testDoRechargeApi() {
        // Given
        String url = "https://api.example.com/recharge";
        Map<String, Object> params = new HashMap<>();
        String expectedResponse = "{\"code\":\"0\",\"redirectUrl\":\"https://payment.example.com/pay\"}";

        when(httpUtil.doPostForEntity(eq(url), eq(params), any()))
            .thenReturn(org.springframework.http.ResponseEntity.ok(expectedResponse));

        // When
        String result = payChannel.doRechargeApi(url, params, rechargeDto);

        // Then
        assertEquals(expectedResponse, result);
        verify(httpUtil).doPostForEntity(eq(url), eq(params), any());
    }

    @Test
    void testHandleRechargeResponse_Success() throws Exception {
        // Given
        String response = "{\"code\":\"0\",\"redirectUrl\":\"https://payment.example.com/pay\"}";
        RechargeResult vo = new RechargeResult();

        when(objectMapper.readValue(eq(response), any(TypeReference.class)))
            .thenReturn(Map.of("code", "0", "redirectUrl", "https://payment.example.com/pay"));

        // When
        boolean result = payChannel.handleRechargeResponse(response, vo, rechargeDto);

        // Then
        assertTrue(result);
        assertEquals("https://payment.example.com/pay", vo.getRedirectUrl());
    }

    @Test
    void testHandleRechargeResponse_Failure() throws Exception {
        // Given
        String response = "{\"code\":\"1001\",\"message\":\"参数错误\"}";
        RechargeResult vo = new RechargeResult();

        when(objectMapper.readValue(eq(response), any(TypeReference.class)))
            .thenReturn(Map.of("code", "1001", "message", "参数错误"));

        // When
        boolean result = payChannel.handleRechargeResponse(response, vo, rechargeDto);

        // Then
        assertFalse(result);
    }

    // ==================== 代付功能测试 ====================

    @Test
    void testGenerateWithdrawRequest() throws Exception {
        // Given
        when(paymentUtils.getValidAmount(any(BigDecimal.class), anyInt())).thenReturn("2000");

        // When
        Map<String, Object> result = payChannel.generateWithdrawRequest(withdrawDto);

        // Then
        assertNotNull(result);
        assertTrue(result.containsKey("merchantCode"));
        assertTrue(result.containsKey("orderNo"));
        assertTrue(result.containsKey("amount"));
        assertTrue(result.containsKey("bankAccount"));
        assertTrue(result.containsKey("sign"));

        assertEquals("MERCHANT001", result.get("merchantCode"));
        assertEquals("WITHDRAW123", result.get("orderNo"));
        assertEquals("2000", result.get("amount"));
        assertEquals("6225880123456789", result.get("bankAccount"));

        verify(paymentUtils).getValidAmount(BigDecimal.valueOf(2000), 0);
    }

    @Test
    void testDoWithdrawApi() {
        // Given
        String url = "https://api.example.com/withdraw";
        Map<String, Object> params = new HashMap<>();
        String expectedResponse = "{\"code\":\"0\",\"message\":\"提交成功\"}";

        when(httpUtil.doPostForEntity(eq(url), eq(params), any()))
            .thenReturn(org.springframework.http.ResponseEntity.ok(expectedResponse));

        // When
        String result = payChannel.doWithdrawApi(url, params, channelMerchantAccountVo);

        // Then
        assertEquals(expectedResponse, result);
        verify(httpUtil).doPostForEntity(eq(url), eq(params), any());
    }

    @Test
    void testHandleWithdrawResponse_Success() throws Exception {
        // Given
        String response = "{\"code\":\"0\",\"message\":\"提交成功\"}";
        WithdrawResultVo resultVo = new WithdrawResultVo();

        when(objectMapper.readValue(eq(response), any(TypeReference.class)))
            .thenReturn(Map.of("code", "0", "message", "提交成功"));

        // When
        payChannel.handleWithdrawResponse(response, resultVo);

        // Then
        assertTrue(resultVo.getIsSuccess());
    }

    @Test
    void testHandleWithdrawResponse_Failure() throws Exception {
        // Given
        String response = "{\"code\":\"1002\",\"message\":\"余额不足\"}";
        WithdrawResultVo resultVo = new WithdrawResultVo();

        when(objectMapper.readValue(eq(response), any(TypeReference.class)))
            .thenReturn(Map.of("code", "1002", "message", "余额不足", "data", "详细信息"));

        // When
        payChannel.handleWithdrawResponse(response, resultVo);

        // Then
        assertFalse(resultVo.getIsSuccess());
        assertEquals("1002", resultVo.getRespCode());
        assertEquals("余额不足", resultVo.getRespMessage());
        assertEquals("详细信息", resultVo.getResData());
    }

    // ==================== 签名验证测试 ====================

    @Test
    void testGenerateSign() throws Exception {
        // Given
        TreeMap<String, Object> params = new TreeMap<>();
        params.put("merchantCode", "MERCHANT001");
        params.put("orderNo", "12345");
        params.put("amount", "1000");
        String privateKey = "test_private_key";

        when(paymentUtils.toUrlQueryEncodedString(any(Map.class), anyString()))
            .thenReturn("amount=1000&merchantCode=MERCHANT001&orderNo=12345");

        // When
        String result = invokePrivateMethod("generateSign", "测试", params, privateKey);

        // Then
        assertNotNull(result);
        assertEquals(32, result.length()); // MD5 length
        assertTrue(result.matches("[A-F0-9]+")); // Uppercase hex

        verify(paymentUtils).toUrlQueryEncodedString(params, "&");
    }

    @Test
    void testIsValidSign_ValidSignature() {
        // Given
        Map<String, String> params = new HashMap<>();
        params.put("merchantCode", "MERCHANT001");
        params.put("orderNo", "12345");
        params.put("amount", "1000");
        params.put("sign", "VALID_SIGNATURE");

        when(paymentUtils.toUrlQueryEncodedString(any(Map.class), anyString()))
            .thenReturn("amount=1000&merchantCode=MERCHANT001&orderNo=12345");

        // When
        boolean result = invokePrivateMethod("isValidSign", "测试", params, "test_private_key");

        // Then
        // 这个测试需要根据实际的签名算法实现
        // assertTrue(result);
    }

    // ==================== 回调处理测试 ====================

    @Test
    void testHandleRechargeNotify_Success() {
        // Given
        Map<String, String> params = Map.of(
            "orderNo", "12345",
            "status", "SUCCESS",
            "amount", "1000"
        );
        NotifyDto notify = new NotifyDto();
        notify.setParameters(params);

        // When
        var result = payChannel.handleRechargeNotify(notify, accountEntity);

        // Then
        assertNotNull(result);
        assertTrue(result.isSuccess());
        assertEquals("12345", result.getOrderNo());
    }

    @Test
    void testHandleRechargeNotify_Failure() {
        // Given
        Map<String, String> params = Map.of(
            "orderNo", "12345",
            "status", "FAILED",
            "amount", "1000"
        );
        NotifyDto notify = new NotifyDto();
        notify.setParameters(params);

        // When
        var result = payChannel.handleRechargeNotify(notify, accountEntity);

        // Then
        assertNotNull(result);
        assertFalse(result.isSuccess());
        assertEquals("12345", result.getOrderNo());
    }

    // ==================== 辅助方法 ====================

    /**
     * 创建模拟的代收参数
     */
    private RechargeParameterDto createMockRechargeDto() {
        RechargeParameterDto dto = new RechargeParameterDto();
        dto.setOrderId(12345L);
        dto.setAmount(BigDecimal.valueOf(1000));
        dto.setMerchantCode("MERCHANT001");
        dto.setPrivateKey("test_private_key");
        dto.setRechargeNotifyUrl("https://example.com/notify");
        return dto;
    }

    /**
     * 创建模拟的代付参数
     */
    private WithdrawParameterDto createMockWithdrawDto() {
        WithdrawParameterDto dto = new WithdrawParameterDto();
        dto.setOrderSubId("WITHDRAW123");
        dto.setAmount(BigDecimal.valueOf(2000));
        dto.setName("张三");
        dto.setBankCode("004");
        dto.setBankName("臺灣銀行");
        dto.setCardNo("6225880123456789");
        dto.setBankBranchName("台北分行");
        dto.setChannelMerchantAccountVo(channelMerchantAccountVo);
        return dto;
    }

    /**
     * 创建模拟的商户账户VO
     */
    private ChannelMerchantAccountVo createMockChannelMerchantAccountVo() {
        ChannelMerchantAccountVo vo = new ChannelMerchantAccountVo();
        vo.setMerchantCode("MERCHANT001");
        vo.setPrivateKey("test_private_key");
        vo.setWithdrawNotifyUrl("https://example.com/withdraw/notify");
        return vo;
    }

    /**
     * 创建模拟的商户账户实体
     */
    private ChannelMerchantAccountEntity createMockChannelMerchantAccountEntity() {
        ChannelMerchantAccountEntity entity = new ChannelMerchantAccountEntity();
        entity.setMerchantCode("MERCHANT001");
        entity.setPrivateKey("test_private_key");
        return entity;
    }

    /**
     * 调用私有方法（用于测试）
     */
    @SuppressWarnings("unchecked")
    private <T> T invokePrivateMethod(String methodName, Object... args) {
        try {
            java.lang.reflect.Method method = PayChannelTemplate.class
                .getDeclaredMethod(methodName, getParameterTypes(args));
            method.setAccessible(true);
            return (T) method.invoke(payChannel, args);
        } catch (Exception e) {
            throw new RuntimeException("Failed to invoke private method: " + methodName, e);
        }
    }

    /**
     * 获取参数类型数组
     */
    private Class<?>[] getParameterTypes(Object[] args) {
        Class<?>[] types = new Class<?>[args.length];
        for (int i = 0; i < args.length; i++) {
            types[i] = args[i].getClass();
        }
        return types;
    }
}