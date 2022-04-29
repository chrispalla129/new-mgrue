import sys

from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal, QTimer

from time import strftime, localtime
import serial

global fileCounter
fileCounter = 0
# Define our backend object, which we will pass to the engine object
class Backend(QObject):

    updated = Signal(str, arguments=['time'])
    status = Signal(str)

    def __init__(self):
        super().__init__()

        self.destination_folder = ""

    # This function is sending data to the frontend (uses the status signal)
    def update_status(self, msg):
        # Pass the current status message to QML.
        self.status.emit(msg)

    # This function is getting data from frontend
    @Slot(str)
    def getFileLocation(self, location):
        print("User selected: " + location)
        self.destination_folder = location

    def readSerial(self):
        with serial.Serial('COM1', 19200, timeout=1) as ser:
            self.update_status("Awaiting Connection")
            if (ser.inWaiting() > 0):
                bytesMessage = ser.readline().decode()   # read a '\n' terminated line

                if bytesMessage == 'connect':
                    ser.write(b'handshake')
                    self.update_status("Device Connected")

                    if (ser.inWaiting() > 0):
                        bytesMessage = ser.readline().decode()

                        if bytesMessage == 'transfer' and self.destination_folder != "":
                            self.update_status("Data transfer in progress....")
                            file = open(self.destination_folder + "/test_" + str(fileCounter) + ".fn", "w")
                            sequenceNum = 0
                            nextLine = ser.readline().decode()
                            while nextLine != '\n':
                                meta = nextLine
                                sequence = ser.readline().decode()
                                file.write(meta)
                                file.write(sequence)
                                sequenceNum += 1

                                if sequenceNum == 4000:
                                    file.close()
                                    fileCounter += 1
                                    sequenceNum = 0
                                    file = open(self.destination_folder + "/test_" + str(fileCounter) + ".fn", "w")

                                nextLine = ser.readline().decode()
                            self.update_status("Data transfer complete! Awaiting new action...")
                                

                        if bytesMessage == 'new_rate':
                            newBaud = ser.readline().decode()
                            self.update_status("Baud rate updated to " + newBaud)
                            ser.setBaudrate(newBaud)


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    # Added to avoid runtime warnings
    app.setOrganizationName("Some Company")
    app.setOrganizationDomain("somecompany.com")
    app.setApplicationName("Amazing Application")
    app.setWindowIcon(QIcon("images/icon.png"))
    engine = QQmlApplicationEngine()

    # Load QML file
    engine.load('main.qml')
    engine.quit.connect(app.quit)

    # Get QML File context
    backend = Backend()
    engine.rootObjects()[0].setProperty('backend', backend)
    backend.readSerial()

    sys.exit(app.exec_())

