# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 20:49:58 2020

@author: user 2
"""

import pandas as pd
from fuzzywuzzy import fuzz

class DataUtils():
    
    def __get_cols(table_rows):
        data_cols = []
        for tr in table_rows:
            th = tr.find_all('th')
            data_cols = [tx.text.strip() for tx in th]
            return data_cols
        
    def __get_rows(table_rows):
        data_rows = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [tx.text.strip() for tx in td]
            data_rows.append(row)
        return data_rows
    
    @classmethod
    def create_df(cls, table):
        cols = cls.__get_cols(table)
        rows = cls.__get_rows(table)
        if not cols:
            return pd.DataFrame(rows)
        else:
            return pd.DataFrame(rows, columns=cols)
        
    @classmethod
    def get_players(cls, soup):
        return soup.find_all("table", attrs={"class" : "engineTable"})
    
    @classmethod
    def remove_asterik_all(cls, series):
        hs_list = []
        for value in series:
            value = cls.remove_asterik(str(value))
            hs_list.append(value)
        return hs_list 
    
    @classmethod
    def remove_asterik(cls, value):
        if '*' in value:
            return value.replace('*', '')
        elif '-' in value:
            return value.replace('-', '0')
        else:
            return value
    
    @classmethod
    def drop_cols(cls, df, cols):
        return df.drop(cols, axis = 'columns') 
    
    @classmethod
    def playing_eleven_df(cls, df, playing_eleven):
        playing_df = pd.DataFrame()
        for player in playing_eleven:
            x = 0
            for i in df.index:
                if df['Player'][i] is not None:
                    player_ci = cls.__check_fuzz(player, df['Player'].tolist())
                    if player_ci == df['Player'][i]:
                        playing_df = playing_df.append(df.loc[i])
                        x = 1
                        break
                    
            if x == 1:
                continue
            
            if not playing_df.empty and player_ci not in playing_df['Player']:
                playing_df = playing_df.append(pd.Series(0, index=playing_df.columns), ignore_index=True)
            else:
                playing_df = playing_df.append({'Player': 'Unknown'}, ignore_index=True).fillna(0)
        
        playing_df['Player'] = playing_eleven
        return playing_df.reset_index(drop=True)
    
    def __check_fuzz(player, player_list):
        for player_name in player_list:
            if player_name is not None:
                partial_ratio = fuzz.partial_ratio(player, player_name)
                if partial_ratio == 100:
                    return player_name
                else:
                    p = player.split()
                    pn = player_name.split()
                    if p[1] == pn[1]:
                        if player[0] == player_name[0]:
                            return player_name
                        elif player_name == "SL Malinga":
                            return player_name
                    
        return player
    
    @classmethod
    def check_range(cls, rs, num):
        for row in rs:
            if num == 0:
                return 0
            elif num >= row[0] and num <= row[1]:
                return row[2]
            elif row[3] > 0 and num >= row[3]:
                return row[2]
        