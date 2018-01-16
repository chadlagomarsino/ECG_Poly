#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 11:28:47 2018

@author: ChadTheMonster
"""
import sqlite3 
import manage_SQL

#connect to SQLite3 Database
conn = sqlite3.connect('ECG.db')
#define cursor
c = conn.cursor()
    
manage_SQL.graph_data()
    



