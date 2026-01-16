# 支付系统页面模式

本文档总结了企业级支付系统中常见的页面模式和代码规范。

## 1. 订单列表页面模式

### 页面结构

```html
<div class="layui-card layadmin-header">
  <div class="layui-breadcrumb" lay-filter="breadcrumb">
    <a lay-href="">主页</a>
    <a><cite>订单管理</cite></a>
  </div>
</div>

<div class="layui-fluid">
  <div class="layui-card">
    <div class="layui-tab layui-tab-brief">
      <ul class="layui-tab-title">
        <li class="layui-this">支付订单</li>
      </ul>
      <div class="layui-tab-content">
        <!-- 搜索表单 + 数据统计 + 数据表格 -->
      </div>
    </div>
  </div>
</div>
```

### 必备搜索字段

- **时间范围**: `createTimeStart`, `createTimeEnd` (默认当天)
- **商户ID**: `mchId`
- **订单号**: `payOrderId`, `mchOrderNo`
- **状态**: `status` (下拉选择)

### 数据统计展示

使用 `blockquote` 展示关键指标：

```html
<blockquote class="layui-elem-quote">
  提交订单数:<span id="allTotalCount" style="color: blue;"></span>
  订单总金额:<span id="allTotalAmount" style="color: blue;"></span>
  已付订单数:<span id="successTotalCount" style="color: green;"></span>
  已付总金额:<span id="successTotalAmount" style="color: green;"></span>
  成功率:<span id="successRate" style="color: green;"></span>
</blockquote>
```

### 行操作按钮

- **查看** (必备)
- **补单** (仅特定状态可用)
- **修改** (根据条件显示)
- **查单** (查询上游接口状态)

## 2. 支付配置页面模式

### 页面特点

- 简洁的搜索表单
- 操作按钮区（新增、编辑等）
- 数据表格展示

### 权限控制

```javascript
var authEdit = true;
admin.req({
  type: 'get',
  url: '/api/mch_info/checkAuth',
  data: { authAction: 'ROLE_PAY_CONFIG_EDIT' },
  success: function(res){
    if(res.data == 'RET_SERVICE_PAGE_NO_AUTH'){
      authEdit = false;
      $("#createButton").removeAttr("data-events");
    }
  }
});
```

### 状态显示

```javascript
var tplStatus = function(d){
  if(d.status == 0) return "关闭";
  else if(d.status == 1) return "<span style='color: green'>开启</span>";
};

var tplRate = function(d){
  return "<span style='color: blue'>"+ d.rate+"%</span>";
};
```

## 3. 对账管理页面模式

### 页面布局

对账页面通常更简洁，主要包含：

- 简单搜索表单（通常只有 1-2 个搜索字段）
- 数据表格
- 查看详情操作

### 常见对账模块

- **缓冲池管理** (`reconciliation/pool/`)
- **批次管理** (`reconciliation/batch/`)
- **差错管理** (`reconciliation/mistake/`)
- **商户账单** (`reconciliation/mch_bill/`)

### 数据格式

对账数据通常包含：

```javascript
cols: [[
  {field: 'channelMchId', title: '渠道商户ID'},
  {field: 'batchNo', title: '对账批次号'},
  {field: 'billDate', title: '账单时间', templet: '<div>{{ layui.util.toDateString(d.billDate, "yyyy-MM-dd") }}</div>'},
  {field: 'bankType', title: '银行类型', templet: '<div>{{ d.bankType == "wxpay" ? "微信" : "支付宝" }}</div>'},
  {field: 'handleStatus', title: '处理状态', templet: '<div>{{ d.handleStatus == 0 ? "未处理" : "已处理" }}</div>'},
  {field: 'edite', title: '操作', toolbar: '#actionBar'}
]]
```

## 4. 数据统计仪表板模式

### 组件组成

1. **数据卡片轮播**
2. **ECharts 图表** (折线图、饼图、柱状图)
3. **实时数据更新**

### 轮播图配置

```javascript
$('.layadmin-carousel').each(function(){
  var othis = $(this);
  carousel.render({
    elem: this,
    width: '100%',
    arrow: 'none',
    interval: othis.data('interval') || 5000,
    autoplay: true,
    trigger: (device.ios || device.android) ? 'click' : 'hover'
  });
});
```

### 数据卡片

```html
<ul class="layui-row layui-col-space10">
  <li class="layui-col-xs6 layui-col-sm3">
    <div class="layadmin-backlog-body">
      <h3>今日支付订单</h3>
      <p><cite id="todayOrderCount">0</cite></p>
    </div>
  </li>
</ul>
```

### 并发请求优化

```javascript
Promise.all([
  fetchData('/api/statistics/pay'),
  fetchData('/api/statistics/recharge'),
  fetchData('/api/statistics/agentpay')
]).then(function(results){
  updateCharts(results);
});
```

## 5. 通用代码模式总结

### 面包屑导航

所有页面都应包含面包屑导航：

```html
<div class="layui-breadcrumb" lay-filter="breadcrumb">
  <a lay-href="">主页</a>
  <a><cite>当前页面</cite></a>
</div>

<script>
layui.element.render('breadcrumb', 'breadcrumb');
</script>
```

### API 请求规范

```javascript
admin.req({
  type: 'get',
  url: layui.setter.baseUrl + '/api/endpoint',
  data: {
    access_token: layui.data(layui.setter.tableName).access_token
  },
  success: function(res){
    if(res.code == 0){
      // 处理成功
    }
  }
});
```

### 表格重载规范

```javascript
table.reload('tableReload', {
  page: { curr: 1 },  // 重置到第一页
  where: searchParams
});
```

### 页面跳转规范

```javascript
// 推荐使用 baseLocal
location.href = layui.setter.baseLocal + "path/to/page/id=" + data.id;

// 或使用 hash
location.hash = "/path/to/page?id=" + data.id;
```

### 日期格式化

```javascript
// 使用 layui.util 工具
layui.util.toDateString(d.createTime, "yyyy-MM-dd HH:mm:ss")
```

### 金额显示

```javascript
// 千分位格式化
function formatAmount(amount) {
  return '￥' + parseFloat(amount || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}
```

## 6. 最佳实践

1. **统一布局**: 所有页面使用相同的布局结构
2. **权限优先**: 在页面加载时检查权限
3. **数据验证**: 前后端都要进行数据验证
4. **错误处理**: 提供友好的错误提示
5. **性能优化**: 使用并发请求、懒加载等技术
6. **响应式设计**: 确保在不同设备上正常显示
7. **代码复用**: 使用模板函数复用渲染逻辑
