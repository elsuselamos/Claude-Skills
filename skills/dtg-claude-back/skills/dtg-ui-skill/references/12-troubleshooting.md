# Layui 常见问题解答

## Q1: 表单组件样式不显示？

**问题描述**：动态插入的表单元素，select、checkbox、radio 等样式不显示。

**原因**：动态插入的元素没有经过 Layui 的渲染。

**解决方案**：

```javascript
// 添加元素后重新渲染
$('#form').append('<select><option>选项</option></select>');
layui.use('form', function(){
  var form = layui.form;
  form.render();          // 更新全部
  form.render('select');  // 只更新 select
  form.render('checkbox'); // 只更新 checkbox
  form.render('radio');   // 只更新 radio
});
```

## Q2: 表格数据不显示？

**问题描述**：表格渲染成功，但是数据不显示。

**检查项**：

1. **接口返回数据格式是否正确**

```json
{
  "code": 0,
  "msg": "",
  "count": 100,
  "data": [
    {"id": 1, "username": "张三"}
  ]
}
```

2. **字段名是否匹配**

```javascript
cols: [[
  {field: 'username', title: '用户名'} // field 必须与数据字段名一致
]]
```

3. **自定义数据格式**

```javascript
table.render({
  parseData: function(res){
    return {
      "code": res.status,
      "msg": res.message,
      "count": res.total,
      "data": res.list
    };
  }
});
```

## Q3: 弹层被遮挡？

**问题描述**：弹层被其他元素遮挡，无法显示。

**解决方案**：

```javascript
layer.open({
  zIndex: layer.zIndex,  // 使用当前最大 zIndex
  success: function(){
    layer.zIndex += 2;   // 提升 zIndex
  }
});

// 或者设置更高的 zIndex
layer.open({
  zIndex: 99999
});
```

## Q4: 日期选择器不显示？

**问题描述**：点击日期输入框，日期选择器不显示。

**检查项**：

1. **elem 必须是选择器字符串**

```javascript
// 正确
laydate.render({
  elem: '#date'
});

// 错误
laydate.render({
  elem: $('#date') // 不要使用 jQuery 对象
});
```

2. **type 参数是否正确**

```javascript
laydate.render({
  elem: '#date',
  type: 'date' // year, month, date, time, datetime
});
```

3. **容器是否可见**

```javascript
// 确保容器是可见的
$('#date').show();
laydate.render({elem: '#date'});
```

## Q5: 上传无反应？

**问题描述**：点击上传按钮没有反应。

**检查项**：

1. **url 是否正确**

```javascript
upload.render({
  elem: '#upload',
  url: '/api/upload', // 检查 URL 是否正确
  done: function(res){
    console.log(res);
  }
});
```

2. **后端返回格式是否正确**

```json
{
  "code": 0,  // 必须是 0 表示成功
  "msg": "",
  "data": {}
}
```

3. **是否跨域**

```javascript
upload.render({
  elem: '#upload',
  url: 'http://other-domain.com/api/upload',
  headers: {
    'Access-Control-Allow-Origin': '*'
  }
});
```

4. **文件类型限制**

```javascript
upload.render({
  elem: '#upload',
  url: '/api/upload',
  accept: 'images', // images, files, video, audio
  exts: 'jpg|png|gif' // 允许的文件后缀
});
```

## Q6: 栅格布局不生效？

**问题描述**：栅格布局没有效果。

**检查项**：

1. **是否引入 IE8/9 兼容脚本**

```html
<!--[if lt IE 9]>
  <script src="https://cdn.staticfile.org/html5shiv/r29/html5.min.js"></script>
  <script src="https://cdn.staticfile.org/respond.js/1.4.2/respond.min.js"></script>
<![endif]-->
```

2. **父容器是否是 layui-container**

```html
<!-- 正确 -->
<div class="layui-container">
  <div class="layui-row">
    <div class="layui-col-md6">内容</div>
  </div>
</div>

<!-- 错误：缺少容器 -->
<div class="layui-row">
  <div class="layui-col-md6">内容</div>
</div>
```

3. **列宽是否正确**

```html
<!-- 总和必须是 12 -->
<div class="layui-col-md4">33%</div>
<div class="layui-col-md8">67%</div>
```

## Q7: 模块加载失败？

**问题描述**：提示模块加载失败。

**解决方案**：

1. **检查 layui.js 路径**

```html
<script src="./layui/layui.js"></script>
```

2. **检查 layui 目录结构**

```
layui/
├── css/
│   └── layui.css
├── fonts/
└── layui.js
```

3. **配置 layui 目录**

```javascript
layui.config({
  dir: '/layui/' // layui.js 所在目录
});
```

## Q8: 表格分页不显示？

**问题描述**：表格分页不显示。

**解决方案**：

```javascript
table.render({
  elem: '#demo',
  url: '/api/data',
  page: true,  // 确保开启分页
  limits: [10, 20, 30, 50],  // 每页条数选项
  limit: 10,  // 每页显示条数
});
```

## Q9: 选项卡切换失败？

**问题描述**：点击选项卡无法切换。

**解决方案**：

1. **确保元素初始化**

```javascript
layui.use('element', function(){
  var element = layui.element;
  // 选项卡会自动初始化
});
```

2. **检查 lay-filter 是否一致**

```html
<div class="layui-tab" lay-filter="demo">
  <ul class="layui-tab-title">
    <li class="layui-this">选项卡1</li>
  </ul>
</div>

<script>
// 监听时 filter 必须一致
element.on('tab(demo)', function(data){
  console.log(data.index);
});
</script>
```

## Q10: 图标不显示？

**问题描述**：图标显示为方块或空白。

**解决方案**：

1. **检查字体文件路径**

```css
@font-face {
  font-family: 'layui-icon';
  src: url('../fonts/iconfont.eot');
  /* 确保路径正确 */
}
```

2. **检查图标代码是否正确**

```html
<i class="layui-icon">&#xe620;</i>  <!-- 使用 Unicode -->
<i class="layui-icon layui-icon-home"></i>  <!-- 使用 class -->
```

3. **清除缓存**

```javascript
// 强制刷新缓存
location.reload(true);
```

## Q11: 弹层内容被截断？

**问题描述**：弹层内容超出高度被截断。

**解决方案**：

```javascript
layer.open({
  type: 1,
  area: ['800px', '600px'],  // 设置足够大的宽高
  content: $('#content'),
  scrollbar: true  // 允许滚动条
});
```

## Q12: 表格固定列错位？

**问题描述**：表格固定列与内容列不对齐。

**解决方案**：

```javascript
table.render({
  elem: '#demo',
  url: '/api/data',
  height: 'full-100',  // 使用高度计算
  cols: [[
    {fixed: 'left', field: 'id', title: 'ID'},
    {field: 'username', title: '用户名'}
  ]],
  done: function(){
    // 渲染完成后重新计算
    $('.layui-table-fixed').css('height', 'auto');
  }
});
```

## Q13: 动态添加的导航无法点击？

**问题描述**：动态添加的导航项点击无反应。

**解决方案**：

```javascript
// 添加导航后重新渲染
$('#nav').append('<li class="layui-nav-item"><a href="">新导航</a></li>');
layui.use('element', function(){
  var element = layui.element;
  element.render('nav');
});
```

## Q14: 日期选择器范围选择无效？

**问题描述**：日期范围选择器无法选择。

**解决方案**：

```javascript
laydate.render({
  elem: '#dateRange',
  type: 'date',
  range: '~',  // 或 true
  rangeLinked: true  // 开启范围选择联动
});
```

## Q15: 文件上传进度不显示？

**问题描述**：文件上传没有进度显示。

**解决方案**：

```javascript
upload.render({
  elem: '#upload',
  url: '/api/upload',
  progress: function(n, elem, res, index){
    var percent = n + '%';
    elem.html(percent);  // 显示进度
  }
});
```

## 调试建议

1. **使用浏览器开发者工具**：检查网络请求、控制台错误
2. **开启 Layui 调试模式**：`layui.config({debug: true})`
3. **打印对象**：`console.log(layer, form, table)`
4. **检查版本**：确保使用 Layui 2.3.0 或兼容版本

## 获取帮助

- 官网：http://www.layui.com/
- 文档：http://www.layui.com/doc/
- 社区：http://fly.layui.com/
