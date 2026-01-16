# 企业级表格开发指南

## 1. 标准表格布局

LayuiAdmin 中的标准表格布局结构：

```html
<div class="layui-fluid">
  <div class="layui-card">
    <div class="layui-tab layui-tab-brief">
      <ul class="layui-tab-title">
        <li class="layui-this">{{tabTitle}}</li>
      </ul>
      <div class="layui-tab-content">
        <!-- 搜索表单区 -->
        <div class="layui-row" style="margin-bottom:15px;">
          <div class="layui-form" style="float:right;">
            <!-- 搜索字段 -->
          </div>
        </div>

        <!-- 工具栏按钮区 -->
        <div class="layuiAdmin-btns" style="margin-bottom: 10px;">
          <button class="layui-btn" data-type="all" data-events="create">新增</button>
        </div>

        <!-- 数据表格 -->
        <table id="dataTable" lay-filter="dataTable"></table>
      </div>
    </div>
  </div>
</div>
```

## 2. 搜索表单设计模式

### 时间范围搜索（最常用）

```html
<div class="layui-input-inline">
  <input type="text" name="createTimeStart" id="createTimeStart"
         autocomplete="off" placeholder="开始时间" class="layui-input">
</div>
<div class="layui-input-inline">
  <input type="text" name="createTimeEnd" id="createTimeEnd"
         autocomplete="off" placeholder="结束时间" class="layui-input">
</div>

<script>
laydate.render({
  elem: '#createTimeStart',
  type: 'datetime',
  format: 'yyyy-MM-dd HH:mm:ss',
  value: new Date() // 默认当天
});

laydate.render({
  elem: '#createTimeEnd',
  type: 'datetime',
  format: 'yyyy-MM-dd HH:mm:ss',
  value: new Date()
});
</script>
```

### 下拉选择框

```html
<div class="layui-input-inline">
  <select name="status" id="status" lay-search="">
    <option value="-99">订单状态</option>
    <option value="0">订单生成</option>
    <option value="1">支付中</option>
    <option value="2">支付成功</option>
  </select>
</div>
```

### 搜索按钮

```javascript
$('#search').on('click', function(){
  table.reload('tableReload', {
    page: { curr: 1 },
    where: {
      createTimeStart: $('#createTimeStart').val(),
      createTimeEnd: $('#createTimeEnd').val(),
      status: $('#status').val()
    }
  });
});
```

## 3. 自定义列模板（templet）

### 状态显示模板

```javascript
var tplStatus = function(d){
  if(d.status == 0) {
    return "关闭";
  } else if(d.status == 1) {
    return "<span style='color: green'>开启</span>";
  }
  return d.status;
};

// 在表格配置中使用
{field: 'status', title: '状态', templet: tplStatus}
```

### 日期格式化模板

```javascript
// 使用 layui.util 工具
{field: 'createTime', title: '创建时间',
 templet: '<div>{{ layui.util.toDateString(d.createTime, "yyyy-MM-dd HH:mm:ss") }}</div>'}
```

### 自定义计算模板

```javascript
var tplRate = function(d){
  return "<span style='color: blue'>"+ d.passageRate+"% + " + d.passageFeeEvery + "</span>";
};

{field: 'passageRate', title: '费率', templet: tplRate}
```

## 4. 行操作工具栏

### 定义工具栏模板

```html
<script type="text/html" id="actionBar">
  <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="detail">查看</a>
  {{# if(d.status == 1){ }}
  <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="reissue">补单</a>
  {{# } else { }}
  <a class="layui-btn layui-btn-primary layui-btn-xs layui-btn-disabled">补单</a>
  {{# } }}
</script>
```

### 监听工具栏事件

```javascript
table.on('tool(dataTable)', function(obj){
  var data = obj.data;

  if(obj.event === 'detail'){
    location.href = '#/order/pay/view?id=' + data.id;
  } else if(obj.event === 'reissue'){
    // 补单逻辑
  } else if(obj.event === 'edit'){
    location.href = '#/order/pay/edit?id=' + data.id;
  }
});
```

## 5. 工具栏按钮

### 头部工具栏

```html
<script type="text/html" id="headerToolbar">
  <div class="layui-btn-container">
    <button class="layui-btn layui-btn-sm" lay-event="add">新增</button>
    <button class="layui-btn layui-btn-sm" lay-event="delete">删除</button>
  </div>
</script>
```

### 监听头部工具栏事件

```javascript
table.on('toolbar(dataTable)', function(obj){
  var checkStatus = table.checkStatus(obj.config.id);
  var data = checkStatus.data;

  if(obj.event === 'add'){
    // 新增操作
  } else if(obj.event === 'delete'){
    if(data.length === 0){
      layer.msg('请选择要删除的数据');
    } else {
      layer.confirm('确定删除选中的 ' + data.length + ' 条数据吗？', function(index){
        // 批量删除
      });
    }
  }
});
```

## 6. 数据统计展示

### 使用 blockquote 展示统计

```html
<div class="layui-form-item" id="statisticsArea" style="display: none">
  <blockquote class="layui-elem-quote" id="amountTip">
    提交订单数:<span id="allTotalCount" style="color: blue; margin-right: 20px;"></span>
    订单总金额:<span id="allTotalAmount" style="color: blue; margin-right: 20px;"></span>
    已付订单数:<span id="successTotalCount" style="color: green; margin-right: 20px;"></span>
    已付总金额:<span id="successTotalAmount" style="color: green; margin-right: 20px;"></span>
    成功率:<span id="successRate" style="color: green;"></span>
  </blockquote>
</div>
```

### 加载统计数据

```javascript
function loadStatistics(createTimeStart, createTimeEnd, mchId, status) {
  admin.req({
    type: 'get',
    url: '/api/pay_order/count',
    data: {
      createTimeStart: createTimeStart,
      createTimeEnd: createTimeEnd,
      mchId: mchId,
      status: status
    },
    success: function(res){
      if(res.code == 0){
        $('#allTotalCount').html(res.data.allTotalCount || 0);
        $('#allTotalAmount').html('￥' + (res.data.allTotalAmount || 0));
        $('#successTotalCount').html(res.data.successTotalCount || 0);
        $('#successTotalAmount').html('￥' + (res.data.successTotalAmount || 0));
        $('#successRate').html((res.data.successRate || 0) + '%');
        $('#statisticsArea').show();
      }
    }
  });
}
```

## 7. 权限控制集成

### 页面级权限检查

```javascript
var authEdit = true;

admin.req({
  type: 'get',
  url: '/api/mch_info/checkAuth',
  data: {
    authAction: 'ROLE_PAY_PASSAGE_EDIT'
  },
  success: function(res){
    if(res.data == 'RET_SERVICE_PAGE_NO_AUTH'){
      authEdit = false;
      // 禁用新增按钮
      $(".layuiAdmin-btns .layui-btn").removeAttr("data-events");
    }
  }
});
```

### 操作级权限检查

```javascript
table.on('tool(dataTable)', function(obj){
  if(!authEdit){
    layer.msg('没有操作权限', {icon: 2});
    return;
  }
  // 执行操作...
});
```

## 8. 导出功能实现

### 前端实现（简单导出）

```javascript
$('#exportBtn').on('click', function(){
  var queryParams = {
    createTimeStart: $('#createTimeStart').val(),
    createTimeEnd: $('#createTimeEnd').val(),
    status: $('#status').val()
  };

  var queryString = $.param(queryParams);
  window.open('/api/pay_order/export?' + queryString, '_blank');
});
```

### 分批导出（大数据量）

```javascript
$('#exportBtn').on('click', function(){
  var pageSize = $('#exportPageSize').val(); // 1000, 2000, 5000, 10000

  // 获取总数
  admin.req({
    type: 'get',
    url: '/api/pay_order/count',
    data: queryParams,
    success: function(res){
      var totalCount = res.data.totalCount;
      var totalPages = Math.ceil(totalCount / pageSize);

      // 存储导出任务信息
      var exportId = 'export_' + Date.now();
      layui.data(exportId, {
        key: 'query',
        value: {
          params: queryParams,
          pageSize: parseInt(pageSize),
          totalPages: totalPages,
          totalCount: totalCount
        }
      });

      // 打开导出页面
      window.open('/api/pay_order/export_page?exportId=' + exportId, '_blank');
    }
  });
});
```

## 9. 完整示例

```javascript
layui.use(['admin', 'table', 'laydate', 'form'], function(){
  var $ = layui.$
    ,admin = layui.admin
    ,table = layui.table
    ,laydate = layui.laydate
    ,form = layui.form;

  // 时间选择器
  laydate.render({
    elem: '#createTimeStart',
    type: 'datetime',
    format: 'yyyy-MM-dd HH:mm:ss',
    value: new Date()
  });

  // 表格配置
  table.render({
    elem: '#payOrderTable',
    url: '/api/pay_order/list',
    where: {
      access_token: layui.data(layui.setter.tableName).access_token
    },
    id: 'tableReload',
    cols: [[
      {field: 'mchId', title: '商户ID', width: 100},
      {field: 'payOrderId', title: '支付订单号', width: 220},
      {field: 'amount', title: '支付金额', width: 100},
      {field: 'status', title: '状态', width: 100, templet: tplStatus},
      {field: 'edit', title: '操作', width: 200, toolbar: '#actionBar'}
    ]],
    page: true,
    skin: 'line',
    limit: 20
  });

  // 搜索功能
  $('#search').on('click', function(){
    table.reload('tableReload', {
      page: { curr: 1 },
      where: {
        createTimeStart: $('#createTimeStart').val(),
        status: $('#status').val()
      }
    });
  });

  // 行操作
  table.on('tool(payOrderTable)', function(obj){
    if(obj.event === 'detail'){
      location.href = '#/order/pay/view?id=' + obj.data.id;
    }
  });
});
```
