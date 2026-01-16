# 国际化 (i18n) 完整指南

## 概述

本系统基于 i18next 实现 LayuiAdmin 应用的多语言支持，支持中英文切换，可扩展到更多语言。

## 核心组件

### 1. 语言文件结构

```
x_mgr/start/json/language/
├── en/                    # 英文翻译
│   ├── merchant.json     # 商户模块
│   ├── common.json       # 通用翻译
│   ├── index.json        # 首页
│   ├── layout.json       # 布局
│   └── user.json         # 用户模块
└── zh/                    # 中文翻译
    ├── merchant.json
    ├── common.json
    ├── index.json
    ├── layout.json
    └── user.json
```

### 2. 语言文件格式

采用嵌套 JSON 结构，支持点号分隔的路径访问：

```json
{
  "list": {
    "home": "主页",
    "mch_view": {
      "basic": "基本信息",
      "merID": "商户ID",
      "requestFailed": "请求失败"
    }
  }
}
```

访问路径：`merchant:list.mch_view.basic` → "基本信息"

### 3. 核心函数

#### initializeI18n(modules)

初始化国际化系统，加载指定模块的语言包。

```javascript
// 在页面脚本开始处调用
initializeI18n(['merchant', 'index', 'layout', 'common']);
```

**参数：**
- `modules`: 字符串数组，指定要加载的模块名称

**示例：**
```javascript
<script>
    initializeI18n(['merchant', 'common']);
    layui.use(['admin', 'form'], function () {
        // 代码...
    });
</script>
```

#### translateMessageByPath(path, defaultMsg)

根据路径获取翻译文本，如果翻译不存在则返回默认文本。

```javascript
var title = translateMessageByPath("merchant:list.mch_view.basic", "基本信息");
```

**参数：**
- `path`: 翻译键路径（格式：`模块名:路径.到.键`）
- `defaultMsg`: 默认文本（当翻译不存在时使用）

**返回：**
- 翻译后的文本或默认文本

**使用场景：**
```javascript
// 在 layer 弹窗中使用
layer.alert(err.msg, {
    title: translateMessageByPath("merchant:list.mch_view.errorNotice", '错误提示')
});

// 在动态内容中使用
$('input[name="status"][value="1"]').attr('title',
    translateMessageByPath("merchant:list.mch_view.enable", "启用")
);
```

#### updateI18nfortable()

更新页面中所有带有 `i18ndata` 属性的元素的文本内容。

```javascript
// 在数据加载完成后调用
updateI18nfortable();
```

**说明：**
- 查找所有具有 `i18ndata` 属性的元素
- 使用属性值作为键获取翻译
- 更新元素的 `innerText`

**典型调用时机：**
```javascript
table.render({
    // ... 配置
    done: function(res, curr, count) {
        setTimeout(function(){
            updateI18nfortable();
            form.render();
        }, 100);
    }
});
```

## HTML 中的国际化

### 使用 i18ndata 属性

在 HTML 元素上添加 `i18ndata` 属性指定翻译键：

```html
<!-- 导航面包屑 -->
<div class="layui-breadcrumb">
    <a lay-href="" i18ndata="merchant:list.mch_view.home">主页</a>
    <a><cite i18ndata="merchant:list.mch_view.management">商户管理</cite></a>
</div>

<!-- 表单标签 -->
<label class="layui-form-label" i18ndata="merchant:list.mch_view.merID">商户ID</label>
<label class="layui-form-label" i18ndata="merchant:list.mch_view.merName">商户名称</label>

<!-- 按钮 -->
<a class="layui-btn" lay-href="merchant/list/" i18ndata="merchant:list.mch_view.return">返回</a>

<!-- 表格标题 -->
{
    field: 'balance',
    title: '<span i18ndata="merchant:list.mch_view.balance">商户余额</span>'
}

<!-- 选项卡 -->
<li class="layui-this" i18ndata="merchant:list.mch_view.basic">基本信息</li>

<!-- 下拉选项 -->
<option value="" i18ndata="merchant:list.all">全部</option>

<!-- ⚠️ 注意：占位符不能使用 HTML 属性，必须使用 JavaScript 动态设置 -->
<!-- ❌ 错误写法 -->
<input type="text" i18n-placeholder="merchant:list.placeholder" />

<!-- ✅ 正确写法 - 见下方 JavaScript 部分 -->
<input type="text" id="searchInput" />
```

### 属性说明

| 属性 | 用途 | 示例 |
|------|------|------|
| `i18ndata` | 元素文本内容的翻译键 | `<span i18ndata="merchant:list.title">标题</span>` |
| ~~`i18n-placeholder`~~ | ❌ 不支持，请使用 JavaScript 动态设置 | 见下方示例 |
| `data-i18n` | ❌ 错误属性，请使用 `i18ndata` | 不要使用 |

## JavaScript 中的国际化

### 弹窗提示

```javascript
// 错误提示
layer.alert(err.msg, {
    title: translateMessageByPath("merchant:list.mch_view.errorNotice", '错误提示')
});

// 成功提示
layer.msg(translateMessageByPath("common:prompt.success", "成功"));

// 确认对话框
layer.confirm(
    translateMessageByPath("merchant:list.mch_change.ensureAddAmount", "确定为商户增加金额"),
    {icon: 3, title: translateMessageByPath("common:prompt.warning", "提示")},
    function(index) {
        // 确认操作
    }
);
```

### 动态属性更新

```javascript
// 单选框标题更新
$('input[name="status"][value="1"]').attr('title',
    translateMessageByPath("merchant:list.mch_view.enable", "启用")
);
$('input[name="status"][value="0"]').attr('title',
    translateMessageByPath("merchant:list.mch_view.disable", "停止")
);

// 占位符更新
$('input[name="mchId"]').attr('placeholder',
    translateMessageByPath("merchant:list.mch_add.name", "输入商户名")
);
```

### API 错误处理

```javascript
admin.req({
    type: 'get',
    url: layui.setter.baseUrl + '/mch_info/get',
    data: {mchId: mchId},
    error: function (err) {
        layer.alert(err.msg, {
            title: translateMessageByPath("merchant:list.mch_view.requestFailed", '请求失败')
        })
    },
    success: function (res) {
        // 成功处理
    }
});
```

## 完整页面示例

```html
<div class="layui-card layadmin-header">
    <div class="layui-breadcrumb" lay-filter="breadcrumb">
        <a lay-href="" i18ndata="merchant:list.mch_view.home">主页</a>
        <a><cite i18ndata="merchant:list.mch_view.management">商户管理</cite></a>
        <a><cite i18ndata="merchant:list.mch_view.viewMer">查看商户</cite></a>
    </div>
</div>

<div class="layui-fluid">
    <div class="layui-card">
        <form class="layui-form layui-form-pane">
            <div class="layui-tab layui-tab-brief">
                <ul class="layui-tab-title">
                    <li class="layui-this" i18ndata="merchant:list.mch_view.basic">基本信息</li>
                </ul>
                <div class="layui-tab-content">
                    <div class="layui-form-item">
                        <label class="layui-form-label" i18ndata="merchant:list.mch_view.merID">商户ID</label>
                        <div class="layui-input-inline">
                            <input type="text" id="mchId" name="mchId" lay-verify="required"
                                   autocomplete="off" class="layui-input" disabled="disabled">
                        </div>
                        <label class="layui-form-label" i18ndata="merchant:list.mch_view.merName">商户名称</label>
                        <div class="layui-input-inline">
                            <input type="text" id="name" name="name" lay-verify="required"
                                   autocomplete="off" class="layui-input" disabled="disabled">
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>

<script>
    // 初始化国际化，加载需要的模块
    initializeI18n(['merchant', 'index', 'layout', 'common']);

    layui.use(['admin', 'form', 'table'], function () {
        var form = layui.form,
            $ = layui.$,
            admin = layui.admin,
            layer = layui.layer;

        var router = layui.router();
        var mchId = router.search.mchId;

        admin.req({
            type: 'get',
            url: layui.setter.baseUrl + '/mch_info/get',
            data: {mchId: mchId},
            error: function (err) {
                layer.alert(JSON.stringify(err.field), {
                    title: translateMessageByPath("merchant:list.mch_view.errorNotice", '错误提示')
                })
            },
            success: function (res) {
                if (res.code == 0) {
                    $('#mchId').val(res.data.mchInfo.mchId);
                    $('#name').val(res.data.mchInfo.name);

                    // 更新动态内容
                    setTimeout(function(){
                        $('input[name="status"][value="1"]').attr('title',
                            translateMessageByPath("merchant:list.mch_view.enable", "启用")
                        );
                        $('input[name="status"][value="0"]').attr('title',
                            translateMessageByPath("merchant:list.mch_view.disable", "停止")
                        );
                        updateI18nfortable();
                        form.render();
                    }, 100);
                }
            }
        });
    })
</script>
```

## 语言文件命名规范

### 模块命名

| 模块名 | 用途 | 示例键 |
|--------|------|--------|
| `merchant` | 商户管理 | `merchant:list.mch_view.basic` |
| `agent` | 代理商管理 | `agent:list.home` |
| `user` | 用户管理 | `user:login.username` |
| `common` | 通用翻译 | `common:prompt.success` |
| `index` | 首页 | `index:dashboard.title` |
| `layout` | 布局组件 | `layout:sidebar.menu` |
| `layui` | Layui 组件 | `layui:table.confirmDelete` |

### 键命名规范

```
模块名:页面类型.功能.子功能.具体项
```

示例：
- `merchant:list.mch_view.basic` - 商户模块：列表页：查看页：基本信息
- `merchant:list.mch_add.merName` - 商户模块：列表页：新增页：商户名称
- `common:prompt.requestFailed` - 通用：提示：请求失败

## 最佳实践

### 1. 模块加载

只加载当前页面需要的模块，避免不必要的资源加载：

```javascript
// 推荐：按需加载
initializeI18n(['merchant', 'common']);

// 避免：加载过多模块
initializeI18n(['merchant', 'agent', 'user', 'common', 'index', 'layout']);
```

### 2. 默认值

始终提供合理的默认值：

```javascript
// 推荐
translateMessageByPath("merchant:list.mch_view.basic", "基本信息")

// 避免：缺少默认值可能导致显示问题
translateMessageByPath("merchant:list.mch_view.basic")
```

### 3. 动态更新时机

确保在 DOM 更新后调用 `updateI18nfortable()`：

```javascript
// 表格渲染完成
table.render({
    // ...
    done: function(res, curr, count) {
        setTimeout(function(){
            updateI18nfortable();
        }, 100);
    }
});

// AJAX 请求完成
admin.req({
    // ...
    success: function(res) {
        // 更新 DOM
        setTimeout(function(){
            updateI18nfortable();
            form.render();
        }, 100);
    }
});
```

### 4. 翻译键组织

按页面和功能组织翻译键：

```json
{
  "list": {
    "home": "主页",
    "mch_view": {
      "basic": "基本信息",
      "merID": "商户ID",
      "accountInfo": "账户信息"
    },
    "mch_add": {
      "basic": "基本信息",
      "merName": "商户名称",
      "save": "保存"
    },
    "mch_edit": {
      "basic": "基本信息",
      "save": "保存"
    }
  }
}
```

### 5. 复用翻译

对于通用文本，使用 `common` 模块：

```javascript
// 通用提示
translateMessageByPath("common:prompt.success", "成功")
translateMessageByPath("common:prompt.error", "错误")
translateMessageByPath("common:prompt.warning", "警告")

// 通用操作
translateMessageByPath("common:button.save", "保存")
translateMessageByPath("common:button.cancel", "取消")
translateMessageByPath("common:button.confirm", "确认")
```

## 常见问题

### Q1: 翻译不生效

**原因：**
1. 忘记调用 `initializeI18n()`
2. 模块名不正确
3. 翻译键路径错误

**解决：**
```javascript
// 检查模块是否加载
initializeI18n(['merchant', 'common']);

// 检查翻译键路径是否正确
// merchant:list.mch_view.basic  (模块名:页面.功能.键)
```

### Q2: 动态添加的元素没有翻译

**解决：**
```javascript
// 动态添加元素后调用
$('#dynamicContent').html('<label i18ndata="merchant:list.mch_view.merID">商户ID</label>');
updateI18nfortable(); // 更新所有 i18ndata 元素
```

### Q3: 表格标题需要翻译

**解决：**
```javascript
table.render({
    cols: [[
        {field: 'mchId', title: '<span i18ndata="merchant:list.mch_view.merID">商户ID</span>'},
        {field: 'name', title: '<span i18ndata="merchant:list.mch_view.merName">商户名称</span>'}
    ]],
    done: function() {
        setTimeout(updateI18nfortable, 100);
    }
});
```

## 新语言添加步骤

1. 在 `x_mgr/start/json/language/` 下创建新语言目录（如 `ja/` 日语）

2. 复制现有语言文件并翻译：

```bash
mkdir -p x_mgr/start/json/language/ja
cp x_mgr/start/json/language/zh/*.json x_mgr/start/json/language/ja/
```

3. 翻译 JSON 文件内容

4. 确保语言切换功能支持新语言（通常在用户设置中）
