# dtg-ui-skill

> **企业级 LayuiAdmin 代码生成助手** - 基于 716+ 实际项目 HTML 文件分析

一个强大的 Claude Code 技能插件，专门用于快速生成企业级 LayuiAdmin 前端代码。本插件基于实际支付系统项目（xxpay-manage、xxpay-merchant、xxpay-agent）共 716+ 个 HTML 文件的代码模式分析，提供真实可靠的企业级开发模板和最佳实践。

## 版本信息

- **当前版本**: 3.0.0
- **Layui 版本**: 2.3.0
- **分析样本**: 716+ 个实际项目 HTML 文件
- **作者**: tommy

## 功能特性

### 企业级页面模板（基于实际项目）

#### 标准页面模板
- **企业级列表页面**: 导航、搜索、统计卡片、数据表格、批量操作
- **详情页面模板**: 只读表单展示、数据回显、操作按钮
- **编辑页面模板**: 表单验证、API 提交、错误处理
- **搜索表单模板**: 文本搜索、下拉筛选、日期范围选择

#### API 集成模板
- **标准 admin.req 模式**: GET/POST 请求、错误处理、loading 状态
- **CRUD 操作模板**: 完整的增删改查实现
- **批量操作模板**: 批量删除、批量更新、批量导出
- **数据统计模板**: 实时统计数据展示

#### 功能组件模板
- **数据统计卡片**: 多种样式的统计卡片组件
- **批量操作工具栏**: 标准的批量操作按钮组
- **权限控制模板**: 按钮级权限显示控制

### LayuiAdmin 企业级页面

#### 后台管理页面
- **订单管理页面**: 复杂搜索、数据统计、导出功能
- **配置管理页面**: 权限控制、状态切换、表单验证
- **对账管理页面**: 简洁布局、数据表格、差错处理
- **数据统计仪表板**: ECharts 图表、轮播组件、实时数据

### 完整的参考文档（25 个）

#### 标准 Layui 文档 (01-12)
- 快速入门、模块总览、布局系统
- 表单、表格、弹层、导航详解
- 数据组件、其他组件、API 速查
- 最佳实践、问题解答

#### LayuiAdmin 企业级文档 (13-17)
- LayuiAdmin 开发指南
- ECharts 集成指南
- 企业级表格开发
- 支付系统页面模式
- 工具函数库

#### 企业级开发文档 (18-25) **新增**
- **18-api-integration-guide.md**: API 集成完整指南
- **22-permission-system.md**: 权限控制系统
- **23-data-visualization.md**: 数据可视化组件
- **24-performance-optimization.md**: 性能优化建议
- **25-security-best-practices.md**: 安全最佳实践

## 使用方法

### 企业级页面模板触发短语

| 触发短语 | 功能模块 |
|----------|----------|
| "create enterprise list page", "admin list page" | 企业级列表页面 |
| "create detail page", "view page" | 详情页面模板 |
| "create edit page", "update form" | 编辑页面模板 |
| "data summary card", "statistics card" | 数据统计卡片 |
| "batch operation", "bulk action" | 批量操作工具栏 |
| "admin.req API", "API integration" | API 集成模板 |

### LayuiAdmin 企业级模块

| 触发短语 | 功能模块 |
|----------|----------|
| "create admin page", "layuiadmin page" | LayuiAdmin 后台页面 |
| "order management page", "order list", "trade page" | 订单管理页面 |
| "config management page", "payment config" | 配置管理页面 |
| "reconciliation page", "bill check page" | 对账管理页面 |
| "data dashboard", "statistics dashboard" | 数据统计仪表板 |
| "echarts chart", "data visualization" | ECharts 图表 |
| "permission control", "auth check" | 权限控制 |

## 目录结构

```
dtg-ui-skill/
├── .claude-plugin/
│   └── marketplace.json        # 插件配置 (v3.0.0)
├── skills/
│   └── dtg-ui-skill/
│       ├── SKILL.md            # 技能定义 (v3.0.0)
│       ├── assets/
│       │   └── templates/      # HTML 模板
│       │   ├── enterprise-list-page.html       # 企业级列表页面
│       │   ├── enterprise-detail-page.html     # 详情页面模板
│       │   ├── enterprise-edit-page.html       # 编辑页面模板
│       │   ├── enterprise-search-form.html     # 搜索表单模板
│       │   ├── api-integration-template.html   # API 集成模板
│       │   ├── data-summary-card.html          # 数据统计卡片
│       │   ├── batch-operation-toolbar.html    # 批量操作工具栏
│       │   ├── admin-layout.html               # LayuiAdmin 标准布局
│       │   ├── layui-admin-page.html           # 后台管理页面
│       │   ├── layui-order-page.html           # 订单管理页面
│       │   ├── layui-config-page.html          # 配置管理页面
│       │   ├── layui-reconciliation-page.html  # 对账管理页面
│       │   └── layui-dashboard.html            # 数据统计仪表板
│       ├── examples/
│       │   ├── admin-dashboard/                # 企业级仪表板示例
│       │   ├── order-management/               # 订单管理完整示例
│       │   └── payment-config/                 # 支付配置完整示例
│       └── references/         # API 参考文档 (25 个)
│           ├── 01-getting-started.md
│           ├── ...
│           ├── 17-utility-functions.md
│           ├── 18-api-integration-guide.md     # API 集成指南
│           ├── 22-permission-system.md         # 权限系统
│           ├── 23-data-visualization.md        # 数据可视化
│           ├── 24-performance-optimization.md  # 性能优化
│           └── 25-security-best-practices.md   # 安全最佳实践
└── README.md                   # 本文件
```

## 核心亮点

### 基于真实项目分析
- **716+ 个 HTML 文件**分析样本
- 涵盖管理后台、商户后台、代理商后台
- 来源于实际运行的支付系统项目

### 企业级代码模式
- **标准 admin.req API 调用**
- **统一的权限控制体系**
- **完整的数据统计展示**
- **规范的批量操作处理**

### 完整的文档体系
- **25 个参考文档**覆盖所有开发场景
- **API 集成指南**确保前后端协作顺畅
- **权限系统文档**实现精细化权限控制
- **性能优化指南**提升应用响应速度
- **安全最佳实践**保障系统安全

## 代码示例

### 企业级列表页面（简化版）

```html
<!-- 头部导航 -->
<div class="layui-card-header layui-card">
  <span class="layui-breadcrumb" lay-filter="breadcrumb">
    <a lay-href="">首页</a>
    <a><cite>订单管理</cite></a>
  </span>
</div>

<!-- 主要内容区 -->
<div class="layui-fluid">
  <div class="layui-card">
    <!-- 数据统计卡片 -->
    <div class="layui-row layui-col-space15">
      <div class="layui-col-md3">
        <div class="layui-card">
          <div class="layui-card-header">订单总数</div>
          <div class="layui-card-body" style="text-align:center;">
            <h2 id="totalCount">0</h2>
          </div>
        </div>
      </div>
      <!-- 更多统计卡片... -->
    </div>

    <!-- 搜索和操作区域 -->
    <div class="layui-row">
      <div class="layui-btn-group">
        <button class="layui-btn" id="addBtn">新增</button>
        <button class="layui-btn" id="batchDeleteBtn">批量删除</button>
      </div>
      <div class="layui-form" style="float:right;">
        <input type="text" id="keyword" placeholder="搜索" class="layui-input">
        <button id="search" class="layui-btn">搜索</button>
      </div>
    </div>

    <!-- 数据表格 -->
    <table id="dataTable" lay-filter="dataTable"></table>
  </div>
</div>

<script>
layui.use(['admin', 'table', 'form'], function(){
  var admin = layui.admin;
  var table = layui.table;

  // 表格渲染
  table.render({
    elem: '#dataTable',
    url: layui.setter.baseUrl + '/api/order/list',
    where: {
      access_token: layui.data(layui.setter.tableName).access_token
    },
    cols: [[
      {type: 'checkbox'},
      {field: 'id', title: 'ID'},
      {field: 'orderNo', title: '订单号'},
      {field: 'amount', title: '金额'},
      {field: 'status', title: '状态'},
      {fixed: 'right', title: '操作', toolbar: '#toolbar'}
    ]],
    page: true
  });

  // 搜索功能
  $('#search').on('click', function(){
    table.reload('dataTable', {
      where: {keyword: $('#keyword').val()}
    });
  });
});
</script>
```

### API 集成示例

```javascript
layui.use(['admin'], function(){
  var admin = layui.admin;

  // GET 请求
  admin.req({
    type: 'get',
    url: layui.setter.baseUrl + '/api/detail',
    data: {id: 123},
    success: function(res){
      if(res.code == 0){
        console.log(res.data);
      } else {
        layer.msg(res.msg);
      }
    }
  });

  // POST 请求
  admin.req({
    type: 'post',
    url: layui.setter.baseUrl + '/api/save',
    data: {name: '张三', age: 25},
    success: function(res){
      if(res.code == 0){
        layer.msg('保存成功');
      }
    }
  });
});
```

## 版本历史

### v3.0.0 (2025-12-28) **重大更新**
- **基于 716+ 实际项目分析**：来源于真实支付系统代码
- **新增 6 个企业级页面模板**：列表、详情、编辑、搜索、API集成、统计卡片
- **新增 5 个企业级参考文档**：API集成、权限、可视化、性能、安全
- **删除 4 个过时模板**：移除基础模板，专注企业级开发
- **升级现有模板**：基于实际项目最佳实践优化
- **版本号升级至 3.0.0**：表示重大功能更新

### v2.0.0
- 新增 LayuiAdmin 企业级支持
- 新增 ECharts 集成指南
- 新增企业级示例代码

### v1.0.0
- 初始版本
- 标准 Layui 2.3.0 支持

## 注意事项

1. **确保正确引入 Layui 的 CSS 和 JS 文件**
2. **数据接口返回格式需符合规范**: `{code: 0, msg: "", count: 100, data: []}`
3. **动态插入的表单元素需要重新渲染**: `form.render()`
4. **注意模块依赖关系**（如 table 依赖 laytpl、laypage、layer、form）
5. **LayuiAdmin 需要正确配置 config.js 和路由系统**
6. **admin.req 会自动携带 access_token**
7. **所有 API 请求应使用 admin.req 方法**
8. **前端权限仅用于 UI 控制，真正的权限验证必须在后端**

## 技术栈

- **前端框架**: Layui 2.3.0
- **后台模板**: LayuiAdmin
- **图表库**: ECharts
- **代码助手**: Claude Code

## 许可证

MIT License

---

**🤖 Generated with [Claude Code](https://claude.com/claude-code)**

*基于真实项目分析，提供企业级 LayuiAdmin 开发支持*
