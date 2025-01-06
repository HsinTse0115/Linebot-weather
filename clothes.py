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