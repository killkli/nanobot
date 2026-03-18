# Nanobot Memory System — 開發者文件

> 適用版本：目前 `main` 分支
> 核心檔案：`nanobot/agent/memory.py`、`nanobot/agent/context.py`、`nanobot/session/manager.py`

---

## 1. 系統概覽

Nanobot 的記憶系統解決一個核心矛盾：**LLM 的 context window 有限，但對話可以無限延伸**。

解法是「雙層記憶 + 游標整合」：

```
對話歷史（短期）                      記憶檔案（長期）
session.messages[]                    workspace/memory/
  [0] user: ...                         MEMORY.md  ← 結構化事實，LLM 覆寫
  [1] assistant: ...                    HISTORY.md ← 時間戳日誌，Append-only
  [2] user: ...
  ── last_consolidated = 3 ──
  [3] user: ...   ← 未整合，送給 LLM
  [4] assistant: ...
  [5] user: ...（當前）
```

---

## 2. 核心元件

### 2.1 MemoryStore（`memory.py:75`）

底層 I/O 層，管理兩個檔案：

| 檔案 | 格式 | 寫入方式 | 用途 |
|------|------|----------|------|
| `MEMORY.md` | Markdown | LLM 全量覆寫 | 長期結構化事實（偏好、背景、關係等） |
| `HISTORY.md` | 純文字 | Append-only | 時間戳事件日誌，支援 grep 搜尋 |

**關鍵方法：**

```python
MemoryStore.consolidate(messages, provider, model) -> bool
```

整合流程：
1. 讀取當前完整 `MEMORY.md`
2. 組合 prompt：`current_memory + formatted_messages`
3. 以 `forced tool_choice = save_memory` 呼叫 LLM
4. LLM 返回 `history_entry`（時間戳摘要）+ `memory_update`（完整 MEMORY.md）
5. `history_entry` → append 到 `HISTORY.md`
6. `memory_update` → 若與現有內容不同則覆寫 `MEMORY.md`

**降級機制（`_fail_or_raw_archive`）：**

```
LLM 整合失敗次數 < 3  →  返回 False（保留 chunk，下輪重試）
LLM 整合失敗次數 >= 3 →  _raw_archive()：直接 dump 原始訊息到 HISTORY.md
                          重置計數器，返回 True
```

### 2.2 MemoryConsolidator（`memory.py:222`）

上層策略層，管理「何時整合、整合哪些、如何鎖定」。

**建構函數依賴：**

```python
MemoryConsolidator(
    workspace,
    provider,               # LLMProvider：執行整合 LLM 呼叫
    model,                  # 整合使用的模型
    sessions,               # SessionManager：持久化游標
    context_window_tokens,  # 模型 context window 大小（預設 65,536）
    build_messages,         # ContextBuilder.build_messages（用於 token 估算）
    get_tool_definitions,   # ToolRegistry.get_definitions（用於 token 估算）
)
```

**並發鎖（`get_lock`）：**

```python
self._locks: weakref.WeakValueDictionary[str, asyncio.Lock]
```

使用 `WeakValueDictionary` 管理 per-session `asyncio.Lock`：
- 同一 session 的並發整合請求會序列化
- 無對話的 session 的鎖自動被 GC 回收，不洩漏記憶體

### 2.3 Session 游標（`session/manager.py:17`）

```python
@dataclass
class Session:
    messages: list[dict]  # Append-only，永不縮減
    last_consolidated: int = 0  # 已整合到檔案的訊息索引
```

**設計原則：`messages` 只增不減**

這保留了 LLM prompt caching 的效率——相同前綴的 token 序列可被快取。整合後只移動 `last_consolidated` 指針，`get_history()` 回傳 `messages[last_consolidated:]`。

---

## 3. Token 感知整合流程

### 3.1 觸發條件

```
maybe_consolidate_by_tokens(session)
  ├─ context_window_tokens <= 0 → 跳過（功能已停用）
  ├─ estimated < context_window_tokens → 空閒，不整合
  └─ estimated >= context_window_tokens → 進入整合循環
```

**目標**：將 prompt 壓縮至 `context_window_tokens // 2`（50%）以下，留出後續對話空間。

**最多執行 5 輪**（`_MAX_CONSOLIDATION_ROUNDS = 5`）。

### 3.2 Token 估算方式

```python
estimate_session_prompt_tokens(session):
  1. history = session.get_history(max_messages=0)  # 全部未整合訊息
  2. probe = build_messages(history, "[token-probe]", ...)
     # 包含完整 system prompt（MEMORY.md 在內）+ 對話歷史 + runtime ctx
  3. estimate_prompt_tokens_chain(provider, model, probe, tool_definitions)
     # 優先 provider 原生 API → tiktoken cl100k_base → len // 4
```

估算會計入 **system prompt 的完整內容**，包括 `MEMORY.md`。

### 3.3 整合邊界選取

```python
pick_consolidation_boundary(session, tokens_to_remove):
  - 從 last_consolidated 開始掃描
  - 只在 role == "user" 處設置邊界（保護 tool_call/tool_result 配對）
  - 累加 token 數，找到足以移除 tokens_to_remove 的最小安全位置
  - 返回 (boundary_idx, removed_tokens)
```

### 3.4 整合執行序列

```
session.messages[last_consolidated:end_idx]  ← chunk
         ↓
MemoryStore.consolidate(chunk)
         ↓ 成功
session.last_consolidated = end_idx
sessions.save(session)          ← 持久化游標
         ↓
重新估算 token，繼續下一輪
```

---

## 4. 記憶讀取路徑（注入 System Prompt）

每次 LLM 呼叫都重建 system prompt，組成如下：

```
build_system_prompt()
  1. 核心身份（OS / workspace / 行為準則）
  2. Bootstrap 文件（AGENTS.md, SOUL.md, USER.md, TOOLS.md）
  3. ← get_memory_context() → "## Long-term Memory\n{MEMORY.md 全文}"
  4. Always-on 技能內容（always=true 的 SKILL.md）
  5. 技能目錄摘要
```

**MEMORY.md 的全文被無條件注入每一次 LLM 呼叫的 system prompt，沒有大小限制。**

---

## 5. 整合觸發時機（`loop.py`）

| 觸發點 | 時機 | 執行模式 |
|--------|------|----------|
| L.370 | 系統訊息處理前 | 前景（同步等待） |
| L.383 | 系統訊息處理後 | 背景（非阻塞） |
| **L.417** | **主訊息 LLM 呼叫前** | **前景（同步等待）← 最關鍵** |
| L.449 | 主訊息回覆後 | 背景（非阻塞） |
| L.402 | `/new` 指令清除 session | 背景（強制歸檔快照） |

---

## 6. 完整資料流圖

```
InboundMessage
  │
  ▼
AgentLoop._process_message()
  │
  ├─ [前景] maybe_consolidate_by_tokens(session)
  │     ├─ 估算 token（含 MEMORY.md）
  │     ├─ 若 >= context_window → pick_boundary → consolidate → 更新游標
  │     └─ 最多 5 輪
  │
  ├─ context.build_messages(session.get_history(), ...)
  │     └─ build_system_prompt()
  │           └─ MemoryStore.get_memory_context() → 讀取 MEMORY.md
  │
  ├─ provider.chat_with_retry(messages)   ← LLM 呼叫
  │
  ├─ _save_turn(session, new_messages)    ← 寫入 session.messages
  ├─ sessions.save(session)
  │
  └─ [背景] maybe_consolidate_by_tokens(session)
```

---

## 7. 設定選項

| 設定欄位 | 型別 | 預設值 | 說明 |
|----------|------|--------|------|
| `context_window_tokens` | `int` | `65536` | 觸發整合的 token 上限 |
| `memory_window` | `int` | — | **已棄用**，保留向後相容 |

整合使用的 model 與 provider 繼承自 agent 主設定（`AgentDefaults.model`）。

---

## 8. MEMORY.md 膨脹問題分析

> ⚠️ **結論：存在可導致對話完全失效的膨脹風險，且系統缺乏自動緩解機制。**

### 8.1 膨脹的根本原因

整合 prompt 的設計直接導致 `MEMORY.md` 只增不減：

```python
# memory.py:38（_SAVE_MEMORY_TOOL 定義）
"memory_update": {
    "description": "Full updated long-term memory as markdown. "
                   "Include all existing facts plus new ones. "  # ← 明確要求保留舊內容
                   "Return unchanged if nothing new.",
}
```

每次整合，LLM 被要求把「現有所有事實 + 新事實」全部寫回 `MEMORY.md`。這是設計上的 **累積語義（accumulation semantics）**，沒有任何自動刪減邏輯。

### 8.2 膨脹的惡性循環

```
對話產生新事實
    │
    ▼
consolidate() 呼叫 LLM：
  prompt = current_memory（N tokens）+ chunk（M tokens）
    │
    ▼
LLM 返回 memory_update：
  = current_memory（N tokens）+ 新增事實（ΔN tokens）
    │
    ▼
MEMORY.md 大小 = N + ΔN  ← 只會增長
    │
    ▼
下次 build_system_prompt() 注入 N+ΔN tokens
下次 consolidate() prompt 包含 N+ΔN tokens（比這次更大）
```

### 8.3 三個失效場景

#### 場景一：慢性劣化

長期使用者的 `MEMORY.md` 逐漸膨脹至數千 token。每次對話的基礎 token 消耗持續上升，可用的對話歷史空間隨之縮小。
**症狀**：整合越來越頻繁，系統需要更多時間在對話前等待整合完成。

#### 場景二：整合加速膨脹

整合本身的 prompt 把完整 `MEMORY.md` 傳給 LLM：

```python
# memory.py:125
prompt = f"""...
## Current Long-term Memory
{current_memory or "(empty)"}     ← 整個 MEMORY.md

## Conversation to Process
{self._format_messages(messages)}"""
```

當 `MEMORY.md` 已有 20,000 tokens，每次整合 LLM 呼叫的 input 就已有 20,000+ tokens，**整合操作本身消耗的 context 遠超過它試圖釋放的空間**。

#### 場景三：完全失效（最嚴重）

假設 `context_window_tokens = 65,536`：

```
MEMORY.md 大小 = 40,000 tokens
系統提示其他部分 ≈ 5,000 tokens
基礎佔用 ≈ 45,000 tokens（僅 system prompt）

觸發條件：estimated >= 65,536
→ 整合觸發
→ pick_consolidation_boundary：找對話歷史的邊界
→ 但對話歷史是 0（全部已整合）
→ boundary = None → 直接 return，什麼都沒做

結果：每次對話開始，bot 已使用 45,000 / 65,536 = 69% 的 context window
      僅剩 20,000 tokens 可用於當前對話
      整合永遠無法幫助，因為問題來源是 MEMORY.md，不是對話歷史
```

### 8.4 無法自救的根因

整合機制的設計假設是：**膨脹來自對話歷史，整合可以將其壓縮**。

但 `MEMORY.md` 膨脹後，整合機制完全無效：

| 問題來源 | 整合能否解決 |
|----------|-------------|
| 對話歷史過長 | ✅ 可以（移動游標，壓縮歷史） |
| MEMORY.md 過大 | ❌ 不行（整合只讀 MEMORY.md，從不刪減它） |

`pick_consolidation_boundary` 只掃描 `session.messages`，與 `MEMORY.md` 大小無關。即便整合成功將歷史全部歸檔（`last_consolidated = len(messages)`），system prompt 中的 `MEMORY.md` 仍然原封不動。

### 8.5 現有的部分緩解

目前唯一相關的緩解是使用者手動執行 `/new`（清除 session），但這只重置對話歷史，**不清理 `MEMORY.md`**。

---

## 9. HISTORY.md 深度分析

### 9.1 定位與設計意圖

`HISTORY.md` 是記憶系統的「冷儲存層」，與 `MEMORY.md` 的關係如下：

| 維度 | MEMORY.md | HISTORY.md |
|------|-----------|------------|
| 內容性質 | 結構化長期事實 | 時間序列事件日誌 |
| 注入方式 | **自動注入** system prompt（每次呼叫） | **不注入**，需 agent 主動讀取 |
| 寫入方式 | LLM 全量覆寫 | Append-only，永不修改舊內容 |
| 存取成本 | 高（每次 LLM 呼叫都消耗 token） | 低（靜態，僅工具呼叫時才消耗） |
| 增長特性 | 緩慢增長（LLM 會合併重複事實） | 持續線性增長，無上限 |

### 9.2 寫入路徑

HISTORY.md 有兩條寫入路徑，對應正常與降級狀態：

**路徑一：正常整合（`consolidate()` 成功）**

```python
# memory.py:189
self.append_history(entry)   # entry 來自 LLM 輸出的 history_entry 欄位
```

LLM 在整合時被要求生成：
```
"A paragraph summarizing key events/decisions/topics.
 Start with [YYYY-MM-DD HH:MM]. Include detail useful for grep search."
```

範例輸出：
```
[2026-03-18 14:30] User asked to set up Slack integration for workspace foo.
Discussed OAuth token storage, decided to use environment variables.
Bot confirmed channel #alerts as notification target.
```

**路徑二：降級歸檔（`_raw_archive()`，連續失敗 ≥ 3 次）**

```python
# memory.py:212-216
ts = datetime.now().strftime("%Y-%m-%d %H:%M")
self.append_history(
    f"[{ts}] [RAW] {len(messages)} messages\n"
    f"{self._format_messages(messages)}"
)
```

`_format_messages` 的輸出格式：
```
[2026-03-18 14:30] USER: 請幫我設定 Slack 整合
[2026-03-18 14:31] ASSISTANT [tools: read_file, write_file]: 好的，我來讀取設定檔...
[2026-03-18 14:32] ASSISTANT: 已完成設定
```

`[RAW]` 條目比 LLM 摘要**大數倍**（保留原始對話全文）。

### 9.3 HISTORY.md 不被注入 System Prompt 的設計

`context.py` 的 `build_system_prompt()` 只注入 MEMORY.md：

```python
# context.py:35-37
memory = self.memory.get_memory_context()  # 讀 MEMORY.md
if memory:
    parts.append(f"# Memory\n\n{memory}")
# HISTORY.md 完全不出現在這裡
```

但 `_get_identity()` 在 system prompt 中告知 agent HISTORY.md 的位置和用法：

```python
# context.py:85-86
f"- History log: {workspace_path}/memory/HISTORY.md "
f"(grep-searchable). Each entry starts with [YYYY-MM-DD HH:MM]."
```

這是「工具導向存取（tool-mediated access）」設計：**agent 被告知 HISTORY.md 的存在，但必須主動呼叫 shell 工具（grep/read）才能取得內容**。這意味著存取是 opt-in 且按需的。

### 9.4 存取模式

Agent 存取 HISTORY.md 的預期方式：

```bash
# grep 搜尋特定事件
grep "Slack" /workspace/memory/HISTORY.md

# 查看最近條目
tail -50 /workspace/memory/HISTORY.md

# 全文讀取（危險，見下節）
cat /workspace/memory/HISTORY.md
```

這些操作透過 `shell` 工具執行，結果作為 tool result 回傳給 LLM。

### 9.5 HISTORY.md 的風險分析

#### 風險一：全文讀取爆炸

HISTORY.md 無上限增長。若 agent（或使用者）要求讀取全文：

```
使用 6 個月後，HISTORY.md = 500,000 tokens
agent 呼叫 read_file("memory/HISTORY.md")
→ tool result = 500,000 tokens 的原始文字
→ 這個 tool result 進入 messages[]
→ context window 立即爆滿
```

`_save_turn()` 對 tool result 有 16,000 字元的截斷（`loop.py`），但這只在**儲存到 session 時**生效。LLM 呼叫本身仍會收到完整的 tool result，可能導致 API 錯誤。

#### 風險二：[RAW] 條目加速膨脹

每當 LLM 連續失敗 3 次（網路問題、模型不支援 tool_choice 等），`_raw_archive` 就把原始對話全文 dump 進去。一次 `[RAW]` 條目的大小等於整合 chunk 的原始大小，可能遠超過正常 LLM 摘要。

```
正常條目：約 100-300 tokens（LLM 摘要段落）
[RAW] 條目：可能 2,000-10,000 tokens（原始對話全文）
```

#### 風險三：grep 結果無上限

`grep "常見關鍵字" HISTORY.md` 在大型 HISTORY.md 上可能匹配數百行，返回大量 token。目前沒有 grep 結果大小的限制或截斷。

#### 風險四：無任何清理機制

HISTORY.md 沒有：
- 自動輪替（log rotation）
- 大小上限
- 時間過期清理
- 壓縮或封存

**HISTORY.md 是永久單向增長的**，唯一清理方式是手動刪除檔案。

### 9.6 與 MEMORY.md 的風險等級比較

| 風險項目 | MEMORY.md | HISTORY.md |
|----------|-----------|------------|
| 自動注入 context（每次呼叫） | ✅ 是 → 高風險 | ❌ 否 → 低風險 |
| 增長速度 | 慢（LLM 合併重複） | 快（無限追加） |
| 最終大小上限 | 無，但受 LLM 摘要壓制 | 無，且無任何壓制 |
| 導致對話失效 | **直接**（系統提示膨脹） | **間接**（工具呼叫結果膨脹） |
| 使用者可見性 | 低（自動發生） | 高（需主動讀取才觸發） |

HISTORY.md 的問題不如 MEMORY.md 緊迫，但長期來看是一個**靜默的資源洩漏**：不會主動傷害對話，但當 agent 試圖回顧歷史時，可能引發 context 爆炸。

### 9.7 HISTORY.md 改進建議

#### 建議一：Log Rotation（低成本）

在 `append_history()` 後檢查檔案大小，超過閾值時封存舊條目：
```
HISTORY.md          ← 最近 90 天
HISTORY.2026-01.md  ← 封存的舊月份
```

#### 建議二：grep 工具結果截斷（低成本）

對 grep 工具的輸出加入行數/字元上限，避免單次工具呼叫回傳過多 token。

#### 建議三：加入條目計數元數據（低成本）

在 HISTORY.md 頭部維護一個元數據行（條目數、起始日期、最後更新日期），讓 agent 在決定是否讀取前先了解規模。

---

## 10. 建議改進方向

以下為開發者可考慮的修復方案，依複雜度排序：

### 方案一：MEMORY.md 大小上限警告（低成本）

在 `get_memory_context()` 或 `build_system_prompt()` 中加入大小檢查，當 `MEMORY.md` 超過閾值時記錄警告或向使用者提示。

### 方案二：MEMORY.md Token 計入整合觸發（中等成本）

目前 `maybe_consolidate_by_tokens` 已透過 `build_messages` 計入 MEMORY.md 的 token，所以估算是正確的。問題在於：整合只能縮減對話歷史，無法縮減 MEMORY.md。

需要新增獨立的「MEMORY.md 自整合」路徑：
```
若 MEMORY.md tokens > threshold:
    呼叫 LLM 執行 compress_memory(current_memory) → 濃縮版 MEMORY.md
    覆寫 MEMORY.md
```

### 方案三：MEMORY.md 分層架構（高成本，根本解）

將 MEMORY.md 拆為：
- `MEMORY_CORE.md`：最重要的常駐事實（大小上限 2,000 tokens）
- `MEMORY_EXTENDED.md`：完整事實庫（按主題索引，不全量注入 system prompt）

system prompt 只注入 `MEMORY_CORE.md`；agent 需要時透過工具讀取 `MEMORY_EXTENDED.md`。

### 方案四：整合 prompt 截斷 MEMORY.md（低成本，局部緩解）

在 `consolidate()` 的 prompt 中，若 `current_memory` 超過閾值，只傳入最近的 N tokens：

```python
if len(current_memory) > MAX_MEMORY_IN_PROMPT:
    current_memory = current_memory[-MAX_MEMORY_IN_PROMPT:]
```

可減輕場景二（整合加速膨脹），但無法解決場景三（根本失效）。
