# 記憶功能入門

想讓 nanobot 在長對話中更連貫，記得你剛剛聊過的重點，這份指南會帶你快速上手。

---

## 記憶功能會做什麼

nanobot 的記憶功能主要分成兩層：

1. **核心記憶（core memory）**
   - 來自 `memory/MEMORY.md`
   - 會在對話時注入 prompt
   - 有字元上限，避免 prompt 無限制膨脹

2. **相關記憶（mem0 檢索，選用）**
   - 依照當前問題做檢索
   - 只在你啟用後才會使用

!!! note "預設行為"
    nanobot 預設不啟用 mem0。即使不開 mem0，核心記憶仍會正常運作。

---

## 預設設定重點

以下是目前的預設值：

| 設定 | 預設值 | 說明 |
|------|--------|------|
| `enabled` | `false` | 是否啟用 mem0 檢索與索引 |
| `max_core_chars` / `maxCoreChars` | `4000` | 核心記憶注入上限 |
| `max_mem0_results` / `maxMem0Results` | `4` | 單次檢索最多結果數 |
| `max_mem0_chars` / `maxMem0Chars` | `2000` | 單次檢索總字元上限 |
| `max_mem0_index_chars` / `maxMem0IndexChars` | `800` | 建立索引時的摘要上限 |

!!! tip "snake_case 與 camelCase"
    設定檔可使用 snake_case 或 camelCase。入門範例通常用 camelCase，比較好讀。

---

## 步驟一，先用預設值開始

如果你剛上線，建議先維持預設值，直接使用核心記憶。

這樣做的好處：

- 設定最少
- 行為穩定
- 不需要額外 mem0 相依

---

## 步驟二，需要時再啟用 mem0

當你希望「依問題補更多相關記憶」時，再開啟 mem0。

把下列片段合併到 `~/.nanobot/config.json`：

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

!!! warning "不要誤會"
    mem0 不是預設開啟。只有 `enabled: true` 時才會啟用檢索與索引。

---

## 步驟三，視情況微調

你可以先從兩個參數開始：

- `maxCoreChars`：prompt 壓力高時，先調小
- `maxMem0Results`：覺得檢索資訊太雜時，先調小

一般不需要一開始就調所有參數。

---

## 啟用後，實際會看到什麼

- 對話仍以核心記憶為基礎
- 有啟用 mem0 時，會多一層與當前問題相關的記憶檢索
- mem0 初始化或檢索失敗時，系統會退回核心記憶模式，主對話不會中斷
- 啟用 mem0 後，只會對後續整合內容建立索引

---

## 隱私與安全提醒

- `MEMORY.md`、`HISTORY.md` 會持久化對話記憶，請避免在對話中輸入不必要的敏感資訊
- 啟用 mem0 時，記憶內容會交給你設定的 mem0 後端與其 LLM/embedder 設定處理
- `config.json` 可能包含 API 金鑰，請勿提交到公開儲存庫

---

## 想看開發細節？

如果你想了解完整架構、讀寫流程、錯誤降級與調校建議，請看開發者文件：

- [記憶系統開發者文件](../memory-system.md)
