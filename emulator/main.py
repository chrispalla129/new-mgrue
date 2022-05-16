import sys
import time
import threading
import argparse

from datetime import datetime
import serial
import gui


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='mGRUE-device', description='Initialize the mGRUE Host Device Software')
    parser.version = '1.0'

    gui.init(500)

    