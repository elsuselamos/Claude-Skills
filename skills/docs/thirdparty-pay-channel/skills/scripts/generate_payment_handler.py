#!/usr/bin/env python3
"""
支付渠道处理类代码生成器
用于快速创建新的支付渠道处理类模板
"""

import os
import argparse
from datetime import datetime

def generate_payment_handler(channel_name, channel_code, support_recharge, support_withdraw, auth_type):
    """
    生成支付渠道处理类代码
    """

    # 计算实现的接口
    interfaces = []
    if support_recharge:
        interfaces.append('RechargeHandler')
    if support_withdraw:
        interfaces.append('WithdrawHandler')
    implements_clause = ', '.join(interfaces) if interfaces else ''

    # 生成import语句
    imports = []
    imports.append("import com.fasterxml.jackson.core.JsonProcessingException;")
    imports.append("import com.fasterxml.jackson.core.type.TypeReference;")
    imports.append("import com.fasterxml.jackson.databind.ObjectMapper;")
    imports.append("import com.galaxy.config.PaymentConfig;")
    imports.append("import com.galaxy.enumeration.JumpMode;")
    imports.append("import com.galaxy.model.channel.vo.ChannelMerchantAccountVo;")
    imports.append("import com.galaxy.model.pay.dto.NotifyDto;")
    if support_recharge:
        imports.append("import com.galaxy.model.pay.dto.RechargeParameterDto;")
    if support_withdraw:
        imports.append("import com.galaxy.model.pay.dto.WithdrawParameterDto;")
    imports.append("import com.galaxy.model.pay.vo.ChannelMerchantAccountBalanceVo;")
    if support_recharge:
        imports.append("import com.galaxy.model.pay.vo.RechargeNotifyResult;")
        imports.append("import com.galaxy.model.pay.vo.RechargeResult;")
    if support_withdraw:
        imports.append("import com.galaxy.model.pay.vo.WithdrawNotifyResult;")
        imports.append("import com.galaxy.model.pay.vo.WithdrawResultVo;")
    imports.append("import com.galaxy.module.utils.http.HttpUtil;")
    if support_recharge:
        imports.append("import com.galaxy.service.pay.RechargeHandler;")
    if support_withdraw:
        imports.append("import com.galaxy.service.pay.WithdrawHandler;")
    imports.append("import com.galaxy.storage.rdbms.entity.ChannelMerchantAccountEntity;")
    imports.append("import com.galaxy.utils.NotifyResultUtils;")
    imports.append("import com.galaxy.utils.PaymentUtils;")
    imports.append("import lombok.RequiredArgsConstructor;")
    imports.append("import lombok.extern.slf4j.Slf4j;")

    if auth_type == 'sign':
        imports.append("import org.apache.commons.codec.digest.DigestUtils;")
    if support_recharge or support_withdraw:
        imports.append("import org.springframework.http.ResponseEntity;")
    imports.append("import org.springframework.stereotype.Service;")

    if support_recharge or support_withdraw or auth_type == 'sign':
        imports.append("import java.util.HashMap;")
    if support_recharge or support_withdraw or auth_type == 'sign':
        imports.append("import java.util.Map;")
    if auth_type == 'sign':
        imports.append("import java.util.TreeMap;")

    # 生成imports部分
    imports_section = '\n'.join(sorted(set(imports)))

    # 生成class头部
    class_header = f"""package com.galaxy.service.pay.thirdparty;

{imports_section}

@Slf4j
@Service
@RequiredArgsConstructor
// 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// 渠道编号: {channel_code}
// 认证方式: {auth_type}
public class Pay{channel_code} implements {implements_clause} {{"""

    # 生成字段和配置
    if auth_type == 'sign':
        fields = f"""
    // DI
    private final HttpUtil httpUtil;
    private final PaymentUtils paymentUtils;
    private final ObjectMapper objectMapper;

    // constant
    private static final String SUCCESS_RESPONSE_CODE = "0";
    private static final String SUCCESS_ORDER_STATUS = "SUCCESS";
    private static final String SUCCESS_CALLBACK_RESPONSE = "success";
    private static final String LOG_PREFIX = "[{channel_name}][支付編號:{channel_code}]";
    private static final String SIGN_SUFFIX_WITH_API_KEY = "&key=";

    private static final Map<String, String> API_HEADER = Map.of(CONTENT_TYPE, APPLICATION_FORM_URLENCODED_VALUE);

    private static final PaymentConfig PAYMENT_CONFIG = PaymentConfig.builder()
        {"rechargeApiPath(\"/api/deplace\")" if support_recharge else ""}
        {"rechargeQueryApiPath(\"/api/deplace/query\")" if support_recharge else ""}
        {"rechargeNotifyPrint(SUCCESS_CALLBACK_RESPONSE)" if support_recharge else ""}
        {"queryBalanceApiPath(\"/api/balance\")" if support_withdraw else ""}
        {"withdrawApiPath(\"/api/withdraw\")" if support_withdraw else ""}
        {"withdrawNotifyPrint(SUCCESS_CALLBACK_RESPONSE)" if support_withdraw else ""}
        .jumpMode(JumpMode.REDIRECT).build();"""

    else:
        fields = f"""
    // DI
    private final HttpUtil httpUtil;
    private final PaymentUtils paymentUtils;
    private final ObjectMapper objectMapper;

    // constant
    private static final String SUCCESS_RESPONSE_CODE = "200";
    private static final String SUCCESS_ORDER_STATUS = "success";
    private static final String SUCCESS_CALLBACK_RESPONSE = "ok";
    private static final String LOG_PREFIX = "[{channel_name}][支付編號:{channel_code}]";

    private static final PaymentConfig PAYMENT_CONFIG = PaymentConfig.builder()
        {"rechargeApiPath(\"/api/deplace\")" if support_recharge else ""}
        {"rechargeQueryApiPath(\"/api/deplace/query\")" if support_recharge else ""}
        {"rechargeNotifyPrint(SUCCESS_CALLBACK_RESPONSE)" if support_recharge else ""}
        {"queryBalanceApiPath(\"/api/balance\")" if support_withdraw else ""}
        {"withdrawApiPath(\"/api/withdraw\")" if support_withdraw else ""}
        {"withdrawNotifyPrint(SUCCESS_CALLBACK_RESPONSE)" if support_withdraw else ""}
        .jumpMode(JumpMode.REDIRECT).build();"""

    # 生成方法
    methods = """

    @Override
    public PaymentConfig getConfig() {
        return PAYMENT_CONFIG;
    }"""

    if support_recharge:
        if auth_type == 'sign':
            methods += """

    @Override
    public Map<String, Object> generateRechargeRequest(RechargeParameterDto dto) throws Exception {
        TreeMap<String, Object> sortedMap = new TreeMap<>();
        // TODO: 实现代收请求参数生成
        sortedMap.put("merchantCode", dto.getMerchantCode());
        sortedMap.put("orderNo", dto.getOrderId().toString());
        sortedMap.put("amount", paymentUtils.getValidAmount(dto.getAmount(), 0));

        return buildBaseParams("代收请求", sortedMap, dto.getPrivateKey());
    }"""
        else:
            methods += """

    @Override
    public Map<String, Object> generateRechargeRequest(RechargeParameterDto dto) throws Exception {
        Map<String, Object> map = new HashMap<>();
        // TODO: 实现代收请求参数生成
        map.put("merchantCode", dto.getMerchantCode());
        map.put("orderNo", dto.getOrderId().toString());
        map.put("amount", paymentUtils.getValidAmount(dto.getAmount(), 0));

        return map;
    }"""

    if support_withdraw:
        if auth_type == 'sign':
            methods += """

    @Override
    public Map<String, Object> generateWithdrawRequest(WithdrawParameterDto dto) throws JsonProcessingException {
        TreeMap<String, Object> sortedMap = new TreeMap<>();
        // TODO: 实现代付请求参数生成
        sortedMap.put("merchantCode", dto.getChannelMerchantAccountVo().getMerchantCode());
        sortedMap.put("orderNo", dto.getOrderSubId());
        sortedMap.put("amount", paymentUtils.getValidAmount(dto.getAmount(), 0));

        return buildBaseParams("代付请求", sortedMap, dto.getChannelMerchantAccountVo().getPrivateKey());
    }"""
        else:
            methods += """

    @Override
    public Map<String, Object> generateWithdrawRequest(WithdrawParameterDto dto) throws JsonProcessingException {
        Map<String, Object> map = new HashMap<>();
        // TODO: 实现代付请求参数生成
        map.put("merchantCode", dto.getChannelMerchantAccountVo().getMerchantCode());
        map.put("orderNo", dto.getOrderSubId());
        map.put("amount", paymentUtils.getValidAmount(dto.getAmount(), 0));

        return map;
    }"""

    if auth_type == 'sign':
        methods += """

    private TreeMap<String, Object> buildBaseParams(String functionName, TreeMap<String, Object> sortedMap, String privateKey) {
        log.info("{}[{}] sortedMap: {}", LOG_PREFIX, functionName, sortedMap);
        String sign = generateSign(functionName, sortedMap, privateKey);
        sortedMap.put("sign", sign);
        return sortedMap;
    }

    private String generateSign(String functionName, TreeMap<String, Object> sortedMap, String privateKey) {
        String queryString = paymentUtils.toUrlQueryEncodedString(sortedMap, StringPool.AMPERSAND);
        String textToBeSigned = queryString + SIGN_SUFFIX_WITH_API_KEY + privateKey;
        log.info("{}[{}] textToBeSigned: {}", LOG_PREFIX, functionName, textToBeSigned);

        String sign = DigestUtils.md5Hex(textToBeSigned);
        log.info("{}[{}] sign: {}", LOG_PREFIX, functionName, sign);

        return sign;
    }"""

    methods += """

    // TODO: 实现其他必要的方法
    // 请参考 SKILL.md 中的完整实现指南
}"""

    # 组装完整的模板
    return class_header + fields + methods

def main():
    parser = argparse.ArgumentParser(description='生成支付渠道处理类')
    parser.add_argument('--channel-name', required=True, help='渠道名称')
    parser.add_argument('--channel-code', required=True, type=int, help='渠道编号')
    parser.add_argument('--support-recharge', action='store_true', help='支持代收')
    parser.add_argument('--support-withdraw', action='store_true', help='支持代付')
    parser.add_argument('--auth-type', choices=['sign', 'token', 'aes', 'none'], default='sign', help='认证方式')
    parser.add_argument('--output', default='./', help='输出目录')

    args = parser.parse_args()

    # 生成代码
    code = generate_payment_handler(
        args.channel_name,
        args.channel_code,
        args.support_recharge,
        args.support_withdraw,
        args.auth_type
    )

    # 生成文件名
    filename = f"Pay{args.channel_code}.java"
    filepath = os.path.join(args.output, filename)

    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

    print(f"✅ 已生成支付渠道处理类: {filepath}")
    print(f"渠道: {args.channel_name} (编号: {args.channel_code})")
    print(f"功能: 代收{'✓' if args.support_recharge else '✗'} / 代付{'✓' if args.support_withdraw else '✗'}")
    print(f"认证: {args.auth_type}")
    print(f"\n⚠️  请实现 TODO 标记的方法，并参考 SKILL.md 中的完整实现指南")

if __name__ == "__main__":
    main()