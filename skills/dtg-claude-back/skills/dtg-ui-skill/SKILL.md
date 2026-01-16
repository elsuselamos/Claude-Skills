---
name: dtg-ui-skill
description: This skill should be used when the user asks to "create enterprise admin page", "build data table with API", "design payment system UI", "implement reconciliation page", "add data statistics dashboard", "integrate admin.req API", "create CRUD operations", "add internationalization i18n", "implement multi-language support", "validate i18n json", "sync translation keys", or similar LayuiAdmin enterprise-level frontend development tasks. Provides enterprise-level code generation templates based on 716+ real project HTML files analysis, including API integration, permission control, data visualization, payment system patterns, complete i18n (internationalization) support, and i18n language file management tools.
version: 3.3.0
---

# dtg-ui-skill

企业级 LayuiAdmin 代码生成助手，基于 716+ 个实际支付系统项目分析。

## 快速路由

### 核心触发短语

| 触发短语 | 路由到 | 索引文件 |
|---------|--------|----------|
| "layui form", "form verification" | 表单模块 | references/INDEX.md#form |
| "build a table", "data table" | 表格模块 | references/INDEX.md#table |
| "laytpl template", "动态模版" | 模板引擎 | references/INDEX.md#laytpl |
| "i18n", "internationalization" | 国际化 | references/INDEX.md#i18n |
| "i18ndata attribute", "add i18n to page" | 国际化属性 | references/INDEX.md#i18n |
| "generate language files", "validate i18n json" | 语言文件管理 | assets/scripts/i18n_manager.py |
| "translateMessageByPath", "updateI18nfortable" | 国际化函数 | references/INDEX.md#i18n |
| "sync translation keys", "extract i18n from html" | 语言文件工具 | assets/scripts/i18n_manager.py |
| "create enterprise list page" | 企业页面 | assets/INDEX.md#enterprise |
| "admin.req API" | API集成 | references/INDEX.md#api |
| "echarts", "data visualization" | 数据可视化 | references/INDEX.md#echarts |
| "reconciliation page" | 对账管理 | references/INDEX.md#payment |

> 更多触发短语查看各 INDEX.md 文件

## 使用流程

1. **识别需求**：根据用户输入匹配触发短语
2. **定位文档**：从对应的 INDEX.md 获取精确文档路径
3. **按需加载**：读取所需的具体文档或模板
4. **生成代码**：基于文档内容生成代码

## 详细索引

| 类型 | 索引文件 | 说明 |
|------|----------|------|
| **文档** | references/INDEX.md | 27个参考文档的智能索引 |
| **模板** | assets/INDEX.md | 18个模板文件的智能索引 |
| **示例** | examples/INDEX.md | 7个示例目录的智能索引 |

## 快速开始

### 模块化方式（推荐）

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Layui 示例</title>
  <link rel="stylesheet" href="./layui/css/layui.css">
</head>
<body>
  <script src="./layui/layui.js"></script>
  <script>
  layui.use(['layer', 'form'], function(){
    var layer = layui.layer;
    var form = layui.form;
    layer.msg('Hello World');
  });
  </script>
</body>
</html>
```

### 非模块化方式

```html
<script src="./layui/layui.all.js"></script>
<script>
var layer = layui.layer;
layer.msg('Hello World');
</script>
```

## 核心能力

1. 快速生成页面结构
2. 表单组件生成（含验证规则）
3. 数据表格生成（含 CRUD）
4. 交互组件生成（弹层、日期选择器等）
5. LayuiAdmin 企业级支持
6. 动态模板引擎（Laytpl）
7. 国际化（i18n）完整支持

## 核心模块速查

| 模块 | 文档索引 |
|------|----------|
| layer | references/06-layer-module.md |
| form | references/04-form-module.md, references/27-form-verification.md |
| table | references/05-table-module.md |
| laytpl | references/26-laytpl-guide.md |
| laydate | references/09-other-components.md |
| upload | references/09-other-components.md |
| element | references/09-other-components.md |
| util | references/10-api-reference.md |

## 注意事项

1. 动态插入的表单元素需要重新渲染：`form.render()`
2. 表格数据格式：`{code: 0, msg: "", count: 100, data: []}`
3. 注意模块依赖关系（如 table 依赖 laytpl、laypage、layer、form）
