# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 12:43:18 2020

@author: user 2
"""

import streamlit as st

from cricpric.dao.dao import TeamsDAO, GroundsDAO, PlayersDAO
from cricpric.processing.services import CricPricService

TEXT_TITLE = """
         # CricPric
         Predict player performance
         """

TEXT_HOST_TEAM = "Host Team"
TEXT_AWAY_TEAM = "Away Team"
TEXT_VENUE = "Venue"
TEXT_HOST_MULTISELECT = "Select playing 11 of host team"
TEXT_AWAY_MULTISELECT = "Select playing 11 of away team"
TEXT_PREDICT = "Predict"
TEXT_PREDICTED_PLAYERS = "Predicted Players"

EX_INVALID_TEAMS = "Invalid teams in ({0})"
EX_INVALID_VENUE = "Invalid venue in ({0})"

# Title and sub-title
st.write(TEXT_TITLE)


def get_grounds():
    return GroundsDAO.get_grounds()


def get_host_playing(host_t):
    return PlayersDAO.get_players(host_t)


def get_away_playing(away_t):
    return PlayersDAO.get_players(away_t)


def get_teams():
    return TeamsDAO.get_teams()


def populate_data():

    teams = get_teams()
    if not teams or teams is None:
        raise ValueError(EX_INVALID_TEAMS, teams)
    teams.insert(0, 'Select Team')
    host_t = st.selectbox(TEXT_HOST_TEAM, teams, index=0)
    away_t = st.selectbox(TEXT_AWAY_TEAM, teams, index=0)

    grounds = get_grounds()
    if not grounds or grounds is None:
        raise ValueError(EX_INVALID_VENUE.format(grounds))
    grounds.insert(0, 'Select Venue')
    ground = st.selectbox(TEXT_VENUE, grounds, index=0)

    host_p = get_host_playing(host_t)
    host_players = st.multiselect(TEXT_HOST_MULTISELECT, host_p)

    away_p = get_away_playing(away_t)
    away_players = st.multiselect(TEXT_AWAY_MULTISELECT, away_p)

    return host_t, away_t, ground, host_players, away_players


def on_predict():
    service = CricPricService()
    prediction, dataset, batting_plot, bowling_plot = service.process(host_team, away_team, venue, host_playing, away_playing)

    st.write(TEXT_PREDICTED_PLAYERS)
    st.write(prediction)

    st.pyplot(batting_plot)
    st.pyplot(bowling_plot)

    st.write()
    st.dataframe(dataset)


def on_venue():
    service = CricPricService()
    ven = service.venue_stats(host_team, away_team, venue, host_playing, away_playing)
    st.write(ven)


host_team, away_team, venue, host_playing, away_playing = populate_data()

if st.button(TEXT_PREDICT):
    on_predict()

if st.button("Venue Stats"):
    on_venue()
