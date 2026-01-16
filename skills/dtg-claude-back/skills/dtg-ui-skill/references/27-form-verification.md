# Layui 表单验证完整指南

## 概述

Layui 的 `form.verify()` 方法用于定义表单验证规则，支持正则表达式验证和函数验证两种方式。

## 基础用法

### 在 HTML 中声明验证规则

```html
<!-- 单个验证规则 -->
<input type="text" name="username" lay-verify="required" placeholder="请输入用户名">

<!-- 多个验证规则（用 | 分隔）-->
<input type="text" name="email" lay-verify="required|email" placeholder="请输入邮箱">

<!-- 自定义验证规则 -->
<input type="text" name="code" lay-verify="required|code" placeholder="请输入编码">
```

### 在 JavaScript 中定义验证规则

```javascript
layui.use(['form'], function() {
    var form = layui.form;

    // 定义验证规则
    form.verify({
        // 数组形式: [正则表达式, 错误提示]
        username: [
            /^[a-zA-Z0-9_]{4,16}$/,
            '用户名必须4到16位（字母、数字、下划线）'
        ],

        // 函数形式
        password: function(value, item) {
            if (!value) {
                return '密码不能为空';
            }
        }
    });
});
```

## 内置验证规则

| 规则 | 说明 | 示例 |
|------|------|------|
| required | 必填项 | `lay-verify="required"` |
| phone | 手机号 | `lay-verify="phone"` |
| email | 邮箱 | `lay-verify="email"` |
| url | 网址 | `lay-verify="url"` |
| number | 数字 | `lay-verify="number"` |
| date | 日期 | `lay-verify="date"` |
| identity | 身份证 | `lay-verify="identity"` |

## 自定义验证规则

### 数组形式（正则表达式）

```javascript
form.verify({
    nonempty: [/\S+/, '必填项不能为空'],
    password: [/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/, '密码必须为8-16位的字母和数字组合'],
    amount: [/^(0|[1-9]\d*)(\.\d{1,2})?$/, '请输入正确的金额格式']
});
```

### 函数形式（复杂逻辑）

```javascript
form.verify({
    // 确认密码
    confirmPassword: function(value, item) {
        var password = $('input[name="password"]').val();
        if (value !== password) {
            return '两次密码输入不一致';
        }
    },

    // 费率验证（基于实际项目）
    rate: function(value, item) {
        if (value) {
            const rateValue = parseFloat(value);
            if (rateValue <= 0 || rateValue >= 100) {
                return '费率必须在0-100之间';
            }
            const parentValue = parseFloat($(item).attr('data-parent-value'));
            if (!isNaN(parentValue) && rateValue < parentValue) {
                return `费率需大于等于上级 ${parentValue}`;
            }
        }
    }
});
```

## 实际项目验证规则集合

基于实际支付系统项目的验证规则：

```javascript
form.verify({
    nonempty: [/\S+/, '必填项不能为空'],
    password: [/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/, '密码必须为8-16位的字母和数字组合'],
    payPassword: [/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/, '资金密码必须为8-16位的字母和数字组合'],
    apiPassword: [/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/, '支付密码必须为8-16位的字母和数字组合'],
    userName: [/^[a-zA-Z0-9_]{4,20}$/, '用户名必须4-20位（字母、数字、下划线）'],
    bankCard: [/^[0-9]{16,19}$/, '请输入正确的银行卡号'],
    idCard: [/^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/, '请输入正确的身份证号'],
    creditCode: [/^[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}$/, '请输入正确的统一社会信用代码'],
    mchId: [/^\d{6,15}$/, '商户号必须6-15位数字'],
    rate: function(value, item) {
        if (value) {
            const rateValue = parseFloat(value);
            if (rateValue <= 0 || rateValue >= 100) {
                return '费率必须在0-100之间';
            }
            const parentValue = parseFloat($(item).attr('data-parent-value'));
            if (!isNaN(parentValue) && rateValue < parentValue) {
                return `费率需大于等于上级 ${parentValue}`;
            }
        }
    }
});
```

## 表单字段验证组合

```html
<form class="layui-form" lay-filter="merchantForm">
    <!-- 商户名称 -->
    <div class="layui-form-item">
        <label class="layui-form-label required">商户名称</label>
        <div class="layui-input-inline">
            <input type="text" name="name" lay-verify="required|mchName" placeholder="请输入商户名称">
        </div>
    </div>

    <!-- 密码 -->
    <div class="layui-form-item">
        <label class="layui-form-label required">登录密码</label>
        <div class="layui-input-inline">
            <input type="password" name="password" id="password" lay-verify="required|password">
        </div>
    </div>

    <!-- 确认密码 -->
    <div class="layui-form-item">
        <label class="layui-form-label required">确认密码</label>
        <div class="layui-input-inline">
            <input type="password" name="confirmPassword" lay-verify="required|confirmPassword">
        </div>
    </div>

    <!-- 费率 -->
    <div class="layui-form-item">
        <label class="layui-form-label">代收费率</label>
        <div class="layui-input-inline">
            <input type="number" name="payRate" lay-verify="rate" data-parent-value="5.5" min="0" max="100" step="0.01">
        </div>
    </div>
</form>
```

## 常见问题

### 1. 验证规则不生效

确保：
- `lay-verify` 属性值与定义的规则名一致
- 表单元素有正确的 `name` 属性
- 表单使用 `layui-form` 类
- 按钮使用 `lay-submit` 和 `lay-filter`

### 2. 多个规则如何书写

使用 `|` 分隔：
```html
<input lay-verify="required|email|code">
```

### 3. 动态添加的表单元素验证不生效

动态添加后需要重新渲染：
```javascript
$('#formContainer').append('<input name="newField" lay-verify="required">');
form.render(null, 'formFilter');
```

## 最佳实践

1. **规则命名**：使用有意义的规则名称
2. **错误提示**：提供清晰的错误提示信息
3. **规则复用**：将常用规则封装为工具函数
4. **安全性**：前端验证仅用于用户体验，后端必须再次验证

## 相关文档

- 表单模块详解 → `04-form-module.md`
- API 参考 → `10-api-reference.md`
- 最佳实践 → `11-best-practices.md`
