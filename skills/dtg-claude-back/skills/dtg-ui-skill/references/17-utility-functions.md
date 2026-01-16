# 工具函数库

本文档收录了 LayuiAdmin 项目中常用的工具函数。

## 1. 金额格式化函数

### 千分位格式化

```javascript
/**
 * 金额千分位格式化（保留两位小数）
 * @param {number|string} number - 要格式化的数字
 * @returns {string} 格式化后的字符串
 */
function formatNumberWithCommas(number) {
  if (number == null || number === '' || isNaN(number)) return '0.00';
  var num = parseFloat(number);
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

// 示例
formatNumberWithCommas(1234567.89); // "1,234,567.89"
formatNumberWithCommas(null);      // "0.00"
```

### 带提示的金额显示

```javascript
/**
 * 带提示的金额显示（鼠标悬停显示完整数字）
 * @param {number|string} number - 要显示的数字
 * @returns {string} HTML 字符串
 */
function formatAmountWithTooltip(number) {
  if (number == null || number === '' || isNaN(number)) {
    return '<span class="amount-display">0.00</span>';
  }
  var formatted = formatNumberWithCommas(number);
  var fullDisplay = formatFullNumberWithCommas(number);
  return '<span class="amount-display" data-original="' + fullDisplay +
         '" data-formatted="' + formatted +
         '" style="cursor: pointer; border-bottom: 1px dashed #ccc;" ' +
         'onmouseover="this.textContent=this.getAttribute(\'data-original\'); this.style.fontWeight=\'bold\';" ' +
         'onmouseout="this.textContent=this.getAttribute(\'data-formatted\'); this.style.fontWeight=\'normal\';">' +
         formatted + '</span>';
}
```

### 金额求和

```javascript
/**
 * 金额数组求和
 * @param {Array} amounts - 金额数组
 * @returns {number} 总和
 */
function sumAmounts(amounts) {
  return amounts.reduce(function(sum, amount) {
    return sum + (parseFloat(amount) || 0);
  }, 0);
}
```

## 2. 日期时间格式化

### 日期格式化

```javascript
/**
 * 格式化日期
 * @param {Date|string|number} date - 日期对象、时间戳或日期字符串
 * @param {string} format - 格式字符串，默认 "yyyy-MM-dd HH:mm:ss"
 * @returns {string} 格式化后的日期字符串
 */
function formatDate(date, format) {
  if (!date) return '';
  format = format || 'yyyy-MM-dd HH:mm:ss';

  var d = new Date(date);
  var o = {
    'M+': d.getMonth() + 1,
    'd+': d.getDate(),
    'H+': d.getHours(),
    'm+': d.getMinutes(),
    's+': d.getSeconds(),
    'q+': Math.floor((d.getMonth() + 3) / 3),
    'S': d.getMilliseconds()
  };

  if (/(y+)/.test(format)) {
    format = format.replace(RegExp.$1, (d.getFullYear() + '').substr(4 - RegExp.$1.length));
  }

  for (var k in o) {
    if (new RegExp('(' + k + ')').test(format)) {
      format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ('00' + o[k]).substr(('' + o[k]).length));
    }
  }

  return format;
}

// 示例
formatDate(new Date(), 'yyyy-MM-dd');           // "2025-12-28"
formatDate(new Date(), 'yyyy-MM-dd HH:mm:ss');  // "2025-12-28 15:30:45"
```

### 获取当天开始/结束时间

```javascript
/**
 * 获取当天开始时间
 * @returns {Date} 当天 00:00:00
 */
function getTodayStart() {
  var now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
}

/**
 * 获取当天结束时间
 * @returns {Date} 当天 23:59:59
 */
function getTodayEnd() {
  var now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
}
```

### 计算日期差

```javascript
/**
 * 计算两个日期之间的天数差
 * @param {Date} date1 - 日期1
 * @param {Date} date2 - 日期2
 * @returns {number} 天数差
 */
function daysBetween(date1, date2) {
  var oneDay = 24 * 60 * 60 * 1000;
  return Math.round(Math.abs((date1 - date2) / oneDay));
}
```

## 3. 权限检查函数

### 检查单个权限

```javascript
/**
 * 检查权限
 * @param {string} authAction - 权限动作代码
 * @param {Function} callback - 回调函数，参数为是否有权限
 */
function checkAuth(authAction, callback) {
  admin.req({
    type: 'get',
    url: '/api/mch_info/checkAuth',
    data: {
      access_token: layui.data(layui.setter.tableName).access_token,
      authAction: authAction
    },
    success: function(res){
      var hasAuth = res.data !== 'RET_SERVICE_PAGE_NO_AUTH';
      callback(hasAuth);
    }
  });
}

// 示例
checkAuth('ROLE_PAY_PASSAGE_EDIT', function(hasAuth){
  if(!hasAuth){
    $('#editButton').hide();
  }
});
```

### 批量检查权限

```javascript
/**
 * 批量检查权限
 * @param {Array} authActions - 权限动作代码数组
 * @param {Function} callback - 回调函数，参数为权限对象
 */
function checkAuthBatch(authActions, callback) {
  var authResults = {};
  var completed = 0;

  authActions.forEach(function(action){
    checkAuth(action, function(hasAuth){
      authResults[action] = hasAuth;
      completed++;
      if(completed === authActions.length){
        callback(authResults);
      }
    });
  });
}
```

## 4. 状态显示模板

### 订单状态

```javascript
/**
 * 订单状态显示模板
 * @param {Object} d - 行数据对象
 * @returns {string} HTML 字符串
 */
function tplOrderStatus(d) {
  var statusMap = {
    0: '<span style="color: blue">订单生成</span>',
    1: '<span style="color: orangered">支付中</span>',
    2: '<span style="color: green">支付成功</span>',
    -1: '<span style="color: red">支付失败</span>',
    -2: '<span style="color: gray">订单过期</span>',
    3: '<span style="color: green">处理完成</span>',
    4: '<span style="color: orange">已退款</span>'
  };
  return statusMap[d.status] || d.status;
}
```

### 通用开关状态

```javascript
/**
 * 开关状态显示模板
 * @param {number} status - 状态值（0=关闭，1=开启）
 * @returns {string} HTML 字符串
 */
function tplSwitchStatus(status) {
  if (status == 0) {
    return "关闭";
  } else if (status == 1) {
    return "<span style='color: green'>开启</span>";
  }
  return status;
}
```

### 处理状态

```javascript
/**
 * 处理状态显示模板
 * @param {number} status - 状态值（0=未处理，1=已处理）
 * @returns {string} HTML 字符串
 */
function tplHandleStatus(status) {
  if (status == 0) {
    return "未处理";
  } else if (status == 1) {
    return "<span style='color: green'>已处理</span>";
  }
  return status;
}
```

## 5. 常用验证规则

### 表单验证规则

```javascript
// 在表单中定义验证规则
form.verify({
  // 必填
  required: function(value) {
    if (!value || value.trim() === '') {
      return '此项不能为空';
    }
  },

  // 手机号
  phone: [/^1[3-9]\d{9}$/, '请输入正确的手机号'],

  // 邮箱
  email: [/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/, '请输入正确的邮箱'],

  // 金额（支持小数）
  amount: [
    /^[1-9]\d{0,8}(\.\d{1,2})?$|^0(\.\d{1,2})?$/
    ,'请输入正确的金额格式'
  ],

  // 正整数
  positiveInt: [/^\d+$/, '请输入正整数'],

  // 百分比（0-100）
  percent: [
    /^(100|[1-9]?\d)(\.\d+)?$/
    ,'请输入0-100之间的数值'
  ],

  // URL
  url: [/^https?:\/\/.+/, '请输入正确的URL'],

  // 身份证号
  idCard: [/^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/, '请输入正确的身份证号'],

  // 自定义验证：密码（6-20位，字母数字组合）
  password: [/(?!^[0-9]+$)(?!^[a-zA-Z]+$)^[a-zA-Z0-9]{6,20}$/, '密码必须为6-20位字母数字组合']
});
```

### 使用验证

```html
<input type="text" name="amount" required lay-verify="required|amount" placeholder="请输入金额" class="layui-input">
```

## 6. 其他常用函数

### 复制到剪贴板

```javascript
/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 */
function copyToClipboard(text) {
  var input = document.createElement('input');
  input.value = text;
  document.body.appendChild(input);
  input.select();
  document.execCommand('copy');
  document.body.removeChild(input);
  layer.msg('已复制到剪贴板');
}
```

### 下载文件

```javascript
/**
 * 下载文件
 * @param {string} url - 文件 URL
 * @param {string} filename - 文件名
 */
function downloadFile(url, filename) {
  var link = document.createElement('a');
  link.href = url;
  link.download = filename || 'download';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
```

### 生成唯一ID

```javascript
/**
 * 生成唯一ID
 * @param {string} prefix - 前缀
 * @returns {string} 唯一ID
 */
function generateId(prefix) {
  prefix = prefix || 'id';
  return prefix + '_' + Date.now() + '_' + Math.floor(Math.random() * 10000);
}
```

### URL 参数解析

```javascript
/**
 * 获取 URL 参数
 * @param {string} name - 参数名
 * @param {string} url - URL 字符串，默认当前页面 URL
 * @returns {string|null} 参数值
 */
function getUrlParam(name, url) {
  url = url || window.location.href;
  var reg = new RegExp('[?&]' + name + '=([^&#]*)');
  var match = url.match(reg);
  return match ? decodeURIComponent(match[1]) : null;
}
```

### 防抖函数

```javascript
/**
 * 防抖函数
 * @param {Function} func - 要执行的函数
 * @param {number} wait - 等待时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
function debounce(func, wait) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      func.apply(context, args);
    }, wait);
  };
}

// 示例：搜索输入防抖
$('#searchInput').on('input', debounce(function() {
  // 执行搜索
}, 300));
```

### 节流函数

```javascript
/**
 * 节流函数
 * @param {Function} func - 要执行的函数
 * @param {number} wait - 等待时间（毫秒）
 * @returns {Function} 节流后的函数
 */
function throttle(func, wait) {
  var lastTime = 0;
  return function() {
    var now = Date.now();
    if (now - lastTime >= wait) {
      func.apply(this, arguments);
      lastTime = now;
    }
  };
}
```
