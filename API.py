LINE_CHANNEL_ACCESS_TOKEN = '4Lwc7G+7yk36dGGQ3UYDltYfEdeN6ABrcigeWbp7Ayd0DOVVQqN2qeyiELXZYo7X2iOe9wUBCEATz/VNzOyiz/4NpLPk46f01cHGlY6b9nptYBjYwMwsqyZ4hzMySsbnQ8khh4OTmv+1c7jVu1yKKAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'addf11df61483cbc918958014c227b5e'
WEATHER_API_KEY = '6b6125fbba974b8e8a6fed683a1b5c4b'

from config import WEATHER_API_KEY, LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
# LINE API 配置
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=zh_tw"
