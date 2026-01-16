#!/usr/bin/env python3
"""
支付渠道处理类代码验证器
用于检查支付代码的安全性、规范性和最佳实践
"""

import os
import re
import argparse
from typing import List, Tuple

class PaymentHandlerValidator:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.code = ""
        self.issues = []
        self.suggestions = []

    def load_code(self) -> bool:
        """加载Java代码文件"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.code = f.read()
            return True
        except Exception as e:
            self.issues.append(f"❌ 无法加载文件: {e}")
            return False

    def validate_security(self) -> List[str]:
        """安全性验证"""
        security_issues = []

        # 检查敏感信息日志
        if re.search(r'log\.(info|debug|error).*?(password|privateKey|secretKey|key)', self.code, re.IGNORECASE):
            security_issues.append("⚠️  发现敏感信息可能被记录到日志中")

        # 检查SQL注入风险
        if re.search(r'executeUpdate?\s*\(\s*".*\+"\s*\)', self.code):
            security_issues.append("⚠️  可能存在SQL注入风险")

        # 检查硬编码密钥
        if re.search(r'(privateKey|secretKey|apiKey)\s*=\s*"[^"]+"', self.code):
            security_issues.append("⚠️  发现硬编码的密钥信息")

        # 检查签名验证
        if not re.search(r'isValidSign', self.code):
            security_issues.append("⚠️  缺少签名验证方法")

        # 检查HTTPS使用
        if re.search(r'http://', self.code) and not re.search(r'https://', self.code):
            security_issues.append("⚠️  建议使用HTTPS而不是HTTP")

        return security_issues

    def validate_best_practices(self) -> List[str]:
        """最佳实践验证"""
        practice_issues = []

        # 检查异常处理
        if not re.search(r'try\s*\{.*\}\s*catch', self.code, re.DOTALL):
            practice_issues.append("⚠️  缺少异常处理")

        # 检查日志记录
        if not re.search(r'log\.(info|debug|error|warn)', self.code):
            practice_issues.append("⚠️  缺少日志记录")

        # 检查常量定义
        if not re.search(r'private static final String', self.code):
            practice_issues.append("⚠️  建议使用常量定义状态码和配置")

        # 检查参数验证
        if not re.search(r'(StringUtils\.isEmpty|Objects\.isNull|@Valid)', self.code):
            practice_issues.append("⚠️  建议添加参数验证")

        # 检查重复代码
        if re.search(r'@SuppressWarnings\("DuplicatedCode"\)', self.code):
            practice_issues.append("💡 检测到重复代码警告，考虑重构")

        return practice_issues

    def validate_structure(self) -> List[str]:
        """代码结构验证"""
        structure_issues = []

        # 检查类注解
        if not re.search(r'@Service\s*\n\s*@RequiredArgsConstructor', self.code):
            structure_issues.append("⚠️  缺少Spring注解")

        # 检查接口实现
        if not re.search(r'implements\s+(RechargeHandler|WithdrawHandler)', self.code):
            structure_issues.append("⚠️  应该实现RechargeHandler或WithdrawHandler接口")

        # 检查必要方法
        required_methods = ['getConfig']
        for method in required_methods:
            if not re.search(f'public PaymentConfig {method}\\s*\\(', self.code):
                structure_issues.append(f"⚠️  缺少必要方法: {method}")

        # 检查PaymentConfig配置
        if not re.search(r'PaymentConfig\.builder\(\)', self.code):
            structure_issues.append("⚠️  缺少PaymentConfig配置")

        return structure_issues

    def validate_documentation(self) -> List[str]:
        """文档验证"""
        doc_issues = []

        # 检查类注释
        if not re.search(r'/\*\*.*?\*/\s*@(Service|Slf4j)', self.code, re.DOTALL):
            doc_issues.append("⚠️  缺少类级别的JavaDoc注释")

        # 检查方法注释
        methods = re.findall(r'public\s+\w+.*?\{', self.code)
        if len(methods) > 5:  # 如果方法超过5个，应该有注释
            if not re.search(r'/\*\*.*?\*/\s*public', self.code, re.DOTALL):
                doc_issues.append("⚠️  建议为公共方法添加JavaDoc注释")

        return doc_issues

    def generate_suggestions(self) -> List[str]:
        """生成改进建议"""
        suggestions = []

        # 性能建议
        if re.search(r'new\s+HashMap\s*\\(\\)', self.code):
            suggestions.append("💡 考虑使用Map.of()创建不可变Map")

        # 代码质量建议
        if not re.search(r'@Override', self.code):
            suggestions.append("💡 建议在重写方法上使用@Override注解")

        # 测试建议
        suggestions.append("💡 建议编写单元测试，重点测试签名生成和回调处理逻辑")

        # 监控建议
        if not re.search(r'(metrics|monitoring|@Timed|@Counted)', self.code, re.IGNORECASE):
            suggestions.append("💡 考虑添加性能监控和业务指标")

        return suggestions

    def run_validation(self) -> Tuple[List[str], List[str]]:
        """运行完整验证"""
        if not self.load_code():
            return self.issues, []

        # 执行各项检查
        self.issues.extend(self.validate_security())
        self.issues.extend(self.validate_best_practices())
        self.issues.extend(self.validate_structure())
        self.issues.extend(self.validate_documentation())

        self.suggestions = self.generate_suggestions()

        return self.issues, self.suggestions

    def print_report(self):
        """打印验证报告"""
        print(f"\n🔍 支付渠道处理类验证报告")
        print(f"📁 文件: {self.filepath}")
        print(f"📏 代码行数: {len(self.code.splitlines())}")
        print("=" * 50)

        if not self.issues and not self.suggestions:
            print("✅ 未发现问题，代码质量良好！")
            return

        if self.issues:
            print(f"\n⚠️  发现 {len(self.issues)} 个问题:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")

        if self.suggestions:
            print(f"\n💡 {len(self.suggestions)} 个改进建议:")
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"  {i}. {suggestion}")

        # 评估等级
        issue_count = len(self.issues)
        if issue_count == 0:
            grade = "A"
        elif issue_count <= 2:
            grade = "B"
        elif issue_count <= 5:
            grade = "C"
        else:
            grade = "D"

        print(f"\n📊 代码质量评级: {grade}")

def main():
    parser = argparse.ArgumentParser(description='验证支付渠道处理类代码质量')
    parser.add_argument('--file', required=True, help='要验证的Java文件路径')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        return

    validator = PaymentHandlerValidator(args.file)
    issues, suggestions = validator.run_validation()

    if args.format == 'json':
        import json
        report = {
            "file": args.file,
            "issues": issues,
            "suggestions": suggestions,
            "issue_count": len(issues),
            "suggestion_count": len(suggestions)
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        validator.print_report()

if __name__ == "__main__":
    main()