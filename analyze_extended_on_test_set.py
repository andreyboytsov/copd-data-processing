import pandas as pd
import numpy as np
from sklearn import dummy
from itertools import product
from sklearn import tree, ensemble, linear_model
from sklearn.metrics import accuracy_score

# ============================== PARAMETERS  ==============================
test_id_selection_random_seed = 0
fraction_train_ids = 0.9
# max_days = 7
# min_days = 3
max_days = 21
min_days = 1
# ============================== END PARAMETERS  ==========================

interesting_columns_weather = ['temp', 'pressure','humidity']  # TODO wind_speed ?
triage_columns = ["pulse_Triage","spo2_Triage","question_Triage","manual_Triage"]


all_data = pd.read_csv("./data_generated/Patients_and_Weather_extended.csv")
all_ids = all_data['Merida ID'].unique()
np.random.seed(test_id_selection_random_seed)
selected_ids = np.random.choice(all_ids, size = int(len(all_ids)*fraction_train_ids))

train_data = all_data[[i in selected_ids for i in all_data['Merida ID']]]
test_data = all_data[[i not in selected_ids for i in all_data['Merida ID']]]
#data = all_data

all_models = {
    "1Dummy:Majority": dummy.DummyClassifier(strategy='most_frequent'),
    "1Dummy:Stratified": dummy.DummyClassifier(random_state=0),
    "DT:default": tree.DecisionTreeClassifier(random_state=0),  # TODO Let's start like that. We will configure later.

    ##"DT-": tree.DecisionTreeClassifier(), # TODO Let's start like that. We will configure later.

    "RF:default": ensemble.RandomForestClassifier(n_estimators=10, random_state=0),
    "GBT:default": ensemble.GradientBoostingClassifier(random_state=0),
    "LR:default": linear_model.LogisticRegression(solver='liblinear', multi_class='ovr', random_state=0),
}

# ==================== GRID SEARCH ====================================
# ======== Logistic regression
regularization_pars = (1e-6, 3e-6, 6e-6, 1e-5, 3e-5, 6e-5,
           1e-4, 3e-4, 6e-4, 1e-3, 3e-3, 6e-3,
           1e-2, 3e-2, 6e-2, 1e-1, 3e-1, 6e-1,
           1, 3, 6, 10, 30, 60, 100, 300, 600)
for penalty in ('l2', 'l1'):
    for reg in regularization_pars:
       all_models["LR:"+penalty+"-"+str(reg)] = \
           linear_model.LogisticRegression(solver='liblinear', multi_class='ovr', random_state=0, C=reg,
                                           penalty=penalty)
# ======== Random forest
for num_estimators in [5, 10, 20, 50, 100]:
    for max_depth in [2,3,4,5,10, None]:
       for max_features in ['auto','log2',None]:
           all_models['RF:'+str(num_estimators)+'-'+str(max_depth)+'-'+str(max_features)] = \
               ensemble.RandomForestClassifier(n_estimators=num_estimators, max_depth=max_depth,
                                               max_features=max_features, random_state=0)

# ======== Gradient boosted trees
for num_estimators in [5, 10, 20, 50, 100]:
    for max_depth in [2,3,4,5,10, None]:
        all_models['RF:'+str(num_estimators)+'-'+str(max_depth)+'-'+str(max_features)] = \
             ensemble.GradientBoostingClassifier(n_estimators=num_estimators, max_depth=max_depth,
                                                 random_state=0)

# ======== Decision trees
for max_depth in [5,10,20,50,None]:
    for max_features in ['auto', 'log2', None]:
        all_models['DT:' + str(max_depth) + '-' + str(max_features)] = \
            tree.DecisionTreeClassifier(max_depth=max_depth, max_features=max_features, random_state=0)

# ==================== END GRID SEARCH ====================================



def print_training_results(columns, triages=triage_columns, features="Weather", print_rules=False,
                           df_to_append=None, skip_existing=False, hist_days=-1, weather_avg_h=-1):
    if df_to_append is None:
        output_df = pd.DataFrame(columns=["Triage", "Features", "History_days","Weather_avg_h",
                                      "Model", "Parameters", "NumTrgSamples", "NumTestSamples",
                                      "TrainAcc", "TestAcc", "Precision", "Recall", "F1",
                                      "TP","TN","FP","FN"])
    else:
        output_df = df_to_append

    for cur_triage in triages:
        output_exists = np.where(~np.isnan(train_data[cur_triage]))[0]
        test_output_exists = np.where(~np.isnan(test_data[cur_triage]))[0]

        # Taking only history
        train_X = train_data.iloc[output_exists, :][columns]
        train_Y = np.array(train_data.iloc[output_exists, :][[cur_triage]]).ravel()

        test_X = test_data.iloc[test_output_exists, :][columns]
        test_Y = np.array(test_data.iloc[test_output_exists, :][[cur_triage]]).ravel()

        train_X = np.array(train_X.fillna(0))
        test_X = np.array(test_X.fillna(0))

        for m in sorted(all_models):
            line_exists = np.sum((output_df["Triage"]==cur_triage) &
                                 (output_df["Features"]==features) &
                                 (output_df["Model"]==m.split(':')[0]) &
                                 (output_df["Parameters"]==m.split(':')[1]) &
                                 (output_df["History_days"]==hist_days) &
                                 (output_df["Weather_avg_h"]==weather_avg_h)) > 0
            if skip_existing and line_exists:
                print("============== SKIPING Model: ", m, cur_triage)
                continue

            print("============== Model: ", m, cur_triage, '=========')

            model = all_models[m]

            print(np.array(train_X).shape)

            model = model.fit(train_X, train_Y)
            train_res = model.predict(train_X)
            test_res = model.predict(test_X)

            train_results = accuracy_score(train_res, train_Y)
            test_results = accuracy_score(test_res, test_Y)

            true_positive = np.sum((test_Y > 1) & (test_res > 1))
            true_negative = np.sum((test_Y == 1) & (test_res == 1))
            false_positive = np.sum((test_Y == 1) & (test_res > 1))
            false_negative = np.sum((test_Y > 1) & (test_res == 1))

            if true_positive > 0 or false_positive > 0:
                precision = true_positive / (true_positive + false_positive)
            else:
                precision = 0

            if true_positive > 0 or false_negative > 0:
                recall = true_positive / (true_positive + false_negative)
            else:
                recall = 0

            if precision > 0 or recall > 0:
                f1 = 2 * precision * recall / (precision + recall)
            else:
                f1 = 0

            # print(confusion_matrix(test_res, cur_Y_test>1))

            if m == "1Dummy:Majority":
                dummy_train_results = np.mean(train_results)
                dummy_test_results = np.mean(test_results)
            output_line = {"Triage": cur_triage,
                           "Features": features,
                           "History_days": hist_days,
                           "Weather_avg_h": weather_avg_h,
                           "Model": m.split(':')[0],
                           "Parameters": m.split(':')[1],
                           "NumTrgSamples": len(train_Y),
                           "NumTestSamples": len(test_Y),
                           "TrainAcc": np.mean(train_results),
                           "TestAcc": np.mean(test_results),
                           "Precision": np.mean(precision),
                           "Recall": np.mean(recall),
                           "ImprOverMajTrain": np.mean(train_results) - dummy_train_results,
                           "ImprOverMajTest": np.mean(test_results) - dummy_test_results,
                           "F1": np.mean(f1),
                           "TP" : np.mean(true_positive),
                           "FP" : np.mean(false_positive),
                           "TN": np.mean(true_negative),
                           "FN": np.mean(false_negative),
                           }
            print("Num training samples: ", output_line["NumTrgSamples"])
            print("Num test samples: ", output_line["NumTestSamples"])
            print("TRAIN: ", output_line["TrainAcc"])
            print("TEST: ", output_line["TestAcc"])
            print("TRAIN (improved over majority): ", output_line["ImprOverMajTrain"])
            print("TEST  (improved over majority): ", output_line["ImprOverMajTest"])
            print("True positive: ", output_line["TP"])
            print("False positive: ", output_line["FP"])
            print("True negative : ", output_line["TN"])
            print("False negative: ", output_line["FN"])
            print("Precision: ", output_line["Precision"])
            print("Recall: ", output_line["Recall"])
            print("F1: ", output_line["F1"])

            output_df = output_df.append(output_line, ignore_index=True)
    return output_df


if __name__=="__main__":

    # ================== STEP 1. History only
    results_df = pd.DataFrame(columns=["Triage", "Features", "History_days", "Weather_avg_h",
                            "Model", "Parameters", "NumTrgSamples", "NumTestSamples",
                            "TrainAcc", "TestAcc", "Precision", "Recall", "F1",
                            "TP", "TN", "FP", "FN"])
    for days in range(min_days,max_days):
        history_dfs = list()
        for cur_triage in triage_columns:
            history_dfs.append(
                print_training_results([cur_triage + "_" + str(i) for i in range(1, days + 1)],
                                       triages=[cur_triage],
                                       features="History", hist_days=days))
        results_df = pd.concat([results_df] + history_dfs, axis=0, sort=False)

    # ================== STEP 2. Weather & history
    for weather_avg in [16,20,24,28,32,36,40,44,48]:
        if weather_avg>0:
            interesting_columns = [i+'_avg'+str(weather_avg)+'h' for i in interesting_columns_weather]
            weather_hours_avg = weather_avg
        else:
            interesting_columns = interesting_columns_weather
            weather_hours_avg = -1

        results_df = pd.concat([results_df, print_training_results(interesting_columns,
                    features="Weather", weather_avg_h=weather_avg)], axis=0, sort=False)

        history_dfs = list()

        for days in range(min_days,max_days):
            for cur_triage in triage_columns:
                history_dfs.append(
                    print_training_results(interesting_columns +
                                                        [cur_triage + "_" + str(i) for i in range(1, days+1)],
                                       triages=[cur_triage],
                                       features="Weather & History", hist_days=days, weather_avg_h=weather_avg))


        results_df = pd.concat([results_df] + history_dfs, axis=0, sort=False)

        results_df.to_csv("./data_generated/final_results_test_set_4.csv")

    # TODO Collapse grid search
