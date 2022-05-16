import sys
import time
import threading
import argparse

from datetime import datetime
import serial
import gui


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='mGRUE-driver',
                                     description='Initialize the mGRUE Host Device Driver')
    parser.version = '1.0'

    gui.init(500)

    