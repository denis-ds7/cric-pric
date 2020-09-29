# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:16:30 2020

@author: user 2
"""

import pandas as pd
import pickle
from os import path
from sklearn.ensemble import RandomForestClassifier
from cricpric.dao.dao import ConsistencyDAO, FormDAO, OppositionDAO, VenueDAO, PlayersDAO


class PlayerPerformance:

    def __init__(self, consistency, total_consistency, form, recent_form, opposition, venue):
        self.consistency = consistency
        self.total_consistency = total_consistency
        self.form = form
        self.recent_form = recent_form
        self.opposition = opposition
        self.venue = venue

    def predict(self, x):
        if path.exists(self.FILE_MODEL):
            with open(self.FILE_MODEL, 'rb') as file:
                model = pickle.load(file)
                result = model.predict(x)
                player_names = x.index.tolist()
                output = {'Players': player_names, 'DreamTeam': result}
                df = pd.DataFrame(output)
                df = df.groupby(['Players'], as_index=False, sort=False).sum()
                return df

    @classmethod
    def fit_model(cls, x, y):
        if path.exists(cls.FILE_MODEL):
            with open(cls.FILE_MODEL, 'rb') as file:
                model = pickle.load(file)
                model.fit(x, y)
                print("Model RF training completed")
        else:
            with open(cls.FILE_MODEL, 'wb') as file:
                model = RandomForestClassifier(bootstrap=False, max_depth=107, max_features=2,
                                               min_samples_leaf=15, min_samples_split=15,
                                               n_estimators=294)
                model.fit(x, y)
                pickle.dump(model, file)
                print("Model RF training completed")
                return model

    def predict_runs(self, x):
        if path.exists(self.FILE_MODEL_RUNS):
            with open(self.FILE_MODEL_RUNS, 'rb') as file:
                model = pickle.load(file)
                result = model.predict(x)
                player_names = x.index.tolist()
                output = {'Players': player_names, 'Runs Prediction': result}
                df = pd.DataFrame(output)
                return df

    @classmethod
    def fit_model_runs(cls, x, y):
        if path.exists(cls.FILE_MODEL_RUNS):
            with open(cls.FILE_MODEL_RUNS, 'rb') as file:
                model = pickle.load(file)
                model.fit(x, y)
                print("Model RF runs predictions training completed")
        else:
            with open(cls.FILE_MODEL_RUNS, 'wb') as file:
                model = RandomForestClassifier()
                model.fit(x, y)
                pickle.dump(model, file)
                print("Model RF runs predictions training completed")
                return model

    def predict_wickets(self, x):
        if path.exists(self.FILE_MODEL_WICKETS):
            with open(self.FILE_MODEL_WICKETS, 'rb') as file:
                model = pickle.load(file)
                result = model.predict(x)
                player_names = x.index.tolist()
                output = {'Players': player_names, 'Wickets Prediction': result}
                df = pd.DataFrame(output)
                return df

    @classmethod
    def fit_model_wickets(cls, x, y):
        if path.exists(cls.FILE_MODEL_WICKETS):
            with open(cls.FILE_MODEL_WICKETS, 'rb') as file:
                model = pickle.load(file)
                model.fit(x, y)
                print("Model RF Wicket Prediction training completed")
        else:
            with open(cls.FILE_MODEL_WICKETS, 'wb') as file:
                model = RandomForestClassifier(criterion='entropy', max_depth=68, max_features=3,
                                               min_samples_leaf=2, min_samples_split=3,
                                               n_estimators=416)
                model.fit(x, y)
                pickle.dump(model, file)
                print("Model RF Wicket Prediction training completed")
                return model

    @classmethod
    def model_runs_score(cls, x, y):
        if path.exists(cls.FILE_MODEL_RUNS):
            with open(cls.FILE_MODEL_RUNS, 'rb') as file:
                model = pickle.load(file)
                score = model.score(x, y)
                print("runs predictions RandomForest Score : ", score)
                print(model.get_params())

    @classmethod
    def model_wickets_score(cls, x, y):
        if path.exists(cls.FILE_MODEL_WICKETS):
            with open(cls.FILE_MODEL_WICKETS, 'rb') as file:
                model = pickle.load(file)
                score = model.score(x, y)
                print("Wicket Prediction RandomForest Score : ", score)
                print(model.get_params())

    @classmethod
    def model_score_rf(cls, x, y):
        if path.exists(cls.FILE_MODEL):
            with open(cls.FILE_MODEL, 'rb') as file:
                model = pickle.load(file)
                score = model.score(x, y)
                print("RandomForest Score : ", score)
                print(model.get_params())

    def calc_da(self):
        # Calculate the Derived Attributes for each Player
        consistency_bat = {}
        consistency_bowl = {}
        total_con_bat = {}
        total_con_bowl = {}
        form_bat = {}
        form_bowl = {}
        recent_form_bat = {}
        recent_form_bowl = {}
        opposition_bat = {}
        opposition_bowl = {}
        venue_bat = {}
        venue_bowl = {}

        for i in self.consistency.index:
            consistency_bat.update({self.consistency[self.COL_PLAYER][i]: \
                                        0.4262 * (
                                            ConsistencyDAO.get_con_range(self.consistency[self.COL_BAT_AVG][i],
                                                                         self.BAT_AVG)) \
                                        + 0.2566 * (
                                            ConsistencyDAO.get_con_range(self.consistency[self.COL_NO_OF_INN_BAT][i],
                                                                         self.NO_OF_INN)) \
                                        + 0.1510 * (
                                            ConsistencyDAO.get_con_range(self.consistency[self.COL_BAT_SR][i],
                                                                         self.BAT_SR)) \
                                        + 0.0787 * (
                                            ConsistencyDAO.get_con_range(self.consistency[self.COL_CENTURIES][i],
                                                                         self.CENTURIES)) \
                                        + 0.0556 * (
                                            ConsistencyDAO.get_con_range(self.consistency[self.COL_FIFTIES][i],
                                                                         self.FIFTIES)) \
                                        - 0.0328 * (
                                            ConsistencyDAO.get_con_range(self.consistency[self.COL_ZEROS][i],
                                                                         self.ZEROS))})

            consistency_bowl.update({self.consistency[self.COL_PLAYER][i]: \
                                         0.4174 * (
                                             ConsistencyDAO.get_con_range(self.consistency[self.COL_OVERS][i],
                                                                          self.OVERS)) \
                                         + 0.2634 * (
                                             ConsistencyDAO.get_con_range(self.consistency[self.COL_NO_OF_INN_BOWL][i],
                                                                          self.NO_OF_INN)) \
                                         + 0.1602 * (
                                             ConsistencyDAO.get_con_range(self.consistency[self.COL_BOWL_SR][i],
                                                                          self.BOWL_SR)) \
                                         + 0.0975 * (
                                             ConsistencyDAO.get_con_range(self.consistency[self.COL_BOWL_AVG][i],
                                                                          self.BOWL_AVG)) \
                                         + 0.0615 * (
                                             ConsistencyDAO.get_con_range(self.consistency[self.COL_WICKET_HAUL][i],
                                                                          self.FF))})

        for i in self.total_consistency.index:
            total_con_bat.update({self.total_consistency[self.COL_PLAYER][i]: \
                                      0.4262 * (
                                          ConsistencyDAO.get_con_range(self.total_consistency[self.COL_BAT_AVG][i],
                                                                       self.BAT_AVG)) \
                                      + 0.2566 * (
                                          ConsistencyDAO.get_con_range(
                                              self.total_consistency[self.COL_NO_OF_INN_BAT][i],
                                              self.NO_OF_INN)) \
                                      + 0.1510 * (
                                          ConsistencyDAO.get_con_range(self.total_consistency[self.COL_BAT_SR][i],
                                                                       self.BAT_SR)) \
                                      + 0.0787 * (
                                          ConsistencyDAO.get_con_range(self.total_consistency[self.COL_CENTURIES][i],
                                                                       self.CENTURIES)) \
                                      + 0.0556 * (
                                          ConsistencyDAO.get_con_range(self.total_consistency[self.COL_FIFTIES][i],
                                                                       self.FIFTIES)) \
                                      - 0.0328 * (
                                          ConsistencyDAO.get_con_range(self.total_consistency[self.COL_ZEROS][i],
                                                                       self.ZEROS))})

            total_con_bowl.update({self.total_consistency[self.COL_PLAYER][i]: \
                                       0.4174 * (
                                           ConsistencyDAO.get_con_range(self.total_consistency[self.COL_OVERS][i],
                                                                        self.OVERS)) \
                                       + 0.2634 * (
                                           ConsistencyDAO.get_con_range(
                                               self.total_consistency[self.COL_NO_OF_INN_BOWL][i],
                                               self.NO_OF_INN)) \
                                       + 0.1602 * (
                                           ConsistencyDAO.get_con_range(self.total_consistency[self.COL_BOWL_SR][i],
                                                                        self.BOWL_SR)) \
                                       + 0.0975 * (
                                           ConsistencyDAO.get_con_range(self.total_consistency[self.COL_BOWL_AVG][i],
                                                                        self.BOWL_AVG)) \
                                       + 0.0615 * (
                                           ConsistencyDAO.get_con_range(self.total_consistency[self.COL_WICKET_HAUL][i],
                                                                        self.FF))})

        for i in self.form.index:
            form_bat.update({self.form[self.COL_PLAYER][i]: \
                                 0.4262 * (FormDAO.get_form_range(self.form[self.COL_BAT_AVG][i], self.BAT_AVG)) \
                                 + 0.2566 * (
                                     FormDAO.get_form_range(self.form[self.COL_NO_OF_INN_BAT][i], self.NO_OF_INN)) \
                                 + 0.1510 * (FormDAO.get_form_range(self.form[self.COL_BAT_SR][i], self.BAT_SR)) \
                                 + 0.0787 * (FormDAO.get_form_range(self.form[self.COL_CENTURIES][i], self.CENTURIES)) \
                                 + 0.0556 * (FormDAO.get_form_range(self.form[self.COL_FIFTIES][i], self.FIFTIES)) \
                                 - 0.0328 * (FormDAO.get_form_range(self.form[self.COL_ZEROS][i], self.ZEROS))})

            form_bowl.update({self.form[self.COL_PLAYER][i]: \
                                  0.3269 * (FormDAO.get_form_range(self.form[self.COL_OVERS][i], self.OVERS)) \
                                  + 0.2846 * (
                                      FormDAO.get_form_range(self.form[self.COL_NO_OF_INN_BOWL][i], self.NO_OF_INN)) \
                                  + 0.1877 * (FormDAO.get_form_range(self.form[self.COL_BOWL_SR][i], self.BOWL_SR)) \
                                  + 0.1210 * (FormDAO.get_form_range(self.form[self.COL_BOWL_AVG][i], self.BOWL_AVG)) \
                                  + 0.0798 * (FormDAO.get_form_range(self.form[self.COL_WICKET_HAUL][i], self.FF))})

        for i in self.recent_form.index:
            recent_form_bat.update({self.recent_form[self.COL_PLAYER][i]: \
                                        0.4262 * (FormDAO.get_form_range(self.recent_form[self.COL_BAT_AVG][i], self.BAT_AVG)) \
                                        + 0.2566 * (
                                            FormDAO.get_form_range(self.recent_form[self.COL_NO_OF_INN_BAT][i],
                                                                   self.NO_OF_INN)) \
                                        + 0.1510 * (FormDAO.get_form_range(self.recent_form[self.COL_BAT_SR][i], self.BAT_SR)) \
                                        + 0.0787 * (
                                            FormDAO.get_form_range(self.recent_form[self.COL_CENTURIES][i], self.CENTURIES)) \
                                        + 0.0556 * (
                                            FormDAO.get_form_range(self.recent_form[self.COL_FIFTIES][i], self.FIFTIES)) \
                                        - 0.0328 * (FormDAO.get_form_range(self.recent_form[self.COL_ZEROS][i], self.ZEROS))})

            recent_form_bowl.update({self.recent_form[self.COL_PLAYER][i]: \
                                         0.3269 * (FormDAO.get_form_range(self.recent_form[self.COL_OVERS][i], self.OVERS)) \
                                         + 0.2846 * (
                                             FormDAO.get_form_range(self.recent_form[self.COL_NO_OF_INN_BOWL][i],
                                                                    self.NO_OF_INN)) \
                                         + 0.1877 * (
                                             FormDAO.get_form_range(self.recent_form[self.COL_BOWL_SR][i], self.BOWL_SR)) \
                                         + 0.1210 * (
                                             FormDAO.get_form_range(self.recent_form[self.COL_BOWL_AVG][i], self.BOWL_AVG)) \
                                         + 0.0798 * (
                                             FormDAO.get_form_range(self.recent_form[self.COL_WICKET_HAUL][i], self.FF))})

        for i in self.opposition.index:
            opposition_bat.update({self.opposition[self.COL_PLAYER][i]: \
                                       0.4262 * (
                                           OppositionDAO.get_opp_range(self.opposition[self.COL_BAT_AVG][i],
                                                                       self.BAT_AVG)) \
                                       + 0.2566 * (
                                           OppositionDAO.get_opp_range(self.opposition[self.COL_NO_OF_INN_BAT][i],
                                                                       self.NO_OF_INN)) \
                                       + 0.1510 * (
                                           OppositionDAO.get_opp_range(self.opposition[self.COL_BAT_SR][i],
                                                                       self.BAT_SR)) \
                                       + 0.0787 * (
                                           OppositionDAO.get_opp_range(self.opposition[self.COL_CENTURIES][i],
                                                                       self.CENTURIES)) \
                                       + 0.0556 * (
                                           OppositionDAO.get_opp_range(self.opposition[self.COL_FIFTIES][i],
                                                                       self.FIFTIES)) \
                                       - 0.0328 * (
                                           OppositionDAO.get_opp_range(self.opposition[self.COL_ZEROS][i],
                                                                       self.ZEROS))})

            opposition_bowl.update({self.opposition[self.COL_PLAYER][i]: \
                                        0.3177 * (
                                            OppositionDAO.get_opp_range(self.opposition[self.COL_OVERS][i], self.OVERS)) \
                                        + 0.3177 * (
                                            OppositionDAO.get_opp_range(self.opposition[self.COL_NO_OF_INN_BOWL][i],
                                                                        self.NO_OF_INN)) \
                                        + 0.1933 * (
                                            OppositionDAO.get_opp_range(self.opposition[self.COL_BOWL_SR][i],
                                                                        self.BOWL_SR)) \
                                        + 0.1465 * (
                                            OppositionDAO.get_opp_range(self.opposition[self.COL_BOWL_AVG][i],
                                                                        self.BOWL_AVG)) \
                                        + 0.0943 * (
                                            OppositionDAO.get_opp_range(self.opposition[self.COL_WICKET_HAUL][i],
                                                                        self.FF))})

        for i in self.venue.index:
            venue_bat.update({self.venue[self.COL_PLAYER][i]: \
                                  0.4262 * (VenueDAO.get_ven_range(self.venue[self.COL_BAT_AVG][i], self.BAT_AVG)) \
                                  + 0.2566 * (
                                      VenueDAO.get_ven_range(self.venue[self.COL_NO_OF_INN_BAT][i], self.NO_OF_INN)) \
                                  + 0.1510 * (VenueDAO.get_ven_range(self.venue[self.COL_BAT_SR][i], self.BAT_SR)) \
                                  + 0.0787 * (VenueDAO.get_ven_range(self.venue[self.COL_CENTURIES][i], self.CENTURIES)) \
                                  + 0.0556 * (VenueDAO.get_ven_range(self.venue[self.COL_FIFTIES][i], self.FIFTIES)) \
                                  + 0.0328 * (VenueDAO.get_ven_range(self.venue[self.COL_HS][i], self.HS))})

            venue_bowl.update({self.venue[self.COL_PLAYER][i]: \
                                   0.3018 * (VenueDAO.get_ven_range(self.venue[self.COL_OVERS][i], self.OVERS)) \
                                   + 0.2783 * (
                                       VenueDAO.get_ven_range(self.venue[self.COL_NO_OF_INN_BOWL][i], self.NO_OF_INN)) \
                                   + 0.1836 * (VenueDAO.get_ven_range(self.venue[self.COL_BOWL_SR][i], self.BOWL_SR)) \
                                   + 0.1391 * (VenueDAO.get_ven_range(self.venue[self.COL_BOWL_AVG][i], self.BOWL_AVG)) \
                                   + 0.0972 * (VenueDAO.get_ven_range(self.venue[self.COL_WICKET_HAUL][i], self.FF))})

        data_set = [consistency_bat, total_con_bat, form_bat, recent_form_bat, opposition_bat, venue_bat, consistency_bowl,
                    total_con_bowl, form_bowl, recent_form_bowl, opposition_bowl, venue_bowl]
        return self.__prepare_df(data_set)

    @staticmethod
    def __prepare_df(data_set):
        df = pd.DataFrame.from_dict(data=data_set)
        df = df.transpose()
        df.columns = ['ConsistencyBat', 'TotalConBat', 'FormBat', 'RecentFormBat', 'OppositionBat', 'VenueBat', 'ConsistencyBowl',
                      'TotalConBowl', 'FormBowl', 'RecentFormBowl',
                      'OppositionBowl', 'VenueBowl']
        return df

    def modify_data_set(self, train_data):
        batsmen = train_data.loc[:, 'ConsistencyBat':'VenueBat']
        bowler = train_data.loc[:, 'ConsistencyBowl':'VenueBowl']

        bowler.columns = self.HEADER_COLS
        batsmen.columns = self.HEADER_COLS

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

    # @staticmethod
    # def __modify_prediction(df):
    #     df = df.groupby(level=0).sum()
    #     return df

    FILE_MODEL = 'model\\model_pickle'
    FILE_MODEL_RUNS = 'model\\model_pickle_runs'
    FILE_MODEL_WICKETS = 'model\\model_pickle_wickets'
    FILE_MODEL_NB = 'model\\model_pickle_nb'
    FILE_MODEL_SVM = 'model\\model_pickle_svm'
    FILE_MODEL_DT = 'model\\model_pickle_dt'

    NO_OF_INN = "No. of Innings"
    BAT_AVG = "Batting Average"
    BAT_SR = "Batting Strike Rate"
    CENTURIES = "Centuries"
    FIFTIES = "Fifties"
    ZEROS = "Zeros"
    HS = "Highest Score"
    OVERS = "Overs"
    BOWL_AVG = "Bowling Average"
    BOWL_SR = "Bowling Strike Rate"
    FF = "FF"

    COL_PLAYER = "Player"
    COL_BAT_AVG = "BatAvg"
    COL_NO_OF_INN_BAT = "No. of Inn (Bat)"
    COL_BAT_SR = "BatSR"
    COL_CENTURIES = "Centuries"
    COL_FIFTIES = "Fifties"
    COL_ZEROS = "Zeros"
    COL_OVERS = "Overs"
    COL_NO_OF_INN_BOWL = "No. of Inn (Bowl)"
    COL_BOWL_SR = "BowlSR"
    COL_BOWL_AVG = "BowlAvg"
    COL_WICKET_HAUL = "WicketHaul"
    COL_HS = "HS"

    HEADER_COLS = ['Consistency', 'TotalConsistency', 'Form', 'RecentForm', 'Opposition', 'Venue']
