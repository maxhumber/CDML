import time
import random
from gazpacho import get, Soup
import pandas as pd
from tqdm import tqdm

START = pd.Timestamp('2018-01-01')
END = pd.Timestamp('today')

url = "https://climate.weather.gc.ca/climate_data/hourly_data_e.html"

def make_soup(date):
    if not isinstance(date, pd.Timestamp):
        date = pd.Timestamp(date)
    params = {
        "StationID": 31688,
        "Year": date.year,
        "Month": date.month,
        "Day": date.day
    }
    html = get(url, params)
    soup = Soup(html)
    return soup

def parse_tr(tr):
    hour = int(tr.find('th', mode='first').text.split(':')[0])
    try:
        temperature = float(tr.find('td', mode='first').text)
    except TypeError:
        temperature = None
    return {'hour': hour, 'temperature': temperature}

def extract_info(soup):
    table = soup.find('div', {'id': 'dynamicDataTable'})
    trs = table.find('tr')[1:]
    tr = trs[0]
    info = [parse_tr(tr) for tr in trs]
    return info

def fetch_temperature(date):
    soup = make_soup(date)
    info = extract_info(soup)
    info = [{**{'date': date}, **i} for i in info]
    return info

temperatures = []
for date in tqdm(pd.date_range(start=START, end=END)):
    try:
        temperatures.extend(fetch_temperature(date))
        time.sleep(random.uniform(1, 10) / 10)
    except ValueError:
        pass

df = pd.DataFrame(temperatures)

df['date'] = df.apply(lambda row: pd.to_datetime(f'{date} {row.hour}:00'), axis=1)
df = df[['date', 'temperature']]
df = df.reset_index(drop=True)

df.to_csv('data/weather.csv', index=False)
