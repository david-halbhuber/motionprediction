import serial, time, datetime
import matplotlib.pyplot as plt
import statistics
# CONSTANTS
COM_PORT = "COM3"
BUD_RATE = 115200
TIMEOUT = .1
SETTLEMENT = 2
TESTCOUNT = 10

# VARIABLES

listOfLatencies = []






def connect(COM_PORT, BUD_RATE, TIMEOUT, SETTLEMENT):
    try:
        arduino = serial.Serial(COM_PORT, BUD_RATE, timeout=TIMEOUT)
        print("Connected to Arduino on", COM_PORT,".")
        sentToArduino(arduino,"initString",SETTLEMENT)
    except:
        print("Connection to Arduino on", COM_PORT, " Aborted!")
        if(len(listOfLatencies)>0):
            plt.plot(listOfLatencies)
            plt.ylabel("Latency in ms")
            plt.xlabel("Number of measurements")
            plt.title("USB-Latency: Arduino/PC ")
            plt.axhline(statistics.mean(listOfLatencies), color='k', linestyle='dashed', linewidth=1)
            plt.show()
            print("Mean of measured latency: ", statistics.mean(listOfLatencies), "ms")

    return

def sentToArduino(arduino,initString,waitForSettlment):
    time.sleep(waitForSettlment)
    timeSent = datetime.datetime.now()
    #print("Sending at: ", timeSent)
    arduino.write(str.encode(initString))

    while True: 
        data = arduino.readline()
        if data: 
            timeReceived = datetime.datetime.now()
            #print("Received answer at: ", timeReceived)
            latency = timeReceived - timeSent
            listOfLatencies.append(latency.microseconds/1000/2)
            print("Current latency: ", latency.microseconds/1000/2, "ms.")
            break
    sentToArduino(arduino,"initString",SETTLEMENT)   
    
    return

connect(COM_PORT, BUD_RATE, TIMEOUT, SETTLEMENT)
   