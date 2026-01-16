---
name: dtg-chrome-skill
description: |
  Chrome DevTools MCP integration for browser automation with persistent user configuration.
  Use when user requests: (1) Launch Chrome in debug mode with user data,
  (2) Browser automation operations (click, fill, hover, drag, screenshot),
  (3) Page content analysis or scraping, (4) Web application testing or debugging,
  (5) Check browser status or manage tabs
---

# dtg-chrome-skill

Chrome DevTools MCP integration for browser automation with persistent user configuration.

## Core Features

- **One-click Launch**: Start Chrome in debug mode with user data (preserves login state, bookmarks)
- **Automation**: Click, type, drag, screenshot and other browser operations
- **Content Extraction**: Page snapshots, screenshots, console logs, network requests
- **Precise Control**: A11y tree-based element targeting with form filling and file upload support

## Quick Start

### 1. Launch Debug Mode Chrome

```bash
# Grant execute permission (first time only)
chmod +x scripts/launch-connected-chrome.sh

# Launch Chrome (closes existing instances and reopens)
./scripts/launch-connected-chrome.sh
```

The script will:
- Close currently running Chrome instances
- Launch Chrome in debug mode (port 9222)
- Preserve all user data (login state, bookmarks, extensions)

### 2. Verify Connection

```bash
./scripts/validate-chrome.sh
```

Verification items:
- Port 9222 availability
- HTTP connection status
- Chrome process status
- MCP configuration check

### 3. Use in Claude Desktop

After launching Chrome, control the browser using natural language in Claude Desktop:

```
"List all current tabs"
"Take a screenshot of the page"
"Click the login button"
"Type 'Chrome DevTools' in the search box"
```

## Workflows

### Typical Page Operations

1. **Get Page Snapshot** (required to obtain element uids)
   ```
   User: "Show me what's on the page"
   Call: take_snapshot()
   ```

2. **Perform Action** (using uid from snapshot)
   ```
   User: "Click the submit button"
   Call: click(uid="button-123")
   ```

3. **Wait and Verify**
   ```
   User: "Wait for loading to complete"
   Call: wait_for(text="Operation successful")
   ```

### Form Filling

```
User: "Fill in the login form, username admin, password 123456"
```

Recommended to use `fill_form` for batch filling:
```json
{
  "elements": [
    {"uid": "input-username", "value": "admin"},
    {"uid": "input-password", "value": "123456"}
  ]
}
```

### Page Navigation

```
User: "Open GitHub and search for Chrome DevTools"
```

Execution flow:
1. `navigate_page(url="https://github.com")`
2. `take_snapshot()` to find search box
3. `fill(uid="search-input", value="Chrome DevTools")`
4. `press_key(key="Enter")`

## MCP Configuration

Configuration file: `scripts/config.json`

Add to Claude Desktop configuration:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222"
      ]
    }
  }
}
```

Configuration path: `~/Library/Application Support/Claude/claude_desktop_config.json`

## Important Notes

- **Do not manually open regular Chrome windows**: Debug mode uses the default profile, manually opening normal windows may disconnect debugging
- **Proper shutdown**: Fully quit Chrome when done, then launch normally to restore
- **Port conflicts**: If port 9222 is occupied, modify the PORT variable in the script

## Troubleshooting

### Chrome Won't Start
```bash
# Check for residual processes
pkill -9 "Google Chrome"
# Re-run launch script
./scripts/launch-connected-chrome.sh
```

### MCP Connection Failed
```bash
# Run validation script to check status
./scripts/validate-chrome.sh
```

### Cannot Find Elements
- Ensure `take_snapshot()` is called first to get latest page structure
- Use uid returned from snapshot, don't guess manually
- Check if element is in iframe (need to switch context first)

## Resources

### scripts/

- **launch-connected-chrome.sh**: Launch debug mode Chrome (with user data)
- **validate-chrome.sh**: Validate Chrome DevTools MCP connection status

### references/

- **mcp-tools.md**: Complete MCP tool reference documentation
  - Page management tools (list_pages, new_page, select_page, etc.)
  - Interaction tools (click, fill, hover, drag, etc.)
  - Content retrieval (take_snapshot, take_screenshot)
  - Advanced operations (upload_file, handle_dialog, emulate)
  - Performance analysis and network monitoring

View full tool documentation: `references/mcp-tools.md`
