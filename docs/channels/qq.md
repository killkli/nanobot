# QQ

nanobot 透過 QQ 官方 **botpy SDK** 以 WebSocket 連線接收訊息，無需公開 IP。支援私聊（C2C）與群組 @提及，以及純文字或 Markdown 格式回覆。

---

## 前置條件

- 一個 QQ 帳號
- 向 QQ 開放平台申請開發者資格

---

## 步驟一：申請開發者並建立 Bot

1. 前往 [QQ 開放平台](https://q.qq.com)
2. 點擊 **立即接入** → 以個人或企業身份申請開發者資格
3. 審核通過後，前往 **機器人管理** → **建立機器人**
4. 填寫機器人基本資訊後建立

---

## 步驟二：取得 AppID 與 AppSecret

1. 進入機器人管理頁面
2. 前往 **開發設定**
3. 複製 **AppID** 和 **AppSecret**

---

## 步驟三：沙盒測試設定

在正式發佈前，可先在沙盒環境中測試：

1. 在機器人管理後台找到 **沙盒配置**
2. 在 **在消息列表配置** 下，點擊 **添加成員**，輸入您的 QQ 號
3. 成員添加後，使用手機 QQ 掃描機器人的 QR Code
4. 開啟機器人主頁 → 點擊 **發消息** 即可開始測試

!!! warning "沙盒與正式環境"
    沙盒環境僅供開發測試。正式上線需在機器人後台提交審核並發佈，詳見 [QQ Bot 文件](https://bot.q.qq.com/wiki/)。

---

## 步驟四：設定 config.json

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_OPENID"],
      "msgFormat": "plain"
    }
  }
}
```

### 完整設定選項

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_OPENID"],
      "msgFormat": "plain"
    }
  }
}
```

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `enabled` | `false` | 是否啟用此頻道 |
| `appId` | `""` | QQ Bot 的 AppID |
| `secret` | `""` | QQ Bot 的 AppSecret |
| `allowFrom` | `[]` | 允許互動的使用者 OpenID 列表 |
| `msgFormat` | `"plain"` | 訊息格式：`"plain"` 或 `"markdown"` |

### `msgFormat` 說明

| 值 | 適用場景 |
|----|----------|
| `"plain"`（預設） | 純文字，相容所有 QQ 客戶端 |
| `"markdown"` | Markdown 格式，僅較新版本 QQ 客戶端支援 |

---

## 步驟五：啟動

```bash
nanobot gateway
```

---

## 取得您的 OpenID

`allowFrom` 填入的是 QQ 的使用者 OpenID，而非 QQ 號碼。

**取得方法：**

1. 先將 `allowFrom` 設為 `["*"]` 暫時允許所有人
2. 啟動 nanobot 並傳訊息給 Bot
3. 查看 nanobot 日誌，其中會顯示您的 OpenID
4. 更新 `allowFrom`

---

## 群組支援

目前 QQ Bot 支援：

- **私聊（C2C）**：一對一私信
- **群組 @提及**：在群組中 @機器人
- **私信（Direct Message）**：透過 Guild 私信

---

## 檔案與媒體處理

### 接收附件（Inbound）

當使用者發送圖片、影片、音頻或一般檔案時，nanobot 會自動下載至媒體目錄，並在訊息內容中附上「Received files:」清單，列出各檔案的路徑。

下載採用分塊流式寫入，記憶體安全。大檔案也能正常處理，不會占用大量記憶體。

### 傳送媒體（Outbound）

在 `OutboundMessage` 中使用 `media` 參數即可傳送圖片或檔案：

```python
OutboundMessage(text="這是一張圖片", media="/path/to/image.png")
OutboundMessage(text="一份文件", media="file:///path/to/document.pdf")
OutboundMessage(text="網頁圖片", media="https://example.com/photo.jpg")
```

`media` 支援三種路徑格式：
- **本地路徑**：如 `/Users/me/photo.png`
- **file:// URI**：如 `file:///Users/me/photo.png`
- **HTTP(S) URL**：如 `https://example.com/image.jpg`

傳送時，系統會先將媒體上傳至 QQ 開放平台，再夾帶 `msg_type=7` 的 rich media 訊息發送，最後再發送文字內容。

### 支援的檔案類型

QQ 對音頻/影片格式有限制，因此採用以下分類：

| 分類 | QQ 類型代碼 | 支援副檔名 |
|------|-------------|------------|
| 圖片 | `1` (IMAGE) | `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`, `.tif`, `.tiff`, `.ico`, `.svg` |
| 一般檔案 | `4` (FILE) | 所有其他副檔名（當作一般檔案傳送） |

音頻與影片檔案目前僅能以一般檔案形式傳送。

### 回覆附件

在 `OutboundMessage` 中使用 `attachments` 欄位即可附加本地檔案至回覆：

```python
OutboundMessage(text="這是回覆", attachments=["/path/to/file.pdf"])
```

不同版本的 botpy 使用的附件欄位名稱不同，系統會自動嘗試多個候選欄位名稱（`attachment`、`attachments`、`file`、`files`），無需特別設定。

---

## 正式發佈流程

沙盒測試完成後：

1. 在機器人管理後台 → **版本管理** → 建立新版本
2. 填寫功能描述與截圖
3. 提交審核
4. 審核通過後發佈

詳細流程請參考 [QQ Bot 官方文件](https://bot.q.qq.com/wiki/)。

---

## 常見問題

**Bot 收到訊息但不回應？**

- 確認 `allowFrom` 中包含您的 OpenID（非 QQ 號）
- 查看日誌確認是否有「Access denied」

**群組中 Bot 不回應？**

- 群組中需要 @機器人才會觸發回應
- 確認機器人已被加入群組

**沙盒環境中找不到機器人？**

- 確認已在沙盒配置中添加您的 QQ 號
- 使用手機 QQ（非電腦版）掃描 QR Code
