# LayuiAdmin 开发指南

## 1. LayuiAdmin 简介

LayuiAdmin 是基于 Layui 框架的企业级后台管理模板，提供了一套完整的前端解决方案。与标准 Layui 相比，LayuiAdmin 提供了更强大的功能：

- 单页面应用（SPA）架构
- 完善的路由系统
- 模块化开发支持
- 内置权限控制
- 丰富的主题系统

## 2. 与标准 Layui 的区别

| 特性 | 标准 Layui | LayuiAdmin |
|------|-----------|------------|
| 架构 | 多页面 | 单页面应用（SPA） |
| 路由 | 无 | 内置路由系统 |
| 模块加载 | layui.use() | layui.use() + 路由懒加载 |
| 配置文件 | 无 | config.js 统一配置 |
| 权限控制 | 需自行实现 | 内置权限拦截 |
| 弹层系统 | layer | admin.popup |

## 3. 配置文件详解（config.js）

LayuiAdmin 的核心配置文件，定义了应用的各种参数：

```javascript
layui.define(function(exports){
  exports('setter', {
    // 容器配置
    container: 'LAY_app',           // 容器ID
    base: layui.cache.base,         // 记录 layuiAdmin 文件夹所在路径
    views: layui.cache.base + 'views/',  // 视图所在目录
    entry: 'index',                 // 默认视图文件名
    engine: '.html',                // 视图文件后缀名

    // API 配置
    baseUrl: '/api',                // API 基础路径
    baseLocal: '/x_mgr/start/index.html#/',  // 本地开发路径

    // 应用信息
    name: '运营平台',                // 应用名称
    tableName: 'layuiAdmin',        // 本地存储表名
    MOD_NAME: 'admin',              // 模块事件名

    // 调试和拦截
    debug: false,                   // 是否开启调试模式
    interceptor: true,              // 是否开启未登入拦截

    // 请求/响应配置
    request: {
      tokenName: 'access_token'     // 自动携带 token 的字段名
    },
    response: {
      statusName: 'code',           // 数据状态的字段名称
      statusCode: {
        ok: 0,                      // 数据状态一切正常的状态码
        logout: 1001                // 登录状态失效的状态码
      },
      msgName: 'msg',               // 状态信息的字段名称
      dataName: 'data'              // 数据详情的字段名称
    },

    // 独立页面路由
    indPage: [
      '/user/login'                 // 登入页
    ],

    // 扩展的第三方模块
    extend: [
      'echarts',                    // echarts 核心包
      'echartsTheme'                // echarts 主题
    ],

    // 主题配置
    theme: {
      color: [{
        main: '#20222A',            // 主题色
        selected: '#009688',        // 选中色
        alias: 'default'            // 默认别名
      }]
    }
  });
});
```

## 4. 路由系统使用

LayuiAdmin 使用 hash 路由，支持参数传递：

```javascript
// 获取路由参数
var router = layui.router();
var payPassageId = router.search.payPassageId;

// 页面跳转
location.hash = '/config/pay_passage_account/create/payPassageId=' + payPassageId;

// 使用 baseLocal 跳转（推荐）
location.href = layui.setter.baseLocal + "config/pay_passage_account/update/id=" + data.id;
```

## 5. admin.req API 使用

`admin.req` 是 LayuiAdmin 封装的统一请求方法，自动处理 token 和错误状态码：

```javascript
admin.req({
  url: '/api/pay_order/list',
  type: 'get',
  data: {
    access_token: layui.data(layui.setter.tableName).access_token,
    status: 2
  },
  done: function(res){
    // 只有 response 的 code 正常才会执行
    console.log(res.data);
  }
});
```

**关键特性**：
- 自动从 localStorage 获取 token
- 自动处理 1001 登录失效状态码
- 支持 done/error/complete 回调

## 6. admin.popup 弹层

`admin.popup` 是 LayuiAdmin 提供的弹层方法，支持视图渲染：

```javascript
admin.popup({
  title: '编辑用户',
  area: ['500px', '450px'],
  id: 'LAY-popup-user-add',
  success: function(layero, index){
    view(this.id).render('user/user/userform', data).done(function(){
      form.render(null, 'layuiadmin-form-useradmin');
      form.on('submit(LAY-user-front-submit)', function(data){
        layui.table.reload('LAY-user-manage');
        layer.close(index);
      });
    });
  }
});
```

## 7. 权限控制模式

LayuiAdmin 推荐的权限控制方式：

```javascript
// 检查权限
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
      $("#createButton").removeAttr("lay-href");
    }
  }
});

// 在操作中使用权限检查
table.on('tool(cList)', function(obj){
  if(authEdit==false){
    layer.msg('没有操作权限', {icon: 2});
    return;
  }
  // 执行操作...
});
```

## 8. 常见问题

### Q1: 如何引入 ECharts？

在 `config.js` 中配置扩展模块：
```javascript
extend: ['echarts', 'echartsTheme']
```

使用：
```javascript
layui.use(['echarts'], function(){
  var echarts = layui.echarts;
  var myChart = echarts.init(document.getElementById('chart'));
  myChart.setOption({...});
});
```

### Q2: 如何获取当前登录用户信息？

```javascript
var userInfo = layui.data(layui.setter.tableName);
console.log(userInfo.access_token);
```

### Q3: 如何监听侧边栏收缩？

```javascript
layui.admin.on('side', function(){
  setTimeout(function(){
    // 重新渲染图表或调整布局
    renderChart();
  }, 300);
});
```

### Q4: 如何实现退出登录？

```javascript
admin.events.logout = function(){
  admin.req({
    url: './json/user/logout.js',
    type: 'get',
    data: {},
    done: function(res){
      localStorage.clear();
      sessionStorage.clear();
      admin.exit();  // 跳转到登入页
    }
  });
};
```

### Q5: 如何切换主题？

```javascript
admin.theme({
  color: {
    main: '#20222A',
    selected: '#009688',
    alias: 'default'
  }
});
```
