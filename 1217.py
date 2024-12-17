import os
import google.generativeai as generativeai

say = input()
generativeai.configure(api_key="AIzaSyBlM3vOqg12mzGzx4axKdsF4uTBQ64gkTk")
response = generativeai.GenerativeModel('gemini-2.0-flash-exp').generate_content(say)
print(response.text)