import pandas as pd
import numpy as np
import os

fname = "Patients_and_Weather.csv"

# Read the csv files
weather_df = pd.read_csv("files/weather_data.csv")
patients_df = pd.read_csv("files/U4H_RawMonitoringData_from_20160623.csv")
patients_df = patients_df[patients_df['Region'].notnull()] # Remove a few last lines

# Find the weather date and time and save them separately
weather_df['dt_weather'] = weather_df['dt'].apply(lambda i: pd.Timestamp(i, unit='s', tz='CET'))
weather_df['weather_only_date'] = [d.date() for d in weather_df['dt_weather']]
weather_df['weather_only_time'] = [d.time() for d in weather_df['dt_weather']]

# Find the patient date and time and save them separately
patients_df['patients_only_date'] = patients_df['Assess_Date_With_Time'].apply(lambda i: i.split()[0])
patients_df['patients_only_time'] = patients_df['Assess_Date_With_Time'].apply(lambda i: i.split()[1])

# Find the weather date and time and save them separately
patients_df['patients_only_date'] = pd.to_datetime(patients_df['patients_only_date']).apply(lambda i: i.date())
patients_df['patients_only_time'] = pd.to_datetime(patients_df['patients_only_time']).apply(lambda i: i.time())


#patients_df['patients_only_date'] = patients_df['Assess_Date_With_Time'].apply(lambda i: datetime.strptime(i.split()[0],'%Y-%m-%d'))

### Merge the file to create a csv with the headers combined
patients_and_weather_df = patients_df.merge(weather_df, how='left', left_on=['patients_only_date'], right_on=['weather_only_date'])

patients_and_weather_df["time_difference"] = patients_and_weather_df.apply(lambda x: np.abs(
                                               (x['patients_only_time'].hour - x['weather_only_time'].hour)*3600+
                                               (x['patients_only_time'].minute - x['weather_only_time'].minute)*60+
                                               (x['patients_only_time'].second - x['weather_only_time'].second)),
                                               axis=1)

pawdf_grouped = patients_and_weather_df.groupby(by=["Merida ID", "Assess_Date_With_Time"])

def select_lowest_time_diff(x):
    index = np.where(x["time_difference"] == x["time_difference"].min())[0][0]
    return x.iloc[index, :]

patients_and_weather_df = pawdf_grouped.apply(select_lowest_time_diff)

### delete all rows in the dataframe and keep only the header so we can append later
#patients_and_weather_final = patients_and_weather_df.iloc[0:0]
patients_and_weather_df.to_csv('files/'+fname)

#for index, row in patients_and_weather_df.iterrows():
    #print(index, row['Region'])
#    if (row['patients_only_date'] == row['weather_only_date']) and (row['patients_only_time'] > row['weather_only_time']):
#        continue

        #patients_and_weather_df.drop([index],axis = 0, inplace = True)
#    print(index)
#patients_and_weather_df = patients_and_weather_df.groupby('patients_only_date')







#print(patients_df[['patients_only_date','patients_only_time']])
#print(patients_df['patients_only_time'][1])
#print(weather_df['weather_only_time'][1])

#print(patients_df['patients_only_date'][1])
#print(weather_df['weather_only_date'][1])

#print(patients_and_weather_df['patients_only_date'][1])
#print(patients_and_weather_df['patients_only_date'][2])



