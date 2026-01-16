# Layui 文档索引

## 使用说明

本文档提供所有参考文档的智能索引，通过关键词快速定位所需文档。

## 快速路由表

### 表单模块 (Form)

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| layui form, form component | 04-form-module.md | 表单组件详解 |
| form verification, form.verify, 表单验证 | 27-form-verification.md | 表单验证规则 |
| custom verify rule, 验证规则, lay-verify | 27-form-verification.md | 自定义验证规则 |

**关联模板**：`assets/templates/form-verification.html`
**关联示例**：`examples/form-verification/`

### 表格模块 (Table)

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| build a table, data table, layui table | 05-table-module.md | 表格模块详解 |
| enterprise table, complex table | 15-enterprise-table.md | 企业级表格 |

**关联模板**：`assets/templates/enterprise-list-page.html`

### 模板引擎 (Laytpl)

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| laytpl template, dynamic template, 动态模版 | 26-laytpl-guide.md | Laytpl 模板引擎 |
| dynamic select, dynamic dropdown | 26-laytpl-guide.md | 动态下拉选择器 |

**关联模板**：`assets/templates/dynamic-select.html`, `assets/templates/laytpl-helpers.html`
**关联示例**：`examples/dynamic-template/`

### 国际化 (i18n)

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| i18n, internationalization, multi-language | 26-i18n-guide.md | 国际化完整指南 |
| i18ndata, translateMessageByPath | 26-i18n-guide.md | HTML 翻译属性 |
| language file, translation json | 26-i18n-guide.md | 语言文件配置 |
| validate i18n json, sync translation keys | i18n_manager.py | 语言文件管理工具 |
| extract i18n from html, generate language files | i18n_manager.py | 语言文件生成工具 |
| updateI18nfortable, initializeI18n | 26-i18n-guide.md | i18n 核心函数 |

**关联模板**：`assets/templates/i18n-page-template.html`, `assets/templates/enterprise-list-page-with-i18n.html`
**工具脚本**：`assets/scripts/i18n_manager.py`

### API 集成

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| admin.req API, API integration | 18-api-integration-guide.md | API 集成完整指南 |

**关联模板**：`assets/templates/api-integration-template.html`

### 数据可视化

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| echarts chart, data visualization | 14-echarts-integration.md | ECharts 集成 |
| data dashboard, statistics dashboard | 23-data-visualization.md | 数据可视化组件 |

**关联模板**：`assets/templates/layui-dashboard.html`

### 支付系统

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| payment system, 支付系统 | 16-payment-system-patterns.md | 支付系统页面模式 |
| reconciliation, 对账 | 相关文档参考 | 对账管理 |

### 权限控制

| 触发关键词 | 文档 | 说明 |
|-----------|------|------|
| permission control, auth check | 22-permission-system.md | 权限控制系统 |

## 完整文档列表

### 标准 Layui 文档

| ID | 文档 | 标签 |
|----|------|------|
| 01 | getting-started.md | 入门 |
| 02 | module-overview.md | 概览 |
| 03 | layout-system.md | 布局 |
| 04 | form-module.md | 表单 |
| 05 | table-module.md | 表格 |
| 06 | layer-module.md | 弹层 |
| 07 | navigation.md | 导航 |
| 08 | data-components.md | 数据组件 |
| 09 | other-components.md | 其他组件 |
| 10 | api-reference.md | API |
| 11 | best-practices.md | 最佳实践 |
| 12 | troubleshooting.md | 故障排查 |

### LayuiAdmin 企业级文档

| ID | 文档 | 标签 |
|----|------|------|
| 13 | layuiadmin-guide.md | LayuiAdmin |
| 14 | echarts-integration.md | ECharts |
| 15 | enterprise-table.md | 企业表格 |
| 16 | payment-system-patterns.md | 支付系统 |
| 17 | utility-functions.md | 工具函数 |
| 18 | api-integration-guide.md | API 集成 |
| 22 | permission-system.md | 权限 |
| 23 | data-visualization.md | 可视化 |
| 24 | performance-optimization.md | 性能 |
| 25 | security-best-practices.md | 安全 |
| 26-i18n | i18n-guide.md | 国际化 |
| 26-laytpl | laytpl-guide.md | 模板引擎 |
| 27 | form-verification.md | 表单验证 |

## 按标签查找

- **入门**: 01
- **表单**: 04, 27
- **表格**: 05, 15
- **国际化**: 26-i18n
- **API**: 18
- **可视化**: 14, 23
- **模板引擎**: 26-laytpl
- **支付**: 16
- **权限**: 22
