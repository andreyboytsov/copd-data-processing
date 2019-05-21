import os
import pandas as pd
import numpy as np
import pytz
import datetime

fname = "./data_generated/Patients_and_Weather_extended.csv"
average_considered_hours = [4,8,12,16,20,24,28,32,36,40,44,48]
weather_columns = ['temp','humidity','pressure','wind_speed']

# Read the csv files
weather_df = pd.read_csv("./data/weather_data.csv")
patients_df = pd.read_csv("./data/U4H_RawMonitoringData_from_20160623.csv")
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

### Merge the file to create a csv with the headers combined
patients_and_weather_df = patients_df.merge(weather_df, how='left', left_on=['patients_only_date'], right_on=['weather_only_date'])


# =========================== STEP 1. Connect to closest weather data (just like before)
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
#patients_and_weather_df.to_csv(fname)


# =========================== STEP 2. Connect to average weather data.
print('==================== STEP 2 STARTED =====================================')
patients_and_weather_df['Assess_Date_With_Time'] = pd.to_datetime(patients_and_weather_df['Assess_Date_With_Time'],
                                                                  format='%Y-%m-%d %H:%M:%S')
patients_and_weather_df['Assess_Date_With_Time'] = \
    patients_and_weather_df['Assess_Date_With_Time'].dt.tz_localize(tz='CET')
patients_and_weather_df['Assess_date_No_Time'] = patients_and_weather_df['Assess_Date_With_Time'].dt.date
for c in weather_columns:
    for h in average_considered_hours:
        patients_and_weather_df[c+"_avg"+str(h)+"h"] = 0

for index, row in patients_and_weather_df.iterrows():
    print("Row: ", index)
    for h in average_considered_hours:
        weather_subselection = weather_df[
            (row['Assess_Date_With_Time'] >= weather_df['dt_weather']) &
            ((row['Assess_Date_With_Time'] - weather_df['dt_weather']) <= datetime.timedelta(hours=h))]
        for c in weather_columns:
            # print(c, np.nanmean(weather_subselection[c]), type(np.nanmean(weather_subselection[c])))
            patients_and_weather_df.loc[index, c+"_avg"+str(h)+"h"] = np.nanmean(weather_subselection[c])
#patients_and_weather_df.to_csv(fname)


# =========================== STEP 3: Add history.
print('==================== STEP 3 STARTED =====================================')
interesting_parameters = ("pulse_Triage", "spo2_Triage", "question_Triage", "manual_Triage")
num_days = 30
for par in interesting_parameters:
    patients_and_weather_df[par + "_" + str(par)] = 0

for index, row in patients_and_weather_df.iterrows():
    print("Row: ", index)
    for d in range(1,num_days):
        subselection = patients_and_weather_df[(patients_and_weather_df['Merida ID'] == row['Merida ID']) &
            ((row['Assess_date_No_Time'] - patients_and_weather_df['Assess_date_No_Time']) < datetime.timedelta(days=d+1)) &
            ((row['Assess_date_No_Time'] - patients_and_weather_df['Assess_date_No_Time']) > datetime.timedelta(days=d-1))]
        #print("\t", len(subselection))
        for par in interesting_parameters:
            patients_and_weather_df.loc[index, par+"_"+str(d)] = np.nanmean(subselection[par])

### delete all rows in the dataframe and keep only the header so we can append later
#patients_and_weather_final = patients_and_weather_df.iloc[0:0]
patients_and_weather_df.to_csv(fname)

