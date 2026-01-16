# Layui 弹层模块详解

## 基础弹层类型

### 1. alert - 信息框

```javascript
// 基础用法
layer.alert('你好');

// 带图标
layer.alert('操作成功', {icon: 1});

// 带回调
layer.alert('确定删除吗？', {
  icon: 3,
  title: '提示'
}, function(index){
  // 确定后执行
  layer.close(index);
});
```

**icon 参数**：
- `0` - 叹息
- `1` - 成功
- `2` - 失败
- `3` - 疑问
- `4` - 锁定
- `5` - 哭脸
- `6` - 笑脸

### 2. confirm - 询问框

```javascript
// 基础用法
layer.confirm('确定删除吗？');

// 自定义按钮
layer.confirm('确定删除吗？', {
  btn: ['确定','取消']
}, function(index){
  // 确定回调
  layer.close(index);
}, function(index){
  // 取消回调
  layer.close(index);
});
```

### 3. msg - 提示框

```javascript
// 基础用法
layer.msg('操作成功');

// 带图标
layer.msg('操作成功', {icon: 1});

// 自动关闭时间
layer.msg('操作成功', {
  icon: 1,
  time: 2000 // 2秒后关闭
});

// 关闭后回调
layer.msg('操作成功', {
  icon: 1,
  time: 2000
}, function(){
  // 关闭后执行
});
```

### 4. tips - 吸附提示

```javascript
// 在元素右侧显示
layer.tips('提示内容', '#id');

// 配置方向
layer.tips('提示内容', '#id', {
  tips: 1 // 上:1, 右:2, 下:3, 左:4
});

// 配置颜色
layer.tips('提示内容', '#id', {
  tips: [1, '#0FA6D8'], // 方向, 颜色
  time: 5000
});
```

## 高级弹层

### 5. 页面层（type: 1）

在页面中弹出 DOM 元素：

```javascript
layer.open({
  type: 1,
  title: '标题',
  area: ['500px', '300px'],
  content: $('#id') // 这里的 content 是 DOM 对象
});

// 或者使用 HTML 字符串
layer.open({
  type: 1,
  title: '标题',
  area: ['500px', '300px'],
  content: '<div style="padding:20px;">内容</div>'
});
```

### 6. iframe 层（type: 2）

弹出 iframe 页面：

```javascript
layer.open({
  type: 2,
  title: 'iframe 页面',
  area: ['800px', '600px'],
  content: 'http://example.com'
});

// 滚动条
layer.open({
  type: 2,
  content: 'http://example.com',
  scrollbar: false
});
```

### 7. 加载层（type: 3）

```javascript
// 基础加载层
var index = layer.load();
// 关闭
layer.close(index);

// 带样式
var index = layer.load(1);
// 0-2 表示不同样式

// 自定义样式
var index = layer.load(1, {
  shade: [0.1, '#fff'] // 透明度, 颜色
});
```

### 8. prompt - 输入框

```javascript
// 基础用法
layer.prompt({
  title: '输入任何值',
}, function(value, index){
  layer.msg('得到：'+value);
  layer.close(index);
});

// 表单类型
layer.prompt({
  formType: 0, // 0:文本, 1:密码, 2:多行文本
  value: '初始值',
  title: '请输入值'
}, function(value, index){
  layer.msg('得到：'+value);
});
```

## 常用参数

### type - 弹层类型

```javascript
layer.open({
  type: 0, // 信息框（默认）
  type: 1, // 页面层
  type: 2, // iframe 层
  type: 3, // 加载层
  type: 4, // tips 层
});
```

### title - 标题

```javascript
layer.open({
  title: '我是标题',
  // 或不显示标题
  title: false
});
```

### area - 宽高

```javascript
layer.open({
  area: ['500px', '300px'],
  // 固定宽度，自适应高度
  area: '500px'
});
```

### offset - 坐标

```javascript
layer.open({
  offset: 'auto', // 默认坐标，垂直水平居中
  offset: '100px', // 只定义 top 坐标，水平居中
  offset: ['100px', '50px'], // [top, left]
  offset: 't', // 顶部
  offset: 'r', // 右侧
  offset: 'b', // 底部
  offset: 'l', // 左侧
  offset: 'lt', // 左上角
  offset: 'lb', // 左下角
  offset: 'rt', // 右上角
  offset: 'rb', // 右下角
});
```

### icon - 图标

```javascript
layer.msg('成功', {icon: 1});
layer.msg('失败', {icon: 2});
layer.msg('疑问', {icon: 3});
```

### btn - 按钮

```javascript
layer.open({
  btn: ['按钮一', '按钮二', '按钮三'],
  yes: function(index, layero){
    // 按钮1的回调
    layer.close(index);
  },
  btn2: function(index, layero){
    // 按钮2的回调
    // return false 开启该按钮的防点击
  }
});
```

### closeBtn - 关闭按钮

```javascript
layer.open({
  closeBtn: 0, // 不显示关闭按钮
  closeBtn: 1, // 默认风格
  closeBtn: 2, // 另一风格
});
```

### shade - 遮罩

```javascript
layer.open({
  shade: 0.3, // 遮罩透明度
  shade: [0.3, '#000'], // 透明度, 颜色
  shadeClose: true, // 点击遮罩关闭
});
```

### time - 自动关闭

```javascript
layer.msg('3秒后自动关闭', {
  time: 3000
});

// 不自动关闭
layer.msg('不自动关闭', {
  time: 0
});
```

### anim - 动画

```javascript
layer.open({
  anim: 0, // 平滑放大
  anim: 1, // 从上掉落
  anim: 2, // 从最底部往上滑入
  anim: 3, // 从左翻入
  anim: 4, // 从左翻入
  anim: 5, // 渐显
  anim: 6, // 抖动
});
```

### zIndex - 层级

```javascript
layer.open({
  zIndex: layer.zIndex, // 获取当前最大 zIndex
  success: function(){
    layer.zIndex += 2; // 提升 zIndex
  }
});
```

### maxmin - 最大化最小化

```javascript
layer.open({
  type: 1,
  maxmin: true,
  content: $('#id')
});
```

## 弹层方法

### layer.open()

核心方法，创建弹层：

```javascript
var index = layer.open({
  type: 1,
  title: '标题',
  content: $('#id')
});
```

### layer.close()

关闭特定层：

```javascript
layer.close(index); // 关闭指定层
layer.closeAll(); // 关闭所有层
layer.closeAll('page'); // 关闭所有页面层
layer.closeAll('iframe'); // 关闭所有 iframe 层
layer.closeAll('loading'); // 关闭所有加载层
```

### layer.msg()

快捷方法，提示框：

```javascript
layer.msg('提示信息');
```

### layer.alert()

快捷方法，信息框：

```javascript
layer.alert('信息');
```

### layer.confirm()

快捷方法，询问框：

```javascript
layer.confirm('确定吗？', function(index){
  layer.close(index);
});
```

### layer.load()

快捷方法，加载层：

```javascript
var index = layer.load(0);
// 业务逻辑
layer.close(index);
```

### layer.tips()

快捷方法，吸附提示：

```javascript
layer.tips('提示', '#id');
```

## 获取 iframe 中的元素

```javascript
layer.open({
  type: 2,
  content: 'iframe.html',
  success: function(layero, index){
    var iframe = window['layui-layer-iframe' + index];
    // 获取 iframe 中的元素
    iframe.getElementById('id');
    // 或者使用 jQuery
    var iframeWindow = window[layero.find('iframe')[0]['name']];
    var $ = iframeWindow.$;
  }
});
```

## 父页面调用 iframe 方法

```javascript
// 在 iframe 页面中定义方法
window.parentMethod = function(){
  // 方法内容
};

// 在父页面中调用
layer.open({
  type: 2,
  content: 'iframe.html',
  end: function(){
    // iframe 关闭后执行
  }
});
```

## iframe 调用父页面方法

```javascript
// 在 iframe 中
var index = parent.layer.getFrameIndex(window.name);
parent.layer.close(index);

// 调用父页面方法
parent.parentMethod();
```

## 完整示例

```javascript
layui.use('layer', function(){
  var layer = layui.layer;

  // 信息框
  layer.alert('基本信息');

  // 询问框
  layer.confirm('确定删除吗？', {
    icon: 3,
    title: '提示'
  }, function(index){
    // 确定后执行
    layer.close(index);
  });

  // 提示框
  layer.msg('操作成功', {icon: 1});

  // 页面层
  layer.open({
    type: 1,
    title: '用户信息',
    area: ['500px', '300px'],
    content: '<div style="padding:20px;">用户详情内容</div>',
    btn: ['确定', '取消'],
    yes: function(index){
      layer.close(index);
    }
  });

  // iframe 层
  layer.open({
    type: 2,
    title: '编辑用户',
    area: ['800px', '600px'],
    content: '/user/edit'
  });

  // 加载层
  var index = layer.load(1);
  setTimeout(function(){
    layer.close(index);
  }, 2000);
});
```

## 下一步

- 查看导航组件 → `07-navigation.md`
- 查看表单模块 → `04-form-module.md`
