# 支付渠道第三方集成开发技能

专业的支付渠道第三方集成开发技能，提供支付渠道处理类的快速生成、最佳实践指南、安全验证和代码模板。

## 功能特性

- 支持代收(Recharge)、代付(Withdraw)、余额查询等功能模块
- 包含签名验证、加密解密、银行映射等常用工具类
- 提供完整的代码模板和最佳实践指南

## 支持的认证方式

- MD5签名认证
- SHA256+MD5双重签名
- HMAC-SHA256签名
- HMAC-SHA1签名
- Token认证
- AES加密
- 无认证方式

## 使用场景

- 开发新的支付渠道集成
- 重构现有支付代码
- 支付安全审计
- 支付接口测试

## 快速开始

```bash
# 创建新的支付渠道处理类
python scripts/generate_payment_handler.py --channel-name NewPay --channel-code 1270 --support-recharge --support-withdraw --auth-type sign

# 验证现有支付代码
python scripts/validate_payment_handler.py --file Pay1270.java
```

## 主要组件

- **代码生成脚本**：`scripts/generate_payment_handler.py`
- **代码验证脚本**：`scripts/validate_payment_handler.py`
- **银行代码映射**：`assets/bank_mappings.json`
- **代码模板**：`assets/templates/`
- **API文档**：`references/api_documentation.md`
- **安全指南**：`references/security_guide.md`

## 支持的银行和地区

支持台湾、泰国、尼泊尔、巴基斯坦等多个地区的银行代码映射和支付方式。