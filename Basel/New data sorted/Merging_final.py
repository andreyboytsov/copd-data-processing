import pandas as pd
import datetime
from datetime import datetime

# Read the csv files
weather_df = pd.read_csv("Weather_new.csv", low_memory=False)
patients_df = pd.read_csv("Patients_new.csv")
patients_df = patients_df[patients_df['Region'].notnull()] # Remove a few last lines
patients_and_weather_df = pd.read_csv("patients_and_weather.csv")

#print(weather_df[['weather_only_date','weather_only_time']])

weather_df['weather_only_date'] = weather_df['weather_only_date'].apply(lambda i: datetime.strptime(i,'%Y-%m-%d'))
patients_df['patients_only_date'] = patients_df['patients_only_date'].apply(lambda i: datetime.strptime(i,'%d/%m/%Y'))

#patients_and_weather_df = pd.merge(patients_df,weather_df,how='left', left_on=['patients_only_date'], right_on=['weather_only_date'])
count = 0
for row in weather_df:
    print(row)
    #if patients_and_weather_df['weather_only_date'][row] == patients_and_weather_df['patients_only_date'][row]:
       # count = count + 1


#patients_and_weather_df['Differences'] = patients_and_weather_df[] - patients_and_weather_df[]

#patients_and_weather_df.to_csv("patients_and_weather.csv")

#print(type(patients_df['patients_only_date']))
#print(type(weather_df['weather_only_date']))
#print(count)