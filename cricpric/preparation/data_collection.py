# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 19:24:09 2020

@author: user 2
"""
import math

import pandas as pd
from cricpric.service.data_url import AlterUrls, ConstantUrl, BSoup
from cricpric.util.util import DataUtils
from cricpric.dao.dao import TeamsDAO, PlayersDAO


class CreateCF:

    TEXT_BAT = "bat"
    TEXT_BOWL = "bowl"
    TEXT_TR = "tr"

    def __init__(self, team_name, bat_bowl, players_list):
        self.team_name = team_name
        self.bat_bowl = bat_bowl
        self.players_list = players_list

    def create_consistency(self):
        alter_url = ''
        if self.bat_bowl == self.TEXT_BAT:
            alter_url = AlterUrls(ConstantUrl.CONSISTENCY_BAT_URL)
        elif self.bat_bowl == self.TEXT_BOWL:
            alter_url = AlterUrls(ConstantUrl.CONSISTENCY_BOWL_URL)

        team_id = TeamsDAO.get_team_id(self.team_name)
        url = alter_url.team_url(team_id)

        soup = BSoup(url).get_soup()
        players = DataUtils.get_players(soup)
        table_rows = players[0].find_all(self.TEXT_TR)

        df = DataUtils.create_df(table_rows)
        return DataUtils.playing_eleven_df(df, self.players_list)

    def create_form(self):
        soup = None
        if self.bat_bowl == self.TEXT_BAT:
            soup = BSoup(ConstantUrl.FORM_BAT_URL).get_soup()
        elif self.bat_bowl == self.TEXT_BOWL:
            soup = BSoup(ConstantUrl.FORM_BOWL_URL).get_soup()

        players = DataUtils.get_players(soup)
        if len(players) > 0:
            table_rows = players[0].find_all(self.TEXT_TR)
            df = DataUtils.create_df(table_rows)
            return DataUtils.playing_eleven_df(df, self.players_list)
        else:
            return

    # def create_form(self):
    #     team_id = TeamsDAO.get_team_id(self.team_name)
    #     alter_url = AlterUrls(ConstantUrl.FORM_BAT_BOWL_URL)
    #     url = alter_url.team_url(team_id)
    #     return self.__prepare_data(url)

    def create_recent_form(self):
        team_id = TeamsDAO.get_team_id(self.team_name)
        alter_url = AlterUrls(ConstantUrl.RECENT_FORM_BAT_BOWL_URL)
        url = alter_url.team_url(team_id)
        return self.__prepare_data(url)

    def __prepare_data(self, url):
        soup = BSoup(url).get_soup()
        players = DataUtils.get_players(soup)

        if len(players) > 0:
            if self.bat_bowl == self.TEXT_BAT:
                table_rows = players[0].find_all(self.TEXT_TR)
                df = DataUtils.create_df(table_rows)
                return DataUtils.playing_eleven_df(df, self.players_list)
            elif self.bat_bowl == self.TEXT_BOWL:
                table_rows = players[1].find_all(self.TEXT_TR)
                df = DataUtils.create_df(table_rows)
                return DataUtils.playing_eleven_df(df, self.players_list)
        else:
            return


class CreateOVC:
    TOTAL_CON_DROP_COLS = ['Batting', 'Not Outs:', 'Aggregate:', '4s:', '6s:', 'Balls Faced:', 'Opened Batting:',
                           'Bowling', 'Balls:', 'Maidens:', 'Runs Conceded:', 'Wickets:', 'Best:', 'Economy Rate:',
                           'Fielding', 'Catches:', 'Most Catches in Match:', 0, 0.0, '0', '0.0',
                           'Wicket Keeping', 'Stumpings:', 'Most Dismissals in Match:',
                           'Captaincy', 'Matches/Won/Lost:', 'Tosses Won:']

    def __init__(self, players_list, bat_bowl):
        self.players_list = players_list
        self.bat_bowl = bat_bowl

    def create_total_consistency(self):
        total_consistency_df = pd.DataFrame()
        players_id_list = PlayersDAO.get_player_id(self.players_list)

        for player_id in players_id_list:
            if player_id is not None:
                alter_url = AlterUrls(ConstantUrl.TOTAL_CONSISTENCY_URL)
                player_url = alter_url.player_url(player_id)
                soup = BSoup(player_url).get_soup()
                consistency = soup.find_all("table", attrs={"border": "0", "width": "270"})
            else:
                total_consistency_df = self.__default_values_total_consistency(total_consistency_df)
                continue

            if len(consistency) > 0:
                table_rows = consistency[0].find_all("tr")
                df = DataUtils.create_df(table_rows)
                total_consistency_df = total_consistency_df.append(df.transpose())
            else:
                total_consistency_df = self.__default_values_total_consistency(total_consistency_df)

        total_consistency_df = self.__modify_tc(total_consistency_df.reset_index(drop=True))

        total_consistency_df['Player'] = self.players_list
        total_consistency_df['InnBowls'] = self.__bowl_inn_tc(total_consistency_df)

        return total_consistency_df.reset_index(drop=True)

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
                    opposition_df = opposition_df.append(self.__check_versus(bat_o_df, opponent_team),
                                                         ignore_index=True)
                elif self.bat_bowl == "bowl":
                    if len(versus) > 1:
                        table_rows = versus[1].find_all("tr")
                        bowl_o_df = self.__get_df(table_rows)
                        opposition_df = opposition_df.append(self.__check_versus(bowl_o_df, opponent_team),
                                                             ignore_index=True)
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

    @staticmethod
    def __default_values_venue(venue_df, stadium_venue):
        if not venue_df.empty:
            venue_df = venue_df.append(pd.Series(0, index=venue_df.columns), ignore_index=True)
            return venue_df
        else:
            venue_df = venue_df.append({'Ground': stadium_venue}, ignore_index=True).fillna(0)
            return venue_df

    @staticmethod
    def __default_values_opposition(opposition_df, opponent_team):
        if not opposition_df.empty:
            opposition_df = opposition_df.append(pd.Series(0, index=opposition_df.columns), ignore_index=True)
            return opposition_df
        else:
            opposition_df = opposition_df.append({'Versus': opponent_team}, ignore_index=True).fillna(0)
            return opposition_df

    @staticmethod
    def __default_values_total_consistency(total_consistency_df):
        if not total_consistency_df.empty:
            total_consistency_df = total_consistency_df.append(pd.Series(0, index=total_consistency_df.columns),
                                                               ignore_index=True)
            return total_consistency_df
        else:
            total_consistency_df = total_consistency_df.append({'Player': "Unknown"}, ignore_index=True).fillna(0)
            return total_consistency_df

    @staticmethod
    def __find_table(player_id, url):
        alter_url = AlterUrls(url)
        player_url = alter_url.player_url(player_id)
        soup = BSoup(player_url).get_soup()
        return soup.find_all("table", attrs={"class": "TableLined"})

    @staticmethod
    def __get_df(table_rows):
        df = DataUtils.create_df(table_rows)
        df.columns = df.loc[0]
        df = df.drop(df.index[0])
        return df

    @staticmethod
    def __check_versus(df, opponent_team):
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

    @staticmethod
    def __bowl_inn(df):
        ser = []
        for i in df.index:
            # pd.to_numeric(df['O'][i]) > 0 and pd.to_numeric(df['O'][i]) <= 3:
            if 0 < pd.to_numeric(df['O'][i]) <= 3:
                ser.append(1)
            else:
                bowl_inns = math.floor(pd.to_numeric(df['O'][i]) / 3)
                if pd.to_numeric(df['O'][i]) % 3 != 0 and bowl_inns > 0:
                    bowl_inns += 1
                ser.append(bowl_inns)
        return ser

    @staticmethod
    def __bowl_inn_tc(df):
        ser = []
        for i in df.index:
            if df['Overs:'][i]:
                # pd.to_numeric(df['O'][i]) > 0 and pd.to_numeric(df['O'][i]) <= 3:
                if 0 < pd.to_numeric(df['Overs:'][i]) <= 3:
                    ser.append(1)
                else:
                    bowl_inns = round(pd.to_numeric(df['Overs:'][i]) / 3)
                    if pd.to_numeric(df['Overs:'][i]) % 3 != 0 and bowl_inns > 0:
                        bowl_inns += 1
                    ser.append(bowl_inns)
            else:
                ser.append(0)
        return ser

    @staticmethod
    def __check_ground(df, stadium_venue):
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
                cols = ['0', 'Date', 'Versus', 'Ground', 'D/N', 'How Dismissed', 'Runs', 'B/F', 'S/R', '9', 'Aggr',
                        'Avg', 'S/R Pro']
                df.columns = cols
                df = df.drop(['0', '9'], axis=1)
                df = df.reset_index(drop=True)
                for i in df.index:
                    if stadium_venue in df['Ground'][i]:
                        if 'DNB' in df['Runs'][i]:
                            continue
                        total_runs += pd.to_numeric(DataUtils.remove_asterisk(df['Runs'][i]))
                        total_bf += pd.to_numeric(DataUtils.remove_asterisk(df['B/F'][i]))

                if total_runs == 0 or total_bf == 0:
                    ser.append(0)
                else:
                    bat_sr = total_runs / total_bf * 100
                    ser.append(round(bat_sr, 2))
            else:
                ser.append(0)

        return ser

    def __modify_tc(self, df):
        df = df.replace(r'^\s*$', 0, regex=True)
        df = df.fillna(0)

        df_bat = df.loc[:, :14]
        df_bowl = df.loc[:, 15:]

        fielding_row = df.loc[df[15] == 'Fielding'].index.tolist()
        for row in fielding_row:
            row += 1
            df_bowl.loc[row] = 0

        wk_row = df.loc[df[15] == 'Wicket Keeping'].index.tolist()
        for row in wk_row:
            row += 1
            df_bowl.loc[row] = 0

        df = pd.concat([df_bat, df_bowl], axis=1, ignore_index=True)
        df = self.__set_columns(df)

        df = DataUtils.drop_cols(df, self.TOTAL_CON_DROP_COLS)
        # df = df.drop(df.columns[[7, 13, 14, 15, 16, 17]], axis=1)
        # df = df.drop_duplicates(keep=False)
        # df = df[~df['Innings:'].str.contains("Innings:")]
        duplicates = df['Innings:'].str.contains("Innings:")
        for index, value in duplicates.items():
            if value is True:
                df.drop(index, inplace=True)

        return df

    @staticmethod
    def __set_columns(df):
        bowling_row = df.loc[df[15] == 'Bowling'].index.tolist()
        for row in bowling_row:
            if df.loc[row].str.contains('Bowling').any():
                df.columns = df.loc[row]
                return df
