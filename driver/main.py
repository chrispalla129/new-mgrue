import sys
import time
import threading
import argparse

from datetime import datetime
import serial
import gui


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='mGRUE-driver', description='Initialize the mGRUE Host Device Driver')
    parser.version = '1.0'
    parser.add_argument('mode',
                        choices=['gui', 'cli'],
                        help='option to use program through a GUI or via Command Line')
    parser.add_argument('-r',
                        '--records',
                        type=int,
                        nargs='?',
                        default=500,
                        help='the number of records per file. Default 500')
    args = parser.parse_args()

    recordsPerFile = args.records

    if(args.mode == 'gui'):
        gui.init(recordsPerFile)

    else:
        destinationFolder = input('Please enter your desired file location:')
        print("File Destination Path: " + destinationFolder)
        currentStatus = ""
        with serial.Serial('/dev/pts/3', 256000, timeout=1) as ser:
            while (True):
                stillReading    = True
                curTime         = datetime.now().strftime("%H-%M-%S")
                sequenceNum     = 0
                fileCounter     = 0
                bytesMessage    = ser.readline().decode()[:-1]     # read a '\n' terminated line, removing the \n

                if bytesMessage == 'connect' and destinationFolder != "":
                    ser.write(b'handshake')
                    currentStatus = "Device Connected"
                    print(currentStatus)
                    file = open(destinationFolder + "/" + curTime + "_file" + str(fileCounter) + ".fn", "w")

                    while (stillReading or currentStatus == "Paused."):       # Run while file is still being read or the reading is paused.
                        bytesMessage = ser.readline().decode()[:-1]     # This should either be the start of a record, a new_rate command, or EOF

                        if bytesMessage == 'new_rate' and currentStatus == "Paused.":     # Only update rate when paused.
                            newBaud = ser.readline().decode()
                            currentStatus = "Baud rate updated to " + newBaud
                            print(currentStatus)
                            ser.setBaudrate(newBaud)
                        elif bytesMessage == 'pause':       # Pauses the transfer for a baud rate change
                            currentStatus = "Paused."
                            print(currentStatus)
                        elif bytesMessage != "" and bytesMessage[0] == '>':     # Ensures that the first piece of data of a record is the metadata
                            
                            currentStatus = "Data transfer in progress...."
                            print(currentStatus)
                            sequence = ser.readline().decode()[:-1]
                            if sequence != "" and sequence[0] != '>':       # Ensures that next piece of data is DNA sequence
                                file.write(bytesMessage + "\n")
                                file.write(sequence + "\n")
                                whiteline = ser.readline().decode()[:-1]
                                if whiteline == "":     # Every third line should be a blankspace
                                    file.write("\n")
                                else:
                                    currentStatus = "Error, line should have been a whiteline..."
                                    print(currentStatus)
                                    break
                                
                                sequenceNum += 1        # A record has successfully been written, increment SequenceNum
                                if sequenceNum == recordsPerFile:     # When backend.recordsPerFile records have been written, close file and start another one
                                    file.close()
                                    fileCounter += 1
                                    file = open(destinationFolder + "/" + curTime + "_file" + str(fileCounter) + ".fn", "w")
                                    sequenceNum = 0
                            else:
                                currentStatus = "Error, line should have been a dna sequence..."
                                print(currentStatus)
                                break
                        elif bytesMessage != "":        # If data is not a command, new record then it must be bad.
                            currentStatus = "Error, Received bad line: " + bytesMessage
                            print(currentStatus)
                            break
                        elif bytesMessage == "" and currentStatus == "Data transfer in progress....":     # If no data is received when not paused must be EOF
                            stillReading = False
                            file.close()
                            currentStatus = "Data transfer complete! Awaiting new action..."
                            print(currentStatus)

                elif bytesMessage == 'connect' and destinationFolder == "":
                    currentStatus = "Error, must set folder before sending data."
                    print(currentStatus)
                                

                        
                time.sleep(.01)
    
