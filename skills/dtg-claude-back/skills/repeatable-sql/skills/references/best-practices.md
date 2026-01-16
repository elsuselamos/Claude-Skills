# 可重复执行SQL最佳实践

本文档总结了在不同数据库中实现可重复执行SQL的通用最佳实践。

## 设计原则

### 1. 幂等性 (Idempotency)
- **定义**: 同一个SQL脚本可以多次执行，产生相同的结果状态
- **重要性**: 确保数据库迁移的安全性和可靠性
- **实现**: 使用条件检查、异常处理、IF NOT EXISTS语法

### 2. 向后兼容性
- 支持多个数据库版本的语法差异
- 提供降级方案和替代实现
- 考虑不同版本的特性支持

### 3. 原子性
- 使用事务确保操作的原子性
- 要么全部成功，要么全部回滚
- 避免部分执行造成的不一致状态

## 通用模式

### 检查后执行 (Check-Then-Execute)

```sql
-- 通用模式
IF NOT EXISTS (SELECT 1 FROM [系统视图] WHERE [条件]) THEN
    -- 执行DDL操作
END IF;

-- 或使用系统存储过程
BEGIN
    -- 检查对象是否存在
    -- 执行相应操作
END;
```

### 异常处理

```sql
-- MySQL
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
BEGIN
    -- 错误处理逻辑
    ROLLBACK;
END;

-- PostgreSQL
BEGIN
    -- DDL操作
EXCEPTION WHEN OTHERS THEN
    -- 错误处理逻辑
    ROLLBACK;
END;
```

### 事务管理

```sql
-- 标准事务模式
BEGIN TRANSACTION;

-- DDL操作1
-- DDL操作2
-- 数据操作

COMMIT;

-- 或者使用自动提交控制
SET autocommit = 0;
-- 执行操作
COMMIT;
SET autocommit = 1;
```

## 数据库特定模式

### MySQL最佳实践

1. **使用存储过程封装检查逻辑**
   ```sql
   CALL Dynamic_Create_Index('table', 'index', 'columns', 'INDEX');
   ```

2. **利用information_schema进行元数据查询**
   ```sql
   SELECT COUNT(*) FROM information_schema.COLUMNS
   WHERE TABLE_SCHEMA = DATABASE()
   AND TABLE_NAME = 'table_name'
   AND COLUMN_NAME = 'column_name';
   ```

3. **注意字符集和排序规则的影响**
   ```sql
   -- 规范化比较
   SET v_normalized_columns = REPLACE(REPLACE(REPLACE(
       UPPER(p_target_columns_with_sort), ' ASC', ''), ' DESC', ''), ' ', '');
   ```

### PostgreSQL最佳实践

1. **优先使用IF NOT EXISTS语法**
   ```sql
   CREATE INDEX IF NOT EXISTS idx_name ON table_name (column_name);
   ALTER TABLE table_name ADD COLUMN IF NOT EXISTS new_column TYPE;
   ```

2. **利用DO块执行复杂逻辑**
   ```sql
   DO $$
   BEGIN
       IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'constraint_name') THEN
           ALTER TABLE table_name ADD CONSTRAINT constraint_name ...;
       END IF;
   END$$;
   ```

3. **使用ON CONFLICT处理数据冲突**
   ```sql
   INSERT INTO table_name (id, name) VALUES (1, 'test')
   ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
   ```

### Oracle最佳实践

1. **使用EXCEPTION处理对象已存在错误**
   ```sql
   BEGIN
       EXECUTE IMMEDIATE 'CREATE INDEX idx_name ON table_name (column_name)';
   EXCEPTION
       WHEN OTHERS THEN
           IF SQLCODE != -955 THEN -- name is already used
               RAISE;
           END IF;
   END;
   ```

2. **利用USER_OBJECTS视图**
   ```sql
   DECLARE
       v_count NUMBER;
   BEGIN
       SELECT COUNT(*) INTO v_count
       FROM USER_OBJECTS
       WHERE OBJECT_NAME = 'OBJECT_NAME'
       AND OBJECT_TYPE = 'INDEX';

       IF v_count = 0 THEN
           -- 创建对象
       END IF;
   END;
   ```

### SQL Server最佳实践

1. **使用IF EXISTS条件**
   ```sql
   IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_name')
   BEGIN
       CREATE INDEX idx_name ON table_name (column_name);
   END
   ```

2. **利用sys.objects系统视图**
   ```sql
   IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE object_id = OBJECT_ID('table_name'))
   BEGIN
       CREATE TABLE table_name (...);
   END
   ```

## 性能考虑

### 大表操作

1. **分批处理**
   ```sql
   -- 使用LIMIT和OFFSET分批更新
   UPDATE large_table SET status = 'processed'
   WHERE id IN (
       SELECT id FROM large_table WHERE status = 'pending' LIMIT 1000
   );
   ```

2. **索引创建优化**
   ```sql
   -- PostgreSQL并发索引
   CREATE INDEX CONCURRENTLY idx_name ON table_name (column_name);

   -- MySQL在线索引（MySQL 5.6+）
   ALTER TABLE table_name ADD INDEX idx_name (column_name), ALGORITHM=INPLACE;
   ```

3. **临时禁用约束**
   ```sql
   -- 禁用外键检查
   SET foreign_key_checks = 0;
   -- 执行操作
   SET foreign_key_checks = 1;
   ```

### 锁定控制

1. **选择合适的隔离级别**
   ```sql
   -- 设置事务隔离级别
   SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
   ```

2. **避免长事务**
   ```sql
   -- 分解大事务为小事务
   BEGIN;
   -- 执行少量操作
   COMMIT;
   ```

## 安全考虑

### 权限管理

1. **最小权限原则**
   ```sql
   -- 只授予权限
   GRANT SELECT, INSERT ON table_name TO user_name;
   ```

2. **避免硬编码敏感信息**
   ```sql
   -- 使用变量或参数化查询
   SET @password = 'secure_password';
   ```

### 输入验证

1. **参数化DDL操作**
   ```sql
   -- 使用存储过程参数
   CREATE PROCEDURE SafeDDL(p_table_name VARCHAR(100))
   BEGIN
       -- 验证表名格式
       IF p_table_name REGEXP '^[a-zA-Z_][a-zA-Z0-9_]*$' THEN
           -- 执行DDL
       END IF;
   END;
   ```

## 测试策略

### 环境隔离

1. **开发环境测试**
   - 验证脚本的正确性
   - 测试不同数据库版本的兼容性

2. **预生产环境验证**
   - 使用生产数据的副本进行测试
   - 验证性能影响

3. **回滚测试**
   - 确保每个迁移都有对应的回滚方案
   - 测试回滚脚本的正确性

### 验证检查点

1. **对象存在性检查**
   ```sql
   -- 检查创建的对象
   SELECT * FROM information_schema.tables WHERE table_name = 'new_table';
   SELECT * FROM information_schema.columns WHERE table_name = 'new_table';
   SELECT * FROM information_schema.statistics WHERE table_name = 'new_table';
   ```

2. **数据完整性验证**
   ```sql
   -- 检查数据一致性
   SELECT COUNT(*) FROM new_table WHERE condition;
   SELECT * FROM new_table LIMIT 10;
   ```

## 监控和日志

### 执行日志

1. **记录迁移执行状态**
   ```sql
   CREATE TABLE migration_log (
       id SERIAL PRIMARY KEY,
       migration_name VARCHAR(255) NOT NULL,
       execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       status ENUM('SUCCESS', 'FAILED', 'ROLLED_BACK'),
       message TEXT
   );
   ```

2. **详细操作记录**
   ```sql
   -- 记录每个操作的结果
   INSERT INTO migration_log (migration_name, status, message)
   VALUES ('V1.0.0__create_table', 'SUCCESS', 'Table created successfully');
   ```

### 性能监控

1. **执行时间统计**
   ```sql
   -- 记录开始和结束时间
   SET @start_time = NOW();
   -- 执行操作
   SET @execution_time = TIMESTAMPDIFF(SECOND, @start_time, NOW());
   ```

2. **资源使用监控**
   ```sql
   -- 监控表大小变化
   SELECT table_name,
          ROUND(data_length/1024/1024, 2) AS data_mb,
          ROUND(index_length/1024/1024, 2) AS index_mb
   FROM information_schema.tables;
   ```

## 工具和自动化

### Flyway集成

1. **版本化命名**
   ```
   V{major}.{minor}.{patch}__description.sql
   U{major}.{minor}.{patch}__description.sql  # 回滚脚本
   R__repeatable_description.sql             # 可重复执行脚本
   ```

2. **验证脚本**
   - 每次迁移后验证数据库状态
   - 检查对象创建是否成功
   - 验证数据完整性

### 持续集成

1. **自动化测试**
   - 在CI/CD流水线中集成迁移测试
   - 自动执行验证脚本
   - 性能回归测试

2. **环境管理**
   - 使用容器化测试环境
   - 自动创建和销毁测试数据库

## 错误处理模式

### 常见错误类型

1. **对象已存在错误**
   ```sql
   -- MySQL: 1050 Table already exists
   -- PostgreSQL: 42P07 relation already exists
   -- Oracle: ORA-00955 name is already used
   ```

2. **约束违反错误**
   ```sql
   -- 外键约束违反
   -- 唯一约束违反
   -- 检查约束违反
   ```

3. **权限不足错误**
   ```sql
   -- 需要适当的权限检查
   ```

### 恢复策略

1. **事务回滚**
   ```sql
   -- 自动回滚
   BEGIN;
   -- 操作
   -- 如果失败则自动回滚
   COMMIT;
   ```

2. **手动修复**
   - 清理部分创建的对象
   - 恢复数据一致性
   - 重新执行迁移

## 文档和维护

### 迁移文档

1. **迁移描述**
   - 变更目的和范围
   - 影响的系统模块
   - 预期的性能影响

2. **回滚指南**
   - 回滚步骤
   - 数据恢复方法
   - 验证检查点

### 维护计划

1. **定期审查**
   - 清理过期的迁移日志
   - 优化索引策略
   - 更新文档

2. **性能调优**
   - 监控慢查询
   - 优化索引使用
   - 调整表结构

## 总结

可重复执行SQL是数据库管理的核心技能，需要：

1. **理解数据库特性** - 不同数据库的语法差异
2. **掌握幂等性设计** - 确保安全性
3. **考虑性能影响** - 避免生产环境问题
4. **建立完善的测试流程** - 确保迁移可靠性
5. **实现监控和日志** - 便于问题排查
6. **遵循最佳实践** - 减少常见错误

通过遵循这些最佳实践，可以构建安全、可靠、可维护的数据库迁移系统。