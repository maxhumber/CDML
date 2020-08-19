import time
import random
import pandas as pd
from tqdm import tqdm

def fetch_year(year):
    url = f"http://reports.ieso.ca/public/DemandZonal/PUB_DemandZonal_{year}.csv"
    df = pd.read_csv(url, skiprows=3)
    return df

df = pd.DataFrame()
for year in tqdm([2018, 2019, 2020]):
    df = df.append(fetch_year(year))
    time.sleep(random.uniform(1,10)/10)

df['date'] = df.apply(lambda row: pd.to_datetime(f'{row.Date} {row.Hour-1}:00'), axis=1)
df = df.rename(columns={
    'Ontario Demand': 'ontario_demand_mw',
    'Toronto': 'toronto_demand_mw'
})
df = df[['date', 'ontario_demand_mw', 'toronto_demand_mw']].reset_index(drop=True)

df.to_csv('data/power.csv', index=False)
