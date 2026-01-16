# Chrome DevTools MCP 工具参考

本文档提供 Chrome DevTools MCP 服务器的完整工具参考。

## 目录

1. [页面管理](#页面管理)
2. [页面交互](#页面交互)
3. [内容获取](#内容获取)
4. [高级操作](#高级操作)
5. [性能分析](#性能分析)
6. [网络分析](#网络分析)
7. [控制台日志](#控制台日志)

---

## 页面管理

### `list_pages` - 列出所有标签页
列出浏览器中打开的所有页面。

**参数**: 无

**返回**: 页面列表，包含索引和标题

**示例**:
```
用户: "列出当前所有标签页"
调用: list_pages
```

---

### `new_page` - 打开新标签页
创建一个新标签页并导航到指定 URL。

**参数**:
- `url` (required): 目标 URL
- `timeout` (optional): 超时时间（毫秒）

**示例**:
```
用户: "打开 GitHub"
调用: new_page(url="https://github.com")
```

---

### `select_page` - 选择标签页
选择指定索引的页面作为后续操作的上下文。

**参数**:
- `pageIdx` (required): 页面索引
- `bringToFront` (optional): 是否将页面带到前台

**示例**:
```
用户: "切换到第二个标签页"
调用: select_page(pageIdx=1, bringToFront=true)
```

---

### `close_page` - 关闭标签页
关闭指定索引的页面（最后一个页面无法关闭）。

**参数**:
- `pageIdx` (required): 页面索引

**示例**:
```
用户: "关闭第三个标签页"
调用: close_page(pageIdx=2)
```

---

### `navigate_page` - 页面导航
导航到指定 URL 或在历史记录中前进/后退。

**参数**:
- `type` (required): 导航类型 (url/back/forward/reload)
- `url` (optional): 目标 URL（仅 type=url 时）
- `ignoreCache` (optional): 是否忽略缓存（仅 type=reload 时）
- `timeout` (optional): 超时时间（毫秒）

**示例**:
```
用户: "刷新页面"
调用: navigate_page(type="reload", ignoreCache=true)

用户: "返回上一页"
调用: navigate_page(type="back")
```

---

## 页面交互

### `click` - 点击元素
点击指定元素。

**参数**:
- `uid` (required): 页面快照中的元素唯一标识符
- `dblClick` (optional): 是否双击（默认 false）

**示例**:
```
用户: "点击登录按钮"
调用: take_snapshot -> click(uid="button-123")
```

---

### `fill` - 填写表单
在输入框、文本区域或下拉选择中输入文本。

**参数**:
- `uid` (required): 页面快照中的元素唯一标识符
- `value` (required): 要填入的值

**示例**:
```
用户: "在搜索框输入 'Chrome DevTools'"
调用: fill(uid="input-456", value="Chrome DevTools")
```

---

### `fill_form` - 批量填写表单
一次性填写多个表单元素。

**参数**:
- `elements` (required): 元素数组，每个包含 `uid` 和 `value`

**示例**:
```json
{
  "elements": [
    {"uid": "input-1", "value": "用户名"},
    {"uid": "input-2", "value": "密码"}
  ]
}
```

---

### `hover` - 悬停元素
鼠标悬停在指定元素上。

**参数**:
- `uid` (required): 页面快照中的元素唯一标识符

---

### `drag` - 拖拽元素
将一个元素拖拽到另一个元素上。

**参数**:
- `from_uid` (required): 要拖拽的元素
- `to_uid` (required): 放置目标元素

---

### `press_key` - 按键
按下键盘按键或组合键。

**参数**:
- `key` (required): 按键或组合键（如 "Enter", "Control+A"）

**示例**:
```
用户: "按 Ctrl+A 全选"
调用: press_key(key="Control+A")

用户: "按回车键"
调用: press_key(key="Enter")
```

---

## 内容获取

### `take_snapshot` - 获取页面快照
基于可访问性树获取页面文本快照。优先使用此方法而非截图。

**参数**:
- `verbose` (optional): 是否包含所有可访问性信息（默认 false）
- `filePath` (optional): 保存快照的文件路径

**返回**: 页面元素列表，每个元素包含唯一标识符 (uid)

**重要**: 始终使用最新的快照。快照会显示在 DevTools Elements 面板中选中的元素（如果有）。

---

### `take_screenshot` - 截图
截取页面或特定元素的屏幕截图。

**参数**:
- `format` (optional): 图片格式 (png/jpeg/webp，默认 png)
- `quality` (optional): 压缩质量（JPEG/WebP，0-100）
- `uid` (optional): 元素唯一标识符（如省略则截取整个页面）
- `fullPage` (optional): 是否截取完整页面（与 uid 不兼容）
- `filePath` (optional): 保存截图的文件路径

**示例**:
```
用户: "给页面截图"
调用: take_screenshot(fullPage=true)

用户: "截取登录按钮"
调用: take_screenshot(uid="button-123")
```

---

### `evaluate_script` - 执行 JavaScript
在当前页面执行 JavaScript 函数。

**参数**:
- `function` (required): JavaScript 函数声明
- `args` (optional): 参数数组，每个参数包含 `uid`

**示例**:
```javascript
// 获取页面标题
function: "() => { return document.title }"

// 获取元素文本
function: "(el) => { return el.innerText }"
args: [{"uid": "element-123"}]
```

---

## 高级操作

### `upload_file` - 上传文件
通过文件输入元素上传文件。

**参数**:
- `uid` (required): 文件输入元素或会打开文件选择器的元素
- `filePath` (required): 本地文件路径

---

### `handle_dialog` - 处理对话框
处理浏览器对话框（alert、confirm、prompt）。

**参数**:
- `action` (required): "accept" 或 "dismiss"
- `promptText` (optional): prompt 对话框中输入的文本

---

### `wait_for` - 等待文本
等待指定文本出现在页面上。

**参数**:
- `text` (required): 要等待的文本
- `timeout` (optional): 最大等待时间（毫秒）

---

### `resize_page` - 调整页面大小
调整页面窗口尺寸。

**参数**:
- `width` (required): 页面宽度
- `height` (required): 页面高度

**示例**:
```
用户: "将窗口设置为 1920x1080"
调用: resize_page(width=1920, height=1080)
```

---

### `emulate` - 模拟设备特性
模拟网络条件、CPU 限制和地理位置。

**参数**:
- `networkConditions` (optional): 网络条件
  - "No emulation" / "Offline" / "Slow 3G" / "Fast 3G" / "Slow 4G" / "Fast 4G"
- `cpuThrottlingRate` (optional): CPU 降速倍率（1-20）
- `geolocation` (optional): 地理位置 {latitude, longitude}

**示例**:
```json
{
  "networkConditions": "Slow 3G",
  "cpuThrottlingRate": 4
}
```

---

## 性能分析

### `performance_start_trace` - 开始性能追踪
启动性能追踪以查找性能问题和优化点。报告 Core Web Vitals 分数。

**参数**:
- `reload` (required): 启动后是否自动重新加载页面
- `autoStop` (required): 是否自动停止追踪

---

### `performance_stop_trace` - 停止性能追踪
停止活动性能追踪并显示结果。

**参数**: 无

---

### `performance_analyze_insight` - 分析性能洞察
获取特定性能洞察集的详细信息。

**参数**:
- `insightSetId` (required): 洞察集 ID
- `insightName` (required): 洞察名称（如 "DocumentLatency", "LCPBreakdown"）

---

## 网络分析

### `list_network_requests` - 列出网络请求
列出自上次导航以来的所有网络请求。

**参数**:
- `pageSize` (optional): 返回的最大请求数
- `pageIdx` (optional): 页码（从 0 开始）
- `resourceTypes` (optional): 过滤的资源类型数组
  - "document", "stylesheet", "image", "media", "font", "script", "xhr", "fetch" 等
- `includePreservedRequests` (optional): 是否包含最近 3 次导航的请求

---

### `get_network_request` - 获取网络请求详情
获取特定网络请求的详细信息。

**参数**:
- `reqid` (optional): 请求 ID（如省略则返回 DevTools Network 面板中当前选中的请求）

---

## 控制台日志

### `list_console_messages` - 列出控制台消息
列出自上次导航以来的所有控制台消息。

**参数**:
- `pageSize` (optional): 返回的最大消息数
- `pageIdx` (optional): 页码（从 0 开始）
- `types` (optional): 过滤的消息类型数组
  - "log", "debug", "info", "error", "warn", "dir" 等
- `includePreservedMessages` (optional): 是否包含最近 3 次导航的消息

---

### `get_console_message` - 获取控制台消息详情
获取特定控制台消息的详细信息。

**参数**:
- `msgid` (required): 消息 ID

---

## 工作流程示例

### 典型的页面操作流程

1. **获取页面快照**
   ```
   take_snapshot()
   ```

2. **查找目标元素的 uid**
   从快照返回的元素列表中找到需要的元素

3. **执行操作**
   ```
   click(uid="button-123")
   // 或
   fill(uid="input-456", value="text")
   ```

4. **等待结果**
   ```
   wait_for(text="登录成功")
   ```

5. **验证结果**
   ```
   take_screenshot(fullPage=true)
   ```

---

## 最佳实践

1. **始终使用快照**: 使用 `take_snapshot()` 而非截图来获取页面结构
2. **等待元素**: 使用 `wait_for()` 确保元素已加载
3. **处理对话框**: 提前使用 `handle_dialog()` 处理可能的弹窗
4. **表单填写**: 使用 `fill_form()` 批量填写多个字段
5. **错误处理**: 检查 `list_console_messages()` 中的 JavaScript 错误
