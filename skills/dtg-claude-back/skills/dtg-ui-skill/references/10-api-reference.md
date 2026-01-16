# Layui API 速查手册

## 模块加载

### layui.use()

加载 Layui 模块：

```javascript
// 加载单个模块
layui.use('layer', function(){
  var layer = layui.layer;
});

// 加载多个模块
layui.use(['layer', 'form', 'table'], function(){
  var layer = layui.layer;
  var form = layui.form;
  var table = layui.table;
});
```

### layui.extend()

扩展模块：

```javascript
layui.extend({
  mod1: 'js/mod1'
});

layui.use('mod1', function(){
  // 使用扩展模块
});
```

### layui.config()

全局配置：

```javascript
layui.config({
  dir: '/layui/', // layui.js 所在目录
  version: false, // 版本号
  debug: false, // 调试模式
  base: '' // 扩展模块目录
});
```

## 全局对象

### layui.$

jQuery 对象：

```javascript
layui.$('#id').html();
```

### layui.layer

弹层模块：

```javascript
layui.layer.msg('消息');
```

### layui.form

表单模块：

```javascript
layui.form.render();
```

### layui.table

表格模块：

```javascript
layui.table.render({...});
```

### layui.element

元素模块：

```javascript
layui.element.tabAdd(...);
```

### layui.laydate

日期模块：

```javascript
layui.laydate.render({...});
```

### layui.upload

上传模块：

```javascript
layui.upload.render({...});
```

### layui.util

工具模块：

```javascript
layui.util.fixbar({...});
```

## layer API

### 基础方法

```javascript
// 信息框
layer.alert(content, options, yes)

// 询问框
layer.confirm(content, options, yes, cancel)

// 提示框
layer.msg(content, options, end)

// 吸附提示
layer.tips(content, follow, options)

// 页面层
layer.open(options)

// iframe 层
layer.iframe(options)

// 加载层
layer.load(icon, options)

// 输入框
layer.prompt(options, yes)
```

### 关闭方法

```javascript
// 关闭特定层
layer.close(index)

// 关闭所有层
layer.closeAll()

// 关闭特定类型层
layer.closeAll('page')
layer.closeAll('iframe')
layer.closeAll('loading')
```

### 获取索引

```javascript
// 获取当前最大 zIndex
layer.zIndex

// 获取当前弹层索引
var index = layer.open({...});
```

## form API

### 渲染方法

```javascript
// 更新全部
form.render()

// 更新特定类型
form.render('select')
form.render('checkbox')
form.render('radio')
```

### 赋值/取值

```javascript
// 赋值
form.val(filter, object)

// 取值
form.on('submit(filter)', function(data){
  console.log(data.field);
})
```

### 验证

```javascript
// 自定义验证规则
form.verify({
  username: function(value){
    if(!/^\w{5,10}$/.test(value)){
      return '用户名必须5到10位';
    }
  }
})
```

## table API

### 渲染表格

```javascript
table.render({
  elem: '#id',
  url: '/api/data',
  cols: [[...]],
  page: true
})
```

### 重载表格

```javascript
table.reload(id, options)
```

### 获取数据

```javascript
// 获取选中行数据
table.checkStatus(id)

// 获取表格所有数据
table.getData(id)
```

### 事件监听

```javascript
// 行工具事件
table.on('event(filter)', function(obj){})

// 工具条事件
table.on('toolbar(filter)', function(obj){})

// 复选框事件
table.on('checkbox(filter)', function(obj){})

// 编辑事件
table.on('edit(filter)', function(obj){})

// 排序事件
table.on('sort(filter)', function(obj){})
```

## element API

### 选项卡

```javascript
// 添加选项卡
element.tabAdd(filter, options)

// 删除选项卡
element.tabDelete(filter, id)

// 切换选项卡
element.tabChange(filter, id)

// 获取选项卡数量
element.tabLength(filter)
```

### 进度条

```javascript
// 设置进度
element.progress(filter, percent)
```

### 事件监听

```javascript
// 导航事件
element.on('nav(filter)', function(elem){})

// 选项卡事件
element.on('tab(filter)', function(data){})

// 折叠面板事件
element.on('collapse(filter)', function(data){})
```

## laydate API

### 渲染日期

```javascript
laydate.render({
  elem: '#id',
  type: 'date',
  format: 'yyyy-MM-dd'
})
```

## upload API

### 渲染上传

```javascript
upload.render({
  elem: '#id',
  url: '/api/upload',
  done: function(res){}
})
```

### 重载上传

```javascript
upload.reload(id, options)
```

## laypage API

### 渲染分页

```javascript
laypage.render({
  elem: 'id',
  count: 100,
  jump: function(obj, first){}
})
```

## 工具方法

### layui.util.toDateString()

时间戳转日期：

```javascript
layui.util.toDateString(timestamp, 'yyyy-MM-dd HH:mm:ss')
```

### layui.util.fixbar()

固定块：

```javascript
layui.util.fixbar({
  bar1: true,
  bar2: true,
  css: {right: 50, bottom: 100},
  click: function(type){}
})
```

### layui.util.timeAgo()

相对时间：

```javascript
layui.util.timeAgo(timestamp, now)
```

## 快捷方法

### layui.data()

本地存储：

```javascript
// 存储数据
layui.data('test', {key: 'value'});

// 读取数据
layui.data('test');

// 删除数据
layui.data('test', null);

// 删除表
layui.data('test', {
  key: null,
  remove: true
});
```

### layui.device()

获取设备信息：

```javascript
var device = layui.device();
console.log(device.weixin); // 是否微信
console.log(device.android); // 是否安卓
console.log(device.ios); // 是否 iOS
```

## 常用选项

### 基础选项

| 选项 | 类型 | 说明 |
|------|------|------|
| elem | string/DOM | 指定容器 |
| url | string | 请求地址 |
| type | string | 请求类型 |
| data | object | 携带参数 |
| method | string | 请求方法 |
| dataType | string | 响应类型 |
| done | function | 完成回调 |

### 样式选项

| 选项 | 说明 |
|------|------|
| layui-bg-black | 黑色背景 |
| layui-bg-gray | 灰色背景 |
| layui-bg-blue | 蓝色背景 |
| layui-bg-cyan | 青色背景 |
| layui-bg-green | 绿色背景 |
| layui-bg-orange | 橙色背景 |
| layui-bg-red | 红色背景 |

## 下一步

- 查看最佳实践 → `11-best-practices.md`
- 查看常见问题 → `12-troubleshooting.md`
