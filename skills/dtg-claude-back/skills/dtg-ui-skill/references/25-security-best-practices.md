# 安全最佳实践

> LayuiAdmin 企业级应用安全开发指南

## 概述

在企业级应用开发中，安全是至关重要的。本文档介绍 LayuiAdmin 应用的安全最佳实践，帮助防范常见的安全风险。

## XSS 防护

### 1. 输入转义

```javascript
// 转义 HTML 特殊字符
function escapeHtml(text){
  if(!text) return '';

  var map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };

  return text.replace(/[&<>"']/g, function(m){
    return map[m];
  });
}

// 使用示例
var userInput = '<script>alert("XSS")</script>';
var safeText = escapeHtml(userInput); // &lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;
```

### 2. 内容安全策略

```html
<!-- 在 meta 标签中设置 CSP -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';">
```

### 3. Layui 模板引擎转义

```javascript
// Layui 的 laytpl 模板引擎默认会转义 HTML
layui.use('laytpl', function(){
  var laytpl = layui.laytpl;

  var tpl = '{{ d.content }}'; // 自动转义
  laytpl(tpl).render({content: userInput}, function(html){
    console.log(html); // 转义后的内容
  });
});
```

## CSRF 防护

### 1. Token 验证

```javascript
// 在请求头中添加 CSRF Token
admin.req({
  type: 'post',
  url: layui.setter.baseUrl + '/api/save',
  data: formData,
  headers: {
    'X-CSRF-TOKEN': layui.data(layui.setter.tableName).csrfToken
  },
  success: function(res){
    // 处理响应
  }
});
```

### 2. 同源策略

```javascript
// 确保所有请求都来自同一源
var baseUrl = layui.setter.baseUrl;

// 检查请求 URL 是否同源
function isSameOrigin(url){
  var link = document.createElement('a');
  link.href = url;
  return link.origin === window.location.origin;
}
```

## SQL 注入防护

### 1. 使用参数化查询

```javascript
// 前端只负责传递参数，后端使用参数化查询
admin.req({
  type: 'post',
  url: layui.setter.baseUrl + '/api/search',
  data: {
    keyword: $('#keyword').val() // 原样传递，不做拼接
  },
  success: function(res){
    // 后端已进行参数化查询
  }
});
```

### 2. 输入验证

```javascript
// 验证用户输入
function validateInput(input){
  // 检查是否包含危险字符
  var dangerous = ['<script', 'javascript:', 'onerror=', 'onload='];
  var lowerInput = input.toLowerCase();

  for(var i = 0; i < dangerous.length; i++){
    if(lowerInput.indexOf(dangerous[i]) !== -1){
      return false;
    }
  }

  return true;
}

// 使用示例
var userInput = $('#comment').val();
if(!validateInput(userInput)){
  layer.msg('输入包含非法字符');
  return;
}
```

## 敏感数据保护

### 1. 密码处理

```javascript
// 前端不存储明文密码
$('#loginForm').on('submit', function(){
  var password = $('#password').val();

  // 不记录到日志
  console.log('登录请求'); // 不要打印密码

  // 发送登录请求（使用 HTTPS）
  admin.req({
    type: 'post',
    url: layui.setter.baseUrl + '/api/login',
    data: {
      username: $('#username').val(),
      password: password // 后端会加密存储
    },
    success: function(res){
      if(res.code == 0){
        // 登录成功
        // 清空密码输入框
        $('#password').val('');
      }
    }
  });

  return false;
});
```

### 2. Token 管理

```javascript
// Token 存储在 localStorage 中（使用 Layui 的 data 方法）
layui.data(layui.setter.tableName, {
  key: 'access_token',
  value: token
});

// Token 失效处理
admin.req({
  url: layui.setter.baseUrl + '/api/data',
  success: function(res){
    if(res.code == 401){
      // 清除无效 Token
      layui.data(layui.setter.tableName, {
        key: 'access_token',
        remove: true
      });

      // 跳转到登录页
      location.href = '/user/login';
    }
  }
});
```

### 3. 敏感信息脱敏

```javascript
// 敏感信息脱敏显示
function maskSensitiveInfo(info, type){
  if(!info) return '';

  switch(type){
    case 'phone':
      // 手机号脱敏：138****1234
      return info.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');

    case 'idcard':
      // 身份证脱敏：110101********1234
      return info.replace(/(\d{6})\d{8}(\d{4})/, '$1********$2');

    case 'bankcard':
      // 银行卡脱敏：6222 **** **** 1234
      return info.replace(/(\d{4})\d{8}(\d{4})/, '$1 **** **** $2');

    case 'email':
      // 邮箱脱敏：a***@example.com
      return info.replace(/(.{1}).*(@.*)/, '$1***$2');

    default:
      return info;
  }
}

// 使用示例
var phoneNumber = '13812345678';
var maskedPhone = maskSensitiveInfo(phoneNumber, 'phone'); // 138****5678
```

## HTTPS 使用

### 1. 强制 HTTPS

```javascript
// 检查是否使用 HTTPS
if(location.protocol !== 'https:' && location.hostname !== 'localhost'){
  // 重定向到 HTTPS
  location.href = 'https:' + window.location.href.substring(window.location.protocol.length);
}
```

### 2. Cookie 安全

```javascript
// 设置 Cookie 时启用安全标志
// 注意：前端无法直接设置，需要后端配合
document.cookie = 'name=value; Secure; HttpOnly; SameSite=Strict';
```

## 权限控制

### 1. 前端权限验证

```javascript
// 前端权限验证（注意：后端也必须验证）
function checkPermission(permCode){
  var permissions = layui.data(layui.setter.tableName).permissions || [];
  return permissions.indexOf(permCode) !== -1;
}

// 敏感操作前检查权限
$('#deleteBtn').on('click', function(){
  if(!checkPermission('USER_DELETE')){
    layer.msg('没有删除权限');
    return;
  }

  // 执行删除操作
});
```

### 2. 敏感操作二次确认

```javascript
// 敏感操作需要二次确认
function sensitiveOperation(callback){
  layer.prompt({
    title: '请输入密码确认',
    formType: 1
  }, function(value, index){
    admin.req({
      type: 'post',
      url: layui.setter.baseUrl + '/api/confirm',
      data: {password: value},
      success: function(res){
        if(res.code == 0){
          layer.close(index);
          callback && callback();
        } else {
          layer.msg('密码错误');
        }
      }
    });
  });
}

// 使用示例
$('#deleteAllBtn').on('click', function(){
  sensitiveOperation(function(){
    // 执行删除操作
  });
});
```

## 日志和审计

### 1. 操作日志

```javascript
// 记录敏感操作
function logOperation(operation, detail){
  admin.req({
    type: 'post',
    url: layui.setter.baseUrl + '/api/log',
    data: {
      operation: operation,
      detail: detail,
      timestamp: Date.now(),
      userAgent: navigator.userAgent
    },
    success: function(res){
      // 日志记录成功
    }
  });
}

// 使用示例
$('#deleteBtn').on('click', function(){
  logOperation('DELETE_USER', '删除用户ID: ' + userId);

  // 执行删除操作
});
```

### 2. 错误日志

```javascript
// 全局错误捕获
window.addEventListener('error', function(event){
  admin.req({
    type: 'post',
    url: layui.setter.baseUrl + '/api/error/log',
    data: {
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      stack: event.error ? event.error.stack : '',
      url: location.href
    }
  });
});
```

## 安全检查清单

### 开发阶段

- [ ] 所有用户输入都进行验证和转义
- [ ] 敏感数据不在前端存储
- [ ] 使用 HTTPS 传输数据
- [ ] Token 正确管理
- [ ] 权限正确配置

### 部署阶段

- [ ] 内容安全策略 (CSP) 已配置
- [ ] CSRF 防护已启用
- [ ] 错误信息不泄露敏感信息
- [ ] 日志记录正常工作
- [ ] 安全响应头已配置

## 注意事项

1. **前端安全只是第一道防线**，真正的安全验证必须在后端进行
2. **永远不要信任用户输入**，始终进行验证和转义
3. **敏感数据不要在前端存储**，必要时使用 sessionStorage 并设置过期
4. **定期更新依赖库**，修复已知安全漏洞
5. **建立安全监控体系**，及时发现和处理安全事件

## 相关文档

- [22-permission-system.md](./22-permission-system.md) - 权限控制系统
- [18-api-integration-guide.md](./18-api-integration-guide.md) - API 集成指南
- [11-best-practices.md](./11-best-practices.md) - 最佳实践
