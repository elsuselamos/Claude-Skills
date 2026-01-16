# Layui 表格模块详解

## 数据表格

### 基础数据表格

```html
<table id="demo" lay-filter="test"></table>

<script>
layui.use('table', function(){
  var table = layui.table;

  table.render({
    elem: '#demo',
    height: 500,
    url: '/api/data', // 数据接口
    page: true, // 开启分页
    cols: [[ // 表头
      {field: 'id', title: 'ID', width:80, sort: true},
      {field: 'username', title: '用户名', width:120},
      {field: 'email', title: '邮箱', width:150},
      {field: 'sign', title: '签名'},
      {field: 'sex', title: '性别', width:80},
      {field: 'city', title: '城市', width:100},
      {field: 'experience', title: '积分', width:80, sort: true}
    ]]
  });
});
</script>
```

### 表格参数

| 参数 | 说明 | 示例 |
|------|------|------|
| elem | 指定容器 | `'#demo'` |
| cols | 设置表头 | `[[...]]` |
| url | 数据接口 | `'/api/data'` |
| method | 请求方式 | `'get'` 或 `'post'` |
| where | 携带参数 | `{token: 'xxx'}` |
| contentType | 发送类型 | `'application/json'` |
| height | 容器高度 | `500` 或 `'full-50'` |
| width | 容器宽度 | `1000` |
| cellMinWidth | 单元格最小宽度 | `60` |
| done | 渲染完成回调 | `function(res, curr, count){}` |
| data | 直接赋值数据 | `[{...}, {...}]` |
| totalRow | 开启合计行 | `true` |
| page | 开启分页 | `true` 或 `{...}` |
| limit | 每页显示条数 | `20` |
| limits | 每页条数选项 | `[10, 20, 30, 50]` |
| loading | 开启加载动画 | `true` |
| title | 定义 table 标题 | `'用户表'` |
| text | 自定义文本 | `{none: '无数据'}` |
| autoSort | 自动排序 | `false` |
| initSort | 初始排序 | `{field: 'id', type: 'desc'}` |
| skin | 边框风格 | `'line'` / `'row'` / `'nob'` |
| even | 开启隔行背景 | `true` |
| size | 尺寸 | `'sm'` / `'lg'` |

### 表头参数

| 参数 | 说明 | 示例 |
|------|------|------|
| field | 字段名 | `'username'` |
| title | 标题 | `'用户名'` |
| width | 宽度 | `120` |
| minWidth | 最小宽度 | `120` |
| type | 类型 | `'checkbox'` / `'radio'` / `'numbers'` |
| fixed | 固定列 | `'left'` / `'right'` |
| unresize | 禁用拖拽 | `true` |
| sort | 开启排序 | `true` |
| edit | 开启编辑 | `'text'` |
| templet | 自定义模板 | `function(d){}` |
| toolbar | 工具条 | `'<div>xxx</div>'` |
| totalRow | 开启合计 | `true` |
| totalRowText | 合计文本 | `'合计：'` |
| style | 自定义样式 | `'color: red;'` |
| event | 单元格事件 | `'click'` |

## 表格功能

### 1. 开启复选框

```javascript
cols: [[
  {type: 'checkbox', fixed: 'left'},
  {field: 'id', title: 'ID'},
  // ...
]]
```

### 2. 开启单选框

```javascript
cols: [[
  {type: 'radio', fixed: 'left'},
  {field: 'id', title: 'ID'},
  // ...
]]
```

### 3. 开启序号列

```javascript
cols: [[
  {type: 'numbers', title: '序号'},
  {field: 'id', title: 'ID'},
  // ...
]]
```

### 4. 自定义列模板

```html
<script type="text/html" id="usernameTpl">
  <a href="/user/{{d.id}}">{{d.username}}</a>
</script>

<script>
cols: [[
  {field: 'username', title: '用户名', templet: '#usernameTpl'},
  // 或使用函数
  {field: 'sex', title: '性别', templet: function(d){
    return d.sex == '女' ? '女' : '男';
  }}
]]
</script>
```

### 5. 开启工具条

```html
<script type="text/html" id="barDemo">
  <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
  <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
</script>

<script>
cols: [[
  {fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
]]
</script>
```

### 6. 开启头部工具条

```html
<script type="text/html" id="toolbarDemo">
  <div class="layui-btn-container">
    <button class="layui-btn layui-btn-sm" lay-event="add">添加</button>
    <button class="layui-btn layui-btn-sm" lay-event="delete">删除</button>
  </div>
</script>

<script>
table.render({
  toolbar: '#toolbarDemo',
  // ...
});
</script>
```

## 表格事件

### 监听行工具事件

```javascript
table.on('tool(test)', function(obj){
  var data = obj.data; // 获得当前行数据
  var tr = obj.tr; // 获得当前行 tr 的 DOM 对象

  if(obj.event === 'del'){
    layer.confirm('真的删除行么', function(index){
      // 向服务端发送删除请求
      $.ajax({
        url: '/api/delete',
        data: {id: data.id},
        success: function(res){
          obj.del(); // 删除对应行的 DOM 结构
          layer.close(index);
        }
      });
    });
  } else if(obj.event === 'edit'){
    // 编辑逻辑
    layer.prompt({
      formType: 0,
      value: data.username
    }, function(value, index){
      // 同步更新缓存和表格
      obj.update({
        username: value
      });
      layer.close(index);
    });
  }
});
```

### 监听头部工具条事件

```javascript
table.on('toolbar(test)', function(obj){
  var checkStatus = table.checkStatus(obj.config.id);
  var data = checkStatus.data; // 获得选中的数据

  switch(obj.event){
    case 'add':
      // 添加逻辑
      break;
    case 'delete':
      if(data.length === 0){
        layer.msg('请选择一行');
      } else {
        layer.msg('删除了 ' + data.length + ' 行');
      }
      break;
  }
});
```

### 监听复选框选择

```javascript
table.on('checkbox(test)', function(obj){
  console.log(obj.checked); // 当前是否选中
  console.log(obj.data); // 选中行的数据
  console.log(obj.type); // 'all' 或 'one'
});
```

### 监听单元格编辑

```javascript
table.on('edit(test)', function(obj){
  var value = obj.value; // 得到修改后的值
  var data = obj.data; // 所在行的所有相关数据
  var field = obj.field; // 得到修改的字段

  // 编辑完后向后端发送请求
  // ...
});
```

### 监听排序

```javascript
table.on('sort(test)', function(obj){
  console.log(obj.field); // 当前排序的字段名
  console.log(obj.type); // 当前排序类型：desc、asc、null
  table.reload('id', {
    initSort: obj,
    where: {
      field: obj.field,
      order: obj.type
    }
  });
});
```

## 表格方法

### table.reload()

重载表格：

```javascript
table.reload('id', {
  where: {token: 'xxx'},
  height: 500
});
```

### table.checkStatus()

获取选中行数据：

```javascript
var checkStatus = table.checkStatus('id');
var data = checkStatus.data; // 选中行的数据
console.log(data.length); // 选中行数量
```

### table.getData()

获取表格所有数据：

```javascript
var data = table.getData('id');
```

### table.exportFile()

导出数据：

```javascript
// 导出 CSV
table.exportFile('id', data, 'csv');

// 导出为 xls 文件
table.exportFile('id', data, 'xls');
```

## 静态表格转换

```html
<table class="layui-table" lay-data="{url:'/api/data', page:true}" lay-filter="test">
  <thead>
    <tr>
      <th lay-data="{field:'username'}">用户名</th>
      <th lay-data="{field:'email'}">邮箱</th>
      <th lay-data="{field:'sign'}">签名</th>
    </tr>
  </thead>
</table>

<script>
layui.use('table', function(){
  var table = layui.table;
});
</script>
```

## 数据格式要求

后端接口返回的数据格式必须符合以下规范：

```json
{
  "code": 0,
  "msg": "",
  "count": 1000,
  "data": [
    {"id": 100, "username": "张三", "email": "test@qq.com"},
    {"id": 101, "username": "李四", "email": "test2@qq.com"}
  ]
}
```

### 自定义数据格式

如果后端返回格式不同，可以使用 parseData 参数：

```javascript
table.render({
  parseData: function(res){
    return {
      "code": res.status,
      "msg": res.message,
      "count": res.total,
      "data": res.list
    };
  }
});
```

## 完整示例

```html
<table id="demo" lay-filter="test"></table>

<script type="text/html" id="toolbarDemo">
  <div class="layui-btn-container">
    <button class="layui-btn layui-btn-sm" lay-event="add">添加</button>
    <button class="layui-btn layui-btn-sm layui-btn-danger" lay-event="delete">批量删除</button>
  </div>
</script>

<script type="text/html" id="barDemo">
  <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
  <a class="layui-btn layui-btn-danger layui-btn-xs" lay-event="del">删除</a>
</script>

<script>
layui.use('table', function(){
  var table = layui.table;
  var layer = layui.layer;

  table.render({
    elem: '#demo',
    url: '/api/user/list',
    toolbar: '#toolbarDemo',
    page: true,
    cols: [[
      {type: 'checkbox', fixed: 'left'},
      {field: 'id', title: 'ID', width:80, sort: true},
      {field: 'username', title: '用户名', width:120},
      {field: 'email', title: '邮箱', width:150},
      {field: 'phone', title: '手机号', width:120},
      {field: 'createTime', title: '创建时间', width:180},
      {fixed: 'right', title:'操作', toolbar: '#barDemo', width:150}
    ]]
  });

  // 头部工具栏事件
  table.on('toolbar(test)', function(obj){
    var checkStatus = table.checkStatus(obj.config.id);
    var data = checkStatus.data;

    if(obj.event === 'add'){
      layer.open({
        type: 1,
        title: '添加用户',
        content: '添加表单...'
      });
    } else if(obj.event === 'delete'){
      if(data.length === 0){
        layer.msg('请选择要删除的数据');
      } else {
        layer.confirm('确定删除选中的 ' + data.length + ' 条数据吗？', function(index){
          // 发送删除请求
          layer.close(index);
        });
      }
    }
  });

  // 行工具事件
  table.on('tool(test)', function(obj){
    var data = obj.data;

    if(obj.event === 'del'){
      layer.confirm('真的删除行么', function(index){
        // 发送删除请求
        obj.del();
        layer.close(index);
      });
    } else if(obj.event === 'edit'){
      layer.open({
        type: 1,
        title: '编辑用户',
        content: '编辑表单...'
      });
    }
  });
});
</script>
```

## 下一步

- 查看弹层模块 → `06-layer-module.md`
- 查看导航组件 → `07-navigation.md`
