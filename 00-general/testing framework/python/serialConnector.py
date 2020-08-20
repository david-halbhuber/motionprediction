import serial
import datetime
import numpy as np
from numpy import savetxt

# Define Arduino consts here: 
COM_PORT = "COM3"
BUD_RATE = 9600
TIMEOUT = .1

# working Array



def connect(COM_PORT, BUD_RATE, TIMEOUT):
    # try:
    arduino = serial.Serial(COM_PORT, BUD_RATE, timeout=TIMEOUT)
    print("Connected to Arduino on", COM_PORT,".")
    receiveFromArduino(arduino)
    # except:
    #     print("Connection to Arduino on", COM_PORT, " Aborted!")
    return 


def receiveFromArduino (arduino):
    i = 0
    while i<1: 
        data = arduino.readline()[:-2]
        currentDate = datetime.datetime.now()
        if data:
            print ("Received Shock Alarm at: ",data)
            print ("Local system time: ", currentDate )
            x = np.array([data,currentDate])
            np.savetxt('test.txt', x, delimiter=",", fmt="%s")
            
          
        

    return 

# Uncomment this to start 
connect(COM_PORT, BUD_RATE, TIMEOUT)

