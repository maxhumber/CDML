import pandas as pd
from gazpacho import get, Soup
from tqdm import tqdm
import random
import time
from matplotlib import pyplot as plt

START = '2020-03-17'

# power - historical

df = pd.read_csv("http://reports.ieso.ca/public/Demand/PUB_Demand_2020.csv", skiprows=3)
df['date'] = df.apply(lambda row: pd.to_datetime(f'{row.Date} {row.Hour-1}:00'), axis=1)
df = df.rename(columns={'Ontario Demand': 'demand'})
df = df[['date', 'demand']]
df = df[df['date'] >= START]
df = df.reset_index(drop=True)
# df['Date'].dt.day_name()
# df['Date'].dt.weekday
power = df
power.to_csv('data/power.csv', index=False)

# power - today

url = 'http://www.ieso.ca/en/Power-Data'
html = get(url)
soup = Soup(html)
soup.find('span', {'class': 'data-item-mw'}, mode='first').text
soup.find('span', {'class': 'data-item-subtitle'}, mode='first').text

# weather

url = "https://climate.weather.gc.ca/climate_data/hourly_data_e.html"

def make_soup(month, day):
    params = {
        "StationID": 31688,
        "Year": 2020,
        "Month": month,
        "Day": day
    }
    html = get(url, params)
    soup = Soup(html)
    return soup

def parse_tr(tr):
    hour = int(tr.find('th', mode='first').text.split(':')[0])
    try:
        temp = float(tr.find('td', mode='first').text)
    except TypeError:
        temp = None
    return {'hour': hour, 'temp': temp}

def extract_info(soup):
    table = soup.find('div', {'id': 'dynamicDataTable'})
    trs = table.find('tr')[1:]
    tr = trs[0]
    info = [parse_tr(tr) for tr in trs]
    return info

def date_to_info(date):
    soup = make_soup(date.month, date.day)
    info = extract_info(soup)
    info = [{**{'month': date.month, 'day': date.day}, **i} for i in info]
    return info

temps = []

dates = pd.date_range(start='START', end='today')
for date in tqdm(dates):
    try:
        info = date_to_info(date)
        temps.extend(info)
        time.sleep(random.uniform(1, 10) / 10)
    except ValueError:
        pass

df = pd.DataFrame(temps)
df['date'] = df.apply(lambda row:
    pd.to_datetime(f'2020-{int(row.month)}-{int(row.day)} {row.hour}:00'),
    axis=1)
df = df.rename(columns={'temp': 'temperature'})
df = df[['date', 'temperature']]
df = df[(df['date'] >= '2020-03-17')]
df = df.reset_index(drop=True)
temp = df
temp.to_csv('data/temperature.csv', index=False)


# stitch

df = pd.merge(power, temp, how='left', on='date')
df.to_csv('data/temp2power.csv', index=False)


# quick EDA

plt.scatter(df['temperature'], df['demand'], alpha=1/20)

plt.plot(df['date'], df['demand'])
plt.plot(df['date'], df['temperature'])
