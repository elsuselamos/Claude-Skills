#!/bin/bash

# Chrome DevTools MCP 连接验证脚本
# 用于验证 Chrome 调试端口是否正常工作

# 配置区域
PORT=9222
MCP_URL="http://127.0.0.1:$PORT"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 正在验证 Chrome DevTools MCP 连接..."
echo ""

# 1. 检查端口是否开放
echo "1️⃣ 检查调试端口 $PORT..."
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} 端口 $PORT 已开放"
else
    echo -e "${RED}❌${NC} 端口 $PORT 未开放"
    echo ""
    echo "💡 解决方案:"
    echo "   运行: ./launch-connected-chrome.sh"
    exit 1
fi

# 2. 检查 HTTP 连接
echo ""
echo "2️⃣ 检查 HTTP 连接..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$MCP_URL/json" 2>/dev/null)
if [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}✅${NC} HTTP 连接正常 (状态码: $HTTP_STATUS)"
else
    echo -e "${RED}❌${NC} HTTP 连接失败 (状态码: $HTTP_STATUS)"
    exit 1
fi

# 3. 检查 Chrome 进程
echo ""
echo "3️⃣ 检查 Chrome 进程..."
if pgrep -f "Chrome.*remote-debugging-port=$PORT" >/dev/null; then
    echo -e "${GREEN}✅${NC} Chrome 调试进程运行中"
else
    echo -e "${YELLOW}⚠️${NC} 未找到调试模式的 Chrome 进程"
fi

# 4. 测试 JSON 端点
echo ""
echo "4️⃣ 测试 JSON 端点..."
TABS=$(curl -s "$MCP_URL/json" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ -n "$TABS" ]; then
    echo -e "${GREEN}✅${NC} JSON 端点响应正常 (检测到 $TABS 个标签页)"
else
    echo -e "${RED}❌${NC} JSON 端点响应异常"
    exit 1
fi

# 5. MCP 服务器配置检查
echo ""
echo "5️⃣ 检查 MCP 配置..."
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$CONFIG_FILE" ]; then
    if grep -q "chrome-devtools" "$CONFIG_FILE"; then
        if grep -q "$PORT" "$CONFIG_FILE"; then
            echo -e "${GREEN}✅${NC} MCP 配置正确"
        else
            echo -e "${YELLOW}⚠️${NC} MCP 配置存在但端口可能不匹配"
        fi
    else
        echo -e "${YELLOW}⚠️${NC} 未找到 chrome-devtools MCP 配置"
        echo ""
        echo "💡 需要添加配置到 $CONFIG_FILE:"
        cat scripts/config.json
    fi
else
    echo -e "${YELLOW}⚠️${NC} 未找到 Claude Desktop 配置文件"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Chrome DevTools MCP 连接验证通过${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "🎯 可以在 Claude Desktop 中使用以下命令:"
echo "   - \"列出当前 Chrome 标签页\""
echo "   - \"给页面截图\""
echo "   - \"点击页面元素\""
