# PostgreSQL 可重复执行SQL模式

本文档包含PostgreSQL数据库中实现可重复执行SQL的最佳实践和模式。

## 核心原则

### 1. 幂等性设计
PostgreSQL提供了更丰富的DDL语法，可以简化幂等性实现。

### 2. 利用系统目录
PostgreSQL的`pg_catalog`提供了完整的元数据查询能力。

## 索引管理模式

### IF NOT EXISTS 语法

PostgreSQL 9.5+支持`CREATE INDEX IF NOT EXISTS`：

```sql
-- 基础索引
CREATE INDEX IF NOT EXISTS idx_table_column ON table_name (column_name);

-- 唯一索引
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_table_column ON table_name (column_name);

-- 复合索引
CREATE INDEX IF NOT EXISTS idx_table_columns ON table_name (column1, column2 DESC);
```

### 函数模式（兼容旧版本）

```sql
CREATE OR REPLACE FUNCTION create_index_if_not_exists(
    p_table_name TEXT,
    p_index_name TEXT,
    p_columns TEXT,
    p_unique BOOLEAN DEFAULT FALSE
)
RETURNS TEXT AS $$
DECLARE
    v_exists BOOLEAN;
    v_sql TEXT;
BEGIN
    -- 检查索引是否存在
    SELECT EXISTS (
        SELECT 1 FROM pg_indexes
        WHERE schemaname = current_schema()
        AND tablename = p_table_name
        AND indexname = p_index_name
    ) INTO v_exists;

    IF NOT v_exists THEN
        -- 创建索引
        IF p_unique THEN
            v_sql := 'CREATE UNIQUE INDEX ' || p_index_name ||
                    ' ON ' || p_table_name || ' (' || p_columns || ')';
        ELSE
            v_sql := 'CREATE INDEX ' || p_index_name ||
                    ' ON ' || p_table_name || ' (' || p_columns || ')';
        END IF;

        EXECUTE v_sql;
        RETURN 'Index created: ' || p_index_name;
    ELSE
        RETURN 'Index already exists: ' || p_index_name;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## 列管理模式

### IF NOT EXISTS 语法

```sql
-- 添加列
ALTER TABLE table_name
ADD COLUMN IF NOT EXISTS new_column_name VARCHAR(100) DEFAULT 'default_value';

-- 添加带注释的列
ALTER TABLE table_name
ADD COLUMN IF NOT EXISTS new_column_name VARCHAR(100) DEFAULT NULL;

COMMENT ON COLUMN table_name.new_column_name IS '列的注释';
```

### 函数模式（增强版本）

```sql
CREATE OR REPLACE FUNCTION add_column_if_not_exists(
    p_table_name TEXT,
    p_column_name TEXT,
    p_column_type TEXT,
    p_default_value TEXT DEFAULT NULL,
    p_nullable BOOLEAN DEFAULT TRUE,
    p_comment TEXT DEFAULT NULL
)
RETURNS TEXT AS $$
DECLARE
    v_exists BOOLEAN;
    v_sql TEXT;
BEGIN
    -- 检查列是否存在
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = current_schema()
        AND table_name = p_table_name
        AND column_name = p_column_name
    ) INTO v_exists;

    IF NOT v_exists THEN
        -- 构建ALTER TABLE语句
        v_sql := 'ALTER TABLE ' || p_table_name || ' ADD COLUMN ' ||
                p_column_name || ' ' || p_column_type;

        -- 添加NULL/NOT NULL约束
        IF NOT p_nullable THEN
            v_sql := v_sql || ' NOT NULL';
        END IF;

        -- 添加默认值
        IF p_default_value IS NOT NULL THEN
            v_sql := v_sql || ' DEFAULT ' || p_default_value;
        END IF;

        EXECUTE v_sql;

        -- 添加注释
        IF p_comment IS NOT NULL THEN
            EXECUTE 'COMMENT ON COLUMN ' || p_table_name || '.' ||
                   p_column_name || ' IS ''' || p_comment || '''';
        END IF;

        RETURN 'Column added: ' || p_column_name;
    ELSE
        RETURN 'Column already exists: ' || p_column_name;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## 表管理模式

### IF NOT EXISTS 语法

```sql
-- 创建表
CREATE TABLE IF NOT EXISTS new_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建表的同时添加索引
CREATE TABLE IF NOT EXISTS new_table (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_new_table_user_id ON new_table (user_id);
CREATE INDEX IF NOT EXISTS idx_new_table_status ON new_table (status);
```

### 完整的表管理函数

```sql
CREATE OR REPLACE FUNCTION create_table_if_not_exists()
RETURNS TEXT AS $$
DECLARE
    v_table_exists BOOLEAN;
BEGIN
    -- 检查表是否存在
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = current_schema()
        AND table_name = 'target_table'
    ) INTO v_table_exists;

    IF NOT v_table_exists THEN
        EXECUTE '
        CREATE TABLE target_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255),
            status VARCHAR(20) DEFAULT ''active'',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )';

        -- 创建索引
        EXECUTE 'CREATE INDEX IF NOT EXISTS idx_target_table_email ON target_table (email)';
        EXECUTE 'CREATE INDEX IF NOT EXISTS idx_target_table_status ON target_table (status)';

        -- 添加注释
        EXECUTE 'COMMENT ON TABLE target_table IS ''目标表''';
        EXECUTE 'COMMENT ON COLUMN target_table.name IS ''姓名''';

        RETURN 'Table created: target_table';
    ELSE
        RETURN 'Table already exists: target_table';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## 约束管理模式

### 主键约束

```sql
-- 添加主键约束（如果不存在）
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'pk_table_name'
    ) THEN
        ALTER TABLE table_name ADD CONSTRAINT pk_table_name PRIMARY KEY (id);
    END IF;
END$$;
```

### 外键约束

```sql
-- 添加外键约束
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_child_parent'
    ) THEN
        ALTER TABLE child_table
        ADD CONSTRAINT fk_child_parent
        FOREIGN KEY (parent_id) REFERENCES parent_table (id);
    END IF;
END$$;
```

### 唯一约束

```sql
-- 添加唯一约束
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'uq_table_name_column'
    ) THEN
        ALTER TABLE table_name
        ADD CONSTRAINT uq_table_name_column UNIQUE (column_name);
    END IF;
END$$;
```

## 数据管理模式

### UPSERT操作（ON CONFLICT）

```sql
-- PostgreSQL 9.5+的UPSERT语法
INSERT INTO target_table (id, name, value)
VALUES (1, 'test', 100)
ON CONFLICT (id)
DO UPDATE SET
    name = EXCLUDED.name,
    value = EXCLUDED.value,
    updated_at = CURRENT_TIMESTAMP;

-- 复合唯一键的UPSERT
INSERT INTO user_roles (user_id, role_id, assigned_at)
VALUES (1, 2, CURRENT_TIMESTAMP)
ON CONFLICT (user_id, role_id)
DO NOTHING;

-- 有条件的UPSERT
INSERT INTO user_preferences (user_id, preference_key, preference_value)
VALUES (1, 'theme', 'dark')
ON CONFLICT (user_id, preference_key)
DO UPDATE SET
    preference_value = EXCLUDED.preference_value,
    updated_at = CURRENT_TIMESTAMP
WHERE user_preferences.active = true;
```

### 条件插入

```sql
-- 使用WHERE子句避免重复
INSERT INTO target_table (id, name, value)
SELECT 1, 'test', 100
WHERE NOT EXISTS (
    SELECT 1 FROM target_table WHERE id = 1
);
```

### 批量操作

```sql
-- 批量插入唯一数据
INSERT INTO target_table (id, name, value)
SELECT unnest(ARRAY[1, 2, 3]), unnest(ARRAY['a', 'b', 'c']), unnest(ARRAY[100, 200, 300])
ON CONFLICT (id) DO NOTHING;

-- 批量更新
UPDATE target_table t
SET value = s.new_value
FROM (VALUES
    (1, 150),
    (2, 250),
    (3, 350)
) AS s(id, new_value)
WHERE t.id = s.id;
```

## 函数和触发器模式

### 可重复执行的函数创建

```sql
-- 创建或替换函数
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 条件创建触发器
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'trigger_name'
    ) THEN
        CREATE TRIGGER trigger_name
        BEFORE UPDATE ON table_name
        FOR EACH ROW
        EXECUTE FUNCTION update_modified_column();
    END IF;
END$$;
```

## 视图管理模式

### 创建或替换视图

```sql
-- 创建或替换视图
CREATE OR REPLACE VIEW user_summary AS
SELECT
    u.id,
    u.name,
    u.email,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.amount), 0) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email;

-- 检查视图是否存在
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_views
        WHERE viewname = 'user_summary'
    ) THEN
        CREATE VIEW user_summary AS
        SELECT u.id, u.name, u.email
        FROM users u;
    END IF;
END$$;
```

## Flyway集成模式

### 完整的迁移脚本模板

```sql
-- V0.3.182__add_postgresql_features.sql

-- 开始事务
BEGIN;

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users (username);

-- 添加列
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS tracking_number VARCHAR(100);

-- 添加约束
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_orders_user_id'
    ) THEN
        ALTER TABLE orders
        ADD CONSTRAINT fk_orders_user_id
        FOREIGN KEY (user_id) REFERENCES users (id);
    END IF;
END$$;

-- 创建函数
CREATE OR REPLACE FUNCTION calculate_order_total(p_order_id INTEGER)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    v_total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(amount), 0)
    INTO v_total
    FROM order_items
    WHERE order_id = p_order_id;

    RETURN v_total;
END;
$$ LANGUAGE plpgsql;

-- 提交事务
COMMIT;

-- 记录迁移完成
DO $$
BEGIN
    INSERT INTO migration_log (migration_name, status, executed_at)
    VALUES ('V0.3.182__add_postgresql_features', 'SUCCESS', CURRENT_TIMESTAMP)
    ON CONFLICT (migration_name) DO NOTHING;
END$$;
```

## 性能优化模式

### 并发索引创建

```sql
-- 在生产环境中创建索引时避免锁定
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_large_table_column ON large_table (column_name);

-- 注意：CONCURRENTLY不能在事务中执行
```

### 分区表管理

```sql
-- 创建分区表（如果不存在）
CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- 创建分区（如果不存在）
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_tables
        WHERE tablename = 'events_2024_01'
    ) THEN
        CREATE TABLE events_2024_01
        PARTITION OF events
        FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
    END IF;
END$$;
```

## 调试和监控

### 迁移状态检查

```sql
-- 检查迁移对象
SELECT
    'table' as object_type,
    table_name as object_name,
    table_comment
FROM information_schema.tables
WHERE table_schema = current_schema()

UNION ALL

SELECT
    'index' as object_type,
    indexname as object_name,
    NULL as table_comment
FROM pg_indexes
WHERE schemaname = current_schema()

UNION ALL

SELECT
    'function' as object_type,
    routine_name as object_name,
    routine_comment
FROM information_schema.routines
WHERE routine_schema = current_schema();
```

### 性能监控

```sql
-- 检查索引使用情况
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- 检查表大小
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = current_schema()
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 最佳实践总结

1. **优先使用IF NOT EXISTS** - PostgreSQL 9.5+的内置语法更简洁
2. **利用ON CONFLICT** - 处理数据冲突的首选方式
3. **使用DO块** - 执行复杂条件逻辑
4. **考虑性能影响** - 大表操作使用CONCURRENTLY
5. **善用系统目录** - pg_catalog提供丰富的元数据
6. **事务管理** - 使用BEGIN/COMMIT确保原子性
7. **错误处理** - 使用EXCEPTION块捕获和处理错误