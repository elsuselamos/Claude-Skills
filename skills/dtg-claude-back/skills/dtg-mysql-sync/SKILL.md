---
name: dtg-mysql-sync
description: Use when user enters "dtg-mysql-sync <table>" or asks to sync MySQL data, copy MySQL table, or replicate MySQL 8 database. Synchronizes MySQL 8 table data from source to target with time filtering, batch processing, retry mechanism, and auto-cleanup. Ask for table name if not provided.
version: 3.0.0
tags: ["mysql", "data-sync", "replication", "mysql-8", "database-operations", "xxpay"]
triggers:
  - "dtg-mysql-sync"
  - "mysql sync"
  - "sync mysql"
  - "copy mysql table"
  - "database sync"
  - "mysql replication"
---

# MySQL 8 数据同步 v2.0

用于同步 MySQL 8 数据库的表数据，从 Node 1（源）完整复制到 Node 2（目标）。

## 新功能（v2.0）

- **🚀 高性能分页**: 自动检测主键，使用游标分页代替 OFFSET，大幅提升大表同步速度
- **🔄 失败重试**: 失败批次自动重试，可配置重试次数和延迟
- **✅ 数据校验**: 同步后自动验证数据一致性
- **💾 断点续传**: 支持中断后继续同步（`--enable-resume`）
- **📊 详细输出**: `--verbose` 显示详细的同步过程信息

## 使用方式

```bash
# 基本用法（默认同步最近 10 天数据）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name>

# 预览模式（推荐先使用）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --dry-run

# 强制同步（跳过确认）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --force

# 同步指定天数的数据
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --days 7

# 同步全部数据
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --days 0

# 启用断点续传（大表推荐）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --enable-resume

# 失败重试 5 次
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --retry-times 5

# 详细输出模式
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --verbose

# 自定义连接
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py \
  --table <table_name> \
  --source-host <host> --source-port <port> \
  --target-host <host> --target-port <port>
```

## 数据库连接配置

| 节点 | Host | Port | Database | User |
|------|------|------|----------|------|
| Node 1 (源) | 127.0.0.1 | 3307 | xxpay | dtgMysqlTest |
| Node 2 (目标) | 127.0.0.1 | 3306 | xxpay | root |

## 功能特性

### 核心功能
- **时间过滤**: 默认同步最近 10 天数据（自动检测时间字段）
- **无事务模式**: 每批独立提交，避免大事务限制
- **容错处理**: 失败批次继续处理，显示详细错误
- **自动清除**: 同步前清除目标表数据
- **批量复制**: 每批 1000 行，适合大数据量

### v2.0 新增功能
- **高性能分页**: 自动检测主键，使用游标分页，避免 OFFSET 性能问题
- **失败重试**: 可配置重试次数和延迟，提高同步成功率
- **数据校验**: 同步后自动验证源表和目标表行数一致性
- **断点续传**: 保存同步进度，中断后可继续
- **进度反馈**: 实时显示同步进度和详细信息
- **详细报告**: 显示成功/失败批次详情，包含验证状态

## 参数说明

### 基础参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--table` | 必需 | 要同步的表名 |
| `--dry-run` | false | 预览模式，显示同步信息但不执行实际操作 |
| `--days` | 10 | 只同步最近 N 天的数据（0 = 全部） |
| `--force` | false | 跳过确认直接执行 |

### 高级参数（v2.0 新增）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--retry-times` | 3 | 失败批次重试次数 |
| `--retry-delay` | 1.0 | 重试延迟（秒） |
| `--no-verify` | false | 禁用数据校验 |
| `--enable-resume` | false | 启用断点续传 |
| `--verbose` | false | 显示详细输出 |

### 数据库连接参数（可选）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--source-host` | 127.0.0.1 | 源数据库主机 |
| `--source-port` | 3307 | 源数据库端口 |
| `--source-database` | xxpay | 源数据库名 |
| `--source-user` | dtgMysqlTest | 源数据库用户 |
| `--source-password` | *** | 源数据库密码 |
| `--target-host` | 127.0.0.1 | 目标数据库主机 |
| `--target-port` | 3306 | 目标数据库端口 |
| `--target-database` | xxpay | 目标数据库名 |
| `--target-user` | root | 目标数据库用户 |
| `--target-password` | *** | 目标数据库密码 |

## 使用示例

### 示例 1: 同步支付订单表最近 10 天数据
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table t_pay_order
```

### 示例 2: 启用断点续传同步大表
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py \
  --table t_pay_order \
  --enable-resume \
  --verbose
```

### 示例 3: 同步最近 30 天数据，失败重试 5 次
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py \
  --table t_pay_order \
  --days 30 \
  --retry-times 5 \
  --force
```

## 依赖

```bash
pip install pymysql rich
```

## 参考

详细说明见 `references/mysql-sync-best-practices.md`
