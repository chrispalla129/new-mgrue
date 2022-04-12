import sys

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QTimer, QObject, Signal

from time import strftime, localtime
import serial


global fileCounter
fileCounter = 0

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('main.qml')



class Backend(QObject):

    updated = Signal(str, arguments=['time'])

    def __init__(self):
        super().__init__()

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs 100 = 1/10th sec
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def update_time(self):
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        self.updated.emit(curr_time)

    # with serial.Serial('COM1', 19200, timeout=1) as ser:
    #     bytesMessage = ser.readline()           # read a '\n' terminated line
    #     bytesMessage += ser.readline()          # Reads data & metadata
    #     message = bytesMessage.decode("utf-8")  # convert bytes to string

    #     #Writes to a new file, increments fileCounter
    #     file = open(backend.fileName + "/test_" + str(fileCounter) + ".fn", "a")
    #     file.write(message)
    #     file.close()
    #     fileCounter += 1


# Crashes most of the time, unsure why.
# engine.rootObjects()[0].setProperty('backend', backend)

# Define our backend object, which we pass to QML.
backend = Backend()


backend.update_time()

sys.exit(app.exec_())