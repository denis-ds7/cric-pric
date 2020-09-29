# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 20:49:58 2020

@author: user 2
"""

import pandas as pd
from fuzzywuzzy import fuzz


class DataUtils:

    @staticmethod
    def __get_cols(table_rows):
        for tr in table_rows:
            th = tr.find_all('th')
            data_cols = [tx.text.strip() for tx in th]
            return data_cols

    @staticmethod
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
        return soup.find_all(cls.TEXT_TABLE, attrs={cls.TEXT_CLASS: cls.TEXT_ENGINE})

    @classmethod
    def remove_asterisk_all(cls, series):
        hs_list = []
        for value in series:
            value = cls.remove_asterisk(str(value))
            hs_list.append(value)
        return hs_list

    @classmethod
    def remove_asterisk(cls, value):
        if '*' in value:
            return value.replace(cls.ASTERISK, cls.EMPTY)
        elif '-' in value:
            return value.replace(cls.HYPHEN, cls.ZERO)
        else:
            return value

    @classmethod
    def drop_cols(cls, df, cols):
        for col in cols:
            if col in df.columns:
                df = df.drop(col, axis=1)
        return df

    @classmethod
    def playing_eleven_df(cls, df, playing_eleven):
        playing_df = pd.DataFrame()
        for player in playing_eleven:
            x = 0
            player_ci = cls.EMPTY
            for i in df.index:
                if df[cls.TEXT_PLAYER][i] is not None:
                    player_ci = cls.__check_fuzz(player, df[cls.TEXT_PLAYER].tolist())
                    if player_ci == df[cls.TEXT_PLAYER][i]:
                        playing_df = playing_df.append(df.loc[i])
                        x = 1
                        break

            if x == 1:
                continue

            if not playing_df.empty and cls.TEXT_PLAYER in playing_df and player_ci not in playing_df[cls.TEXT_PLAYER]:
                playing_df = playing_df.append(pd.Series(0, index=playing_df.columns), ignore_index=True)
            else:
                playing_df = playing_df.append({cls.TEXT_UNKNOWN: cls.TEXT_UNKNOWN}, ignore_index=True).fillna(0)

        playing_df[cls.TEXT_PLAYER] = playing_eleven
        return playing_df.reset_index(drop=True)

    @staticmethod
    def __check_fuzz(player, player_list):
        ci_unknown_players = ["SL Malinga", "GC Viljoen", "KD Karthik", "CV Chakravarthy"]
        for player_name in player_list:
            if player_name is not None:
                partial_ratio = fuzz.partial_ratio(player, player_name)
                if partial_ratio == 100:
                    return player_name
                else:
                    p = player.split()
                    pn = player_name.split()
                    if len(p) > 1 and len(pn) > 1:
                        if p[1] == pn[1]:
                            if player[0] == player_name[0]:
                                return player_name
                            elif player_name in ci_unknown_players:
                                return player_name

        return player

    @classmethod
    def check_range(cls, rs, num):
        if not rs or rs is None:
            raise ValueError(cls.EX_INVALID_RS.format(rs))

        for row in rs:
            if num == 0:
                return 0
            # num >= row[0] and num <= row[1]:
            elif row[0] <= num <= row[1]:
                return row[2]
            # row[3] > 0 and num >= row[3]:
            elif 0 < row[3] <= num:
                return row[2]

    EX_INVALID_RS = "Invalid result set ({0})"

    TEXT_PLAYER = "Player"
    TEXT_UNKNOWN = "Unknown"
    TEXT_TABLE = "table"
    TEXT_CLASS = "class"
    TEXT_ENGINE = "engineTable"
    ASTERISK = "*"
    EMPTY = ""
    HYPHEN = "-"
    ZERO = "0"
