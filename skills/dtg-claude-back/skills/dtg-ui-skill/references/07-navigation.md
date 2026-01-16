# Layui 导航组件详解

## 导航组件（element 模块）

Layui 的导航组件包含：水平导航、垂直导航（侧边栏）、面包屑。

## 水平导航

### 基础导航

```html
<ul class="layui-nav" lay-filter="">
  <li class="layui-nav-item"><a href="">最新活动</a></li>
  <li class="layui-nav-item layui-this"><a href="">产品</a></li>
  <li class="layui-nav-item"><a href="">大数据</a></li>
  <li class="layui-nav-item">
    <a href="javascript:;">解决方案</a>
    <dl class="layui-nav-child">
      <dd><a href="">移动模块</a></dd>
      <dd><a href="">后台模版</a></dd>
      <dd><a href="">电商平台</a></dd>
    </dl>
  </li>
  <li class="layui-nav-item"><a href="">社区</a></li>
</ul>

<script>
layui.use('element', function(){
  var element = layui.element;
});
</script>
```

### 带图片的导航

```html
<ul class="layui-nav layui-bg-green" lay-filter="">
  <li class="layui-nav-item">
    <a href="">控制台<span class="layui-badge-dot"></span></a>
  </li>
  <li class="layui-nav-item">
    <a href="">个人中心<span class="layui-badge">9</span></a>
  </li>
  <li class="layui-nav-item">
    <a href="">
      <img src="http://t.cn/RCzsdCq" class="layui-nav-img">
      贤心
    </a>
    <dl class="layui-nav-child">
      <dd><a href="">修改信息</a></dd>
      <dd><a href="">安全管理</a></dd>
      <dd><a href="">退了</a></dd>
    </dl>
  </li>
</ul>
```

## 垂直导航（侧边栏）

### 基础垂直导航

```html
<ul class="layui-nav layui-nav-tree" lay-filter="test">
  <li class="layui-nav-item layui-nav-itemed">
    <a href="">默认展开</a>
    <dl class="layui-nav-child">
      <dd><a href="">选项1</a></dd>
      <dd><a href="">选项2</a></dd>
    </dl>
  </li>
  <li class="layui-nav-item">
    <a href="">解决方案</a>
    <dl class="layui-nav-child">
      <dd><a href="">移动模块</a></dd>
      <dd><a href="">后台模版</a></dd>
    </dl>
  </li>
  <li class="layui-nav-item"><a href="">产品</a></li>
  <li class="layui-nav-item"><a href="">大数据</a></li>
</ul>

<script>
layui.use('element', function(){
  var element = layui.element;
});
</script>
```

### 侧边栏样式

```html
<ul class="layui-nav layui-nav-tree layui-bg-cyan layui-inline">
  <!-- 导航项 -->
</ul>

<!-- 背景类 -->
layui-bg-black  <!-- 黑色背景 -->
layui-bg-gray   <!-- 灰色背景 -->
layui-bg-cyan   <!-- 青色背景 -->
layui-bg-blue   <!-- 蓝色背景 -->
layui-bg-green  <!-- 绿色背景 -->
layui-bg-orange <!-- 橙色背景 -->
layui-bg-red    <!-- 红色背景 -->
```

## 导航事件监听

```javascript
layui.use('element', function(){
  var element = layui.element;

  // 监听导航点击
  element.on('nav(filter)', function(elem){
    console.log(elem); // 获取当前点击的元素对象
  });
});
```

## 面包屑

```html
<span class="layui-breadcrumb">
  <a href="/">首页</a>
  <a href="/demo/">演示</a>
  <a><cite>导航元素</cite></a>
</span>

<!-- 自定义分隔符 -->
<span class="layui-breadcrumb" lay-separator="-">
  <a href="">首页</a>
  <a href="">国际新闻</a>
  <a><cite>亚太地区</cite></a>
</span>

<!-- 居中显示 -->
<span class="layui-breadcrumb" lay-separator="|">
  <a href="">娱乐</a>
  <a href="">八卦</a>
  <a href="">体育</a>
  <a href="">搞笑</a>
  <a href="">视频</a>
  <a href="">游戏</a>
  <a href="">综艺</a>
</span>
```

## 选项卡

### 基础选项卡

```html
<div class="layui-tab">
  <ul class="layui-tab-title">
    <li class="layui-this">网站设置</li>
    <li>用户管理</li>
    <li>权限分配</li>
    <li>商品管理</li>
    <li>订单管理</li>
  </ul>
  <div class="layui-tab-content">
    <div class="layui-tab-item layui-show">内容1</div>
    <div class="layui-tab-item">内容2</div>
    <div class="layui-tab-item">内容3</div>
    <div class="layui-tab-item">内容4</div>
    <div class="layui-tab-item">内容5</div>
  </div>
</div>

<script>
layui.use('element', function(){
  var element = layui.element;
});
</script>
```

### 简约选项卡

```html
<div class="layui-tab layui-tab-brief">
  <!-- 内容同上 -->
</div>
```

### 卡片风格选项卡

```html
<div class="layui-tab layui-tab-card">
  <!-- 内容同上 -->
</div>
```

### 选项卡删除

```html
<div class="layui-tab" lay-filter="demo">
  <ul class="layui-tab-title">
    <li class="layui-this" lay-id="11">网站设置</li>
    <li lay-id="22">用户管理</li>
    <li lay-id="33">权限分配</li>
    <li lay-id="44">商品管理</li>
    <li lay-id="55">订单管理</li>
  </ul>
  <div class="layui-tab-content">
    <div class="layui-tab-item layui-show">1</div>
    <div class="layui-tab-item">2</div>
    <div class="layui-tab-item">3</div>
    <div class="layui-tab-item">4</div>
    <div class="layui-tab-item">5</div>
  </div>
</div>

<script>
layui.use('element', function(){
  var element = layui.element;

  // 监听选项卡切换
  element.on('tab(demo)', function(data){
    console.log(data.index); // 得到当前索引
    console.log(data.elem); // 得到当前的 DOM 对象
    console.log(data.id); // 得到 lay-id
  });

  // 删除指定选项卡
  element.tabDelete('demo', '22');

  // 切换到指定选项卡
  element.tabChange('demo', '33');
});
</script>
```

### 动态增删选项卡

```html
<div class="layui-tab" lay-filter="demo" lay-allowClose="true">
  <ul class="layui-tab-title">
    <li class="layui-this" lay-id="11">网站设置</li>
  </ul>
  <div class="layui-tab-content">
    <div class="layui-tab-item layui-show">内容1</div>
  </div>
</div>

<button class="layui-btn" onclick="addTab()">添加选项卡</button>

<script>
layui.use('element', function(){
  window.element = layui.element;
});

function addTab(){
  element.tabAdd('demo', {
    title: '新选项卡'
    ,content: '内容' + Math.random()
    ,id: new Date().getTime()
  });
}
</script>
```

## 折叠面板

```html
<div class="layui-collapse">
  <div class="layui-colla-item">
    <h2 class="layui-colla-title">杜甫</h2>
    <div class="layui-colla-content layui-show">
      <p>内容区域</p>
    </div>
  </div>
  <div class="layui-colla-item">
    <h2 class="layui-colla-title">李清照</h2>
    <div class="layui-colla-content">
      <p>内容区域</p>
    </div>
  </div>
  <div class="layui-colla-item">
    <h2 class="layui-colla-title">鲁迅</h2>
    <div class="layui-colla-content">
      <p>内容区域</p>
    </div>
  </div>
</div>

<script>
layui.use('element', function(){
  var element = layui.element;
});
</script>
```

### 手风琴效果

```html
<div class="layui-collapse" lay-accordion>
  <!-- 同时只会展开一个面板 -->
</div>
```

### 监听折叠面板

```javascript
layui.use('element', function(){
  var element = layui.element;

  element.on('collapse(filter)', function(data){
    console.log(data.show); // 得到展开状态
    console.log(data.title); // 得到当前点击的面板标题对象
    console.log(data.content); // 得到当前点击的面板内容区域对象
  });
});
```

## 常用类名

### 导航类名

| 类名 | 说明 |
|------|------|
| layui-nav | 导航容器 |
| layui-nav-item | 导航项 |
| layui-nav-child | 子导航 |
| layui-nav-more | 展开/收起图标 |
| layui-this | 当前选中项 |
| layui-nav-itemed | 当前展开项 |
| layui-nav-img | 导航图片 |
| layui-nav-tree | 垂直导航 |

### 导航背景类

| 类名 | 说明 |
|------|------|
| layui-bg-black | 黑色背景 |
| layui-bg-gray | 灰色背景 |
| layui-bg-blue | 蓝色背景 |
| layui-bg-cyan | 青色背景 |
| layui-bg-green | 绿色背景 |
| layui-bg-orange | 橙色背景 |
| layui-bg-red | 红色背景 |

### 选项卡类名

| 类名 | 说明 |
|------|------|
| layui-tab | 选项卡容器 |
| layui-tab-title | 选项卡标题 |
| layui-tab-content | 选项卡内容 |
| layui-tab-item | 选项卡内容项 |
| layui-tab-brief | 简约风格 |
| layui-tab-card | 卡片风格 |

### 折叠面板类名

| 类名 | 说明 |
|------|------|
| layui-collapse | 折叠面板容器 |
| layui-colla-item | 折叠面板项 |
| layui-colla-title | 折叠面板标题 |
| layui-colla-content | 折叠面板内容 |

## 下一步

- 查看数据展示组件 → `08-data-components.md`
- 查看其他组件 → `09-other-components.md`
