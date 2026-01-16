#!/usr/bin/env python3
"""
Repeatable SQL Table Migrator
用于生成可重复执行的表结构变更SQL脚本
支持字段添加、修改、删除等操作的幂等性处理
"""

import json
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum

class AlterOperation(Enum):
    ADD_COLUMN = "ADD"
    MODIFY_COLUMN = "MODIFY"
    DROP_COLUMN = "DROP"
    ADD_CONSTRAINT = "ADD_CONSTRAINT"
    DROP_CONSTRAINT = "DROP_CONSTRAINT"

@dataclass
class ColumnDefinition:
    """列定义"""
    name: str
    data_type: str
    nullable: bool = True
    default_value: Optional[str] = None
    comment: Optional[str] = None

@dataclass
class TableAlterSpec:
    """表变更规范"""
    table_name: str
    operation: AlterOperation
    column_name: Optional[str] = None
    column_def: Optional[ColumnDefinition] = None
    constraint_name: Optional[str] = None
    constraint_sql: Optional[str] = None

class RepeatableTableMigrator:
    """可重复执行表迁移生成器"""

    def __init__(self, database_type: str = "mysql"):
        self.database_type = database_type.lower()

    def generate_column_check_procedure(self) -> str:
        """生成列检查存储过程"""
        if self.database_type == "mysql":
            return self._generate_mysql_column_procedure()
        elif self.database_type == "postgresql":
            return self._generate_postgresql_column_function()
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")

    def _generate_mysql_column_procedure(self) -> str:
        """生成MySQL版本的列管理存储过程"""
        return '''DELIMITER $$
-- =================================================================
-- 存储过程: 检查并添加列的通用逻辑
-- =================================================================
DROP PROCEDURE IF EXISTS Dynamic_Add_Column$$
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

    -- 根据结果执行动作
    IF v_column_exists = 0 THEN
        -- 列不存在，添加列
        SET @sql = CONCAT('ALTER TABLE ', p_target_table, ' ADD COLUMN ', p_column_name, ' ', p_column_definition);
        SET @sql = IF(p_column_comment IS NOT NULL AND p_column_comment != '',
                      CONCAT(@sql, ' COMMENT ''', p_column_comment, ''''),
                      @sql);

        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SELECT CONCAT('[CREATED]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中添加成功。') AS message;
    ELSE
        -- 列已存在
        SELECT CONCAT('[SKIPPED]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中已存在。') AS message;
    END IF;
END$$

-- =================================================================
-- 存储过程: 检查并修改列定义的通用逻辑
-- =================================================================
DROP PROCEDURE IF EXISTS Dynamic_Modify_Column$$
CREATE PROCEDURE Dynamic_Modify_Column(
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

    -- 根据结果执行动作
    IF v_column_exists > 0 THEN
        -- 列存在，修改列
        SET @sql = CONCAT('ALTER TABLE ', p_target_table, ' MODIFY COLUMN ', p_column_name, ' ', p_column_definition);
        SET @sql = IF(p_column_comment IS NOT NULL AND p_column_comment != '',
                      CONCAT(@sql, ' COMMENT ''', p_column_comment, ''''),
                      @sql);

        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SELECT CONCAT('[MODIFIED]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中修改成功。') AS message;
    ELSE
        -- 列不存在
        SELECT CONCAT('[ERROR]: 列 ', p_column_name, ' 在表 ', p_target_table, ' 中不存在，无法修改。') AS message;
    END IF;
END$$
DELIMITER ;'''

    def _generate_postgresql_column_function(self) -> str:
        """生成PostgreSQL版本的列管理函数"""
        return '''-- =================================================================
-- 函数: 检查并添加列的通用逻辑 (PostgreSQL版本)
-- =================================================================
CREATE OR REPLACE FUNCTION dynamic_add_column(
    p_target_table VARCHAR(64),
    p_column_name VARCHAR(64),
    p_column_definition TEXT,
    p_column_comment VARCHAR(255) DEFAULT NULL
)
RETURNS TEXT AS $$
DECLARE
    v_column_exists INT;
    v_sql TEXT;
BEGIN
    -- 检查列是否存在
    SELECT COUNT(*)
    INTO v_column_exists
    FROM information_schema.columns
    WHERE table_schema = current_schema()
    AND table_name = p_target_table
    AND column_name = p_column_name;

    IF v_column_exists = 0 THEN
        -- 列不存在，添加列
        v_sql := 'ALTER TABLE ' || p_target_table || ' ADD COLUMN ' || p_column_name || ' ' || p_column_definition;

        EXECUTE v_sql;

        -- 添加注释（如果提供）
        IF p_column_comment IS NOT NULL THEN
            EXECUTE 'COMMENT ON COLUMN ' || p_target_table || '.' || p_column_name || ' IS ''' || p_column_comment || '''';
        END IF;

        RETURN '[CREATED]: 列 ' || p_column_name || ' 在表 ' || p_target_table || ' 中添加成功。';
    ELSE
        RETURN '[SKIPPED]: 列 ' || p_column_name || ' 在表 ' || p_target_table || ' 中已存在。';
    END IF;
END;
$$ LANGUAGE plpgsql;'''

    def generate_table_alters(self, alters: List[TableAlterSpec]) -> str:
        """生成表变更语句"""
        statements = []

        for alter in alters:
            if alter.operation == AlterOperation.ADD_COLUMN and alter.column_def:
                if self.database_type == "mysql":
                    column_def = self._build_mysql_column_def(alter.column_def)
                    call = f"CALL Dynamic_Add_Column('{alter.table_name}', '{alter.column_def.name}', '{column_def}', '{alter.column_def.comment or ''}');"
                elif self.database_type == "postgresql":
                    column_def = self._build_postgresql_column_def(alter.column_def)
                    call = f"SELECT dynamic_add_column('{alter.table_name}', '{alter.column_def.name}', '{column_def}', '{alter.column_def.comment or ''}');"
                statements.append(call)

            elif alter.operation == AlterOperation.MODIFY_COLUMN and alter.column_def:
                if self.database_type == "mysql":
                    column_def = self._build_mysql_column_def(alter.column_def)
                    call = f"CALL Dynamic_Modify_Column('{alter.table_name}', '{alter.column_def.name}', '{column_def}', '{alter.column_def.comment or ''}');"
                    statements.append(call)

            elif alter.operation == AlterOperation.DROP_COLUMN and alter.column_name:
                # 对于删除操作，需要先检查列是否存在
                if self.database_type == "mysql":
                    sql = f"""SET @column_exists = (SELECT COUNT(*) FROM information_schema.COLUMNS
                              WHERE TABLE_SCHEMA = DATABASE()
                              AND TABLE_NAME = '{alter.table_name}'
                              AND COLUMN_NAME = '{alter.column_name}');
                              SET @drop_sql = IF(@column_exists > 0,
                                'ALTER TABLE {alter.table_name} DROP COLUMN {alter.column_name}',
                                'SELECT ''[SKIPPED]: 列 {alter.column_name} 在表 {alter.table_name} 中不存在。'' AS message');
                              PREPARE stmt FROM @drop_sql;
                              EXECUTE stmt;
                              DEALLOCATE PREPARE stmt;"""
                elif self.database_type == "postgresql":
                    sql = f"""DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns
               WHERE table_schema = current_schema()
               AND table_name = '{alter.table_name}'
               AND column_name = '{alter.column_name}') THEN
        EXECUTE 'ALTER TABLE {alter.table_name} DROP COLUMN {alter.column_name}';
        RAISE NOTICE '[DROPPED]: 列 % 在表 % 中删除成功。', '{alter.column_name}', '{alter.table_name}';
    ELSE
        RAISE NOTICE '[SKIPPED]: 列 % 在表 % 中不存在。', '{alter.column_name}', '{alter.table_name}';
    END IF;
END $$;"""
                statements.append(sql)

        return "\n".join(statements)

    def _build_mysql_column_def(self, column: ColumnDefinition) -> str:
        """构建MySQL列定义"""
        parts = [column.data_type]

        if not column.nullable:
            parts.append("NOT NULL")

        if column.default_value is not None:
            parts.append(f"DEFAULT {column.default_value}")

        return " ".join(parts)

    def _build_postgresql_column_def(self, column: ColumnDefinition) -> str:
        """构建PostgreSQL列定义"""
        parts = [column.data_type]

        if not column.nullable:
            parts.append("NOT NULL")

        if column.default_value is not None:
            parts.append(f"DEFAULT {column.default_value}")

        return " ".join(parts)

    def generate_cleanup_procedure(self) -> str:
        """生成清理存储过程的语句"""
        if self.database_type == "mysql":
            return "-- 清理存储过程\nDROP PROCEDURE IF EXISTS Dynamic_Add_Column;\nDROP PROCEDURE IF EXISTS Dynamic_Modify_Column;"
        elif self.database_type == "postgresql":
            return "-- 清理函数\nDROP FUNCTION IF EXISTS dynamic_add_column(VARCHAR, VARCHAR, TEXT, VARCHAR);"

    def generate_full_script(self, alters: List[TableAlterSpec]) -> str:
        """生成完整的可重复执行表迁移脚本"""
        # 只选择需要存储过程的操作
        needs_procedures = any(
            alter.operation in [AlterOperation.ADD_COLUMN, AlterOperation.MODIFY_COLUMN]
            for alter in alters
        )

        parts = []

        if needs_procedures:
            parts.append(self.generate_column_check_procedure())
            parts.append("")
            parts.append("-- =================================================================")
            parts.append("-- 执行表结构变更逻辑")
            parts.append("-- =================================================================")
            parts.append("")

        parts.append(self.generate_table_alters(alters))
        parts.append("")

        if needs_procedures:
            parts.append(self.generate_cleanup_procedure())

        return "\n".join(parts)

def main():
    """示例使用"""
    migrator = RepeatableTableMigrator("mysql")

    # 示例表变更定义（基于commit中的NotifyUrl字段变更）
    alters = [
        TableAlterSpec(
            table_name="t_mch_agentpay_record",
            operation=AlterOperation.MODIFY_COLUMN,
            column_def=ColumnDefinition(
                name="NotifyUrl",
                data_type="varchar(256)",
                nullable=True,
                comment="通知地址"
            )
        ),
        TableAlterSpec(
            table_name="example_table",
            operation=AlterOperation.ADD_COLUMN,
            column_def=ColumnDefinition(
                name="new_field",
                data_type="VARCHAR(100)",
                nullable=True,
                default_value="NULL",
                comment="新增字段"
            )
        )
    ]

    script = migrator.generate_full_script(alters)
    print(script)

if __name__ == "__main__":
    main()