---
name: repeatable-sql
description: 可重复执行SQL技能生成器，专门用于创建幂等的数据库迁移脚本。支持MySQL和PostgreSQL，提供索引管理、表结构变更、数据操作的模板和工具。当需要编写可安全重复执行的SQL脚本、设计Flyway迁移、或确保数据库操作幂等性时使用。
---

# 可重复执行SQL技能

## 概述

此技能帮助创建可以安全多次执行的SQL脚本，确保数据库迁移的幂等性和可靠性。基于最新commit中的`Dynamic_Create_Index`存储过程模式，提供完整的可重复执行SQL解决方案。

## 快速开始

### 核心使用场景

1. **Flyway迁移脚本生成** - 创建符合Flyway规范的可重复执行迁移
2. **索引管理** - 智能检查并创建索引，避免重复创建错误
3. **表结构变更** - 安全地添加、修改列，检查存在性
4. **数据库版本控制** - 确保SQL脚本在多环境中可重复执行

### 选择数据库类型

```bash
# MySQL项目
python scripts/index_manager.py --database mysql

# PostgreSQL项目
python scripts/index_manager.py --database postgresql
```

## 核心功能

### 1. 索引管理器 (`scripts/index_manager.py`)

**功能**: 基于最新commit的Dynamic_Create_Index存储过程，生成可重复执行的索引创建脚本

**使用示例**:
```python
from scripts.index_manager import IndexSpec, ColumnSpec, RepeatableSQLGenerator

# 定义索引
indexes = [
    IndexSpec(
        table_name="deposit",
        index_name="idx_merchant_order_id",
        columns=[ColumnSpec("merchant_order_id")],
        index_type=IndexType.INDEX
    )
]

# 生成脚本
generator = RepeatableSQLGenerator("mysql")
script = generator.generate_full_script(indexes)
```

**生成内容**:
- MySQL: 完整的存储过程 + 调用语句
- PostgreSQL: 函数版本或IF NOT EXISTS语法

### 2. 表迁移器 (`scripts/table_migrator.py`)

**功能**: 生成表结构变更的幂等SQL脚本

**支持操作**:
- `ADD_COLUMN` - 智能添加列（检查存在性）
- `MODIFY_COLUMN` - 修改列定义
- `DROP_COLUMN` - 安全删除列

**使用示例**:
```python
# 基于commit中的NotifyUrl字段变更
alter_spec = TableAlterSpec(
    table_name="t_mch_agentpay_record",
    operation=AlterOperation.MODIFY_COLUMN,
    column_def=ColumnDefinition(
        name="NotifyUrl",
        data_type="varchar(256)",
        nullable=True,
        comment="通知地址"
    )
)
```

### 3. Flyway验证器 (`scripts/flyway_validator.py`)

**功能**: 验证Flyway迁移脚本的规范性和安全性

**验证项目**:
- ✅ 文件命名规范 (V{version}__description.sql)
- ⚠️ 幂等性保护检查
- ✅ 事务控制验证
- ℹ️ 回滚支持提示
- 🔴 性能风险识别

## 数据库特定模式

### MySQL模式

基于项目中的实际存储过程实现：

```sql
-- 核心存储过程
DELIMITER $$
CREATE PROCEDURE Dynamic_Create_Index(
    IN p_target_table VARCHAR(64),
    IN p_target_index_name VARCHAR(64),
    IN p_target_columns_with_sort TEXT,
    IN p_target_index_type VARCHAR(10)
)
BEGIN
    -- [完整的索引检查和创建逻辑]
END$$
DELIMITER ;

-- 使用方式
CALL Dynamic_Create_Index('table', 'index', 'columns', 'INDEX');
```

**关键特性**:
- 使用information_schema检查索引存在性
- 支持索引排序方向（ASC/DESC）
- 区分UNIQUE和普通索引
- 自动清理存储过程

### PostgreSQL模式

利用PostgreSQL高级语法：

```sql
-- 方法1: IF NOT EXISTS语法 (PostgreSQL 9.5+)
CREATE INDEX IF NOT EXISTS idx_name ON table_name (column1, column2 DESC);

-- 方法2: DO块复杂逻辑
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_name') THEN
        CREATE INDEX idx_name ON table_name (column1);
    END IF;
END$$;

-- 方法3: ON CONFLICT数据操作
INSERT INTO table (id, name) VALUES (1, 'test')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
```

## 模板使用

### MySQL迁移模板

**位置**: `assets/templates/mysql_migration_template.sql`

**使用步骤**:
1. 复制模板并重命名: `V1.0.0__add_indexes.sql`
2. 在"执行迁移操作"部分添加具体操作
3. 根据需要调整存储过程

**示例操作**:
```sql
-- 添加索引
CALL Dynamic_Create_Index('users', 'idx_email', 'email', 'INDEX');
CALL Dynamic_Create_Index('orders', 'idx_user_status', 'user_id, status DESC', 'UNIQUE');

-- 添加列
CALL Dynamic_Add_Column('products', 'description', 'TEXT NULL', '产品描述');
```

### PostgreSQL迁移模板

**位置**: `assets/templates/postgresql_migration_template.sql`

**特点**:
- 支持多种语法模式
- 内置迁移日志记录
- 自动清理辅助函数

## 参考文档

### [MySQL模式](references/mysql-patterns.md)
完整的MySQL可重复执行SQL模式，包括：
- 索引管理最佳实践
- 列操作模式
- Flyway集成方案
- 性能优化技巧

### [PostgreSQL模式](references/postgresql-patterns.md)
PostgreSQL特有的实现方式：
- IF NOT EXISTS语法使用
- DO块高级逻辑
- ON CONFLICT数据操作
- 并发索引创建

### [最佳实践](references/best-practices.md)
通用指导原则：
- 幂等性设计原理
- 事务管理策略
- 错误处理模式
- 安全考虑因素

## 典型工作流程

### 1. 设计迁移
1. 确定变更内容（索引、列、数据）
2. 选择合适的模式（存储过程 vs 内置语法）
3. 规划性能影响和执行顺序

### 2. 生成脚本
```bash
# 生成索引脚本
python scripts/index_manager.py

# 生成表变更脚本
python scripts/table_migrator.py

# 验证脚本规范
python scripts/flyway_validator.py path/to/migration.sql
```

### 3. 测试验证
```bash
# 在测试环境验证
python scripts/flyway_validator.py --directory migrations/

# 生成验证报告
python scripts/flyway_validator.py --directory migrations/ --report validation_report.md
```

### 4. 部署执行
1. 备份生产数据
2. 在低峰期执行
3. 监控执行状态
4. 验证结果

## 注意事项

### 性能考虑
- 大表索引创建使用`CONCURRENTLY` (PostgreSQL) 或 `ALGORITHM=INPLACE` (MySQL)
- 避免长事务锁定
- 考虑分批执行大数据量操作

### 安全提醒
- 遵循最小权限原则
- 避免硬编码敏感信息
- 充分测试回滚方案

### 兼容性
- MySQL 5.7+ / MariaDB 10.2+
- PostgreSQL 9.5+
- 支持Flyway、Liquibase等版本控制工具

## 资源说明

### scripts/
可执行的Python脚本，用于生成和验证可重复执行SQL：

**核心脚本**:
- `index_manager.py` - 基于Dynamic_Create_Index存储过程的索引管理器
- `table_migrator.py` - 表结构变更操作生成器
- `flyway_validator.py` - Flyway迁移脚本验证器

**使用方式**: 直接执行Python脚本生成SQL模板或验证现有迁移脚本

### references/
详细的参考文档和技术指南：

**核心文档**:
- `mysql-patterns.md` - MySQL数据库可重复执行SQL完整模式
- `postgresql-patterns.md` - PostgreSQL特定实现和高级语法
- `best-practices.md` - 通用最佳实践和安全考虑

**使用场景**: 在编写迁移脚本时参考具体的实现模式和注意事项

### assets/
可复用的SQL模板文件：

**模板文件**:
- `templates/mysql_migration_template.sql` - MySQL完整迁移模板
- `templates/postgresql_migration_template.sql` - PostgreSQL迁移模板

**使用方式**: 复制模板并根据具体需求修改，生成符合规范的迁移脚本
