# Layui 模块总览

## 模块分类

Layui 2.3.0 包含 17 个核心模块，可分为以下 8 大类：

### 1. 基础核心（2 个）

| 模块 | 说明 |
|------|------|
| jquery | jQuery 库，作为 Layui 的基础依赖 |
| util | 工具函数集合，包含固定块、倒计时等 |

### 2. UI 交互（1 个）

| 模块 | 说明 | 功能 |
|------|------|------|
| layer | 弹层组件 | alert、confirm、msg、tips、页面层、iframe 层、prompt |

### 3. 常用元素（1 个）

| 模块 | 说明 | 功能 |
|------|------|------|
| element | 常用元素操作 | 导航 nav、选项卡 tab、折叠面板 collapse、进度条 progress、徽章 badge、时间线 timeline |

### 4. 表单相关（2 个）

| 模块 | 说明 | 功能 |
|------|------|------|
| form | 表单组件 | 输入框、选择框、复选框、开关、表单验证、事件监听 |
| upload | 文件上传 | 拖拽上传、多文件上传、图片预览、进度显示 |

### 5. 数据展示（3 个）

| 模块 | 说明 | 功能 |
|------|------|------|
| table | 数据表格 | 静态表格、数据表格、分页、排序、筛选、工具栏、行操作 |
| carousel | 轮播图 | 自动播放、切换动画、指示器 |
| tree | 树形结构 | 基础树、复选树、拖拽排序、点击回调 |

### 6. 日期时间（1 个）

| 模块 | 说明 | 功能 |
|------|------|------|
| laydate | 日期选择器 | 年选择器、年月选择器、日期选择器、时间选择器、日期时间范围选择 |

### 7. 编辑器（1 个）

| 模块 | 说明 |
|------|------|
| layedit | 富文本编辑器，提供基本的文本编辑功能 |

### 8. 其他组件（6 个）

| 模块 | 说明 | 触发词 |
|------|------|--------|
| laypage | 分页组件 | pagination, pager |
| flow | 流加载（无限滚动） | flow, infinite scroll, lazy load |
| rate | 评分组件 | rate, star rating |
| code | 代码修饰器 | code, syntax highlight |
| laytpl | 模板引擎 | template |
| util | 工具集 | util, fixbar, countdown |

## 模块依赖关系图

```
                    ┌─────────┐
                    │  jquery │
                    └────┬────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │  util   │     │  layer  │     │ element │
   └────┬────┘     └────┬────┘     └────┬────┘
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │  flow   │     │  form   │     │  tree   │
   └─────────┘     └────┬────┘     └─────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │  upload │     │ layedit │     │  table  │
   └─────────┘     └─────────┘     └────┬────┘
                                        │
                         ┌──────────────┼──────────────┐
                         ▼              ▼              ▼
                    ┌─────────┐   ┌─────────┐   ┌─────────┐
                    │ laytpl  │   │ laypage │   │  layer  │
                    └─────────┘   └─────────┘   └─────────┘
```

## 模块加载方式

### layui.use() 加载模块

```javascript
// 加载单个模块
layui.use('layer', function(){
  var layer = layui.layer;
  layer.msg('Hello');
});

// 加载多个模块
layui.use(['layer', 'form', 'table'], function(){
  var layer = layui.layer;
  var form = layui.form;
  var table = layui.table;
});
```

### 模块全局对象

模块加载后，可以通过 `layui.模块名` 访问：

```javascript
layui.use(['layer', 'form'], function(){
  // 方法1: 直接使用
  layui.layer.msg('消息');

  // 方法2: 赋值给变量（推荐）
  var layer = layui.layer;
  layer.msg('消息');
});
```

## 扩展模块

### 自定义模块路径

如果使用扩展模块，需要配置模块路径：

```javascript
layui.config({
  base: '/js/modules/' // 扩展模块目录
}).extend({
  mod1: 'mod1'         // 模块别名: 模块文件名
});

layui.use('mod1', function(){
  // 使用扩展模块 mod1
});
```

### 定义自定义模块

```javascript
layui.define(['jquery'], function(exports){
  var $ = layui.jquery;

  var obj = {
    hello: function(){
      alert('Hello');
    }
  };

  exports('mod1', obj);
});

// 使用
layui.use('mod1', function(){
  var mod1 = layui.mod1;
  mod1.hello();
});
```

## 模块使用建议

### 1. 按需加载

```javascript
// 推荐：按需加载
layui.use(['layer', 'form'], function(){
  // 只加载需要的模块
});

// 避免：一次性加载所有模块
layui.use(['layer', 'form', 'table', 'laydate', 'upload', 'laypage'], function(){
  // 不推荐这样做
});
```

### 2. 模块加载顺序

Layui 会自动处理模块依赖关系，无需手动控制加载顺序：

```javascript
// table 依赖 laytpl, laypage, layer, form
// Layui 会自动加载这些依赖模块
layui.use('table', function(){
  var table = layui.table;
  // 可以安全使用 table
});
```

### 3. 回调函数执行时机

```javascript
layui.use(['layer', 'form'], function(){
  // 这里是模块加载完成后的回调
  // 所有模块都已加载完成，可以安全使用
});
```

## 下一步

- 学习布局系统 → `03-layout-system.md`
- 查看表单模块 → `04-form-module.md`
- 查看表格模块 → `05-table-module.md`
