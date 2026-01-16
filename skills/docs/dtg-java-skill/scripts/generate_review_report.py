#!/usr/bin/env python3
"""
智能代码审查报告生成脚本
为ai-coding-java插件的review命令生成详细的Markdown报告
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# 添加skills目录到Python路径
current_dir = Path(__file__).parent
skills_dir = current_dir.parent / "skills"
sys.path.insert(0, str(skills_dir))

try:
    from review_report_generation.report_engine import ReportEngine
    from review_report_generation.data_aggregator import ReviewDataAggregator
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装 jinja2 和 pyyaml 依赖:")
    print("pip install jinja2>=3.1.0 pyyaml>=6.0")
    sys.exit(1)


def load_review_data_from_file(data_file: str) -> Dict[str, Any]:
    """从文件加载审查数据"""
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            if data_file.endswith('.json'):
                return json.load(f)
            else:
                # 假设是文本文件，包含代理输出
                content = f.read()
                return {
                    "code_reviewer_output": content,
                    "architecture_analyzer_output": "",
                    "intelligent_diagnoser_output": "",
                    "quality_gate_output": ""
                }
    except Exception as e:
        print(f"❌ 加载数据文件失败: {e}")
        sys.exit(1)


def generate_report_from_outputs(code_reviewer_output: str,
                                architecture_analyzer_output: str = "",
                                intelligent_diagnoser_output: str = "",
                                quality_gate_output: str = "",
                                output_dir: str = "docs",
                                template_name: str = "comprehensive_review.md.j2") -> str:
    """从代理输出生成报告"""
    try:
        # 初始化报告引擎
        engine = ReportEngine()

        # 生成报告
        report_path = engine.generate_from_agent_outputs(
            code_reviewer_output=code_reviewer_output,
            architecture_analyzer_output=architecture_analyzer_output,
            intelligent_diagnoser_output=intelligent_diagnoser_output,
            quality_gate_output=quality_gate_output,
            output_dir=output_dir
        )

        return report_path

    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="生成AI智能代码审查报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 从标准输入生成报告
  echo "代码审查结果..." | python generate_review_report.py

  # 从文件生成报告
  python generate_review_report.py --input review_output.txt

  # 指定输出目录
  python generate_review_report.py --input review_output.txt --output-dir ./reports

  # 使用摘要模板
  python generate_review_report.py --input review_output.txt --template summary_report.md.j2

  # 完整参数示例
  python generate_review_report.py \\
    --code-reviewer-output code_reviewer.txt \\
    --architecture-output architecture.txt \\
    --diagnoser-output diagnoser.txt \\
    --quality-gate-output quality_gate.txt \\
    --output-dir ./docs
        """
    )

    # 输入参数
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        '--input', '-i',
        type=str,
        help='输入文件路径（JSON或文本格式）'
    )
    input_group.add_argument(
        '--stdin',
        action='store_true',
        help='从标准输入读取审查数据'
    )

    # 代理输出参数
    parser.add_argument(
        '--code-reviewer-output',
        type=str,
        help='code-reviewer代理输出文件路径'
    )
    parser.add_argument(
        '--architecture-output',
        type=str,
        help='architecture-analyzer代理输出文件路径'
    )
    parser.add_argument(
        '--diagnoser-output',
        type=str,
        help='intelligent-diagnoser代理输出文件路径'
    )
    parser.add_argument(
        '--quality-gate-output',
        type=str,
        help='质量门禁输出文件路径'
    )

    # 输出参数
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='docs',
        help='输出目录路径（默认: docs）'
    )
    parser.add_argument(
        '--template', '-t',
        type=str,
        default='comprehensive_review.md.j2',
        help='报告模板文件名（默认: comprehensive_review.md.j2）'
    )

    # 其他参数
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出信息'
    )
    parser.add_argument(
        '--list-templates',
        action='store_true',
        help='列出可用的报告模板'
    )

    args = parser.parse_args()

    # 列出模板
    if args.list_templates:
        try:
            engine = ReportEngine()
            templates = engine.get_available_templates()
            print("可用的报告模板:")
            for template in templates:
                print(f"  - {template}")
            return
        except Exception as e:
            print(f"❌ 获取模板列表失败: {e}")
            sys.exit(1)

    # 验证输出目录
    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ 创建输出目录失败: {e}")
        sys.exit(1)

    # 验证模板
    if args.template:
        try:
            engine = ReportEngine()
            if not engine.validate_template(args.template):
                print(f"❌ 无效的模板文件: {args.template}")
                sys.exit(1)
        except Exception as e:
            if args.verbose:
                print(f"⚠️ 模板验证警告: {e}")

    # 获取审查数据
    code_reviewer_output = ""
    architecture_analyzer_output = ""
    intelligent_diagnoser_output = ""
    quality_gate_output = ""

    # 从单独文件加载
    if args.code_reviewer_output:
        try:
            with open(args.code_reviewer_output, 'r', encoding='utf-8') as f:
                code_reviewer_output = f.read()
        except Exception as e:
            print(f"❌ 读取code-reviewer输出文件失败: {e}")
            sys.exit(1)

    if args.architecture_output:
        try:
            with open(args.architecture_output, 'r', encoding='utf-8') as f:
                architecture_analyzer_output = f.read()
        except Exception as e:
            if args.verbose:
                print(f"⚠️ 读取architecture输出文件失败: {e}")

    if args.diagnoser_output:
        try:
            with open(args.diagnoser_output, 'r', encoding='utf-8') as f:
                intelligent_diagnoser_output = f.read()
        except Exception as e:
            if args.verbose:
                print(f"⚠️ 读取diagnoser输出文件失败: {e}")

    if args.quality_gate_output:
        try:
            with open(args.quality_gate_output, 'r', encoding='utf-8') as f:
                quality_gate_output = f.read()
        except Exception as e:
            if args.verbose:
                print(f"⚠️ 读取quality-gate输出文件失败: {e}")

    # 从输入文件加载
    if args.input:
        data = load_review_data_from_file(args.input)
        if isinstance(data, dict) and "code_reviewer_output" in data:
            code_reviewer_output = data.get("code_reviewer_output", "")
            architecture_analyzer_output = data.get("architecture_analyzer_output", "")
            intelligent_diagnoser_output = data.get("intelligent_diagnoser_output", "")
            quality_gate_output = data.get("quality_gate_output", "")
        else:
            code_reviewer_output = str(data)

    # 从标准输入读取
    elif args.stdin:
        try:
            code_reviewer_output = sys.stdin.read()
        except Exception as e:
            print(f"❌ 读取标准输入失败: {e}")
            sys.exit(1)

    # 检查是否有输入数据
    if not code_reviewer_output.strip():
        print("❌ 没有找到审查数据")
        print("请使用 --input 参数指定文件，或使用 --stdin 从标准输入读取")
        sys.exit(1)

    # 生成报告
    if args.verbose:
        print("🔍 开始生成代码审查报告...")
        print(f"📁 输出目录: {output_dir}")
        print(f"📄 模板: {args.template}")
        print(f"📊 输入数据长度: {len(code_reviewer_output)} 字符")

    try:
        report_path = generate_report_from_outputs(
            code_reviewer_output=code_reviewer_output,
            architecture_analyzer_output=architecture_analyzer_output,
            intelligent_diagnoser_output=intelligent_diagnoser_output,
            quality_gate_output=quality_gate_output,
            output_dir=str(output_dir),
            template_name=args.template
        )

        print(f"✅ 报告生成成功!")
        print(f"📄 报告文件: {report_path}")

        # 显示文件大小
        file_size = Path(report_path).stat().st_size
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"

        print(f"📊 文件大小: {size_str}")

        # 如果是详细模式，显示报告摘要
        if args.verbose:
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    print(f"📏 报告行数: {len(lines)}")

                    # 提取总体评分
                    import re
                    score_match = re.search(r'总体评分[：:]\s*([A-F])\s*\(([^)]+)\)', content)
                    if score_match:
                        print(f"🎯 总体评分: {score_match.group(1)} 级 ({score_match.group(2)})")

                    # 提取问题数量
                    issue_matches = re.findall(r'(🔴|🟡|🟢)\s*[^\\n]*?\((\d+)\s*个?\)', content)
                    for emoji, count in issue_matches:
                        print(f"   {emoji} {count} 个问题")

            except Exception as e:
                if args.verbose:
                    print(f"⚠️ 读取报告摘要失败: {e}")

    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()