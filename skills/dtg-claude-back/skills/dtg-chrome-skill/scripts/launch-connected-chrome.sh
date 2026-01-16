#!/bin/bash

# =================配置区域=================
# 设置调试端口 (Claude MCP 默认使用 9222)
PORT=9222

# 设置用户数据目录
# 注意：你原本的命令指向的是 Default 子目录。
# 通常 Chrome 的根数据目录是 ".../Google/Chrome"，Chrome 会自动在其中找 "Default"。
# 但为了严格遵循你的指令，保留你指定的路径。
# ⚠️ 警告：直接使用日常使用的 Default 目录作为调试目录，必须先彻底关闭当前 Chrome。
USER_DATA_DIR="$HOME/Library/Application Support/Google/Chrome/Default"

# 或者使用更安全的独立目录(推荐)，避免影响日常使用：
# USER_DATA_DIR="$HOME/.chrome-mcp-profile"
# =========================================

echo "🛑 正在关闭当前运行的 Google Chrome (必须步骤)..."
# 必须关闭现有实例，否则无法绑定调试端口
osascript -e 'tell application "Google Chrome" to quit' 2>/dev/null || true

# 等待进程完全结束
sleep 2

echo "🚀 正在启动“有记忆”的 Chrome (调试模式)..."
echo "📂 数据目录: $USER_DATA_DIR"
echo "🔌 调试端口: $PORT"

# 启动 Chrome
# 使用 open -a 方式，并传入参数
# --remote-debugging-port: 让 MCP 可以连接
# --no-first-run: 跳过欢迎页
open -a "Google Chrome" --args \
  --user-data-dir="$USER_DATA_DIR" \
  --remote-debugging-port=$PORT \
  --no-first-run \
  --no-default-browser-check

echo "✅ Chrome 已启动！"
echo "👉 现在打开 Claude Desktop，它应该能控制这个浏览器窗口了。"
echo "⚠️ 注意：在这个模式下关闭这个终端窗口不会关闭 Chrome。"