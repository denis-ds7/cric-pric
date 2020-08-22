# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:03:02 2020

@author: user 2
"""

from com.cricpric.service.db_resource import DBResource
from com.cricpric.util.util import DataUtils

class TeamsDAO:
    
    @classmethod
    def get_team_id(cls, team_name):
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select citid from teams where teamName = ?", team_name)
        for row in rs:
            return row[0]
        
    @classmethod
    def get_teams(cls):
        teams = []
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select teamName from teams")
        for row in rs:
            teams.append(row[0])
        return teams
        
        
class PlayersDAO:
    
    @classmethod
    def get_player_id(cls, players_list):    
        p_list = []
        for player in players_list:
            cursor = DBResource.get_instance().get_cursor()
            rs = cursor.execute("select hspid from players where playerName like '%%%s%%'" %(player))
            for row in rs:
                p_list.append(row[0])
        return p_list
    
    @classmethod
    def get_players(cls, team_name):
        players = []
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select playerName from players \
                            inner join teams \
                            on players.teamid = teams.teamid \
                            where teamName = ?", team_name)
        for row in rs:
            players.append(row[0])
        return players
        
class GroundsDAO:
    
    @classmethod
    def get_grounds(cls):
        grounds = []
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select gname from grounds")
        for row in rs:
            grounds.append(row[0])
        return grounds
    
class ConsistencyDAO:
    
    @classmethod
    def get_con_range(cls, num, ta_name):
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select startRange, endRange, value, maxRange from Consistency \
                            inner join TraditionalAttribs \
                            on Consistency.tid = TraditionalAttribs.tid \
                            where attribName = ?", ta_name)
        return DataUtils.check_range(rs, num)
    
class FormDAO:
    
    @classmethod
    def get_form_range(cls, num, ta_name):
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select startRange, endRange, value, maxRange from Form \
                            inner join TraditionalAttribs \
                            on Form.tid = TraditionalAttribs.tid \
                            where attribName = ?", ta_name)
        return DataUtils.check_range(rs, num)
    
class OppositionDAO:
    
    @classmethod
    def get_opp_range(cls, num, ta_name):
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select startRange, endRange, value, maxRange from Opposition \
                            inner join TraditionalAttribs \
                            on Opposition.tid = TraditionalAttribs.tid \
                            where attribName = ?", ta_name)
        return DataUtils.check_range(rs, num)
    
class VenueDAO:
    
    @classmethod
    def get_ven_range(cls, num, ta_name):
        cursor = DBResource.get_instance().get_cursor()
        rs = cursor.execute("select startRange, endRange, value, maxRange from Venue \
                            inner join TraditionalAttribs \
                            on Venue.tid = TraditionalAttribs.tid \
                            where attribName = ?", ta_name)
        return DataUtils.check_range(rs, num)