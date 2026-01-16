# 国际化 (i18n) 语言文件管理指南

## 版本更新

- **版本**: 3.2.0
- **更新日期**: 2025-12-29
- **更新内容**: 添加语言文件管理工具和完整的 i18n 工作流支持

---

## 📋 目录

1. [语言文件管理工具](#语言文件管理工具)
2. [语言文件结构规范](#语言文件结构规范)
3. [工作流程](#工作流程)
4. [最佳实践](#最佳实践)
5. [常见问题](#常见问题)

---

## 语言文件管理工具

### 📦 i18n_manager.py - 语言文件管理脚本

位置: `assets/scripts/i18n_manager.py`

#### 安装和准备

```bash
# 确保脚本有执行权限
chmod +x assets/scripts/i18n_manager.py

# 或使用 python3 直接运行
python3 assets/scripts/i18n_manager.py --help
```

#### 功能 1: validate - 验证语言文件一致性

检查所有语言文件的键是否一致，确保没有缺失或多余的翻译键。

```bash
# 验证语言文件
python3 i18n_manager.py validate --dir ./language

# 输出示例:
# 📦 模块: merchant.json
#   📌 zh: 156 个键（基准）
#   ✅ en: 156 个键（一致）
#   ⚠️  ja: 150 个键
#      缺少 6 个键:
#        - list.mch_view.accountInfo
#        - list.mch_view.requestFailed
```

#### 功能 2: generate - 生成语言文件模板

创建新的模块语言文件或添加新的翻译键。

```bash
# 生成新模块的完整语言文件
python3 i18n_manager.py generate \
  --module payment \
  --keys "page.title=支付管理" "button.search=查询" "table.orderNo=订单号"

# 为现有模块添加新键
python3 i18n_manager.py generate \
  --module merchant \
  --keys "list.mch_new.email=邮箱" "list.mch_new.phone=手机号"
```

#### 功能 3: sync - 同步翻译键

确保所有语言文件具有相同的键结构（以基准语言为准）。

```bash
# 同步所有语言文件（以 zh 为基准）
python3 i18n_manager.py sync --module merchant --base-lang zh

# 预览模式（不实际修改文件）
python3 i18n_manager.py sync --module merchant --base-lang zh --dry-run
```

#### 功能 4: extract - 从 HTML 提取翻译键

自动从 HTML 文件中提取 `i18ndata` 属性的翻译键。

```bash
# 从单个 HTML 文件提取
python3 i18n_manager.py extract --file merchant-list.html

# 从整个目录提取
python3 i18n_manager.py extract --dir ./views --pattern "*.html"

# 提取并生成语言文件
python3 i18n_manager.py extract --dir ./views --output language/zh/merchant.json
```

---

## 语言文件结构规范

### 目录结构

```
x_mgr/start/json/language/
├── en/                    # 英文翻译
│   ├── merchant.json     # 商户模块
│   ├── payment.json      # 支付模块
│   ├── common.json       # 通用翻译
│   ├── index.json        # 首页
│   ├── layout.json       # 布局
│   └── user.json         # 用户模块
├── zh/                    # 中文翻译
│   ├── merchant.json
│   ├── payment.json
│   ├── common.json
│   └── ...
└── ja/                    # 其他语言（如日语）
    ├── merchant.json
    └── ...
```

### JSON 格式规范

采用**嵌套结构**，支持点号分隔的路径访问：

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
      "merName": "商户名称"
    }
  },
  "button": {
    "save": "保存",
    "cancel": "取消",
    "delete": "删除"
  },
  "prompt": {
    "deleteConfirm": "确定要删除吗？",
    "saveSuccess": "保存成功"
  }
}
```

**访问方式**：`模块名:list.mch_view.basic` → "基本信息"

### 键命名规范

```
格式: 模块名:页面类型.功能.子功能.具体项
```

| 前缀 | 用途 | 示例 |
|------|------|------|
| `merchant` | 商户管理 | `merchant:list.mch_view.basic` |
| `payment` | 支付管理 | `payment:reconciliation.title` |
| `agent` | 代理商管理 | `agent:list.home` |
| `user` | 用户管理 | `user:login.username` |
| `common` | 通用翻译 | `common:prompt.success` |

---

## 工作流程

### 1. 开发新页面时的 i18n 工作流

```bash
# 步骤 1: 在 HTML 中添加 i18ndata 属性
# <label i18ndata="merchant:form.merName">商户名称</label>

# 步骤 2: 从 HTML 提取所有翻译键
python3 i18n_manager.py extract --file merchant-list.html --output language/zh/merchant.json

# 步骤 3: 编辑生成的 JSON 文件，完善翻译
# vim language/zh/merchant.json

# 步骤 4: 同步到其他语言
python3 i18n_manager.py sync --module merchant --base-lang zh

# 步骤 5: 验证所有语言文件一致性
python3 i18n_manager.py validate --dir ./language
```

### 2. 添加新的翻译键

```bash
# 方法 1: 使用 generate 命令添加
python3 i18n_manager.py generate \
  --module merchant \
  --keys "list.mch_new.newField=新字段"

# 方法 2: 手动编辑基准语言文件后同步
# 1. 编辑 language/zh/merchant.json 添加新键
# 2. 运行同步命令
python3 i18n_manager.py sync --module merchant --base-lang zh
```

### 3. 支持新语言

```bash
# 步骤 1: 创建新语言目录
mkdir -p language/ja

# 步骤 2: 同步现有语言文件结构（自动创建）
python3 i18n_manager.py sync --module merchant --base-lang zh

# 步骤 3: 翻译生成的文件（标记为 [TODO] 的项）
# vim language/ja/merchant.json
```

---

## 最佳实践

### 1. 始终提供默认值

```html
<!-- ✅ 推荐：提供默认值 -->
<label i18ndata="merchant:form.merName">商户名称</label>

<!-- ❌ 避免：缺少默认值 -->
<label i18ndata="merchant:form.merName"></label>
```

### 2. 使用嵌套结构组织键

```json
// ✅ 推荐：按功能分组
{
  "list": {
    "mch_view": {
      "basic": "基本信息",
      "account": "账户信息"
    },
    "mch_add": {
      "basic": "基本信息"
    }
  }
}

// ❌ 避免：扁平结构
{
  "list_mch_view_basic": "基本信息",
  "list_mch_view_account": "账户信息"
}
```

### 3. 复用 common 模块

```javascript
// ✅ 推荐：使用 common 模块存储通用翻译
translateMessageByPath("common:button.save", "保存")
translateMessageByPath("common:prompt.success", "成功")

// ❌ 避免：在每个模块重复定义
// merchant:button.save
// payment:button.save
// agent:button.save
```

### 4. 定期验证语言文件

```bash
# 在每次添加新翻译后运行验证
python3 i18n_manager.py validate --dir ./language
```

### 5. 使用版本控制

```bash
# 确保 .gitignore 包含
# language/*/node_modules/
# language/*/.DS_Store

# 提交前验证
pre-commit: python3 i18n_manager.py validate --dir ./language
```

---

## 常见问题

### Q1: 翻译不生效怎么办？

**检查清单**：
1. 是否调用了 `initializeI18n(['yourModule'])`？
2. 模块名是否正确？
3. 翻译键路径是否正确？
4. 是否在 DOM 更新后调用了 `updateI18nfortable()`？

```javascript
// 标准初始化流程
initializeI18n(['merchant', 'common']);
layui.use(['admin', 'table'], function() {
    table.render({
        // ...
        done: function() {
            setTimeout(updateI18nfortable, 100);
        }
    });
});
```

### Q2: 动态添加的元素没有翻译？

```javascript
// 动态添加元素后必须调用 updateI18nfortable()
$('#dynamicContent').html(
    '<label i18ndata="merchant:form.merName">商户名称</label>'
);
updateI18nfortable(); // 必须调用
```

### Q3: 表格标题如何翻译？

```javascript
// 在 cols 配置中使用 i18ndata 属性
cols: [[
    {field: 'id', title: '<span i18ndata="merchant:table.id">ID</span>'},
    {field: 'name', title: '<span i18ndata="merchant:table.name">名称</span>'}
]],
done: function() {
    setTimeout(updateI18nfortable, 100);
}
```

### Q4: 如何处理占位符国际化？

```javascript
// ❌ HTML 属性方式不支持
// <input i18n-placeholder="merchant:form.placeholder" />

// ✅ 使用 JavaScript 动态设置
$('#searchInput').attr('placeholder',
    translateMessageByPath("merchant:form.placeholder", "请输入商户名称")
);
```

---

## 触发短语

| 触发短语 | 功能 |
|----------|------|
| "validate i18n json" | 验证语言文件 |
| "generate language files" | 生成语言文件 |
| "sync translation keys" | 同步翻译键 |
| "extract i18n from html" | 从 HTML 提取翻译键 |
| "add i18n support" | 添加国际化支持 |
| "i18ndata attribute" | HTML 翻译属性 |
| "translateMessageByPath" | JS 翻译函数 |
| "updateI18nfortable" | 更新 i18ndata 元素 |

---

## 文档参考

- **完整指南**: `references/26-i18n-guide.md`
- **页面模板**: `assets/templates/i18n-page-template.html`
- **管理脚本**: `assets/scripts/i18n_manager.py`
