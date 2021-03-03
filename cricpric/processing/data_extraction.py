# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 16:11:50 2020

@author: user 2
"""

from cricpric.util.util import DataUtils
import pandas as pd


class ModifyCFOV:

    def modify_cf_df(self, bat, bowl):
        if bat is None or bowl is None or bat.empty or bowl.empty:
            raise RuntimeError(self.EX_MODIFY_CF.format(bat, bowl))

        # bat = self.__drop_na(bat)
        # bowl = self.__drop_na(bowl)
        
        bat = self.__replace_zero(bat)
        bowl = self.__replace_zero(bowl)

        bat = bat.fillna(0)
        bowl = bowl.fillna(0)
        
        bat[self.TEXT_HS] = DataUtils.remove_asterisk_all(bat[self.TEXT_HS])
        bowl[self.TEXT_WICKET_HAUL] = self.__wicket_haul_col(bowl)
        
        if self.TEXT_SPAN in bat.columns:
            bat = DataUtils.drop_cols(bat, self.CONSISTENCY_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.CONSISTENCY_BOWL_DROP_COLS)
        else:
            bat = DataUtils.drop_cols(bat, self.FORM_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.FORM_BOWL_DROP_COLS)
        
        df = pd.merge(bat, bowl, on=self.TEXT_PLAYER)
        
        return df.reset_index(drop=True)

    def modify_total_consistency(self, df):
        if df.empty or df is None:
            raise RuntimeError(self.EX_MODIFY_TC.format(df))

        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)

        df = self.__replace_zero(df)
        df = self.__replace_na(df)

        df[self.TEXT_HIGH_SCORE] = DataUtils.remove_asterisk_all(df[self.TEXT_HIGH_SCORE])
        df[self.TEXT_WICKET_HAUL] = pd.to_numeric(df[self.TEXT_FOUR_WICKETS]) + pd.to_numeric(df[self.TEXT_FIVE_WICKETS])

        df = DataUtils.drop_cols(df, self.TOTAL_CONSISTENCY_DROP_COLS)

        return df.reset_index(drop=True)

    @staticmethod
    def __drop_na(df):
        return df.dropna()
    
    @staticmethod
    def __replace_zero(df):
        return df.replace("-", 0)

    @staticmethod
    def __replace_na(df):
        return df.replace("N/A", 0)

    @staticmethod
    def __wicket_haul_col(df):
        return pd.to_numeric(df['4']) + pd.to_numeric(df['5'])          
    
    def modify_ov_df(self, bat, bowl):
        if bat is None or bowl is None or bat.empty or bowl.empty:
            raise RuntimeError(self.EX_MODIFY_OV.format(bat, bowl))
        
        bat = bat.replace(r'^\s*$', 0, regex=True)
        bowl = bowl.replace(r'^\s*$', 0, regex=True)
        
        bat = bat.fillna(0)
        bowl = bowl.fillna(0)
        
        bat[self.TEXT_HS] = DataUtils.remove_asterisk_all(bat[self.TEXT_HS])
        
        if self.TEXT_VERSUS in bat.columns and self.TEXT_VERSUS in bowl.columns:
            bat = DataUtils.drop_cols(bat, self.OPPOSITION_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.OPPOSITION_BOWL_DROP_COLS)
        elif self.TEXT_GROUND in bat.columns and self.TEXT_GROUND in bowl.columns:
            bat = DataUtils.drop_cols(bat, self.VENUE_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.VENUE_BOWL_DROP_COLS)
            
        df = pd.merge(bat, bowl, on=self.TEXT_PLAYER)
        return df.reset_index(drop=True)

    CONSISTENCY_BAT_DROP_COLS = ['Span', 'Mat', 'NO', 'Runs', 'BF', '4s', '6s', 'Unknown']
    CONSISTENCY_BOWL_DROP_COLS = ['Span', 'Mat', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Econ', '4', '5', 'Ct', 'St', 'Unknown']
    FORM_BAT_DROP_COLS = ['Mat', 'NO', 'Runs', 'BF', '4s', '6s', 'Unknown']
    FORM_BOWL_DROP_COLS = ['Mat', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Econ', '4', '5', 'Ct', 'St', 'Unknown']
    VENUE_BAT_DROP_COLS = ['Ca', 'Ground', 'M', 'NO', 'Runs', 'St']
    VENUE_BOWL_DROP_COLS = ['Best', 'E/R', 'M', 'R', 'Ground', 'W']
    OPPOSITION_BAT_DROP_COLS = ['Ca', 'M', 'NO', 'Runs', 'St', 'Versus']
    OPPOSITION_BOWL_DROP_COLS = ['Best', 'E/R', 'M', 'R', 'Versus', 'W']
    TOTAL_CONSISTENCY_DROP_COLS = ['4 Wickets in Innings:', '5 Wickets in Innings:']

    TEXT_HS = 'HS'
    TEXT_WICKET_HAUL = 'WicketHaul'
    TEXT_SPAN = 'Span'
    TEXT_PLAYER = 'Player'
    TEXT_HIGH_SCORE = 'Highest Score:'
    TEXT_FOUR_WICKETS = '4 Wickets in Innings:'
    TEXT_FIVE_WICKETS = '5 Wickets in Innings:'
    TEXT_VERSUS = 'Versus'
    TEXT_GROUND = 'Ground'

    EX_MODIFY_OV = "Failed getting modify data for opposition or venue from ({0}) and ({1})"
    EX_MODIFY_CF = "Failed getting modify data for consistency or form from ({0}) and ({1})"
    EX_MODIFY_TC = "Failed getting modify data for total consistency from ({0})"
