#import os
import pandas as pd
#import numpy as np

hourly_weather_df = pd.read_csv("weather_data.csv")
hourly_weather_df['dt_local'] = hourly_weather_df['dt'].apply(lambda i: pd.Timestamp(i, unit='s', tz='CET'))
hourly_weather_df['day_local'] = hourly_weather_df['dt_local'].apply(lambda i: pd.Timestamp(day=i.day, month=i.month, year=i.year))

daily_weather = hourly_weather_df.groupby('day_local')

#print(hourly_weather_df['dt_local'])
def daily_aggregation(x):
    names = {
        'temp_daily_min': x['temp_min'].min() - 273.15,
        'temp_daily_max': x['temp_max'].max() - 273.15,
        'pressure_min': x['pressure'].min(),
        'pressure_max': x['pressure'].max(),
        'clouds_min': x['clouds_all'].min(),
        'clouds_max': x['clouds_all'].max()
    }

    return pd.Series(names, index=reversed(sorted(names.keys())))


daily_weather_df = daily_weather.apply(daily_aggregation)
daily_weather_df.to_csv("daily_weather.csv")

