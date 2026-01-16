# Layui 表单模块详解

## 基础表单结构

```html
<form class="layui-form" action="">
  <div class="layui-form-item">
    <label class="layui-form-label">标题</label>
    <div class="layui-input-block">
      <input type="text" name="title" required placeholder="请输入标题"
             autocomplete="off" class="layui-input">
    </div>
  </div>

  <div class="layui-form-item">
    <div class="layui-input-block">
      <button class="layui-btn" lay-submit lay-filter="formDemo">立即提交</button>
      <button type="reset" class="layui-btn layui-btn-primary">重置</button>
    </div>
  </div>
</form>

<script>
layui.use('form', function(){
  var form = layui.form;

  // 监听提交
  form.on('submit(formDemo)', function(data){
    console.log(data.field);
    return false; // 阻止表单跳转
  });
});
</script>
```

## 表单组件类型

### 1. 输入框

```html
<div class="layui-form-item">
  <label class="layui-form-label">输入框</label>
  <div class="layui-input-inline">
    <input type="text" name="username" placeholder="请输入"
           autocomplete="off" class="layui-input">
  </div>
</div>
```

### 2. 下拉选择框

```html
<div class="layui-form-item">
  <label class="layui-form-label">选择框</label>
  <div class="layui-input-block">
    <select name="city" lay-verify="required">
      <option value="">请选择</option>
      <option value="北京">北京</option>
      <option value="上海">上海</option>
      <option value="广州">广州</option>
      <option value="深圳">深圳</option>
    </select>
  </div>
</div>
```

### 3. 分组选择框

```html
<select name="quiz">
  <option value="">请选择</option>
  <optgroup label="城市记忆">
    <option value="你工作的第一个城市">你工作的第一个城市？</option>
  </optgroup>
  <optgroup label="学生时代">
    <option value="你的工号">你的工号？</option>
    <option value="你最喜欢的老师">你最喜欢的老师？</option>
  </optgroup>
</select>
```

### 4. 复选框

```html
<!-- 默认复选框 -->
<div class="layui-form-item">
  <label class="layui-form-label">复选框</label>
  <div class="layui-input-block">
    <input type="checkbox" name="like[read]" title="阅读">
    <input type="checkbox" name="like[game]" title="游戏">
    <input type="checkbox" name="like[sleep]" title="睡觉">
  </div>
</div>

<!-- 原始风格复选框 -->
<input type="checkbox" name="" title="写作" lay-skin="primary">
```

### 5. 开关

```html
<div class="layui-form-item">
  <label class="layui-form-label">开关</label>
  <div class="layui-input-block">
    <input type="checkbox" name="switch" lay-skin="switch" lay-text="ON|OFF">
    <input type="checkbox" name="switch" lay-skin="switch" lay-text="开启|关闭">
    <input type="checkbox" name="switch" disabled lay-skin="switch">
  </div>
</div>
```

### 6. 单选框

```html
<div class="layui-form-item">
  <label class="layui-form-label">单选框</label>
  <div class="layui-input-block">
    <input type="radio" name="sex" value="男" title="男">
    <input type="radio" name="sex" value="女" title="女" checked>
    <input type="radio" name="sex" value="禁" title="禁用" disabled>
  </div>
</div>

<!-- 点选风格 -->
<input type="radio" name="a" title="男" lay-skin="primary">
```

### 7. 文本域

```html
<div class="layui-form-item layui-form-text">
  <label class="layui-form-label">文本域</label>
  <div class="layui-input-block">
    <textarea name="desc" placeholder="请输入内容" class="layui-textarea"></textarea>
  </div>
</div>
```

### 8. 行内表单

```html
<form class="layui-form" action="">
  <div class="layui-form-item">
    <div class="layui-inline">
      <label class="layui-form-label">范围</label>
      <div class="layui-input-inline" style="width: 100px;">
        <input type="text" name="price_min" placeholder="￥" autocomplete="off" class="layui-input">
      </div>
      <div class="layui-form-mid">-</div>
      <div class="layui-input-inline" style="width: 100px;">
        <input type="text" name="price_max" placeholder="￥" autocomplete="off" class="layui-input">
      </div>
  </div>
</form>
```

## 表单验证

### 内置验证规则

| 规则 | 说明 |
|------|------|
| required | 必填项 |
| phone | 手机号 |
| email | 邮箱 |
| url | 网址 |
| number | 数字 |
| date | 日期 |
| identity | 身份证 |

### 使用验证

```html
<input type="text" name="username" lay-verify="required" placeholder="请输入">
<input type="text" name="email" lay-verify="email" placeholder="请输入邮箱">
<input type="text" name="phone" lay-verify="phone" placeholder="请输入手机号">

<!-- 多个验证规则 -->
<input type="text" name="username" lay-verify="required|phone" placeholder="请输入">
```

### 自定义验证规则

```javascript
layui.use('form', function(){
  var form = layui.form;

  form.verify({
    username: function(value, item){
      if(!new RegExp("^[a-zA-Z0-9_\u4e00-\u9fa5\\s·]+$").test(value)){
        return '用户名不能有特殊字符';
      }
      if(/(^\_)|(\__)|(\_+$)/.test(value)){
        return '用户名首尾不能出现下划线';
      }
    }
    ,pass: [
      /^[\S]{6,12}$/,
      '密码必须6到12位，且不能出现空格'
    ]
    ,repass: function(value){
      if(value !== $('#LAY_password').val()){
        return '两次密码不一致';
      }
    }
  });
});
```

## 表单事件

### form.on()

监听表单事件：

```javascript
layui.use('form', function(){
  var form = layui.form;

  // 监听 select
  form.on('select(filter)', function(data){
    console.log(data.elem); // 得到 select 原始 DOM 对象
    console.log(data.value); // 得到被选中的值
    console.log(data.othis); // 得到美化后的 DOM 对象
  });

  // 监听 checkbox
  form.on('checkbox(filter)', function(data){
    console.log(data.elem); // checkbox 的 DOM 对象
    console.log(data.elem.checked); // 是否选中
  });

  // 监听 switch
  form.on('switch(filter)', function(data){
    console.log(data.elem); // switch 的 DOM 对象
    console.log(data.elem.checked); // 开关状态
  });

  // 监听 radio
  form.on('radio(filter)', function(data){
    console.log(data.elem); // radio 的 DOM 对象
    console.log(data.value); // 被选中的值
  });

  // 监听 submit
  form.on('submit(filter)', function(data){
    console.log(data.elem); // 被 select 元素
    console.log(data.form); // 获得 form 所在的 DOM 对象
    console.log(data.field); // 获得全部表单字段，名值对形式
    return false; // 阻止表单跳转
  });
});
```

## 表单方法

### form.render()

重新渲染表单：

```javascript
form.render(); // 更新全部
form.render('select'); // 更新 select
form.render('checkbox'); // 更新 checkbox
form.render('radio'); // 更新 radio
```

**注意**：当动态添加表单元素时，需要重新渲染。

### form.val()

给表单赋值：

```html
<form class="layui-form" lay-filter="test">
  <input type="text" name="username">
  <input type="checkbox" name="sex" value="男" title="男">
  <input type="checkbox" name="sex" value="女" title="女">
</form>

<script>
layui.use('form', function(){
  var form = layui.form;

  form.val('test', {
    "username": "贤心"
    ,"sex": "女"
  });
});
</script>
```

### form.verify()

设置验证规则，见自定义验证规则部分。

## 完整表单示例

```html
<form class="layui-form" action="">
  <div class="layui-form-item">
    <label class="layui-form-label">用户名</label>
    <div class="layui-input-block">
      <input type="text" name="username" required lay-verify="required"
             placeholder="请输入用户名" autocomplete="off" class="layui-input">
    </div>
  </div>

  <div class="layui-form-item">
    <label class="layui-form-label">密码</label>
    <div class="layui-input-block">
      <input type="password" name="password" required lay-verify="required"
             placeholder="请输入密码" autocomplete="off" class="layui-input">
    </div>
  </div>

  <div class="layui-form-item">
    <label class="layui-form-label">性别</label>
    <div class="layui-input-block">
      <input type="radio" name="sex" value="男" title="男">
      <input type="radio" name="sex" value="女" title="女">
    </div>
  </div>

  <div class="layui-form-item">
    <label class="layui-form-label">爱好</label>
    <div class="layui-input-block">
      <input type="checkbox" name="like" title="写作">
      <input type="checkbox" name="like" title="阅读">
      <input type="checkbox" name="like" title="游戏">
    </div>
  </div>

  <div class="layui-form-item">
    <label class="layui-form-label">城市</label>
    <div class="layui-input-block">
      <select name="city">
        <option value="">请选择</option>
        <option value="北京">北京</option>
        <option value="上海">上海</option>
      </select>
    </div>
  </div>

  <div class="layui-form-item">
    <label class="layui-form-label">开关</label>
    <div class="layui-input-block">
      <input type="checkbox" name="switch" lay-skin="switch">
    </div>
  </div>

  <div class="layui-form-item layui-form-text">
    <label class="layui-form-label">简介</label>
    <div class="layui-input-block">
      <textarea name="desc" class="layui-textarea"></textarea>
    </div>
  </div>

  <div class="layui-form-item">
    <div class="layui-input-block">
      <button class="layui-btn" lay-submit lay-filter="formDemo">立即提交</button>
      <button type="reset" class="layui-btn layui-btn-primary">重置</button>
    </div>
  </div>
</form>

<script>
layui.use('form', function(){
  var form = layui.form;
  form.render();
});
</script>
```

## 常见问题

### 1. 动态添加表单元素后不显示

解决：重新渲染表单
```javascript
$('#form').append('<select>...</select>');
form.render('select');
```

### 2. 获取表单值

```javascript
// 方法1: 通过 submit 事件
form.on('submit(filter)', function(data){
  console.log(data.field);
  return false;
});

// 方法2: 手动获取
var data = form.val('filter');
```

## 下一步

- 查看表格模块 → `05-table-module.md`
- 查看弹层模块 → `06-layer-module.md`
