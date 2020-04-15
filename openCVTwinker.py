import os
import tkinter
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import tkinter.messagebox
import pyqrcode
from pyzbar.pyzbar import  decode
from PIL import Image
from urllib import request, parse
from urllib.request import Request, urlopen
from datetime import datetime

from urllib.error import HTTPError
import  time
def mainQr():
    count = 0

    def center(win):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 5 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    class FullScreenApp(object):
        def __init__(self, master, **kwargs):
            self.master=master
            pad=3
            self._geom='200x200+0+0'
            master.geometry("{0}x{1}+0+0".format(
                master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
            master.bind('<Escape>',self.toggle_geom)
        def toggle_geom(self,event):
            geom=self.master.winfo_geometry()
            print(geom,self._geom)
            self.master.geometry(self._geom)
            self._geom=geom
    def select_image():
            # grab a reference to the image panels
            global panelA
            global count
            global qrDataDisplayName
            global qrDataDisplayDate
            global qrDataDisplayTimeOne
            global qrDataDisplayTimeTwo
            global fileName
            global buttonVerify




            # open a file chooser dialog and allow the user to select an input
            # image
            path = filedialog.askopenfilename()
            try:
                def checkBooking(parentName,studentName,pickUpDate,pickUpTimeOne,pickUpTimeTwo):

                #check booking data by passing all data inhere
                    try:
                        url = "https://piegensoftware.com/myhtp.php"
                        data = {
                            'checkBooking':"1",
                            # 'updateBooking': "1",

                            'parentName': parentName,
                            'studentName': studentName,
                            'pickUpDate': pickUpDate,
                            'pickUpTimeOne': pickUpTimeOne,
                            'pickUpTimeTwo': pickUpTimeTwo,
                        }

                        data = parse.urlencode(data).encode()
                        TimeNow = (datetime.now().strftime("%H:%M"))
                        #get the currrent time in hour and minit format
                        if (isNowInTimePeriod(pickUpTimeOne,pickUpTimeTwo,TimeNow)) == True:
                            #if time are with in the range then request

                            req = Request(
                                    url,
                                    headers={'User-Agent': 'Mozilla/5.0'}
                                    ,data=data)
                            webpage = urlopen(req).read().decode()
                            print(webpage)
                            if webpage == "Valid":
                                print("can bring children home")
                                tkinter.messagebox.showinfo(title="Valid Qr Code", message="can bring children home")

                            elif webpage == "Not Valid":
                                print("qr code expired")
                                tkinter.messagebox.showinfo(title="Qr Code Not Valid", message="qr code expired")

                            elif webpage == "No Record Found":
                                tkinter.messagebox.showwarning(title="No Booking Record Found", message="No Booking Record Found , Please make the booking first.")


                                print("No Booking Record Found , Please make the booking first.")
                        else:
                            tkinter.messagebox.showwarning(title="Time Not Reached Yet",
                                                           message="Time Now Are Not With in the range")

                            print( "Booking Time Not With In The Range")

                    except HTTPError as e:

                         content = e.read()
                         print(e)
                #return the response

                def clearWidget():
                    #clear widget on the form after it reload to prevent duplication
                    list = root.pack_slaves()
                    for l in list:

                        fileName.destroy()
                        qrDataDisplayName.destroy()
                        qrDataDisplayDate.destroy()
                        qrDataDisplayTimeTwo.destroy()
                        qrDataDisplayTimeOne.destroy()

                        buttonVerify.destroy()

                def isNowInTimePeriod(startTime, endTime, nowTime):
                    #check if the time are with in the range , if not then cannot use qrcode
                    if startTime < nowTime and nowTime < endTime:
                         return True
                    else:
                         return False
                if len(path) > 0:
                    # load the image from disk, convert it to grayscale, and detect
                    # edges in it
                    image = cv2.imread(path)
                    oriname = os.path.basename(path)
                    if "qrcode" in path:
                        qrcodeData = decode(Image.open(oriname))
                        print("In qrcode file - -- ")
                    else:
                        qrcodeData = decode(Image.open(path))
                        print("not in qrcode file")
                    print(oriname)
                    print(path)
                    qrcode = (qrcodeData[0].data.decode('utf8'))
                    qrcodeArr = qrcode.split(",")
                    print(qrcodeArr[0])
                    print(qrcodeArr[1])
                    print(qrcodeArr[2])
                    print(qrcodeArr[3])

                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # OpenCV represents images in BGR order; however PIL represents
                    # images in RGB order, so we need to swap the channels
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    # convert the images to PIL format...
                    image = Image.fromarray(image)
                    # ...and then to ImageTk format
                    image = ImageTk.PhotoImage(image)
                    if panelA is None and count < 1:

                        # the first panel will store our original image
                        panelA = Label(image=image)
                        panelA.image = image
                        panelA.pack(side="left", padx=10, pady=10)
                        TimeNow = (datetime.now().strftime("%H:%M"))

                        fileName = Label(root, text="Date Today : "+datetime.now().strftime("%m-%d-%Y")+"\n\nTime Now : "+TimeNow+"\n\nQR Code Info:\n\nFile Name = "+str(oriname),font=("Helvetica", 16))
                        fileName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayName = Label(root, text="QR CODE NAME = " + str(qrcodeArr[0]),bg="black",fg="white",font=("Helvetica", 16))
                        qrDataDisplayDate = Label(root, text="QR CODE DATE = " + str(qrcodeArr[1]),font=("Helvetica", 16))
                        qrDataDisplayTimeOne = Label(root, text="QR CODE TIME START FROM = " + str(qrcodeArr[2]),bg="black",fg="white",font=("Helvetica", 16))
                        qrDataDisplayTimeTwo = Label(root, text="QR CODE = TIME END = " + str(qrcodeArr[3]),font=("Helvetica", 16))

                        qrDataDisplayName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayDate.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayTimeOne.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayTimeTwo.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        buttonVerify = tkinter.Button(text='Verify', width=25,command= lambda: checkBooking("myparent",qrcodeArr[0],qrcodeArr[1],qrcodeArr[2],qrcodeArr[3]),font=("Helvetica", 16))
                        buttonVerify.pack()
                        #pass this lambda function to get thogught
                        count = count + 1
                        print(count)

                        print("open image ")
                        # while the second panel will store the edge map

                        # otherwise, update the image panels
                    elif(count >= 1):
                        clearWidget()
                        count = count + 1
                        print(count)

                        # update the pannels
                        panelA.configure(image=image)
                        panelA.image = image
                        TimeNow = (datetime.now().strftime("%H:%M"))

                        fileName = Label(root, text="Date Today : " + datetime.now().strftime(
                            "%m-%d-%Y") + "\n\nTime Now : " + TimeNow + "\n\nQR Code Info:\n\nFile Name = " + str(oriname),
                                         font=("Helvetica", 16))
                        fileName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayName = Label(root, text="QR CODE NAME = " + str(qrcodeArr[0]),bg="black",fg="white",font=("Helvetica", 16))
                        qrDataDisplayDate = Label(root, text="QR CODE DATE = " + str(qrcodeArr[1]),font=("Helvetica", 16))
                        qrDataDisplayTimeOne = Label(root, text="QR CODE TIME START FROM = " + str(qrcodeArr[2]),bg="black",fg="white",font=("Helvetica", 16))
                        qrDataDisplayTimeTwo = Label(root, text="QR CODE = TIME END = " + str(qrcodeArr[3]),font=("Helvetica", 16))

                        qrDataDisplayName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayDate.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayTimeOne.pack(side=TOP, anchor=W, fill=X, expand=YES)
                        qrDataDisplayTimeTwo.pack(side=TOP, anchor=W, fill=X, expand=YES)

                        buttonVerify = tkinter.Button(text='Verify', width=25,command= lambda: checkBooking("myparent",qrcodeArr[0],qrcodeArr[1],qrcodeArr[2],qrcodeArr[3]),font=("Helvetica", 16))
                        buttonVerify.pack()

                        print("open image 2")

            except Exception  as e:
                 print(e)

                 tkinter.messagebox.showerror(title=None, message="Not A Valid Qr Code")


    # initialize the window toolkit along with the two image panels
    root = Tk()

    root.title("Qr Code Information")
    center(root)
    app=FullScreenApp(root)

    panelA = None
    # create a button, then when pressed, will trigger a file chooser
    # dialog and allow the user to select an input image; then add the
    # button the GUI
    btn = Button(root, text="Click Me to Select an qr code", command=select_image,font=("Helvetica", 16))
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    # kick off the GUI
    root.mainloop()

    #first step , scan and display the data ,

    #compare the data by using , select * from booking table where qrcode is not scanned
    #if got record then green light
    #after green light , update the record to make it scanned
mainQr()

