import pytz
import pandas as pd
import os
import fitbit
from jinja2 import Template
from datetime import datetime

FITBIT_ACCESS_TOKEN = os.environ['FITBIT_ACCESS_TOKEN']
FITBIT_CONSUMER_KEY = os.environ['FITBIT_CONSUMER_KEY']
FITBIT_CONSUMER_SECRET = os.environ['FITBIT_CONSUMER_SECRET']
FITBIT_REFRESH_TOKEN = os.environ['FITBIT_REFRESH_TOKEN']

print(FITBIT_CONSUMER_KEY)
print(FITBIT_REFRESH_TOKEN)

tz_Aus = pytz.timezone('Australia/Sydney')
datetime_Aus = datetime.now(tz_Aus)
today = datetime_Aus.strftime("%Y-%m-%d")

authd_client = fitbit.Fitbit(FITBIT_CONSUMER_KEY, 
                            FITBIT_CONSUMER_SECRET,
                            access_token=FITBIT_ACCESS_TOKEN, 
                            refresh_token=FITBIT_REFRESH_TOKEN,
                            system='METRIC')

data = authd_client.get_bodyweight()

print(data)

df = pd.DataFrame.from_dict(data['weight'])

print(df)

weight = df["weight"].mean().astype(int)
bmi = df["bmi"].mean().astype(int)

with open('index.html.j2') as file_:
    template = Template(file_.read())

html = template.render(last_updated=datetime_Aus.strftime("%A, %d/%m/%Y %I:%M:%S %p"),
                       data=data, 
                       bmi=bmi,
                       weight=weight)

#print(html)

with open("index.html", "w") as fh:
    fh.write(html)
