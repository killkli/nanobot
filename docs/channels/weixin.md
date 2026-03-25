# WeChat / 微信

nanobot 支援透過個人微信帳號接收及發送訊息，採用 HTTP Long Polling 方式連接 ilinkai API，無需安裝本地微信客戶端或開放 WebSocket。

---

## 前置條件

- 個人微信帳號（需能掃描 QR Code 登入）
- Python `qrcode` 套件（可選，用於在終端顯示 QR Code）

> nanobot 使用 [@tencent-weixin/openclaw-weixin](https://github.com/tencent-weixin/openclaw-weixin) v1.0.3 協定，這是個人微信機器人的開源解決方案。

---

## 步驟一：安裝選用依賴套件

個人微信頻道需要額外安裝加密相關套件：

```bash
pip install nanobot-ai[weixin]
```

或若使用 `uv`：

```bash
uv pip install nanobot-ai[weixin]
```

QR Code 顯示需要 `qrcode` 套件（可選）：

```bash
pip install qrcode
```

---

## 步驟二：設定 config.json

```json
{
  "channels": {
    "weixin": {
      "enabled": true,
      "allowFrom": ["your_user_id"]
    }
  }
}
```

### 完整設定選項

```json
{
  "channels": {
    "weixin": {
      "enabled": true,
      "allowFrom": ["your_user_id"],
      "baseUrl": "https://ilinkai.weixin.qq.com",
      "cdnBaseUrl": "https://novac2c.cdn.weixin.qq.com/c2c",
      "routeTag": null,
      "token": "",
      "stateDir": "",
      "pollTimeout": 35
    }
  }
}
```

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `enabled` | `false` | 是否啟用此頻道 |
| `allowFrom` | `[]` | 允許互動的使用者 ID 列表（微信 OpenID） |
| `baseUrl` | `https://ilinkai.weixin.qq.com` | API 伺服器位址 |
| `cdnBaseUrl` | `https://novac2c.cdn.weixin.qq.com/c2c` | CDN 伺服器位址（用於多媒體下載） |
| `routeTag` | `null` | 必填值（搭配 ilinkai 1.0.3），用於指定路由標籤，系統會在請求時傳送 `SKRouteTag` Header以適配微信官方的 ilinkai 1.0.3 協定要求 |
| `token` | `""` | 手動設定 Bot Token，若留空則透過 QR Code 登入取得 |
| `stateDir` | `""` | 狀態檔案儲存目錄（預設：`~/.nanobot/weixin/`） |
| `pollTimeout` | `35` | Long Polling 逾時秒數 |

---

## 步驟三：登入認證

啟動前需先登入個人微信帳號：

```bash
nanobot channels login weixin
```

過程說明：

1. 終端機會顯示 QR Code
2. 開啟手機微信，使用「掃一掃」功能掃描 QR Code
3. 在手機上點選「確認登入」
4. 登入成功後，Bot Token 會自動儲存至 `~/.nanobot/weixin/account.json`

!!! tip "QR Code 失效"
    QR Code 有效時間有限，若超過 3 次刷新後仍未掃描，請重新執行登入指令。

!!! tip "QR Code 自動刷新"
    登入過程中，若 QR Code 過期，系統會自動重新取得並顯示新 QR Code，無需手動重新執行指令。

!!! tip "多實例登入"
    同一個微信帳號無法同時在多個 nanobot 實例中使用。

---

## 步驟四：啟動

```bash
nanobot gateway
```

---

## 對話管理（Session）與輪詢機制

為提升訊息處理穩定性，系統實作了以下機制：

### 過期 Session 處理
- 當 session 過期或失效（如 "WeChat session paused" 錯誤）時，系統會自動停止向該 session 發送訊息，避免無效重試
- 此狀態表示 Bot 與微信伺服器的長輪詢連接已中斷，需重啟 nanobot 重新建立連線

### 自動重連
- 系統會自動嘗試恢復與微信伺服器的連線，無需手動干預
- 若懷疑連線異常，可重啟 nanobot 解決

### 注意事項
- 同一個微信帳號無法同時在多個 nanobot 實例中使用
- 若 session 持续异常，請刪除 `~/.nanobot/weixin/account.json` 後重新登入

---

## 取得您的使用者 ID

`allowFrom` 填入的是微信使用者的 OpenID（不是 UserID）。

**取得方法：**

1. 先將 `allowFrom` 設為 `["*"]` 暫時允許所有人
2. 啟動 nanobot 並傳訊息給 Bot
3. 查看 nanobot 日誌，其中會顯示您的 OpenID
4. 更新 `allowFrom`

---

## 多媒體支援

個人微信頻道支援以下媒體類型：

| 訊息類型 | 處理方式 |
|----------|----------|
| 文字 | 直接傳遞給 AI |
| 圖片 | 下載後傳遞給視覺模型 |
| 語音 | 若有 Whisper 支援則自動轉錄，否則下載後傳遞 |
| 檔案 | 下載後傳遞給 AI |
| 影片 | 下載後傳遞給 AI |
| 引用訊息 | 解析引用內容後與回覆文字合併 |

### 發送多媒體（CDN 上傳）

Bot 主動發送圖片、影片、檔案時，會透過 CDN 上傳至微信伺服器後再發送，確保訊息傳遞穩定。



---

## 狀態持久化

nanobot 會在 `~/.nanobot/weixin/` 目錄儲存以下檔案：

| 檔案 | 說明 |
|------|------|
| `account.json` | 儲存 Bot Token、API URL、以及各使用者的 `_context_token`（用於對話上下文恢復） |

- `_context_token` 會隨著每次請求更新，刪除後重啟時會導致對話上下文遺失，需重新與 Bot 互動建立新 session
- 若刪除 `account.json`，下次啟動時需重新登入。

---

## 安全性說明

- 個人微信機器人需要掃描 QR Code 登入，Token 會儲存在本機
- 請妥善保管 `account.json` 檔案，避免外洩
- 建議將 `allowFrom` 設為特定使用者的 OpenID，而非 `["*"]`

---

## 常見問題

**QR Code 無法顯示？**

- 確認已安裝 `qrcode` 套件：`pip install qrcode`
- 若在遠端伺服器上，可透過日誌中的 URL 在本地掃描

**登入失敗，提示「QR Code 失效」？**

- QR Code 有效時間有限，請在短時間內完成掃描
- 可嘗試重新執行 `nanobot channels login weixin --force`

**Bot 無法發送訊息？**

- 確認帳號已成功登入（日誌應顯示 "WeChat login successful"）
- 檢查 `allowFrom` 是否包含您的 OpenID
- 確認微信帳號狀態正常（未被封鎖）

**Session 暂停？**

- 若出現 "WeChat session paused" 錯誤，表示 session 已過期
- 刪除 `~/.nanobot/weixin/account.json` 後重新登入即可
