import os
import pandas as pd
import numpy as np

# ============================== CONFIGURATION ===============================
input_data_dir = 'data'
generated_data_dir = 'data_generated'

do_regenerate_daily_weather = True
do_join_patients_and_weather = True

daily_weather_file = 'daily_weather.csv'
hourly_weather_file = 'weather_data.csv'
patients_data_file = 'U4H_RawMonitoringData_from_20160623.csv'
patients_and_weather_data_file = 'daily_patients_weather.csv'
# ============================== END OF CONFIGURATION ===============================


daily_weather_full_filename = generated_data_dir + os.path.sep + daily_weather_file
if do_regenerate_daily_weather or not os.path.isfile(daily_weather_full_filename):
    hourly_weather_df = pd.read_csv(input_data_dir+os.path.sep+hourly_weather_file)
    hourly_weather_df['dt_local'] = hourly_weather_df['dt'].apply(lambda i: pd.Timestamp(i, unit='s', tz='CET'))
    hourly_weather_df['day_local'] = hourly_weather_df['dt_local'].apply(lambda i : pd.Timestamp(day=i.day,
                                                                                    month=i.month, year=i.year))

    daily_weather = hourly_weather_df.groupby('day_local')

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
    daily_weather_df.to_csv(daily_weather_full_filename)
    del daily_weather_df  # For clean experiment

if do_join_patients_and_weather:
    daily_weather_df = pd.read_csv(daily_weather_full_filename)
    patients_df = pd.read_csv(input_data_dir+os.path.sep+patients_data_file)
    patients_df = patients_df[patients_df['Region'].notnull()] # Remove a few last lines
    # Those are status like "Number of patients: ", not really part of the table

    patients_df['Assess_date_No_Time'] = patients_df['Assess_date_No_Time'].apply(lambda i: pd.Timestamp(i))
    daily_weather_df['day_local'] = daily_weather_df['day_local'].apply(lambda i: pd.Timestamp(i))

    patients_and_weather_df = patients_df.merge(daily_weather_df, how='left',
                                                left_on=['Assess_date_No_Time'],
                                                right_on=['day_local'])
    print("Number of records with missing weather data: ", np.sum(patients_and_weather_df['day_local'].apply(lambda i: np.isnan(i.day))))
    patients_and_weather_df.to_csv(generated_data_dir + os.path.sep + patients_and_weather_data_file)

