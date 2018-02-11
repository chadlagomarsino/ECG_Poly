#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 9 17:10:13 2018

@author: ChadTheMonster
"""

import multiprocessing 
import DB_manager
import time 
import serial 
import mysql.connector # connection from python to mySQL
from datetime import datetime # allows date/time of entries to be recordered
import live_graphECG

def Producer(): 
    #print(threading.currentThread().getName(), 'STARTING')
    # open serial port at 9600 baud to pair with Ardiuno board
    dev = '/dev/cu.usbmodem1421'
    try:
        ser = serial.Serial(dev, 9600, timeout = 1)
    except: 
        print('ARDUINO CONNECTION NOT FOUND')
        #print(threading.currentThread().getName(), 'EXITING')
        return
    # while connected to arudino
    while True:
        try:
            # if ser.in_waiting() > 0:
            # read 1 byte from serial connection (one voltage value)
            # remove tags
            voltage = ser.readline().decode().strip('\r\n').strip()
            try:
                voltage = float(voltage)
            except:
                print("BLANK INPUT")
                continue
            #print(type(voltage))
            #print(voltage) # uncomment for testing
            # add voltage table
            try: 
                dbu.AddEntryToTable(voltage)
            except:
                print('DATABASE ERROR')
                #print(threading.currentThread().getName(), 'EXITING')
                return
        except:
            print('ARDUINO CONNECTION LOST')
            #print(threading.currentThread().getName(), 'EXITING')
            return
            

def Consumer():
    #print(threading.currentThread().getName(), 'STARTING')
    try:
        p = 'spooky74'
        cnx2 = mysql.connector.connect(user = 'root',
									password = p,
									host = 'localhost')
        cursor2 = cnx2.cursor()
        cnx2.database = dbu.db
    except:
        print("Connection 2 ERROR")
    for x in range(50):
            cmd = "SELECT voltage FROM test"
            print ("RUNNING COMMAND2: " + cmd)
            try:
                cursor2.execute(cmd)
            except mysql.connector.Error as err:
                print ('ERROR MESSAGE: ' + str(err.msg))
                print ('WITH ' + cmd)
            try:
                # clear lists
                voltages = []
                for row in cursor2.fetchall():
                    # rebuild value lists 
                    voltages.append(row[0])
                    live_graphECG.buildgraph(voltages)
            except: 
                print("Unable to Fetch Data")
            
    #print(threading.currentThread().getName(), 'EXITING')
    return

if __name__ == '__main__':
    database = 'ECG2'
    tableName = 'test' 
    dbu = DB_manager.DatabaseUtility(database, tableName) # create DB object 
    p = multiprocessing.Process(target = Producer, name = 'Producer')
    p.start()
    time.sleep(5)
    c = multiprocessing.Process(target = Consumer, name = 'Consumer')
    c.start()
        
        