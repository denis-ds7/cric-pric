# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:21:04 2020

@author: user 2
"""
from bs4 import BeautifulSoup
import requests


class ConstantUrl:
    CONSISTENCY_BAT_URL = "https://stats.espncricinfo.com/ci/engine/records/averages/batting.html?id=117;type=trophy"
    CONSISTENCY_BOWL_URL = "https://stats.espncricinfo.com/ci/engine/records/averages/bowling.html?id=117;type=trophy"
    FORM_BAT_BOWL_URL = "https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=12741;type=tournament"
    FORM_BAT_URL = "https://stats.espncricinfo.com/ci/engine/records/averages/batting.html?id=12741;type=tournament"
    FORM_BOWL_URL = "https://stats.espncricinfo.com/ci/engine/records/averages/bowling.html?id=12741;type=tournament"
    OPPOSITION_URL = "http://www.howstat.com/cricket//Statistics/IPL/PlayerOpponents.asp?"
    VENUE_URL = "http://www.howstat.com/cricket/Statistics/IPL/PlayerGrounds.asp?"
    CAREER_INN_BAT_URL = "http://howstat.com/cricket/Statistics/IPL/PlayerProgressBat.asp?"
    TOTAL_CONSISTENCY_URL = "http://www.howstat.com/cricket/Statistics/IPL/PlayerOverview.asp?"
    RECENT_FORM_BAT_BOWL_URL = "https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=13533;type=tournament"


class AlterUrls:
    def __init__(self, url):
        if not url or url is None:
            raise ValueError("Invalid url")
        self.url = url
        
    def team_url(self, team_id):
        if not team_id or team_id is None:
            raise ValueError(self.EX_TEAM_ID.format(team_id))
        return self.url+";team="+team_id
    
    def player_url(self, player_id):
        if not player_id or player_id is None:
            raise ValueError(self.EX_Player_ID.format(player_id))
        return self.url+"PlayerID="+player_id
    
    EX_TEAM_ID = "Invalid team id in ({0})"
    EX_Player_ID = "Invalid player id in ({0})"


class BSoup:
    
    def __init__(self, url):
        if not url or url is None:
            raise ValueError("Invalid url")
        self.url = url
        
    def get_soup(self):
        html = requests.get(self.url)
        return BeautifulSoup(html.content, 'lxml')
