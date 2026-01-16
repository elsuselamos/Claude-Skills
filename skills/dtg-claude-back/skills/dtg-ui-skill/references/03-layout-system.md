# Layui 布局系统

## 栅格布局系统

Layui 采用 12 列栅格系统，支持响应式设计。

### 栅格参数

| 类名 | 说明 | 屏幕宽度 |
|------|------|----------|
| layui-col-xs* | 超小屏幕 | < 768px |
| layui-col-sm* | 小屏幕 | ≥ 768px |
| layui-col-md* | 中等屏幕 | ≥ 992px |
| layui-col-lg* | 大屏幕 | ≥ 1200px |

### 基础栅格

```html
<div class="layui-container">
  <div class="layui-row">
    <div class="layui-col-xs6 layui-col-md4">
      50% 移动，33.33% 桌面
    </div>
    <div class="layui-col-xs6 layui-col-md8">
      50% 移动，66.67% 桌面
    </div>
  </div>
</div>
```

### 列偏移

```html
<div class="layui-row">
  <div class="layui-col-md4">
    列1
  </div>
  <div class="layui-col-md4 layui-col-md-offset4">
    列2（向右偏移4列）
  </div>
</div>
```

### 列嵌套

```html
<div class="layui-row">
  <div class="layui-col-md6">
    <div class="layui-row">
      <div class="layui-col-md6">嵌套1</div>
      <div class="layui-col-md6">嵌套2</div>
    </div>
  </div>
</div>
```

### 列间隔

使用 `layui-col-space*` 类设置列之间的间距：

```html
<!-- 间距 3px -->
<div class="layui-row layui-col-space3">
  <div class="layui-col-md4">列1</div>
  <div class="layui-col-md4">列2</div>
  <div class="layui-col-md4">列3</div>
</div>

<!-- 间距 15px -->
<div class="layui-row layui-col-space15">
  <div class="layui-col-md4">列1</div>
  <div class="layui-col-md4">列2</div>
  <div class="layui-col-md4">列3</div>
</div>
```

可选值：`layui-col-space1` ~ `layui-col-space30`

## 容器

### layui-container

固定宽度居中容器：

```html
<div class="layui-container">
  <!-- 内容 -->
</div>
```

### layui-fluid

流体容器（100% 宽度）：

```html
<div class="layui-fluid">
  <!-- 内容 -->
</div>
```

## 后台布局

### 经典后台布局结构

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>后台布局</title>
  <link rel="stylesheet" href="./layui/css/layui.css">
</head>
<body class="layui-layout-body">

<div class="layui-layout layui-layout-admin">
  <!-- 头部 -->
  <div class="layui-header">
    <div class="layui-logo">Layui 后台</div>
    <ul class="layui-nav layui-layout-left">
      <li class="layui-nav-item"><a href="">控制台</a></li>
      <li class="layui-nav-item"><a href="">商品管理</a></li>
      <li class="layui-nav-item">
        <a href="javascript:;">其它</a>
        <dl class="layui-nav-child">
          <dd><a href="">邮件管理</a></dd>
          <dd><a href="">消息管理</a></dd>
        </dl>
      </li>
    </ul>
    <ul class="layui-nav layui-layout-right">
      <li class="layui-nav-item">
        <a href="javascript:;">
          <img src="http://t.cn/RCzsdCq" class="layui-nav-img">
          贤心
        </a>
        <dl class="layui-nav-child">
          <dd><a href="">基本资料</a></dd>
          <dd><a href="">安全设置</a></dd>
        </dl>
      </li>
      <li class="layui-nav-item"><a href="">退了</a></li>
    </ul>
  </div>

  <!-- 侧边栏 -->
  <div class="layui-side layui-bg-black">
    <div class="layui-side-scroll">
      <ul class="layui-nav layui-nav-tree" lay-filter="test">
        <li class="layui-nav-item layui-nav-itemed">
          <a href="">所有商品</a>
          <dl class="layui-nav-child">
            <dd><a href="javascript:;">列表一</a></dd>
            <dd><a href="javascript:;">列表二</a></dd>
          </dl>
        </li>
        <li class="layui-nav-item">
          <a href="">解决方案</a>
        </li>
        <li class="layui-nav-item"><a href="">云市场</a></li>
        <li class="layui-nav-item"><a href="">发布商品</a></li>
      </ul>
    </div>
  </div>

  <!-- 主体内容 -->
  <div class="layui-body">
    <div style="padding: 15px;">
      <!-- 内容区域 -->
      内容主体
    </div>
  </div>

  <!-- 底部 -->
  <div class="layui-footer">
    © 底部固定区域
  </div>
</div>

<script src="./layui/layui.js"></script>
<script>
layui.use('element', function(){
  var element = layui.element;
});
</script>
</body>
</html>
```

## 响应式工具类

### 隐藏/显示类

| 类名 | 说明 |
|------|------|
| layui-hide-xs | 在超小屏幕隐藏 |
| layui-hide-sm | 在小屏幕隐藏 |
| layui-hide-md | 在中等屏幕隐藏 |
| layui-hide-lg | 在大屏幕隐藏 |
| layui-show-xs-* | 在超小屏幕显示为指定类型 |
| layui-show-sm-* | 在小屏幕显示为指定类型 |
| layui-show-md-* | 在中等屏幕显示为指定类型 |
| layui-show-lg-* | 在大屏幕显示为指定类型 |

### 显示类型

- `layui-show-xs-block` - 显示为 block
- `layui-show-xs-inline` - 显示为 inline
- `layui-show-xs-inline-block` - 显示为 inline-block

### 示例

```html
<!-- 移动端隐藏 -->
<div class="layui-hide-md">
  只在移动端显示
</div>

<!-- 桌面端显示为 inline-block -->
<div class="layui-show-md-inline-block">
  只在桌面端显示为 inline-block
</div>
```

## 响应式栅格示例

```html
<div class="layui-container">
  <div class="layui-row">
    <!-- 超小屏幕占12列，小屏幕6列，中等4列，大屏幕3列 -->
    <div class="layui-col-xs12 layui-col-sm6 layui-col-md4 layui-col-lg3">
      响应式列
    </div>
  </div>
</div>
```

## 常见布局模式

### 1. 固定容器居中

```html
<div class="layui-container" style="background: #f0f0f0;">
  固定宽度，居中显示
</div>
```

### 2. 全屏流体容器

```html
<div class="layui-fluid" style="background: #f0f0f0;">
  100% 宽度，全屏显示
</div>
```

### 3. 卡片式布局

```html
<div class="layui-container">
  <div class="layui-row layui-col-space15">
    <div class="layui-col-md4">
      <div class="layui-card">
        <div class="layui-card-header">卡片标题</div>
        <div class="layui-card-body">
          卡片内容
        </div>
      </div>
    </div>
  </div>
</div>
```

## 下一步

- 查看表单模块 → `04-form-module.md`
- 查看表格模块 → `05-table-module.md`
- 查看弹层模块 → `06-layer-module.md`
