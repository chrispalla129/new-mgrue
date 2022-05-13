import sys
import time
import threading

from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal

from datetime import datetime
import serial

# Define our backend object, which we will pass to the engine object
class Backend(QObject):
    recordsPerFile = 500        # Set max number of records that will be written to each file here
    currentStatus = "awaiting"
    buttonMessage = "Start Transfer"
    status = Signal(str)
    def __init__(self):
        super().__init__()

        self.destination_folder = ""

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
        
    #This function sets the max records per file based on user input
    def update_records(self,n):
        self.recordsPerFile = n

    # This function is getting data from frontend
    @Slot()
    def startTransfer(self):
        print("User Clicked Button!")
        if (self.currentStatus == "Awaiting Connection" or \
                self.currentStatus == "Attempting to Connect..."): 
            thread = threading.Thread(target=self.writeSerial, args=())
            thread.start()
        elif (self.currentStatus == "Connected"):
            print("Pausing...")
            self.update_status("Pausing...")
        elif (self.currentStatus == "Paused"):
            print("Unpaused!")
            self.update_status("Connected")
        elif (self.currentStatus == "Finished Transfer"):
            thread = threading.Thread(target=self.writeSerial, args=())
            thread.start()

    def writeSerial(self):
        with serial.Serial('/dev/ttyGS0', 256000, timeout=1) as ser:
            while (self.currentStatus != "Finished Transfer"):
                if (self.currentStatus == "Awaiting Connection" or \
                        self.currentStatus == "Attempting to Connect..."):
                    bytesMessage = ser.readline().decode()[:-1]     # read a '\n' terminated line, removing the \n
                    print(bytesMessage)
                    if(bytesMessage == "handshake"):
                        self.update_status("Connected")
                        print("connected!")
                    else:
                        self.update_status("Attempting to Connect...")
                        ser.write(b"connect\r\n")
                        print("connecting...")
                        time.sleep(.5)
                elif(self.currentStatus == "Connected"):
                    with open("/home/pi/Projects/true-mgrue/largeSet.fn", "r") as f:
                        for line in f.readlines():
                            ser.write(line.encode("utf-8"))
                            if (self.currentStatus == "Pausing..." and line == "\n"):     
                                while(self.currentStatus == "Pausing..." or self.currentStatus == "Paused"):
                                    if (self.currentStatus == "Pausing..."):
                                        ser.write(b"pause\r\n")
                                        self.update_status("Paused")
                                    time.sleep(.1)
                                
                        self.update_status("Finished Transfer")
                        print("finished writing to port")
                
                    


def init(recordsPerFile):
    app = QGuiApplication(sys.argv)

    # Added to avoid runtime warnings
    app.setOrganizationName("UB CSE-453")
    app.setOrganizationDomain("engineering.buffalo")
    app.setApplicationName("mGRUE Emulator")
    app.setWindowIcon(QIcon("images/icon.png"))
    
    engine = QQmlApplicationEngine()
    
    # Load QML file
    engine.load('main.qml')
    engine.quit.connect(app.quit)

    # Get QML File context
    backend = Backend()
    engine.rootObjects()[0].setProperty('backend', backend)
    backend.update_records(recordsPerFile)
    
    backend.update_status("Awaiting Connection")
    sys.exit(app.exec_())
