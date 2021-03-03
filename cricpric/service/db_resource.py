# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:15:03 2020

@author: user 2
"""
# import pyodbc as sql
import psycopg2 as psql
import threading


class DBResource:
    
    __singleton_lock = threading.Lock() 
    __con_instance = None
    # SERVER = 'localhost'
    # DATABASE = 'CricPric'
    # USERNAME = 'sa'
    # PASSWORD = 'sqlserver17'

    HOST = "ec2-54-211-77-238.compute-1.amazonaws.com"
    DATABASE = 'ddp61d32kckkl6'
    USERNAME = 'gretqxgonfiuce'
    PASSWORD = '72a79a5c33a1e3399a3f60df6e3aaf00714f76cb7826741ef9d5bbf23d47663d'
    
    @classmethod
    def get_instance(cls):
        if not cls.__con_instance:
            with cls.__singleton_lock:
                if not cls.__con_instance:
                    cls.__con_instance = cls()
                    
        return cls.__con_instance

    def get_connection(self):
        try:
            # return sql.connect(driver='{SQL Server}', server=self.SERVER, database=self.DATABASE, uid=self.USERNAME, pwd=self.PASSWORD)
            return psql.connect(host=self.HOST, database=self.DATABASE, user=self.USERNAME, password=self.PASSWORD)
        except BaseException as be:
            raise RuntimeError(self.EX_CON_FAILED.format(self.HOST, self.DATABASE, self.USERNAME), be)

    EX_CON_FAILED = "Failed to create connection using ({0}), ({1}) and ({2})"
