import time
import schedule
from weather import get_weather
from linebot import LineBotApi
from linebot.models import TextSendMessage
from database import USER_CITIES
from config import LINE_CHANNEL_ACCESS_TOKEN

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def send_weather_update():
    """分別推送天氣資訊給不同用戶"""
    for user_id, city in USER_CITIES.items():  # 遍歷每個用戶及其對應的城市
        weather_info = get_weather(city)
        try:
            line_bot_api.push_message(
                user_id,  # 每個用戶的 ID
                TextSendMessage(text=f"每日天氣播報：\n{weather_info}")
            )
            print(f"天氣資訊已成功推送！城市：{city} 用戶：{user_id}")
        except Exception as e:
            print(f"推送天氣資訊失敗：{e}")

# 定義排程任務
schedule.every(1).minutes.do(send_weather_update)  # 每 1 分鐘執行一次
#schedule.every().day.at("08:00").do(send_weather_update) # 每天早上 8 點執行一次
def run_scheduler():
    """執行排程任務"""
    while True:
        schedule.run_pending()
        time.sleep(1)