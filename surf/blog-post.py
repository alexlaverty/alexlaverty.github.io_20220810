from bs4 import BeautifulSoup
import requests 

url = "https://www.seabreeze.com.au/weather/wind-forecast/sydney"

page = requests.get(url)         
soup = BeautifulSoup(page.content, "html.parser")

#print(soup)


import re
import json

# Needs a better regex expression
pattern = re.compile(r'var json={.*};', re.DOTALL)

script = soup.find('script', text=pattern)

data = pattern.search(script.text).group(0)

# tidies beginning and end of json string so json.loads works correctly
data = data.replace("var json=", "")
data = data.replace("};", "}")

json = json.loads(data)

forecast = json["forecasts"][0]["forecast"]

for day in forecast:
    print("--------------------------")
    print(day['sunrise'])
    print(day['sunset'])


headers = [
            'localDate',
            'day',
            'hour',
            'minute',
            'minTemp',
            'maxTemp',
            'shortDesc',
            'weatherIcon',
            'probabilityPrecip',
            'rangePrecipText',
            'sunrise',
            'sunset',
            'moonPhase'
        ]

import pandas as pd



data = []

for day in forecast:  

        data.append(
            [
                day['localDate'],
                day['day'],
                "0",
                "0",
                day['minTemp'],
                day['maxTemp'],
                day['shortDesc'],
                day['weatherIcon'],
                day['probabilityPrecip'],
                day['rangePrecipText'],
                day['sunrise'],
                day['sunset'],
                day['moonPhase']
            ]
        )

        wave_data = day['waves'].split(",")
        del wave_data[0]
        wave_data = [wave_data[i:i+5] for i in range(0, len(wave_data), 5)]
        headers = ['hour','minute','waveheight','wavedirection','waveperiod']
        df_wave = pd.DataFrame(wave_data,columns=headers)
        df_wave["waveheight"] = pd.to_numeric(df_wave["waveheight"])
        df_wave["waveperiod"] = pd.to_numeric(df_wave["waveperiod"])
        df_wave["wavedirection"] = pd.to_numeric(df_wave["wavedirection"])
        # print("================")
        # print(df_wave) 
        # print("================")

df = pd.DataFrame(data, columns=headers)

#print(df)