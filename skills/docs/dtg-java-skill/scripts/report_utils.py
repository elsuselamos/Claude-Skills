#!/usr/bin/env python3
"""
报告生成工具函数
提供报告生成的辅助功能和实用工具
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import subprocess


class ReportUtils:
    """报告生成工具类"""

    @staticmethod
    def find_latest_report(output_dir: str = "docs") -> Optional[str]:
        """查找最新的报告文件"""
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                return None

            # 查找所有报告文件
            report_files = list(output_path.glob("review-*.md"))
            if not report_files:
                return None

            # 按修改时间排序，返回最新的
            latest_file = max(report_files, key=lambda f: f.stat().st_mtime)
            return str(latest_file)

        except Exception:
            return None

    @staticmethod
    def get_report_history(output_dir: str = "docs", limit: int = 10) -> List[Dict[str, Any]]:
        """获取报告历史记录"""
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                return []

            report_files = list(output_path.glob("review-*.md"))
            report_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

            history = []
            for report_file in report_files[:limit]:
                stat = report_file.stat()
                history.append({
                    "path": str(report_file),
                    "name": report_file.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "created": datetime.fromtimestamp(stat.st_ctime)
                })

            return history

        except Exception:
            return []

    @staticmethod
    def extract_report_summary(report_path: str) -> Dict[str, Any]:
        """从报告文件中提取摘要信息"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()

            summary = {}

            # 提取总体评分
            score_match = re.search(r'总体评分[：:]\s*([A-F])\s*\(([^)]+)\)', content)
            if score_match:
                summary["overall_grade"] = score_match.group(1)
                summary["overall_score"] = score_match.group(2)

            # 提取健康度
            health_match = re.search(r'代码健康度[：:]\s*(\d+)', content)
            if health_match:
                summary["health_score"] = int(health_match.group(1))

            # 提取问题数量
            issue_stats = {}
            priority_patterns = [
                (r'🔴[^\\n]*?(\d+)\s*个', 'high'),
                (r'🟡[^\\n]*?(\d+)\s*个', 'medium'),
                (r'🟢[^\\n]*?(\d+)\s*个', 'low')
            ]

            for pattern, priority in priority_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    issue_stats[priority] = int(matches[0])

            summary["issue_counts"] = issue_stats

            # 提取文件数量
            files_match = re.search(r'分析文件数[：:]\s*(\d+)', content)
            if files_match:
                summary["files_analyzed"] = int(files_match.group(1))

            # 提取审查时间
            time_match = re.search(r'审查时间[：:]\s*([^\n]+)', content)
            if time_match:
                summary["review_time"] = time_match.group(1).strip()

            return summary

        except Exception:
            return {}

    @staticmethod
    def calculate_quality_trend(report_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算质量趋势"""
        if len(report_history) < 2:
            return {
                "trend": "insufficient_data",
                "score_change": 0,
                "health_change": 0,
                "issue_change": 0
            }

        # 提取最近的两个报告的摘要
        current_summary = ReportUtils.extract_report_summary(report_history[0]["path"])
        previous_summary = ReportUtils.extract_report_summary(report_history[1]["path"])

        # 计算变化
        trend_data = {
            "trend": "stable",
            "score_change": 0,
            "health_change": 0,
            "issue_change": 0
        }

        # 计算评分变化
        current_score = current_summary.get("overall_score", "0")
        previous_score = previous_summary.get("overall_score", "0")

        try:
            current_num = float(re.findall(r'\\d+\\.?\\d*', current_score)[0])
            previous_num = float(re.findall(r'\\d+\\.?\\d*', previous_score)[0])
            trend_data["score_change"] = current_num - previous_num
        except:
            pass

        # 计算健康度变化
        current_health = current_summary.get("health_score", 0)
        previous_health = previous_summary.get("health_score", 0)
        trend_data["health_change"] = current_health - previous_health

        # 计算问题数量变化
        current_issues = sum(current_summary.get("issue_counts", {}).values())
        previous_issues = sum(previous_summary.get("issue_counts", {}).values())
        trend_data["issue_change"] = current_issues - previous_issues

        # 确定趋势
        if trend_data["score_change"] > 5 or trend_data["health_change"] > 5:
            trend_data["trend"] = "improving"
        elif trend_data["score_change"] < -5 or trend_data["health_change"] < -5:
            trend_data["trend"] = "declining"
        else:
            trend_data["trend"] = "stable"

        return trend_data

    @staticmethod
    def clean_old_reports(output_dir: str = "docs", keep_count: int = 20) -> int:
        """清理旧报告文件，保留指定数量的最新报告"""
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                return 0

            report_files = list(output_path.glob("review-*.md"))
            if len(report_files) <= keep_count:
                return 0

            # 按修改时间排序
            report_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

            # 删除超出保留数量的文件
            files_to_delete = report_files[keep_count:]
            deleted_count = 0

            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception:
                    pass

            return deleted_count

        except Exception:
            return 0

    @staticmethod
    def get_report_statistics(output_dir: str = "docs") -> Dict[str, Any]:
        """获取报告统计信息"""
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                return {
                    "total_reports": 0,
                    "total_size": 0,
                    "latest_report": None,
                    "oldest_report": None
                }

            report_files = list(output_path.glob("review-*.md"))

            if not report_files:
                return {
                    "total_reports": 0,
                    "total_size": 0,
                    "latest_report": None,
                    "oldest_report": None
                }

            # 计算统计信息
            total_size = sum(f.stat().st_size for f in report_files)
            latest_file = max(report_files, key=lambda f: f.stat().st_mtime)
            oldest_file = min(report_files, key=lambda f: f.stat().st_mtime)

            return {
                "total_reports": len(report_files),
                "total_size": total_size,
                "latest_report": {
                    "path": str(latest_file),
                    "name": latest_file.name,
                    "modified": datetime.fromtimestamp(latest_file.stat().st_mtime)
                },
                "oldest_report": {
                    "path": str(oldest_file),
                    "name": oldest_file.name,
                    "modified": datetime.fromtimestamp(oldest_file.stat().st_mtime)
                }
            }

        except Exception:
            return {
                "total_reports": 0,
                "total_size": 0,
                "latest_report": None,
                "oldest_report": None
            }

    @staticmethod
    def validate_report_file(report_path: str) -> Dict[str, Any]:
        """验证报告文件的完整性"""
        try:
            report_path = Path(report_path)
            if not report_path.exists():
                return {
                    "valid": False,
                    "error": "文件不存在"
                }

            if not report_path.is_file():
                return {
                    "valid": False,
                    "error": "路径不是文件"
                }

            # 检查文件大小
            if report_path.stat().st_size == 0:
                return {
                    "valid": False,
                    "error": "文件为空"
                }

            # 检查文件内容
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                return {
                    "valid": False,
                    "error": "文件内容为空"
                }

            # 检查是否是Markdown报告
            required_headers = [
                "# 📋 AI 智能代码审查报告",
                "## 📊 审查概述",
                "## 🎯 智能质量评估"
            ]

            missing_headers = []
            for header in required_headers:
                if header not in content:
                    missing_headers.append(header)

            if missing_headers:
                return {
                    "valid": False,
                    "error": f"缺少必要的标题: {', '.join(missing_headers)}"
                }

            # 提取基本信息
            summary = ReportUtils.extract_report_summary(str(report_path))

            return {
                "valid": True,
                "summary": summary,
                "file_size": report_path.stat().st_size,
                "line_count": len(content.split('\n'))
            }

        except Exception as e:
            return {
                "valid": False,
                "error": f"验证失败: {str(e)}"
            }

    @staticmethod
    def open_report_in_editor(report_path: str, editor: Optional[str] = None) -> bool:
        """在编辑器中打开报告文件"""
        try:
            # 确定编辑器
            if editor:
                cmd = [editor, report_path]
            else:
                # 尝试使用系统默认编辑器
                editor = os.environ.get('EDITOR')
                if editor:
                    cmd = [editor, report_path]
                else:
                    # 根据操作系统选择默认编辑器
                    import platform
                    if platform.system() == 'Darwin':  # macOS
                        cmd = ['open', '-a', 'TextEdit', report_path]
                    elif platform.system() == 'Windows':
                        cmd = ['notepad', report_path]
                    else:  # Linux
                        cmd = ['xdg-open', report_path]

            # 执行命令
            subprocess.run(cmd, check=True)
            return True

        except Exception:
            return False

    @staticmethod
    def generate_report_index(output_dir: str = "docs") -> str:
        """生成报告索引文件"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            # 获取报告历史
            history = ReportUtils.get_report_history(output_dir)
            statistics = ReportUtils.get_report_statistics(output_dir)

            # 生成索引内容
            index_content = f"""# 代码审查报告索引

## 📊 统计信息

- **总报告数**: {statistics['total_reports']}
- **总大小**: {ReportUtils._format_size(statistics['total_size'])}
- **最新报告**: {statistics['latest_report']['name'] if statistics['latest_report'] else '无'}
- **最早报告**: {statistics['oldest_report']['name'] if statistics['oldest_report'] else '无'}

## 📋 报告历史

| 序号 | 报告名称 | 生成时间 | 文件大小 | 摘要 |
|------|----------|----------|----------|------|
"""

            for i, report in enumerate(history, 1):
                summary = ReportUtils.extract_report_summary(report["path"])
                grade = summary.get("overall_grade", "N/A")
                health = summary.get("health_score", "N/A")
                issues = sum(summary.get("issue_counts", {}).values())

                index_content += f"| {i} | [{report['name']}]({report['name']}) | {report['modified'].strftime('%Y-%m-%d %H:%M')} | {ReportUtils._format_size(report['size'])} | 评分: {grade} | 健康度: {health} | 问题数: {issues} |\n"

            index_content += f"""

---

*索引生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            # 写入索引文件
            index_path = output_path / "REPORT_INDEX.md"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)

            return str(index_path)

        except Exception:
            return ""

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"


def main():
    """命令行工具入口"""
    import argparse

    parser = argparse.ArgumentParser(description="报告生成工具")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # list命令
    list_parser = subparsers.add_parser('list', help='列出报告历史')
    list_parser.add_argument('--output-dir', '-o', default='docs', help='输出目录')
    list_parser.add_argument('--limit', '-l', type=int, default=10, help='显示数量限制')

    # latest命令
    latest_parser = subparsers.add_parser('latest', help='显示最新报告路径')
    latest_parser.add_argument('--output-dir', '-o', default='docs', help='输出目录')

    # stats命令
    stats_parser = subparsers.add_parser('stats', help='显示报告统计信息')
    stats_parser.add_argument('--output-dir', '-o', default='docs', help='输出目录')

    # clean命令
    clean_parser = subparsers.add_parser('clean', help='清理旧报告')
    clean_parser.add_argument('--output-dir', '-o', default='docs', help='输出目录')
    clean_parser.add_argument('--keep', '-k', type=int, default=20, help='保留数量')

    # validate命令
    validate_parser = subparsers.add_parser('validate', help='验证报告文件')
    validate_parser.add_argument('report_path', help='报告文件路径')

    # index命令
    index_parser = subparsers.add_parser('index', help='生成报告索引')
    index_parser.add_argument('--output-dir', '-o', default='docs', help='输出目录')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'list':
        history = ReportUtils.get_report_history(args.output_dir, args.limit)
        if history:
            print(f"报告历史 (最近{len(history)}个):")
            for i, report in enumerate(history, 1):
                summary = ReportUtils.extract_report_summary(report["path"])
                grade = summary.get("overall_grade", "N/A")
                health = summary.get("health_score", "N/A")
                print(f"{i:2d}. {report['name']} ({report['modified'].strftime('%Y-%m-%d %H:%M')}) - 评分:{grade} 健康度:{health}")
        else:
            print("未找到报告文件")

    elif args.command == 'latest':
        latest = ReportUtils.find_latest_report(args.output_dir)
        if latest:
            print(f"最新报告: {latest}")
        else:
            print("未找到报告文件")

    elif args.command == 'stats':
        stats = ReportUtils.get_report_statistics(args.output_dir)
        print(f"报告统计信息:")
        print(f"  总报告数: {stats['total_reports']}")
        print(f"  总大小: {ReportUtils._format_size(stats['total_size'])}")
        if stats['latest_report']:
            print(f"  最新报告: {stats['latest_report']['name']} ({stats['latest_report']['modified'].strftime('%Y-%m-%d %H:%M')})")

    elif args.command == 'clean':
        deleted = ReportUtils.clean_old_reports(args.output_dir, args.keep)
        print(f"已清理 {deleted} 个旧报告文件")

    elif args.command == 'validate':
        result = ReportUtils.validate_report_file(args.report_path)
        if result['valid']:
            print("✅ 报告文件有效")
            if 'summary' in result:
                summary = result['summary']
                print(f"  评分: {summary.get('overall_grade', 'N/A')}")
                print(f"  健康度: {summary.get('health_score', 'N/A')}")
                print(f"  文件大小: {ReportUtils._format_size(result['file_size'])}")
        else:
            print(f"❌ 报告文件无效: {result['error']}")

    elif args.command == 'index':
        index_path = ReportUtils.generate_report_index(args.output_dir)
        if index_path:
            print(f"✅ 报告索引已生成: {index_path}")
        else:
            print("❌ 生成报告索引失败")


if __name__ == "__main__":
    main()