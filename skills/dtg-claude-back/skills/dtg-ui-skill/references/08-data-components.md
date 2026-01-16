# Layui 数据展示组件详解

## 树形组件（tree）

### 基础树

```html
<ul id="demo"></ul>

<script>
layui.use('tree', function(){
  layui.tree({
    elem: '#demo',
    nodes: [ // 节点数据
      {
        name: '常用文件夹',
        id: 1,
        children: [
          {name: '所有未读', id: 11},
          {name: '置顶邮件', id: 12},
          {name: '标签邮件', id: 13}
        ]
      },
      {
        name: '我的邮箱',
        id: 2,
        children: [
          {name: 'QQ邮箱', id: 21},
          {name: '阿里云邮', id: 22},
          {name: '企业邮箱', id: 23}
        ]
      }
    ],
    click: function(node){
      console.log(node); // node 即为当前点击的节点数据
    }
  });
});
</script>
```

### 复选树

```html
<div id="test1" class="demo-tree-more"></div>

<script>
layui.use(['tree', 'util'], function(){
  var tree = layui.tree
  ,util = layui.util;

  tree.render({
    elem: '#test1'
    ,data: [{
      title: '成都'
      ,id: 1
      ,children: [{
        title: '高新区'
        ,id: 11
        ,children: [{
          title: '天府软件园'
          ,id: 111
        }]
      }]
    }, {
      title: '重庆'
      ,id: 2
      ,children: [{
        title: '渝中区'
        ,id: 21
      }]
    }]
    ,showCheckbox: true  // 是否显示复选框
    ,id: 'demoId1'
    ,isJump: true // 是否允许点击节点时弹出新窗口跳转
    ,click: function(obj){
      var data = obj.data;  // 获取当前点击的节点数据
      layer.msg('状态：'+ obj.state + '<br>节点数据：'+ JSON.stringify(data));
    }
    ,oncheck: function(obj){
      console.log(obj.checked); // 当前是否选中
      console.log(obj.data); // 获取当前点击的节点数据
    }
  });
});
</script>
```

### 获取选中节点

```javascript
var checkData = tree.getChecked('demoId1');
```

### 设置节点选中/取消

```javascript
tree.setChecked('demoId1', [11, 111]); // 批量设置
```

## 轮播组件（carousel）

### 基础轮播

```html
<div class="layui-carousel" id="test1">
  <div carousel-item>
    <div>条目1</div>
    <div>条目2</div>
    <div>条目3</div>
    <div>条目4</div>
  </div>
</div>

<script>
layui.use('carousel', function(){
  var carousel = layui.carousel;

  carousel.render({
    elem: '#test1',
    width: '100%',
    height: '280px',
    arrow: 'always' // 始终显示箭头
  });
});
</script>
```

### 轮播参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| elem | 指向容器选择器 | - |
| width | 设定轮播宽度 | - |
| height | 设定轮播高度 | - |
| full | 是否全屏轮播 | false |
| arrow | 切换箭头默认显示 | hover |
| indicator | 指示器位置 | inside |
| autoplay | 是否自动切换 | true |
| interval | 自动切换的时间间隔 | 3000 |
| anim | 切换动画方式 | default |
| index | 初始开始的条目索引 | 0 |

### 轮播事件

```javascript
carousel.render({
  elem: '#test1',
  change: function(result){
    console.log(result.index); // 当前条目的索引
    console.log(result.prevIndex); // 上一个条目的索引
    console.log(result.item); // 当前条目的元素对象
  }
});
```

### 图片轮播

```html
<div class="layui-carousel" id="test2">
  <div carousel-item>
    <div><img src="1.jpg"></div>
    <div><img src="2.jpg"></div>
    <div><img src="3.jpg"></div>
  </div>
</div>

<script>
layui.use('carousel', function(){
  var carousel = layui.carousel;
  carousel.render({
    elem: '#test2',
    width: '100%',
    height: '400px',
    anim: 'updown' // 切换动画方式：updown（上下切换）
  });
});
</script>
```

## 代码修饰器（code）

### 基础用法

```html
<pre class="layui-code">
  // 代码内容
  layui.use('layer', function(){
    var layer = layui.layer;
    layer.msg('Hello');
  });
</pre>
```

### 配置参数

```html
<!-- 带标题 -->
<pre class="layui-code" lay-title="HTML结构">
  <div>代码</div>
</pre>

<!-- 指定高度 -->
<pre class="layui-code" lay-height="150px">
  代码内容
</pre>

<!-- 不显示编码 -->
<pre class="layui-code" lay-encode="false">
  代码内容
</pre>

<!-- 皮肤：notepad 风格 -->
<pre class="layui-code" lay-skin="notepad">
  代码内容
</pre>
```

## 流加载（flow）

### 列表流加载

```html
<ul id="demo"></ul>

<script>
layui.use('flow', function(){
  var flow = layui.flow;

  flow.load({
    elem: '#demo',
    done: function(page, next){
      // 模拟数据
      var lis = [];
      for(var i = 0; i < 10; i++){
        lis.push('<li>' + ((page-1)*10 + i + 1) + '</li>');
      }

      // 下一页
      next(lis.join(''), page < 10);
    }
  });
});
</script>
```

### 图片流加载（懒加载）

```html
<div id="demo2"></div>

<script>
layui.use('flow', function(){
  var flow = layui.flow;

  flow.load({
    elem: '#demo2',
    scrollElem: '#demo2', // 滚动条所在元素
    isAuto: true,
    mb: 50, // 距离底部多少像素时触发
    done: function(page, next){
      // 模拟数据
      var lis = [];
      for(var i = 0; i < 10; i++){
        lis.push('<li><img src="https://picsum.photos/200/200?r='+ (page*10+i) +'"></li>');
      }

      next(lis.join(''), page < 10);
    }
  });
});
</script>
```

### 信息流

```html
<ul class="flow-default" id="LAY_demo1"></ul>

<script>
layui.use('flow', function(){
  var flow = layui.flow;

  flow.load({
    elem: '#LAY_demo1',
    isAuto: false,
    isLazyimg: true,
    done: function(page, next){
      // 模拟数据
      var lis = [];
      for(var i = 0; i < 10; i++){
        lis.push('<li>'+ (page*10+i) +'</li>');
      }
      next(lis.join(''), page < 10);
    }
  });
});
</script>
```

## 进度条（progress）

### 基础进度条

```html
<div class="layui-progress">
  <div class="layui-progress-bar" lay-percent="30%"></div>
</div>

<script>
layui.use('element', function(){
  var element = layui.element;
  element.progress('demo', '50%');
});
</script>
```

### 不同颜色

```html
<div class="layui-progress">
  <div class="layui-progress-bar layui-bg-green" lay-percent="50%"></div>
</div>

<div class="layui-progress">
  <div class="layui-progress-bar layui-bg-blue" lay-percent="30%"></div>
</div>

<div class="layui-progress">
  <div class="layui-progress-bar layui-bg-orange" lay-percent="70%"></div>
</div>

<div class="layui-progress">
  <div class="layui-progress-bar layui-bg-red" lay-percent="40%"></div>
</div>
```

### 显示百分比

```html
<div class="layui-progress" lay-showpercent="true">
  <div class="layui-progress-bar" lay-percent="50%"></div>
</div>
```

### 大尺寸进度条

```html
<div class="layui-progress layui-progress-big">
  <div class="layui-progress-bar" lay-percent="30%"></div>
</div>
```

## 徽章（badge）

### 小圆点徽章

```html
<span class="layui-badge-dot"></span>
<span class="layui-badge-dot layui-bg-gray"></span>
<span class="layui-badge-dot layui-bg-blue"></span>
```

### 椭圆徽章

```html
<span class="layui-badge">6</span>
<span class="layui-badge">Hot</span>

<span class="layui-badge layui-bg-gray">666</span>
<span class="layui-badge layui-bg-blue">腹黑</span>
<span class="layui-badge layui-bg-orange">活跃</span>
<span class="layui-badge layui-bg-green">新手</span>
```

### 边框徽章

```html
<span class="layui-badge-rim">666</span>
```

### 在导航中使用

```html
<ul class="layui-nav">
  <li class="layui-nav-item">
    <a href="">控制台<span class="layui-badge-dot"></span></a>
  </li>
  <li class="layui-nav-item">
    <a href="">个人中心<span class="layui-badge">9</span></a>
  </li>
</ul>
```

## 时间线（timeline）

```html
<ul class="layui-timeline">
  <li class="layui-timeline-item">
    <i class="layui-icon layui-timeline-axis">&#xe63f;</i>
    <div class="layui-timeline-content layui-text">
      <h3 class="layui-timeline-title">8月18日</h3>
      <p>
        layui 2.0 的一切准备工作似乎都已到位。
        发布之期，确实是迫在眉睫了。
        估计下周一就能 layui 发布。
      </p>
    </div>
  </li>
  <li class="layui-timeline-item">
    <i class="layui-icon layui-timeline-axis">&#xe63f;</i>
    <div class="layui-timeline-content layui-text">
      <h3 class="layui-timeline-title">8月16日</h3>
      <p>杜甫的思想核心是儒家的仁政思想。</p>
    </div>
  </li>
  <li class="layui-timeline-item">
    <i class="layui-icon layui-timeline-axis">&#xe63f;</i>
    <div class="layui-timeline-content layui-text">
      <h3 class="layui-timeline-title">8月15日</h3>
      <p>
        中国人民抗日战争胜利日
      </p>
    </div>
  </li>
  <li class="layui-timeline-item">
    <i class="layui-icon layui-timeline-axis">&#xe63f;</i>
  </li>
</ul>
```

## 下一步

- 查看其他组件 → `09-other-components.md`
- 查看 API 速查 → `10-api-reference.md`
