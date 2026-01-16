# 性能优化建议

> LayuiAdmin 企业级应用性能优化最佳实践

## 概述

在企业级应用中，性能优化直接影响用户体验和系统稳定性。本文档介绍 LayuiAdmin 应用的常见性能优化策略。

## 表格优化

### 1. 分页加载

```javascript
table.render({
  elem: '#dataTable',
  url: layui.setter.baseUrl + '/api/list',
  page: {
    layout: ['count', 'prev', 'page', 'next', 'limit', 'skip'],
    limits: [10, 20, 50, 100],
    limit: 20 // 默认每页20条
  },
  height: 'full-200' // 固定表头
});
```

### 2. 按需加载数据

```javascript
// 只在需要时才加载数据
var loadFlag = false;

$('#tab').on('click', function(){
  if(!loadFlag){
    table.reload('dataTable');
    loadFlag = true;
  }
});
```

### 3. 减少列数

```javascript
// 只显示必要的列
table.render({
  elem: '#dataTable',
  url: layui.setter.baseUrl + '/api/list',
  cols: [[
    {field: 'id', title: 'ID', width: 80},
    {field: 'name', title: '名称'},
    {field: 'status', title: '状态'},
    // 避免过多列，影响渲染性能
  ]]
});
```

## 图片优化

### 1. 懒加载

```javascript
// 使用 Layui 的图片懒加载
layui.use('flow', function(){
  var flow = layui.flow;

  flow.load({
    elem: '#imageContainer',
    done: function(page, next){
      // 获取图片数据
      var images = [];
      next(images.join(''), page < 10);
    }
  });
});
```

### 2. 图片压缩

```javascript
// 上传前压缩图片
upload.render({
  elem: '#upload',
  url: layui.setter.baseUrl + '/api/upload',
  before: function(file){
    // 压缩图片
    compressImage(file, function(compressedFile){
      this.data.file = compressedFile;
    }.bind(this));
  }
});
```

## 请求优化

### 1. 合并请求

```javascript
// 不好的做法：多次请求
loadUserInfo();
loadUserOrders();
loadUserStatistics();

// 好的做法：一次请求获取所有数据
loadUserData({
  success: function(res){
    renderUserInfo(res.userInfo);
    renderOrders(res.orders);
    renderStatistics(res.statistics);
  }
});
```

### 2. 防抖处理

```javascript
// 搜索输入防抖
var searchTimer = null;

$('#searchInput').on('input', function(){
  clearTimeout(searchTimer);
  searchTimer = setTimeout(function(){
    table.reload('dataTable', {
      where: {keyword: $('#searchInput').val()}
    });
  }, 500);
});
```

### 3. 请求缓存

```javascript
// 简单的请求缓存
var cache = {};

function getData(key, apiCallback){
  if(cache[key]){
    // 使用缓存数据
    apiCallback(cache[key]);
  } else {
    // 请求数据
    admin.req({
      url: layui.setter.baseUrl + '/api/data',
      success: function(res){
        cache[key] = res.data;
        apiCallback(res.data);
      }
    });
  }
}
```

## DOM 操作优化

### 1. 减少DOM操作

```javascript
// 不好的做法：频繁操作DOM
for(var i = 0; i < 1000; i++){
  $('#list').append('<li>' + i + '</li>');
}

// 好的做法：一次性插入
var html = '';
for(var i = 0; i < 1000; i++){
  html += '<li>' + i + '</li>';
}
$('#list').html(html);
```

### 2. 使用事件委托

```javascript
// 不好的做法：给每个元素绑定事件
$('.delete-btn').each(function(){
  $(this).on('click', function(){
    // 删除操作
  });
});

// 好的做法：使用事件委托
$('#list').on('click', '.delete-btn', function(){
  // 删除操作
});
```

## 内存优化

### 1. 销毁不需要的对象

```javascript
// 页面销毁时清理
$(window).on('unload', function(){
  if(chart){
    chart.dispose();
    chart = null;
  }
  if(timer){
    clearInterval(timer);
    timer = null;
  }
});
```

### 2. 避免内存泄漏

```javascript
// 解除事件绑定
$('#myButton').off('click');

// 清空定时器
clearInterval(timer);

// 清空数据
layui.data('cache', null);
```

## 渲染优化

### 1. 虚拟滚动

```javascript
// 大数据列表使用虚拟滚动
function renderVirtualList(data, itemHeight, visibleCount){
  var scrollTop = 0;
  var startIndex = 0;

  $('#container').on('scroll', function(){
    scrollTop = $(this).scrollTop();
    startIndex = Math.floor(scrollTop / itemHeight);
    renderItems();
  });

  function renderItems(){
    var endIndex = startIndex + visibleCount;
    var items = data.slice(startIndex, endIndex);
    // 渲染可见项
  }
}
```

### 2. 分批渲染

```javascript
// 大数据分批渲染
function renderBatch(data, batchSize, callback){
  var index = 0;

  function render(){
    var batch = data.slice(index, index + batchSize);
    // 渲染当前批次
    renderItems(batch);

    index += batchSize;
    if(index < data.length){
      setTimeout(render, 0);
    } else {
      callback && callback();
    }
  }

  render();
}
```

## 代码优化

### 1. 按需加载模块

```javascript
// 不好的做法：一次性加载所有模块
layui.use(['table', 'form', 'upload', 'laydate', 'layedit', 'layer'], function(){
  // 即使只需要用到 table
});

// 好的做法：按需加载
layui.use(['table'], function(){
  var table = layui.table;
  // 只使用 table
});
```

### 2. 避免全局污染

```javascript
// 不好的做法：使用全局变量
var globalData = {};

// 好的做法：使用模块作用域
layui.define(function(exports){
  var data = {};

  exports('myModule', {
    getData: function(){
      return data;
    }
  });
});
```

## 监控与调试

### 1. 性能监控

```javascript
// 记录页面加载时间
var startTime = Date.now();

window.addEventListener('load', function(){
  var loadTime = Date.now() - startTime;
  console.log('页面加载时间:', loadTime + 'ms');

  // 上报到监控系统
  reportPerformance({
    loadTime: loadTime,
    url: location.href
  });
});
```

### 2. 请求耗时监控

```javascript
// 监控 API 请求耗时
layui.use(['admin'], function(){
  var admin = layui.admin;
  var originalReq = admin.req;

  admin.req = function(options){
    var requestStart = Date.now();

    var originalSuccess = options.success;
    options.success = function(){
      var requestTime = Date.now() - requestStart;
      console.log('请求耗时:', requestTime + 'ms', options.url);
      originalSuccess && originalSuccess.apply(this, arguments);
    };

    originalReq.call(admin, options);
  };
});
```

## 注意事项

1. **避免过早优化**：先确保功能正确，再进行性能优化
2. **测量再优化**：使用性能分析工具找出瓶颈
3. **权衡取舍**：性能优化需要考虑代码可读性和维护成本
4. **持续监控**：建立性能监控体系，及时发现性能问题

## 相关文档

- [11-best-practices.md](./11-best-practices.md) - 最佳实践
- [18-api-integration-guide.md](./18-api-integration-guide.md) - API 集成指南
