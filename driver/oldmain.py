import sys
import time
import threading

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal, QTimer

from datetime import datetime
import serial


# Define our backend object, which we will pass to the engine object
class Backend(QObject):
    recordsPerFile = 500        # Set max number of records that will be written to each file here
    currentStatus = ""
    updated = Signal(str, arguments=['time'])
    status = Signal(str)

    def __init__(self):
        super().__init__()

        self.destination_folder = ""

    # This function is sending data to the frontend (uses the status signal)
    def update_status(self, msg):
        # Pass the current status message to QML.
        backend.currentStatus = msg
        self.status.emit(msg)
        

    # This function is getting data from frontend
    @Slot(str)
    def getFileLocation(self, location):
        print("User selected: " + location[7:])
        self.destination_folder = location[7:]

    def readSerial(self):
        with serial.Serial('/dev/pts/9', 256000, timeout=1) as ser:
            while (True):
                stillReading    = True
                curTime         = datetime.now().strftime("%H-%M-%S")
                sequenceNum     = 0
                fileCounter     = 0
                bytesMessage    = ser.readline().decode()[:-1]     # read a '\n' terminated line, removing the \n

                if bytesMessage == 'connect' and self.destination_folder != "":
                    ser.write(b'handshake')
                    self.update_status("Device Connected")
                    file = open(self.destination_folder + "/" + curTime + "_file" + str(fileCounter) + ".fn", "w")

                    while (stillReading or self.currentStatus == "Paused."):       # Run while file is still being read or the reading is paused.
                        bytesMessage = ser.readline().decode()[:-1]     # This should either be the start of a record, a new_rate command, or EOF

                        if bytesMessage == 'new_rate' and self.currentStatus == "Paused.":     # Only update rate when paused.
                            newBaud = ser.readline().decode()
                            self.update_status("Baud rate updated to " + newBaud)
                            ser.setBaudrate(newBaud)
                        elif bytesMessage == 'pause':       # Pauses the transfer for a baud rate change
                            self.update_status("Paused.")
                        elif bytesMessage != "" and bytesMessage[0] == '>':     # Ensures that the first piece of data of a record is the metadata
                            self.update_status("Data transfer in progress....")
                            sequence = ser.readline().decode()[:-1]
                            if sequence != "" and sequence[0] != '>':       # Ensures that next piece of data is DNA sequence
                                file.write(bytesMessage + "\n")
                                file.write(sequence + "\n")
                                whiteline = ser.readline().decode()[:-1]
                                if whiteline == "":     # Every third line should be a blankspace
                                    file.write("\n")
                                else:
                                    self.update_status("Error, line should have been a whiteline...")
                                    return
                                
                                sequenceNum += 1        # A record has successfully been written, increment SequenceNum
                                if sequenceNum == backend.recordsPerFile:     # When backend.recordsPerFile records have been written, close file and start another one
                                    file.close()
                                    fileCounter += 1
                                    file = open(self.destination_folder + "/" + curTime + "_file" + str(fileCounter) + ".fn", "w")
                                    sequenceNum = 0
                            else:
                                self.update_status("Error, line should have been a dna sequence...")
                                return
                        elif bytesMessage != "":        # If data is not a command, new record then it must be bad.
                            self.update_status("Error, Received bad line: " + bytesMessage)
                            return
                        elif bytesMessage == "" and self.currentStatus == "Data transfer in progress....":     # If no data is received when not paused must be EOF
                            stillReading = False
                            file.close()
                            self.update_status("Data transfer complete! Awaiting new action...")

                elif bytesMessage == 'connect' and self.destination_folder == "":
                    self.update_status("Error, must set folder before sending data.")
                                

                        
                time.sleep(.01)


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    # Added to avoid runtime warnings
    app.setOrganizationName("Some Company")
    app.setOrganizationDomain("somecompany.com")
    app.setApplicationName("Amazing Application")

    engine = QQmlApplicationEngine()

    # Load QML file
    engine.load('main.qml')
    engine.quit.connect(app.quit)

    # Get QML File context
    backend = Backend()
    engine.rootObjects()[0].setProperty('backend', backend)

    backend.update_status("Awaiting Connection")
    thread = threading.Thread(target=backend.readSerial, args=())
    thread.start()
    #backend.readSerial(ser)

    sys.exit(app.exec_())

