# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:03:02 2020

@author: user 2
"""

from cricpric.service.db_resource import DBResource


class TeamsDAO:

    @classmethod
    def get_team_id(cls, team_name):
        if not team_name or team_name is None:
            raise ValueError(cls.EX_TEAM_NAME.format(team_name))

        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_TEAM_ID, (team_name,))
            for row in cursor:
                return row[0]
        except BaseException as be:
            raise RuntimeError(cls.EX_TEAM_ID.format(team_name), be)
        finally:
            cursor.close()
            con.close()

    @classmethod
    def get_teams(cls):
        teams = []
        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            # rs = cursor.execute(cls.GET_TEAMS)
            cursor.execute(cls.GET_TEAMS)
            for row in cursor:
                teams.append(row[0])
            return teams
        except BaseException as be:
            raise RuntimeError(cls.EX_TEAMS, be)
        finally:
            cursor.close()
            con.close()

    EX_TEAM_ID = "Failed getting team id using ({0})"
    EX_TEAMS = "Failed to get teams"
    EX_TEAM_NAME = "Invalid team name in ({0})"
    GET_TEAMS = "select teamName from dbo.teams"
    GET_TEAM_ID = "select citid from dbo.teams where teamname = (%s)"


class PlayersDAO:

    @classmethod
    def get_player_id(cls, players_list):
        if not players_list or players_list is None:
            raise ValueError(cls.EX_INVALID_PLAYERS.format(players_list))

        p_list = []
        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_PLAYER_ID, (players_list,))
            for row in cursor:
                p_list.append(row[0])
            return p_list
        except BaseException as be:
            raise RuntimeError(cls.EX_PLAYER_ID.format(players_list), be)
        finally:
            cursor.close()
            con.close()

    @classmethod
    def get_player_role(cls, player_name):
        if not player_name or player_name is None:
            raise ValueError(cls.EX_INVALID_PLAYER_NAME.format(player_name))

        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_PLAYER_ROLE % player_name)
            for row in cursor:
                return row[0]
        except BaseException as be:
            raise RuntimeError(cls.EX_PLAYER_ROLE.format(player_name), be)
        finally:
            cursor.close()
            con.close()

    @classmethod
    def get_players(cls, team_name):
        if not team_name or team_name is None:
            raise ValueError(cls.EX_INVALID_TEAM_NAME.format(team_name))

        players = []
        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_PLAYERS, (team_name,))
            for row in cursor:
                players.append(row[0])
            return players
        except BaseException as be:
            raise RuntimeError(cls.EX_PLAYERS.format(team_name), be)
        finally:
            cursor.close()
            con.close()

    EX_PLAYER_ID = "Error while getting player id using ({0})"
    EX_PLAYERS = "Error while getting players using ({0})"
    EX_PLAYER_ROLE = "Error while getting player role using ({0})"
    EX_INVALID_TEAM_NAME = "Invalid team name in ({0})"
    EX_INVALID_PLAYERS = "Invalid players in ({0})"
    EX_INVALID_PLAYER_NAME = "Invalid player name in ({0})"
    GET_PLAYER_ID = "select hspid from dbo.players where playerName = ANY(%s)" \
                    "order by playerName;"
    GET_PLAYER_ROLE = "select batbowl from dbo.players where playerName like '%%%s%%'"
    GET_PLAYERS = """select playerName from dbo.players
                  inner join dbo.teams
                  on dbo.players.teamid = dbo.teams.teamid
                  where teamName = (%s)"""


class GroundsDAO:

    @classmethod
    def get_grounds(cls):
        grounds = []
        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_GROUNDS)
            for row in cursor:
                grounds.append(row[0])
            return grounds
        except BaseException as be:
            raise RuntimeError(cls.EX_GROUNDS, be)
        finally:
            cursor.close()
            con.close()

    EX_GROUNDS = "Error while getting ground."
    GET_GROUNDS = "select gname from dbo.grounds"


class ConsistencyDAO:

    @classmethod
    def get_con_range(cls, ta_name):
        if not ta_name or ta_name is None:
            raise ValueError(cls.EX_TA_NAME.format(ta_name))

        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_CON_RANGE, (ta_name,))
            if cursor is not None:
                inn_range = cursor.fetchmany(5)
                bat_avg_range = cursor.fetchmany(5)
                bat_sr_range = cursor.fetchmany(5)
                centuries_range = cursor.fetchmany(3)
                fifties_range = cursor.fetchmany(5)
                zeros_range = cursor.fetchmany(5)
                overs_range = cursor.fetchmany(5)
                bowl_avg_range = cursor.fetchmany(5)
                bowl_sr_range = cursor.fetchmany(5)
                ff_range = cursor.fetchmany(4)
                return [inn_range, bat_avg_range, bat_sr_range, centuries_range, fifties_range, zeros_range,
                        overs_range, bowl_avg_range, bowl_sr_range, ff_range]
        except BaseException as be:
            raise RuntimeError(cls.EX_CON_RANGE.format(ta_name), be)
        finally:
            cursor.close()
            con.close()

    EX_CON_RANGE = "Error while getting consistency range using ({0})"
    EX_TA_NAME = "Invalid traditional attribute in ({0})"
    GET_CON_RANGE = "select startRange, endRange, value, maxRange from dbo.consistency \
                    inner join dbo.traditionalattribs \
                    on dbo.consistency.tid = dbo.traditionalattribs.tid \
                    where attribName = ANY(%s)"


class FormDAO:

    @classmethod
    def get_form_range(cls, ta_name):
        if not ta_name or ta_name is None:
            raise ValueError(cls.EX_TA_NAME.format(ta_name))

        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_FORM_RANGE, (ta_name,))
            if cursor is not None:
                inn_range = cursor.fetchmany(5)
                bat_avg_range = cursor.fetchmany(5)
                bat_sr_range = cursor.fetchmany(5)
                centuries_range = cursor.fetchmany(3)
                fifties_range = cursor.fetchmany(5)
                zeros_range = cursor.fetchmany(3)
                overs_range = cursor.fetchmany(5)
                bowl_avg_range = cursor.fetchmany(5)
                bowl_sr_range = cursor.fetchmany(5)
                ff_range = cursor.fetchmany(2)
                return [inn_range, bat_avg_range, bat_sr_range, centuries_range, fifties_range, zeros_range,
                        overs_range, bowl_avg_range, bowl_sr_range, ff_range]
        except BaseException as be:
            raise RuntimeError(cls.EX_FORM_RANGE.format(ta_name), be)
        finally:
            cursor.close()
            con.close()

    EX_TA_NAME = "Invalid traditional attribute in ({0})"
    EX_FORM_RANGE = "Error while getting form range using ({0})"
    GET_FORM_RANGE = "select startRange, endRange, value, maxRange from dbo.form \
                    inner join dbo.traditionalattribs \
                    on dbo.form.tid = dbo.traditionalattribs.tid \
                    where attribName = ANY(%s)"


class OppositionDAO:

    @classmethod
    def get_opp_range(cls, ta_name):
        if not ta_name or ta_name is None:
            raise ValueError(cls.EX_TA_NAME.format(ta_name))

        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_OPP_RANGE, (ta_name,))
            if cursor is not None:
                inn_range = cursor.fetchmany(5)
                bat_avg_range = cursor.fetchmany(5)
                bat_sr_range = cursor.fetchmany(5)
                centuries_range = cursor.fetchmany(3)
                fifties_range = cursor.fetchmany(5)
                zeros_range = cursor.fetchmany(3)
                overs_range = cursor.fetchmany(5)
                bowl_avg_range = cursor.fetchmany(5)
                bowl_sr_range = cursor.fetchmany(5)
                ff_range = cursor.fetchmany(2)
                return [inn_range, bat_avg_range, bat_sr_range, centuries_range, fifties_range, zeros_range,
                        overs_range, bowl_avg_range, bowl_sr_range, ff_range]
        except BaseException as be:
            raise RuntimeError(cls.EX_OPP_RANGE.format(ta_name), be)
        finally:
            cursor.close()
            con.close()

    EX_TA_NAME = "Invalid traditional attribute in ({0})"
    EX_OPP_RANGE = "Error while getting opposition range using ({0})"
    GET_OPP_RANGE = "select startRange, endRange, value, maxRange from dbo.opposition \
                    inner join dbo.traditionalattribs \
                    on dbo.opposition.tid = dbo.traditionalattribs.tid \
                    where attribName = ANY(%s)"


class VenueDAO:

    @classmethod
    def get_ven_range(cls, ta_name):
        if not ta_name or ta_name is None:
            raise ValueError(cls.EX_TA_NAME.format(ta_name))

        con = None
        cursor = None
        try:
            con = DBResource.get_instance().get_connection()
            cursor = con.cursor()
            cursor.execute(cls.GET_VEN_RANGE, (ta_name,))
            if cursor is not None:
                inn_range = cursor.fetchmany(5)
                bat_avg_range = cursor.fetchmany(5)
                bat_sr_range = cursor.fetchmany(5)
                centuries_range = cursor.fetchmany(2)
                fifties_range = cursor.fetchmany(2)
                hs_range = cursor.fetchmany(5)
                overs_range = cursor.fetchmany(5)
                bowl_avg_range = cursor.fetchmany(5)
                bowl_sr_range = cursor.fetchmany(5)
                ff_range = cursor.fetchmany(2)
                return [inn_range, bat_avg_range, bat_sr_range, centuries_range, fifties_range, hs_range,
                        overs_range, bowl_avg_range, bowl_sr_range, ff_range]
        except BaseException as be:
            raise RuntimeError(cls.EX_VEN_RANGE.format(ta_name), be)
        finally:
            cursor.close()
            con.close()

    EX_TA_NAME = "Invalid traditional attribute in ({0})"
    EX_VEN_RANGE = "Error while getting venue range using ({0})"
    GET_VEN_RANGE = "select startRange, endRange, value, maxRange from dbo.venue \
                    inner join dbo.traditionalattribs \
                    on dbo.venue.tid = dbo.traditionalattribs.tid \
                    where attribName = ANY(%s)"
