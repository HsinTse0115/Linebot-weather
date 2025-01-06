# 每日即時天氣播報系統

## 簡介

透過這個系統,使用者可以輕鬆接收到每日的天氣預報,不再需要主動查詢,從而有效避免因為忽視天氣變化而帶來的困擾和不便。我們的研究動機就是希望以簡單易用的方式,將天氣資訊更便捷地傳遞給每一位使用者,進一步提升生活質量,減少因天氣因素帶來的風險。

## 主要功能

*   **天氣查詢**: 使用者可以透過輸入 "XX市天氣" 來查尋當地當天的天氣狀況。
*   **每日天氣播報**:系統會在固定時間自動發送天氣資訊到使用者的聊天室。
*   **穿衣建議**:除了天氣資訊以外，系統會根據當下天氣狀況來判斷，並給予使用者衣著建議。
*   **更改城市**:使用者可透過輸入"設定城市+XX市"來設定天氣播報的城市。
*   **查詢ID**:使用者可透過輸入"查詢ID"來查詢自己的使用者Line UserID。

## 技術架構

*   **程式語言**: Python
*   **Web 框架**: Flask
*   **Line Bot API**: 使用 Line Bot SDK 與 Line Bot 互動
*   **資料庫**:使用python字典模擬資料庫
*   **排程工具**:使用 schedule 套件進行排程任務
*   **HTTP請求**:使用 requests 套件進行 API 請求
*   **環境變數管理**:使用 config.py 文件管理環境變數

## 專案架構
Linebot-weather/ 
├── requirements.txt
├── src/
│   ├── bot.py
│   ├── config.py
│   ├── database.py
│   ├── scheduler.py
│   └── weather.py      
└── README.md
   

*   `requirements.txt`:文件用於列出專案所需的 Python 套件
    *   `Flask`用於建立 Web 應用程式的輕量級框架。
    *   `line-bot-sdk`用於與 Line Bot API 互動的 SDK。
    *   `requests`用於發送 HTTP 請求的套件。
    *   `schedule`用於排程任務的套件。
*   `src/`: 包含主要程式碼。
    *   `bot.py`Flask 應用程式入口點，處理 Line Bot 的 webhook 請求。
    *   `config.py` 管理環境變數和配置設定
    *   `database.py`模擬資料庫，儲存使用者的城市資訊。
    *   `scheduler.py`負責排程每日天氣播報的任務
    *   `weather.py`: 處理天氣資訊的函式。

## 環境設定

1.  **安裝套件**:確保程式有辦法執行。
 ```pip install -r requirements.txt```
2.  **設定環境變數**: 建立`config.py`檔案並設定以下變數

    ```
       LINE_CHANNEL_ACCESS_TOKEN = 'LINE_CHANNEL_ACCESS_TOKEN'
       LINE_CHANNEL_SECRET = 'LINE_CHANNEL_SECRET'
       WEATHER_API_KEY = 'WEATHER_API_KEY'
    ```

    *   `LINE_CHANNEL_SECRET`: Line Bot的通道密鑰，用於驗證來自Line平台的Webhook請求。
    *   `LINE_CHANNEL_ACCESS_TOKEN`: Line Bot的通道存取令牌，用於授權和驗證與Line平台的API請求。
    *   `WEATHER_API_KEY`: 用來訪問天氣API的密鑰

## 如何執行

1.  **執行bot.py**
2.  **開始使用**

## 開發輔助工具

*   **GitHub**: 用於版本控制和協作。

## 貢獻

吳承儒、陳昕澤、秦鼎軒、張瑋倫
