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

    TEXT_TR = "tr"

    def create_consistency_bat(self, team, playing_eleven):
        alter_url = AlterUrls(ConstantUrl.CONSISTENCY_BAT_URL)
        return self.__consistency(alter_url, team, playing_eleven)

    def create_consistency_bowl(self, team, playing_eleven):
        alter_url = AlterUrls(ConstantUrl.CONSISTENCY_BOWL_URL)
        return self.__consistency(alter_url, team, playing_eleven)

    def __consistency(self, alter_url, team, playing_eleven):
        team_id = TeamsDAO.get_team_id(team)
        url = alter_url.team_url(team_id)

        soup = BSoup(url).get_soup()
        players = DataUtils.get_players(soup)
        table_rows = players[0].find_all(self.TEXT_TR)

        df = DataUtils.create_df(table_rows)
        return DataUtils.playing_eleven_df(df, playing_eleven)

    def create_form_bat(self, playing_eleven):
        soup = BSoup(ConstantUrl.FORM_BAT_URL).get_soup()
        return self.__form(soup, playing_eleven)

    def create_form_bowl(self, playing_eleven):
        soup = BSoup(ConstantUrl.FORM_BOWL_URL).get_soup()
        return self.__form(soup, playing_eleven)

    def __form(self, soup, playing_eleven):
        players = DataUtils.get_players(soup)
        if len(players) > 0:
            table_rows = players[0].find_all(self.TEXT_TR)
            df = DataUtils.create_df(table_rows)
            return DataUtils.playing_eleven_df(df, playing_eleven)
        else:
            return

    def create_recent_form(self, team, playing_eleven):
        team_id = TeamsDAO.get_team_id(team)
        alter_url = AlterUrls(ConstantUrl.RECENT_FORM_BAT_BOWL_URL)
        url = alter_url.team_url(team_id)
        return self.__prepare_data(url, playing_eleven)

    def __prepare_data(self, url, playing_eleven):
        soup = BSoup(url).get_soup()
        players = DataUtils.get_players(soup)

        if len(players) > 0:
            # Can add thread to run both simultaneously
            recent_form_bat = self.__process_rf(players, 0, playing_eleven)
            recent_form_bowl = self.__process_rf(players, 1, playing_eleven)
            return recent_form_bat, recent_form_bowl
        else:
            return

    def __process_rf(self, players, index, playing_eleven):
        table_rows = players[index].find_all(self.TEXT_TR)
        df = DataUtils.create_df(table_rows)
        return DataUtils.playing_eleven_df(df, playing_eleven)


class CreateOV:

    def create_total_consistency(self, playing_eleven):
        playing_eleven.sort()
        total_consistency_df = pd.DataFrame()
        players_id_list = PlayersDAO.get_player_id(playing_eleven)
        for player_id in players_id_list:
            if player_id is not None:
                consistency = self.__process_tc(player_id)
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

        total_consistency_df['Player'] = playing_eleven
        total_consistency_df['InnBowls'] = self.__bowl_inn_tc(total_consistency_df)

        return total_consistency_df.reset_index(drop=True)

    @staticmethod
    def __process_tc(player_id):
        alter_url = AlterUrls(ConstantUrl.TOTAL_CONSISTENCY_URL)
        player_url = alter_url.player_url(player_id)
        soup = BSoup(player_url).get_soup()
        return soup.find_all("table", attrs={"border": "0", "width": "270"})

    def create_opposition(self, opponent_team, playing_eleven):
        playing_eleven.sort()
        opposition_df_bat = pd.DataFrame()
        opposition_df_bowl = pd.DataFrame()
        players_id_list = PlayersDAO.get_player_id(playing_eleven)

        for player_id in players_id_list:
            if player_id is not None:
                versus = self.__find_table(player_id, ConstantUrl.OPPOSITION_URL)
            else:
                opposition_df_bat = self.__default_values_opposition(opposition_df_bat, opponent_team)
                opposition_df_bowl = self.__default_values_opposition(opposition_df_bowl, opponent_team)
                continue

            if len(versus) > 0:
                opposition_df_bat = opposition_df_bat.append(self.__process_opposition(versus, 0, opponent_team),
                                                             ignore_index=True)
                if len(versus) > 1:
                    opposition_df_bowl = opposition_df_bowl.append(self.__process_opposition(versus, 1, opponent_team),
                                                                   ignore_index=True)
                else:
                    opposition_df_bowl = self.__default_values_opposition(opposition_df_bowl, opponent_team)
            else:
                opposition_df_bat = self.__default_values_opposition(opposition_df_bat, opponent_team)
                opposition_df_bowl = self.__default_values_opposition(opposition_df_bowl, opponent_team)

        opposition_df_bat = opposition_df_bat.fillna(0)
        opposition_df_bowl = opposition_df_bowl.fillna(0)
        opposition_df_bat['Player'] = playing_eleven
        opposition_df_bowl['Player'] = playing_eleven

        opposition_df_bat['Zeros'] = self.__bat_zeros_opposition(players_id_list, opponent_team)
        opposition_df_bowl['InnsBowl'] = self.__bowl_inn(opposition_df_bowl)

        return opposition_df_bat, opposition_df_bowl

    def __process_opposition(self, versus, index, opponent_team):
        table_rows = versus[index].find_all("tr")
        df = self.__get_df(table_rows)
        return self.__check_versus(df, opponent_team)

    def create_venue(self, stadium, playing_eleven):
        playing_eleven.sort()
        venue_df_bat = pd.DataFrame()
        venue_df_bowl = pd.DataFrame()
        players_id_list = PlayersDAO.get_player_id(playing_eleven)

        for player_id in players_id_list:
            if player_id is not None:
                venue = self.__find_table(player_id, ConstantUrl.VENUE_URL)
            else:
                venue_df_bat = self.__default_values_venue(venue_df_bat, stadium)
                venue_df_bowl = self.__default_values_venue(venue_df_bowl, stadium)
                continue

            if len(venue) > 0:
                venue_df_bat = venue_df_bat.append(self.__process_venue(venue, 0, stadium), ignore_index=True)
                if len(venue) > 1:
                    venue_df_bowl = venue_df_bowl.append(self.__process_venue(venue, 1, stadium), ignore_index=True)
                else:
                    venue_df_bowl = self.__default_values_venue(venue_df_bowl, stadium)
            else:
                venue_df_bat = self.__default_values_venue(venue_df_bat, stadium)
                venue_df_bowl = self.__default_values_venue(venue_df_bowl, stadium)

        venue_df_bat = venue_df_bat.fillna(0)
        venue_df_bowl = venue_df_bowl.fillna(0)
        venue_df_bat['Player'] = playing_eleven
        venue_df_bowl['Player'] = playing_eleven

        venue_df_bat['Zeros'] = self.__bat_zeros_venue(players_id_list, stadium)
        venue_df_bat['BatSR'] = self.__bat_sr_venue(players_id_list, stadium)

        venue_df_bowl['InnsBowl'] = self.__bowl_inn(venue_df_bowl)

        return venue_df_bat, venue_df_bowl

    def __process_venue(self, venue, index, stadium):
        table_rows = venue[index].find_all("tr")
        df = self.__get_df(table_rows)
        return self.__check_ground(df, stadium)

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

        df_bat = df.loc[:, :15]
        df_bowl = df.loc[:, 16:]

        fielding_row = df.loc[df[16] == 'Fielding'].index.tolist()
        for row in fielding_row:
            row += 1
            df_bowl.loc[row] = 0

        wk_row = df.loc[df[16] == 'Wicket Keeping'].index.tolist()
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
        bowling_row = df.loc[df[16] == 'Bowling'].index.tolist()
        for row in bowling_row:
            if df.loc[row].str.contains('Bowling').any():
                df.columns = df.loc[row]
                return df

    TOTAL_CON_DROP_COLS = ['Batting', 'Not Outs:', 'Aggregate:', '4s:', '6s:', 'Balls Faced:', 'Opened Batting:',
                           'Top Scored in Innings:',
                           'Bowling', 'Balls:', 'Maidens:', 'Runs Conceded:', 'Wickets:', 'Best:', 'Economy Rate:',
                           'Fielding', 'Catches:', 'Most Catches in Match:', 0, 0.0, '0', '0.0',
                           'Wicket Keeping', 'Stumpings:', 'Most Dismissals in Match:',
                           'Captaincy', 'Matches/Won/Lost:', 'Tosses Won:']
