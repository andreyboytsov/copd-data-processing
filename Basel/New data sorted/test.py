import csv

with open('patients_and_weather.csv', newline='') as File:
    reader = csv.reader(File)
    count = 0
    for row in reader:
        if row['weather_only_date'] < '26/12/2014':
            print(row['weather_only_date'])

