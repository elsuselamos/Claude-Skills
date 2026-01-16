# Layui 其他组件详解

## 按钮（button）

### 按钮主题

```html
<button class="layui-btn">默认按钮</button>
<button class="layui-btn layui-btn-primary">原始按钮</button>
<button class="layui-btn layui-btn-normal">百搭按钮</button>
<button class="layui-btn layui-btn-warm">暖色按钮</button>
<button class="layui-btn layui-btn-danger">警告按钮</button>
<button class="layui-btn layui-btn-disabled">禁用按钮</button>
```

### 按钮尺寸

```html
<button class="layui-btn layui-btn-big">大型按钮</button>
<button class="layui-btn">默认按钮</button>
<button class="layui-btn layui-btn-small">小型按钮</button>
<button class="layui-btn layui-btn-xs">迷你按钮</button>
```

### 圆角按钮

```html
<button class="layui-btn layui-btn-radius">默认按钮</button>
<button class="layui-btn layui-btn-primary layui-btn-radius">原始按钮</button>
```

### 图标按钮

```html
<button class="layui-btn">
  <i class="layui-icon">&#xe654;</i> 添加
</button>
<button class="layui-btn layui-btn-sm">
  <i class="layui-icon">&#xe642;</i> 编辑
</button>
<button class="layui-btn layui-btn-primary layui-btn-sm">
  <i class="layui-icon">&#xe640;</i> 删除
</button>
```

### 按钮组

```html
<div class="layui-btn-group">
  <button class="layui-btn">增加</button>
  <button class="layui-btn">编辑</button>
  <button class="layui-btn">删除</button>
</div>
```

### 按钮容器

```html
<div class="layui-btn-container">
  <button class="layui-btn">按钮1</button>
  <button class="layui-btn">按钮2</button>
  <button class="layui-btn">按钮3</button>
</div>
```

## 表单组件（详细）

### 日期选择器（laydate）

```html
<input type="text" class="layui-input" id="date1">

<script>
layui.use('laydate', function(){
  var laydate = layui.laydate;

  // 执行一个laydate实例
  laydate.render({
    elem: '#date1',
    type: 'date', // year, month, date, time, datetime
    format: 'yyyy-MM-dd',
    value: new Date(),
    min: '2020-1-1',
    max: '2099-12-31',
    trigger: 'click',
    showBottom: false,
    btns: ['clear', 'now', 'confirm'],
    lang: 'cn',
    theme: 'default',
    calendar: false,
    mark: {},
    zIndex: 99999999,
    done: function(value, date){
      console.log(value);
      console.log(date);
    }
  });
});
</script>
```

### 日期范围

```html
<input type="text" class="layui-input" id="dateRange">

<script>
layui.use('laydate', function(){
  var laydate = layui.laydate;

  laydate.render({
    elem: '#dateRange',
    range: '~',
    rangeLinked: true
  });
});
</script>
```

### 文件上传（upload）

```html
<button type="button" class="layui-btn" id="upload1">
  <i class="layui-icon">&#xe67c;</i>上传图片
</button>

<script>
layui.use('upload', function(){
  var upload = layui.upload;

  // 执行实例
  var uploadInst = upload.render({
    elem: '#upload1',
    url: '/api/upload/',
    method: 'post',
    data: {},
    accept: 'images', // images, files, video, audio
    acceptMime: 'image/*',
    exts: 'jpg|png|gif',
    auto: true,
    bindAction: '',
    field: 'file',
    size: 0,
    multiple: false,
    number: 0,
    drag: true,
    choose: function(obj){
      // 选择文件后的回调
      var files = obj.pushFile();
      obj.preview(function(index, file, result){
        console.log(file.name);
        console.log(file.size);
      });
    },
    before: function(obj){
      // 上传前的回调
      layer.load();
    },
    progress: function(n, elem, res, index){
      var percent = n + '%';
      elem.html(percent);
    },
    done: function(res, index, upload){
      // 上传完毕回调
      layer.closeAll('loading');
    },
    error: function(){
      // 请求异常回调
      layer.closeAll('loading');
    }
  });
});
</script>
```

### 拖拽上传

```html
<div class="layui-upload-drag" id="uploadDrag">
  <i class="layui-icon">&#xe67c;</i>
  <p>点击上传，或将文件拖拽到此处</p>
</div>

<script>
layui.use('upload', function(){
  var upload = layui.upload;

  upload.render({
    elem: '#uploadDrag',
    url: '/api/upload/',
    accept: 'file',
    done: function(res){
      console.log(res);
    }
  });
});
</script>
```

### 多图片上传

```html
<div class="layui-upload">
  <button type="button" class="layui-btn" id="uploadImg">多图片上传</button>
  <blockquote class="layui-elem-quote layui-quote-nm" style="margin-top: 10px;">
    预览图：
    <div class="layui-upload-list" id="uploadImgList"></div>
  </blockquote>
</div>

<script>
layui.use('upload', function(){
  var upload = layui.upload;

  upload.render({
    elem: '#uploadImg',
    url: '/api/upload/',
    multiple: true,
    before: function(obj){
      layer.msg('选择中');
    },
    done: function(res){
      $('#uploadImgList').append('<img src="'+ res.src +'">');
    }
  });
});
</script>
```

## 分页组件（laypage）

```html
<div id="page"></div>

<script>
layui.use('laypage', function(){
  var laypage = layui.laypage;

  laypage.render({
    elem: 'page',
    count: 100, // 数据总数
    limit: 10, // 每页显示条数
    limits: [10, 20, 30, 50],
    curr: 1, // 当前页
    groups: 5, // 连续分页数
    first: '首页',
    last: '尾页',
    prev: '<em></em>',
    next: '<em></em>',
    layout: ['count', 'prev', 'page', 'next', 'limit', 'skip'],
    theme: '#1E9FFF',
    jump: function(obj, first){
      // obj 包含了当前分页的所有参数
      console.log(obj.curr); // 当前页
      console.log(obj.limit); // 每页显示条数

      // 首次不执行
      if(!first){
        // 加载数据
      }
    }
  });
});
</script>
```

## 评分组件（rate）

```html
<div id="rate1"></div>

<script>
layui.use('rate', function(){
  var rate = layui.rate;

  rate.render({
    elem: '#rate1',
    value: 3.5, // 初始值
    half: true, // 开启半星
    text: true, // 开启文本
    readonly: false, // 只读
    length: 5, // 星星数量
    theme: '#FF8000', // 主题颜色
    choose: function(value){
      if(value > 4) alert('么么哒')
    }
  });
});
</script>
```

## 面板组件

### 折叠面板

详见 `07-navigation.md` 中的折叠面板部分。

### 卡片面板

```html
<div class="layui-card">
  <div class="layui-card-header">卡片标题</div>
  <div class="layui-card-body">
    卡片内容
  </div>
</div>
```

### 常用面板组合

```html
<div class="layui-row layui-col-space15">
  <div class="layui-col-md6">
    <div class="layui-card">
      <div class="layui-card-header">标题</div>
      <div class="layui-card-body">内容</div>
    </div>
  </div>
  <div class="layui-col-md6">
    <div class="layui-card">
      <div class="layui-card-header">标题</div>
      <div class="layui-card-body">内容</div>
    </div>
  </div>
</div>
```

## 辅助元素

### 引用块

```html
<blockquote class="layui-elem-quote">引用内容的文字</blockquote>
<blockquote class="layui-elem-quote layui-quote-nm">引用内容的文字</blockquote>
```

### 字段集

```html
<fieldset class="layui-elem-field">
  <legend>字段集区块</legend>
  <div class="layui-field-box">
    内容区域
  </div>
</fieldset>
```

### 分割线

```html
<hr>
<hr class="layui-bg-red">
<hr class="layui-bg-orange">
<hr class="layui-bg-green">
<hr class="layui-bg-cyan">
<hr class="layui-bg-blue">
<hr class="layui-bg-black">
```

### 圆角

```html
<div class="layui-inline">
  <img src="..." class="layui-circle">
</div>
```

## 栅格系统

详见 `03-layout-system.md`。

## 下一步

- 查看 API 速查 → `10-api-reference.md`
- 查看最佳实践 → `11-best-practices.md`
