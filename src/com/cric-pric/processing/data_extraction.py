# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 16:11:50 2020

@author: user 2
"""

from util import DataUtils
import pandas as pd

class ModifyCFOV:
    
    CONSISTENCY_BAT_DROP_COLS = ['Span', 'Mat', 'NO', 'Runs', 'BF', '4s', '6s']
    CONSISTENCY_BOWL_DROP_COLS = ['Span', 'Mat', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Econ', '4', '5', 'Ct', 'St']
    FORM_BAT_DROP_COLS = ['Mat', 'NO', 'Runs', 'BF', '4s', '6s']
    FORM_BOWL_DROP_COLS = ['Mat', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Econ', '4', '5', 'Ct', 'St']
    VENUE_BAT_DROP_COLS =['Ca', 'Ground', 'M', 'NO', 'Runs', 'St']
    VENUE_BOWL_DROP_COLS = ['Best', 'E/R', 'M', 'R', 'Ground', 'W']
    OPPOSITION_BAT_DROP_COLS = ['Ca', 'M', 'NO', 'Runs', 'St', 'Versus']
    OPPOSITION_BOWL_DROP_COLS = ['Best', 'E/R', 'M', 'R', 'Versus', 'W']
    
    def modify_cf_df(self, bat, bowl): 
        if bat.empty or bowl.empty:
            return
        bat = self.__drop_na(bat)
        bowl = self.__drop_na(bowl)
        
        bat = self.__replace_zero(bat)
        bowl = self.__replace_zero(bowl)
        
        bat['HS'] = DataUtils.remove_asterik_all(bat['HS'])
        bowl['WicketHaul'] = self.__wicket_haul_col(bowl)
        
        if 'Span' in bat.columns:
            bat = DataUtils.drop_cols(bat, self.CONSISTENCY_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.CONSISTENCY_BOWL_DROP_COLS)
        else:
            bat = DataUtils.drop_cols(bat, self.FORM_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.FORM_BOWL_DROP_COLS)
        
        df = pd.merge(bat, bowl, on='Player')
        
        return df.reset_index(drop=True)
        
    def __drop_na(self, df):
        return df.dropna()
    
    def __replace_zero(self, df):
        return df.replace("-", 0)
        
    def __wicket_haul_col(self, df):
        return pd.to_numeric(df['4']) + pd.to_numeric(df['5'])          
    
    def modify_ov_df(self, bat, bowl):
        if bat.empty or bowl.empty:
            return
        
        bat = bat.replace(r'^\s*$', 0, regex=True)
        bowl = bowl.replace(r'^\s*$', 0, regex=True)
        
        bat = bat.fillna(0)
        bowl = bowl.fillna(0)
        
        bat['HS'] = DataUtils.remove_asterik_all(bat['HS'])
        
        if 'Versus' in bat.columns and 'Versus' in bowl.columns:
            bat = DataUtils.drop_cols(bat, self.OPPOSITION_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.OPPOSITION_BOWL_DROP_COLS)
        elif 'Ground' in bat.columns and 'Ground' in bowl.columns:
            bat = DataUtils.drop_cols(bat, self.VENUE_BAT_DROP_COLS)
            bowl = DataUtils.drop_cols(bowl, self.VENUE_BOWL_DROP_COLS)
            
        df = pd.merge(bat, bowl, on='Player')
        
        return df.reset_index(drop=True)