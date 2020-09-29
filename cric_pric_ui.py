# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 12:43:18 2020

@author: user 2
"""
import os
# from threading import Thread

import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

from cricpric.dao.dao import TeamsDAO, GroundsDAO, PlayersDAO
from cricpric.modeling.predict_performance import PlayerPerformance
from cricpric.processing.create_modify import DerivedAttrs
import pandas as pd
from os import path

TEXT_TITLE = """
         # CricPric
         Predict player performance
         """
TEXT_SUB_HEADER = "Players Stats"

TEXT_BAT = "bat"
TEXT_BOWL = "bowl"
TEXT_HOST_TEAM = "Host Team"
TEXT_AWAY_TEAM = "Away Team"
TEXT_VENUE = "Venue"
TEXT_HOST_MULTISELECT = "Select playing 11 of host team"
TEXT_AWAY_MULTISELECT = "Select playing 11 of away team"
TEXT_PREDICT = "Predict"
TEXT_DATA_SET = "Data Set"
TEXT_PREDICTED_PLAYERS = "Predicted Players"

EX_INVALID_HOST_TEAM = "Invalid host team in ({0})"
EX_INVALID_AWAY_TEAM = "Invalid away team in ({0})"
EX_INVALID_VENUE = "Invalid venue in ({0})"
EX_INVALID_HOST_PLAYING = "Invalid host playing in ({0})"
EX_INVALID_AWAY_PLAYING = "Invalid away playing in ({0})"
EX_INVALID_DETAILS = "Invalid details selected"
EX_CON_DATA = "Invalid consistency data ({0}) from ({1})"
EX_TOTAL_CON_DATA = "Invalid total consistency data ({0}) from ({1})"
EX_FORM_DATA = "Invalid form data ({0}) from ({1})"
EX_RECENT_FORM_DATA = "Invalid recent form data ({0}) from ({1})"
EX_OPP_DATA = "Invalid opposition data ({0}) from ({1})"
EX_VEN_DATA = "Invalid venue data ({0}) from ({1})"

FILE_TRAIN_DATA = "config\\train_data.csv"
FILE_TRAIN_DATA_FORM = "config\\train_data_r_form.csv"
FILE_TRAIN_DATA_RUNS = "config\\train_data_runs.csv"
FILE_TRAIN_DATA_WICKETS = "config\\train_data_wickets.csv"
FILE_DATASET = "config\\dataset.csv"

# Title and sub-title
st.write(TEXT_TITLE)

teams = TeamsDAO.get_teams()
host_team = st.selectbox(TEXT_HOST_TEAM, teams)
away_team = st.selectbox(TEXT_AWAY_TEAM, teams)

grounds = GroundsDAO.get_grounds()
venue = st.selectbox(TEXT_VENUE, grounds)

host_players = PlayersDAO.get_players(host_team)
host_playing = st.multiselect(TEXT_HOST_MULTISELECT, host_players, default=[])

away_players = PlayersDAO.get_players(away_team)
away_playing = st.multiselect(TEXT_AWAY_MULTISELECT, away_players)

if st.button(TEXT_PREDICT):
    if not host_team or host_team is None:
        raise ValueError(EX_INVALID_HOST_TEAM.format(host_team))
    if not away_team or away_team is None:
        raise ValueError(EX_INVALID_AWAY_TEAM.format(away_team))
    if not venue or venue is None:
        raise ValueError(EX_INVALID_VENUE.format(venue))
    if not host_playing or host_playing is None:
        raise ValueError(EX_INVALID_HOST_PLAYING.format(host_playing))
    if not away_playing or away_playing is None:
        raise ValueError(EX_INVALID_AWAY_PLAYING.format(away_playing))

    derived_attr = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
    # t1 = Thread(target=derived_attr.consistency_form, args=(TEXT_BAT, TEXT_BOWL))
    # t2 = Thread(target=derived_attr.total_consistency)
    # t3 = Thread(target=derived_attr.opposition_venue, args=(TEXT_BAT, TEXT_BOWL))
    # t1.start()
    # t2.start()
    # t3.start()
    # t1.join()
    # t2.join()
    # t3.join()
    # derived_attr.execute_run(TEXT_BAT, TEXT_BOWL)
    derived_attr.consistency_form(TEXT_BAT, TEXT_BOWL)
    derived_attr.opposition_venue(TEXT_BAT, TEXT_BOWL)
    derived_attr.total_consistency()

    st.subheader(TEXT_SUB_HEADER)
    if path.exists(derived_attr.FILE_CONSISTENCY) and path.exists(derived_attr.FILE_FORM) \
            and path.exists(derived_attr.FILE_OPPOSITION) and path.exists(derived_attr.FILE_VENUE):

        con = pd.read_csv(derived_attr.FILE_CONSISTENCY)
        tot_con = pd.read_csv(derived_attr.FILE_TOTAL_CONSISTENCY)
        form = pd.read_csv(derived_attr.FILE_FORM)
        r_form = pd.read_csv(derived_attr.FILE_RECENT_FORM)
        opp = pd.read_csv(derived_attr.FILE_OPPOSITION)
        ven = pd.read_csv(derived_attr.FILE_VENUE)

        if con is None or con.empty:
            raise ValueError(EX_CON_DATA.format(con, derived_attr.FILE_CONSISTENCY))
        if tot_con is None or tot_con.empty:
            raise ValueError(EX_TOTAL_CON_DATA.format(tot_con, derived_attr.FILE_TOTAL_CONSISTENCY))
        if form is None or form.empty:
            raise ValueError(EX_FORM_DATA.format(form, derived_attr.FILE_FORM))
        if r_form is None or r_form.empty:
            raise ValueError(EX_RECENT_FORM_DATA.format(r_form, derived_attr.FILE_RECENT_FORM))
        if opp is None or opp.empty:
            raise ValueError(EX_OPP_DATA.format((opp, derived_attr.FILE_OPPOSITION)))
        if ven is None or ven.empty:
            raise ValueError(EX_VEN_DATA.format(ven, derived_attr.FILE_VENUE))

        ipl = PlayerPerformance(con, tot_con, form, r_form, opp, ven)
        dataset = ipl.calc_da()
        if path.exists(FILE_DATASET):
            os.remove(FILE_DATASET)
        dataset.to_csv(FILE_DATASET)

        dataset = ipl.modify_data_set(dataset)
        dataset_recent = dataset.drop('RecentForm', axis=1)
        result = ipl.predict(dataset_recent)

        batsmen = dataset_recent[dataset_recent['BatBowl'] == 1]
        bowlers = dataset_recent[dataset_recent['BatBowl'] == 0]

        # runs_wicket_data = dataset.drop('BatBowl', axis=1)
        batsmen.drop('BatBowl', axis=1, inplace=True)
        bowlers.drop('BatBowl', axis=1, inplace=True)
        runs_predict = ipl.predict_runs(batsmen)
        wickets_predict = ipl.predict_wickets(bowlers)

        all_predictions = pd.merge(pd.merge(result, runs_predict, on='Players', how='left'), wickets_predict, on='Players', how='left')

        st.write(TEXT_PREDICTED_PLAYERS)
        st.write(all_predictions)
        #
        # st.write("Players Run Prediction")
        # st.write(runs_predict)
        #
        # st.write("Players Wickets Prediction")
        # st.write(wickets_predict)

        if os.path.exists(FILE_TRAIN_DATA):
            with open(FILE_TRAIN_DATA, 'a', newline='') as f:
                dataset_recent.to_csv(f, mode='a', header=False)
        else:
            dataset_recent.to_csv(FILE_TRAIN_DATA)

        if os.path.exists(FILE_TRAIN_DATA_FORM):
            with open(FILE_TRAIN_DATA_FORM, 'a', newline='') as f:
                dataset.to_csv(f, mode='a', header=False)
        else:
            dataset.to_csv(FILE_TRAIN_DATA_FORM)

        if os.path.exists(FILE_TRAIN_DATA_RUNS):
            with open(FILE_TRAIN_DATA_RUNS, 'a', newline='') as f:
                batsmen.to_csv(f, mode='a', header=False)
        else:
            batsmen.to_csv(FILE_TRAIN_DATA_RUNS)

        if os.path.exists(FILE_TRAIN_DATA_WICKETS):
            with open(FILE_TRAIN_DATA_WICKETS, 'a', newline='') as f:
                bowlers.to_csv(f, mode='a', header=False)
        else:
            bowlers.to_csv(FILE_TRAIN_DATA_WICKETS)

        bowlers = bowlers.reset_index()
        batsmen = batsmen.reset_index()

        bat_labels = batsmen['index']
        bat_opp = batsmen['Opposition']
        bat_ven = batsmen['Venue']
        recent_bat = dataset[dataset['BatBowl'] == 1]
        bat_rf = recent_bat['RecentForm']

        bowl_labels = bowlers['index']
        bowl_opp = bowlers['Opposition']
        bowl_ven = bowlers['Venue']
        recent_bowl = dataset[dataset['BatBowl'] == 0]
        bowl_rf = recent_bowl['RecentForm']
        # men_means = [20, 34, 30, 35, 27]
        # women_means = [25, 32, 34, 20, 25]

        x = np.arange(len(bat_labels))  # the label locations
        x1 = np.arange(len(bowl_labels))  # the label locations
        y = np.arange(0, 6, 0.5)
        width = 0.15  # the width of the bars

        fig1, ax1 = plt.subplots()
        ax1.bar(x - width, bat_opp, width, label='Opposition')
        ax1.bar(x, bat_ven, width, label='Venue')
        ax1.bar(x + width, bat_rf, width, label='Recent Form')

        fig2, ax2 = plt.subplots()
        ax2.bar(x1 - width, bowl_opp, width, label='Opposition')
        ax2.bar(x1, bowl_ven, width, label='Venue')
        ax2.bar(x1 + width, bowl_rf, width, label='Recent Form')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax1.set_ylabel('Scores')
        ax1.set_title('Batting Scores')
        ax1.set_xticks(x)
        ax1.set_xticklabels(bat_labels, rotation=90)
        ax1.set_yticks(y)
        ax1.set_yticklabels(y)
        ax1.axhline(3.0, color='gray', lw=1)
        ax1.legend()

        ax2.set_ylabel('Scores')
        ax2.set_title('Bowling Scores')
        ax2.set_xticks(x1)
        ax2.set_xticklabels(bowl_labels, rotation=90)
        ax2.set_yticks(y)
        ax2.set_yticklabels(y)
        ax2.axhline(3.0, color='gray', lw=1)
        ax2.legend()

        fig1.tight_layout()
        fig2.tight_layout()

        st.pyplot(fig1)
        st.pyplot(fig2)

        st.write()
        st.dataframe(dataset)

    else:
        st.write(EX_INVALID_DETAILS)
