# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:45:38 2020

@author: user 2
"""
import os
from threading import Thread

from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE
from cricpric.dao.dao import PlayersDAO
from cricpric.preparation.data_collection import CreateOVC
from cricpric.processing.create_modify import DerivedAttrs
import pandas as pd
import numpy as np
from cricpric.modeling.predict_performance import PlayerPerformance
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from cricpric.processing.data_extraction import ModifyCFOV

host_team = "Kolkata Knight Riders"
away_team = "Sunrisers Hyderabad"
venue = "Eden Gardens"

bat = "bat"
bowl = "bowl"

host_playing = ["Dinesh Karthik", "Piyush Chawla"]
away_playing = ["David Warner", "Jonny Bairstow", "Bhuvneshwar Kumar"]

# host_playing = ["Faf du Plessis", "Shane Watson", "Suresh Raina", "Ambati Rayudu", "MS Dhoni", "Ravindra Jadeja",
#                 "Dwayne Bravo", "Deepak Chahar", "Shardul Thakur", "Harbhajan Singh", "Imran Tahir"]
# away_playing = ["Quinton de Kock", "Rohit Sharma", "Suryakumar Yadav", "Ishan Kishan", "Hardik Pandya",
#                 "Kieron Pollard", "Krunal Pandya", "Mitchell McClenaghan", "Rahul Chahar", "Lasith Malinga",
#                 "Jasprit Bumrah"]

FILE_TRAIN_DATA = "config/train_data.csv"
HEADER_COLS = ['Con', 'TotCon', 'Form', 'Opp', 'Ven', 'DreamTeam']
HEADER_COLS_CSV = ['Con', 'TotCon', 'Form', 'Opp', 'Ven', 'DreamTeam', 'BatBowl']

# create = CreateOVC(away_playing, '')
# df = create.create_total_consistency()
# modify = ModifyCFOV()
# df = modify.modify_total_consistency(df)
# print(df)


def test_predict():
    # da = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
    # Thread(target=da.consistency_form(bat, bowl)).start()
    # Thread(target=da.total_consistency()).start()
    # Thread(target=da.opposition_venue(bat, bowl)).start()
    # da.execute_run(bat, bowl)
    # da.consistency_form(bat, bowl)
    # da.opposition_venue(bat, bowl)
    # da.total_consistency()

    con = pd.read_csv(da.FILE_CONSISTENCY)

    total_con = pd.read_csv(da.FILE_TOTAL_CONSISTENCY)

    form = pd.read_csv(da.FILE_FORM)

    opp = pd.read_csv(da.FILE_OPPOSITION)

    ven = pd.read_csv(da.FILE_VENUE)

    ipl = PlayerPerformance(con, total_con, form, opp, ven)
    array = ipl.predict()
    print(array)


def modify_train_data(train_data):
    batsmen = train_data.loc[:, 'ConsistencyBat':'VenueBat']
    batsmen['DreamTeam'] = train_data.DreamTeam

    bowler = train_data.loc[:, ('ConsistencyBowl', 'TotalConBowl', 'FormBowl', 'OppositionBowl', 'VenueBowl')]
    bowler['DreamTeam'] = train_data.DreamTeam

    # for i, row in batsmen.iterrows():
    #     if row['TotalConBat'] == 0:
    #         batsmen.drop(i, inplace=True)
    #         continue
    #     if row['ConsistencyBat'] == 0 and row['FormBat'] == 0:
    #         batsmen.drop(i, inplace=True)
    #
    # for i, row in bowler.iterrows():
    #     if row['TotalConBowl'] <= 0.7:
    #         bowler.drop(i, inplace=True)
    #         continue
    #     if row['ConsistencyBowl'] == 0 and row['FormBowl'] == 0:
    #         bowler.drop(i, inplace=True)

    bowler.columns = HEADER_COLS
    batsmen.columns = HEADER_COLS

    batsmen['BatBowl'] = 1
    bowler['BatBowl'] = 0

    players = batsmen.index.tolist()
    players = list(dict.fromkeys(players))
    for player in players:
        player_role = PlayersDAO.get_player_role(player)
        if player_role == 'batsman' and bowler['BatBowl'][player].all() == 0:
            bowler.drop(player, inplace=True)
        elif player_role == 'bowler' and batsmen['BatBowl'][player].all() == 1:
            batsmen.drop(player, inplace=True)

    data = batsmen.append(bowler)
    return data


def test_train_data():
    train_data = pd.read_csv("config/train_data.csv")
    train_data.set_index('Unnamed: 0', inplace=True, drop=True)
    # train_data = modify_train_data(train_data)

    # train_data.to_csv("config/Final_Train_set.csv", header=HEADER_COLS_CSV,)

    y = train_data['DreamTeam']
    x = train_data.drop("DreamTeam", axis='columns')
    # x.set_index('Unnamed: 0', inplace=True)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    PlayerPerformance.fit_model(x_train, y_train)
    # PlayerPerformance.fit_model_svm(x_train, y_train)
    # PlayerPerformance.fit_model_nb(x_train, y_train)
    # PlayerPerformance.fit_model_dt(x_train, y_train)

    PlayerPerformance.model_score_rf(x_test, y_test)
    # PlayerPerformance.model_score_svm(x_test, y_test)
    # PlayerPerformance.model_score_nb(x_test, y_test)
    # PlayerPerformance.model_score_dt(x_test, y_test)

    # # Number of trees in random forest
    # n_estimators = [int(x) for x in np.linspace(start=10, stop=2000, num=50)]
    # # Number of features to consider at every split
    # max_features = ['auto', 'sqrt', 2, 3, 4, 5, 6]
    # # Maximum number of levels in tree
    # max_depth = [int(x) for x in np.linspace(1, 110, num=50)]
    # max_depth.append(None)
    # # Minimum number of samples required to split a node
    # min_samples_split = [2, 3, 4, 5, 10, 20]
    # # Minimum number of samples required at each leaf node
    # min_samples_leaf = [2, 3, 4, 10, 15]
    # # Method of selecting samples for training each tree
    # bootstrap = [True, False]
    # criterion = ['gini', 'entropy']
    #
    # # Create the random grid
    # random_grid = {'n_estimators': n_estimators,
    #                'criterion': criterion,
    #                'max_features': max_features,
    #                'max_depth': max_depth,
    #                'min_samples_split': min_samples_split,
    #                'min_samples_leaf': min_samples_leaf,
    #                'bootstrap': bootstrap}
    #
    # rf_model = RandomForestClassifier()
    #
    # rf_random = RandomizedSearchCV(estimator=rf_model, param_distributions=random_grid, n_iter=50, cv=5, verbose=2,
    #                                n_jobs=-1)
    #
    # rf_random.fit(x_train, y_train)
    #
    # best_params = rf_random.best_params_
    # best_score = rf_random.best_score_
    # print("RandomSearchCV best params are", best_params)
    # print("RandomSearchCV best score are", best_score)
    #
    # # base_model = PlayerPerformance.fit_model(x_train, y_train)
    # # score = base_model.score(x_test, y_test)
    # # print('Base Model Score : ', score)
    # # base_accuracy = evaluate(base_model, x_test, y_test)
    #
    # best_random = rf_random.best_estimator_
    # score = best_random.score(x_test, y_test)
    # print('Best RandomCV Score : ', score)
    # print("RandomSearchCV best estimator are", best_random)
    # # random_accuracy = evaluate(best_random, x_test, y_test)
    #
    # # print('Improvement of {:0.2f}%.'.format(100 * (random_accuracy - base_accuracy) / base_accuracy))
    # #
    # # Create the parameter grid based on the results of random search
    # param_grid = {
    #     'bootstrap': [False, True],
    #     'criterion': ['gini', 'entropy'],
    #     'max_depth': [5, 6, 7, 8, 9, 20, 60, 95],
    #     'max_features': [2, 3, 4, 5, 6],
    #     'min_samples_leaf': [3, 4, 5, 7, 10, 12, 25, 55, 75],
    #     'min_samples_split': [8, 10, 12, 20, 50, 55],
    #     'n_estimators': [100, 200, 300, 400, 500, 600, 700]
    # }
    # # Create a based model
    # rf = RandomForestClassifier()
    # # Instantiate the grid search model
    # grid_search = GridSearchCV(estimator=rf, param_grid=param_grid,
    #                            cv=5, n_jobs=-1, verbose=2)
    #
    # # Fit the grid search to the data
    # grid_search.fit(x_train, y_train)
    # grid_best_params = grid_search.best_params_
    # print("GridSearchCV best params :", grid_best_params)
    #
    # best_grid = grid_search.best_estimator_
    # score = best_grid.score(x_test, y_test)
    # print('Best GridCV Score : ', score)
    # # grid_accuracy = evaluate(best_grid, x_test, y_test)


# def evaluate(model, test_features, test_labels):
#     predictions = model.predict(test_features)
#     errors = abs(predictions - test_labels)
#     mape = 100 * np.mean(errors / test_labels)
#     accuracy = 100 - mape
#     score = model.score(test_features, test_labels)
#     print('Model Performance')
#     print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
#     print('Accuracy = {:0.2f}%.'.format(accuracy))
#     print('Score : ', score)
#
#     return accuracy


def prepare_train_data():
    da = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
    da.execute_run(bat, bowl)
    # da.consistency_form(bat, bowl)
    # da.opposition_venue(bat, bowl)
    # da.total_consistency()

    con = pd.read_csv(da.FILE_CONSISTENCY)
    tot_con = pd.read_csv(da.FILE_TOTAL_CONSISTENCY)
    form = pd.read_csv(da.FILE_FORM)
    opp = pd.read_csv(da.FILE_OPPOSITION)
    ven = pd.read_csv(da.FILE_VENUE)

    ipl = PlayerPerformance(con, tot_con, form, opp, ven)
    data = ipl.calc_da()

    if os.path.exists(FILE_TRAIN_DATA):
        with open(FILE_TRAIN_DATA, 'a', newline='') as f:
            data.to_csv(f, mode='a', header=False, index=False)
    else:
        data.to_csv(FILE_TRAIN_DATA, index=False)


# test_train_data()


def train_player_runs():
    train_data = pd.read_csv("config/train_data_runs.csv")
    y = train_data['DreamTeam']
    x = train_data.drop("DreamTeam", axis='columns')
    x.set_index('Unnamed: 0', inplace=True)

    # ros = SMOTE()
    # x_sampler, y_sampler = ros.fit_sample(x, y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    PlayerPerformance.fit_model_runs(x_train, y_train)
    PlayerPerformance.model_runs_score(x_test, y_test)

    # # Number of trees in random forest
    # n_estimators = [int(x) for x in np.linspace(start=10, stop=2000, num=50)]
    # # Number of features to consider at every split
    # max_features = ['auto', 'sqrt', 2, 3, 4, 5]
    # # Maximum number of levels in tree
    # max_depth = [int(x) for x in np.linspace(1, 110, num=40)]
    # max_depth.append(None)
    # # Minimum number of samples required to split a node
    # min_samples_split = [2, 3, 4, 5, 10]
    # # Minimum number of samples required at each leaf node
    # min_samples_leaf = [2, 3, 4, 10]
    # # Method of selecting samples for training each tree
    # bootstrap = [True, False]
    # criterion = ['gini', 'entropy']
    #
    # # Create the random grid
    # random_grid = {'n_estimators': n_estimators,
    #                'criterion': criterion,
    #                'max_features': max_features,
    #                'max_depth': max_depth,
    #                'min_samples_split': min_samples_split,
    #                'min_samples_leaf': min_samples_leaf,
    #                'bootstrap': bootstrap}
    #
    # rf_model = RandomForestClassifier()
    #
    # rf_random = RandomizedSearchCV(estimator=rf_model, param_distributions=random_grid, n_iter=50, cv=5, verbose=2,
    #                                n_jobs=-1)
    #
    # rf_random.fit(x_train, y_train)
    #
    # best_params = rf_random.best_params_
    # best_score = rf_random.best_score_
    # print("RandomSearchCV best params are", best_params)
    # print("RandomSearchCV best score are", best_score)
    #
    # # base_model = PlayerPerformance.fit_model(x_train, y_train)
    # # score = base_model.score(x_test, y_test)
    # # print('Base Model Score : ', score)
    # # base_accuracy = evaluate(base_model, x_test, y_test)
    #
    # best_random = rf_random.best_estimator_
    # score = best_random.score(x_test, y_test)
    # print('Best RandomCV Score : ', score)
    # print("RandomSearchCV best estimator are", best_random)
    # # random_accuracy = evaluate(best_random, x_test, y_test)


def train_player_wickets():
    train_data = pd.read_csv("config/train_data_wickets.csv")
    y = train_data['DreamTeam']
    x = train_data.drop("DreamTeam", axis='columns')
    x.set_index('Unnamed: 0', inplace=True)

    # ros = SMOTE()
    # x_sampler, y_sampler = ros.fit_sample(x, y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    PlayerPerformance.fit_model_wickets(x_train, y_train)
    PlayerPerformance.model_wickets_score(x_test, y_test)

    # # Number of trees in random forest
    # n_estimators = [int(x) for x in np.linspace(start=10, stop=2000, num=50)]
    # # Number of features to consider at every split
    # max_features = ['auto', 'sqrt', 2, 3, 4, 5]
    # # Maximum number of levels in tree
    # max_depth = [int(x) for x in np.linspace(1, 110, num=40)]
    # max_depth.append(None)
    # # Minimum number of samples required to split a node
    # min_samples_split = [2, 3, 4, 5, 10]
    # # Minimum number of samples required at each leaf node
    # min_samples_leaf = [2, 3, 4, 10]
    # # Method of selecting samples for training each tree
    # bootstrap = [True, False]
    # criterion = ['gini', 'entropy']
    #
    # # Create the random grid
    # random_grid = {'n_estimators': n_estimators,
    #                'criterion': criterion,
    #                'max_features': max_features,
    #                'max_depth': max_depth,
    #                'min_samples_split': min_samples_split,
    #                'min_samples_leaf': min_samples_leaf,
    #                'bootstrap': bootstrap}
    #
    # rf_model = RandomForestClassifier()
    #
    # rf_random = RandomizedSearchCV(estimator=rf_model, param_distributions=random_grid, n_iter=50, cv=5, verbose=2,
    #                                n_jobs=-1)
    #
    # rf_random.fit(x_train, y_train)
    #
    # best_params = rf_random.best_params_
    # best_score = rf_random.best_score_
    # print("RandomSearchCV best params are", best_params)
    # print("RandomSearchCV best score are", best_score)
    #
    # # base_model = PlayerPerformance.fit_model(x_train, y_train)
    # # score = base_model.score(x_test, y_test)
    # # print('Base Model Score : ', score)
    # # base_accuracy = evaluate(base_model, x_test, y_test)
    #
    # best_random = rf_random.best_estimator_
    # score = best_random.score(x_test, y_test)
    # print('Best RandomCV Score : ', score)
    # print("RandomSearchCV best estimator are", best_random)
    # # random_accuracy = evaluate(best_random, x_test, y_test)


# da = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
# t1 = Thread(target=da.consistency_form, args=(bat, bowl))
# t2 = Thread(target=da.total_consistency)
# t3 = Thread(target=da.opposition_venue, args=(bat, bowl))
# t1.start()
# t2.start()
# t3.start()
# t1.join()
# t2.join()
# t3.join()

# test_predict()
# test_train_data()
# train_player_runs()
# train_player_wickets()
