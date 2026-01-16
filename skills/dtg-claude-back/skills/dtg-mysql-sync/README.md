# dtg-mysql-sync - MySQL 8 数据同步技能

用于同步 MySQL 8 数据库的表数据，从 Node 1（源）完整复制到 Node 2（目标）。

## 功能特性

- ✅ **自动数据清除**: 同步前自动清除目标表数据
- ✅ **批量复制**: 每批 1000 行，高效处理大数据量
- ✅ **事务安全**: 失败自动回滚，保证数据一致性
- ✅ **进度反馈**: 实时显示同步进度和统计信息
- ✅ **连接验证**: 先验证两个数据库连接后再执行
- ✅ **外键处理**: 自动禁用/启用外键检查

## 数据库配置

| 节点 | Host | Port | Database | User |
|------|------|------|----------|------|
| Node 1 (源) | 127.0.0.1 | 3307 | xxpay | dtgMysqlTest |
| Node 2 (目标) | 127.0.0.1 | 3306 | xxpay | root |

## 使用方式

```bash
# 基本用法
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name>

# 强制同步（跳过确认）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py --table <table_name> --force

# 自定义连接
python3 ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/mysql_sync.py \
  --table <table_name> \
  --source-host <host> --source-port <port> \
  --target-host <host> --target-port <port>
```

## 验证结果

### 基本功能测试

| 测试项 | 状态 | 说明 |
|--------|------|------|
| 目录结构 | ✅ | 所有必需文件已创建 |
| SKILL.md | ✅ | Frontmatter 格式正确，包含触发条件 |
| 脚本权限 | ✅ | 可执行权限已设置 |
| 依赖安装 | ✅ | pymysql 和 rich 已安装 |
| 数据库连接 | ✅ | 源和目标数据库都能连接 |
| 数据同步 | ✅ | 350 行数据成功同步 |

### 同步测试示例

```
MySQL 8 数据同步工具

✓ 源数据库连接成功 (127.0.0.1:3307/xxpay)
✓ 目标数据库连接成功 (127.0.0.1:3306/xxpay)
检测到 10 个列
源表数据: 350 行
清除 350 行旧数据
  复制数据 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

✓ 同步完成: 350 行
```

### 数据验证

```python
# 目标数据库验证结果
目标数据库 flyway_schema_history 表行数: 350
数据分布:
  success=1: 350 行
```

## Skill 触发条件

当用户输入以下内容时，skill 会自动触发：

- `dtg-mysql-sync <table_name>`
- `sync MySQL data`
- `copy MySQL table`
- `MySQL data replication`
- `database sync`

如果用户输入 `dtg-mysql-sync` 但没有提供表名，会询问用户要同步的表名。

## 目录结构

```
dtg-mysql-sync/
├── SKILL.md                              # 技能定义
├── README.md                             # 本文件
├── scripts/
│   ├── mysql_sync.py                     # 同步脚本
│   └── requirements.txt                  # Python 依赖
└── references/
    └── mysql-sync-best-practices.md      # 最佳实践文档
```

## 依赖

```bash
pip install pymysql rich
```

或安装 requirements.txt：

```bash
pip install -r ${CLAUDE_PLUGIN_ROOT}/skills/dtg-mysql-sync/scripts/requirements.txt
```

## 技术实现

- **Python 3**: 脚本语言
- **PyMySQL**: MySQL 数据库连接
- **Rich**: 美观的终端输出和进度条
- **批量插入**: 每批 1000 行，提高性能
- **事务管理**: 自动提交/回滚

## 错误处理

脚本包含完善的错误处理：

- 连接失败：明确的错误提示
- 表不存在：清晰的错误信息
- 数据类型不匹配：PyMySQL 自动处理
- 权限不足：详细的错误提示

## 相关文档

- [MySQL 同步最佳实践](references/mysql-sync-best-practices.md)
- [SKILL.md](SKILL.md) - 技能定义和触发条件

## 版本

- **版本**: 3.0.0
- **兼容**: MySQL 8.0+
- **Python**: 3.6+
