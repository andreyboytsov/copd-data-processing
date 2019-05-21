import pandas as pd
import numpy as np
from sklearn import dummy
from itertools import product
from sklearn import tree, ensemble, linear_model
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

# ============================== PARAMETERS  ==============================
test_id_selection_random_seed = 0
fraction_train_ids = 0.9
# max_days = 7
# min_days = 3
max_days = 8
min_days = 1
# ============================== END PARAMETERS  ==========================

interesting_columns_weather = ['temp', 'pressure','humidity']  # TODO wind_speed ?
triage_columns = ["pulse_Triage","spo2_Triage","question_Triage","manual_Triage"]


all_data = pd.read_csv("./data_generated/Patients_and_Weather_extended.csv")
all_ids = all_data['Merida ID'].unique()
np.random.seed(test_id_selection_random_seed)
selected_ids = np.random.choice(all_ids, size = int(len(all_ids)*fraction_train_ids))

#data = all_data[[i in selected_ids for i in all_data['Merida ID']]]
data = all_data

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
        output_exists = np.where(~np.isnan(data[cur_triage]))[0]

        # Taking only history
        all_X = data.iloc[output_exists, :][columns]
        all_Y = data.iloc[output_exists, :][[cur_triage]]

        all_X.fillna(0, inplace=True)

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

            kfold_split = KFold(n_splits=10, random_state=0, shuffle=True)
            all_splits = kfold_split.split(all_X)

            model = all_models[m]

            train_results = list()
            test_results = list()
            precision = list()
            recall = list()
            f1 = list()
            tp = list()
            fp = list()
            tn = list()
            fn = list()
            for cur_train_index, cur_test_index in all_splits:
                cur_X_train = all_X.iloc[cur_train_index, :]
                cur_X_test = all_X.iloc[cur_test_index, :]
                cur_Y_train = np.ravel(all_Y.iloc[cur_train_index])
                cur_Y_test = np.ravel(all_Y.iloc[cur_test_index])

                model = model.fit(cur_X_train, cur_Y_train)
                test_res = model.predict(cur_X_test)
                train_res = model.predict(cur_X_train)

                train_results.append(accuracy_score(train_res, cur_Y_train))
                test_results.append(accuracy_score(test_res, cur_Y_test))

                true_positive = np.sum((cur_Y_test > 1) & (test_res > 1))
                true_negative = np.sum((cur_Y_test == 1) & (test_res == 1))
                false_positive = np.sum((cur_Y_test == 1) & (test_res > 1))
                false_negative = np.sum((cur_Y_test > 1) & (test_res == 1))

                tp.append(true_positive)
                tn.append(true_negative)
                fp.append(false_positive)
                fn.append(false_negative)

                if true_positive > 0 or false_positive > 0:
                    cur_precision = true_positive / (true_positive + false_positive)
                else:
                    cur_precision = 0

                if true_positive > 0 or false_negative > 0:
                    cur_recall = true_positive / (true_positive + false_negative)
                else:
                    cur_recall = 0

                if cur_precision > 0 or cur_recall > 0:
                    cur_f1 = 2 * cur_precision * cur_recall / (cur_precision + cur_recall)
                else:
                    cur_f1 = 0

                precision.append(cur_precision)
                recall.append(cur_recall)
                f1.append(cur_f1)
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
                           "NumTrgSamples": len(cur_Y_train),
                           "NumTestSamples": len(cur_Y_test),
                           "TrainAcc": np.mean(train_results),
                           "TestAcc": np.mean(test_results),
                           "Precision": np.mean(precision),
                           "Recall": np.mean(recall),
                           "ImprOverMajTrain": np.mean(train_results) - dummy_train_results,
                           "ImprOverMajTest": np.mean(test_results) - dummy_test_results,
                           "F1": np.mean(f1),
                           "TP" : np.mean(tp),
                           "FP" : np.mean(fp),
                           "TN": np.mean(tn),
                           "FN": np.mean(fn),
                           }
            print("Num training samples: ", output_line["NumTrgSamples"])
            print("Num test samples: ", output_line["NumTestSamples"])
            print("TRAIN: ", output_line["TrainAcc"])
            print("TEST: ", output_line["TestAcc"])
            print("TRAIN (improved over majority): ", output_line["ImprOverMajTrain"])
            print("TEST  (improved over majority): ", output_line["ImprOverMajTest"])
            print("True positive (avg over K-Fold): ", np.mean(tp))
            print("False positive (avg over K-Fold): ", np.mean(fp))
            print("True negative (avg over K-Fold): ", np.mean(tn))
            print("False negative (avg over K-Fold): ", np.mean(fn))
            print("Precision: ", output_line["Precision"])
            print("Recall: ", output_line["Recall"])
            print("F1: ", output_line["F1"])

            output_df = output_df.append(output_line, ignore_index=True)

            if print_rules:
                model = model.fit(all_X, np.ravel(all_Y))
                values_list = list(product(*[[1, 3, 5] for i in all_X.columns]))
                test_dataframe = pd.DataFrame(columns=all_X.columns)
                for cur_values_list in values_list:
                    appended_line = dict()
                    for i in range(len(all_X.columns)):
                        cur_column = all_X.columns[i]
                        cur_value = cur_values_list[i]
                        appended_line[cur_column] = cur_value
                    test_dataframe = test_dataframe.append(appended_line, ignore_index=True)
                test_dataframe["RESULTS"] = model.predict(test_dataframe)
                print(test_dataframe)
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
    for weather_avg in [0,4,8,12]:
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

        results_df.to_csv("./data_generated/final_results_no_cv_upto8days.csv")

    # TODO Collapse grid search
