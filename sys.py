import pandas as pd
import requests


youbike = requests.get('https://apis.youbike.com.tw/json/station-yb2.json').json()
df = pd.DataFrame(youbike)

print(df)
print(df.at[0,'area_code'])
area = df.loc[:,'area_code']
counts= df.groupby('area_code').size()
print(counts)



