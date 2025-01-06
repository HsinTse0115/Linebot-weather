from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
from datetime import datetime, timedelta
from config import WEATHER_API_KEY, LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

app = Flask(__name__)

# LINE API 配置
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# 時間段判斷
def get_time_of_day(hour=None):
    if hour is None:
        hour = datetime.now().hour
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    else:
        return "evening"

#穿衣建議
def get_clothing_advice(temperature, humidity, wind_speed, weather_description, time_of_day, feels_like_temp):
    """根據更多氣象條件提供更精細的穿衣建議"""
    # 根據氣溫範圍提供基礎建議
    if temperature < 10:
        clothing_advice = "氣溫偏低，建議穿保暖大衣、毛衣，並戴上手套和圍巾。"
        if wind_speed > 10:
            clothing_advice += " 風速較大，記得加穿防風外套。"
        if humidity > 80:
            clothing_advice += " 濕度較高，建議選擇防水材質的衣物。"
    elif 10 <= temperature < 20:
        clothing_advice = "氣溫微涼，建議穿外套或薄毛衣。"
        if wind_speed > 15:
            clothing_advice += " 有較強風力，適合穿風衣以防寒。"
        if "雨" in weather_description or "雷" in weather_description:
            clothing_advice += " 預計會下雨，記得攜帶雨具！"
    elif 20 <= temperature < 30:
        clothing_advice = "氣溫舒適，建議穿輕便的短袖或長袖襯衫。"
        if wind_speed > 20:
            clothing_advice += " 風速較強，適合穿長袖襯衫以保護皮膚。"
        if humidity > 70:
            clothing_advice += " 濕度偏高，選擇透氣的衣物會讓你更舒適。"
        if "晴" in weather_description:
            clothing_advice += " 天氣晴朗，請注意防曬，使用防曬霜或戴帽子。"
    else:
        clothing_advice = "氣溫炎熱，建議穿短袖和涼爽的衣物，並注意防曬。"
        if "雷" in weather_description or "大風" in weather_description:
            clothing_advice += " 若有雷陣雨或大風，請攜帶雨具並穿防風衣物。"
        if humidity > 80:
            clothing_advice += " 高濕度，選擇透氣或速乾衣物更為舒適。"

    # 針對時間段進行調整（早上、中午、晚上）
    if time_of_day == "morning":
        clothing_advice += " 早晨氣溫較低，建議帶上一件薄外套，並準備好迎接天氣變化。"
    elif time_of_day == "afternoon":
        clothing_advice += " 中午時段氣溫較高，適合穿著輕便的服裝，但要注意防曬。"
    elif time_of_day == "evening":
        clothing_advice += " 晚上的氣溫會逐漸下降，建議穿上外套或長袖衣物以保持溫暖。"

    # 根據體感溫度調整建議（風寒效應與熱指數）
    if feels_like_temp < 10:
        clothing_advice += " 體感溫度很低，請增加保暖措施，特別是手腳部位。"
    elif 10 <= feels_like_temp < 20:
        clothing_advice += " 體感溫度稍低，建議穿上適合保暖的衣物。"
    elif feels_like_temp > 30:
        clothing_advice += " 體感溫度過高，建議穿涼爽衣物，並隨時補充水分以避免中暑。"

    return clothing_advice

# 天氣預報查詢
def get_weather_forecast(lat, lon, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=zh_tw"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != "200":
            return "抱歉，無法取得該地區的天氣預報資訊。請稍後再試。"

        forecast_list = data.get('list', [])
        forecast_info = f"{city} 的天氣預報：\n"
        for forecast in forecast_list[:5]:  # 只取前5筆預報資料
            dt_txt = forecast.get('dt_txt', '無法取得時間')
            weather_description = forecast.get('weather', [{}])[0].get('description', '無法取得天氣描述')
            temperature = forecast.get('main', {}).get('temp', '無法取得溫度')
            humidity = forecast.get('main', {}).get('humidity', '無法取得濕度')
            wind_speed = forecast.get('wind', {}).get('speed', '無法取得風速')
            forecast_info += f"{dt_txt} - {weather_description}, 氣溫：{temperature}°C, 濕度：{humidity}%, 風速：{wind_speed} m/s\n"

        return forecast_info

    except requests.exceptions.RequestException as e:
        return f"抱歉，無法取得天氣預報資訊。錯誤信息：{e}"

# 即時天氣查詢
def get_weather(city="高雄"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=zh_tw"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查 HTTP 請求是否成功
        data = response.json()

        if data.get("cod") != 200:
            return "抱歉，無法取得該地區的天氣資訊。請稍後再試。"

        city_name = data.get('name', '未知城市')
        weather_description = data.get('weather', [{}])[0].get('description', '無法取得天氣描述')
        temperature = data.get('main', {}).get('temp', '無法取得溫度')
        humidity = data.get('main', {}).get('humidity', '無法取得濕度')
        wind_speed = data.get('wind', {}).get('speed', '無法取得風速')
        wind_direction = data.get('wind', {}).get('deg', '無法取得風向')
        feels_like_temp = data.get('main', {}).get('feels_like', '無法取得體感溫度')

        # 使用 get_clothing_advice 函數提供穿衣建議
        clothing_advice = get_clothing_advice(temperature, humidity, wind_speed, weather_description, "afternoon", feels_like_temp)

        return f"{city_name} 的天氣狀況：{weather_description}\n" \
               f"氣溫：{temperature}°C\n" \
               f"濕度：{humidity}%\n" \
               f"風速：{wind_speed} m/s,風向:{wind_direction}°\n" \
               f"穿衣建議：{clothing_advice}"
       
    except requests.exceptions.RequestException as e:
        return f"抱歉，無法取得天氣資訊。錯誤信息：{e}"

# 處理用戶訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    
    if user_message.startswith("天氣"):
        city = user_message.replace("天氣", "").strip()
        if city:
            weather_info = get_weather(city)
            reply_message = weather_info
        else:
            reply_message = "請輸入要查詢天氣的城市名稱，例如：天氣高雄"
    
    elif user_message.startswith("預報"):
        city = user_message.replace("預報", "").strip()
        if city:
            # 使用城市名稱取得經緯度，然後進行預報查詢
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}"
            try:
                geo_response = requests.get(geo_url)
                geo_response.raise_for_status()
                geo_data = geo_response.json()
                
                if geo_data:
                    lat = geo_data[0]['lat']
                    lon = geo_data[0]['lon']
                    forecast_info = get_weather_forecast(lat, lon, city)
                    reply_message = forecast_info
                else:
                    reply_message = "無法取得該城市的地理資訊，請確認城市名稱是否正確。"
            
            except requests.exceptions.RequestException as e:
                reply_message = f"抱歉，無法取得天氣預報資訊。錯誤信息：{e}"
        else:
            reply_message = "請輸入要查詢天氣預報的城市名稱，例如：預報台北"
    
    else:
        reply_message = "歡迎使用天氣小幫手！\n- 查詢即時天氣：『天氣[城市名稱]』\n- 查詢預報：『預報[城市名稱]』"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# LINE Bot Webhook
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理用戶訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    
    if user_message.startswith("天氣"):
        city = user_message.replace("天氣", "").strip()
        if city:
            weather_info = get_weather(city)
            reply_message = weather_info
        else:
            reply_message = "請輸入要查詢天氣的城市名稱，例如：天氣高雄"
    
    elif user_message.startswith("預報"):
        city = user_message.replace("預報", "").strip()
        if city:
            forecast_info = get_weather_forecast(city)
            reply_message = forecast_info
        else:
            reply_message = "請輸入要查詢天氣預報的城市名稱，例如：預報高雄"
    
    else:
        reply_message = "歡迎使用天氣小幫手！\n- 查詢即時天氣：『天氣[城市名稱]』\n- 查詢預報：『預報[城市名稱]』"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )


if __name__ == "__main__":
    app.run(port=8000)
