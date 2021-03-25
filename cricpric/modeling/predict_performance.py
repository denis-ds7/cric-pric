# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:16:30 2020

@author: user 2
"""
import os

import boto3
import pandas as pd
import pickle
from os import path
from sklearn.ensemble import RandomForestClassifier
from cricpric.dao.dao import ConsistencyDAO, FormDAO, OppositionDAO, VenueDAO
from cricpric.util.util import DataUtils


class PlayerPerformance:

    def __init__(self, consistency, total_consistency, form, recent_form, opposition, venue):
        self.consistency = consistency
        self.total_consistency = total_consistency
        self.form = form
        self.recent_form = recent_form
        self.opposition = opposition
        self.venue = venue

    @staticmethod
    def get_model(file_name):
        client = boto3.client('s3')
        bucket = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        response = client.get_object(Bucket=bucket, Key=file_name)
        body = response['Body'].read()

        return pickle.loads(body)

    def predict(self, x):
        # if path.exists(self.FILE_MODEL):
        #     with open(self.FILE_MODEL, 'rb') as file:
        model = self.get_model("model_pickle.pkl")
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
        # if path.exists(self.FILE_MODEL_RUNS):
        #     with open(self.FILE_MODEL_RUNS, 'rb') as file:
        model = self.get_model("model_pickle_runs.pkl")
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
        # if path.exists(self.FILE_MODEL_WICKETS):
        #     with open(self.FILE_MODEL_WICKETS, 'rb') as file:
        model = self.get_model("model_pickle_wickets.pkl")
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
                print("Runs Predictions RandomForest Score : ", score)
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

    def consistency_range(self, consistency_range):
        consistency_bat = {}
        consistency_bowl = {}
        for i in self.consistency.index:
            consistency_bat.update({self.consistency[self.COL_PLAYER][i]:
                                        0.4262 * (DataUtils.check_range(consistency_range[1],
                                                                        self.consistency[self.COL_BAT_AVG][i]))
                                        + 0.2566 * (DataUtils.check_range(consistency_range[0],
                                                                          self.consistency[self.COL_NO_OF_INN_BAT][i]))
                                        + 0.1510 * (DataUtils.check_range(consistency_range[2],
                                                                          self.consistency[self.COL_BAT_SR][i]))
                                        + 0.0787 * (DataUtils.check_range(consistency_range[3],
                                                                          self.consistency[self.COL_CENTURIES][i]))
                                        + 0.0556 * (DataUtils.check_range(consistency_range[4],
                                                                          self.consistency[self.COL_FIFTIES][i]))
                                        - 0.0328 * (DataUtils.check_range(consistency_range[5],
                                                                          self.consistency[self.COL_ZEROS][i]))
                                    })

            consistency_bowl.update({self.consistency[self.COL_PLAYER][i]:
                                         0.4174 * (DataUtils.check_range(consistency_range[6],
                                                                         self.consistency[self.COL_OVERS][i]))
                                         + 0.2634 * (DataUtils.check_range(consistency_range[0],
                                                                           self.consistency[self.COL_NO_OF_INN_BOWL][i]))
                                         + 0.1602 * (DataUtils.check_range(consistency_range[8],
                                                                           self.consistency[self.COL_BOWL_SR][i]))
                                         + 0.0975 * (DataUtils.check_range(consistency_range[7],
                                                                           self.consistency[self.COL_BOWL_AVG][i]))
                                         + 0.0615 * (DataUtils.check_range(consistency_range[9],
                                                                           self.consistency[self.COL_WICKET_HAUL][i]))
                                     })
        return consistency_bat, consistency_bowl

    def total_consistency_range(self, consistency_range):
        total_con_bat = {}
        total_con_bowl = {}
        for i in self.total_consistency.index:
            total_con_bat.update({self.total_consistency[self.COL_PLAYER][i]:
                                      0.4262 * (DataUtils.check_range(consistency_range[1],
                                                                      self.total_consistency[self.COL_BAT_AVG][i]))
                                      + 0.2566 * (DataUtils.check_range(consistency_range[0],
                                                                        self.total_consistency[self.COL_NO_OF_INN_BAT][i]))
                                      + 0.1510 * (DataUtils.check_range(consistency_range[2],
                                                                        self.total_consistency[self.COL_BAT_SR][i]))
                                      + 0.0787 * (DataUtils.check_range(consistency_range[3],
                                                                        self.total_consistency[self.COL_CENTURIES][i]))
                                      + 0.0556 * (DataUtils.check_range(consistency_range[4],
                                                                        self.total_consistency[self.COL_FIFTIES][i]))
                                      - 0.0328 * (DataUtils.check_range(consistency_range[5],
                                                                        self.total_consistency[self.COL_ZEROS][i]))
                                  })

            total_con_bowl.update({self.total_consistency[self.COL_PLAYER][i]:
                                       0.4174 * (DataUtils.check_range(consistency_range[6],
                                                                       self.total_consistency[self.COL_OVERS][i]))
                                       + 0.2634 * (DataUtils.check_range(consistency_range[0],
                                                                         self.total_consistency[self.COL_NO_OF_INN_BOWL][i]))
                                       + 0.1602 * (DataUtils.check_range(consistency_range[8],
                                                                         self.total_consistency[self.COL_BOWL_SR][i]))
                                       + 0.0975 * (DataUtils.check_range(consistency_range[7],
                                                                         self.total_consistency[self.COL_BOWL_AVG][i]))
                                       + 0.0615 * (DataUtils.check_range(consistency_range[9],
                                                                         self.total_consistency[self.COL_WICKET_HAUL][i]))
                                   })
        return total_con_bat, total_con_bowl

    def form_range(self, form_range):
        form_bat = {}
        form_bowl = {}
        for i in self.form.index:
            form_bat.update({self.form[self.COL_PLAYER][i]:
                                 0.4262 * (DataUtils.check_range(form_range[1], self.form[self.COL_BAT_AVG][i]))
                                 + 0.2566 * (DataUtils.check_range(form_range[0], self.form[self.COL_NO_OF_INN_BAT][i]))
                                 + 0.1510 * (DataUtils.check_range(form_range[2], self.form[self.COL_BAT_SR][i]))
                                 + 0.0787 * (DataUtils.check_range(form_range[3], self.form[self.COL_CENTURIES][i]))
                                 + 0.0556 * (DataUtils.check_range(form_range[4], self.form[self.COL_FIFTIES][i]))
                                 - 0.0328 * (DataUtils.check_range(form_range[5], self.form[self.COL_ZEROS][i]))
                             })
            form_bowl.update({self.form[self.COL_PLAYER][i]:
                                  0.3269 * (DataUtils.check_range(form_range[6], self.form[self.COL_OVERS][i]))
                                  + 0.2846 * (DataUtils.check_range(form_range[0], self.form[self.COL_NO_OF_INN_BOWL][i]))
                                  + 0.1877 * (DataUtils.check_range(form_range[8], self.form[self.COL_BOWL_SR][i]))
                                  + 0.1210 * (DataUtils.check_range(form_range[7], self.form[self.COL_BOWL_AVG][i]))
                                  + 0.0798 * (DataUtils.check_range(form_range[9], self.form[self.COL_WICKET_HAUL][i]))
                              })
        return form_bat, form_bowl

    def recent_form_range(self, form_range):
        recent_form_bat = {}
        recent_form_bowl = {}
        for i in self.recent_form.index:
            recent_form_bat.update({self.recent_form[self.COL_PLAYER][i]:
                                        0.4262 * (DataUtils.check_range(form_range[1], self.recent_form[self.COL_BAT_AVG][i]))
                                        + 0.2566 * (DataUtils.check_range(form_range[0], self.recent_form[self.COL_NO_OF_INN_BAT][i]))
                                        + 0.1510 * (DataUtils.check_range(form_range[2], self.recent_form[self.COL_BAT_SR][i]))
                                        + 0.0787 * (DataUtils.check_range(form_range[3], self.recent_form[self.COL_CENTURIES][i]))
                                        + 0.0556 * (DataUtils.check_range(form_range[4], self.recent_form[self.COL_FIFTIES][i]))
                                        - 0.0328 * (DataUtils.check_range(form_range[5], self.recent_form[self.COL_ZEROS][i]))
                                    })

            recent_form_bowl.update({self.recent_form[self.COL_PLAYER][i]:
                                         0.3269 * (DataUtils.check_range(form_range[6], self.recent_form[self.COL_OVERS][i]))
                                         + 0.2846 * (DataUtils.check_range(form_range[0], self.recent_form[self.COL_NO_OF_INN_BOWL][i]))
                                         + 0.1877 * (DataUtils.check_range(form_range[8], self.recent_form[self.COL_BOWL_SR][i]))
                                         + 0.1210 * (DataUtils.check_range(form_range[7], self.recent_form[self.COL_BOWL_AVG][i]))
                                         + 0.0798 * (DataUtils.check_range(form_range[9], self.recent_form[self.COL_WICKET_HAUL][i]))
                                     })
        return recent_form_bat, recent_form_bowl

    def opposition_range(self, opposition_range):
        opposition_bat = {}
        opposition_bowl = {}
        for i in self.opposition.index:
            opposition_bat.update({self.opposition[self.COL_PLAYER][i]:
                                       0.4262 * (DataUtils.check_range(opposition_range[1],
                                                                       self.opposition[self.COL_BAT_AVG][i]))
                                       + 0.2566 * (DataUtils.check_range(opposition_range[0],
                                                                         self.opposition[self.COL_NO_OF_INN_BAT][i]))
                                       + 0.1510 * (DataUtils.check_range(opposition_range[2],
                                                                         self.opposition[self.COL_BAT_SR][i]))
                                       + 0.0787 * (DataUtils.check_range(opposition_range[3],
                                                                         self.opposition[self.COL_CENTURIES][i]))
                                       + 0.0556 * (DataUtils.check_range(opposition_range[4],
                                                                         self.opposition[self.COL_FIFTIES][i]))
                                       - 0.0328 * (DataUtils.check_range(opposition_range[5],
                                                                         self.opposition[self.COL_ZEROS][i]))
                                   })

            opposition_bowl.update({self.opposition[self.COL_PLAYER][i]:
                                        0.3177 * (DataUtils.check_range(opposition_range[6],
                                                                        self.opposition[self.COL_OVERS][i]))
                                        + 0.3177 * (DataUtils.check_range(opposition_range[0],
                                                                          self.opposition[self.COL_NO_OF_INN_BOWL][i]))
                                        + 0.1933 * (DataUtils.check_range(opposition_range[8],
                                                                          self.opposition[self.COL_BOWL_SR][i]))
                                        + 0.1465 * (DataUtils.check_range(opposition_range[7],
                                                                          self.opposition[self.COL_BOWL_AVG][i]))
                                        + 0.0943 * (DataUtils.check_range(opposition_range[9],
                                                                          self.opposition[self.COL_WICKET_HAUL][i]))
                                    })
        return opposition_bat, opposition_bowl

    def venue_range(self, venue_range):
        venue_bat = {}
        venue_bowl = {}
        for i in self.venue.index:
            venue_bat.update({self.venue[self.COL_PLAYER][i]:
                                  0.4262 * (DataUtils.check_range(venue_range[1], self.venue[self.COL_BAT_AVG][i]))
                                  + 0.2566 * (DataUtils.check_range(venue_range[0], self.venue[self.COL_NO_OF_INN_BAT][i]))
                                  + 0.1510 * (DataUtils.check_range(venue_range[2], self.venue[self.COL_BAT_SR][i]))
                                  + 0.0787 * (DataUtils.check_range(venue_range[3], self.venue[self.COL_CENTURIES][i]))
                                  + 0.0556 * (DataUtils.check_range(venue_range[4], self.venue[self.COL_FIFTIES][i]))
                                  + 0.0328 * (DataUtils.check_range(venue_range[5], self.venue[self.COL_HS][i]))
                              })

            venue_bowl.update({self.venue[self.COL_PLAYER][i]:
                                   0.3018 * (DataUtils.check_range(venue_range[6], self.venue[self.COL_OVERS][i]))
                                   + 0.2783 * (DataUtils.check_range(venue_range[0], self.venue[self.COL_NO_OF_INN_BOWL][i]))
                                   + 0.1836 * (DataUtils.check_range(venue_range[8], self.venue[self.COL_BOWL_SR][i]))
                                   + 0.1391 * (DataUtils.check_range(venue_range[7], self.venue[self.COL_BOWL_AVG][i]))
                                   + 0.0972 * (DataUtils.check_range(venue_range[9], self.venue[self.COL_WICKET_HAUL][i]))
                               })
        return venue_bat, venue_bowl

    def calc_da(self):
        consistency_range = ConsistencyDAO.get_con_range(self.TRADITIONAL_ATTRS)
        consistency_bat, consistency_bowl = self.consistency_range(consistency_range)
        total_con_bat, total_con_bowl = self.total_consistency_range(consistency_range)

        form_range = FormDAO.get_form_range(self.TRADITIONAL_ATTRS)
        form_bat, form_bowl = self.form_range(form_range)
        recent_form_bat, recent_form_bowl = self.recent_form_range(form_range)

        opposition_range = OppositionDAO.get_opp_range(self.TRADITIONAL_ATTRS)
        opposition_bat, opposition_bowl = self.opposition_range(opposition_range)

        venue_range = VenueDAO.get_ven_range(self.TRADITIONAL_ATTRS)
        venue_bat, venue_bowl = self.venue_range(venue_range)

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

    # @staticmethod
    # def __modify_prediction(df):
    #     df = df.groupby(level=0).sum()
    #     return df

    FILE_MODEL = 'model\\model_pickle.pkl'
    FILE_MODEL_RUNS = 'model\\model_pickle_runs.pkl'
    FILE_MODEL_WICKETS = 'model\\model_pickle_wickets.pkl'
    FILE_MODEL_NB = 'model\\model_pickle_nb'
    FILE_MODEL_SVM = 'model\\model_pickle_svm'
    FILE_MODEL_DT = 'model\\model_pickle_dt'

    TRADITIONAL_ATTRS = ['No. of Innings', 'Batting Average', 'Batting Strike Rate', 'Centuries', 'Fifties', 'Zeros',
                         'Highest Score', 'Overs', 'Bowling Average', 'Bowling Strike Rate', 'FF']

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
