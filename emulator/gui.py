import sys
import time
import threading
import os

from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal

from datetime import datetime
import serial
import math
# Define our backend object, which we will pass to the engine object
class Backend(QObject):
    recordsPerFile = 500        # Set max number of records that will be written to each file here
    currentStatus = "awaiting"
    buttonMessage = "Start Transfer"
    transferSpeed = 5
    stopFunction  = False
    status = Signal(str)
    speed = Signal(int)
    thread = 0
    def __init__(self):
        super().__init__()

        self.source_file = ""

    # This function is sending data to the frontend (uses the status signal)
    def update_status(self, msg):
        # Pass the current status message to QML.
        self.currentStatus = msg
        self.status.emit(msg)

    # This function is sending data to the frontend (uses the status signal)
    def update_buton_msg(self, msg):
        # Pass the current status message to QML.
        self.buttonMessage = msg
        self.status.emit(msg)
    # This function is sending the updated speed to the frontend (uses the speed signal)
    def update_speed(self,speed):
        self.transferSpeed = speed
        self.speed.emit(speed)

    #This function sets the max records per file based on user input
    def update_records(self,n):
        self.recordsPerFile = n

    def getDelay(self,n):
        if n == 1:
            return 1/2000
        elif n == 2:
            return 1/6000
        elif n == 3:
            return 1/24000
        elif n == 4:
            return 1/72000
        elif n == 5:
            return 0

    # This function is getting data from frontend
    @Slot()
    def stopTransfer(self):
        self.stopFunction = True
        
    # This function increases the transfer speed by 1
    @Slot()
    def upSpeed(self):
        print("Speed Increased")
        self.transferSpeed += 1
        self.update_speed(self.transferSpeed)

    # This function decreases the transfer speed by 1
    @Slot()
    def downSpeed(self):
        print("Speed Decreased")
        self.transferSpeed -= 1
        self.update_speed(self.transferSpeed)

    # This function is getting data from frontend
    @Slot()
    def startTransfer(self):
        print("User Clicked Button!")
        if (self.currentStatus == "Awaiting Connection" or \
                self.currentStatus == "Attempting to Connect..."):

            self.thread = threading.Thread(target=self.writeStarter, args=())
            self.thread.start()
        elif "Connected" in self.currentStatus:
            print("Pausing...")
            self.update_status("Pausing...")
        elif (self.currentStatus == "Paused"):
            print("Unpaused!")
            self.update_status("Connected, transferring....")
        elif self.currentStatus == "Finished Transfer" or self.currentStatus == "User stopped transfer early.":
            self.stopFunction = False


    def writeStarter(self):
        while True:
            if not self.stopFunction:
                self.update_status("Awaiting Connection")
                self.writeSerial()

    def writeSerial(self):
        waitTime = self.getDelay(self.transferSpeed)
        try:                
            ser = serial.Serial('/dev/ttyGS0', 921600, timeout=1)
        except:
            self.update_status("ERROR: Serial port connection error!")
            return
        with ser:
            while (True):
                if (self.currentStatus == "Awaiting Connection" or \
                        self.currentStatus == "Attempting to Connect..."):
                    bytesMessage = ser.readline().decode()[:-1]     # read a '\n' terminated line, removing the \n
                    print(bytesMessage)
                    if(bytesMessage == "handshake"):
                        self.update_status("Connected")
                        print("connected!")
                    else:
                        self.update_status("Attempting to Connect...")
                        ser.write(b"connect\n")
                        print("connecting...")
                        time.sleep(.5)
                elif "Connected" in self.currentStatus:
                    try:
                        f = open("/home/pi/data/largeSet.fn", "r")
                    except:
                        self.update_status("ERROR: File read error!")
                        return
                    self.update_status("Connected, transferring....")
                    with f:
                        lines = f.readlines()
                        count = 0
                        total = len(lines)
                        for line in lines:
                            ser.write(line.encode("utf-8"))
                            if (self.currentStatus == "Pausing..."):     
                                while(self.currentStatus == "Pausing..." or self.currentStatus == "Paused"):
                                    if (self.currentStatus == "Pausing..."):
                                        ser.write(b"pause\n")
                                        self.update_status("Paused")
                                    elif self.stopFunction:
                                        self.update_status("User stopped transfer early.")
                                        ser.write(b"kill\n")
                                        time.sleep(1)
                                        return
                                    time.sleep(.1)
                            if self.stopFunction:
                                self.update_status("User stopped transfer early.")
                                ser.write(b"kill\n")
                                time.sleep(1)
                                return
                            time.sleep(waitTime)
                            # Slows down the program too much, unfortunately...
                            # if (self.currentStatus != "Pausing..."):
                            #     self.update_status("Connected: " + \
                            #                         str(math.floor((count / total) * 100)) + "% complete")
                            count += 1

                        self.update_status("Finished Transfer")
                        print("finished writing to port")
                elif self.currentStatus == "Finished Transfer":
                    ser.write(b"done\n")
                    print("Wrote done!")
                    self.stopFunction = True
                    time.sleep(5)
                    return



def init(recordsPerFile):
    app = QGuiApplication(sys.argv)

    # Added to avoid runtime warnings
    app.setOrganizationName("UB CSE-453")
    app.setOrganizationDomain("engineering.buffalo")
    app.setApplicationName("mGRUE Emulator")
    app.setWindowIcon(QIcon("images/icon.png"))

    engine = QQmlApplicationEngine()

    # Load QML file
    engine.load(os.path.dirname(os.path.abspath(__file__)) + '/main.qml')
    engine.quit.connect(app.quit)

    # Get QML File context
    backend = Backend()
    engine.rootObjects()[0].setProperty('backend', backend)
    backend.update_records(recordsPerFile)

    backend.update_status("Awaiting Connection")
    sys.exit(app.exec_())
