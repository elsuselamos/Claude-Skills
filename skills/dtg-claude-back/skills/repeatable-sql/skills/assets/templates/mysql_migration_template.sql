-- V{major}.{minor}.{patch}__{description}.sql
-- MySQL可重复执行迁移模板
-- 基于项目中的Dynamic_Create_Index存储过程模式

-- =================================================================
-- 设置执行环境
-- =================================================================
SET autocommit = 0;
SET foreign_key_checks = 0;

-- =================================================================
-- 存储过程: 动态索引创建
-- =================================================================
DELIMITER $$
DROP PROCEDURE IF EXISTS Dynamic_Create_Index$$
CREATE PROCEDURE Dynamic_Create_Index(
    IN p_target_table VARCHAR(64),
    IN p_target_index_name VARCHAR(64),
    IN p_target_columns_with_sort TEXT,
    IN p_target_index_type VARCHAR(10)
)
BEGIN
    DECLARE v_is_unique INT;
    DECLARE v_normalized_columns TEXT;
    DECLARE v_expected_collation TEXT;
    DECLARE v_index_exists INT DEFAULT 0;
    DECLARE v_s TEXT;

    SET v_is_unique = IF(p_target_index_type = 'UNIQUE', 0, 1);
    SET v_normalized_columns = REPLACE(REPLACE(REPLACE(UPPER(p_target_columns_with_sort), ' ASC', ''), ' DESC', ''), ' ', '');

    SELECT GROUP_CONCAT(
                   IF(UPPER(SUBSTRING_INDEX(SUBSTRING_INDEX(p_target_columns_with_sort, ',', n), ',', -1)) LIKE '%DESC',
                      'D', 'A')
                   ORDER BY n
           )
    INTO v_expected_collation
    FROM (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
          UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8
          UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12
          UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16) AS numbers
    WHERE n <= LENGTH(p_target_columns_with_sort) - LENGTH(REPLACE(p_target_columns_with_sort, ',', '')) + 1;

    SET v_s = CONCAT('
        SELECT COUNT(*) INTO @index_exists_temp
        FROM (
            SELECT
                s1.NON_UNIQUE,
                GROUP_CONCAT(s1.COLUMN_NAME ORDER BY s1.SEQ_IN_INDEX ASC) AS columns,
                GROUP_CONCAT(s1.COLLATION ORDER BY s1.SEQ_IN_INDEX ASC) AS collation_str
            FROM information_schema.STATISTICS s1
            WHERE s1.TABLE_SCHEMA = DATABASE()
            AND s1.TABLE_NAME = ''', p_target_table, '''
            AND s1.INDEX_NAME != ''PRIMARY''
            GROUP BY s1.INDEX_NAME, s1.NON_UNIQUE
        ) AS idx
        WHERE idx.columns = ''', v_normalized_columns, '''
        AND idx.NON_UNIQUE = ', v_is_unique, '
        AND idx.collation_str = ''', v_expected_collation, '''
    ');

    SET @v_s_to_exec = v_s;
    PREPARE stmt FROM @v_s_to_exec;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET v_index_exists = @index_exists_temp;

    IF v_index_exists = 0 THEN
        IF UPPER(p_target_index_type) = 'UNIQUE' THEN
            SET v_s = CONCAT('CREATE UNIQUE INDEX ', p_target_index_name, ' ON ', p_target_table, ' (',
                             p_target_columns_with_sort, ')');
        ELSE
            SET v_s = CONCAT('CREATE INDEX ', p_target_index_name, ' ON ', p_target_table, ' (',
                             p_target_columns_with_sort, ')');
        END IF;

        SET @v_s_to_exec = v_s;
        PREPARE stmt FROM @v_s_to_exec;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SELECT CONCAT('[CREATED]: 索引 ', p_target_index_name, ' (', v_normalized_columns, ') 创建成功。') AS message;
    ELSE
        SELECT CONCAT('[SKIPPED]: 匹配的索引 ', p_target_index_name, ' (', v_normalized_columns, ') 已存在。') AS message;
    END IF;

END$$
DELIMITER ;

-- =================================================================
-- 存储过程: 动态列添加
-- =================================================================
DELIMITER $$
DROP PROCEDURE IF EXISTS Dynamic_Add_Column$$
CREATE PROCEDURE Dynamic_Add_Column(
    IN p_target_table VARCHAR(64),
    IN p_column_name VARCHAR(64),
    IN p_column_definition TEXT,
    IN p_column_comment VARCHAR(255)
)
BEGIN
    DECLARE v_column_exists INT DEFAULT 0;

    SELECT COUNT(*)
    INTO v_column_exists
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = p_target_table
    AND COLUMN_NAME = p_column_name;

    IF v_column_exists = 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', p_target_table, ' ADD COLUMN ', p_column_name, ' ', p_column_definition);
        SET @sql = IF(p_column_comment IS NOT NULL AND p_column_comment != '',
                      CONCAT(@sql, ' COMMENT ''', p_column_comment, ''''),
                      @sql);

        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SELECT CONCAT('[CREATED]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中添加成功。') AS message;
    ELSE
        SELECT CONCAT('[SKIPPED]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中已存在。') AS message;
    END IF;
END$$
DELIMITER ;

-- =================================================================
-- 存储过程: 动态列修改
-- =================================================================
DELIMITER $$
DROP PROCEDURE IF EXISTS Dynamic_Modify_Column$$
CREATE PROCEDURE Dynamic_Modify_Column(
    IN p_target_table VARCHAR(64),
    IN p_column_name VARCHAR(64),
    IN p_column_definition TEXT,
    IN p_column_comment VARCHAR(255)
)
BEGIN
    DECLARE v_column_exists INT DEFAULT 0;

    SELECT COUNT(*)
    INTO v_column_exists
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = p_target_table
    AND COLUMN_NAME = p_column_name;

    IF v_column_exists > 0 THEN
        SET @sql = CONCAT('ALTER TABLE ', p_target_table, ' MODIFY COLUMN ', p_column_name, ' ', p_column_definition);
        SET @sql = IF(p_column_comment IS NOT NULL AND p_column_comment != '',
                      CONCAT(@sql, ' COMMENT ''', p_column_comment, ''''),
                      @sql);

        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SELECT CONCAT('[MODIFIED]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中修改成功。') AS message;
    ELSE
        SELECT CONCAT('[ERROR]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中不存在，无法修改。') AS message;
    END IF;
END$$
DELIMITER ;

-- =================================================================
-- 执行迁移操作
-- =================================================================

-- 在此添加具体的迁移操作:
-- 示例: 添加索引
-- CALL Dynamic_Create_Index('table_name', 'idx_column1', 'column1', 'INDEX');
-- CALL Dynamic_Create_Index('table_name', 'idx_columns', 'column1, column2 DESC', 'UNIQUE');

-- 示例: 添加列
-- CALL Dynamic_Add_Column('table_name', 'new_column', 'VARCHAR(100) NULL', '新增列');

-- 示例: 修改列
-- CALL Dynamic_Modify_Column('table_name', 'existing_column', 'VARCHAR(256) NULL', '修改后的列注释');

-- =================================================================
-- 提交事务
-- =================================================================
COMMIT;

-- =================================================================
-- 清理存储过程
-- =================================================================
DROP PROCEDURE IF EXISTS Dynamic_Create_Index;
DROP PROCEDURE IF EXISTS Dynamic_Add_Column;
DROP PROCEDURE IF EXISTS Dynamic_Modify_Column;

-- 恢复外键检查
SET foreign_key_checks = 1;
SET autocommit = 1;

-- =================================================================
-- 记录迁移完成
-- =================================================================
-- 如果需要，可以在这里添加日志记录逻辑