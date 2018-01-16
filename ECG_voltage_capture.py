#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 19:02:56 2018

@author: ChadTheMonster
"""

import serial 
import sqlite3 
import manage_SQL

# open serial port at 9600 baud to pair with Ardiuno board
dev = '/dev/cu.usbmodem1421'
#connect to SQLite3 Database
conn = sqlite3.connect('ECG.db')
#define cursor
c = conn.cursor()

with serial.Serial(dev, 9600, timeout = 1) as ser: 
    
    while True: 
        # read 1 bytes from serial connection (one voltage value)
        # remove tags
        voltage = ser.readline().decode().strip('\r\n')
        #if connection is broken, the recording will stop 
        if voltage:
            print(voltage)
            manage_SQL.create_table()
            manage_SQL.data_entry(voltage)

manage_SQL.db_close()
        


    
        
            