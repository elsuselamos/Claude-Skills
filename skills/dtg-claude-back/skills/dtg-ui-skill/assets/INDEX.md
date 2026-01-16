# Layui 模板索引

## 使用说明

本文档提供所有模板文件的智能索引，通过关键词快速定位所需模板。

## 快速路由表

### 企业级页面模板

| 触发关键词 | 模板文件 | 说明 |
|-----------|----------|------|
| create enterprise list page | enterprise-list-page.html | 标准列表页 |
| create enterprise list page + i18n | enterprise-list-page-with-i18n.html | 带国际化 |
| create detail page, view page | enterprise-detail-page.html | 详情页 |
| create edit page, update form | enterprise-edit-page.html | 编辑页 |
| enterprise search form | enterprise-search-form.html | 搜索表单 |
| batch operation, bulk action | batch-operation-toolbar.html | 批量操作 |
| data summary card, statistics card | data-summary-card.html | 统计卡片 |

**参考文档**：`references/15-enterprise-table.md`
**示例**：`examples/enterprise-order-management/`

### API 集成与动态模板

| 触发关键词 | 模板文件 | 说明 |
|-----------|----------|------|
| admin.req API, API integration | api-integration-template.html | API 集成 |
| dynamic select, dynamic dropdown | dynamic-select.html | 动态下拉框 |
| laytpl template, laytpl helpers | laytpl-helpers.html | 工具函数集合 |

**参考文档**：`references/18-api-integration-guide.md`, `references/26-laytpl-guide.md`

### 表单验证模板

| 触发关键词 | 模板文件 | 说明 |
|-----------|----------|------|
| form verification, form rules | form-verification.html | 验证规则集合 |

**参考文档**：`references/27-form-verification.md`
**示例**：`examples/form-verification/`

### 国际化模板

| 触发关键词 | 模板文件 | 说明 |
|-----------|----------|------|
| i18n page template | i18n-page-template.html | 国际化页面 |

**参考文档**：`references/26-i18n-guide.md`

### LayuiAdmin 模板

| 触发关键词 | 模板文件 | 说明 |
|-----------|----------|------|
| admin layout, backend layout | admin-layout.html | 后台布局 |
| layuiadmin page | layui-admin-page.html | 后台页面 |
| order management page, trade page | layui-order-page.html | 订单管理 |
| config management page, payment config | layui-config-page.html | 配置管理 |
| reconciliation page, bill check | layui-reconciliation-page.html | 对账管理 |
| data dashboard, statistics dashboard | layui-dashboard.html | 数据仪表板 |

**参考文档**：`references/13-layuiadmin-guide.md`
**示例**：`examples/admin-dashboard/`, `examples/order-management/`

## 完整模板列表

### 企业级模板（716+ 项目）

| 文件 | 用途 | 标签 |
|------|------|------|
| enterprise-list-page.html | 企业级列表页 | list, enterprise |
| enterprise-list-page-with-i18n.html | 带国际化的列表页 | list, i18n |
| enterprise-detail-page.html | 详情页模板 | detail, enterprise |
| enterprise-edit-page.html | 编辑页模板 | edit, enterprise |
| enterprise-search-form.html | 标准搜索表单 | search, form |
| api-integration-template.html | API 集成模板 | api, integration |
| data-summary-card.html | 数据统计卡片 | statistics, card |
| batch-operation-toolbar.html | 批量操作工具栏 | batch, toolbar |
| dynamic-select.html | 动态下拉选择器 | dynamic, select |
| laytpl-helpers.html | Laytpl 工具函数 | laytpl, helpers |
| form-verification.html | 表单验证规则 | form, verification |
| i18n-page-template.html | 国际化页面模板 | i18n, template |

### LayuiAdmin 模板

| 文件 | 用途 | 标签 |
|------|------|------|
| admin-layout.html | LayuiAdmin 标准布局 | layout, admin |
| layui-admin-page.html | 后台管理页面 | admin |
| layui-order-page.html | 订单管理页面 | order, trade |
| layui-config-page.html | 配置管理页面 | config, payment |
| layui-reconciliation-page.html | 对账管理页面 | reconciliation |
| layui-dashboard.html | 数据统计仪表板 | dashboard, echarts |

## 按标签查找

- **list**: enterprise-list-page, enterprise-list-page-with-i18n
- **form**: enterprise-edit-page, enterprise-search-form, form-verification
- **table**: enterprise-list-page
- **i18n**: enterprise-list-page-with-i18n, i18n-page-template
- **api**: api-integration-template, dynamic-select
- **laytpl**: laytpl-helpers
- **verification**: form-verification
- **dashboard**: layui-dashboard
- **order**: layui-order-page
- **config**: layui-config-page
