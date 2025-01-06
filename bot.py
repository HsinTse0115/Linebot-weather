import threading
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from weather import get_weather
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from database import USER_CITIES
from scheduler import run_scheduler

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    reply = ""

    if "天氣" in user_message:
        city = user_message.replace("天氣", "").strip()
        if city:
            weather_info = get_weather(city)
            reply = weather_info
        else:
            reply = "請提供有效的城市名稱，例如「新竹市天氣」。"
    elif "設定城市" in user_message:
        # 用戶指令修改推送城市
        city = user_message.replace("設定城市", "").strip()
        if city:
            # 更新用戶對應的城市
            user_id = event.source.user_id
            USER_CITIES[user_id] = city
            reply = f"已成功設定推送城市為：{city}。"
        else:
            reply = "請提供有效的城市名稱。"
    elif "查詢ID" in user_message:
        # 查詢用戶的 LINE User ID
        user_id = event.source.user_id
        reply = f"您的 LINE User ID 是：{user_id}"
    else:
        reply = "抱歉，我目前只能處理天氣查詢。如果需要查詢天氣，請輸入以下指令\n" \
            "功能:\n" \
            "查詢天氣：(城市名+天氣)\n" \
            "修改自動播報的地區：設定城市（空格）城市名\n" \
            "查詢自己的Line UserID:查詢ID"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# 啟動排程任務的執行緒
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == "__main__":
    app.run(port=8000)