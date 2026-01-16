-- V{major}.{minor}.{patch}__{description}.sql
-- PostgreSQL可重复执行迁移模板
-- 利用PostgreSQL的IF NOT EXISTS和DO块语法

-- =================================================================
-- 开始事务
-- =================================================================
BEGIN;

-- =================================================================
-- 函数: 动态索引创建（兼容旧版本PostgreSQL）
-- =================================================================
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
    SELECT EXISTS (
        SELECT 1 FROM pg_indexes
        WHERE schemaname = current_schema()
        AND tablename = p_table_name
        AND indexname = p_index_name
    ) INTO v_exists;

    IF NOT v_exists THEN
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

-- =================================================================
-- 函数: 动态列添加
-- =================================================================
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
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = current_schema()
        AND table_name = p_table_name
        AND column_name = p_column_name
    ) INTO v_exists;

    IF NOT v_exists THEN
        v_sql := 'ALTER TABLE ' || p_table_name || ' ADD COLUMN ' ||
                p_column_name || ' ' || p_column_type;

        IF NOT p_nullable THEN
            v_sql := v_sql || ' NOT NULL';
        END IF;

        IF p_default_value IS NOT NULL THEN
            v_sql := v_sql || ' DEFAULT ' || p_default_value;
        END IF;

        EXECUTE v_sql;

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

-- =================================================================
-- 执行迁移操作
-- =================================================================

-- 在此添加具体的迁移操作:

-- 示例1: 使用IF NOT EXISTS语法（PostgreSQL 9.5+推荐）
/*
-- 创建表
CREATE TABLE IF NOT EXISTS new_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_new_table_name ON new_table (name);
CREATE UNIQUE INDEX IF NOT EXISTS idx_new_table_name_unique ON new_table (name);

-- 添加列
ALTER TABLE existing_table
ADD COLUMN IF NOT EXISTS new_column VARCHAR(100) DEFAULT NULL;

-- 添加注释
COMMENT ON TABLE new_table IS '新表';
COMMENT ON COLUMN new_table.name IS '名称列';
*/

-- 示例2: 使用DO块处理复杂逻辑
/*
-- 添加外键约束
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_child_table_parent_id'
    ) THEN
        ALTER TABLE child_table
        ADD CONSTRAINT fk_child_table_parent_id
        FOREIGN KEY (parent_id) REFERENCES parent_table (id);
    END IF;
END$$;

-- 添加检查约束
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'chk_table_age_positive'
    ) THEN
        ALTER TABLE users
        ADD CONSTRAINT chk_table_age_positive
        CHECK (age >= 0);
    END IF;
END$$;
*/

-- 示例3: 使用函数方式（兼容旧版本）
/*
-- 创建索引
SELECT create_index_if_not_exists('table_name', 'idx_column_name', 'column_name', FALSE);
SELECT create_index_if_not_exists('table_name', 'idx_columns', 'column1, column2 DESC', TRUE);

-- 添加列
SELECT add_column_if_not_exists('table_name', 'new_column', 'VARCHAR(100)', 'NULL', TRUE, '新增列');
SELECT add_column_if_not_exists('table_name', 'required_column', 'INTEGER', '0', FALSE, '必需列');
*/

-- 示例4: 数据迁移（UPSERT）
/*
-- 使用ON CONFLICT进行幂等数据插入
INSERT INTO config_table (key, value, description)
VALUES
    ('feature_flag', 'enabled', 'Feature toggle status'),
    ('max_retries', '3', 'Maximum retry attempts')
ON CONFLICT (key)
DO UPDATE SET
    value = EXCLUDED.value,
    description = EXCLUDED.description,
    updated_at = CURRENT_TIMESTAMP;
*/

-- =================================================================
-- 提交事务
-- =================================================================
COMMIT;

-- =================================================================
-- 清理函数（可选）
-- =================================================================
-- 如果不想保留辅助函数，可以删除它们
/*
DROP FUNCTION IF EXISTS create_index_if_not_exists(TEXT, TEXT, TEXT, BOOLEAN);
DROP FUNCTION IF EXISTS add_column_if_not_exists(TEXT, TEXT, TEXT, TEXT, BOOLEAN, TEXT);
*/

-- =================================================================
-- 记录迁移完成
-- =================================================================
DO $$
BEGIN
    -- 创建迁移日志表（如果不存在）
    CREATE TABLE IF NOT EXISTS migration_log (
        id SERIAL PRIMARY KEY,
        migration_name VARCHAR(255) UNIQUE NOT NULL,
        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'SUCCESS',
        message TEXT
    );

    -- 记录迁移执行
    INSERT INTO migration_log (migration_name, status, message)
    VALUES ('V{major}.{minor}.{patch}__{description}', 'SUCCESS', 'Migration completed successfully')
    ON CONFLICT (migration_name) DO UPDATE SET
        executed_at = CURRENT_TIMESTAMP,
        status = EXCLUDED.status,
        message = EXCLUDED.message;
END$$;