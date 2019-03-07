import pandas as pd
from datetime import datetime

# Read the csv files
weather_df = pd.read_csv("weather_data.csv")
patients_df = pd.read_csv("U4H_RawMonitoringData_from_20160623.csv")
patients_df = patients_df[patients_df['Region'].notnull()] # Remove a few last lines

# Find the weather date and time and save them separately
weather_df['dt_weather'] = weather_df['dt'].apply(lambda i: pd.Timestamp(i, unit='s', tz='CET'))
weather_df['weather_only_date'] = [d.date() for d in weather_df['dt_weather']]
weather_df['weather_only_time'] = [d.time() for d in weather_df['dt_weather']]

#weather_df['weather_only_date'] = [str(d.date()) for d in weather_df['dt_weather']]
#weather_df['weather_only_time'] = [str(d.time()) for d in weather_df['dt_weather']]

# Find the patient date and time and save them separately

patients_df['patients_only_date'] = patients_df['Assess_Date_With_Time'].apply(lambda i: i.split()[0])
patients_df['patients_only_time'] = patients_df['Assess_Date_With_Time'].apply(lambda i: i.split()[1])

patients_df['patients_only_date'] = pd.to_datetime(patients_df['patients_only_date']).apply(lambda i: i.date())
patients_df['patients_only_time'] = pd.to_datetime(patients_df['patients_only_time']).apply(lambda i: i.time())


#patients_df['patients_only_date'] = patients_df['Assess_Date_With_Time'].apply(lambda i: datetime.strptime(i.split()[0],'%Y-%m-%d'))


#######################################################################################
## Now the data is saved in 2 dataframes that has the date and time sparated as strings
#######################################################################################

weather_df.to_csv("Weather_DateTime_Separated.csv")
patients_df.to_csv("Patients__DateTime_Separated.csv")


#weather_df.sort_values(['weather_only_date', 'weather_only_time'], ascending=[True, True])
#patients_df.sort_values(['patients_only_date'], ascending=[True])


#print(patients_df[['patients_only_date','patients_only_time']])
print(patients_df['patients_only_time'][1])
print(weather_df['weather_only_time'][1])

print(patients_df['patients_only_date'][1])
print(weather_df['weather_only_date'][1])

#if patients_df['patients_only_time'][1]> weather_df['weather_only_time'][1]:
 #   print("after")
#else:
  #  print("before")