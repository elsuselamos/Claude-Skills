#!/usr/bin/env bash
#
# dtg-pay 项目检测脚本
#
# 功能：检测当前目录是否为 dtg-pay 项目
# 输出：JSON 格式的检测结果
#

set -euo pipefail

# 获取脚本所在目录的父目录（插件根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 检测函数
detect_dtg_pay() {
    local current_dir="${1:-$(pwd)}"
    local detected=false
    local detection_reason=""

    # 1. 检查当前目录名称
    local dir_name=$(basename "$current_dir")
    if [[ "$dir_name" == *"dtg-pay"* ]] || [[ "$dir_name" == "xxpay"* ]]; then
        detected=true
        detection_reason="目录名称匹配: $dir_name"
    fi

    # 2. 检查 pom.xml 是否包含 Spring Boot 和 Dubbo
    if [ "$detected" = false ] && [ -f "$current_dir/pom.xml" ]; then
        if grep -q "spring-boot-starter-parent" "$current_dir/pom.xml" && \
           grep -q "dubbo-spring-boot-starter" "$current_dir/pom.xml"; then
            detected=true
            detection_reason="检测到 Spring Boot + Dubbo 配置"
        fi
    fi

    # 3. 检查父目录
    if [ "$detected" = false ]; then
        local parent_dir=$(dirname "$current_dir")
        local parent_name=$(basename "$parent_dir")
        if [[ "$parent_name" == *"dtg-pay"* ]] || [[ "$parent_name" == "xxpay"* ]]; then
            detected=true
            detection_reason="父目录名称匹配: $parent_name"
        fi
    fi

    # 4. 检查是否存在 dtg-pay 特征模块目录
    if [ "$detected" = false ] && [ -d "$current_dir" ]; then
        if [ -d "$current_dir/xxpay-pay" ] || \
           [ -d "$current_dir/xxpay-gateway" ] || \
           [ -d "$current_dir/xxpay-shop" ]; then
            detected=true
            detection_reason="检测到 dtg-pay 特征模块目录"
        fi
    fi

    # 输出 JSON 结果
    if [ "$detected" = true ]; then
        cat <<EOF
{
  "detected": true,
  "project_path": "$current_dir",
  "reason": "$detection_reason",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
        return 0
    else
        cat <<EOF
{
  "detected": false,
  "project_path": "$current_dir",
  "reason": "未检测到 dtg-pay 项目特征",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
        return 1
    fi
}

# 主程序
main() {
    if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
        echo "用法: $0 [项目目录路径]"
        echo ""
        echo "检测指定目录是否为 dtg-pay 项目"
        echo "默认检测当前工作目录"
        echo ""
        echo "检测标准："
        echo "  1. 目录名称包含 'dtg-pay' 或 'xxpay'"
        echo "  2. pom.xml 包含 Spring Boot 和 Dubbo 依赖"
        echo "  3. 父目录名称匹配"
        echo "  4. 包含 dtg-pay 特征模块目录"
        echo ""
        echo "返回值："
        echo "  0 - 检测到 dtg-pay 项目"
        echo "  1 - 未检测到"
        exit 0
    fi

    detect_dtg_pay "${1:-$(pwd)}"
}

main "$@"
