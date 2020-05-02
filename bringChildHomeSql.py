import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import time
from difflib import SequenceMatcher
import datetime
from mysql.connector import Error

import urllib.parse

import urllib.request
import json
from fbchat import Client, ThreadType, Message
from urllib import request, parse
from urllib.request import Request, urlopen
import subprocess
import smtplib, ssl
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

client = Client()


def ledLightOnGreen():
    print("LED Green On")


    GPIO.setmode(GPIO.BCM)

    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(21, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(16, GPIO.OUT)
    print("LED on")
    GPIO.output(16, GPIO.HIGH)
    time.sleep(5)
    GPIO.cleanup()  # Clean up


def ledLightOnRed():
    print("LED Red On")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(21, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print("LED on")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(5)

    GPIO.cleanup()  # Clean up


def ledLightOnOrange():
    print("LED Orange On")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)
    print("LED on")
    GPIO.output(21, GPIO.HIGH)
    time.sleep(5)
    GPIO.cleanup()  # Clean up


def refresh(word, sid, parentName, timeNow):
    # Raspberry Pi pin configuration:
    print("Begin Display")
    RST = None  # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    # Beaglebone Black pin configuration:
    # RST = 'P9_12'
    # Note the following are only used with SPI:
    # DC = 'P9_15'
    # SPI_PORT = 1
    # SPI_DEVICE = 0

    # 128x32 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    # 128x64 display with hardware I2C:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

    # Note you can change the I2C address by passing an i2c_address parameter like:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

    # Alternatively you can specify an explicit I2C bus number, for example
    # with the 128x32 display you would use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

    # 128x32 display with hardware SPI:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # 128x64 display with hardware SPI:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # Alternatively you can specify a software SPI implementation by providing
    # digital GPIO pin numbers for all the required display pins.  For example
    # on a Raspberry Pi with the 128x32 display you might use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

    # Initialize library.
    disp.begin()
    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)

    # Write two lines of text.

    draw.text((x, top), str(word), font=font, fill=255)
    draw.text((x, top + 8), str(sid), font=font, fill=255)
    draw.text((x, top + 16), str(parentName), font=font, fill=255)
    draw.text((x, top + 25), str(timeNow), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()


refresh("1", "2", "3", "4")


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def connectSql():
    conn = mysql.connector.connect(
        host="194.59.164.64",
        user="u615769276_boitan",
        passwd="password",
        database="u615769276_finalyear"
    )
    return conn

#cursor.execute("SELECT * FROM tblCard")
#result = cursor.fetchall()
#print(result)
conn = connectSql()
print(conn)
today = datetime.date.today()
print(today)

def getStudent():

    cursor = conn.cursor(buffered=True)

    cursor.execute("SELECT studentId,parentId FROM studentTable WHERE parentId = '867364651663'")
    result = list(cursor.fetchall())
    final_result = [list(i) for i in result]
    print(final_result)
    print(final_result[0][1])

    bad_chars = [';', ':', '!', "*","'","[","]"]
    for x in final_result:
        test_string = ''.join(i for i in x if not i in bad_chars)
        print(str(test_string) , " in new student list")
    #['321', '123 Foord', '123', '943343799769', '867364651663']
getStudent()



#
def checkAttendance(scardId, datetoday):

    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT Attendance FROM Attendance WHERE StudentCardId='%s' AND Datee='%s'""" % (str(scardId),str(datetoday))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment

        # pass in the query and the argurment
        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        #print(len(result),"num row")
        if len(result) > 0 :
            #if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]","(",")",",","'"]
            #remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                #loop thought the result and get only one result
            return str(returnResult)
        else:
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()
print(checkAttendance("943343799769",today),"is check attendance")

#SELECT StudentCardId FROM Attendance WHERE StudentCardId='$scard' AND Datee='$datetoday'

# print(checkAttendance('943343799769',"2019-12-13"),"9s")

def checkCard(scardId, datetoday):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT StudentCardId FROM Attendance WHERE StudentCardId='%s' AND Datee='%s'""" % (str(scardId), str(datetoday))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return len(result)
        else:
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()
#print(checkCard("943343799769",today),"is check CARD")
#pneed to check here

# print(checkCard('943343799769',"2019-12-123"),"is student check card")
def checkCardCheckin(scardId, datetoday):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT StudentCardId FROM Attendance WHERE StudentCardId='%s' AND Datee='%s' AND CheckIn IS NULL""" % (
    str(scardId), str(datetoday))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return len(result)
        else:
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()


print(checkCardCheckin("943343799769","2019-12-19"),"is the result from the list")
# print(type(checkCardCheckin("943343799769","2019-12-19")),"is type")
# newstr = checkCardCheckin("943343799769","2019-12-19")
# if int(newstr) == 1 :
#    print("new str is 1")
# else:
##   print("neww")
# def insertCheckinOut(CardId):
#     try:
#
#         url = 'https://piegensoftware.com/myhtp.php'
#         values = {'insertCheckinOut': '',
#                   'CardId': CardId,
#                   }
#
#         data = parse.urlencode(values).encode()
#         req = Request(url,
#                       headers={'User-Agent': 'Mozilla/5.0'}
#                       , data=data)
#         webpage = urlopen(req).read().decode()
#         print(webpage)
#     except Exception as e:
#         print(e)

#
# def insertCheckin(CardId, time, datetoday):
#     try:
#
#         url = 'https://piegensoftware.com/myhtp.php'
#         values = {'insertCheckin': '',
#                   'CardId': CardId,
#                   'time': time,
#                   'datetoday': datetoday,
#                   }
#
#         data = parse.urlencode(values).encode()
#         req = Request(url,
#                       headers={'User-Agent': 'Mozilla/5.0'}
#                       , data=data)
#         webpage = urlopen(req).read().decode()
#         print(webpage)
#     except Exception as e:
#         print(e)


# undone part !!!!!!!!!!!!!!!!!



def CheckIfNotNull(scardID, datetoday):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT CheckIn FROM Attendance WHERE StudentCardId='%s' AND Datee='%s'""" % (
    str(scardID), str(datetoday))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


print(CheckIfNotNull('943343799769','2020-04-00'),"is the check if not null")

def updateCheckOut(CardId, checkouttime):

    cursor = conn.cursor(prepared=True)
    try:

        present = "present"
        sql_update_query = """UPDATE Attendance SET Checkout='%s', Attendance='%s' WHERE StudentCardId='%s' AND Checkout IS NULL"""

        data_tuple = (checkouttime,present,CardId)
        cursor.execute(sql_update_query, data_tuple)
        conn.commit()
        print("updateCheckOut table updated using the prepared statement")

    except mysql.connector.Error as error:
        print("updateCheckOut parameterized query failed {}".format(error))
    finally:
        cursor.close()


def insertStudentCheckin(CardId, datetoday):

    cursor = conn.cursor(prepared=True)
    try:
        absent = 'absent'

        sql_insert_query = """INSERT INTO Attendance (StudentCardId,Datee,Attendance) VALUES ('%s','%s','%s')"""

        insert_tuple= (CardId,datetoday,absent)

        cursor.execute(sql_insert_query, insert_tuple)
        conn.commit()
        print("Data inserted successfully into attendance table using the prepared statement")

    except mysql.connector.Error as error:
        print("attendance table parameterized query failed {}".format(error))
    finally:
        cursor.close()

def getParentName(studentId):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentName FROM tblCard WHERE studentId = '%s'""" % (
        str(studentId))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()

def getStudentName(studentId):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentName FROM studentTable WHERE studentId = '%s'""" % (
        str(studentId))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()
def getParentId(studentId):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentId FROM studentTable WHERE studentId = '%s'""" % (
        str(studentId))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()

def validStudent(studentId,dateToday,type):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentId FROM tblNotifications WHERE studentId = '%s' AND msgDate = '%s' and type = '%s'""" % (
        str(studentId),str(dateToday),str(type))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return len(result)
        else:
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()

print(getParentName(943343799769),"is parent Name")
print(getStudentName(943343799769),"is student Name")
print(getParentId(943343799769),"is pARENT ID")

def insertCheckinNotification(sCardId, timeNow, datetoday):

    cursor = conn.cursor(prepared=True)
    try:
        parentName = getParentName(sCardId)
        studentName = getStudentName(sCardId)
        parentId = getParentId(sCardId)

        message = "Dear "+str(parentName)+", Your Child "+ str(studentName)+" Check In at "+str(timeNow)
        numOfResult = validStudent(sCardId,datetoday, "checkIn")
        numOfResult2 = validStudent(sCardId,datetoday, "checkOut")
        totalResult = numOfResult + numOfResult2
        confirmStatus = "0"
        type = "CheckIn"
        status = "unread"
        if totalResult < 2 :
            #if student check in twice then cannot liao
            sql_insert_query = """INSERT INTO tblNotifications (parentId,parentName,studentId,type,status,message,checkInOutTime,msgDate,confirmStatus) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"""

            insert_tuple = (parentId,parentName,sCardId,type,status,message,timeNow,datetoday,confirmStatus)

            cursor.execute(sql_insert_query, insert_tuple)
            conn.commit()
            print("Data inserted successfully into tblNotification table using the prepared statement")
        else:
            print("student punch card already today")

    except mysql.connector.Error as error:
        print("tblNotification table parameterized query failed {}".format(error))
    finally:
        cursor.close()


def insertCheckoutNotification(sCardId, timeNow, datetoday):

    cursor = conn.cursor(prepared=True)
    try:
        parentName = getParentName(sCardId)
        studentName = getStudentName(sCardId)
        parentId = getParentId(sCardId)

        message = "Dear " + str(parentName) + ", Your Child " + str(studentName) + " Check Out at " + str(timeNow)
        numOfResult = validStudent(sCardId, datetoday, "checkIn")
        numOfResult2 = validStudent(sCardId, datetoday, "checkOut")
        totalResult = numOfResult + numOfResult2
        confirmStatus = "0"
        type = "CheckOut"
        status = "unread"
        if totalResult < 2:
            # if student check in twice then cannot liao
            sql_insert_query = """INSERT INTO tblNotifications (parentId,parentName,studentId,type,status,message,checkInOutTime,msgDate,confirmStatus) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"""

            insert_tuple = (parentId, parentName, sCardId, type, status, message, timeNow, datetoday, confirmStatus)

            cursor.execute(sql_insert_query, insert_tuple)
            conn.commit()
            print("Data inserted successfully into tblNotification table using the prepared statement")
        else:
            print("student punch card already today")

    except mysql.connector.Error as error:
        print("tblNotification table parameterized query failed {}".format(error))
    finally:
        cursor.close()


def findParentId(studentCardId):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentId FROM studentTable WHERE studentId = '%s'""" % (
        str(studentCardId))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


def findFbId(parentCardId):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentFbId FROM parentTable WHERE parentId = '%s' AND parentFbId IS NOT NULL""" % (
        str(parentCardId))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


def updateCheckin(CardId, checkInTime):

    cursor = conn.cursor(prepared=True)
    try:
        absent = 'absent'

        sql_update_query = """UPDATE Attendance SET CheckIn='%s', Attendance='%s' WHERE StudentCardId='%s' AND CheckIn IS NULL"""

        data_tuple = (checkInTime,absent,CardId)
        cursor.execute(sql_update_query, data_tuple)
        conn.commit()
        print("update attendance table updated using the prepared statement")

    except mysql.connector.Error as error:
        print("update attendance parameterized query failed {}".format(error))
    finally:
        cursor.close()


def allStudrecord():

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentId FROM studentTable"""
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())

        final_result = [list(i) for i in result]
        print(final_result)
        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result
            #['321', '123 Foord', '123', '943343799769', '867364651663']


            return final_result
        else:
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()

print(allStudrecord())
    #insertStudentCheckin(z, today)


def checkStudentCardStatus(sCardId):
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentCardStatus FROM studentTable WHERE studentId = '%s'""" % (
        str(sCardId))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()
print(checkStudentCardStatus(943343799769),"is staatus student card")


def checkParentCardStatus(pCardId):
    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentCardStatus FROM parentTable WHERE parentId = '%s'""" % (
        str(pCardId))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


# print(allStudrecord(),"is student record")
newStudentList = []


# print(CheckIfNotNull('943343799769','2019-12-19'),"is check if not null")

async def main():
    await client.start("0169787592", "nimabi123")
    print("****Login Success*****")
    print(f"Own ID: {client.uid}")
    # await client.logout()
    # print(returnParentIds())
    reader = SimpleMFRC522()


    try:
        while True:
            studentCardList = [943343799769]
            parentCardList = [867364651663]
            # store the list of card to check

            counter = 0
            today = datetime.date.today()

            for x in allStudrecord():
                bad_chars = [';', ':', '!', "*", "'", "[", "]"]
                test_string = ''.join(i for i in x if not i in bad_chars)
                print(str(test_string), " in new student list")
                # print(newStudentRecord)#None after remove the extra character
                newStudentList.append(test_string)  # result = ['321', 'None', 'None', '943343799769']
            try:
                for z in newStudentList:
                    # newStudentList return all the student card id in card table
                    if z != "None" and int(checkCard(z, today)) < 1:
                        # if student id is not equal to none and check card today record is lest than one
                        print("Havent punch card today", z)
                        # then help that student to insert record
                        insertStudentCheckin(z, today)
                    elif z != "None" and int(checkCard(z, today)) >= 1:
                        print(z, "punch card already today!")
            except:
                print("***Something else when wrong***")

            # auto insertion of the record that have not punch car4d today
            del newStudentList[:]
            # clear the list or else it will duplicate
            refresh("---", "Scan your card to bring", "record attendance", "----")

            print("Scan your Card to record attendance")
            id1, text = reader.read()
            refresh("---", "reading card", "recording attendance", "----")

            # get the id and name of the card

            # print(id)
            # print(text)
            # print("Num of time :",counter)
            # print how many time it scan

            # do a validation that cannot scan the card twice
            # can be done by forcing all the 4 column to be the diffrent value or comparison with the value that previosly inserted

            myFirstCard = text
            myCardId = id1  #
            today = datetime.date.today()
            print(today)
            todaytime = datetime.datetime.now().time()
            print(todaytime)
            studentCardStatus = checkStudentCardStatus(myCardId)
            print(studentCardStatus, "is card status")
            parentId = findParentId(myCardId)
            # get the parent id by scanning student id
            parentFb = findFbId(parentId)
            # get the parent fb by passing parent id in

            try:
                if studentCardStatus == "Valid":
                    print("card valid")
                    checkCardIn = checkCardCheckin(myCardId, today)
                    checkAttend = checkAttendance(myCardId, today)
                    if checkCardIn == str(1):
                        # the checkCard check in return the row where

                        # student already punch card but no check in record found
                        #
                        print("Havent punch card today")
                        bl = CheckIfNotNull(myCardId, today)
                        if bl == "" or bl == "None":
                            # if the check in return null or havent check in yet

                            print("Student Havent check in yet")
                            updateCheckin(myCardId, todaytime)
                            insertCheckinNotification(myCardId, todaytime, today)
                            refresh("-----------------", "check in success", "successfuly checked", "----")

                            # print(parentId ,"is parent id")

                            # get the parent id for search it in the email or fb
                            if parentId != "None":  # if the user really have fb id
                                user = (await client.search_for_users(parentFb))[0]
                                parentFbId = user.uid
                                parentFbName = user.name

                                # store the parentFb id
                                await client.send(Message(text="Dear " + str(parentFbName) + ", Your child : " + str(
                                    myFirstCard) + " checked in at " + str(todaytime) + ", in the date of, " + str(
                                    today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                                refresh("----------------", "NOTIFICATIONS", "SUCCESSFULLY SENDED", "---------------")
                            else:
                                refresh("----------------", "PARENT FACEBOOK", "NOT FOUND", "---------------")

                                print("parent fb not found")

                            time.sleep(3)
                            # if the student already check in then update the check up
                        else:
                            #
                            print("updating the checwwwwwk out")
                            updateCheckOut(myCardId, todaytime)
                            # get the parent id for search it in the email or fb
                            if parentId != "None":  # if the user really have fb id

                                user = (await client.search_for_users(parentFb))[0]
                                parentFbId = user.uid
                                parentFbName = user.name

                                # store the parentFb id
                                await client.send(Message(text="Dear " + str(parentFbName) + ", Your child : " + str(
                                    myFirstCard) + " checked in at " + str(todaytime) + ", in the date of" + str(
                                    today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                            time.sleep(3)

                    elif checkAttend == "present":
                        # add one more condition to check whether if he or she is present today
                        print("punch card already today can go back ")
                        refresh("---", "punch card already", "today can go back ", "----")

                        time.sleep(3)


                    elif int(checkCard(myCardId, today)) >= 1 and CheckIfNotNull(myCardId, today) != "None":

                        # if the check in is not null and already insert today but the card
                        # print("punch check in already")
                        print("updating the check out")

                        updateCheckOut(myCardId, todaytime)
                        insertCheckoutNotification(myCardId, todaytime, today)
                        refresh("---", "student check out ", "checking out ", "----")

                        if parentId != "None":  # if the user really have fb id
                            # get the parent id for search it in the email or fb
                            user = (await client.search_for_users(parentFb))[0]
                            parentFbId = user.uid
                            parentFbName = user.name

                            # store the parentFb id
                            await client.send(Message(text="Dear " + str(parentFbName) + ", Your child : " + str(
                                myFirstCard) + " checked out at " + str(todaytime) + ", in the date of, " + str(today)),
                                              thread_id=int(parentFbId), thread_type=ThreadType.USER)
                            refresh("---", "message sended ", "to fb checkout ", "----")

                        time.sleep(3)
                    else:

                        ###############if the card does not in the list
                        print("card invalid")
                        refresh("---", "card invalid", "card invalid", "----")

                elif studentCardStatus == "Invalid".casefold():
                    print("student card invalid")
                    refresh("---", "student card invalid", "card invalid", "----")

                elif studentCardStatus == "None".casefold():
                    print("cannot use parent card")
                    refresh("------------", "Card not registed yet", "please use registered card", "--------")
                else:
                    refresh("------------", "Card not useable", "please use registered card", "--------")


            except:
                print("£££Something when wrong£££")

        # print(str(myFirstCardId),"printed in string")
        # check for duplicated entry



    finally:
        GPIO.cleanup()


client.loop.run_until_complete(main())