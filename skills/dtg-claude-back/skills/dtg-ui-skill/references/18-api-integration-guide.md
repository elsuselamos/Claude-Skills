# API 集成完整指南

> 基于 716+ 实际项目 HTML 文件分析的 LayuiAdmin API 集成最佳实践

## 概述

在 LayuiAdmin 中，所有 API 请求都应使用 `admin.req()` 方法进行统一管理。这是 LayuiAdmin 提供的标准 AJAX 请求封装，内置了：
- 自动携带 access_token
- 统一的错误处理
- loading 状态管理
- 权限验证

## admin.req 基本用法

### 1. GET 请求 - 获取数据

```javascript
layui.use(['admin'], function(){
  var admin = layui.admin;

  admin.req({
    type: 'get',
    url: layui.setter.baseUrl + '/api/getData',
    data: {id: 123},
    success: function(res){
      if(res.code == 0){
        console.log('数据:', res.data);
      } else {
        layer.msg(res.msg);
      }
    }
  });
});
```

### 2. POST 请求 - 提交数据

```javascript
admin.req({
  type: 'post',
  url: layui.setter.baseUrl + '/api/saveData',
  data: {
    name: '张三',
    age: 25
  },
  success: function(res){
    if(res.code == 0){
      layer.msg('保存成功');
    } else {
      layer.msg(res.msg);
    }
  }
});
```

### 3. 完整参数配置

```javascript
admin.req({
  type: 'get',           // 请求方式: get/post
  url: '/api/list',      // 请求地址
  data: {                // 请求参数
    page: 1,
    limit: 20
  },
  dataType: 'json',      // 响应数据类型
  timeout: 10000,        // 超时时间(毫秒)
  headers: {             // 自定义请求头
    'Custom-Header': 'value'
  },
  success: function(res){
    // 成功回调
  },
  error: function(xhr){
    // 错误回调
  },
  done: function(res){
    // 完成回调（无论成功失败）
  }
});
```

## 标准响应格式

### 成功响应

```json
{
  "code": 0,
  "msg": "操作成功",
  "data": {
    "id": 1,
    "name": "数据"
  }
}
```

### 分页数据响应

```json
{
  "code": 0,
  "msg": "",
  "count": 100,
  "data": [
    {"id": 1, "name": "数据1"},
    {"id": 2, "name": "数据2"}
  ]
}
```

### 错误响应

```json
{
  "code": 1,
  "msg": "操作失败"
}
```

## 常见错误码

| code | 说明 | 处理方式 |
|------|------|----------|
| 0 | 成功 | 正常处理数据 |
| 401 | 未登录/登录过期 | 跳转到登录页 |
| 403 | 无权限 | 提示权限不足 |
| 500 | 服务器错误 | 提示服务器错误 |

## 表格数据集成

### 表格配置

```javascript
layui.use(['table', 'admin'], function(){
  var table = layui.table;
  var admin = layui.admin;

  table.render({
    elem: '#dataTable',
    url: layui.setter.baseUrl + '/api/list',
    where: {
      access_token: layui.data(layui.setter.tableName).access_token
    },
    parseData: function(res){
      // 解析服务端返回的数据
      return {
        "code": res.code,
        "msg": res.msg,
        "count": res.count,
        "data": res.data
      };
    },
    request: {
      pageName: 'page',
      limitName: 'limit'
    },
    response: {
      statusCode: 0
    },
    cols: [[
      {field: 'id', title: 'ID'},
      {field: 'name', title: '名称'}
    ]],
    page: true
  });
});
```

### 表格搜索重载

```javascript
$('#searchBtn').on('click', function(){
  table.reload('dataTable', {
    page: {curr: 1},
    where: {
      keyword: $('#keyword').val(),
      status: $('#status').val()
    }
  });
});
```

## 表单提交集成

### 表单提交

```javascript
layui.use(['form', 'admin'], function(){
  var form = layui.form;
  var admin = layui.admin;

  form.on('submit(saveBtn)', function(data){
    var formData = data.field;

    admin.req({
      type: 'post',
      url: layui.setter.baseUrl + '/api/save',
      data: formData,
      success: function(res){
        if(res.code == 0){
          layer.msg('保存成功', {icon: 1}, function(){
            // 关闭弹窗
            var index = parent.layer.getFrameIndex(window.name);
            parent.layer.close(index);
            // 刷新父页面表格
            parent.layui.table.reload('dataTable');
          });
        } else {
          layer.msg(res.msg, {icon: 2});
        }
      }
    });

    return false; // 阻止表单跳转
  });
});
```

### 表单数据回显

```javascript
// 编辑页面加载数据
var editId = layui.router().search.id;

admin.req({
  type: 'get',
  url: layui.setter.baseUrl + '/api/detail',
  data: {id: editId},
  success: function(res){
    if(res.code == 0){
      // 方式1: 使用 form.val() 回显
      form.val('editForm', res.data);

      // 方式2: 手动设置
      $('#id').val(res.data.id);
      $('#name').val(res.data.name);

      // 重新渲染表单
      form.render();
    }
  }
});
```

## 批量操作

### 批量删除

```javascript
$('#batchDeleteBtn').on('click', function(){
  var checkStatus = table.checkStatus('dataTable');
  var data = checkStatus.data;

  if(data.length === 0){
    layer.msg('请选择要删除的数据');
    return;
  }

  layer.confirm('确定删除？', function(index){
    var ids = data.map(function(item){
      return item.id;
    }).join(',');

    admin.req({
      type: 'post',
      url: layui.setter.baseUrl + '/api/batchDelete',
      data: {ids: ids},
      success: function(res){
        if(res.code == 0){
          layer.msg('删除成功');
          table.reload('dataTable');
        }
      }
    });

    layer.close(index);
  });
});
```

## 文件上传

### 单文件上传

```javascript
admin.req({
  type: 'post',
  url: layui.setter.baseUrl + '/api/upload',
  data: {
    file: fileObject
  },
  success: function(res){
    if(res.code == 0){
      layer.msg('上传成功');
      console.log('文件URL:', res.data.fileUrl);
    }
  }
});
```

### FormData 上传

```javascript
var formData = new FormData();
formData.append('file', $('#fileInput')[0].files[0]);

admin.req({
  type: 'post',
  url: layui.setter.baseUrl + '/api/upload',
  data: formData,
  contentType: false,
  processData: false,
  success: function(res){
    if(res.code == 0){
      layer.msg('上传成功');
    }
  }
});
```

## 数据导出

### 导出功能

```javascript
$('#exportBtn').on('click', function(){
  var queryParams = {
    createTimeStart: $('#createTimeStart').val(),
    createTimeEnd: $('#createTimeEnd').val(),
    status: $('#status').val()
  };

  admin.req({
    type: 'get',
    url: layui.setter.baseUrl + '/api/export',
    data: queryParams,
    success: function(res){
      if(res.code == 0){
        // 下载文件
        window.location.href = res.data.fileUrl;
        layer.msg('导出成功');
      }
    }
  });
});
```

## 数据统计

### 加载统计数据

```javascript
function loadStatistics(){
  admin.req({
    type: 'get',
    url: layui.setter.baseUrl + '/api/statistics',
    data: {
      createTimeStart: $('#createTimeStart').val(),
      createTimeEnd: $('#createTimeEnd').val()
    },
    success: function(res){
      if(res.code == 0){
        $('#totalCount').html(res.data.totalCount);
        $('#totalAmount').html('￥' + res.data.totalAmount);
        $('#successRate').html(res.data.successRate + '%');
      }
    }
  });
}

// 页面加载时获取
loadStatistics();

// 搜索时重新获取
$('#searchBtn').on('click', function(){
  loadStatistics();
});
```

## 错误处理最佳实践

### 统一错误处理

```javascript
function apiRequest(url, data, successCallback, errorCallback){
  admin.req({
    type: 'post',
    url: layui.setter.baseUrl + url,
    data: data,
    success: function(res){
      if(res.code == 0){
        successCallback && successCallback(res.data);
      } else if(res.code == 401){
        layer.alert('登录已过期，请重新登录', {icon: 2}, function(){
          location.href = layui.setter.baseLocal + 'user/login';
        });
      } else if(res.code == 403){
        layer.msg('没有操作权限', {icon: 2});
        errorCallback && errorCallback(res);
      } else {
        layer.msg(res.msg || '操作失败', {icon: 2});
        errorCallback && errorCallback(res);
      }
    },
    error: function(xhr){
      if(xhr.status == 0){
        layer.msg('网络连接失败', {icon: 2});
      } else if(xhr.status == 500){
        layer.msg('服务器错误', {icon: 2});
      } else {
        layer.msg('请求失败', {icon: 2});
      }
      errorCallback && errorCallback(xhr);
    }
  });
}

// 使用示例
apiRequest('/api/save', formData, function(data){
  layer.msg('保存成功');
  table.reload('dataTable');
}, function(err){
  console.error('保存失败:', err);
});
```

## 完整 CRUD 示例

```javascript
layui.use(['admin', 'table', 'form'], function(){
  var admin = layui.admin;
  var table = layui.table;
  var form = layui.form;

  // CREATE - 新增
  function createData(formData){
    admin.req({
      type: 'post',
      url: layui.setter.baseUrl + '/api/create',
      data: formData,
      success: function(res){
        if(res.code == 0){
          layer.msg('新增成功');
          table.reload('dataTable');
        }
      }
    });
  }

  // READ - 获取列表
  table.render({
    elem: '#dataTable',
    url: layui.setter.baseUrl + '/api/list',
    page: true,
    cols: [[
      {field: 'id', title: 'ID'},
      {field: 'name', title: '名称'}
    ]]
  });

  // READ - 获取详情
  function getDetail(id){
    admin.req({
      type: 'get',
      url: layui.setter.baseUrl + '/api/detail',
      data: {id: id},
      success: function(res){
        if(res.code == 0){
          form.val('detailForm', res.data);
        }
      }
    });
  }

  // UPDATE - 更新
  function updateData(formData){
    admin.req({
      type: 'post',
      url: layui.setter.baseUrl + '/api/update',
      data: formData,
      success: function(res){
        if(res.code == 0){
          layer.msg('更新成功');
          table.reload('dataTable');
        }
      }
    });
  }

  // DELETE - 删除
  function deleteData(id){
    layer.confirm('确定删除？', function(index){
      admin.req({
        type: 'post',
        url: layui.setter.baseUrl + '/api/delete',
        data: {id: id},
        success: function(res){
          if(res.code == 0){
            layer.msg('删除成功');
            layer.close(index);
            table.reload('dataTable');
          }
        }
      });
    });
  }
});
```

## 注意事项

1. **请求地址**: 始终使用 `layui.setter.baseUrl + '/api/path'` 的方式
2. **Token 管理**: access_token 会自动添加到请求参数中
3. **错误处理**: 始终检查 `res.code` 并处理错误情况
4. **loading 状态**: admin.req 会自动显示/隐藏 loading
5. **超时设置**: 对于耗时操作，设置合适的 timeout
6. **数据格式**: 确保服务端返回符合 LayuiAdmin 的数据格式

## 相关文档

- [05-table-module.md](./05-table-module.md) - 表格模块详解
- [04-form-module.md](./04-form-module.md) - 表单模块详解
- [10-api-reference.md](./10-api-reference.md) - API 速查手册
