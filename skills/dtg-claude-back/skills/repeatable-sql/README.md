# 可重复执行SQL技能

可重复执行SQL技能生成器，专门用于创建幂等的数据库迁移脚本。

## 支持的数据库

- MySQL 5.7+
- MariaDB 10.2+
- PostgreSQL 9.5+

## 核心功能

- **索引管理**：智能检查并创建索引，避免重复创建错误
- **表结构变更**：安全地添加、修改列，检查存在性
- **数据库版本控制**：确保SQL脚本在多环境中可重复执行
- **Flyway集成**：创建符合Flyway规范的可重复执行迁移

## 使用方法

在 Claude Code 中使用 `repeatable-sql:skills` 技能来生成可重复执行的SQL脚本。

## 快速开始

```bash
# MySQL项目
python scripts/index_manager.py --database mysql

# PostgreSQL项目
python scripts/index_manager.py --database postgresql
```

## 主要组件

- **index_manager.py** - 索引管理器
- **table_migrator.py** - 表迁移器
- **flyway_validator.py** - Flyway验证器

## 模板和参考

- MySQL迁移模板：`assets/templates/mysql_migration_template.sql`
- PostgreSQL迁移模板：`assets/templates/postgresql_migration_template.sql`
- 最佳实践指南：`references/best-practices.md`