# ECharts 集成指南

## 1. ECharts 在 Layui 中的引入方式

### 配置扩展模块

在 `config.js` 中配置 ECharts 扩展：

```javascript
extend: [
  'echarts',       // echarts 核心包
  'echartsTheme'   // echarts 主题
]
```

### 基本使用

```javascript
layui.use(['echarts'], function(){
  var echarts = layui.echarts;

  // 创建图表实例
  var myChart = echarts.init(document.getElementById('chartId'), layui.echartsTheme);

  // 设置图表配置
  myChart.setOption({
    title: { text: '示例图表' },
    xAxis: { type: 'category', data: ['A', 'B', 'C'] },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: [10, 20, 30] }]
  });

  // 响应式调整
  window.onresize = function(){
    myChart.resize();
  };
});
```

## 2. 主题配置（echartsTheme）

LayuiAdmin 提供了内置的 ECharts 主题，主题配置文件位于 `lib/echartsTheme.js`：

```javascript
layui.define(function(exports) {
  exports('echartsTheme', {
    // 默认色板
    color: [
      '#009688', '#1E9FFF', '#5FB878', '#FFB980', '#D87A80',
      '#8d1b6d', '#589c66', '#0580c2', '#e67a51', '#adb5bd'
    ],

    // 图表标题
    title: {
      textStyle: {
        fontWeight: 'normal',
        color: '#666'
      }
    },

    // 工具箱
    toolbox: {
      color: ['#1e90ff', '#1e90ff', '#1e90ff', '#1e90ff'],
      effectiveColor: '#ff4500'
    }
  });
});
```

## 3. 轮播图表模式

在数据统计仪表板中，可以使用轮播方式展示多个图表：

```javascript
layui.use(['carousel', 'echarts'], function(){
  var echarts = layui.echarts;
  var carousel = layui.carousel;
  var echartsApp = [];

  // 多个图表配置
  var options = [
    {
      title: {text: '今日流量趋势', x: 'center'},
      tooltip: {trigger: 'axis'},
      xAxis: [{type: 'category', data: ['06:00', '06:30', '07:00']}],
      yAxis: [{type: 'value'}],
      series: [{name:'PV', type:'line', data: [111, 222, 333]}]
    },
    {
      title: {text: '访客浏览器分布', x: 'center'},
      tooltip: {trigger: 'item'},
      legend: {data:['Chrome', 'Firefox', 'IE', 'Safari']},
      series: [{type:'pie', data: [...]}]
    }
  ];

  // 渲染函数
  var renderDataView = function(index){
    echartsApp[index] = echarts.init(elemDataView[index], layui.echartsTheme);
    echartsApp[index].setOption(options[index]);
    window.onresize = echartsApp[index].resize;
  };

  // 监听轮播切换
  carousel.on('change(LAY-index-dataview)', function(obj){
    renderDataView(carouselIndex = obj.index);
  });
});
```

## 4. 单图表模式

对于单个图表，直接初始化即可：

```javascript
layui.use(['echarts'], function(){
  var echarts = layui.echarts;
  var myChart = echarts.init(document.getElementById('payOrderAcount'), layui.echartsTheme);

  myChart.setOption({
    tooltip: {trigger: 'axis', formatter: "{b}<br>交易金额：{c}"},
    xAxis: {
      type: 'category',
      data: ['7天前', '6天前', '5天前', '4天前', '3天前', '前天', '昨天']
    },
    yAxis: {type: 'value'},
    series: [{
      type: 'line',
      data: [1200, 1800, 1500, 2200, 1900, 2800, 3100],
      smooth: true,
      itemStyle: {normal: {areaStyle: {type: 'default'}}}
    }]
  });

  // 响应式调整
  window.onresize = function(){
    myChart.resize();
  }
});
```

## 5. 常用图表类型示例

### 折线图（流量趋势）

```javascript
{
  title: {text: '今日流量趋势'},
  tooltip: {trigger: 'axis'},
  legend: {data: ['PV', 'UV']},
  xAxis: [{
    type: 'category',
    boundaryGap: false,
    data: ['06:00', '06:30', '07:00', '07:30', '08:00']
  }],
  yAxis: [{type: 'value'}],
  series: [
    {name:'PV', type:'line', smooth: true, data: [111, 222, 333, 444, 555]},
    {name:'UV', type:'line', smooth: true, data: [11, 22, 33, 44, 55]}
  ]
}
```

### 饼图（数据分布）

```javascript
{
  title: {text: '支付方式分布'},
  tooltip: {trigger: 'item', formatter: "{a} <br/>{b}: {c} ({d}%)"},
  legend: {
    orient: 'vertical',
    x: 'left',
    data: ['支付宝', '微信支付', '银联', '其他']
  },
  series: [{
    name: '支付方式',
    type: 'pie',
    radius: '55%',
    center: ['50%', '50%'],
    data: [
      {value: 335, name: '支付宝'},
      {value: 310, name: '微信支付'},
      {value: 234, name: '银联'},
      {value: 135, name: '其他'}
    ]
  }]
}
```

### 柱状图（排行榜）

```javascript
{
  title: {text: '商户交易排行'},
  tooltip: {trigger: 'axis', formatter: "{b}<br/>交易金额：￥{c}"},
  xAxis: {type: 'value', boundaryGap: [0, 0.01]},
  yAxis: {type: 'category', data: ['商户A', '商户B', '商户C', '商户D', '商户E']},
  series: [{
    name: '交易金额',
    type: 'bar',
    data: [18203, 23489, 29034, 104970, 131744]
  }]
}
```

## 6. 响应式图表配置

### 监听侧边栏收缩

```javascript
layui.admin.on('side', function(){
  setTimeout(function(){
    // 重新渲染所有图表
    for(var i = 0; i < echartsApp.length; i++){
      if(echartsApp[i]){
        echartsApp[i].resize();
      }
    }
  }, 300);
});
```

### 监听路由切换

```javascript
layui.admin.on('hash(tab)', function(){
  layui.router().path.join('') || renderChart(carouselIndex);
});
```

### 窗口大小变化

```javascript
window.onresize = function(){
  for(var i = 0; i < echartsApp.length; i++){
    if(echartsApp[i]){
      echartsApp[i].resize();
    }
  }
};
```

## 7. 金额格式化工具函数

### 千分位格式化

```javascript
function formatNumberWithCommas(number) {
  if (number == null || number === '' || isNaN(number)) return '0.00';
  var num = parseFloat(number);
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

// 使用示例
formatNumberWithCommas(1234567.89); // "1,234,567.89"
```

### 带提示的金额显示

```javascript
function formatAmountWithTooltip(number) {
  if (number == null || number === '' || isNaN(number)) {
    return '<span class="amount-display">0.00</span>';
  }
  var formatted = formatNumberWithCommas(number);
  var fullDisplay = formatFullNumberWithCommas(number);
  return '<span class="amount-display" data-original="' + fullDisplay +
         '" data-formatted="' + formatted +
         '" style="cursor: pointer; border-bottom: 1px dashed #ccc;">' +
         formatted + '</span>';
}
```

## 8. 性能优化（并发请求）

使用 `Promise.all` 并发请求多个数据接口：

```javascript
Promise.all([
  new Promise(function(resolve, reject) {
    admin.req({
      type: 'get',
      url: '/api/statistics/pay',
      success: function(res) {
        resolve(res.code === 0 ? res.data : null);
      }
    });
  }),
  new Promise(function(resolve, reject) {
    admin.req({
      type: 'get',
      url: '/api/statistics/recharge',
      success: function(res) {
        resolve(res.code === 0 ? res.data : null);
      }
    });
  }),
  new Promise(function(resolve, reject) {
    admin.req({
      type: 'get',
      url: '/api/statistics/agentpay',
      success: function(res) {
        resolve(res.code === 0 ? res.data : null);
      }
    });
  })
]).then(function(results) {
  // 处理并发结果
  var payData = results[0];
  var rechargeData = results[1];
  var agentpayData = results[2];

  // 更新图表
  updateCharts(payData, rechargeData, agentpayData);
});
```

## 9. 常见问题

### Q1: 图表不显示？

- 检查容器元素是否存在
- 检查容器是否设置了高度
- 确保在 DOM 加载完成后初始化图表

### Q2: 如何更新图表数据？

```javascript
myChart.setOption({
  series: [{
    data: newData
  }]
});
```

### Q3: 如何销毁图表实例？

```javascript
myChart.dispose();
```
