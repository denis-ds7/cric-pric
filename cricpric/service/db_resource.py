# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:15:03 2020

@author: user 2
"""
import pyodbc as sql
import threading


class DBResource:
    
    __singleton_lock = threading.Lock() 
    __con_instance = None
    SERVER = 'localhost'
    DATABASE = 'CricPric'
    USERNAME = 'sa'
    PASSWORD = 'sqlserver17'
    
    @classmethod
    def get_instance(cls):
        if not cls.__con_instance:
            with cls.__singleton_lock:
                if not cls.__con_instance:
                    cls.__con_instance = cls()
                    
        return cls.__con_instance

    def get_connection(self):
        try:
            return sql.connect(driver='{SQL Server}', server=self.SERVER, database=self.DATABASE, uid=self.USERNAME, pwd=self.PASSWORD)
        except BaseException as be:
            raise RuntimeError(self.EX_CON_FAILED.format(self.SERVER, self.DATABASE, self.USERNAME), be)

    EX_CON_FAILED = "Failed to create connection using ({0}), ({1}) and ({2})"
