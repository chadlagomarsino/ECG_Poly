#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 20:30:20 2018

@author: ChadTheMonster
"""

import sqlite3
import time
import datetime
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib import style 
import numpy
from drawnow import drawnow 
style.use('fivethirtyeight')

#connect to SQLite3 Database
conn = sqlite3.connect('ECG.db')
#define cursor
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS output(datestamp TEXT, unix REAL, value REAL)')
    
def data_entry(value):
    unix = time.clock()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    value = value
    c.execute('INSERT INTO output (datestamp, unix, value) VALUES(?, ?, ?)', (date, unix, value))
    conn.commit()
    
def read_from_db():
    c.execute('SELECT unix, value FROM output')
    c.fetchone()
    
def del_data():
    c.execute('SELECT * FROM output')
    [print(row) for row in c.fetchall()]
    c.execute('DELETE FROM output')
    conn.commit()

def graph_data():
    
    plt.ion() #Tell matplotlib you want to enter live data
    
    while True: 
        c.execute('SELECT unix, value FROM output') #select values from database
        time = []
        values = []
        
        for row in c.fetchall(): 
            time.append(row[0]) 
            values.append(row[1])
           # if (count > 50):
                
        def makeFig():
            plt.ylim(0,5) #set y limit and prevent rescaling 
            plt.grid(True)
            plt.ylabel('Voltage (V)')
            plt.plot(time,values, 'r-', markersize = 6)
    
        drawnow(makeFig)
        plt.pause(.000001) #allow system to redraw itself 
    
'''
    #Sentdex dynamic graph 
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
      
    def animate(i):
        c.execute('SELECT unix, value FROM output')
        time = []
        values = []
        for row in c.fetchall():
            time.append(row[0]) 
            values.append(row[1])
        ax1.clear()
        ax1.plot(time, values, '-')
            
    ani = animation.FuncAnimation(fig, animate, interval = 1000)
    plt.show() 

'''
    
'''
    #static graph 
    c.execute('SELECT unix, value FROM output')
    time = []
    values = []
    for row in c.fetchall():
        time.append(row[0]) 
        values.append(row[1])
    #static graph 
    plt.plot(time, values, '-')
    plt.show()
'''        

def db_close():
    c.close()
    conn.close()

'''
#Test script
if __name__ == '__main__':
    create_table()
    for value in range(0,10):
        data_entry(value)
    db_close()
'''