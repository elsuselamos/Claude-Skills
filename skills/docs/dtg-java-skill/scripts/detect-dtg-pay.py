#!/usr/bin/env python3
"""
dtg-pay 项目检测脚本 (Python 版本)

功能：检测当前目录是否为 dtg-pay 项目
输出：JSON 格式的检测结果
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple
import re


def check_pom_features(pom_file: str) -> Tuple[bool, str, Dict[str, str]]:
    """
    检查 pom.xml 的特征

    Args:
        pom_file: pom.xml 文件路径

    Returns:
        (是否匹配, 检测原因, 版本信息字典)
    """
    try:
        with open(pom_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False, "", {}

    # 移除 XML 注释，避免匹配到注释中的内容
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # 检测 Spring Boot 配置（多种方式）
    has_spring_boot_parent = "spring-boot-starter-parent" in content
    has_spring_boot_dependencies = "spring-boot-dependencies" in content
    has_spring_boot_starter = "spring-boot-starter" in content

    # 检测 Dubbo 配置（多种方式）
    has_dubbo_starter = "dubbo-spring-boot-starter" in content
    has_dubbo_bom = "dubbo-bom" in content

    # 提取版本信息
    versions = {}

    spring_boot_version_match = re.search(r'<spring-boot\.version>([^<]+)</spring-boot\.version>', content)
    if spring_boot_version_match:
        versions['spring_boot'] = spring_boot_version_match.group(1).strip()

    dubbo_version_match = re.search(r'<dubbo\.version>([^<]+)</dubbo\.version>', content)
    if dubbo_version_match:
        versions['dubbo'] = dubbo_version_match.group(1).strip()

    java_version_match = re.search(r'<java\.version>([^<]+)</java\.version>', content)
    if java_version_match:
        versions['java'] = java_version_match.group(1).strip()

    # 多层次检测逻辑
    if has_spring_boot_parent and (has_dubbo_starter or has_dubbo_bom):
        return True, "检测到 Spring Boot (parent) + Dubbo 配置", versions

    if has_spring_boot_dependencies and (has_dubbo_starter or has_dubbo_bom):
        return True, "检测到 Spring Boot (dependencyManagement) + Dubbo 配置", versions

    if has_spring_boot_starter and (has_dubbo_starter or has_dubbo_bom):
        return True, "检测到 Spring Boot Starter + Dubbo 依赖", versions

    return False, "", versions


def detect_dtg_pay(project_path: str = None) -> Tuple[bool, str, Dict[str, str]]:
    """
    检测指定目录是否为 dtg-pay 项目

    Args:
        project_path: 要检测的项目路径，默认为当前工作目录

    Returns:
        (检测结果, 检测原因, 版本信息)
    """
    if project_path is None:
        project_path = os.getcwd()

    project_path = os.path.abspath(project_path)
    dir_name = os.path.basename(project_path)

    # 1. 检查根 pom.xml（增强版）
    pom_file = os.path.join(project_path, "pom.xml")
    if os.path.exists(pom_file):
        detected, reason, versions = check_pom_features(pom_file)
        if detected:
            return True, reason, versions

    # 2. 检查目录名称
    if "dtg-pay" in dir_name.lower() or "xxpay" in dir_name.lower():
        return True, f"目录名称匹配: {dir_name}", {}

    # 3. 检查父目录
    parent_dir = os.path.dirname(project_path)
    parent_name = os.path.basename(parent_dir)
    if "dtg-pay" in parent_name.lower() or "xxpay" in parent_name.lower():
        return True, f"父目录名称匹配: {parent_name}", {}

    # 4. 检查是否存在 dtg-pay 特征模块目录
    characteristic_modules = [
        "xxpay-pay",
        "xxpay-manage",
        "xxpay-service",
        "xxpay-core",
        "xxpay-merchant"
    ]

    for module in characteristic_modules:
        if os.path.exists(os.path.join(project_path, module)):
            return True, f"检测到特征模块: {module}", {}

    return False, "未检测到 dtg-pay 项目特征", {}


def main():
    """主程序"""
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("用法: python3 detect-dtg-pay.py [项目目录路径]")
        print("")
        print("检测指定目录是否为 dtg-pay 项目")
        print("默认检测当前工作目录")
        print("")
        print("检测标准：")
        print("  1. 目录名称包含 'dtg-pay' 或 'xxpay'")
        print("  2. pom.xml 包含 Spring Boot 和 Dubbo 依赖")
        print("  3. 父目录名称匹配")
        print("  4. 包含 dtg-pay 特征模块目录")
        print("")
        print("返回值：")
        print("  0 - 检测到 dtg-pay 项目")
        print("  1 - 未检测到")
        sys.exit(0)

    project_path = sys.argv[1] if len(sys.argv) > 1 else None
    detected, reason, versions = detect_dtg_pay(project_path)

    result = {
        "detected": detected,
        "project_path": os.path.abspath(project_path) if project_path else os.getcwd(),
        "reason": reason,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "versions": versions
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 新增：如果检测到项目，设置环境变量到 $CLAUDE_ENV_FILE
    if detected:
        env_file = os.environ.get("CLAUDE_ENV_FILE")
        if env_file:
            try:
                with open(env_file, 'a') as f:
                    f.write(f"export DTG_PAY_PROJECT=true\n")
                    f.write(f"export DTG_PAY_PATH='{result['project_path']}'\n")
                    if versions:
                        versions_json = json.dumps(versions).replace('"', '\\"')
                        f.write(f"export DTG_PAY_VERSIONS='{versions_json}'\n")
            except Exception as e:
                print(f"# Warning: Could not write to env file: {e}", file=sys.stderr)

    sys.exit(0 if detected else 1)


if __name__ == "__main__":
    main()
