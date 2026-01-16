#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LayuiAdmin 国际化 (i18n) 语言文件管理工具

功能：
1. validate - 验证多语言 JSON 文件的键一致性
2. generate - 生成新的语言文件模板
3. sync - 同步翻译键到所有语言文件
4. extract - 从 HTML 文件提取 i18ndata 键
"""

import json
import os
import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class I18nManager:
    """国际化语言文件管理器"""

    def __init__(self, base_dir: str = None):
        """
        初始化管理器

        Args:
            base_dir: 语言文件根目录，默认为当前目录的 language/ 文件夹
        """
        if base_dir is None:
            self.base_dir = Path.cwd()
        else:
            self.base_dir = Path(base_dir)

        self.language_dirs = {}
        self._find_language_dirs()

    def _find_language_dirs(self):
        """查找所有语言目录（如 en/, zh/, ja/）"""
        for item in self.base_dir.iterdir():
            if item.is_dir() and len(item.name) == 2:
                self.language_dirs[item.name] = item

        if not self.language_dirs:
            print(f"警告：在 {self.base_dir} 中未找到语言目录（如 en/, zh/）")

    def _load_json_file(self, file_path: Path) -> Dict:
        """加载 JSON 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"错误：{file_path} JSON 格式错误: {e}")
            return {}
        except Exception as e:
            print(f"错误：无法读取 {file_path}: {e}")
            return {}

    def _save_json_file(self, file_path: Path, data: Dict, indent: int = 2):
        """保存 JSON 文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            print(f"✅ 已保存: {file_path}")
        except Exception as e:
            print(f"错误：无法保存 {file_path}: {e}")

    def _get_all_keys(self, data: Dict, prefix: str = '') -> Set[str]:
        """递归获取 JSON 中的所有键（支持嵌套路径）"""
        keys = set()
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                keys.update(self._get_all_keys(value, full_key))
            else:
                keys.add(full_key)
        return keys

    def _get_nested_value(self, data: Dict, path: str) -> any:
        """根据点号分隔的路径获取嵌套值"""
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value

    def _set_nested_value(self, data: Dict, path: str, value: any):
        """根据点号分隔的路径设置嵌套值"""
        keys = path.split('.')
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def validate(self) -> bool:
        """
        验证所有语言文件的键一致性

        Returns:
            bool: 验证是否通过
        """
        if len(self.language_dirs) < 2:
            print("错误：至少需要两个语言目录进行比较")
            return False

        # 收集所有模块文件及其键
        module_files = defaultdict(lambda: defaultdict(set))
        all_modules = set()

        for lang, lang_dir in self.language_dirs.items():
            for json_file in lang_dir.glob("*.json"):
                module_name = json_file.stem
                all_modules.add(module_name)
                data = self._load_json_file(json_file)
                keys = self._get_all_keys(data)
                module_files[module_name][lang] = keys

        # 比较键的一致性
        all_valid = True
        for module in sorted(all_modules):
            print(f"\n📦 模块: {module}.json")

            # 获取基准语言（通常是第一个语言）
            base_lang = list(module_files[module].keys())[0]
            base_keys = module_files[module][base_lang]

            for lang, keys in module_files[module].items():
                if lang == base_lang:
                    print(f"  📌 {lang}: {len(keys)} 个键（基准）")
                    continue

                missing_in_lang = base_keys - keys
                extra_in_lang = keys - base_keys

                if missing_in_lang or extra_in_lang:
                    all_valid = False
                    print(f"  ⚠️  {lang}: {len(keys)} 个键")

                    if missing_in_lang:
                        print(f"     缺少 {len(missing_in_lang)} 个键:")
                        for key in sorted(missing_in_lang)[:5]:
                            print(f"       - {key}")
                        if len(missing_in_lang) > 5:
                            print(f"       ... 还有 {len(missing_in_lang) - 5} 个")

                    if extra_in_lang:
                        print(f"     多余 {len(extra_in_lang)} 个键:")
                        for key in sorted(extra_in_lang)[:5]:
                            print(f"       + {key}")
                        if len(extra_in_lang) > 5:
                            print(f"       ... 还有 {len(extra_in_lang) - 5} 个")
                else:
                    print(f"  ✅ {lang}: {len(keys)} 个键（一致）")

        return all_valid

    def generate_template(self, module_name: str, languages: List[str] = None,
                          keys: Dict[str, str] = None) -> bool:
        """
        生成新的语言文件模板

        Args:
            module_name: 模块名称（如 merchant, common）
            languages: 语言列表（如 ['en', 'zh']），默认使用所有已存在的语言
            keys: 键值对字典，键为翻译键路径，值为默认值

        Returns:
            bool: 是否成功
        """
        if languages is None:
            languages = list(self.language_dirs.keys())

        if not languages:
            print("错误：没有可用的语言目录")
            return False

        if keys is None:
            print("错误：必须提供键值对")
            return False

        # 构建嵌套结构的 JSON
        def build_nested(keys_dict):
            result = {}
            for path, value in keys_dict.items():
                self._set_nested_value(result, path, value)
            return result

        data = build_nested(keys)

        # 为每种语言生成文件
        for lang in languages:
            lang_dir = self.base_dir / lang
            if not lang_dir.exists():
                lang_dir.mkdir(parents=True, exist_ok=True)
                print(f"📁 已创建目录: {lang_dir}")

            file_path = lang_dir / f"{module_name}.json"

            # 如果文件已存在，合并而非覆盖
            if file_path.exists():
                existing_data = self._load_json_file(file_path)
                # 合并数据
                merged_data = existing_data.copy()
                for path, value in keys.items():
                    self._set_nested_value(merged_data, path, value)
                self._save_json_file(file_path, merged_data)
            else:
                self._save_json_file(file_path, data)

        print(f"\n✅ 已生成模块 '{module_name}' 的语言文件")
        return True

    def sync_keys(self, module_name: str, base_lang: str = 'zh',
                  dry_run: bool = False) -> bool:
        """
        同步翻译键：确保所有语言文件具有相同的键结构

        Args:
            module_name: 模块名称
            base_lang: 基准语言（默认 zh）
            dry_run: 预演模式，不实际修改文件

        Returns:
            bool: 是否成功
        """
        base_file = self.base_dir / base_lang / f"{module_name}.json"
        if not base_file.exists():
            print(f"错误：基准文件不存在: {base_file}")
            return False

        base_data = self._load_json_file(base_file)
        base_keys = self._get_all_keys(base_data)

        changes_made = False

        for lang, lang_dir in self.language_dirs.items():
            if lang == base_lang:
                continue

            lang_file = lang_dir / f"{module_name}.json"
            if not lang_file.exists():
                print(f"⚠️  {lang}/{module_name}.json 不存在，跳过")
                continue

            lang_data = self._load_json_file(lang_file)

            # 找出缺少的键
            missing_keys = []
            for key_path in base_keys:
                if self._get_nested_value(lang_data, key_path) is None:
                    missing_keys.append(key_path)

            if missing_keys:
                changes_made = True
                print(f"\n📝 {lang}/{module_name}.json 需要添加 {len(missing_keys)} 个键:")

                for key_path in missing_keys:
                    default_value = self._get_nested_value(base_data, key_path)
                    print(f"  + {key_path}: \"{default_value}\"")

                    if not dry_run:
                        self._set_nested_value(lang_data, key_path, f"[TODO: {default_value}]")

                if not dry_run:
                    self._save_json_file(lang_file, lang_data)
            else:
                print(f"✅ {lang}/{module_name}.json 已同步")

        if not changes_made:
            print("✅ 所有语言文件已同步")

        return True

    def extract_from_html(self, html_file: str, include_js: bool = True) -> List[Tuple[str, str]]:
        """
        从 HTML 文件中提取 i18ndata 属性和 translateMessageByPath 调用的翻译键

        Args:
            html_file: HTML 文件路径
            include_js: 是否提取 JavaScript 中的 translateMessageByPath 调用

        Returns:
            List[Tuple[str, str]]: (键路径, 默认文本) 列表
        """
        results = []
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 模式 1: i18ndata 属性
            # 匹配: i18ndata="module:key.path"默认文本</tag>
            i18ndata_pattern = r'i18ndata\s*=\s*["\']([^"\']+)["\'][^>]*>([^<]+)'
            matches = re.finditer(i18ndata_pattern, content)
            for match in matches:
                key_path = match.group(1)
                default_text = match.group(2).strip()
                results.append((key_path, default_text))

            # 模式 2: translateMessageByPath 函数调用
            # 匹配: translateMessageByPath("key", "default")
            if include_js:
                # 支持单引号和双引号
                js_pattern = r'translateMessageByPath\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
                js_matches = re.finditer(js_pattern, content)
                for match in js_matches:
                    key_path = match.group(1)
                    default_text = match.group(2)
                    # 避免重复添加
                    if not any(k[0] == key_path for k in results):
                        results.append((key_path, default_text))

        except Exception as e:
            print(f"错误：无法读取 {html_file}: {e}")

        return results

    def extract_from_dir(self, dir_path: str, pattern: str = "*.html") -> Dict[str, List[Tuple[str, str]]]:
        """
        从目录中的所有 HTML 文件提取翻译键

        Args:
            dir_path: 目录路径
            pattern: 文件匹配模式

        Returns:
            Dict: {文件名: [(键路径, 默认文本), ...]}
        """
        results = {}
        dir_path = Path(dir_path)

        for html_file in dir_path.rglob(pattern):
            relative_path = html_file.relative_to(dir_path)
            keys = self.extract_from_html(str(html_file))
            if keys:
                results[str(relative_path)] = keys

        return results


def main():
    parser = argparse.ArgumentParser(
        description='LayuiAdmin 国际化语言文件管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 验证语言文件一致性
  python i18n_manager.py validate --dir ./language

  # 生成新的模块模板
  python i18n_manager.py generate --module merchant --keys "page.title=页面标题" "button.save=保存"

  # 同步翻译键
  python i18n_manager.py sync --module merchant --base-lang zh

  # 从 HTML 提取翻译键
  python i18n_manager.py extract --file merchant-list.html

  # 从目录提取所有翻译键
  python i18n_manager.py extract --dir ./views --pattern "*.html"
        """
    )

    parser.add_argument('--dir', type=str, default='.',
                        help='语言文件根目录（默认：当前目录）')

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证语言文件键一致性')

    # generate 命令
    generate_parser = subparsers.add_parser('generate', help='生成新的语言文件模板')
    generate_parser.add_argument('--module', type=str, required=True,
                                 help='模块名称（如 merchant, common）')
    generate_parser.add_argument('--keys', type=str, nargs='+', required=True,
                                 help='键值对，格式: "path.key=value"（支持嵌套路径如 page.title）')
    generate_parser.add_argument('--languages', type=str, nargs='+',
                                 help='语言列表（如 en zh），默认使用所有已存在的语言')

    # sync 命令
    sync_parser = subparsers.add_parser('sync', help='同步翻译键到所有语言')
    sync_parser.add_argument('--module', type=str, required=True,
                             help='模块名称')
    sync_parser.add_argument('--base-lang', type=str, default='zh',
                             help='基准语言（默认: zh）')
    sync_parser.add_argument('--dry-run', action='store_true',
                             help='预演模式，不实际修改文件')

    # extract 命令
    extract_parser = subparsers.add_parser('extract', help='从 HTML 提取翻译键')
    extract_group = extract_parser.add_mutually_exclusive_group(required=True)
    extract_group.add_argument('--file', type=str, help='HTML 文件路径')
    extract_group.add_argument('--dir', type=str, help='HTML 文件目录')
    extract_parser.add_argument('--pattern', type=str, default='*.html',
                                help='文件匹配模式（默认: *.html）')
    extract_parser.add_argument('--output', type=str,
                                help='输出 JSON 文件路径（可选）')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    manager = I18nManager(args.dir)

    if args.command == 'validate':
        success = manager.validate()
        return 0 if success else 1

    elif args.command == 'generate':
        # 解析键值对
        keys = {}
        for key_value in args.keys:
            if '=' in key_value:
                key, value = key_value.split('=', 1)
                keys[key] = value
            else:
                print(f"警告：忽略无效的键值对: {key_value}")

        success = manager.generate_template(
            args.module,
            args.languages,
            keys
        )
        return 0 if success else 1

    elif args.command == 'sync':
        success = manager.sync_keys(
            args.module,
            args.base_lang,
            args.dry_run
        )
        return 0 if success else 1

    elif args.command == 'extract':
        if args.file:
            results = {args.file: manager.extract_from_html(args.file)}
        else:
            results = manager.extract_from_dir(args.dir, args.pattern)

        # 输出结果
        print("\n📋 提取的翻译键:\n")
        all_keys = {}

        for file_path, keys in results.items():
            print(f"📄 {file_path}:")
            for key_path, default_text in keys:
                print(f"  i18ndata=\"{key_path}\" → \"{default_text}\"")
                all_keys[key_path] = default_text
            print()

        # 保存到 JSON 文件
        if args.output:
            manager.base_dir = Path(args.output).parent
            module_name = Path(args.output).stem
            manager.generate_template(module_name, None, all_keys)

        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
