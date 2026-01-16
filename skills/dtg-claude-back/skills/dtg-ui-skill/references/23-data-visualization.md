# 数据可视化组件

> LayuiAdmin + ECharts 企业级数据可视化实践

## 概述

在企业级应用中，数据可视化是展示关键业务指标的重要手段。本文档介绍如何在 LayuiAdmin 中集成 ECharts 实现数据可视化。

## ECharts 集成

### 基础配置

```javascript
layui.use(['admin'], function(){
  var admin = layui.admin;

  // 初始化 ECharts
  var chart = echarts.init(document.getElementById('chart'));

  // 配置项
  var option = {
    title: {
      text: '数据统计'
    },
    tooltip: {},
    xAxis: {
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {},
    series: [{
      name: '销量',
      type: 'bar',
      data: [5, 20, 36, 10, 10, 20, 10]
    }]
  };

  // 设置配置项
  chart.setOption(option);

  // 响应式
  window.addEventListener('resize', function(){
    chart.resize();
  });
});
```

### 折线图 - 交易趋势

```javascript
// 交易趋势折线图
function renderTrendChart(elementId, data){
  var chart = echarts.init(document.getElementById(elementId));

  var option = {
    title: {
      text: '交易趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>{a}: {c} 笔'
    },
    legend: {
      data: ['支付订单', '退款订单'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.dates
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '支付订单',
        type: 'line',
        smooth: true,
        data: data.payOrders,
        itemStyle: {color: '#1E9FFF'}
      },
      {
        name: '退款订单',
        type: 'line',
        smooth: true,
        data: data.refundOrders,
        itemStyle: {color: '#FF5722'}
      }
    ]
  };

  chart.setOption(option);
  return chart;
}

// 使用示例
admin.req({
  url: layui.setter.baseUrl + '/api/statistics/trend',
  success: function(res){
    if(res.code == 0){
      renderTrendChart('trendChart', res.data);
    }
  }
});
```

### 饼图 - 支付方式占比

```javascript
// 支付方式饼图
function renderPieChart(elementId, data){
  var chart = echarts.init(document.getElementById(elementId));

  var option = {
    title: {
      text: '支付方式占比',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '支付方式',
        type: 'pie',
        radius: '60%',
        data: data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  chart.setOption(option);
  return chart;
}

// 使用示例
var payMethodData = [
  {value: 335, name: '微信支付'},
  {value: 310, name: '支付宝'},
  {value: 234, name: '银行卡'},
  {value: 135, name: '云闪付'},
  {value: 1548, name: '其他'}
];
renderPieChart('payMethodChart', payMethodData);
```

### 柱状图 - 商户交易排行

```javascript
// 商户交易排行柱状图
function renderBarChart(elementId, data){
  var chart = echarts.init(document.getElementById(elementId));

  var option = {
    title: {
      text: '商户交易排行',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: '{b}<br/>交易额: ￥{c}'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      boundaryGap: [0, 0.01]
    },
    yAxis: {
      type: 'category',
      data: data.mchNames
    },
    series: [
      {
        name: '交易额',
        type: 'bar',
        data: data.amounts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            {offset: 0, color: '#1E9FFF'},
            {offset: 1, color: '#00B0FF'}
          ])
        }
      }
    ]
  };

  chart.setOption(option);
  return chart;
}
```

### 仪表盘 - 成功率

```javascript
// 支付成功率仪表盘
function renderGaugeChart(elementId, value){
  var chart = echarts.init(document.getElementById(elementId));

  var option = {
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        min: 0,
        max: 100,
        splitNumber: 10,
        axisLine: {
          lineStyle: {
            width: 20,
            color: [
              [0.3, '#FF5722'],
              [0.7, '#FFB800'],
              [1, '#009688']
            ]
          }
        },
        pointer: {
          itemStyle: {
            color: 'auto'
          }
        },
        axisTick: {
          distance: -20,
          length: 5
        },
        splitLine: {
          distance: -20,
          length: 15
        },
        axisLabel: {
          distance: -40,
          formatter: '{value}%'
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}%',
          color: 'auto',
          fontSize: 30
        },
        data: [{value: value}]
      }
    ]
  };

  chart.setOption(option);
  return chart;
}
```

## 实时数据更新

### 定时刷新

```javascript
var chart = null;
var timer = null;

// 初始化图表
function initChart(){
  chart = echarts.init(document.getElementById('realtimeChart'));
  loadChartData();

  // 每30秒刷新一次
  timer = setInterval(loadChartData, 30000);
}

// 加载图表数据
function loadChartData(){
  admin.req({
    url: layui.setter.baseUrl + '/api/statistics/realtime',
    success: function(res){
      if(res.code == 0){
        updateChart(res.data);
      }
    }
  });
}

// 更新图表
function updateChart(data){
  chart.setOption({
    series: [{
      data: data
    }]
  });
}

// 页面销毁时清除定时器
$(window).on('unload', function(){
  if(timer){
    clearInterval(timer);
  }
});
```

## 响应式处理

```javascript
// 监听窗口大小变化
var charts = [];

function initCharts(){
  charts.push(echarts.init(document.getElementById('chart1')));
  charts.push(echarts.init(document.getElementById('chart2')));
  charts.push(echarts.init(document.getElementById('chart3')));
}

// 统一处理响应式
window.addEventListener('resize', function(){
  charts.forEach(function(chart){
    chart.resize();
  });
});
```

## 注意事项

1. **销毁实例**：页面销毁时记得调用 `chart.dispose()`
2. **内存泄漏**：避免重复创建 ECharts 实例
3. **响应式**：监听 window resize 事件
4. **数据格式**：确保后端返回的数据格式正确
5. **性能优化**：大数据量时使用数据抽样

## 相关文档

- [14-echarts-integration.md](./14-echarts-integration.md) - ECharts 集成指南
- [18-api-integration-guide.md](./18-api-integration-guide.md) - API 集成指南
