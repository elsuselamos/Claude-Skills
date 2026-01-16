# Layui 最佳实践

## 1. 模块化使用

### 按需加载

```javascript
// 推荐：按需加载
layui.use(['layer', 'form'], function(){
  var layer = layui.layer;
  var form = layui.form;
});

// 避免：一次性加载所有模块
layui.use(['layer', 'form', 'table', 'laydate', 'upload', 'laypage', 'element'], function(){
  // 不推荐这样做，会增加加载时间
});
```

### 模块复用

```javascript
// 推荐：将常用模块提取为变量
layui.use(['layer', 'form', 'table'], function(){
  var layer = layui.layer;
  var form = layui.form;
  var table = layui.table;

  // 多次使用这些变量
  layer.msg('消息');
  form.render();
  table.render({...});
});
```

## 2. 事件委托

### 动态元素事件

```javascript
// 推荐：使用事件委托
$(document).on('click', '.my-btn', function(){
  // 这样可以处理动态添加的元素
});

// 避免：直接绑定
$('.my-btn').on('click', function(){
  // 这样无法处理动态添加的元素
});
```

### 表单动态渲染

```javascript
// 添加动态元素后，需要重新渲染
$('#form').append('<select>...</select>');
form.render('select');
```

## 3. 表单验证

### 自定义验证规则

```javascript
form.verify({
  username: [
    /^\w{5,10}$/,
    '用户名必须5到10位'
  ],
  phone: [
    /^1\d{10}$/,
    '手机号格式不正确'
  ],
  password: [
    /^[\S]{6,12}$/,
    '密码必须6到12位，且不能出现空格'
  ],
  equalTo: function(value){
    if(value !== $('#password').val()){
      return '两次密码输入不一致';
    }
  }
});
```

### 异步验证

```javascript
form.verify({
  username: function(value, item){
    var msg;
    $.ajax({
      url: '/api/checkUsername',
      data: {username: value},
      async: false,
      success: function(res){
        if(res.code === 1){
          msg = '用户名已存在';
        }
      }
    });
    return msg;
  }
});
```

## 4. 表格性能优化

### 固定高度

```javascript
table.render({
  height: 500, // 固定高度，启用虚拟滚动
  page: true,
  limit: 20    // 合理的每页数量
});
```

### 延迟加载

```javascript
// 使用 done 回调处理数据
table.render({
  url: '/api/data',
  done: function(res, curr, count){
    // 渲染完成后执行
  }
});
```

### 合理使用分页

```javascript
table.render({
  page: {
    layout: ['count', 'prev', 'page', 'next', 'limit', 'skip'],
    limits: [10, 20, 30, 50],
    limit: 20
  }
});
```

## 5. 弹层管理

### 记录弹层索引

```javascript
// 推荐：记录索引，方便关闭
var index = layer.open({...});
layer.close(index);

// 避免：盲目关闭所有弹层
layer.closeAll();
```

### 层级管理

```javascript
// 自动提升层级
layer.open({
  zIndex: layer.zIndex,
  success: function(){
    layer.zIndex += 2;
  }
});
```

### 弹层复用

```javascript
// 推荐：复用弹层内容
var layerIndex;
function showLayer(){
  if(layerIndex){
    layer.close(layerIndex);
  }
  layerIndex = layer.open({...});
}
```

## 6. 响应式设计

### 栅格断点

```html
<!-- 移动端优先 -->
<div class="layui-col-xs12 layui-col-sm6 layui-col-md4 layui-col-lg3">
  响应式内容
</div>
```

### 隐藏/显示

```html
<!-- 移动端隐藏 -->
<div class="layui-hide-md">
  只在移动端显示
</div>

<!-- 桌面端隐藏 -->
<div class="layui-hide-xs layui-hide-sm">
  只在桌面端显示
</div>
```

### 响应式工具

```javascript
// 根据屏幕大小调整
layui.device();
if(layui.device().android || layui.device().ios){
  // 移动端处理
} else {
  // 桌面端处理
}
```

## 7. 数据交互

### 统一数据格式

```javascript
// 后端统一返回格式
{
  "code": 0,      // 0 表示成功
  "msg": "success",
  "count": 100,   // 数据总数
  "data": []      // 数据列表
}
```

### 错误处理

```javascript
table.render({
  url: '/api/data',
  error: function(){
    layer.msg('数据加载失败');
  }
});
```

### 请求拦截

```javascript
// 统一添加 token
$.ajaxSetup({
  headers: {
    'X-Token': localStorage.getItem('token')
  }
});
```

## 8. 代码组织

### 模块化代码

```javascript
// 推荐：模块化组织代码
var app = {
  init: function(){
    this.bindEvents();
    this.loadData();
  },
  bindEvents: function(){
    // 绑定事件
  },
  loadData: function(){
    // 加载数据
  }
};

layui.use(['layer', 'form'], function(){
  app.init();
});
```

### 配置分离

```javascript
// 推荐：配置与代码分离
var config = {
  api: {
    list: '/api/list',
    save: '/api/save',
    delete: '/api/delete'
  },
  pageSize: 20
};

table.render({
  url: config.api.list,
  limit: config.pageSize
});
```

## 9. 性能优化

### 减少重绘

```javascript
// 推荐：批量操作 DOM
var html = '';
data.forEach(function(item){
  html += '<div>' + item.name + '</div>';
});
$('#container').html(html);

// 避免：频繁操作 DOM
data.forEach(function(item){
  $('#container').append('<div>' + item.name + '</div>');
});
```

### 防抖与节流

```javascript
// 推荐：使用防抖
var debounce = function(fn, delay){
  var timer;
  return function(){
    clearTimeout(timer);
    timer = setTimeout(function(){
      fn.apply(this, arguments);
    }, delay);
  };
};

$('#input').on('input', debounce(function(){
  // 搜索操作
}, 300));
```

### 图片懒加载

```javascript
// 使用 Layui 的流加载
layui.use('flow', function(){
  var flow = layui.flow;
  flow.load({
    elem: '#container',
    isLazyimg: true,
    done: function(page, next){
      // 加载图片
    }
  });
});
```

## 10. 安全建议

### XSS 防护

```javascript
// 推荐：转义 HTML
function escapeHtml(text){
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// 使用 Layui 的代码修饰器
<pre class="layui-code" lay-encode="true">
  <script>alert('xss')</script>
</pre>
```

### CSRF 防护

```javascript
// 推荐：使用 token
$.ajaxSetup({
  headers: {
    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
  }
});
```

## 11. 调试技巧

### 开启调试模式

```javascript
layui.config({
  debug: true
});
```

### 控制台输出

```javascript
// 检查元素是否选中
console.log($('#id').length);

// 检查数据格式
console.log(data);

// 检查 Layui 对象
console.log(layui);
```

## 下一步

- 查看常见问题 → `12-troubleshooting.md'
