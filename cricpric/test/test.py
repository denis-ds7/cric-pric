# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:45:38 2020

@author: user 2
"""
import os

from cricpric.preparation.data_collection import CreateOVC
from cricpric.processing.create_modify import DerivedAttrs
import pandas as pd
from cricpric.modeling.predict_performance import PlayerPerformance
from cricpric.processing.data_extraction import ModifyCFOV

host_team = "Chennai Super Kings"
away_team = "Mumbai Indians"
venue = "Rajiv Gandhi International Stadium"

bat = "bat"
bowl = "bowl"

host_playing = ["Parthiv Patel", "Umesh Yadav"]
away_playing = ["Kedar Jadhav", "Suresh Raina"]

# host_playing = ["Faf du Plessis", "Shane Watson", "Suresh Raina", "Ambati Rayudu", "MS Dhoni", "Ravindra Jadeja",
#                 "Dwayne Bravo", "Deepak Chahar", "Shardul Thakur", "Harbhajan Singh", "Imran Tahir"]
# away_playing = ["Quinton de Kock", "Rohit Sharma", "Suryakumar Yadav", "Ishan Kishan", "Hardik Pandya",
#                 "Kieron Pollard", "Krunal Pandya", "Mitchell McClenaghan", "Rahul Chahar", "Lasith Malinga",
#                 "Jasprit Bumrah"]

FILE_TRAIN_DATA = "../../config/train_data.csv"

# create = CreateOVC(away_playing, '')
# df = create.create_total_consistency()
# modify = ModifyCFOV()
# df = modify.modify_total_consistency(df)
# df.to_csv("test.csv")
# print(df)


def test_predict():
    da = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
    da.consistency_form(bat, bowl)
    da.opposition_venue(bat, bowl)
    da.total_consistency()

    con = pd.read_csv(da.FILE_CONSISTENCY)

    total_con = pd.read_csv(da.FILE_TOTAL_CONSISTENCY)

    form = pd.read_csv(da.FILE_FORM)

    opp = pd.read_csv(da.FILE_OPPOSITION)

    ven = pd.read_csv(da.FILE_VENUE)

    ipl = PlayerPerformance(con, total_con, form, opp, ven)
    array = ipl.predict()
    print(array)


def test_train_data():
    train_data = pd.read_csv("../../config/train_data_old.csv")
    y = train_data['DreamTeam']
    x = train_data.drop("DreamTeam", axis='columns')
    x.set_index('Unnamed: 0', inplace=True)

    PlayerPerformance.fit_model(x, y)


def prepare_train_data():
    da = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
    da.consistency_form(bat, bowl)
    da.opposition_venue(bat, bowl)
    da.total_consistency()

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


prepare_train_data()
