# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 19:24:09 2020

@author: user 2
"""


import pandas as pd
from com.cricpric.service.data_url import AlterUrls, ConstantUrl, BSoup
from com.cricpric.util.util import DataUtils
from com.cricpric.dao.dao import TeamsDAO, PlayersDAO

class CreateCF:
    
    def __init__(self, team_name, bat_bowl, players_list):
        self.team_name = team_name
        self.bat_bowl = bat_bowl
        self.players_list = players_list
        
    def create_consistency(self):
        if self.bat_bowl == "bat":
            alter_url = AlterUrls(ConstantUrl.CONSISTENCY_BAT_URL)
        elif self.bat_bowl == "bowl":
            alter_url = AlterUrls(ConstantUrl.CONSISTENCY_BOWL_URL)
            
        team_id = TeamsDAO.get_team_id(self.team_name)
        url = alter_url.team_url(team_id)
        
        soup = BSoup(url).get_soup()
        players = DataUtils.get_players(soup)
        table_rows = players[0].find_all("tr")
        
        df = DataUtils.create_df(table_rows)
        return DataUtils.playing_eleven_df(df, self.players_list)
    
    def create_form(self):
        team_id = TeamsDAO.get_team_id(self.team_name)
        alter_url = AlterUrls(ConstantUrl.FORM_BAT_BOWL_URL)
        url = alter_url.team_url(team_id)
        
        soup = BSoup(url).get_soup()
        players = DataUtils.get_players(soup)
        
        if self.bat_bowl == "bat":
            table_rows = players[0].find_all("tr")
            df = DataUtils.create_df(table_rows)
            return DataUtils.playing_eleven_df(df, self.players_list)
        elif self.bat_bowl == "bowl":
            table_rows = players[1].find_all("tr")
            df = DataUtils.create_df(table_rows)
            return DataUtils.playing_eleven_df(df, self.players_list)
    
    
class CreateOV:
    
    def __init__(self, players_list, bat_bowl):
        self.players_list = players_list
        self.bat_bowl = bat_bowl
    
    def create_opposition(self, opponent_team):
        opposition_df = pd.DataFrame()
        players_id_list = PlayersDAO.get_player_id(self.players_list)
    
        for player_id in players_id_list:
            if player_id is not None:
                versus = self.__find_table(player_id, ConstantUrl.OPPOSITION_URL)
            else:
                opposition_df = self.__default_values_opposition(opposition_df, opponent_team)
                continue
            
            if len(versus) > 0:
                if self.bat_bowl == "bat":
                    table_rows = versus[0].find_all("tr")
                    bat_o_df = self.__get_df(table_rows)
                    opposition_df = opposition_df.append(self.__check_versus(bat_o_df, opponent_team), ignore_index=True)
                elif self.bat_bowl == "bowl":
                    if len(versus) > 1:
                        table_rows = versus[1].find_all("tr")
                        bowl_o_df = self.__get_df(table_rows)
                        opposition_df = opposition_df.append(self.__check_versus(bowl_o_df, opponent_team), ignore_index=True)
                    else:
                        opposition_df = self.__default_values_opposition(opposition_df, opponent_team)
            else:
                opposition_df = self.__default_values_opposition(opposition_df, opponent_team)
        
        opposition_df = opposition_df.fillna(0)
        opposition_df['Player'] = self.players_list
    
        if self.bat_bowl == "bat":
            opposition_df['Zeros'] = self.__bat_zeros_opposition(players_id_list, opponent_team)
        elif self.bat_bowl == "bowl":
            opposition_df['InnsBowl'] = self.__bowl_inn(opposition_df)
            
        return opposition_df
    
    def create_venue(self, stadium_venue):
        venue_df = pd.DataFrame()
        players_id_list = PlayersDAO.get_player_id(self.players_list)
    
        for player_id in players_id_list:
            if player_id is not None:
                venue = self.__find_table(player_id, ConstantUrl.VENUE_URL)
            else:
                venue_df = self.__default_values_venue(venue_df, stadium_venue)
                continue
            
            if len(venue) > 0:
                if self.bat_bowl == "bat":
                    table_rows = venue[0].find_all("tr")
                    bat_v_df = self.__get_df(table_rows)
                    venue_df = venue_df.append(self.__check_ground(bat_v_df, stadium_venue), ignore_index=True)
                elif self.bat_bowl == "bowl":
                    if len(venue) > 1:
                        table_rows = venue[1].find_all("tr")
                        bowl_v_df = self.__get_df(table_rows)
                        venue_df = venue_df.append(self.__check_ground(bowl_v_df, stadium_venue), ignore_index=True)
                    else:
                        venue_df = self.__default_values_venue(venue_df, stadium_venue)
            else:
                venue_df = self.__default_values_venue(venue_df, stadium_venue)
                
        venue_df = venue_df.fillna(0)
        venue_df['Player'] = self.players_list
        
        if self.bat_bowl == "bat":
            venue_df['Zeros'] = self.__bat_zeros_venue(players_id_list, stadium_venue)
            venue_df['BatSR'] = self.__bat_sr_venue(players_id_list, stadium_venue)
        elif self.bat_bowl == "bowl":
            venue_df['InnsBowl'] = self.__bowl_inn(venue_df)
            
        return venue_df
    
    def __default_values_venue(self, venue_df, stadium_venue):
        if not venue_df.empty:
            venue_df = venue_df.append(pd.Series(0, index=venue_df.columns), ignore_index=True)
            return venue_df
        else:
            venue_df = venue_df.append({'Ground' : stadium_venue}, ignore_index=True).fillna(0)
            return venue_df
            
    def __default_values_opposition(self, opposition_df, opponent_team):
        if not opposition_df.empty:
            opposition_df = opposition_df.append(pd.Series(0, index=opposition_df.columns), ignore_index=True)        
            return opposition_df
        else:
            opposition_df = opposition_df.append({'Versus' : opponent_team}, ignore_index=True).fillna(0)
            return opposition_df

    def __find_table(self, player_id, url):
        alter_url = AlterUrls(url)
        player_url = alter_url.player_url(player_id)
        soup = BSoup(player_url).get_soup()
        return soup.find_all("table", attrs={"class" : "TableLined"})
    
    def __get_df(self, table_rows):
        df = DataUtils.create_df(table_rows)
        df.columns = df.loc[0]
        df = df.drop(df.index[0])
        return df
    
    def __check_versus(self, df, opponent_team):
        for i in df.index:
            if opponent_team in df['Versus'][i]:
                return df.loc[i]      
        return pd.Series(0, index=df.columns)
    
    def __bat_zeros_opposition(self, players_id_list, opponent_team):
        ser = []
        
        for player_id in players_id_list:
            count = 0
            df = self.__get_zeros_df(player_id)
            if df is not None:
                for i in df.index:
                    if opponent_team in df['Versus'][i]:
                        if df['Runs'][i] == "0":
                            count += 1
                
            ser.append(count)
        return ser
    
    def __get_zeros_df(self, player_id):
        if player_id is not None:
            table = self.__find_table(player_id, ConstantUrl.CAREER_INN_BAT_URL)
        else:
            return
        
        if len(table) > 0:
            table_rows = table[0].find_all("tr")
            df = DataUtils.create_df(table_rows)
            df.columns = df.loc[2]
            df = df.drop(df.index[2])
            df = df.dropna()
            return df
        return
    
    def __bowl_inn(self, df):
        ser = []
        for i in df.index:
            if pd.to_numeric(df['O'][i]) > 0 and pd.to_numeric(df['O'][i]) <= 3:
                ser.append(1)
            else:
                bowl_inns = round(pd.to_numeric(df['O'][i])/3)
                if pd.to_numeric(df['O'][i])%3 != 0 and bowl_inns > 0:
                    bowl_inns += 1
                ser.append(bowl_inns)
        return ser
    
    def __check_ground(self, df, stadium_venue):
        for i in df.index:
            if stadium_venue in df['Ground'][i]:
                return df.loc[i]
        return pd.Series(0, index=df.columns)
    
    def __bat_zeros_venue(self, player_id_list, stadium_venue):
        ser = []
        for player_id in player_id_list:
            count = 0
            df = self.__get_zeros_df(player_id)
            if df is not None:
                for i in df.index:
                    if stadium_venue in df['Ground'][i]:
                        if df['Runs'][i] == "0":
                            count += 1
            
            ser.append(count)
        return ser
    
    def __bat_sr_venue(self, player_id_list, stadium_venue):
        ser = []
        for player_id in player_id_list:
            total_runs = 0
            total_bf = 0
            if player_id is not None:
                table = self.__find_table(player_id, ConstantUrl.CAREER_INN_BAT_URL)
            else:
                ser.append(0)
                continue
            
            if len(table) > 0:
                table_rows = table[0].find_all("tr")
                df = DataUtils.create_df(table_rows)
                df = df.dropna()
                cols = ['0', 'Date', 'Versus', 'Ground', 'D/N', 'How Dismissed', 'Runs', 'B/F', 'S/R', '9', 'Aggr', 'Avg', 'S/R Pro']
                df.columns = cols
                df = df.drop(['0', '9'], axis=1)
                df = df.reset_index(drop=True)
                for i in df.index:
                    if stadium_venue in df['Ground'][i]:
                        total_runs += pd.to_numeric(DataUtils.remove_asterik(df['Runs'][i]))
                        total_bf += pd.to_numeric(DataUtils.remove_asterik(df['B/F'][i]))
                  
                if total_runs == 0 or total_bf == 0:
                    ser.append(0)
                else:
                    bat_sr = total_runs/total_bf * 100
                    ser.append(round(bat_sr, 2))
            else:
                ser.append(0)
                    
        return ser