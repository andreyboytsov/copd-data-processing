#Author: Ayan Chatterjee (ayan.chatterjee@uia.no or ayan1.c2@gmail.com) - Ph.D. Research fellow in ICT-eHealth, Norway

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from sklearn.preprocessing import LabelEncoder  
#from sklearn.preprocessing import OneHotEncoder
import warnings 
warnings.filterwarnings("ignore")
#from sklearn.model_selection import train_test_split
#from sklearn.svm import SVC
#from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
#from pylab import savefig

sns.color_palette("husl")
sns.set(style="ticks", color_codes=True)

data = 'sourcefiles/Patients_and_Weather.csv'

#interesting_columns_weather = ['manual_Triage', 'temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg', 'rain_1h', 'rain_3h', 'rain_24h', 'rain_today', 'snow_1h', 'snow_3h', 'snow_24h', 'snow_today', 'clouds_all']
#interesting_columns_weather = ['manual_Triage', 'temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg', 'rain_3h', 'snow_3h', 'snow_24h', 'clouds_all']
#interesting_columns_weather = ['manual_Triage', 'temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg', 'clouds_all']
interesting_columns_weather = ['manual_Triage', 'temp', 'pressure', 'humidity']


data = pd.read_csv(data)
#print data.shape

data = pd.DataFrame(data, columns = interesting_columns_weather)
data.head()

data = data.dropna()
dataset = data
#print data.shape

#plotting dependency
sns.scatterplot(x=dataset.manual_Triage, y=dataset.temp);
sns.lineplot(x=dataset.manual_Triage, y=dataset.temp);
plt.xlabel('manual_Triage')
plt.ylabel('temp')
plt.title('Dependency-1')
plt.savefig("images/dependency-temp.png", dpi=200)
plt.show()

sns.scatterplot(x=dataset.manual_Triage, y=dataset.pressure);
sns.lineplot(x=dataset.manual_Triage, y=dataset.pressure);
plt.xlabel('manual_Triage')
plt.ylabel('pressure')
plt.title('Dependency-2')
plt.savefig("images/dependency-pressure.png", dpi=200)
plt.show()

sns.scatterplot(x=dataset.manual_Triage, y=dataset.humidity);
sns.lineplot(x=dataset.manual_Triage, y=dataset.humidity);
plt.xlabel('manual_Triage')
plt.ylabel('humidity')
plt.title('Dependency-3')
plt.savefig("images/dependency-humidity.png", dpi=200)
plt.show()

data.to_csv('destinationfiles/Patients_and_Weather_refined.csv')

#label_encoder = LabelEncoder()
#data.iloc[:,0] = label_encoder.fit_transform(data.iloc[:,0]).astype('int8')
#print data.info()

corr = data.corr()
#print corr.head()
#print corr.shape
corr.to_csv('destinationfiles/corr.csv')

sns.heatmap(corr)
plt.savefig("images/corr.png", dpi=200)
plt.show()

#Next, we compare the correlation between features and remove one of two features that have a correlation higher than 0.9
columns = np.full((corr.shape[0],), True, dtype=bool)
for i in range(corr.shape[0]):
    for j in range(i+1, corr.shape[0]):
        if corr.iloc[i,j] >= 0.9:
            if columns[j]:
                columns[j] = False
                
selected_columns = data.columns[columns]
#print selected_columns.shape

data = data[selected_columns]

selected_columns = selected_columns[1:].values         # Removing the manual_Triage column as it will be predicted

import statsmodels.formula.api as sm
def backwardElimination(x, Y, sl, columns):
    numVars = len(x[0])
    for i in range(0, numVars):
        regressor_OLS = sm.OLS(Y, x).fit()
        maxVar = max(regressor_OLS.pvalues).astype(float)
        if maxVar > sl:
            for j in range(0, numVars - i):
                if (regressor_OLS.pvalues[j].astype(float) == maxVar):
                    x = np.delete(x, j, 1)
                    columns = np.delete(columns, j)
                    
    regressor_OLS.summary()
    return x, columns

#define confidence factor for P-Value
SL = 0.05
data_modeled, selected_columns = backwardElimination(data.iloc[:,1:].values, data.iloc[:,0].values, SL, selected_columns)

#Moving the result to a new dataframe
result = pd.DataFrame()
result['manual_Triage'] = data.iloc[:,0]

#print result['manual_Triage'], result['manual_Triage'].shape

#Creating a dataframe with the columns selected using the p-value and correlation
data = pd.DataFrame(data = data_modeled, columns = selected_columns)
print data.shape
data.to_csv('destinationfiles/p_val_Ha.csv') #store alternative hypothesis data


