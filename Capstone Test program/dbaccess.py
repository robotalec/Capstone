from random import randint
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from mysql.connector import Error
import time
from random import seed
from random import randint
import Tkinter as Tk
import functools 
import operator
#import Read_test
import signal
import Tkinter



def showData(usr,pss,db):
    try:#using try catch to ensure access is only further done if conenction can be successfully done.
                connection = mysql.connector.connect(host='192.168.1.11',
                                                     database=db,
                                                     user=usr,
                                                     password=pss
                                                     #auth_plugin = 'mysql_native_password'
                                                     )
                print("Authenticating")

                if connection.is_connected():
                    print("connected")
                    
                    db_Info = connection.get_server_info()
                    print("Connected to MySQL Server version ", db_Info)
                    cursor = connection.cursor()
                    cursor.execute("select database();")
                    record = cursor.fetchone()
                    print("You're connected to database: ", record)

                    #INSERT INTO `verifydb`.`verify` (`UID`, `theKey`) VALUES ('222', '22');
                    
                    sql_select_query_5 = """select * from patient_info """
                    cursor.execute(sql_select_query_5)
                    hold3 = str(cursor.fetchall())
                    db = hold3
                    print(str(db))



                

    except Error as e:
        print("Error while connecting to MySQL", e)
        success = False
        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
