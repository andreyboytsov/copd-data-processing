
import pandas as pd


daily_weather_df = pd.read_csv("daily_weather.csv")
patients_df = pd.read_csv("U4H_RawMonitoringData_from_20160623.csv")
patients_df = patients_df[patients_df['Region'].notnull()] # Remove a few last lines

daily_weather_df['day_local'] = daily_weather_df['day_local'].apply(lambda i: pd.Timestamp(i))
patients_df['Assess_date_No_Time'] = patients_df['Assess_date_No_Time'].apply(lambda i: pd.Timestamp(i))

patients_and_weather_df = patients_df.merge(daily_weather_df, how='left', left_on=['Assess_date_No_Time'], right_on=['day_local'])
patients_and_weather_df.to_csv("patients_and_weather.csv")
