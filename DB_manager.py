#!/usr/bin/python

import mysql.connector # connection from python to mySQL
from mysql.connector import errorcode # import error messages 
from datetime import datetime # allows date/time of entries to be recordered

##===============================================

class DatabaseUtility:
    # Initilize Constructor 
    def __init__(self, database, tableName):
        self.db = database
        self.tableName = tableName
        
        p = 'spooky74' 
        # User has admin status, localhost is the user's computer 
        self.cnx = mysql.connector.connect(user = 'root',
									password = p,
									host = 'localhost')
        # create cursor 
        self.cursor = self.cnx.cursor()
        
        # create class methods
        self.ConnectToDatabase()
        self.CreateTable()
		
    def ConnectToDatabase(self):
        # connect to database passed to class when run. If that database 
        # does not exist, catch error and force the creation of that database 
        try:
            self.cnx.database = self.db
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.CreateDatabase()
                self.cnx.database = self.db
            # if that fails for some reason, throw an error message
            else:
                print(err.msg)

    def CreateDatabase(self):
        try:
            # run function to execute command, create database with db name from user
            self.RunCommand("CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8';" %self.db)
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

    def CreateTable(self):
        # ID == data point number, date and time are self explanatory,
        # voltage is the input voltage from ECG sensor 
        # primary key organizes values based on ID
        # InnoDB == engine for setting up table 
        cmd = (" CREATE TABLE IF NOT EXISTS " + self.tableName + " ("
			" `ID` int(5) NOT NULL AUTO_INCREMENT,"
			" `date` date NOT NULL,"
			" `time` time NOT NULL,"
			" `voltage` float(5) NOT NULL,"
			" PRIMARY KEY (`ID`)"
			") ENGINE=InnoDB;")
        self.RunCommand(cmd)

    def GetTable(self):
        self.CreateTable()
        return self.RunCommand("SELECT * FROM %s;" % self.tableName)

    def GetColumns(self):
        return self.RunCommand("SHOW COLUMNS FROM %s;" % self.tableName)

    def RunCommand(self, cmd):
        print ("RUNNING COMMAND: " + cmd)
        try:
            self.cursor.execute(cmd)
        except mysql.connector.Error as err:
            print ('ERROR MESSAGE: ' + str(err.msg))
            print ('WITH ' + cmd)
        try:
            msg = self.cursor.fetchall()
        except:
            #Returns none if fetchall produces no output 
            msg = self.cursor.fetchone()
        return msg

    def AddEntryToTable(self, voltage):
        date1 = datetime.now().strftime("%y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")

        cmd = " INSERT INTO " + self.tableName + " (date, time, voltage)"
        cmd += " VALUES ('%s', '%s', '%.2f' );" % (date1, time, voltage)
        self.RunCommand(cmd)
        
    # clean up code 
    def __del__(self):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()
 
##===============================================
##===============================================

# if running the script as the main, this code will execute 
if __name__ == '__main__':
	db = 'myFirstDB2'
	tableName = 'test8'

	dbu = DatabaseUtility(db, tableName)

	# dbu.AddEntryToTable ('testing')
	# dbu.AddEntryToTable ('testing2')
	# print (dbu.GetColumns())
	# print (dbu.GetTable())
	
