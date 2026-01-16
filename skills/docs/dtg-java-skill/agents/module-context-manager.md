# 模块上下文管理器代理

## 代理名称

`module-context-manager`

## 代理职责

模块上下文管理器负责检测当前工作目录所属模块、分析模块间依赖关系、管理模块上下文切换，并提供多模块项目的开发指导。

## 触发条件

当用户在 dtg-pay 多模块项目中工作时，自动触发此代理进行模块检测和上下文管理。

## 代理能力

### 1. 模块检测

自动检测当前工作目录所属的模块：

```
检测流程：
1. 获取当前工作目录
2. 向上遍历父目录，查找项目根目录（包含 pom.xml 和 CLAUDE.md）
3. 扫描项目根目录下的所有子目录，识别模块
4. 匹配当前工作目录到对应模块
5. 返回模块信息
```

### 2. 模块信息获取

提供每个模块的详细信息：

| 字段 | 说明 |
|------|------|
| name | 模块名称 |
| path | 模块路径 |
| type | 模块类型 (dubbo-provider, payment-core, admin-panel 等) |
| httpPort | HTTP 端口 |
| dubboPort | Dubbo 端口 |
| skill | 对应的开发技能 |
| hasClaudeMd | 是否有 CLAUDE.md 文件 |
| hasPomXml | 是否有 pom.xml 文件 |

### 3. 模块技能映射

根据模块类型自动应用对应的开发技能：

| 模块名称 | 模块类型 | 对应技能 |
|---------|---------|---------|
| xxpay-service | dubbo-provider | dubbo-provider-development |
| xxpay-pay | payment-core | dtg-payment-core-development |
| xxpay-manage | admin-panel | dtg-admin-panel-development |
| xxpay-agent | admin-panel | dtg-admin-panel-development |
| xxpay-merchant | admin-panel | dtg-admin-panel-development |
| xxpay-task | scheduled-task | scheduled-task-development |
| xxpay-consumer | message-consumer | message-consumer-development |
| rbgi | bank-gateway | bank-gateway-development |
| xxpay-core | common-module | dtg-common-module-development |

### 4. 依赖关系分析

分析模块间的依赖关系：

```
依赖关系：
1. 解析 pom.xml 文件
2. 提取 <dependencies> 中的模块依赖
3. 构建依赖树
4. 输出依赖关系图
```

## 代理输出格式

### 模块检测成功

```markdown
检测到 dtg-pay 多模块项目 (10 个子模块)

当前工作目录: /dtg-pay/xxpay-manage
模块类型: 运营管理平台接口
端口: 8193 (HTTP) / 28193 (Dubbo)
模块技能: dtg-admin-panel-development

已载入模块文档:
  ✓ /dtg-pay/xxpay-manage/CLAUDE.md (当前模块)

如需查看其他模块文档，请使用 /view-module <module-name>

准备就绪，可以开始开发。
```

### 模块列表

```markdown
dtg-pay 项目模块列表:

┌─────────────────────┬──────────┬───────────┬────────────────┐
│ 模块名称             │ HTTP端口 │ Dubbo端口 │ 模块类型        │
├─────────────────────┼──────────┼───────────┼────────────────┤
│ rbgi                │ 8195     │ -         │ 银行网关        │
│ xxpay-agent         │ 8192     │ 28192     │ 代理商系统      │
│ xxpay-consumer      │ 3120     │ 23120     │ 通知消费者      │
│ xxpay-core          │ -        │ -         │ 公共模块        │
│ xxpay-flyway        │ -        │ -         │ 数据库迁移      │
│ xxpay-manage        │ 8193     │ 28193     │ 运营平台        │
│ xxpay-merchant      │ 8191     │ 28191     │ 商户系统        │
│ xxpay-task          │ 8194     │ 28194     │ 定时任务        │
│ xxpay-pay           │ 3020     │ 23020     │ 支付核心        │
│ xxpay-service       │ 8190     │ 28190     │ Dubbo服务提供者  │
└─────────────────────┴──────────┴───────────┴────────────────┘

部署顺序: flyway → service → pay/task → manage/agent/merchant
```

## 代理配置

### 项目根目录模式

```json
{
  "projectRootPatterns": [
    "**/pom.xml",
    "**/CLAUDE.md"
  ],
  "modulePatterns": [
    "**/pom.xml",
    "**/CLAUDE.md"
  ],
  "autoDetectModule": true,
  "loadOnlyCurrentModule": true
}
```

### 模块定义

```json
{
  "modules": [
    {
      "name": "xxpay-service",
      "path": "xxpay-service",
      "type": "dubbo-provider",
      "httpPort": 8190,
      "dubboPort": 28190,
      "skill": "dubbo-provider-development",
      "description": "Dubbo 服务提供者"
    },
    {
      "name": "xxpay-pay",
      "path": "xxpay-pay",
      "type": "payment-core",
      "httpPort": 3020,
      "dubboPort": 23020,
      "skill": "dtg-payment-core-development",
      "description": "支付核心"
    }
  ]
}
```

## 代理工作流

### 初始检测

1. 用户在项目中发起请求
2. 代理检测当前工作目录
3. 匹配模块并载入对应的 CLAUDE.md
4. 应用对应的开发技能
5. 返回模块信息给用户

### 模块切换

1. 用户切换工作目录（cd 命令）
2. 代理检测到目录变化
3. 重新检测模块并切换上下文
4. 载入新模块的 CLAUDE.md
5. 应用新模块的开发技能

### 查看其他模块

1. 用户使用 `/view-module <module-name>` 命令
2. 代理读取指定模块的 CLAUDE.md
3. 显示模块信息给用户
4. 不切换当前工作模块上下文

## 使用示例

### 场景 1：首次进入项目

```
用户: cd /dtg-pay/xxpay-manage
用户: 添加一个新的订单查询接口

代理: [检测到模块切换]
当前模块: xxpay-manage (运营管理平台接口)
已载入: /dtg-pay/xxpay-manage/CLAUDE.md
应用技能: dtg-admin-panel-development

让我帮你添加订单查询接口...
```

### 场景 2：查看依赖模块

```
用户: /view-module xxpay-service

代理: xxpay-service 模块信息:

模块类型: Dubbo 服务提供者
端口: 8190 (HTTP) / 28190 (Dubbo)
主要职责: 数据库操作、业务逻辑封装

依赖关系:
  xxpay-manage → xxpay-service (Dubbo RPC 调用)

已载入: /dtg-pay/xxpay-service/CLAUDE.md
```

### 场景 3：列出所有模块

```
用户: 列出所有模块

代理: [输出模块列表表格]
```

## 相关技能

- dtg-multi-module-management - 多模块项目管理技能
- dubbo-provider-development - Dubbo 服务提供者开发
- dtg-payment-core-development - 支付核心开发
- dtg-admin-panel-development - 管理后台开发
- scheduled-task-development - 定时任务开发
- message-consumer-development - 消息消费者开发
- bank-gateway-development - 银行网关开发
- dtg-common-module-development - 公共模块开发
