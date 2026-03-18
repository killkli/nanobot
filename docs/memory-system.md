# Nanobot 記憶系統開發者文件

> 適用分支: `main`
> 主要程式: `nanobot/agent/memory.py`、`nanobot/agent/context.py`、`nanobot/config/schema.py`

## 1. 概覽與改版動機

Nanobot 的記憶系統要同時解兩件事:

1. 對話可以很長
2. 每次 LLM 呼叫的 prompt 空間有限

這次改版的重點是把「常駐記憶注入」和「可選檢索記憶」拆開，避免長期把整份 `MEMORY.md` 無上限塞進 system prompt。

### 本版核心結論

- `MEMORY.md` 不再全文注入
- 核心記憶注入受 `max_core_chars` 限制
- mem0 檢索與索引是可選功能，且預設關閉
- 相關記憶來自 `mem0.search(query=..., user_id=..., limit=...)`
- token 估算探針 `[token-probe]` 不會觸發即時 mem0 檢索
- `HISTORY.md` 仍是 append-only 的歷史稽核軌跡
- consolidation 仍寫入 `HISTORY.md` 與 `MEMORY.md`
- 啟用 mem0 時，`history_entry` 會索引，`memory_update` 只有內容變更時才會以有上限摘錄索引

## 2. 舊架構與新架構對照

| 面向 | 舊行為 | 新行為 |
| --- | --- | --- |
| `MEMORY.md` 注入 | 全文注入 | 以 `max_core_chars` 截斷後注入 |
| 相關記憶來源 | 無明確可選檢索層 | 可選 mem0 檢索，預設關閉 |
| 相關記憶觸發 | 不適用 | `get_memory_context(query, include_relevant=True)` 時，才會走 mem0 |
| token probe 行為 | 可能觸發一般注入流程 | `[token-probe]` 明確關閉 relevant memory 查詢 |
| consolidation 檔案寫入 | `HISTORY.md` append、`MEMORY.md` 覆寫 | 行為維持一致 |
| consolidation 後索引 | 無 | 啟用 mem0 時 best-effort 索引 |

### 為什麼要改

舊模式長期把大體積記憶直接放入 prompt，會讓每輪對話的固定成本變高。新模式改為:

- 固定注入只保留 bounded core memory
- 額外相關資訊改成按 query 查詢
- 估算 token 時避免做即時檢索，減少不必要成本

## 3. 核心元件與職責

### 3.1 `MemoryStore` (`nanobot/agent/memory.py`)

職責:

- 管理 `memory/MEMORY.md` 與 `memory/HISTORY.md`
- 提供記憶讀取組裝 (`get_memory_context`)
- 執行 consolidation 寫入
- 在可用時對接 mem0 (`from_config` / `search` / `add`)

檔案語義:

- `MEMORY.md`: 長期結構化記憶，consolidation 成功時可能被全量更新
- `HISTORY.md`: append-only 歷史日誌，不修改舊條目

### 3.2 `ContextBuilder` (`nanobot/agent/context.py`)

職責:

- `build_system_prompt(...)` 內呼叫 `MemoryStore.get_memory_context(...)`
- `build_messages(...)` 會把 `current_message` 當作 `memory_query`
- 遇到 `[token-probe]` 時，將 `include_relevant_memory=False`

### 3.3 `MemoryConsolidator` (`nanobot/agent/memory.py`)

職責:

- token 感知式整合策略
- 以 per-session lock 避免同一 session 的整合競態
- 成功整合後更新 `session.last_consolidated` 並持久化

### 3.4 `AgentMemoryConfig` (`nanobot/config/schema.py`)

職責:

- 定義記憶模式開關與上限值
- 提供安全預設值，尤其是 mem0 預設關閉

## 4. 讀取路徑: Prompt 組裝

讀取路徑由 `ContextBuilder.build_messages(...)` 觸發。

### 4.1 流程圖

```text
build_messages(history, current_message, ...)
  -> is_token_probe = (current_message == "[token-probe]")
  -> build_system_prompt(memory_query=current_message,
                         include_relevant_memory=not is_token_probe)
      -> memory.get_memory_context(query, include_relevant)
          -> _build_core_memory_context()
              -> read MEMORY.md
              -> _truncate_for_prompt(max_core_chars)
          -> (optional) _build_mem0_context(query)
              -> mem0.search(query, user_id, limit)
  -> 組出 system + history + current message
```

### 4.2 Core memory 注入規則 (always-on)

`_build_core_memory_context()` 會:

1. 讀 `MEMORY.md`
2. 套用 `_truncate_for_prompt(text, max_core_chars)`
3. 若超過上限，加上 `"[... truncated ...]"`

這代表核心記憶注入永遠有上限，不再是全文注入。

### 4.3 Relevant memory 注入規則 (optional)

`_build_mem0_context(query)` 只會在以下條件同時成立時執行:

- `memory.enabled == true`
- query 非空
- mem0 client 初始化成功

查詢介面:

```python
client.search(
    query=query,
    user_id=self._mem0_user_id,
    limit=self.config.max_mem0_results,
)
```

結果處理重點:

- 最多取 `max_mem0_results`
- 總字元受 `max_mem0_chars` 限制
- 每筆結果會轉字串後再裁切
- 無結果或失敗則不注入 relevant 區塊

### 4.4 token probe 特殊行為

`build_messages(...)` 在 `current_message == "[token-probe]"` 時，會將 `include_relevant_memory=False`。

效果:

- token 估算路徑不會觸發 live mem0 retrieval
- 估算更穩定，且不額外依賴檢索可用性

## 5. 寫入路徑: Consolidation、持久化、索引

### 5.1 consolidation 成功路徑

`MemoryStore.consolidate(messages, provider, model)` 會:

1. 讀取目前 `MEMORY.md`
2. 用 `save_memory` 工具呼叫 LLM，要求回傳:
   - `history_entry`
   - `memory_update`
3. `history_entry` append 到 `HISTORY.md`
4. 若 `memory_update != current_memory`，覆寫 `MEMORY.md`

所以檔案語義維持既有模式:

- `HISTORY.md` 一律 append-only
- `MEMORY.md` 依 consolidation 結果更新

### 5.2 consolidation 後 mem0 索引 (optional, best-effort)

只有在 `memory.enabled == true` 且 mem0 client 可用時才執行。

索引規則:

- `history_entry`: 每次成功 consolidation 都會嘗試 `client.add(...)`
- `memory_update`: 只有內容變更時才嘗試索引
- 索引 `memory_update` 時，不送全文，只送 `max_mem0_index_chars` 上限摘錄

對應 `add` 呼叫:

```python
client.add(history_entry, user_id=..., metadata={"source": "history_entry"})
client.add(memory_update_excerpt, user_id=..., metadata={"source": "memory_update_excerpt"})
```

## 6. Token 估算與整合行為

### 6.1 估算入口

`MemoryConsolidator.estimate_session_prompt_tokens(session)` 會:

1. 取未整合 history
2. 呼叫 `build_messages(..., current_message="[token-probe]")`
3. 交給 `estimate_prompt_tokens_chain(...)` 估算

重點是第 2 步會帶入 token probe，所以 relevant memory 檢索在估算時被關閉。

### 6.2 觸發與目標

`maybe_consolidate_by_tokens(session)` 行為:

- `context_window_tokens <= 0` 或無訊息時直接跳過
- 估算值 `< context_window_tokens` 時不整合
- 估算值 `>= context_window_tokens` 時進入整合迴圈
- 目標是降到 `context_window_tokens // 2`
- 最多跑 5 輪

### 6.3 邊界選取

`pick_consolidation_boundary(...)` 只在 user 訊息邊界切段，避免切壞多訊息配對語義。找不到安全邊界就停止本輪整合。

### 6.4 鎖與持久化

- 同一 session 使用共享 lock 序列化整合
- 每輪成功後更新 `last_consolidated`
- 呼叫 `sessions.save(session)` 寫回持久層

## 7. 設定參考與預設值

設定位置:

```text
agents.defaults.memory
```

### 7.1 記憶相關設定

| 欄位 | 型別 | 預設值 | 說明 |
| --- | --- | --- | --- |
| `enabled` | `bool` | `false` | 是否啟用 mem0 檢索與索引 |
| `max_core_chars` | `int` | `4000` | `MEMORY.md` 注入 prompt 的字元上限 |
| `max_mem0_results` | `int` | `4` | 單次 relevant memory 最多結果數 |
| `max_mem0_chars` | `int` | `2000` | 單次 relevant memory 總字元上限 |
| `max_mem0_index_chars` | `int` | `800` | `memory_update` 索引摘錄上限 |
| `mem0_config` | `dict[str, object]` | `{}` | 傳給 `Memory.from_config(...)` |

### 7.2 相關全域設定

| 欄位 | 預設值 | 說明 |
| --- | --- | --- |
| `agents.defaults.context_window_tokens` | `65536` | token 感知 consolidation 觸發上限 |
| `agents.defaults.memory_window` | `null` | 已棄用，相容舊設定，執行期忽略 |

> `schema.py` 採用 alias generator，設定可接受 snake_case 與 camelCase。

### 7.3 可直接複製的 `config.json` 範例（啟用 mem0）

如果你想先看使用者角度的設定與啟用方式，請先讀 [記憶功能入門](./getting-started/memory.md)。

以下範例可直接合併到 `~/.nanobot/config.json`，路徑是 `agents.defaults.memory`。

```json
{
  "agents": {
    "defaults": {
      "memory": {
        "enabled": true,
        "maxCoreChars": 4000,
        "maxMem0Results": 4,
        "maxMem0Chars": 2000,
        "maxMem0IndexChars": 800,
        "mem0Config": {
          "llm": {
            "provider": "openai",
            "config": {
              "openai_base_url": "http://localhost:8317/v1",
              "model": "claude-haiku-4-5"
            }
          },
          "embedder": {
            "provider": "gemini",
            "config": {
              "model": "gemini-embedding-2-preview",
              "embedding_dims": 1536
            }
          }
        }
      }
    }
  }
}
```

!!! note "mem0 是選用功能"
    `enabled` 預設是 `false`，不開啟也能正常使用核心記憶。

!!! tip "不使用 mem0 時"
    即使 `mem0Config` 保持空物件或不設定，`MEMORY.md` 的 core memory 注入與 consolidation 仍會照常運作。

## 8. 降級與失敗處理

### 8.1 mem0 相關失敗

- mem0 模組不存在、初始化失敗、`search/add` 失敗
- 行為: 記錄 warning/exception，流程不中斷
- 結果: 只退化成 core-memory-only，主對話仍可運作

### 8.2 consolidation 相關失敗

失敗來源例如:

- LLM 沒有呼叫 `save_memory`
- tool payload 格式不符或欄位缺失
- provider/tool 呼叫例外

處理邏輯:

1. `_consecutive_failures += 1`
2. 未達 3 次，回傳 `False`，等待下次重試
3. 連續達 3 次，執行 `_raw_archive(messages)`
4. `_raw_archive` 會把原始訊息以 `[RAW]` 條目 append 到 `HISTORY.md`
5. 重置失敗計數，回傳 `True`

### 8.3 tool_choice 相容路徑

當 forced `tool_choice` 被 provider 拒絕時，會自動改用 `tool_choice="auto"` 再試一次。

## 9. 營運說明、 rollout、相容性

### 9.1 always-on 與 optional 邊界

always-on:

- `MEMORY.md` bounded core 注入
- `HISTORY.md` append-only 寫入
- consolidation 主流程

optional:

- mem0 檢索 (`search`)
- mem0 索引 (`add`)

### 9.2 預設 rollout 策略

因為 `enabled=false` 是預設值，所以升級後的預設行為是:

- 不依賴 mem0
- 先享受 bounded core memory 的 prompt 穩定性
- 需要時再開啟 mem0 做增強

### 9.3 與既有資料相容

- 舊有 `MEMORY.md` 與 `HISTORY.md` 可直接沿用
- consolidation 寫檔語義維持一致
- 未實作自動 migration pipeline，啟用 mem0 後僅對後續 consolidation 進行索引

### 9.4 實務調校建議

- 若 prompt 壓力高，先調小 `max_core_chars`
- 若 relevant memory 噪音高，先調小 `max_mem0_results`
- 若索引成本高，先調小 `max_mem0_index_chars`

## 10. 建議除錯與 QA 檢查清單

以下清單可用於開發驗證與上線前檢查。

### 10.1 設定與啟動

- [ ] 確認 `agents.defaults.memory.enabled` 預期值
- [ ] 確認各 char/result 上限有設定
- [ ] 啟用 mem0 時，`mem0_config` 可成功初始化 client

### 10.2 讀取路徑驗證

- [ ] 一般訊息可看到 core memory 區塊，且不超過 `max_core_chars`
- [ ] 啟用 mem0 且 query 存在時，能注入 relevant memory
- [ ] `current_message="[token-probe]"` 時，不做 relevant memory 查詢

### 10.3 寫入路徑驗證

- [ ] consolidation 成功時 `HISTORY.md` 有新條目
- [ ] `memory_update` 有變更時才覆寫 `MEMORY.md`
- [ ] 啟用 mem0 時，`history_entry` 會索引
- [ ] `memory_update` 未變更時，不索引 memory excerpt

### 10.4 失敗與降級驗證

- [ ] mem0 初始化失敗時，對話仍能進行
- [ ] 連續 consolidation 失敗 3 次後，會產生 `[RAW]` 歷史條目
- [ ] forced tool_choice 不支援時，可 fallback 到 `auto`

### 10.5 回歸重點

- [ ] 沒有任何敘述仍宣稱 `MEMORY.md` 會全文注入
- [ ] 文件已清楚區分 always-on 與 optional
- [ ] 文件內容只使用現有程式可驗證的行為
