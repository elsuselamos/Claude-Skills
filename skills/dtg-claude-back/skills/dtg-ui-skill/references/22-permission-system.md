# 权限控制系统

> LayuiAdmin 企业级权限管理最佳实践

## 概述

在企业级应用中，权限控制是核心功能之一。LayuiAdmin 提供了完整的权限管理体系，包括：
- 菜单权限控制
- 按钮权限控制
- 接口权限验证
- 数据权限过滤

## 菜单权限

### 菜单配置

在 LayuiAdmin 中，菜单权限通常通过后端动态返回：

```javascript
// 菜单数据结构
{
  "list": [{
    "name": "订单管理",
    "icon": "layui-icon-list",
    "jump": "order/index",
    "spread": true,
    "children": [{
      "name": "支付订单",
      "jump": "order/pay/index"
    }, {
      "name": "退款订单",
      "jump": "order/refund/index"
    }]
  }]
}
```

### 菜单权限判断

```javascript
// 判断是否有菜单权限
function hasMenuPermission(menuPath){
  var menus = layui.data(layui.setter.tableName).menus || [];
  return menus.some(function(menu){
    return menu.jump === menuPath ||
           (menu.children && menu.children.some(function(child){
             return child.jump === menuPath;
           }));
  });
}
```

## 按钮权限

### 按钮权限模板

```html
<!-- 方式1: 使用模板引擎判断权限 -->
<script type="text/html" id="toolbarTpl">
  {{# if(layui.permission.has('ORDER_DETAIL')){ }}
    <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="detail">查看</a>
  {{# } }}

  {{# if(layui.permission.has('ORDER_EDIT')){ }}
    <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
  {{# } }}

  {{# if(layui.permission.has('ORDER_DELETE')){ }}
    <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="delete">删除</a>
  {{# } }}
</script>
```

### 按钮权限判断

```javascript
// 方式2: JavaScript 判断按钮权限
layui.use(['admin'], function(){
  var admin = layui.admin;

  // 判断是否有某个权限
  if(admin.hasPermission('ORDER_DELETE')){
    $('#deleteBtn').show();
  } else {
    $('#deleteBtn').hide();
  }
});
```

### 扩展 permission 模块

```javascript
// 定义 permission 模块
layui.define(function(exports){
  var permission = {
    // 权限列表
    permissions: [],

    // 初始化权限
    init: function(permList){
      this.permissions = permList || [];
    },

    // 判断是否有权限
    has: function(permCode){
      return this.permissions.indexOf(permCode) !== -1;
    },

    // 批量判断权限
    hasAll: function(permCodes){
      var self = this;
      return permCodes.every(function(code){
        return self.has(code);
      });
    },

    // 判断是否有任一权限
    hasAny: function(permCodes){
      var self = this;
      return permCodes.some(function(code){
        return self.has(code);
      });
    }
  };

  exports('permission', permission);
});

// 使用示例
layui.use(['permission'], function(){
  var permission = layui.permission;

  // 初始化权限（从后端获取）
  permission.init(['ORDER_VIEW', 'ORDER_EDIT', 'ORDER_DELETE']);

  // 判断权限
  if(permission.has('ORDER_DELETE')){
    // 有删除权限
  }
});
```

## 接口权限

### 自动携带 Token

```javascript
// admin.req 会自动携带 access_token
admin.req({
  type: 'post',
  url: layui.setter.baseUrl + '/api/delete',
  data: {id: 123},
  success: function(res){
    // 后端会验证 access_token 的有效性
  }
});
```

### 权限验证处理

```javascript
admin.req({
  type: 'post',
  url: layui.setter.baseUrl + '/api/sensitiveOperation',
  data: {id: 123},
  success: function(res){
    if(res.code == 0){
      // 操作成功
    } else if(res.code == 403){
      layer.msg('没有操作权限', {icon: 2});
    }
  }
});
```

### 全局权限拦截

```javascript
// 拦截所有 admin.req 请求
layui.use(['admin'], function(){
  var admin = layui.admin;
  var originalReq = admin.req;

  // 重写 admin.req
  admin.req = function(options){
    var originalSuccess = options.success;

    options.success = function(res){
      if(res.code == 401){
        // 未登录或登录过期
        layer.alert('登录已过期', {icon: 2}, function(){
          location.href = layui.setter.baseLocal + 'user/login';
        });
      } else if(res.code == 403){
        // 无权限
        layer.msg('没有操作权限', {icon: 2});
      } else {
        originalSuccess && originalSuccess(res);
      }
    };

    originalReq.call(admin, options);
  };
});
```

## 数据权限

### 数据权限过滤

```javascript
// 根据用户角色过滤数据
admin.req({
  type: 'get',
  url: layui.setter.baseUrl + '/api/order/list',
  data: {
    // 服务端根据用户角色返回相应数据
    // 管理员：可以看到所有订单
    // 商户：只能看到自己的订单
    // 代理商：只能看到自己下级商户的订单
  },
  success: function(res){
    table.render({
      elem: '#dataTable',
      data: res.data,
      cols: [[...]]
    });
  }
});
```

### 商户数据隔离

```javascript
// 商户只能看到自己的数据
table.render({
  elem: '#dataTable',
  url: layui.setter.baseUrl + '/api/order/list',
  where: {
    // 商户ID会从登录信息中获取，自动添加到请求参数
    mchId: layui.data(layui.setter.tableName).mchId
  },
  cols: [[...]]
});
```

## 角色管理

### 角色权限配置

```javascript
// 角色权限配置数据结构
var rolePermissions = {
  admin: ['*'], // 管理员拥有所有权限
  operator: [
    'ORDER_VIEW',
    'ORDER_EDIT',
    'MERCHANT_VIEW'
  ],
  merchant: [
    'ORDER_VIEW',
    'ORDER_EDIT',
    'REFUND_VIEW'
  ]
};

// 获取当前用户角色的权限
function getUserPermissions(){
  var userInfo = layui.data(layui.setter.tableName);
  var role = userInfo.role;
  return rolePermissions[role] || [];
}
```

### 角色切换功能

```javascript
// 管理员切换商户视图
function switchToMerchantView(mchId){
  admin.req({
    type: 'post',
    url: layui.setter.baseUrl + '/api/admin/switchMerchant',
    data: {mchId: mchId},
    success: function(res){
      if(res.code == 0){
        layer.msg('切换成功');
        // 刷新页面
        location.reload();
      }
    }
  });
}
```

## 前端权限示例

### 完整的列表页权限控制

```html
<!DOCTYPE html>
<html>
<head>
  <title>订单管理</title>
</head>
<body>

<!-- 操作按钮组（根据权限显示） -->
<div class="layui-btn-group">
  <button class="layui-btn layui-btn-normal" id="addBtn" perm="ORDER_ADD">
    <i class="layui-icon layui-icon-add-1"></i> 新增
  </button>
  <button class="layui-btn layui-btn-danger" id="batchDeleteBtn" perm="ORDER_DELETE">
    <i class="layui-icon layui-icon-delete"></i> 批量删除
  </button>
  <button class="layui-btn layui-btn-primary" id="exportBtn" perm="ORDER_EXPORT">
    <i class="layui-icon layui-icon-export"></i> 导出
  </button>
</div>

<!-- 数据表格 -->
<table id="dataTable" lay-filter="dataTable"></table>

<!-- 行操作工具栏（根据权限显示） -->
<script type="text/html" id="toolbarTpl">
  {{# if(layui.permission.has('ORDER_DETAIL')){ }}
    <a class="layui-btn layui-btn-primary layui-btn-xs" lay-event="detail">查看</a>
  {{# } }}

  {{# if(layui.permission.has('ORDER_EDIT')){ }}
    <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
  {{# } }}

  {{# if(layui.permission.has('ORDER_DELETE')){ }}
    <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="delete">删除</a>
  {{# } }}
</script>

<script>
layui.use(['admin', 'table', 'permission'], function(){
  var admin = layui.admin;
  var table = layui.table;
  var permission = layui.permission;

  // 初始化权限
  permission.init(layui.data(layui.setter.tableName).permissions || []);

  // 根据权限显示/隐藏按钮
  $('[perm]').each(function(){
    var perm = $(this).attr('perm');
    if(!permission.has(perm)){
      $(this).hide();
    }
  });

  // 渲染表格
  table.render({
    elem: '#dataTable',
    url: layui.setter.baseUrl + '/api/order/list',
    cols: [[
      {field: 'id', title: 'ID'},
      {field: 'orderNo', title: '订单号'},
      {field: 'amount', title: '金额'},
      {fixed: 'right', title: '操作', toolbar: '#toolbarTpl'}
    ]]
  });

  // 行操作事件
  table.on('tool(dataTable)', function(obj){
    var data = obj.data;

    if(obj.event === 'detail'){
      if(!permission.has('ORDER_DETAIL')){
        layer.msg('没有查看权限');
        return;
      }
      location.href = '/order/detail/id=' + data.id;
    } else if(obj.event === 'edit'){
      if(!permission.has('ORDER_EDIT')){
        layer.msg('没有编辑权限');
        return;
      }
      location.href = '/order/edit/id=' + data.id;
    } else if(obj.event === 'delete'){
      if(!permission.has('ORDER_DELETE')){
        layer.msg('没有删除权限');
        return;
      }
      // 删除操作...
    }
  });

  // 新增按钮
  $('#addBtn').on('click', function(){
    if(!permission.has('ORDER_ADD')){
      layer.msg('没有新增权限');
      return;
    }
    location.href = '/order/add';
  });
});
</script>
</body>
</html>
```

## 权限常量定义

```javascript
// 权限常量定义
var PermissionCodes = {
  // 订单管理
  ORDER_VIEW: 'ORDER_VIEW',
  ORDER_ADD: 'ORDER_ADD',
  ORDER_EDIT: 'ORDER_EDIT',
  ORDER_DELETE: 'ORDER_DELETE',
  ORDER_EXPORT: 'ORDER_EXPORT',

  // 商户管理
  MERCHANT_VIEW: 'MERCHANT_VIEW',
  MERCHANT_ADD: 'MERCHANT_ADD',
  MERCHANT_EDIT: 'MERCHANT_EDIT',
  MERCHANT_DELETE: 'MERCHANT_DELETE',
  MERCHANT_AUDIT: 'MERCHANT_AUDIT',

  // 用户管理
  USER_VIEW: 'USER_VIEW',
  USER_ADD: 'USER_ADD',
  USER_EDIT: 'USER_EDIT',
  USER_DELETE: 'USER_DELETE',
  USER_RESET_PASSWORD: 'USER_RESET_PASSWORD',

  // 系统配置
  CONFIG_VIEW: 'CONFIG_VIEW',
  CONFIG_EDIT: 'CONFIG_EDIT',

  // 超级管理员
  SUPER_ADMIN: '*'
};
```

## 注意事项

1. **前端权限仅用于 UI 控制**，真正的权限验证必须在后端进行
2. **权限验证应该分层**：菜单权限、按钮权限、接口权限、数据权限
3. **权限粒度要合理**，过细会增加维护成本，过粗会降低安全性
4. **角色设计要清晰**，避免权限交叉和冲突
5. **敏感操作需要二次确认**，即使有权限也要防止误操作

## 相关文档

- [13-layuiadmin-guide.md](./13-layuiadmin-guide.md) - LayuiAdmin 开发指南
- [18-api-integration-guide.md](./18-api-integration-guide.md) - API 集成指南
