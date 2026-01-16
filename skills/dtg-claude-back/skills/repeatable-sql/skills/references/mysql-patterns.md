# MySQL 可重复执行SQL模式

本文档包含MySQL数据库中实现可重复执行SQL的最佳实践和模式。

## 核心原则

### 1. 幂等性 (Idempotency)
SQL脚本应该能够安全地多次执行而不产生错误或不一致状态。

### 2. 检查后执行 (Check-Then-Act)
在执行DDL操作前检查对象是否已存在。

## 索引管理模式

### 存储过程模式

基于最新commit中的`Dynamic_Create_Index`存储过程：

```sql
DELIMITER $$
CREATE PROCEDURE Dynamic_Create_Index(
    IN p_target_table VARCHAR(64),
    IN p_target_index_name VARCHAR(64),
    IN p_target_columns_with_sort TEXT,
    IN p_target_index_type VARCHAR(10) -- 'INDEX' or 'UNIQUE'
)
BEGIN
    -- 实现检查并创建索引的逻辑
END$$
DELIMITER ;
```

### 使用方式

```sql
-- 检查并创建索引
CALL Dynamic_Create_Index('table_name', 'index_name', 'column1, column2 DESC', 'INDEX');

-- 清理存储过程
DROP PROCEDURE IF EXISTS Dynamic_Create_Index;
```

## 列管理模式

### 添加列的存储过程

```sql
DELIMITER $$
CREATE PROCEDURE Dynamic_Add_Column(
    IN p_target_table VARCHAR(64),
    IN p_column_name VARCHAR(64),
    IN p_column_definition TEXT,
    IN p_column_comment VARCHAR(255)
)
BEGIN
    DECLARE v_column_exists INT DEFAULT 0;

    -- 检查列是否存在
    SELECT COUNT(*)
    INTO v_column_exists
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = p_target_table
    AND COLUMN_NAME = p_column_name;

    -- 执行添加操作
    IF v_column_exists = 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', p_target_table, ' ADD COLUMN ',
                         p_column_name, ' ', p_column_definition);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END$$
DELIMITER ;
```

## 表管理模式

### 检查表是否存在

```sql
-- 方法1: 使用SHOW TABLES
SET @table_exists = (SELECT COUNT(*)
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'target_table');

-- 方法2: 使用存储过程
DELIMITER $$
CREATE PROCEDURE CreateTableIfNotExists()
BEGIN
    DECLARE v_table_exists INT DEFAULT 0;

    SELECT COUNT(*) INTO v_table_exists
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'new_table';

    IF v_table_exists = 0 THEN
        -- 创建表的SQL语句
        CREATE TABLE new_table (
            id INT PRIMARY KEY AUTO_INCREMENT,
            -- 其他列定义
        );
    END IF;
END$$
DELIMITER ;
```

## 数据管理模式

### 条件插入

```sql
-- 方法1: 使用INSERT IGNORE
INSERT IGNORE INTO target_table (id, name, value)
VALUES (1, 'test', 100);

-- 方法2: 使用ON DUPLICATE KEY UPDATE
INSERT INTO target_table (id, name, value)
VALUES (1, 'test', 100)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    value = VALUES(value);

-- 方法3: 使用存储过程检查
DELIMITER $$
CREATE PROCEDURE SafeInsert(
    IN p_id INT,
    IN p_name VARCHAR(100),
    IN p_value INT
)
BEGIN
    DECLARE v_exists INT DEFAULT 0;

    SELECT COUNT(*) INTO v_exists
    FROM target_table
    WHERE id = p_id;

    IF v_exists = 0 THEN
        INSERT INTO target_table (id, name, value)
        VALUES (p_id, p_name, p_value);
    END IF;
END$$
DELIMITER ;
```

### 条件更新

```sql
-- 使用子查询避免更新不存在的行
UPDATE target_table
SET value = 200
WHERE id = 1
AND EXISTS (SELECT 1 FROM target_table WHERE id = 1);
```

## Flyway集成模式

### 版本化迁移命名

```
V{major}.{minor}.{patch}__description.sql
例如: V0.3.181__alter_table_index.sql
```

### 完整的迁移脚本模板

```sql
-- V0.3.182__add_indexes_and_columns.sql

-- 设置事务
SET autocommit = 0;

-- 创建索引管理存储过程
DELIMITER $$
[包含Dynamic_Create_Index存储过程定义]
DELIMITER ;

-- 创建列管理存储过程
DELIMITER $$
[包含Dynamic_Add_Column存储过程定义]
DELIMITER ;

-- 执行索引创建
CALL Dynamic_Create_Index('table1', 'idx_column1', 'column1', 'INDEX');
CALL Dynamic_Create_Index('table2', 'idx_columns', 'column1, column2 DESC', 'UNIQUE');

-- 执行列添加
CALL Dynamic_Add_Column('table3', 'new_column', 'VARCHAR(100) NULL', '新增列');

-- 提交事务
COMMIT;

-- 清理存储过程
DROP PROCEDURE IF EXISTS Dynamic_Create_Index;
DROP PROCEDURE IF EXISTS Dynamic_Add_Column;
```

## 错误处理模式

### 使用DECLARE CONTINUE HANDLER

```sql
DELIMITER $$
CREATE PROCEDURE SafeMigration()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    -- 存储过程逻辑
END$$
DELIMITER ;
```

### 使用条件语句

```sql
-- 安全的删除操作
SET @foreign_key_checks = @@foreign_key_checks;
SET foreign_key_checks = 0;

-- 执行可能违反外键约束的操作
DELETE FROM child_table WHERE condition;
DELETE FROM parent_table WHERE condition;

-- 恢复外键检查
SET foreign_key_checks = @foreign_key_checks;
```

## 性能考虑

### 大表操作

```sql
-- 分批更新
DELIMITER $$
CREATE PROCEDURE BatchUpdate()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE batch_id INT;
    DECLARE batch_cursor CURSOR FOR
        SELECT id FROM large_table WHERE status = 'pending' LIMIT 1000;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN batch_cursor;

    batch_loop: LOOP
        FETCH batch_cursor INTO batch_id;
        IF done THEN
            LEAVE batch_loop;
        END IF;

        UPDATE large_table
        SET status = 'processed', processed_time = NOW()
        WHERE id = batch_id;

        -- 提交每批数据
        COMMIT;
    END LOOP;

    CLOSE batch_cursor;
END$$
DELIMITER ;
```

### 索引创建优化

```sql
-- 对于大表，先禁用索引
ALTER TABLE large_table DISABLE KEYS;

-- 批量插入数据
INSERT INTO large_table SELECT * FROM source_table;

-- 重新启用索引
ALTER TABLE large_table ENABLE KEYS;
```

## 调试和监控

### 记录执行状态

```sql
-- 创建迁移日志表
CREATE TABLE IF NOT EXISTS migration_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    migration_name VARCHAR(255),
    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('SUCCESS', 'FAILED'),
    message TEXT
);

-- 在迁移脚本中记录状态
INSERT INTO migration_log (migration_name, status, message)
VALUES ('V0.3.182__add_indexes', 'SUCCESS', 'All operations completed');
```

### 检查迁移状态

```sql
-- 检查特定对象是否已创建
SELECT
    'Table' as object_type,
    table_name as object_name,
    create_time
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME LIKE 'pattern%'

UNION ALL

SELECT
    'Index' as object_type,
    index_name as object_name,
    NULL as create_time
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
AND INDEX_NAME LIKE 'idx_pattern%';
```

## 最佳实践总结

1. **始终使用事务** - 确保数据一致性
2. **检查对象存在性** - 避免重复创建错误
3. **使用存储过程** - 封装复杂的检查逻辑
4. **记录执行状态** - 便于故障排查
5. **考虑性能影响** - 大表操作要特别小心
6. **测试回滚** - 确保迁移可以安全回滚
7. **遵循命名规范** - 便于维护和管理