# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 12:43:18 2020

@author: user 2
"""


import streamlit as st
from com.cricpric.dao.dao import TeamsDAO, GroundsDAO, PlayersDAO
from com.cricpric.processing.create_modify import DerivedAttrs
import pandas as pd
from os import path

#Title and sub-title
st.write("""
         # CricPric
         Predict player performance
         """)
         
bat = "bat"
bowl = "bowl"

teams = TeamsDAO.get_teams()
host_team = st.selectbox("Host Team", teams, key='host')
away_team = st.selectbox("Away Team", teams, key='away')

grounds = GroundsDAO.get_grounds()
venue = st.selectbox("Venue", grounds, key='venue')

host_players = PlayersDAO.get_players(host_team)
host_playing = st.multiselect("Select playing 11 of host team", host_players, key='host_playing')

away_players = PlayersDAO.get_players(away_team)
away_playing = st.multiselect("Select playing 11 of away team", away_players, key='away_playing')

if st.button("Predict"):
    derived_attr = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
    derived_attr.consistency_form(bat, bowl)
    derived_attr.opposition_venue(bat, bowl)
    
    st.subheader("Players Stats")
    if path.exists(derived_attr.FILE_CONSISTENCY) and path.exists(derived_attr.FILE_FORM) \
        and path.exists(derived_attr.FILE_OPPOSITION) and path.exists(derived_attr.FILE_VENUE):
        
        st.write("Consistency")
        con = pd.read_csv('consistency.csv')
        st.dataframe(con)
        
        st.write("Form")
        form = pd.read_csv('form.csv')
        st.dataframe(form)
        
        st.write("Opposition")
        opp = pd.read_csv('opposition.csv')
        st.dataframe(opp)
        
        st.write("Venue")
        ven = pd.read_csv('venue.csv')
        st.dataframe(ven)
    else:
        st.write("Invalid details selected")