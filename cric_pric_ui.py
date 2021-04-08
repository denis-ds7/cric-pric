# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 12:43:18 2020

@author: user 2
"""

import streamlit as st

from cricpric.dao.dao import TeamsDAO, GroundsDAO, PlayersDAO
from cricpric.processing.services import CricPricService
# from PIL import Image

# st.set_page_config(page_title="CricPric",
#                    page_icon="🏏")
#
# image = Image.open('media\\i01_cric-pric-logo.JPG')
# image_logo, title = st.beta_columns([0.5, 3])
# image_logo.image(image)
# title.write("# CricPric")

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


@st.cache(suppress_st_warning=True)
def on_predict():
    service = CricPricService()
    return service.process(host_team, away_team, venue, host_playing, away_playing)


@st.cache(suppress_st_warning=True)
def on_consistency():
    service = CricPricService()
    return service.consistency_stats(host_team, away_team, venue, host_playing, away_playing)


@st.cache(suppress_st_warning=True)
def on_venue():
    service = CricPricService()
    return service.venue_stats(host_team, away_team, venue, host_playing, away_playing)


@st.cache(suppress_st_warning=True)
def on_opposition():
    service = CricPricService()
    return service.opposition_stats(host_team, away_team, venue, host_playing, away_playing)


@st.cache(suppress_st_warning=True)
def on_recent_form():
    service = CricPricService()
    return service.recent_form_stats(host_team, away_team, venue, host_playing, away_playing)


@st.cache(suppress_st_warning=True)
def on_form():
    service = CricPricService()
    return service.form_stats(host_team, away_team, venue, host_playing, away_playing)


host_team, away_team, venue, host_playing, away_playing = populate_data()


if st.button(TEXT_PREDICT, help='Click to get the players performance prediction.'
                                'Ex: Will a player be in DreamTeam, Run Prediction and Wicket Prediction'):
    if host_team == 'Select Team':
        st.info("Please select Host Team")
        st.stop()
    if away_team == 'Select Team':
        st.info("Please select Away Team")
        st.stop()
    if venue == 'Select Venue':
        st.info("Please select Venue")
        st.stop()
    if not host_playing:
        st.info("Please select host players")
        st.stop()
    if not away_playing:
        st.info("Please select away players")
        st.stop()

    prediction, dataset, batting_plot, bowling_plot = on_predict()

    st.write(TEXT_PREDICTED_PLAYERS)
    st.write(prediction)
    st.pyplot(batting_plot)
    st.pyplot(bowling_plot)
    st.dataframe(dataset)
if st.button("Consistency Stats", help='Click to get the stats of all match played by a player for a IPL team.'
                                       'Ex: Stats of MS Dhoni played for CSK in all IPL Season.'):
    if host_team == 'Select Team':
        st.info("Please select Host Team")
        st.stop()
    if away_team == 'Select Team':
        st.info("Please select Away Team")
        st.stop()
    if venue == 'Select Venue':
        st.info("Please select Venue")
        st.stop()
    if not host_playing:
        st.info("Please select host players")
        st.stop()
    if not away_playing:
        st.info("Please select away players")
        st.stop()
    con = on_consistency()
    st.write(con)

if st.button("Venue Stats", help='Click to get the stats of player played in an venue. '
                                 'Ex: Stats of Rohit Sharma played in Wankhede Stadium.'):
    if host_team == 'Select Team':
        st.info("Please select Host Team")
        st.stop()
    if away_team == 'Select Team':
        st.info("Please select Away Team")
        st.stop()
    if venue == 'Select Venue':
        st.info("Please select Venue")
        st.stop()
    if not host_playing:
        st.info("Please select host players")
        st.stop()
    if not away_playing:
        st.info("Please select away players")
        st.stop()
    ven = on_venue()
    st.write(ven)

if st.button("Opposition Stats", help='Click to get the stats of player played against opposition team. '
                                      'Ex: Stats of MS Dhoni played against Mumbai Indians'):
    if host_team == 'Select Team':
        st.info("Please select Host Team")
        st.stop()
    if away_team == 'Select Team':
        st.info("Please select Away Team")
        st.stop()
    if venue == 'Select Venue':
        st.info("Please select Venue")
        st.stop()
    if not host_playing:
        st.info("Please select host players")
        st.stop()
    if not away_playing:
        st.info("Please select away players")
        st.stop()
    opp = on_opposition()
    st.write(opp)

if st.button("Recent Form Stats", help='Click to get the stats of player performance in the current season. '
                                       'Ex. Stats of MS Dhoni in IPL 2021'):
    if host_team == 'Select Team':
        st.info("Please select Host Team")
        st.stop()
    if away_team == 'Select Team':
        st.info("Please select Away Team")
        st.stop()
    if venue == 'Select Venue':
        st.info("Please select Venue")
        st.stop()
    if not host_playing:
        st.info("Please select host players")
        st.stop()
    if not away_playing:
        st.info("Please select away players")
        st.stop()
    rf = on_recent_form()
    st.write(rf)

if st.button("Form Stats", help='Click to get the stats of player performance in the last IPL season. '
                                'Ex: Stats of Rohit Sharma in IPL 2020'):
    if host_team == 'Select Team':
        st.info("Please select Host Team")
        st.stop()
    if away_team == 'Select Team':
        st.info("Please select Away Team")
        st.stop()
    if venue == 'Select Venue':
        st.info("Please select Venue")
        st.stop()
    if not host_playing:
        st.info("Please select host players")
        st.stop()
    if not away_playing:
        st.info("Please select away players")
        st.stop()
    form = on_form()
    st.write(form)
