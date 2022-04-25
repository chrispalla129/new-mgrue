import sys

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal, QTimer

from time import strftime, localtime
import serial


global fileCounter
fileCounter = 0


# Define our backend object, which we will pass to the engine object
class Backend(QObject):

    updated = Signal(str, arguments=['time'])

    def __init__(self):
        super().__init__()

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs 100 = 1/10th sec
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        self.destination_folder = ""

    def update_time(self):
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        self.updated.emit(curr_time)

    @Slot(str)
    def getFileLocation(self, location):
        print("User selected: " + location)
        self.destination_folder = location

    def readSerial(self):
        with serial.Serial('COM1', 19200, timeout=1) as ser:
            bytesMessage = ser.readline()           # read a '\n' terminated line
            bytesMessage += ser.readline()          # Reads data & metadata
            message = bytesMessage.decode("utf-8")  # convert bytes to string

            #Writes to a new file, increments fileCounter
            file = open(self.destination_folder + "/test_" + str(fileCounter) + ".fn", "a")
            file.write(message)
            file.close()
            fileCounter += 1


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Load QML file
    engine.load('main.qml')
    engine.quit.connect(app.quit)

    # Get QML File context
    backend = Backend()
    engine.rootObjects()[0].setProperty('backend', backend)
    backend.update_time()

    sys.exit(app.exec_())

