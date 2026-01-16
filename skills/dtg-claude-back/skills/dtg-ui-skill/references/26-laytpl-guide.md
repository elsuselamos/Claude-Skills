# Layui Laytpl 模板引擎完整指南

## 概述

`laytpl` 是 Layui 的模板引擎，用于生成动态 HTML 内容。它采用简洁的模板语法，支持数据遍历、条件判断、自定义语法等功能。

## 基础语法

### 1. 输出变量

```javascript
// 模板
<script id="demo-tpl" type="text/html">
  <div>{{ d.title }}</div>
  <div>{{= d.content }}</div>
</script>

// 数据
var data = {
  title: 'Hello Laytpl',
  content: 'This is content'
};

// 渲染
laytpl($('#demo-tpl').html()).render(data, function(html){
  console.log(html);
});
```

**转义说明**：
- `{{ d.name }}` - 转义输出（防止 XSS）
- `{{= d.name }}` - 原样输出（不转义）

### 2. 条件判断

```html
<script type="text/html" id="if-tpl">
  {{# if(d.status === 1) { }}
    <span class="layui-badge layui-bg-green">启用</span>
  {{# } else if(d.status === 0) { }}
    <span class="layui-badge layui-bg-gray">禁用</span>
  {{# } else { }}
    <span class="layui-badge">未知</span>
  {{# } }}
</script>
```

### 3. 循环遍历

#### 遍历数组

```html
<script type="text/html" id="for-tpl">
  <select>
    <option value="">全部</option>
    {{# d.forEach(function(item, index) { }}
      <option value="{{= item.value }}">{{= item.text }}</option>
    {{# }); }}
  </select>
</script>
```

## 动态下拉选择器模板

### 标准模式（基于实际项目）

```html
<!-- 容器 -->
<div style="float: right;" id="currencyFilter-view" class="layui-form"></div>

<!-- 模板 -->
<script id="currencyFilter-tpl" type="text/html">
    <select id="currencyFilter" lay-search lay-filter="currencySelectChange"
            style="padding: 5px; border-radius: 4px; border: 1px solid #ddd; width: 120px;">
        <option value="">全部</option>
        {{# d.forEach(function(item, index) { }}
        <option value="{{= item }}" {{ item === 'PHP' ? 'selected' : '' }}>{{= item }}</option>
        {{# }); }}
    </select>
</script>

<!-- JavaScript -->
<script>
layui.use(['form', 'laytpl'], function () {
    var form = layui.form;
    var laytpl = layui.laytpl;

    const template = document.getElementById('currencyFilter-tpl').innerHTML;
    const target = document.getElementById('currencyFilter-view');
    const dataList = [];

    // 获取数据
    admin.req({
        type: 'get',
        url: layui.setter.baseUrl + '/config/common/getBalanceTypeList',
        success: function (res) {
            if (res.code === 0) {
                var data = res.data;
                Object.keys(data).forEach(key => {
                    dataList.push(data[key]);
                });

                // 渲染模板
                laytpl(template).render(dataList, function (html) {
                    target.innerHTML = html;
                    form.render(); // 重新渲染表单
                });
            }
        }
    });

    // 监听选择变化
    form.on('select(currencySelectChange)', function (data) {
        const currencyValue = data.value === "" ? null : data.value;
        table.reload("tableReload", {
            where: {
                currency: currencyValue
            }
        });
    });
});
</script>
```

## 常用模板片段

### 状态徽章渲染

```html
<script type="text/html" id="statusBadge-tpl">
  {{# if(d.status === 1) { }}
    <span class="layui-badge layui-bg-green">启用</span>
  {{# } else if(d.status === 0) { }}
    <span class="layui-badge layui-bg-gray">禁用</span>
  {{# } else if(d.status === 2) { }}
    <span class="layui-badge layui-bg-orange">审核中</span>
  {{# } else { }}
    <span class="layui-badge layui-bg-red">异常</span>
  {{# } }}
</script>

<!-- 使用 -->
<script>
var tplStatus = function (d) {
    return layui.laytpl($('#statusBadge-tpl').html()).render(d);
};

table.render({
    cols: [[
        { field: 'status', title: '状态', templet: tplStatus }
    ]]
});
</script>
```

### 费率显示模板

```html
<script type="text/html" id="rateDisplay-tpl">
  {{# if((d.rate == '' || d.rate == null) && (d.fee == '' || d.fee == null)) { }}
    <span>未设置</span>
  {{# } else { }}
    {{# if(d.rate == '' || d.rate == null) { }}
      <span style="color: blue">{{= d.fee }}/笔</span>
    {{# } else { }}
      <span style="color: blue">{{= d.rate }}%+{{= d.fee }}/笔</span>
    {{# } }}
  {{# } }}
</script>
```

### 操作按钮模板

```html
<script type="text/html" id="actionButtons-tpl">
  <div class="layui-btn-group">
    <a class="layui-btn layui-btn-xs" lay-event="edit">编辑</a>
    {{# if(d.status === 1) { }}
      <a class="layui-btn layui-btn-xs layui-btn-warm" lay-event="disable">禁用</a>
    {{# } else { }}
      <a class="layui-btn layui-btn-xs layui-btn-normal" lay-event="enable">启用</a>
    {{# } }}
  </div>
</script>
```

## 表格列模板与 Laytpl 结合

### 方式一：内联模板函数

```javascript
var tplStatus = function (d) {
    if (d.status == 0) {
        return '<span class="layui-badge layui-bg-gray">关闭</span>';
    } else if (d.status == 1) {
        return '<span class="layui-badge layui-bg-green">开启</span>';
    }
};

table.render({
    cols: [[
        { field: 'status', title: '状态', templet: tplStatus }
    ]]
});
```

### 方式二：使用 Laytpl 模板

```html
<script type="text/html" id="table-status-tpl">
  {{# if(d.status === 1) { }}
    <span class="layui-badge layui-bg-green">开启</span>
  {{# } else { }}
    <span class="layui-badge layui-bg-gray">关闭</span>
  {{# } }}
</script>

<script>
table.render({
    cols: [[
        {
            field: 'status',
            title: '状态',
            templet: function(d) {
                return layui.laytpl($('#table-status-tpl').html()).render(d);
            }
        }
    ]]
});
</script>
```

### 方式三：使用 script 模板 ID

```html
<script type="text/html" id="table-status-tpl">
  {{# if(d.status === 1) { }}
    <span class="layui-badge layui-bg-green">开启</span>
  {{# } else { }}
    <span class="layui-badge layui-bg-gray">关闭</span>
  {{# } }}
</script>

<script>
table.render({
    cols: [[
        { field: 'status', title: '状态', templet: '#table-status-tpl' }
    ]]
});
</script>
```

## 常见问题

### 1. 模板渲染后 Layui 组件不生效

**原因**：动态插入的元素需要重新渲染

**解决方案**：
```javascript
laytpl(template).render(data, function(html) {
    target.innerHTML = html;
    form.render();      // 重新渲染表单
    element.render();   // 重新渲染元素组件
});
```

### 2. 转义导致 HTML 标签显示为文本

**解决方案**：使用 `{{= }}` 而不是 `{{ }}`
```html
<!-- 错误：会转义 -->
<div>{{ d.html }}</div>

<!-- 正确：不转义 -->
<div>{{= d.html }}</div>
```

## 最佳实践

1. **模板分离**：将模板定义在 `<script type="text/html">` 标签中
2. **避免过深嵌套**：复杂逻辑拆分为多个小模板
3. **使用转义**：默认使用 `{{ }}` 防止 XSS 攻击
4. **缓存模板**：频繁使用的模板可以缓存编译后的结果
5. **错误处理**：对空值和异常情况进行判断

## 相关文档

- 表格模块 → `05-table-module.md`
- 表单模块 → `04-form-module.md`
- API 参考 → `10-api-reference.md`
