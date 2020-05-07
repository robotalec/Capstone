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

import dbaccess

from mfrc522 import SimpleMFRC522

uid = ''#string for id of the card
currentkey = ''
reader = SimpleMFRC522()
valid = False
continue_reading = True
Tries = 0
def Key_Manager():#random key maker
    key = [0,0,0,0,0,0]#storage array

    for _ in range(6):
        value = randint(0x00,0xff)#generates 10 numbers from the possible scale of hex to use
        #print(hex(value)) #hex() will allow the value from theis be formatted correctly to be inserted into the key
        key[_] = hex(value)
        
    key = map(str, key)#convert hex list to string list
    print (key)
    newkey = ''.join(key)#string list to string
    
    return(newkey)

def ValidfyTrue():
    global valid
    valid = True
   # print("setting True")

def ValidfyFalse():
    global valid
    Valid = False



def sql_formatting(key):
    key = key.replace('(', '')
    key = key.replace('u', '')
    key = key.replace("'", '')
    key = key.replace(')', '')
    key = key.replace(',', '')
    key = key.replace(' ', '')
    
    return(key)


def program():
    
    global uid
    uid = ''
    global valid
    try:#using try catch to ensure access is only further done if conenction can be successfully done.
        connection = mysql.connector.connect(host='192.168.1.11',
                                             database='verifydb',
                                             user='project',
                                             password='Password123'
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
            valid = False
            while valid == False:
                print("Hold a tag near the reader")
                global currentkey
                currentkey = ''
                
                uid, currentkey = reader.read()
                
                sql_select_query = """select distinct theKey from verify where UID = '""" + str(uid) + """'"""#select statement for sql
                cursor.execute(sql_select_query)
                record1 = cursor.fetchone()

                
                ValidfyFalse()
                #print(record1)
                verifykey = str(record1)
                verifykey.encode("utf-8")
                #print("converint to string")
                #print (uid)
                #print (str(currentkey) + "end")
                #print (sql_formatting(Key_Manager()))
                currentkey = sql_formatting(currentkey)
                verifykey = (sql_formatting(verifykey))
                #print (str(verifykey) + "end")
                #print (str(currentkey) + "end")
                
                
                if(str(currentkey) == str(verifykey)):#checks if key and the verify key are the same
                    ValidfyTrue()
                    theNewKey = ''#formats the key storing to a variable that can be written to the card
                    theNewKey = sql_formatting(Key_Manager())
                    print("updating")
                    #print(Card_Manager())
                    sql_select_query2 = """update verify Set theKey = '""" + str(theNewKey) + """' where UID = '""" + str(uid) + """'""" #updates verify database
                    reader.write(theNewKey)
                    print("success"  )
                    cursor.execute(sql_select_query2)
                    connection.commit()#commits the change
                    #print(valid)
                    
                    
                    sql_select_query_3 = """select username from userinfo where UID = '""" + str(uid) + """'"""
                    cursor.execute(sql_select_query_3)
                    hold1 = str(cursor.fetchone())
                    userName = sql_formatting(hold1)
                    print(str(userName))
                    sql_select_query_4 = """select password from userinfo where UID = '""" + str(uid) + """'"""
                    cursor.execute(sql_select_query_4)
                    hold2 = str(cursor.fetchone())
                    passw = sql_formatting(hold2)
                    print(str(passw))
                    sql_select_query_5 = """select database_used from userinfo where UID = '""" + str(uid) + """'"""
                    cursor.execute(sql_select_query_5)
                    hold3 = str(cursor.fetchone())
                    db = sql_formatting(hold3)
                    print(str(db))
                    
                    dbaccess.showData(userName, passw, db)
                else:
                    print("Error the verifing keies do not match please trie again.")
                    print("\n")
                    global Tries
                    print("you have " + str(Tries) + " out of 3 tries remaing before card lockout")
                    Tries = Tries + 1
                    ValidfyFalse()
                    time.sleep(3)
                global Tries    
                if(Tries == 3):
                    print("error out of tries beginning card lockout...")
                    
                    lockoutKey = ''
                    lockoutKey = sql_formatting(Key_Manager())
                    
                    sql_select_query2 = """update verify Set theKey = '""" + str(lockoutKey) + """' where UID = '""" + str(uid) + """'""" #updates verify database

                    cursor.execute(sql_select_query2)
                    connection.commit()#commits the change
                    ValidfyTrue()
                    print("Lockout Succeful")

            print(record)

        else:
            print("error unable to connect")


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
      

            
            
#top = Tkinter.Tk()

#top.minsize(200, 150)              

#def runProgram():
    #global Tries
    #end = False
    #while end == False:
        #program()
        #if(valid == True):#tells you if card worked
            #print("Card Verified")
            #end = True
        #else:#if card does not work
            #print("Card Denied")
            #if(Tries < 3):# allows card to try three times
                #Tries = Tries + 1
                #print("You have" + str(Tries) +" out of 3 tries remaining")
            #else:#if it failed three times
                #print("Error out of tries card locking...")
                #print("Card locking successful")
                #end = True
                

#def addUser():
    #print("adding User...")




#B1 = Tkinter.Button(top, text = "Read Card", command = runProgram)

#B2 = Tkinter.Button(top, text = "Add New User Card", command = addUser)


#B1.pack()
#B2.pack()
#top.mainloop()
#GPIO.cleanup()





























