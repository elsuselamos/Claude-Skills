# Layui 快速入门指南

## 引入 Layui

### 方法一：模块化方式（推荐）

适用于需要按需加载模块的场景：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>开始使用 Layui</title>
  <link rel="stylesheet" href="./layui/css/layui.css">
</head>
<body>

<!-- 你的 HTML 代码 -->

<script src="./layui/layui.js"></script>
<script>
layui.use(['layer', 'form'], function(){
  var layer = layui.layer
  ,form = layui.form;

  layer.msg('Hello World');
});
</script>
</body>
</html>
```

### 方法二：非模块化方式

适用于所有模块一次性加载的场景：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>非模块化方式使用 Layui</title>
  <link rel="stylesheet" href="./layui/css/layui.css">
</head>
<body>

<!-- 你的 HTML 代码 -->

<script src="./layui/layui.all.js"></script>
<script>
//由于模块都一次性加载，因此不用执行 layui.use()
var layer = layui.layer;
var form = layui.form;

layer.msg('Hello World');
</script>
</body>
</html>
```

## 基础页面结构

### 标准页面模板

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>我的 Layui 页面</title>
  <link rel="stylesheet" href="./layui/css/layui.css">
  <style>
    body { padding: 20px; }
  </style>
</head>
<body>
  <div class="layui-container">
    <h1>页面标题</h1>
    <div class="layui-row">
      <div class="layui-col-md12">
        <!-- 页面内容 -->
      </div>
    </div>
  </div>

  <script src="./layui/layui.js"></script>
  <script>
  layui.use(['layer', 'form', 'element'], function(){
    var layer = layui.layer;
    var form = layui.form;
    var element = layui.element;

    // 在这里编写你的代码
  });
  </script>
</body>
</html>
```

## 17 个核心模块速查表

| 模块名 | 文件名 | 大小 | 说明 | 触发词 |
|--------|--------|------|------|--------|
| jQuery | jquery.js | 293KB | 基础库 | - |
| 工具函数 | util.js | 5.4KB | 常用工具方法 | util, fixbar, countdown |
| 弹层 | layer.js | 39.4KB | 弹窗、提示、遮罩 | modal, dialog, popup, alert, confirm, msg |
| 表单 | form.js | 22.2KB | 表单组件与验证 | form, input, select, checkbox, radio |
| 表格 | table.js | 42.5KB | 数据表格 | table, grid, data |
| 日期 | laydate.js | 58.3KB | 日期时间选择器 | date, time, calendar, datetime |
| 常用元素 | element.js | 15.4KB | Tab、导航等 | tab, nav, accordion, progress |
| 上传 | upload.js | 15KB | 文件上传 | upload, file upload, image upload |
| 分页 | laypage.js | 9.2KB | 分页组件 | pagination, pager |
| 树形 | tree.js | 6KB | 树形结构 | tree, tree menu |
| 轮播 | carousel.js | 8.3KB | 轮播图 | carousel, slider |
| 流加载 | flow.js | 5.2KB | 无限滚动 | flow, infinite scroll, lazy load |
| 评分 | rate.js | 6KB | 评分组件 | rate, star rating |
| 富文本 | layedit.js | 21.7KB | 富文本编辑器 | editor, rich text |
| 代码修饰 | code.js | 1.9KB | 代码高亮 | code, syntax highlight |
| 模板引擎 | laytpl.js | 3.2KB | 模板解析 | template |

## 模块加载方式

### 加载单个模块

```javascript
layui.use('layer', function(){
  var layer = layui.layer;
  layer.msg('加载成功');
});
```

### 加载多个模块

```javascript
layui.use(['layer', 'form', 'table'], function(){
  var layer = layui.layer;
  var form = layui.form;
  var table = layui.table;
});
```

### 扩展模块加载

如果使用了扩展模块，需要先配置模块路径：

```javascript
layui.config({
  base: '/js/' // 扩展模块所在目录
}).extend({
  mod1: 'mod1' // 模块别名对应模块文件名
});

layui.use('mod1', function(){
  // 使用扩展模块
});
```

## 模块依赖关系

```
table 依赖: laytpl, laypage, layer, form
form   依赖: layer
upload 依赖: layer
layedit 依赖: layer
```

注意：当使用这些模块时，Layui 会自动加载其依赖模块。

## 路径建议

```
项目目录/
├── layui/
│   ├── css/
│   │   └── layui.css
│   ├── fonts/
│   ├── layui.js
│   └── layui.all.js (可选)
└── index.html
```

引用路径：
```html
<link rel="stylesheet" href="./layui/css/layui.css">
<script src="./layui/layui.js"></script>
```

## 下一步

- 了解模块总览 → `02-module-overview.md`
- 学习布局系统 → `03-layout-system.md`
- 查看表单模块 → `04-form-module.md`
