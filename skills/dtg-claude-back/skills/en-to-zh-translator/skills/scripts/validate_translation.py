#!/usr/bin/env python3
"""
Translation validation script for English to Chinese technical translator skill.
This script helps validate that translations maintain technical integrity.
"""

import re
import sys
from typing import List, Dict, Any

class TranslationValidator:
    def __init__(self):
        self.issues: List[Dict[str, Any]] = []

    def validate_code_blocks(self, original: str, translation: str) -> None:
        """Validate that code blocks are preserved exactly."""
        # Extract code blocks from both texts
        original_blocks = re.findall(r'```(\w+)?\n(.*?)```', original, re.DOTALL)
        translation_blocks = re.findall(r'```(\w+)?\n(.*?)```', translation, re.DOTALL)

        if len(original_blocks) != len(translation_blocks):
            self.issues.append({
                'type': 'code_block_count',
                'message': f'Code block count mismatch: {len(original_blocks)} vs {len(translation_blocks)}'
            })

        for i, (orig_block, trans_block) in enumerate(zip(original_blocks, translation_blocks)):
            if orig_block != trans_block:
                self.issues.append({
                    'type': 'code_block_content',
                    'block_index': i,
                    'message': f'Code block {i+1} content differs'
                })

    def validate_inline_code(self, original: str, translation: str) -> None:
        """Validate that inline code is preserved."""
        original_inline = re.findall(r'`([^`]+)`', original)
        translation_inline = re.findall(r'`([^`]+)`', translation)

        if original_inline != translation_inline:
            self.issues.append({
                'type': 'inline_code',
                'message': f'Inline code mismatch: {original_inline} vs {translation_inline}'
            })

    def validate_math_expressions(self, original: str, translation: str) -> None:
        """Validate that LaTeX math expressions are preserved."""
        original_math = re.findall(r'\$([^$]+)\$', original)
        translation_math = re.findall(r'\$([^$]+)\$', translation)

        if original_math != translation_math:
            self.issues.append({
                'type': 'math_expressions',
                'message': f'Math expressions mismatch: {original_math} vs {translation_math}'
            })

    def validate_urls(self, original: str, translation: str) -> None:
        """Validate that URLs are preserved."""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        original_urls = re.findall(url_pattern, original)
        translation_urls = re.findall(url_pattern, translation)

        if original_urls != translation_urls:
            self.issues.append({
                'type': 'urls',
                'message': f'URL mismatch: {original_urls} vs {translation_urls}'
            })

    def validate_structure_preservation(self, original: str, translation: str) -> None:
        """Validate that markdown structure is preserved."""
        # Check heading levels
        original_headings = re.findall(r'^(#{1,6})\s', original, re.MULTILINE)
        translation_headings = re.findall(r'^(#{1,6})\s', translation, re.MULTILINE)

        if original_headings != translation_headings:
            self.issues.append({
                'type': 'headings',
                'message': f'Heading structure mismatch'
            })

        # Check list items
        original_lists = len(re.findall(r'^\s*[-*+]\s', original, re.MULTILINE))
        translation_lists = len(re.findall(r'^\s*[-*+]\s', translation, re.MULTILINE))

        if original_lists != translation_lists:
            self.issues.append({
                'type': 'lists',
                'message': f'List item count mismatch: {original_lists} vs {translation_lists}'
            })

    def validate_technical_terms(self, translation: str) -> None:
        """Check for common technical term preservation."""
        # Common technical terms that should be preserved
        technical_terms = [
            'API', 'JSON', 'XML', 'HTML', 'CSS', 'HTTP', 'REST', 'SQL',
            'Python', 'JavaScript', 'Rust', 'Java', 'Go', 'C++',
            'IDE', 'CLI', 'GUI', 'CI/CD', 'DevOps'
        ]

        for term in technical_terms:
            if term.lower() not in translation.lower() and term not in translation:
                self.issues.append({
                    'type': 'technical_term',
                    'term': term,
                    'message': f'Technical term "{term}" may have been incorrectly translated'
                })

    def validate(self, original: str, translation: str) -> bool:
        """Run all validation checks."""
        self.issues.clear()

        self.validate_code_blocks(original, translation)
        self.validate_inline_code(original, translation)
        self.validate_math_expressions(original, translation)
        self.validate_urls(original, translation)
        self.validate_structure_preservation(original, translation)
        self.validate_technical_terms(translation)

        return len(self.issues) == 0

    def print_report(self) -> None:
        """Print validation report."""
        if not self.issues:
            print("✅ 翻译验证通过！所有技术要素都正确保留。")
            return

        print("❌ 翻译验证发现问题：")
        print()

        for i, issue in enumerate(self.issues, 1):
            print(f"{i}. {issue['type'].upper()}: {issue['message']}")

        print()
        print("请检查并修正这些问题。")

def main():
    if len(sys.argv) != 3:
        print("用法: python validate_translation.py <original_file> <translation_file>")
        sys.exit(1)

    original_file = sys.argv[1]
    translation_file = sys.argv[2]

    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            original = f.read()

        with open(translation_file, 'r', encoding='utf-8') as f:
            translation = f.read()

        validator = TranslationValidator()
        is_valid = validator.validate(original, translation)

        validator.print_report()

        sys.exit(0 if is_valid else 1)

    except FileNotFoundError as e:
        print(f"错误: 找不到文件 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()