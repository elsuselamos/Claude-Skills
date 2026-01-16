# 斜線命令

> 在互動式工作階段中使用斜線命令控制 Claude 的行為。

## 內建斜線命令

| 命令                        | 用途                                                                       |
| :------------------------ | :----------------------------------------------------------------------- |
| `/add-dir`                | 新增其他工作目錄                                                                 |
| `/agents`                 | 管理用於專門任務的自訂 AI 子代理                                                       |
| `/bashes`                 | 列出並管理背景工作                                                                |
| `/bug`                    | 回報錯誤（將對話傳送至 Anthropic）                                                   |
| `/clear`                  | 清除對話歷史                                                                   |
| `/compact [instructions]` | 壓縮對話並可選擇性地提供焦點指示                                                         |
| `/config`                 | 開啟設定介面（設定標籤）                                                             |
| `/context`                | 將目前的上下文使用情況視覺化為彩色網格                                                      |
| `/cost`                   | 顯示權杖使用統計資料（請參閱[成本追蹤指南](/zh-TW/costs#using-the-cost-command)以了解訂閱特定的詳細資訊） |
| `/doctor`                 | 檢查您的 Claude Code 安裝的健康狀況                                                 |
| `/exit`                   | 結束 REPL                                                                  |
| `/export [filename]`      | 將目前的對話匯出到檔案或剪貼簿                                                          |
| `/help`                   | 取得使用說明                                                                   |
| `/hooks`                  | 管理工具事件的掛鉤配置                                                              |
| `/init`                   | 使用 CLAUDE.md 指南初始化專案                                                     |
| `/login`                  | 切換 Anthropic 帳戶                                                          |
| `/logout`                 | 登出您的 Anthropic 帳戶                                                        |
| `/mcp`                    | 管理 MCP 伺服器連線和 OAuth 驗證                                                   |
| `/memory`                 | 編輯 CLAUDE.md 記憶檔案                                                        |
| `/model`                  | 選擇或變更 AI 模型                                                              |
| `/output-style [style]`   | 直接設定輸出樣式或從選擇功能表中選擇                                                       |
| `/permissions`            | 檢視或更新[權限](/zh-TW/iam#configuring-permissions)                            |
| `/pr_comments`            | 檢視提取請求註解                                                                 |
| `/privacy-settings`       | 檢視並更新您的隱私設定                                                              |
| `/review`                 | 要求程式碼審查                                                                  |
| `/sandbox`                | 啟用具有檔案系統和網路隔離的沙箱 bash 工具，以實現更安全、更自主的執行                                   |
| `/rewind`                 | 倒帶對話和/或程式碼                                                               |
| `/status`                 | 開啟設定介面（狀態標籤），顯示版本、模型、帳戶和連線狀態                                             |
| `/statusline`             | 設定 Claude Code 的狀態列 UI                                                   |
| `/terminal-setup`         | 安裝 Shift+Enter 按鍵繫結以換行（僅限 iTerm2 和 VSCode）                               |
| `/todos`                  | 列出目前的待辦事項                                                                |
| `/usage`                  | 顯示方案使用限制和速率限制狀態（僅限訂閱方案）                                                  |
| `/vim`                    | 進入 vim 模式以交替插入和命令模式                                                      |

## 自訂斜線命令

自訂斜線命令可讓您將常用的提示定義為 Markdown 檔案，Claude Code 可以執行這些檔案。命令按範圍（專案特定或個人）組織，並透過目錄結構支援命名空間。

### 語法

```
/<command-name> [arguments]
```

#### 參數

| 參數               | 說明                                 |
| :--------------- | :--------------------------------- |
| `<command-name>` | 衍生自 Markdown 檔案名稱（不含 `.md` 副檔名）的名稱 |
| `[arguments]`    | 傳遞至命令的選擇性引數                        |

### 命令類型

#### 專案命令

儲存在您的儲存庫中並與您的團隊共享的命令。在 `/help` 中列出時，這些命令在其說明後會顯示「(project)」。

**位置**：`.claude/commands/`

在下列範例中，我們建立 `/optimize` 命令：

```bash  theme={null}
# 建立專案命令
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
```

#### 個人命令

可在您所有專案中使用的命令。在 `/help` 中列出時，這些命令在其說明後會顯示「(user)」。

**位置**：`~/.claude/commands/`

在下列範例中，我們建立 `/security-review` 命令：

```bash  theme={null}
# 建立個人命令
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

### 功能

#### 命名空間

在子目錄中組織命令。子目錄用於組織，並出現在命令說明中，但不會影響命令名稱本身。說明將顯示命令是來自專案目錄（`.claude/commands`）還是使用者層級目錄（`~/.claude/commands`），以及子目錄名稱。

不支援使用者和專案層級命令之間的衝突。否則，多個具有相同基本檔案名稱的命令可以共存。

例如，位於 `.claude/commands/frontend/component.md` 的檔案會建立命令 `/component`，說明顯示「(project:frontend)」。
同時，位於 `~/.claude/commands/component.md` 的檔案會建立命令 `/component`，說明顯示「(user)」。

#### 引數

使用引數預留位置將動態值傳遞至命令：

##### 使用 `$ARGUMENTS` 的所有引數

`$ARGUMENTS` 預留位置會擷取傳遞至命令的所有引數：

```bash  theme={null}
# 命令定義
echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md

# 使用方式
> /fix-issue 123 high-priority
# $ARGUMENTS 變成：「123 high-priority」
```

##### 使用 `$1`、`$2` 等的個別引數

使用位置參數（類似於 shell 指令碼）個別存取特定引數：

```bash  theme={null}
# 命令定義  
echo 'Review PR #$1 with priority $2 and assign to $3' > .claude/commands/review-pr.md

# 使用方式
> /review-pr 456 high alice
# $1 變成「456」，$2 變成「high」，$3 變成「alice」
```

在以下情況下使用位置引數：

* 在命令的不同部分中個別存取引數
* 為遺漏的引數提供預設值
* 使用特定參數角色建立更結構化的命令

#### Bash 命令執行

使用 `!` 前置詞在斜線命令執行前執行 bash 命令。輸出包含在命令上下文中。您\_必須\_包含 `allowed-tools` 和 `Bash` 工具，但您可以選擇允許的特定 bash 命令。

例如：

```markdown  theme={null}
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

#### 檔案參考

使用 `@` 前置詞在命令中包含檔案內容以[參考檔案](/zh-TW/common-workflows#reference-files-and-directories)。

例如：

```markdown  theme={null}
# Reference a specific file

Review the implementation in @src/utils/helpers.js

# Reference multiple files

Compare @src/old-version.js with @src/new-version.js
```

#### 思考模式

斜線命令可以透過包含[延伸思考關鍵字](/zh-TW/common-workflows#use-extended-thinking)來觸發延伸思考。

### Frontmatter

命令檔案支援 frontmatter，用於指定有關命令的中繼資料：

| Frontmatter                | 用途                                                                                       | 預設值       |
| :------------------------- | :--------------------------------------------------------------------------------------- | :-------- |
| `allowed-tools`            | 命令可以使用的工具清單                                                                              | 繼承自對話     |
| `argument-hint`            | 斜線命令預期的引數。範例：`argument-hint: add [tagId] \| remove [tagId] \| list`。此提示在自動完成斜線命令時向使用者顯示。 | 無         |
| `description`              | 命令的簡短說明                                                                                  | 使用提示中的第一行 |
| `model`                    | 特定的模型字串（請參閱[模型概觀](https://docs.claude.com/en/docs/about-claude/models/overview)）         | 繼承自對話     |
| `disable-model-invocation` | 是否防止 `SlashCommand` 工具呼叫此命令                                                              | false     |

例如：

```markdown  theme={null}
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---

Create a git commit with message: $ARGUMENTS
```

使用位置引數的範例：

```markdown  theme={null}
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

## 外掛程式命令

[外掛程式](/zh-TW/plugins)可以提供與 Claude Code 無縫整合的自訂斜線命令。外掛程式命令的運作方式完全像使用者定義的命令，但透過[外掛程式市集](/zh-TW/plugin-marketplaces)分發。

### 外掛程式命令的運作方式

外掛程式命令具有以下特點：

* **命名空間**：命令可以使用 `/plugin-name:command-name` 格式以避免衝突（除非存在名稱衝突，否則外掛程式前置詞是選擇性的）
* **自動可用**：安裝並啟用外掛程式後，其命令會出現在 `/help` 中
* **完全整合**：支援所有命令功能（引數、frontmatter、bash 執行、檔案參考）

### 外掛程式命令結構

**位置**：外掛程式根目錄中的 `commands/` 目錄

**檔案格式**：具有 frontmatter 的 Markdown 檔案

**基本命令結構**：

```markdown  theme={null}
---
description: Brief description of what the command does
---

# Command Name

Detailed instructions for Claude on how to execute this command.
Include specific guidance on parameters, expected outcomes, and any special considerations.
```

**進階命令功能**：

* **引數**：在命令說明中使用 `{arg1}` 之類的預留位置
* **子目錄**：在子目錄中組織命令以進行命名空間
* **Bash 整合**：命令可以執行 shell 指令碼和程式
* **檔案參考**：命令可以參考和修改專案檔案

### 呼叫模式

```shell 直接命令（無衝突時） theme={null}
/command-name
```

```shell 外掛程式前置詞（需要消除歧義時） theme={null}
/plugin-name:command-name
```

```shell 使用引數（如果命令支援） theme={null}
/command-name arg1 arg2
```

## MCP 斜線命令

MCP 伺服器可以將提示公開為斜線命令，這些命令在 Claude Code 中變為可用。這些命令是從連接的 MCP 伺服器動態發現的。

### 命令格式

MCP 命令遵循以下模式：

```
/mcp__<server-name>__<prompt-name> [arguments]
```

### 功能

#### 動態發現

MCP 命令在以下情況下自動可用：

* MCP 伺服器已連接並處於活動狀態
* 伺服器透過 MCP 協定公開提示
* 在連接期間成功擷取提示

#### 引數

MCP 提示可以接受伺服器定義的引數：

```
# 無引數
> /mcp__github__list_prs

# 使用引數
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug title" high
```

#### 命名慣例

* 伺服器和提示名稱已正規化
* 空格和特殊字元變成底線
* 名稱已轉換為小寫以保持一致性

### 管理 MCP 連線

使用 `/mcp` 命令來：

* 檢視所有已設定的 MCP 伺服器
* 檢查連線狀態
* 使用啟用 OAuth 的伺服器進行驗證
* 清除驗證權杖
* 檢視來自每個伺服器的可用工具和提示

### MCP 權限和萬用字元

設定 [MCP 工具的權限](/zh-TW/iam#tool-specific-permission-rules)時，請注意**不支援萬用字元**：

* ✅ **正確**：`mcp__github`（核准來自 github 伺服器的所有工具）
* ✅ **正確**：`mcp__github__get_issue`（核准特定工具）
* ❌ **不正確**：`mcp__github__*`（不支援萬用字元）

若要核准來自 MCP 伺服器的所有工具，只需使用伺服器名稱：`mcp__servername`。若要僅核准特定工具，請個別列出每個工具。

## `SlashCommand` 工具

`SlashCommand` 工具允許 Claude 在對話期間以程式設計方式執行[自訂斜線命令](/zh-TW/slash-commands#custom-slash-commands)。這使 Claude 能夠在適當時機代表您呼叫自訂命令。

若要鼓勵 Claude 觸發 `SlashCommand` 工具，您的指示（提示、CLAUDE.md 等）通常需要使用斜線參考命令名稱。

範例：

```
> Run /write-unit-test when you are about to start writing tests.
```

此工具將每個可用自訂斜線命令的中繼資料放入上下文中，直到達到字元預算限制。您可以使用 `/context` 監視權杖使用情況，並按照以下操作管理上下文。

### `SlashCommand` 工具支援的命令

`SlashCommand` 工具僅支援以下自訂斜線命令：

* 是使用者定義的。內建命令（如 `/compact` 和 `/init`）\_不\_受支援。
* 已填入 `description` frontmatter 欄位。我們在上下文中使用 `description`。

對於 Claude Code 版本 >= 1.0.124，您可以透過執行 `claude --debug` 並觸發查詢來查看 `SlashCommand` 工具可以呼叫的自訂斜線命令。

### 停用 `SlashCommand` 工具

若要防止 Claude 透過工具執行任何斜線命令：

```bash  theme={null}
/permissions
# 新增至拒絕規則：SlashCommand
```

這也會從上下文中移除 SlashCommand 工具（和斜線命令說明）。

### 僅停用特定命令

若要防止特定斜線命令變為可用，請在斜線命令的 frontmatter 中新增 `disable-model-invocation: true`。

這也會從上下文中移除命令的中繼資料。

### `SlashCommand` 權限規則

權限規則支援：

* **完全符合**：`SlashCommand:/commit`（僅允許不帶引數的 `/commit`）
* **前置詞符合**：`SlashCommand:/review-pr:*`（允許 `/review-pr` 帶任何引數）

### 字元預算限制

`SlashCommand` 工具包含字元預算以限制向 Claude 顯示的命令說明的大小。這可防止在許多命令可用時發生權杖溢位。

預算包括每個自訂斜線命令的名稱、引數和說明。

* **預設限制**：15,000 個字元
* **自訂限制**：透過 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 環境變數設定

當超過字元預算時，Claude 將只看到可用命令的子集。在 `/context` 中，警告將顯示「M of N commands」。

## 技能與斜線命令

**斜線命令**和**代理技能**在 Claude Code 中有不同的用途：

### 使用斜線命令來

**快速、經常使用的提示**：

* 您經常使用的簡單提示片段
* 快速提醒或範本
* 適合在一個檔案中的經常使用的指示

**範例**：

* `/review` → 「審查此程式碼以查找錯誤並建議改進」
* `/explain` → 「用簡單的術語解釋此程式碼」
* `/optimize` → 「分析此程式碼以查找效能問題」

### 使用技能來

**具有結構的綜合功能**：

* 具有多個步驟的複雜工作流程
* 需要指令碼或公用程式的功能
* 跨多個檔案組織的知識
* 您想要標準化的團隊工作流程

**範例**：

* 具有表單填充指令碼和驗證的 PDF 處理技能
* 具有不同資料類型參考文件的資料分析技能
* 具有樣式指南和範本的文件技能

### 主要差異

| 方面      | 斜線命令             | 代理技能                |
| ------- | ---------------- | ------------------- |
| **複雜性** | 簡單提示             | 複雜功能                |
| **結構**  | 單一 .md 檔案        | 具有 SKILL.md + 資源的目錄 |
| **發現**  | 明確呼叫（`/command`） | 自動（基於上下文）           |
| **檔案**  | 僅一個檔案            | 多個檔案、指令碼、範本         |
| **範圍**  | 專案或個人            | 專案或個人               |
| **共享**  | 透過 git           | 透過 git              |

### 範例比較

**作為斜線命令**：

```markdown  theme={null}
# .claude/commands/review.md
Review this code for:
- Security vulnerabilities
- Performance issues
- Code style violations
```

使用方式：`/review`（手動呼叫）

**作為技能**：

```
.claude/skills/code-review/
├── SKILL.md (overview and workflows)
├── SECURITY.md (security checklist)
├── PERFORMANCE.md (performance patterns)
├── STYLE.md (style guide reference)
└── scripts/
    └── run-linters.sh
```

使用方式：「您可以審查此程式碼嗎？」（自動發現）

技能提供更豐富的上下文、驗證指令碼和組織的參考資料。

### 何時使用各個

**使用斜線命令**：

* 您重複呼叫相同的提示
* 提示適合在單一檔案中
* 您想要明確控制何時執行

**使用技能**：

* Claude 應該自動發現功能
* 需要多個檔案或指令碼
* 具有驗證步驟的複雜工作流程
* 團隊需要標準化、詳細的指導

斜線命令和技能可以共存。使用適合您需求的方法。

深入瞭解[代理技能](/zh-TW/skills)。

## 另請參閱

* [外掛程式](/zh-TW/plugins) - 透過外掛程式使用自訂命令擴展 Claude Code
* [身分識別和存取管理](/zh-TW/iam) - 權限完整指南，包括 MCP 工具權限
* [互動模式](/zh-TW/interactive-mode) - 快捷鍵、輸入模式和互動功能
* [CLI 參考](/zh-TW/cli-reference) - 命令列旗標和選項
* [設定](/zh-TW/settings) - 設定選項
* [記憶體管理](/zh-TW/memory) - 跨工作階段管理 Claude 的記憶體


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt

