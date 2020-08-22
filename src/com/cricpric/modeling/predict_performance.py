# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 18:16:30 2020

@author: user 2
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from com.cricpric.dao.dao import ConsistencyDAO, FormDAO, OppositionDAO, VenueDAO

class PlayerPerformance:
    
    NO_OF_INN = "No. of Innings"
    BAT_AVG = "Batting Average"
    BAT_SR = "Batting Strike Rate"
    CENTURIES = "Centuries"
    FIFTIES = "Fifties"
    ZEROS = "Zeros"
    HS = "Highest Score"
    OVERS = "Overs"
    BOWL_AVG = "Bowling Average"
    BOWL_SR = "Bowling Strike Rate"
    FF = "FF"
    
    def __init__(self, consistency, form, opposition, venue):
        self.consistency = consistency
        self.form = form
        self.opposition = opposition
        self.venue = venue
    
    def predict(self):
        calc_derived_attrs = self.calc_da()

    def calc_da(self):
        #Caluclate the Derived Attributes for each Player
        consistency_bat = {}
        consistency_bowl = {}
        form_bat = {}
        form_bowl = {}
        opposition_bat = {}
        opposition_bowl = {}
        venue_bat = {}
        venue_bowl = {}
        
        for i in self.consistency.index:
            consistency_bat.update({self.consistency['Player'][i] : \
                                    0.4262*(ConsistencyDAO.get_con_range(self.consistency['BatAvg'][i], self.BAT_AVG)) \
                                   + 0.2566*(ConsistencyDAO.get_con_range(self.consistency['No. of Inn (Bat)'][i], self.NO_OF_INN)) \
                                   + 0.1510*(ConsistencyDAO.get_con_range(self.consistency['BatSR'][i], self.BAT_SR)) \
                                   + 0.0787*(ConsistencyDAO.get_con_range(self.consistency['Centuries'][i], self.CENTURIES)) \
                                   + 0.0556*(ConsistencyDAO.get_con_range(self.consistency['Fifties'][i], self.FIFTIES)) \
                                   - 0.0328*(ConsistencyDAO.get_con_range(self.consistency['Zeros'][i], self.ZEROS))})
            
            consistency_bowl.update({self.consistency['Player'][i] : \
                                     0.4174*(ConsistencyDAO.get_con_range(self.consistency['Overs'][i], self.OVERS)) \
                                    + 0.2634*(ConsistencyDAO.get_con_range(self.consistency['No. of Inn (Bowl)'][i], self.NO_OF_INN))\
                                    + 0.1602*(ConsistencyDAO.get_con_range(self.consistency['BowlSR'][i], self.BOWL_SR)) \
                                    + 0.0975*(ConsistencyDAO.get_con_range(self.consistency['BowlAvg'][i], self.BOWL_AVG)) \
                                    + 0.0615*(ConsistencyDAO.get_con_range(self.consistency['WicketHaul'][i], self.FF))})
            
        for i in self.form.index:
            form_bat.update({self.form['Player'][i] : \
                            0.4262*(FormDAO.get_form_range(self.form['BatAvg'][i], self.BAT_AVG)) \
                            + 0.2566*(FormDAO.get_form_range(self.form['No. of Inn (Bat)'][i], self.NO_OF_INN)) \
                            + 0.1510*(FormDAO.get_form_range(self.form['BatSR'][i], self.BAT_SR)) \
                            + 0.0787*(FormDAO.get_form_range(self.form['Centuries'][i], self.CENTURIES)) \
                            + 0.0556*(FormDAO.get_form_range(self.form['Fifties'][i], self.FIFTIES)) \
                            - 0.0328*(FormDAO.get_form_range(self.form['Zeros'][i], self.ZEROS))})
            
            form_bowl.update({self.form['Player'][i] : \
                            0.3269*(FormDAO.get_form_range(self.form['Overs'][i], self.OVERS)) \
                            + 0.2846*(FormDAO.get_form_range(self.form['No. of Inn (Bowl)'][i], self.NO_OF_INN)) \
                            + 0.1877*(FormDAO.get_form_range(self.form['BowlSR'][i], self.BOWL_SR)) \
                            + 0.1210*(FormDAO.get_form_range(self.form['BowlAvg'][i], self.BOWL_AVG)) \
                            + 0.0798*(FormDAO.get_form_range(self.form['WicketHaul'][i], self.FF))})
    
        for i in self.opposition.index:
            opposition_bat.update({self.opposition['Player'][i] : \
                            0.4262*(OppositionDAO.get_opp_range(self.opposition['BatAvg'][i], self.BAT_AVG)) \
                            + 0.2566*(OppositionDAO.get_opp_range(self.opposition['No. of Inn (Bat)'][i], self.NO_OF_INN)) \
                            + 0.1510*(OppositionDAO.get_opp_range(self.opposition['BatSR'][i], self.BAT_SR)) \
                            + 0.0787*(OppositionDAO.get_opp_range(self.opposition['Centuries'][i], self.CENTURIES)) \
                            + 0.0556*(OppositionDAO.get_opp_range(self.opposition['Fifties'][i], self.FIFTIES)) \
                            - 0.0328*(OppositionDAO.get_opp_range(self.opposition['Zeros'][i], self.ZEROS))})
            
            opposition_bowl.update({self.opposition['Player'][i] : \
                            0.3177*(OppositionDAO.get_opp_range(self.opposition['Overs'][i], self.OVERS)) \
                            + 0.3177*(OppositionDAO.get_opp_range(self.opposition['No. of Inn (Bowl)'][i], self.NO_OF_INN)) \
                            + 0.1933*(OppositionDAO.get_opp_range(self.opposition['BowlSR'][i], self.BOWL_SR)) \
                            + 0.1465*(OppositionDAO.get_opp_range(self.opposition['BowlAvg'][i], self.BOWL_AVG)) \
                            + 0.0943*(OppositionDAO.get_opp_range(self.opposition['WicketHaul'][i], self.FF))})
            
        for i in self.venue.index:
            venue_bat.update({self.venue['Player'][i] : \
                             0.4262*(VenueDAO.get_ven_range(self.venue['BatAvg'][i], self.BAT_AVG)) \
                             + 0.2566*(VenueDAO.get_ven_range(self.venue['No. of Inn (Bat)'][i], self.NO_OF_INN)) \
                             + 0.1510*(VenueDAO.get_ven_range(self.venue['BatSR'][i], self.BAT_SR)) \
                             + 0.0787*(VenueDAO.get_ven_range(self.venue['Centuries'][i], self.CENTURIES)) \
                             + 0.0556*(VenueDAO.get_ven_range(self.venue['Fifties'][i], self.FIFTIES)) \
                             + 0.0328*(VenueDAO.get_ven_range(self.venue['HS'][i], self.HS))})
            
            venue_bowl.update({self.venue['Player'][i] : \
                              0.3018*(VenueDAO.get_ven_range(self.venue['Overs'][i], self.OVERS)) \
                              + 0.2783*(VenueDAO.get_ven_range(self.venue['No. of Inn (Bowl)'][i], self.NO_OF_INN)) \
                              + 0.1836*(VenueDAO.get_ven_range(self.venue['BowlSR'][i], self.BOWL_SR)) \
                              + 0.1391*(VenueDAO.get_ven_range(self.venue['BowlAvg'][i], self.BOWL_AVG)) \
                              + 0.0972*(VenueDAO.get_ven_range(self.venue['WicketHaul'][i], self.FF))})
                
        data_set = [consistency_bat, form_bat, opposition_bat, venue_bat, consistency_bowl, form_bowl, opposition_bowl, venue_bowl]
        return pd.DataFrame.from_dict(data=data_set).T
            