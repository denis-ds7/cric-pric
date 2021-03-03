# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 13:21:37 2020

@author: user 2
"""
from threading import Thread

from cricpric.preparation.data_collection import CreateCF, CreateOV
from cricpric.processing.data_extraction import ModifyCFOV
from os import path
import os
import pandas as pd


class DerivedAttrs:
    
    def __init__(self, host_team, away_team, stadium, host_playing, away_playing):
        self.host_team = host_team
        self.away_team = away_team
        self.stadium = stadium
        self.host_playing = host_playing
        self.away_playing = away_playing

    def process(self):
        t1 = Thread(target=self.consistency)
        t2 = Thread(target=self.form)
        t3 = Thread(target=self.recent_form)
        t4 = Thread(target=self.total_consistency)
        t5 = Thread(target=self.opposition)
        t6 = Thread(target=self.venue)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()

        # with thread.ThreadPoolExecutor() as executor:
        #     executor.submit(self.consistency, create_cf, modify)
        #     executor.submit(self.form, create_cf, modify)
        #     executor.submit(self.recent_form, create_cf, modify)
        #     executor.submit(self.total_consistency, create_ov, modify)
        #     executor.submit(self.opposition, create_ov, modify)
        #     executor.submit(self.venue, create_ov, modify)

    # def create_da(self):
    #     create_cf = CreateCF()
    #     modify = ModifyCFOV()
    #     create_ov = CreateOV()
    #     self.consistency(create_cf, modify)
    #     self.form(create_cf, modify)
    #     self.recent_form(create_cf, modify)
    #     self.total_consistency(create_ov, modify)
    #     self.opposition(create_ov, modify)
    #     self.venue(create_ov, modify)

    def consistency(self):
        create_cf = CreateCF()
        modify = ModifyCFOV()
        # with thread.ThreadPoolExecutor as executor:
        #     f1 = executor.submit(create_cf.create_consistency_bat, self.host_team, self.host_playing)
        #     f2 = executor.submit(create_cf.create_consistency_bowl, self.host_team, self.host_playing)
        #     f3 = executor.submit(create_cf.create_consistency_bat, self.away_team, self.away_playing)
        #     f4 = executor.submit(create_cf.create_consistency_bowl, self.away_team, self.away_playing)
        #
        #     host_con_bat = f1.result()
        #     host_con_bowl = f2.result()
        #     host_consistency = modify.modify_cf_df(host_con_bat, host_con_bowl)
        #
        #     away_con_bat = f3.result()
        #     away_con_bowl = f4.result()
        #     away_consistency = modify.modify_cf_df(away_con_bat, away_con_bowl)

        host_con_bat = create_cf.create_consistency_bat(self.host_team, self.host_playing)
        away_con_bat = create_cf.create_consistency_bat(self.away_team, self.away_playing)
        host_con_bowl = create_cf.create_consistency_bowl(self.host_team, self.host_playing)
        away_con_bowl = create_cf.create_consistency_bowl(self.away_team, self.away_playing)

        host_consistency = modify.modify_cf_df(host_con_bat, host_con_bowl)
        away_consistency = modify.modify_cf_df(away_con_bat, away_con_bowl)

        if host_consistency is None or away_consistency is None:
            raise RuntimeError(self.EX_CON_DATA.format(host_consistency, away_consistency))
        consistency = pd.concat([host_consistency, away_consistency])

        if path.exists(self.FILE_CONSISTENCY):
            os.remove(self.FILE_CONSISTENCY)
        consistency.to_csv(self.FILE_CONSISTENCY, header=self.CON_FORM_COLS, index=False)

    def form(self):
        create_cf = CreateCF()
        modify = ModifyCFOV()
        # with thread.ThreadPoolExecutor as executor:
        #     f1 = executor.submit(create_cf.create_form_bat, self.host_playing)
        #     f2 = executor.submit(create_cf.create_form_bowl, self.host_playing)
        #     f3 = executor.submit(create_cf.create_form_bat, self.away_playing)
        #     f4 = executor.submit(create_cf.create_form_bowl, self.away_playing)
        #
        #     host_form_bat = f1.result()
        #     host_form_bowl = f2.result()
        #     host_form = modify.modify_cf_df(host_form_bat, host_form_bowl)
        #
        #     away_form_bat = f3.result()
        #     away_form_bowl = f4.result()
        #     away_form = modify.modify_cf_df(away_form_bat, away_form_bowl)

        host_form_bat = create_cf.create_form_bat(self.host_playing)
        away_form_bat = create_cf.create_form_bat(self.away_playing)
        host_form_bowl = create_cf.create_form_bowl(self.host_playing)
        away_form_bowl = create_cf.create_form_bowl(self.away_playing)

        host_form = modify.modify_cf_df(host_form_bat, host_form_bowl)
        away_form = modify.modify_cf_df(away_form_bat, away_form_bowl)

        if host_form is None or away_form is None:
            raise RuntimeError(self.EX_FORM_DATA.format(host_form, away_form))
        form = pd.concat([host_form, away_form])

        if path.exists(self.FILE_FORM):
            os.remove(self.FILE_FORM)
        form.to_csv(self.FILE_FORM, header=self.CON_FORM_COLS, index=False)

    def recent_form(self):
        create_cf = CreateCF()
        modify = ModifyCFOV()
        host_recent_form_bat, host_recent_form_bowl = create_cf.create_recent_form(self.host_team, self.host_playing)
        away_recent_form_bat, away_recent_form_bowl = create_cf.create_recent_form(self.away_team, self.away_playing)

        host_recent_form = modify.modify_cf_df(host_recent_form_bat, host_recent_form_bowl)
        away_recent_form = modify.modify_cf_df(away_recent_form_bat, away_recent_form_bowl)

        if host_recent_form is None or away_recent_form is None:
            raise RuntimeError(self.EX_RECENT_FORM.format(host_recent_form, away_recent_form))
        recent_form = pd.concat([host_recent_form, away_recent_form])

        if path.exists(self.FILE_RECENT_FORM):
            os.remove(self.FILE_RECENT_FORM)
        recent_form.to_csv(self.FILE_RECENT_FORM, header=self.CON_FORM_COLS, index=False)

    def total_consistency(self):
        modify = ModifyCFOV()
        create_ov = CreateOV()

        host_total_consistency = create_ov.create_total_consistency(self.host_playing)
        away_total_consistency = create_ov.create_total_consistency(self.away_playing)

        host_total_consistency = modify.modify_total_consistency(host_total_consistency)
        away_total_consistency = modify.modify_total_consistency(away_total_consistency)

        if host_total_consistency is None or away_total_consistency is None:
            raise RuntimeError(self.EX_TOT_CON_DATA.format(host_total_consistency, away_total_consistency))
        total_consistency = pd.concat([host_total_consistency, away_total_consistency])

        if path.exists(self.FILE_TOTAL_CONSISTENCY):
            os.remove(self.FILE_TOTAL_CONSISTENCY)
        total_consistency.to_csv(self.FILE_TOTAL_CONSISTENCY, header=self.TOT_CON_COLS, index=False)

    def opposition(self):
        modify = ModifyCFOV()
        create_ov = CreateOV()

        host_opp_bat, host_opp_bowl = create_ov.create_opposition(self.away_team, self.host_playing)
        away_opp_bat, away_opp_bowl = create_ov.create_opposition(self.host_team, self.away_playing)

        host_opposition = modify.modify_ov_df(host_opp_bat, host_opp_bowl)
        away_opposition = modify.modify_ov_df(away_opp_bat, away_opp_bowl)

        if host_opposition is None or away_opposition is None:
            raise RuntimeError(self.EX_OPP_DATA.format(host_opposition, away_opposition))
        opposition = pd.concat([host_opposition, away_opposition])

        if path.exists(self.FILE_OPPOSITION):
            os.remove(self.FILE_OPPOSITION)
        opposition.to_csv(self.FILE_OPPOSITION, header=self.OPP_COLS, index=False)

    def venue(self):
        modify = ModifyCFOV()
        create_ov = CreateOV()

        host_ven_bat, host_ven_bowl = create_ov.create_venue(self.stadium, self.host_playing)
        away_ven_bat, away_ven_bowl = create_ov.create_venue(self.stadium, self.away_playing)

        host_venue = modify.modify_ov_df(host_ven_bat, host_ven_bowl)
        away_venue = modify.modify_ov_df(away_ven_bat, away_ven_bowl)

        if host_venue is None or away_venue is None:
            raise RuntimeError(self.EX_VEN_DATA.format(host_venue, away_venue))
        venue = pd.concat([host_venue, away_venue])

        if path.exists(self.FILE_VENUE):
            os.remove(self.FILE_VENUE)
        venue.to_csv(self.FILE_VENUE, header=self.VEN_COLS, index=False)

    # current_form = self.__merge_form(form, recent_form)
    @staticmethod
    def __merge_form(form, recent_form):
        if form is None or form.empty:
            return
        if recent_form is None or recent_form.empty:
            return

        rf = pd.DataFrame()

        players_form = form['Player']
        form_without_players = form.drop('Player', axis='columns')

        players_recent_form = recent_form['Player']
        rf_without_players = recent_form.drop('Player', axis='columns')

        form = form_without_players.astype(float)
        recent_form = rf_without_players.astype(float)

        form['Player'] = players_form
        recent_form['Player'] = players_recent_form

        form_and_recent = pd.concat((form, recent_form))
        by_player = form_and_recent.groupby(form_and_recent['Player'])

        rf['Zeros'] = pd.to_numeric(form['0']) + pd.to_numeric(recent_form['0'])
        rf['Centuries'] = pd.to_numeric(form['100']) + pd.to_numeric(recent_form['100'])
        rf['Fifties'] = pd.to_numeric(form['50']) + pd.to_numeric(recent_form['50'])
        rf['BatAvg'] = by_player['Ave_x'].mean()
        # form['BatAvg'] = form[pd.to_numeric(form['Ave_x']), pd.to_numeric(recent_form['Ave_x'])].mean(axis=1)
        rf['HS'] = by_player['HS'].max()
        # form['HS'] = form[pd.to_numeric(form['HS']), pd.to_numeric(recent_form['HS'])].max(axis=1)
        rf['No. of Inn (Bat)'] = pd.to_numeric(form['Inns_x']) + pd.to_numeric(recent_form['Inns_x'])
        rf['Player'] = players_form
        rf['BatSR'] = by_player['SR_x'].mean()
        # form['BatSR'] = form[pd.to_numeric(form['SR_x']), pd.to_numeric(recent_form['SR_x'])].mean(axis=1)
        rf['BowlAvg'] = by_player['Ave_y'].mean()
        # form['BowlAvg'] = form[pd.to_numeric(form['Ave_y']), pd.to_numeric(recent_form['Ave_y'])].mean(axis=1)
        rf['No. of Inn (Bowl)'] = pd.to_numeric(form['Inns_y']) + pd.to_numeric(recent_form['Inns_y'])
        rf['Overs'] = pd.to_numeric(form['Overs']) + pd.to_numeric(recent_form['Overs'])
        rf['BowlSR'] = by_player['SR_y'].mean()
        # form['BowlSR'] = form[pd.to_numeric(form['SR_y']), pd.to_numeric(recent_form['SR_y'])].mean(axis=1)
        rf['WicketHaul'] = pd.to_numeric(form['WicketHaul']) + pd.to_numeric(recent_form['WicketHaul'])

        return rf

    CON_FORM_COLS = ['Zeros', 'Centuries', 'Fifties', 'BatAvg', 'HS', 'No. of Inn (Bat)', 'Player', 'BatSR',
                     'BowlAvg', 'No. of Inn (Bowl)', 'Overs', 'BowlSR', 'WicketHaul']

    OPP_COLS = ['Centuries', 'Fifties', 'BatAvg', 'HS', 'No. of Inn (Bat)', 'BatSR', 'Player',
                'Zeros', 'WicketHaul', 'BowlAvg', 'Overs', 'BowlSR', 'No. of Inn (Bowl)']

    VEN_COLS = ['Centuries', 'Fifties', 'BatAvg', 'HS', 'No. of Inn (Bat)', 'Player', 'Zeros',
                'BatSR', 'WicketHaul', 'BowlAvg', 'Overs', 'BowlSR', 'No. of Inn (Bowl)']

    TOT_CON_COLS = ['No. of Inn (Bat)', 'HS', 'BatAvg', 'Fifties', 'Centuries', 'Zeros', 'BatSR', 'Overs',
                    'BowlAvg', 'BowlSR', 'Player', 'No. of Inn (Bowl)', 'WicketHaul']

    FILE_CONSISTENCY = "data\\consistency.csv"
    FILE_FORM = "data\\form.csv"
    FILE_RECENT_FORM = "data\\recent_form.csv"
    FILE_OPPOSITION = "data\\opposition.csv"
    FILE_VENUE = "data\\venue.csv"
    FILE_TOTAL_CONSISTENCY = "data\\total_consistency.csv"

    EX_CON_DATA = "Failed getting consistency data from ({0}) and ({1})"
    EX_FORM_DATA = "Failed getting form data from ({0}) and ({1})"
    EX_RECENT_FORM = "Failed getting recent form data from ({0}) and ({1})"
    EX_TOT_CON_DATA = "Failed getting total consistency data from ({0}) and ({1})"
    EX_OPP_DATA = "Failed getting total opposition data from ({0}) and ({1})"
    EX_VEN_DATA = "Failed getting total venue data from ({0}) and ({1})"
