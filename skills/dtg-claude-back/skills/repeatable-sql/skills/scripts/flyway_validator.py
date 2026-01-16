#!/usr/bin/env python3
"""
Flyway Migration Script Validator
验证Flyway迁移脚本的可重复执行性和最佳实践
基于实际项目中的Flyway使用模式
"""

import re
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

@dataclass
class ValidationIssue:
    level: ValidationLevel
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None

@dataclass
class ValidationResult:
    file_path: str
    issues: List[ValidationIssue]
    is_valid: bool

class FlywayValidator:
    """Flyway迁移脚本验证器"""

    def __init__(self):
        self.validation_rules = {
            'naming_convention': self._validate_naming_convention,
            'repeatable_operations': self._validate_repeatable_operations,
            'transaction_control': self._validate_transaction_control,
            'rollback_support': self._validate_rollback_support,
            'performance_considerations': self._validate_performance_considerations,
            'security_checks': self._validate_security_checks
        }

    def validate_file(self, file_path: str) -> ValidationResult:
        """验证单个迁移文件"""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # 运行所有验证规则
            for rule_name, rule_func in self.validation_rules.items():
                rule_issues = rule_func(file_path, content, lines)
                issues.extend(rule_issues)

        except Exception as e:
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                message=f"文件读取失败: {str(e)}"
            ))

        is_valid = not any(issue.level == ValidationLevel.ERROR for issue in issues)
        return ValidationResult(file_path=file_path, issues=issues, is_valid=is_valid)

    def _validate_naming_convention(self, file_path: str, content: str, lines: List[str]) -> List[ValidationIssue]:
        """验证文件命名规范"""
        issues = []
        filename = os.path.basename(file_path)

        # 检查Flyway命名规范
        flyway_patterns = [
            r'^V\d+\.\d+\.\d+__[A-Za-z0-9_]+\.sql$',  # Versioned migrations
            r'^R__[A-Za-z0-9_]+\.sql$',  # Repeatable migrations
            r'^U\d+\.\d+\.\d+__[A-Za-z0-9_]+\.sql$'  # Undo migrations
        ]

        valid_pattern = any(re.match(pattern, filename) for pattern in flyway_patterns)

        if not valid_pattern:
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                message=f"文件名不符合Flyway命名规范: {filename}",
                suggestion="使用 V{version}__description.sql 格式，例如 V0.3.181__alter_table_index.sql"
            ))

        return issues

    def _validate_repeatable_operations(self, file_path: str, content: str, lines: List[str]) -> List[ValidationIssue]:
        """验证可重复执行操作"""
        issues = []
        filename = os.path.basename(file_path)

        # 检查是否为版本化迁移但缺少幂等性保护
        if filename.startswith('V'):
            # 检查CREATE INDEX是否没有检查
            if re.search(r'\bCREATE\s+(?:UNIQUE\s+)?INDEX\s+\w+', content, re.IGNORECASE):
                if not re.search(r'DROP\s+PROCEDURE\s+IF\s+EXISTS.*Dynamic_Create_Index', content, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="检测到CREATE INDEX操作但缺少幂等性保护",
                        suggestion="考虑使用存储过程检查索引是否存在，或使用CREATE INDEX IF NOT EXISTS语法（如果数据库支持）"
                    ))

            # 检查ALTER TABLE ADD COLUMN是否没有检查
            if re.search(r'\bALTER\s+TABLE\s+\w+\s+ADD\s+(?:COLUMN\s+)?\w+', content, re.IGNORECASE):
                if not re.search(r'information_schema\.COLUMNS', content, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="检测到ALTER TABLE ADD COLUMN操作但缺少列存在性检查",
                        suggestion="使用information_schema.COLUMNS检查列是否已存在"
                    ))

        return issues

    def _validate_transaction_control(self, file_path: str, content: str, lines: List[str]) -> List[ValidationIssue]:
        """验证事务控制"""
        issues = []

        # 检查自动提交控制
        if re.search(r'\bSET\s+autocommit\s*=\s*0', content, re.IGNORECASE):
            if not re.search(r'\bCOMMIT\b', content, re.IGNORECASE):
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="设置了autocommit=0但没有找到COMMIT语句",
                    suggestion="确保在脚本结束时提交事务"
                ))

        # 检查事务边界
        explicit_transactions = re.findall(r'\b(START\s+TRANSACTION|BEGIN)\b', content, re.IGNORECASE)
        commits = re.findall(r'\bCOMMIT\b', content, re.IGNORECASE)
        rollbacks = re.findall(r'\bROLLBACK\b', content, re.IGNORECASE)

        if explicit_transactions and (len(commits) + len(rollbacks)) < len(explicit_transactions):
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                message="事务开始和结束不匹配",
                suggestion="每个START TRANSACTION都应该有对应的COMMIT或ROLLBACK"
            ))

        return issues

    def _validate_rollback_support(self, file_path: str, content: str, lines: List[str]) -> List[ValidationIssue]:
        """验证回滚支持"""
        issues = []
        filename = os.path.basename(file_path)

        # 对于版本化迁移，检查是否有对应的回滚文件
        if filename.startswith('V'):
            version = re.match(r'V(\d+\.\d+\.\d+)__', filename)
            if version:
                rollback_filename = f"U{version.group(1)}__{filename.split('__', 1)[1]}"
                rollback_path = os.path.join(os.path.dirname(file_path), rollback_filename)

                if not os.path.exists(rollback_path):
                    issues.append(ValidationIssue(
                        level=ValidationLevel.INFO,
                        message=f"建议为版本迁移创建回滚文件: {rollback_filename}",
                        suggestion="创建对应的U迁移文件以支持回滚操作"
                    ))

        return issues

    def _validate_performance_considerations(self, file_path: str, content: str, lines: List[str]) -> List[ValidationIssue]:
        """验证性能考虑"""
        issues = []

        # 检查大表操作
        large_table_patterns = [
            (r'\bUPDATE\s+\w+\s+SET', "全表UPDATE操作可能影响性能"),
            (r'\bDELETE\s+FROM\s+\w+(?:\s+WHERE\s+\w+\s*=\s*\w+)?$', "无WHERE条件的DELETE操作"),
            (r'\bALTER\s+TABLE\s+\w+\s+MODIFY', "大表ALTER操作可能锁定表"),
        ]

        for pattern, message in large_table_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=message,
                    suggestion="考虑分批执行或在低峰期执行"
                ))

        # 检查索引创建
        if re.search(r'\bCREATE\s+INDEX\s+\w+', content, re.IGNORECASE):
            issues.append(ValidationIssue(
                level=ValidationLevel.INFO,
                message="检测到索引创建操作",
                suggestion="对于大表，考虑使用ONLINE或CONCURRENTLY选项（如果数据库支持）"
            ))

        return issues

    def _validate_security_checks(self, file_path: str, content: str, lines: List[str]) -> List[ValidationIssue]:
        """验证安全性检查"""
        issues = []

        # 检查硬编码敏感信息
        sensitive_patterns = [
            (r'password\s*=\s*['\"][^'\"]+['\"]', "检测到可能的硬编码密码"),
            (r'secret\s*=\s*['\"][^'\"]+['\"]', "检测到可能的硬编码密钥"),
            (r'key\s*=\s*['\"][^'\"]+['\"]', "检测到可能的硬编码密钥"),
        ]

        for pattern, message in sensitive_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=message,
                    suggestion="使用环境变量或配置文件管理敏感信息"
                ))

        # 检查权限操作
        if re.search(r'\bGRANT\s+ALL\s+PRIVILEGES', content, re.IGNORECASE):
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message="检测到ALL PRIVILEGES授权",
                suggestion="遵循最小权限原则，只授予必要的权限"
            ))

        return issues

    def validate_directory(self, directory_path: str) -> Dict[str, ValidationResult]:
        """验证目录中的所有迁移文件"""
        results = {}

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.sql'):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.validate_file(file_path)

        return results

    def generate_report(self, results: Dict[str, ValidationResult]) -> str:
        """生成验证报告"""
        report_lines = []
        report_lines.append("# Flyway Migration Validation Report")
        report_lines.append("=" * 50)
        report_lines.append("")

        total_files = len(results)
        valid_files = sum(1 for result in results.values() if result.is_valid)
        error_count = sum(
            sum(1 for issue in result.issues if issue.level == ValidationLevel.ERROR)
            for result in results.values()
        )
        warning_count = sum(
            sum(1 for issue in result.issues if issue.level == ValidationLevel.WARNING)
            for result in results.values()
        )
        info_count = sum(
            sum(1 for issue in result.issues if issue.level == ValidationLevel.INFO)
            for result in results.values()
        )

        report_lines.append(f"## Summary")
        report_lines.append(f"- Total files: {total_files}")
        report_lines.append(f"- Valid files: {valid_files}")
        report_lines.append(f"- Files with errors: {error_count}")
        report_lines.append(f"- Warnings: {warning_count}")
        report_lines.append(f"- Info messages: {info_count}")
        report_lines.append("")

        # 详细结果
        for file_path, result in results.items():
            report_lines.append(f"## {os.path.basename(file_path)}")
            report_lines.append(f"Status: {'✅ PASS' if result.is_valid else '❌ FAIL'}")

            if result.issues:
                report_lines.append("### Issues:")
                for issue in result.issues:
                    status_icon = {"ERROR": "🔴", "WARNING": "🟡", "INFO": "🔵"}[issue.level.value]
                    report_lines.append(f"- {status_icon} **{issue.level.value}**: {issue.message}")
                    if issue.line_number:
                        report_lines.append(f"  Line: {issue.line_number}")
                    if issue.suggestion:
                        report_lines.append(f"  Suggestion: {issue.suggestion}")

            report_lines.append("")

        return "\n".join(report_lines)

def main():
    """示例使用"""
    validator = FlywayValidator()

    # 验证单个文件
    sample_file = "/tmp/sample_migration.sql"
    sample_content = """V0.3.182__example_migration.sql
CREATE INDEX idx_example ON example_table (column1);
"""

    with open(sample_file, 'w') as f:
        f.write(sample_content)

    result = validator.validate_file(sample_file)
    print(f"Validation result: {'PASS' if result.is_valid else 'FAIL'}")
    for issue in result.issues:
        print(f"  {issue.level.value}: {issue.message}")

if __name__ == "__main__":
    main()