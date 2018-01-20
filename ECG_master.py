#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 19:11:01 2018

@author: ChadTheMonster

Notes: This master script will be activated by a Kivy app ON/OFF button
for the host GUI. It runs two threads on the same process. 
The first thread collects voltage data from an arduino sensor and 
uploads voltage data to a SQLite3 table. The second thread accesses 
this table and then produces a real-time graph.

It relies on the custom module manage_SQL, which includes SQL table
functionality

The code begins with the __main__ script at the bottom, and then assigns
objects, calling the run methods to execute the threads.  
"""

import threading 
import time
import logging
import random
import serial 
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from drawnow import drawnow
import manage_SQL #custom module

# logging for DEBUGGING
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

# Thread for script receiving voltage data from the arudino
# and updating SQL table with voltage data
class ProducerThread(threading.Thread):
    # initalize class
    def __init__(self, group=None,target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).init()
        # target and name refer to the variables within this class
        self.target = target
        self.name = name 
        
    # run producer script 
    def run(self):
        # open serial port at 9600 baud to pair with Ardiuno board
        dev = '/dev/cu.usbmodem1421'
        # connect to SQLite3 Database
        conn = sqlite3.connect('ECG.db')
        # define cursor
        c = conn.cursor()
        
        with serial.Serial(dev, 9600, timeout = 1) as ser:
            # run continously 
            while True:
                # when there is data passed by arduino 
                if ser.in_waiting() > 0:
                    # read 1 byte from serial connection (one voltage value)
                    # remove tags
                    voltage = ser.readline().decode().strip('\r\n') 
                    # print(voltage), uncomment for testing
                    # debugging message to check connection 
                    logging.debug('Voltage:' + str(voltage))
                    # create table if not already existing
                    manage_SQL.create_table()
                    # insert timestamp, voltage, absolute time into table
                    manage_SQL.data_entry(voltage)
                # once connection is broken or no data is being passed
                else:
                    #close database
                    manage_SQL.db_close()
                    return
                
# Thread for recieving voltage data from SQL table and producing
# a real-time, scrolling graph of voltage output 
class ConsumerThread(threading.Thread):
    # initalize class
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        # target and name refer to the variables within this class
        self.target = target
        self.name = name
        return
    
    #run consumer script 
    def run(self):
        #connect to SQLite3 Database
        conn = sqlite3.connect('ECG.db')
        #define cursor
        c = conn.cursor()
        #Tell matplotlib you want to enter live data
        plt.ion()
        
        while True: 
            #select all time, voltage values from database
            c.execute('SELECT unix, value FROM output')
            # clear arrays 
            time = []
            values = []
        
            for row in c.fetchall():
                # rebuild time, value arrays 
                time.append(row[0]) 
                values.append(row[1])
                
                def makeFig():
                    plt.ylim(0,5) #set y limit and prevent rescaling 
                    plt.grid(True)
                    plt.ylabel('Voltage (V)')
                    plt.plot(time,values, 'r-', markersize = 6)
    
            drawnow(makeFig)
            plt.pause(.000001) #allow system to redraw itself
        
        

# script begins running here
if __name__ == '__main__':
    
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')
    
    # five second delay before data capture begins
    time.sleep(5)
    # begin collecting data from arduino 
    p.start()
    # three second delay before reading voltage from table
    time.sleep(3)
    # begin reading table and plotting voltage data 
    c.start()
    
