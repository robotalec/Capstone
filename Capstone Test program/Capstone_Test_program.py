import mysql.connector
from mysql.connector import Error
import time
from random import seed
from random import randint
import Tkinter as Tk
import functools 
import operator
#import Read_test
import RPi.GPIO as GPIO
import MFRC522
import signal
import Tkinter

id = "10.3.3.3"#string for id of the card
currentkey = ""

valid = False
continue_reading = True
Tries = 0
def Key_Manager():#random key maker
    key = [0,0,0,0,0,0]#storage array

    for _ in range(6):
        value = randint(0x00,0xff)#generates 10 numbers from the possible scale of hex to use
        #print(hex(value)) #hex() will allow the value from theis be formatted correctly to be inserted into the key
        key[_] = hex(value)

    return(key)

def ValidfyTrue():
    global valid
    valid = True
   # print("setting True")

def ValidfyFalse():
    global valid
    Valid = False
    

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read." 
    continue_reading = False
    GPIO.cleanup()

def readCard():
    global continue_reading

    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        
            # This is the default key for authentication
            
            ## Select the scanned tag
            #MIFAREReader.MFRC522_SelectTag(uid)

            ## Authenticate
            #status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            #print "\n"

            ## Check if authenticated
            #if status == MIFAREReader.MI_OK:

                #print "It now looks like this:"
                ## Check to see if it was written
                #MIFAREReader.MFRC522_Read(8)
                #print "\n"


                ## Stop
                #MIFAREReader.MFRC522_StopCrypto1()

                ## Make sure to stop reading for cards
                #continue_reading = False
            #else:
                #print "Authentication error"


def program():
    

    try:#using try catch to ensure access is only further done if conenction can be successfully done.
        connection = mysql.connector.connect(host='192.168.1.8',
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
            
            
            global continue_reading

            signal.signal(signal.SIGINT, end_read)

            # Create an object of the class MFRC522
            MIFAREReader = MFRC522.MFRC522()

            # This loop keeps checking for chips. If one is near it will get the UID and authenticate
            while continue_reading:
                
                # Scan for cards    
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                # If a card is found
                if status == MIFAREReader.MI_OK:
                    print "Card detected"
                
                # Get the UID of the card
                (status,uid) = MIFAREReader.MFRC522_Anticoll()

                # If we have the UID, continue
                if status == MIFAREReader.MI_OK:

                    # Print UID
                    print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                    global id
                    id = (str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
                    
                    
                    
                    sql_select_query = """select distinct theKey from verify where UID = '""" + id + """'"""#select statement for sql
                    cursor.execute(sql_select_query)
                    record = cursor.fetchone()
                    print(id)
                    ValidfyFalse()
                    
                    #realkey = ''.join(currentkey)
                    verifykey = functools.reduce(operator.add, (record))
                    
                    thekey = verifykey.split(",")
                    intkey = [0,0,0,0,0,0]#sets db data to a format auth can understand
                    for i in range(6):
                    
                        intkey[i] = int(thekey[i], 16) 
                        print(intkey)
                   
                        
                        print(intkey[i])
                    #readCard()
                    print(intkey)
                    
                    # Select the scanned tag
                    MIFAREReader.MFRC522_SelectTag(uid)

                    # Authenticate
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, intkey, uid)
                    print "\n"

                    # Check if authenticated
                    if status == MIFAREReader.MI_OK:
                        print("verified")
                        MIFAREReader.MFRC522_Read(8)
                        
                        continue_reading = False
                        GPIO.cleanup()
                        ValidfyTrue()
                        
                        newkey = Key_Manager()
                        print(newkey)
                        MIFAREReader.MFRC522_Write(8, newkey)
                        
                        sql_select_query2 = """update verify Set theKey = '""" + newkey + """' where UID = '""" + id + """'""" #updates verify database
                        cursor.execute(sql_select_query2)
                        connection.commit()#commits the change
                        
                        
                        
                        MIFAREReader.MFRC522_Read(8)
                        MIFAREReader.MFRC522_StopCrypto1()
                    print(intkey)
                    
                    
                    
                    #MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
                    
            
            
            

            
            
            print("converint to string")

            #if(realkey == verifykey):#checks if key and the verify key are the same
                #print("updating")
                ##print(Card_Manager())
                #sql_select_query2 = """update verify Set theKey = '""" + Card_Manager() + """' where UID = '""" + id + """'""" #updates verify database
                #print("success"  )
                #cursor.execute(sql_select_query2)
                #connection.commit()#commits the change
                #ValidfyTrue()
                ##print(valid)
                
            #if(Tries == 3):#ran only if the card fails 3 times locks the card by settign the cards key stored to a random
                #sql_select_query2 = """update verify Set theKey = '""" + Card_Manager() + """' where UID = '""" + id + """'""" #updates verify database

                #cursor.execute(sql_select_query2)
                #connection.commit()#commits the change


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
      
end = False
#print(valid)
program()
#print(valid)
while end == False:
    
    if(valid == True):#tells you if card worked
        print("Card Verified")
        end = True
    else:#if card does not work
        print("Card Denied")
        if(Tries < 3):# allows card to try three times
            Tries = Tries + 1
            print("You have" + str(Tries) +" out of 3 tries remaining")
            program()
        else:#if it failed three times
            print("Error out of tries card locking...")
            program()
            print("Card locking successful")
            end = True
            
            
            
top = Tkinter.Tk()

top.minsize(200, 150)              

def runProgram():
    program()

B1 = Tkinter.Button(top, text = "start program", command = runProgram)

B1.pack()
top.mainloop()
GPIO.cleanup()
