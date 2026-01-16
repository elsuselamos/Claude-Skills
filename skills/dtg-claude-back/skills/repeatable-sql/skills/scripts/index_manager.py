#!/usr/bin/env python3
"""
Repeatable SQL Index Manager
基于最新commit中的Dynamic_Create_Index存储过程的Python实现
生成可重复执行索引创建的SQL脚本
"""

import json
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum

class IndexType(Enum):
    INDEX = "INDEX"
    UNIQUE = "UNIQUE"

@dataclass
class ColumnSpec:
    """列规范"""
    name: str
    direction: str = "ASC"  # ASC 或 DESC

@dataclass
class IndexSpec:
    """索引规范"""
    table_name: str
    index_name: str
    columns: List[ColumnSpec]
    index_type: IndexType = IndexType.INDEX

class RepeatableSQLGenerator:
    """可重复执行SQL生成器"""

    def __init__(self, database_type: str = "mysql"):
        self.database_type = database_type.lower()

    def generate_stored_procedure(self) -> str:
        """生成动态索引创建存储过程"""
        if self.database_type == "mysql":
            return self._generate_mysql_stored_procedure()
        elif self.database_type == "postgresql":
            return self._generate_postgresql_function()
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")

    def _generate_mysql_stored_procedure(self) -> str:
        """生成MySQL版本的存储过程"""
        return '''DELIMITER $$
-- =================================================================
-- 存储过程: 检查并创建索引的通用逻辑
-- =================================================================
DROP PROCEDURE IF EXISTS Dynamic_Create_Index$$
CREATE PROCEDURE Dynamic_Create_Index(
    IN p_target_table VARCHAR(64),
    IN p_target_index_name VARCHAR(64),
    IN p_target_columns_with_sort TEXT,
    IN p_target_index_type VARCHAR(10) -- 'INDEX' or 'UNIQUE'
)
BEGIN
    -- 内部变量声明
    DECLARE v_is_unique INT;
    DECLARE v_normalized_columns TEXT;
    DECLARE v_expected_collation TEXT;
    DECLARE v_index_exists INT DEFAULT 0;
    DECLARE v_s TEXT;

    -- 内部变量定义与预处理
    SET v_is_unique = IF(p_target_index_type = 'UNIQUE', 0, 1);

    -- 合并正则化步骤：去除 ASC/DESC 和空格，并转换为大写
    SET v_normalized_columns = REPLACE(REPLACE(REPLACE(UPPER(p_target_columns_with_sort), ' ASC', ''), ' DESC', ''), ' ', '');

    -- 计算期望的 COLLATION 字符串
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

    -- 动态SQL: 检查匹配的索引
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

    -- 执行检查语句
    SET @v_s_to_exec = v_s;
    PREPARE stmt FROM @v_s_to_exec;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET v_index_exists = @index_exists_temp;

    -- 动态SQL: 根据结果执行动作
    IF v_index_exists = 0 THEN
        IF UPPER(p_target_index_type) = 'UNIQUE' THEN
            SET v_s = CONCAT('CREATE UNIQUE INDEX ', p_target_index_name, ' ON ', p_target_table, ' (',
                             p_target_columns_with_sort, ')');
        ELSE
            SET v_s = CONCAT('CREATE INDEX ', p_target_index_name, ' ON ', p_target_table, ' (',
                             p_target_columns_with_sort, ')');
        END IF;

        -- 执行创建语句
        SET @v_s_to_exec = v_s;
        PREPARE stmt FROM @v_s_to_exec;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SELECT CONCAT('[CREATED]: 索引 ', p_target_index_name, ' (', v_normalized_columns, ') 创建成功。') AS message;
    ELSE
        SELECT CONCAT('[SKIPPED]: 匹配的索引 ', p_target_index_name, ' (', v_normalized_columns,
                      ') 已存在。') AS message;
    END IF;

END$$
DELIMITER ;'''

    def _generate_postgresql_function(self) -> str:
        """生成PostgreSQL版本的函数"""
        return '''-- =================================================================
-- 函数: 检查并创建索引的通用逻辑 (PostgreSQL版本)
-- =================================================================
CREATE OR REPLACE FUNCTION dynamic_create_index(
    p_target_table VARCHAR(64),
    p_target_index_name VARCHAR(64),
    p_target_columns TEXT,
    p_target_index_type VARCHAR(10) DEFAULT 'INDEX'
)
RETURNS TEXT AS $$
DECLARE
    v_index_exists INT;
    v_sql TEXT;
    v_normalized_columns TEXT;
    v_columns_array TEXT[];
BEGIN
    -- 正则化列名
    v_normalized_columns := REPLACE(REPLACE(REPLACE(UPPER(p_target_columns), ' ASC', ''), ' DESC', ''), ' ', '');

    -- 检查索引是否存在
    SELECT COUNT(*)
    INTO v_index_exists
    FROM pg_indexes
    WHERE schemaname = current_schema()
    AND tablename = p_target_table
    AND indexname = p_target_index_name;

    IF v_index_exists = 0 THEN
        -- 创建索引
        IF UPPER(p_target_index_type) = 'UNIQUE' THEN
            v_sql := 'CREATE UNIQUE INDEX ' || p_target_index_name ||
                    ' ON ' || p_target_table || ' (' || p_target_columns || ')';
        ELSE
            v_sql := 'CREATE INDEX ' || p_target_index_name ||
                    ' ON ' || p_target_table || ' (' || p_target_columns || ')';
        END IF;

        EXECUTE v_sql;

        RETURN '[CREATED]: 索引 ' || p_target_index_name || ' (' || v_normalized_columns || ') 创建成功。';
    ELSE
        RETURN '[SKIPPED]: 索引 ' || p_target_index_name || ' (' || v_normalized_columns || ') 已存在。';
    END IF;
END;
$$ LANGUAGE plpgsql;'''

    def generate_index_calls(self, indexes: List[IndexSpec]) -> str:
        """生成索引创建调用语句"""
        calls = []
        for idx in indexes:
            columns_str = ", ".join([f"{col.name} {col.direction}".strip() for col in idx.columns])
            if self.database_type == "mysql":
                call = f"CALL Dynamic_Create_Index('{idx.table_name}', '{idx.index_name}', '{columns_str}', '{idx.index_type.value}');"
            elif self.database_type == "postgresql":
                call = f"SELECT dynamic_create_index('{idx.table_name}', '{idx.index_name}', '{columns_str}', '{idx.index_type.value}');"
            calls.append(call)

        return "\n".join(calls)

    def generate_cleanup_procedure(self) -> str:
        """生成清理存储过程的语句"""
        if self.database_type == "mysql":
            return "-- 清理存储过程\nDROP PROCEDURE IF EXISTS Dynamic_Create_Index;"
        elif self.database_type == "postgresql":
            return "-- 清理函数\nDROP FUNCTION IF EXISTS dynamic_create_index(VARCHAR, VARCHAR, TEXT, VARCHAR);"

    def generate_full_script(self, indexes: List[IndexSpec]) -> str:
        """生成完整的可重复执行索引脚本"""
        parts = [
            self.generate_stored_procedure(),
            "",
            "-- =================================================================",
            "-- 执行索引创建逻辑 (调用存储过程)",
            "-- =================================================================",
            "",
            self.generate_index_calls(indexes),
            "",
            self.generate_cleanup_procedure()
        ]

        return "\n".join(parts)

def main():
    """示例使用"""
    generator = RepeatableSQLGenerator("mysql")

    # 示例索引定义
    indexes = [
        IndexSpec(
            table_name="deposit",
            index_name="idx_merchant_order_id",
            columns=[ColumnSpec("merchant_order_id")],
            index_type=IndexType.INDEX
        ),
        IndexSpec(
            table_name="t_mch_account_history",
            index_name="idx_mch_createtime",
            columns=[ColumnSpec("MchId"), ColumnSpec("CreateTime")],
            index_type=IndexType.INDEX
        ),
        IndexSpec(
            table_name="t_mch_account_history",
            index_name="idx_child_createtime",
            columns=[ColumnSpec("IsChild"), ColumnSpec("CreateTime", "DESC")],
            index_type=IndexType.INDEX
        ),
        IndexSpec(
            table_name="t_agent_income_report",
            index_name="idx_agent_balance",
            columns=[ColumnSpec("AgentId"), ColumnSpec("BalanceType")],
            index_type=IndexType.UNIQUE
        )
    ]

    script = generator.generate_full_script(indexes)
    print(script)

if __name__ == "__main__":
    main()