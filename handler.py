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