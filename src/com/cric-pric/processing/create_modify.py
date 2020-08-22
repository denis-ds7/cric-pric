# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 13:21:37 2020

@author: user 2
"""

from data_collection import CreateCF, CreateOV
from data_extraction import ModifyCFOV
from os import path
import os
import pandas as pd

class DerivedAttrs():
    
    CON_FORM_COLS = ['Zeros', 'Centuries', 'Fifties', 'BatAvg', 'HS', 'No. of Inn (Bat)', 'Player', 'BatSR', \
                     'BowlAvg', 'No. of Inn (Bowl)', 'Overs', 'BowlSR', 'WicketHaul']
        
    OPP_COLS = ['Centuries', 'Fifties', 'BatAvg', 'HS', 'No. of Inn (Bat)', 'BatSR', 'Player Name', \
                    'Zeros', 'WicketHaul', 'BowlAvg', 'Overs', 'BowlSR', 'No. of Inn (Bowl)']
        
    VEN_COLS = ['Centuries', 'Fifties', 'BatAvg', 'HS', 'No. of Inn (Bat)', 'Player Name', 'Zeros', \
                'BatSR', 'WicketHaul', 'BowlAvg', 'Overs', 'BowlSR', 'No. of Inn (Bowl)']
    
    FILE_CONSISTENCY = "consistency.csv"
    FILE_FORM = "form.csv"
    FILE_OPPOSITION = "opposition.csv"
    FILE_VENUE = "venue.csv"
    
    def __init__(self, host_team, away_team, venue, host_playing, away_playing):
        self.host_team = host_team
        self.away_team = away_team
        self.venue = venue
        self.host_playing = host_playing
        self.away_playing = away_playing
        
    def consistency_form(self, bat, bowl):
        
        # Team1 batting consistency and form
        create_cf = CreateCF(self.host_team, bat, self.host_playing)
        host_con_bat = create_cf.create_consistency()
        host_form_bat = create_cf.create_form()
        
        # Team2 batting consistency and form
        create_cf = CreateCF(self.away_team, bat, self.away_playing)
        away_con_bat = create_cf.create_consistency()
        away_form_bat = create_cf.create_form()
        
        # Team1 bowling consistency and form
        create_cf = CreateCF(self.host_team, bowl, self.host_playing)
        host_con_bowl = create_cf.create_consistency()
        host_form_bowl = create_cf.create_form()
        
        # Team2 batting consistency and form
        create_cf = CreateCF(self.away_team, bowl, self.away_playing)
        away_con_bowl = create_cf.create_consistency()
        away_form_bowl = create_cf.create_form()
        
        #Modify df
        modify = ModifyCFOV()
        host_consistency = modify.modify_cf_df(host_con_bat, host_con_bowl)
        away_consistency = modify.modify_cf_df(away_con_bat, away_con_bowl)
        
        host_form = modify.modify_cf_df(host_form_bat, host_form_bowl)
        away_form = modify.modify_cf_df(away_form_bat, away_form_bowl)
        
        if host_consistency is None or away_consistency is None:
            return
        consistency = pd.concat([host_consistency, away_consistency])
        
        if host_form is None or away_form is None:
            return
        form = pd.concat([host_form, away_form])        
        
        if path.exists(self.FILE_CONSISTENCY):
            os.remove(self.FILE_CONSISTENCY)
            
        if path.exists(self.FILE_FORM):
            os.remove(self.FILE_FORM)
        
        consistency.to_csv(self.FILE_CONSISTENCY, header=self.CON_FORM_COLS, index=False)
        form.to_csv(self.FILE_FORM, header=self.CON_FORM_COLS, index=False)
        
    def opposition_venue(self, bat, bowl):
        
        #Team1 batting opposition and venue
        create_ov = CreateOV(self.host_playing, bat)
        host_opp_bat = create_ov.create_opposition(self.away_team)
        host_ven_bat = create_ov.create_venue(self.venue)
        
        #Team2 batting opposition and venue
        create_ov = CreateOV(self.away_playing, bat)
        away_opp_bat = create_ov.create_opposition(self.host_team)
        away_ven_bat = create_ov.create_venue(self.venue)
        
        #Team1 bowling opposition and venue
        create_ov = CreateOV(self.host_playing, bowl)
        host_opp_bowl = create_ov.create_opposition(self.away_team)
        host_ven_bowl = create_ov.create_venue(self.venue)
        
        #Team2 bowling opposition and venue
        create_ov = CreateOV(self.away_playing, bowl) 
        away_opp_bowl = create_ov.create_opposition(self.host_team)
        away_ven_bowl = create_ov.create_venue(self.venue)
        
        #Modify df
        modify = ModifyCFOV()
        host_opposition = modify.modify_ov_df(host_opp_bat, host_opp_bowl)
        away_opposition = modify.modify_ov_df(away_opp_bat, away_opp_bowl)
        
        host_venue = modify.modify_ov_df(host_ven_bat, host_ven_bowl)
        away_venue = modify.modify_ov_df(away_ven_bat, away_ven_bowl)
        
        if host_opposition is None or away_opposition is None:
            return
        opposition = pd.concat([host_opposition, away_opposition])
        
        if host_venue is None or away_venue is None:
            return
        venue = pd.concat([host_venue, away_venue])
        
        if path.exists(self.FILE_OPPOSITION):
            os.remove(self.FILE_OPPOSITION)
            
        if path.exists(self.FILE_VENUE):
            os.remove(self.FILE_VENUE)
        
        opposition.to_csv(self.FILE_OPPOSITION, header=self.OPP_COLS, index=False)
        venue.to_csv(self.FILE_VENUE, header=self.VEN_COLS, index=False)
    
    
    