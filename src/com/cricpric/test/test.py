# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:45:38 2020

@author: user 2
"""

from com.cricpric.processing.create_modify import DerivedAttrs
from com.cricpric.dao.dao import PlayersDAO

host_team = "Mumbai Indians"
away_team = "Chennai Super Kings"
venue = "Rajiv Gandhi International Stadium"

bat = "bat"
bowl = "bowl"

host_playing = ["Rohit Sharma", "Hardik Pandya", "Lasith Malinga"]
away_playing = ["MS Dhoni", "Imran Tahir", "Suresh Raina"]

# derived_attr = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
# derived_attr.consistency_form(bat, bowl)
# derived_attr.opposition_venue(bat, bowl)

players = PlayersDAO.get_players(away_team)

da = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
da.consistency_form(bat, bowl)
da.opposition_venue(bat, bowl)

