# thirdparty-pay-channel 技能包

## 技能概述

`thirdparty-pay-channel` 是一个专业的支付渠道第三方集成开发技能，提供支付渠道处理类的快速生成、最佳实践指南、安全验证和代码模板。

## 技能功能

### 🚀 核心功能
- **代码生成器**：快速生成新的支付渠道处理类模板
- **代码验证器**：检查支付代码的安全性和规范性
- **最佳实践指南**：完整的开发指导和安全建议
- **代码模板**：高质量的生产级代码模板

### 📚 包含内容

#### 1. SKILL.md - 主要指导文档
- 快速开始指南
- 支付渠道类型分类
- 核心组件开发指南
- 签名生成模式
- 错误处理最佳实践
- 安全性检查清单
- 常见问题解决

#### 2. scripts/ - 实用工具脚本
- **generate_payment_handler.py** - 支付渠道处理类代码生成器
- **validate_payment_handler.py** - 代码质量和安全性验证器

#### 3. references/ - 详细文档
- **api_documentation.md** - 完整的API文档参考
- **security_guide.md** - 安全开发指南
- **error_codes.md** - 错误代码参考

#### 4. assets/ - 资源文件
- **bank_mappings.json** - 台湾银行代码映射表
- **templates/** - 代码模板目录
  - **PayChannelTemplate.java** - 支付渠道处理类模板
  - **test_template.java** - 单元测试模板

## 使用方法

### 快速生成新的支付渠道类

```bash
# 生成支持代收和代付的支付渠道（签名认证）
python scripts/generate_payment_handler.py \
  --channel-name "NewPay" \
  --channel-code 1271 \
  --support-recharge \
  --support-withdraw \
  --auth-type sign

# 生成仅支持代收的支付渠道（Token认证）
python scripts/generate_payment_handler.py \
  --channel-name "SimplePay" \
  --channel-code 1272 \
  --support-recharge \
  --auth-type token
```

### 验证现有代码

```bash
# 验证支付渠道处理类的代码质量
python scripts/validate_payment_handler.py --file Pay1270.java

# 输出格式化的验证报告
python scripts/validate_payment_handler.py --file Pay1270.java --format json
```

## 支持的认证方式

### 1. 签名认证 (sign)
- MD5签名
- SHA256+MD5双重签名
- 参数排序和加密

### 2. Token认证 (token)
- Bearer Token
- API Key认证

### 3. AES加密认证 (aes)
- AES/CBC/PKCS5Padding
- 双重Base64编码

### 4. 无认证 (none)
- 直接API调用

## 支付渠道分类

### 按功能支持
- **代收Only**：仅支持充值
- **代付Only**：仅支持提现
- **全功能**：支持代收+代付+余额查询

### 按认证方式
- **签名认证**：MD5/SHA256 + 私钥
- **Token认证**：Bearer Token
- **AES加密**：AES/CBC/PKCS5Padding
- **无认证**：直接API调用

## 最佳实践

### 安全性
- ✅ 签名验证逻辑正确性
- ✅ 金额精度处理
- ✅ 订单号重复检查
- ✅ IP白名单验证
- ✅ 敏感信息日志脱敏

### 代码质量
- ✅ 异常处理完善
- ✅ 日志记录规范
- ✅ 常量定义规范
- ✅ 参数验证完整

### 可维护性
- ✅ 清晰的代码结构
- ✅ 完善的文档注释
- ✅ 统一的错误处理
- ✅ 标准化的响应格式

## 文件结构

```
payChannel-thirdparty/
├── SKILL.md                     # 主要指导文档
├── README.md                    # 技能包说明（本文件）
├── scripts/                     # 工具脚本
│   ├── generate_payment_handler.py
│   └── validate_payment_handler.py
├── references/                  # 详细文档
│   ├── api_documentation.md
│   ├── security_guide.md
│   └── error_codes.md
└── assets/                      # 资源文件
    ├── bank_mappings.json
    └── templates/
        ├── PayChannelTemplate.java
        └── test_template.java
```

## 技能特性

### 🎯 精确匹配
- 通过详细的description确保技能在正确的场景下被触发
- 针对支付渠道第三方集成的专业领域

### 📖 渐进式学习
- 三级加载系统：元数据 → SKILL.md → 资源文件
- 从基础概念到高级实现的完整学习路径

### 🛠️ 实用工具
- 代码生成器减少重复工作
- 验证器确保代码质量
- 模板提供最佳实践参考

### 🔒 安全导向
- 完整的安全检查清单
- 常见安全漏洞防护
- 敏感信息处理指南

## 安装和使用

1. 将 `.skill` 文件导入到支持技能的平台
2. 查看主要指导文档了解使用方法
3. 根据具体需求选择合适的工具和模板
4. 遵循最佳实践指南进行开发

## 版本信息

- **版本**: 1.0
- **创建时间**: 2025-12-03
- **适用场景**: Java Spring Boot 支付系统开发
- **兼容性**: 支持主流的三方支付平台集成

## 技术支持

如需技术支持或有改进建议，请参考：
- SKILL.md 中的详细指南
- references/ 中的完整文档
- assets/templates/ 中的代码示例

---

🚀 **快速开始**: 查看 SKILL.md 中的"快速开始"部分，立即开始创建您的第一个支付渠道处理类！