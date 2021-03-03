import os
from os import path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from cricpric.dao.dao import PlayersDAO
from cricpric.modeling.predict_performance import PlayerPerformance
from cricpric.processing.create_modify import DerivedAttrs


class CricPricService:

    def process(self, host_team, away_team, venue, host_playing, away_playing):
        derived_attr = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
        derived_attr.process()

        if path.exists(derived_attr.FILE_CONSISTENCY) and path.exists(derived_attr.FILE_FORM) \
                and path.exists(derived_attr.FILE_OPPOSITION) and path.exists(derived_attr.FILE_VENUE):
            con = pd.read_csv(derived_attr.FILE_CONSISTENCY)
            if con is None or con.empty:
                raise ValueError(self.EX_CON_DATA.format(con, derived_attr.FILE_CONSISTENCY))

            tot_con = pd.read_csv(derived_attr.FILE_TOTAL_CONSISTENCY)
            if tot_con is None or tot_con.empty:
                raise ValueError(self.EX_TOTAL_CON_DATA.format(tot_con, derived_attr.FILE_TOTAL_CONSISTENCY))

            form = pd.read_csv(derived_attr.FILE_FORM)
            if form is None or form.empty:
                raise ValueError(self.EX_FORM_DATA.format(form, derived_attr.FILE_FORM))

            r_form = pd.read_csv(derived_attr.FILE_RECENT_FORM)
            if r_form is None or r_form.empty:
                raise ValueError(self.EX_RECENT_FORM_DATA.format(r_form, derived_attr.FILE_RECENT_FORM))

            opp = pd.read_csv(derived_attr.FILE_OPPOSITION)
            if opp is None or opp.empty:
                raise ValueError(self.EX_OPP_DATA.format((opp, derived_attr.FILE_OPPOSITION)))

            ven = pd.read_csv(derived_attr.FILE_VENUE)
            if ven is None or ven.empty:
                raise ValueError(self.EX_VEN_DATA.format(ven, derived_attr.FILE_VENUE))

            player_performance = PlayerPerformance(con, tot_con, form, r_form, opp, ven)
            dataset = player_performance.calc_da()

            if path.exists(self.FILE_DATASET):
                os.remove(self.FILE_DATASET)
            dataset.to_csv(self.FILE_DATASET)

            dataset = self.__modify_data_set(dataset)
            dataset_wo_rf = dataset.drop('RecentForm', axis=1)

            result = player_performance.predict(dataset_wo_rf)

            batsmen = dataset_wo_rf[dataset_wo_rf['BatBowl'] == 1]
            bowlers = dataset_wo_rf[dataset_wo_rf['BatBowl'] == 0]

            # runs_wicket_data = dataset.drop('BatBowl', axis=1)
            batsmen.drop('BatBowl', axis=1, inplace=True)
            bowlers.drop('BatBowl', axis=1, inplace=True)
            runs_predict = player_performance.predict_runs(batsmen)
            wickets_predict = player_performance.predict_wickets(bowlers)

            all_predictions = None
            if (result and result is not None) and (runs_predict and runs_predict is not None) \
                    and (wickets_predict and wickets_predict is not None):
                all_predictions = pd.merge(pd.merge(result, runs_predict, on='Players', how='left'), wickets_predict,
                                           on='Players', how='left')
            batting_plot, bowling_plot = self.__plot_graphs(dataset, batsmen, bowlers)

            self.__train_data_collection(dataset_wo_rf, self.FILE_TRAIN_DATA)
            self.__train_data_collection(dataset, self.FILE_TRAIN_DATA_FORM)
            self.__train_data_collection(batsmen, self.FILE_TRAIN_DATA_RUNS)
            self.__train_data_collection(bowlers, self.FILE_TRAIN_DATA_WICKETS)
            return all_predictions, dataset, batting_plot, bowling_plot
        else:
            return self.EX_INVALID_DETAILS

    def venue_stats(self, host_team, away_team, venue, host_playing, away_playing):
        derived_attr = DerivedAttrs(host_team, away_team, venue, host_playing, away_playing)
        derived_attr.venue()

        if path.exists(derived_attr.FILE_VENUE):
            ven = pd.read_csv(derived_attr.FILE_VENUE)
            if ven is None or ven.empty:
                raise ValueError(self.EX_VEN_DATA.format(ven, derived_attr.FILE_VENUE))

            return ven

    @staticmethod
    def __plot_graphs(dataset, batsmen, bowlers):
        bowlers = bowlers.reset_index()
        batsmen = batsmen.reset_index()

        bat_labels = batsmen['index']
        bat_opp = batsmen['Opposition']
        bat_ven = batsmen['Venue']
        recent_bat = dataset[dataset['BatBowl'] == 1]
        bat_rf = recent_bat['RecentForm']

        bowl_labels = bowlers['index']
        bowl_opp = bowlers['Opposition']
        bowl_ven = bowlers['Venue']
        recent_bowl = dataset[dataset['BatBowl'] == 0]
        bowl_rf = recent_bowl['RecentForm']

        x = np.arange(len(bat_labels))  # the label locations
        x1 = np.arange(len(bowl_labels))  # the label locations
        y = np.arange(0, 6, 0.5)
        width = 0.15  # the width of the bars

        fig1, ax1 = plt.subplots()
        ax1.bar(x - width, bat_opp, width, label='Opposition')
        ax1.bar(x, bat_ven, width, label='Venue')
        ax1.bar(x + width, bat_rf, width, label='Recent Form')

        fig2, ax2 = plt.subplots()
        ax2.bar(x1 - width, bowl_opp, width, label='Opposition')
        ax2.bar(x1, bowl_ven, width, label='Venue')
        ax2.bar(x1 + width, bowl_rf, width, label='Recent Form')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax1.set_ylabel('Scores')
        ax1.set_title('Batting Scores')
        ax1.set_xticks(x)
        ax1.set_xticklabels(bat_labels, rotation=90)
        ax1.set_yticks(y)
        ax1.set_yticklabels(y)
        ax1.axhline(3.0, color='gray', lw=1)
        ax1.legend()

        ax2.set_ylabel('Scores')
        ax2.set_title('Bowling Scores')
        ax2.set_xticks(x1)
        ax2.set_xticklabels(bowl_labels, rotation=90)
        ax2.set_yticks(y)
        ax2.set_yticklabels(y)
        ax2.axhline(3.0, color='gray', lw=1)
        ax2.legend()

        fig1.tight_layout()
        fig2.tight_layout()

        return fig1, fig2

    def __modify_data_set(self, train_data):
        batsmen = train_data.loc[:, 'ConsistencyBat':'VenueBat']
        bowler = train_data.loc[:, 'ConsistencyBowl':'VenueBowl']

        bowler.columns = self.HEADER_COLS
        batsmen.columns = self.HEADER_COLS

        batsmen['BatBowl'] = 1
        bowler['BatBowl'] = 0

        players = batsmen.index.tolist()
        players = list(dict.fromkeys(players))
        for player in players:
            player_role = PlayersDAO.get_player_role(player)
            if player_role == 'batsman' and bowler['BatBowl'][player].all() == 0:
                bowler.drop(player, inplace=True)
            elif player_role == 'bowler' and batsmen['BatBowl'][player].all() == 1:
                batsmen.drop(player, inplace=True)

        data = batsmen.append(bowler)
        return data

    @staticmethod
    def __train_data_collection(data, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'a', newline='') as f:
                data.to_csv(f, mode='a', header=False)
        else:
            data.to_csv(file_name)

    EX_CON_DATA = "Invalid consistency data ({0}) from ({1})"
    EX_TOTAL_CON_DATA = "Invalid total consistency data ({0}) from ({1})"
    EX_FORM_DATA = "Invalid form data ({0}) from ({1})"
    EX_RECENT_FORM_DATA = "Invalid recent form data ({0}) from ({1})"
    EX_OPP_DATA = "Invalid opposition data ({0}) from ({1})"
    EX_VEN_DATA = "Invalid venue data ({0}) from ({1})"

    EX_INVALID_DETAILS = "Invalid details selected"

    FILE_TRAIN_DATA = "config\\train_data.csv"
    FILE_TRAIN_DATA_FORM = "config\\train_data_r_form.csv"
    FILE_TRAIN_DATA_RUNS = "config\\train_data_runs.csv"
    FILE_TRAIN_DATA_WICKETS = "config\\train_data_wickets.csv"
    FILE_DATASET = "config\\dataset.csv"

    HEADER_COLS = ['Consistency', 'TotalConsistency', 'Form', 'RecentForm', 'Opposition', 'Venue']
