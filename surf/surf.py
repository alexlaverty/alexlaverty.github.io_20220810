import json
import re
import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd
from datetime import datetime
import pytz

class seabreeze():

    def __init__(self):
        """ Init of the client """
        self.location = "sydney"
        self.url = "https://www.seabreeze.com.au/weather/wind-forecast/%s" % (self.location)
        self.local = "sample-index.html"
        self.json = {}
        self.desired_temp = 20
        self.max_precip = 50
        self.max_wind = 10
        self.max_waves = 2
        self.headers = [
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

        self.dataframe = pd.DataFrame(columns=self.headers)

    def load_json(self):
        if args.local:
            print("Parsing local file : %s" % (self.local))
            soup = BeautifulSoup(open(self.local, encoding="utf8"), 'html.parser')
        else:
            page = requests.get(self.url)         
            soup = BeautifulSoup(page.content, "html.parser")

        # Needs a better regex expression
        pattern = re.compile(r'var json={.*};', re.DOTALL)

        script = soup.find('script', text=pattern)
        
        data = pattern.search(script.text).group(0)

        # tidies beginning and end of json string so json.loads works correctly
        data = data.replace("var json=", "")
        data = data.replace("};", "}")

        self.json = json.loads(data)

    def print_json(self, data):
        print(json.dumps(data, indent=4, sort_keys=True))

    def forecast(self):
        return self.json["forecasts"][0]["forecast"]

    def rate(self, day):
            rating = 0

            if day["maxTemp"] > self.desired_temp:
                rating += 1

            if day["weatherIcon"] != "Shower":
                rating += 1

            if day["probabilityPrecip"] < self.max_precip:
                rating += 1

            if self.get_wind(day["wind"])['Knots'].mean() < self.max_wind:
                rating += 1

            if self.get_waves(day["waves"])['Height'].mean() < self.max_waves:
                rating += 1

            return rating 

    def get_waves(self, day):
        #print(waves)
        wave_data = day['waves'].split(",")
        del wave_data[0]
        wave_data = [wave_data[i:i+5] for i in range(0, len(wave_data), 5)]
        headers = ['hour','minute','waveheight','wavedirection','waveperiod']
        df = pd.DataFrame(wave_data,columns=headers)
        df["waveheight"] = pd.to_numeric(df["waveheight"])
        df["waveperiod"] = pd.to_numeric(df["waveperiod"])
        df["wavedirection"] = pd.to_numeric(df["wavedirection"])
        return df
        
    def get_wind(self, day):
        wind_data = day['wind'].split(",")
        del wind_data[0]
        wind_data = [wind_data[i:i+4] for i in range(0, len(wind_data), 4)]
        headers = ['hour','minute','knots','winddirection']
        df = pd.DataFrame(wind_data, columns=headers)
        df["knots"] = pd.to_numeric(df["knots"])
        df["winddirection"] = pd.to_numeric(df["winddirection"])
        return df

    def get_temperature(self, day):
        temperature_data = day['temperature'].split(",")
        del temperature_data[0]
        temperature_data = [temperature_data[i:i+3] for i in range(0, len(temperature_data), 3)]
        headers = ['hour','minute','temperature']
        df = pd.DataFrame(temperature_data, columns=headers)
        df["temperature"] = pd.to_numeric(df["temperature"])
        return df

    def print_forecast(self):
        print("Seabreeze.com.au Forecast")
        print("Location : %s" % (s.location))

        for day in self.forecast():
            print("-----------------------------")
            print("Date             : %s" % (day["localDate"])) 
            print("Day              : %s" % (day["day"])) 
            print("Max Temperature  : %s" % (day["maxTemp"])) 
            print("Weather          : %s" % (day["weatherIcon"])) 
            print("Chance of Rain   : %s %%" % (day["probabilityPrecip"])) 
            print("Amount of Rain   : %s" % (day["rangePrecipText"])) 

    def print_table(self):
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Seabreeze Scraper')
    parser.add_argument('-l', '--local', action='store_true')
    args = parser.parse_args()

    s = seabreeze()

    data = s.load_json()

    forcast = s.forecast()

    for day in forcast:

        data = []

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
    
        df = pd.DataFrame(data, columns=s.headers)


        df_wave = s.get_waves(day)
       
        df_wave['localDate']         = day['localDate']
        df_wave['day']               = day['day']
        df_wave['minTemp']           = day['minTemp']
        df_wave['maxTemp']           = day['maxTemp']
        df_wave['weatherIcon']       = day['weatherIcon']
        df_wave['shortDesc']         = day['shortDesc']
        df_wave['probabilityPrecip'] = day['probabilityPrecip']
        df_wave['rangePrecipText']   = day['rangePrecipText']
        df_wave['sunrise']           = day['sunrise']
        df_wave['sunset']            = day['sunset']
        df_wave['moonPhase']         = day['moonPhase']

        df_wind = s.get_wind(day)
        #print(df_wave)
        df_wave = df_wave.merge(df_wind, how='left', on=['hour','minute'])

        #df_temperature = s.get_temperature(day)
        
        #df_wave = df_wave.merge(df_temperature, how='right', on=['hour','minute'])
        
        s.dataframe = s.dataframe.append(df_wave, ignore_index=True)

    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    index_names = {
        'selector': '.index_name',
        'props': ''
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #000066; color: white;'
    }

    s.dataframe["hour"] = pd.to_numeric(s.dataframe["hour"])
    s.dataframe["minute"] = pd.to_numeric(s.dataframe["minute"])

    df_filtered = s.dataframe[s.dataframe.knots < 15 ]
    df_filtered = df_filtered[(df_filtered['hour'] >= 6) & (df_filtered['hour'] <= 18)]
    df_filtered = df_filtered[df_filtered.probabilityPrecip <= 70 ]
    df_filtered = df_filtered[df_filtered.waveheight < 2 ]

    with pd.option_context('display.precision', 1):
        df_style = df_filtered.style

    df_style.hide_index()
    df_style.applymap(lambda x: f"background-color: {'lightgreen' if (x > 6 and x < 20) else '#ffcccb'}", subset=['hour'])
    df_style.applymap(lambda x: f"background-color: {'#ffcccb' if 'Shower' in x else 'lightgreen'}", subset=['weatherIcon'])
    df_style.applymap(lambda x: f"background-color: {'#ffcccb' if x > 50 else 'lightgreen'}", subset=['probabilityPrecip'])
    #df_style.applymap(lambda x: f"background-color: {'green' if x >= 20 else 'red'}", subset=['temperature'])
    df_style.applymap(lambda x: f"background-color: {'lightgreen' if x >= 10 else '#ffcccb'}", subset=['waveperiod'])
    df_style.applymap(lambda x: f"background-color: {'lightgreen' if x <= 10 else '#ffcccb'}", subset=['knots'])
    df_style.applymap(lambda x: f"background-color: {'lightgreen' if (x > 225 and x < 315) else '#ffcccb'}", subset=['winddirection'])
    df_style.applymap(lambda x: f"background-color: {'lightgreen' if (x > 40 and x < 250) else '#ffcccb'}", subset=['wavedirection'])
    df_style.applymap(lambda x: f"background-color: {'lightgreen' if x < 2 else '#ffcccb'}", subset=['waveheight'])

    df_style.hide_columns(["minTemp", "maxTemp","moonPhase","shortDesc","sunrise","sunset"])
    
    html = df_style.format().set_table_styles([cell_hover, headers])
    tz_Aus = pytz.timezone('Australia/Sydney')
    datetime_Aus = datetime.now(tz_Aus)
    
    html = html.render()
    last_updated_time  = "Page last updated :" + datetime_Aus.strftime("%A, %d/%m/%Y %I:%M:%S %p")
    html = last_updated_time + html
    
    #write html to file
    text_file = open("index.html", "w")
    text_file.write(html)
    text_file.close()