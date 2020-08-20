# Copyright © 2018 Naturalpoint
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# OptiTrack NatNet direct depacketization library for Python 3.x

import socket
import struct
#import csv
import time
from threading import Thread
#import tensorflow as tf
#import keras as ks
from tensorflow.python.keras.models import load_model
#from keras.backend.tensorflow_backend import set_session
import numpy as np

def trace(*args):
    # print( "".join(map(str,args)) )
    pass

def trace2(*args):
    # print( "".join(map(str,args)))
    pass

# Create structs for reading various object types to speed up parsing.
Vector3 = struct.Struct('<fff')
Quaternion = struct.Struct('<ffff')
FloatValue = struct.Struct('<f')
DoubleValue = struct.Struct('<d')


class NatNetClient:
    def __init__(self):
        # Change this value to the IP address of the NatNet server.
        # 132.199.129.200
        self.serverIPAddress = "132.199.129.200"

        # Change this value to the IP address of your local network interface
        # 132.199.133.85
        self.localIPAddress = "192.168.178.27"

        # Should fetch the right address. Otherwise hardcode it like above
        # self.localIPAddress = socket.gethostbyname(socket.gethostname())


        self.localInterceptPort = 1511


        # This should match the multicast address listed in Motive's streaming settings.
        # 239.255.42.99
        self.multicastAddress = "239.255.42.99"

        # NatNet Command channel
        self.commandPort = 1510

        # NatNet Data channel     
        self.dataPort = 8203

        # Intercept IP Address
        self.outgoingTargetIpAddress = "132.199.133.85"

        # Intercept Target Port
        self.outgoingTargetPort = 1511

        # Set this to a callback method of your choice to receive per-rigid-body data at each frame.
        self.rigidBodyListener = None

        # NatNet stream version. This will be updated to the actual version the server is using during initialization.
        self.__natNetStreamVersion = (3, 0, 0, 0)

        # Create a separate thread for loading models
        #self.preloadModelsThread = Thread(target=self.loadModels, args=())

        # Model Array
        self.modelNames = ["Joints12F","Joints15F","Joints20F","Joints25F","Joints50F","Joints100F"]
        self.models = {}

        # Prediction
        self.predictFingers = False
        self.interceptionStatus = False
        self.dataFrameForPredictionBody = []
        self.dataFrameForPredictionFingers = []
        self.activePredictionModelIndex = 0




    # Client/server message ids
    NAT_PING = 0
    NAT_PINGRESPONSE = 1
    NAT_REQUEST = 2
    NAT_RESPONSE = 3
    NAT_REQUEST_MODELDEF = 4
    NAT_MODELDEF = 5
    NAT_REQUEST_FRAMEOFDATA = 6
    NAT_FRAMEOFDATA = 7
    NAT_MESSAGESTRING = 8
    NAT_DISCONNECT = 9
    NAT_UNRECOGNIZED_REQUEST = 100

    def setServerIpAndPort(self, ip, port):
        self.serverIPAddress = ip
        self.dataPort = int(port)

    def setTargetIpAndPort(self, ip, port):
        self.outgoingTargetIpAddress = ip

        if(port != ""):
            self.outgoingTargetPort = int(port)

    def setMulticastAddress(self, ip):
        self.multicastAddress = ip

    def setLocalIpAddress(self, ip):
        self.localIPAddress = ip
        print("Local IP Address entered: ", self.localIPAddress)

    def __createSocketForRedir(self, port):
        result = socket.socket(socket.AF_INET,
                               socket.SOCK_DGRAM,
                               socket.IPPROTO_UDP)
        result.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.multicastAddress) + socket.inet_aton(self.localIPAddress))
        result.bind((self.localIPAddress, port))

        return result

    # Create a data socket to attach to the NatNet stream
    def __createDataSocket(self, port):

        result = socket.socket(socket.AF_INET,  # Internet
                               socket.SOCK_DGRAM,
                               socket.IPPROTO_UDP)  # UDP

        result.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.multicastAddress) + socket.inet_aton(self.localIPAddress))

        result.bind((self.localIPAddress, port))

        return result

    # Create a command socket to attach to the NatNet stream
    def __createCommandSocket(self):

        result = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        result.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result.bind(('', 0))
        result.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        return result

    # Unpack a rigid body object from a data packet
    def __unpackRigidBody(self, data, rigidBodyId):

        offset = 0

        # ID (4 bytes)
        id = int.from_bytes(data[offset:offset + 4], byteorder='little')
        offset += 4

        # Position and orientation
        pos = Vector3.unpack(data[offset:offset + 12])
        offset += 12

        rot = Quaternion.unpack(data[offset:offset + 16])
        offset += 16

        if(rigidBodyId == 0):
            self.dataFrameForPredictionBody.append(pos[0])
            self.dataFrameForPredictionBody.append(pos[1])
            self.dataFrameForPredictionBody.append(pos[2])
            self.dataFrameForPredictionBody.append(rot[0])
            self.dataFrameForPredictionBody.append(rot[1])
            self.dataFrameForPredictionBody.append(rot[2])
            self.dataFrameForPredictionBody.append(rot[3])

        elif(rigidBodyId >=1 and rigidBodyId <=20):
            self.dataFrameForPredictionBody.append(rot[0])
            self.dataFrameForPredictionBody.append(rot[1])
            self.dataFrameForPredictionBody.append(rot[2])
            self.dataFrameForPredictionBody.append(rot[3])

        elif(rigidBodyId >=21 and rigidBodyId < 51):
            self.dataFrameForPredictionFingers.append(rot[0])
            self.dataFrameForPredictionFingers.append(rot[1])
            self.dataFrameForPredictionFingers.append(rot[2])
            self.dataFrameForPredictionFingers.append(rot[3])


        # Send information to any listener.
        if self.rigidBodyListener is not None:
            self.rigidBodyListener(id, pos, rot)

        if (self.__natNetStreamVersion[0] >= 2):
            markerError, = FloatValue.unpack(data[offset:offset + 4])
            offset += 4
            trace("\tMarker Error:", markerError)

        # Version 2.6 and later
        if (((self.__natNetStreamVersion[0] == 2) and (self.__natNetStreamVersion[1] >= 6)) or
                self.__natNetStreamVersion[0] > 2 or self.__natNetStreamVersion[0] == 0):
            param, = struct.unpack('h', data[offset:offset + 2])
            trackingValid = (param & 0x01) != 0
            offset += 2
            trace("\tTracking Valid:", 'True' if trackingValid else 'False')
        return offset

    def __replaceRigidbody(self, data, rigidBodyId, fingercount, prediction, predictionFingers):

        offset = 0

        ## Adding ID
        offset += 4

        ## Real Data Pos
        #dataPosVector = Vector3.unpack(data[offset:offset + 12])

        # offset += 12
        #print("Pos:", dataPosVector[0], dataPosVector[1], dataPosVector[2])

        ## Real Data Quat
        #dataQuatVector = Quaternion.unpack(data[offset+12:offset + 28])

        # offset += 16
        #print("Quat:", dataQuatVector[0], dataQuatVector[1], dataQuatVector[2], dataQuatVector[3])

        ## Set Pos = 0
        #posZero = Vector3.pack(dataPosVector[0], dataPosVector[1], dataPosVector[2])


        # Hip
        if (rigidBodyId == 0):
            #print(rigidBodyId, " Hip")
            #predInput = pd.DataFrame([[dataPosVector[0],dataPosVector[1],dataPosVector[2],dataQuatVector[0], dataQuatVector[1], dataQuatVector[2], dataQuatVector[3]]])
            #prediction = self.models[rigidBodyId].predict(predInput.iloc[0:1])
            #prediction = prediction[0]
            posVectorNew = Vector3.pack(prediction[0], prediction[1], prediction[2])
            rotVectorNew = Quaternion.pack(prediction[3], prediction[4], prediction[5], prediction[6])


            ## Create new Data Slice
            newDataSlice = b''.join(
                [data[offset - 4:offset],           # RB ID
                 posVectorNew,            # RB Pos
                 rotVectorNew,     # RB Quat
                 data[offset + 28: offset + 32],  # Marker Error
                 data[offset + 32:offset + 34]])  # RB Tracking Valid

        # Body
        elif (rigidBodyId >= 1 and rigidBodyId <= 20):
            #print(rigidBodyId, " Body")
            #predInput = pd.DataFrame([[dataQuatVector[0], dataQuatVector[1], dataQuatVector[2], dataQuatVector[3]]])
            #prediction = self.models[rigidBodyId].predict(predInput.iloc[0:1])
            rotVectorNew = Quaternion.pack(prediction[rigidBodyId*4+3], prediction[rigidBodyId*4+4], prediction[rigidBodyId*4+5], prediction[rigidBodyId*4+6])
            #posVectorNew = Vector3.pack(0, 0, 0)

            ## Create new Data Slice
            newDataSlice = b''.join(
                [data[offset - 4:offset],  # RB ID
                 data[offset:offset + 12],  # RB Pos
                 rotVectorNew,  # RB Quat
                 data[offset+ 28: offset + 32], # Marker Error
                 data[offset + 32:offset + 34]])  # RB Tracking Valid

        # Fingers
        else:
            posVectorNew = Vector3.pack(0, 0, 0)

            if(self.predictFingers == True):
                #print(rigidBodyId, " Fingers predicted")

                rotVectorNew = Quaternion.pack(predictionFingers[fingercount * 4 + 0], predictionFingers[fingercount * 4 + 1],predictionFingers[fingercount * 4 + 2], predictionFingers[fingercount * 4 + 3])

                ## Create new Data Slice
                newDataSlice = b''.join(
                    [data[offset - 4:offset],  # RB ID
                     data[offset:offset + 12],  # RB Pos
                     #data[offset + 12:offset + 28],  # RB Quat
                     rotVectorNew,
                     data[offset + 28: offset + 32],  # Marker Error
                     data[offset + 32:offset + 34]])  # RB Tracking Valid
            else:
                #print(rigidBodyId, " Fingers unpredicted")
                # Create new Data Slice
                newDataSlice = b''.join(
                    [data[offset - 4:offset],  # RB ID
                     data[offset:offset + 12],  # RB Pos
                     data[offset + 12:offset + 28],  # RB Quat
                     data[offset + 28: offset + 32],  # Marker Error
                     data[offset + 32:offset + 34]])  # RB Tracking Valid

        return newDataSlice


    # Unpack a skeleton object from a data packet
    def __unpackSkeleton(self, data, dataFull, offsetTotal):
        self.dataFrameForPredictionBody = []
        self.dataFrameForPredictionFingers = []
        offset = 0
        offsetUnpack = 0

        id = int.from_bytes(data[offset:offset + 4], byteorder='little')
        offset += 4
        offsetUnpack += 4
        trace("ID:", id)

        rigidBodyCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
        offset += 4
        offsetUnpack += 4
        trace("Rigid Body Count:", rigidBodyCount)

        dataSkeletonBeforeRigid = data[:offset]
        dataSliceRigidbodies = b""

        for j in range(0, rigidBodyCount):
            offsetUnpack += self.__unpackRigidBody(data[offsetUnpack:], j)

        start_time = time.time_ns()
        npArrayBody = np.array([self.dataFrameForPredictionBody])
        framePredictionBody = self.models[self.activePredictionModelIndex].predict(npArrayBody)[0]
        framePredictionFingers = []

        if(self.predictFingers == True):
            npArrayFingers = np.array([self.dataFrameForPredictionFingers])
            framePredictionFingers = self.models[6].predict(npArrayFingers)[0]

        end_time = time.time_ns()
        #print(end_time - start_time)

        for j in range(0, rigidBodyCount):
            fingercount = 0

            dataSliceRigidbodies = b"".join([dataSliceRigidbodies, self.__replaceRigidbody(data[offset:], j, fingercount,  framePredictionBody, framePredictionFingers)])
            offset += 38

            if(self.predictFingers == True and rigidBodyCount >=21):
                fingercount += 1



        dataSliceNew = b"".join([dataSkeletonBeforeRigid, dataSliceRigidbodies])

        return offset, dataSliceNew

    # Unpack data from a motion capture frame message
    def __unpackMocapData(self, dataFull, offset):
        if (self.interceptionStatus == False):
            if(self.redirSocket is None):
                'no socket'
                pass
            else:
                self.redirSocket.sendto(dataFull, (self.outgoingTargetIpAddress, self.outgoingTargetPort))

        else:

            offsetTotal = offset

            data = dataFull[offset:]

            trace("Begin MoCap Frame\n-----------------\n")

            offset = 0

            # Frame number (4 bytes)
            frameNumber = int.from_bytes(data[offset:offset + 4], byteorder='little')
            offset += 4
            trace("Frame #:", frameNumber)

            # Marker set count (4 bytes)
            markerSetCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
            offset += 4
            trace("Marker Set Count:", markerSetCount)

            for i in range(0, markerSetCount):
                # Model name
                modelName, separator, remainder = bytes(data[offset:]).partition(b'\0')
                offset += len(modelName) + 1
                trace("Model Name:", modelName.decode('utf-8'))

                # Marker count (4 bytes)
                markerCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
                offset += 4
                trace("Marker Count:", markerCount)

                for j in range(0, markerCount):
                    pos = Vector3.unpack(data[offset:offset + 12])
                    offset += 12
                    # trace( "\tMarker", j, ":", pos[0],",", pos[1],",", pos[2] )

            # Unlabeled markers count (4 bytes)
            unlabeledMarkersCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
            offset += 4
            trace("Unlabeled Markers Count:", unlabeledMarkersCount)

            for i in range(0, unlabeledMarkersCount):
                pos = Vector3.unpack(data[offset:offset + 12])
                offset += 12
                trace("\tMarker", i, ":", pos[0], ",", pos[1], ",", pos[2])

            # Rigid body count (4 bytes)
            rigidBodyCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
            offset += 4
            trace("Rigid Body Count:", rigidBodyCount)
            for i in range(0, rigidBodyCount):
                offset += self.__unpackRigidBody(data[offset:], i)

            # Version 2.1 and later
            skeletonCount = 0
            if ((self.__natNetStreamVersion[0] == 2 and self.__natNetStreamVersion[1] > 0) or self.__natNetStreamVersion[
                0] > 2):
                skeletonCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
                offset += 4
                trace("Skeleton Count:", skeletonCount)
                offsetTotal += offset

                dataFramePreSkeleton = dataFull[:offsetTotal]

                for i in range(0, skeletonCount):
                    offsetChange, dataSliceNew = self.__unpackSkeleton(data[offset:], dataFull, offsetTotal)
                    offset += offsetChange
                    offsetTotal += offsetChange

                dataFrameAfterSkeleton = dataFull[offsetTotal:]

                dataFrameNew = b"".join([dataFramePreSkeleton, dataSliceNew, dataFrameAfterSkeleton])
                self.redirSocket.sendto(dataFrameNew, (self.outgoingTargetIpAddress, self.outgoingTargetPort))


    # Unpack a marker set description packet
    def __unpackMarkerSetDescription(self, data):
        offset = 0

        name, separator, remainder = bytes(data[offset:]).partition(b'\0')
        offset += len(name) + 1
        trace("Markerset Name:", name.decode('utf-8'))

        markerCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
        offset += 4

        for i in range(0, markerCount):
            name, separator, remainder = bytes(data[offset:]).partition(b'\0')
            offset += len(name) + 1
            trace("\tMarker Name:", name.decode('utf-8'))

        return offset

    # Unpack a rigid body description packet
    def __unpackRigidBodyDescription(self, data):
        offset = 0

        # Version 2.0 or higher
        if (self.__natNetStreamVersion[0] >= 2):
            name, separator, remainder = bytes(data[offset:]).partition(b'\0')
            offset += len(name) + 1
            trace("\tRigidBody Name:", name.decode('utf-8'))

        id = int.from_bytes(data[offset:offset + 4], byteorder='little')
        offset += 4

        parentID = int.from_bytes(data[offset:offset + 4], byteorder='little')
        offset += 4

        timestamp = Vector3.unpack(data[offset:offset + 12])
        offset += 12

        # Version 3.0 and higher, rigid body marker information contained in description
        if (self.__natNetStreamVersion[0] >= 3 or self.__natNetStreamVersion[0] == 0):
            markerCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
            offset += 4
            trace("\tRigidBody Marker Count:", markerCount)

            markerCountRange = range(0, markerCount)
            for marker in markerCountRange:
                markerOffset = Vector3.unpack(data[offset:offset + 12])
                offset += 12
            for marker in markerCountRange:
                activeLabel = int.from_bytes(data[offset:offset + 4], byteorder='little')
                offset += 4

        return offset

    # Unpack a skeleton description packet
    def __unpackSkeletonDescription(self, data):

        offset = 0

        name, separator, remainder = bytes(data[offset:]).partition(b'\0')
        offset += len(name) + 1
        trace("\tMarker Name:", name.decode('utf-8'))
        trace2("\tMarker Name:", name.decode('utf-8'))

        id = int.from_bytes(data[offset:offset + 4], byteorder='little')
        trace2(id)
        offset += 4

        rigidBodyCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
        trace2(rigidBodyCount)
        offset += 4

        for i in range(0, rigidBodyCount):
            offset += self.__unpackRigidBodyDescription(data[offset:])

        return offset

    # Unpack a data description packet
    def __unpackDataDescriptions(self, data, socket):

        #socket.sendto(data, (self.outgoingTargetIpAddress, self.commandPort))

        offset = 0
        datasetCount = int.from_bytes(data[offset:offset + 4], byteorder='little')
        offset += 4

        for i in range(0, datasetCount):
            type = int.from_bytes(data[offset:offset + 4], byteorder='little')
            offset += 4
            if (type == 0):
                offset += self.__unpackMarkerSetDescription(data[offset:])
            elif (type == 1):
                offset += self.__unpackRigidBodyDescription(data[offset:])
            elif (type == 2):
                offset += self.__unpackSkeletonDescription(data[offset:])

        self.streamConnectionListener(True)

    def __dataThreadFunction(self, socket, stopThread):
        self.loadModels()
        while True:
            # Block for input
            start_time = time.time_ns()
            data, addr = socket.recvfrom(32768)  # 32k byte buffer size
            if (len(data) > 0):
                self.__processMessage(data)
            end_time = time.time_ns()
            #print(end_time - start_time)
            if stopThread == True:
                break

    def __processMessage(self, data):
        trace("Begin Packet\n------------\n")

        messageID = int.from_bytes(data[0:2], byteorder='little')
        trace("Message ID:", messageID)
        packetSize = int.from_bytes(data[2:4], byteorder='little')
        trace("Packet Size:", packetSize)

        offset = 4
        if (messageID == self.NAT_FRAMEOFDATA):
            self.__unpackMocapData(data, offset)
        else:
            self.redirSocket.sendto(data, (self.outgoingTargetIpAddress, self.outgoingTargetPort))

        trace("End Packet\n----------\n")

    def sendCommand(self, command, commandStr, socket, address):
        # Compose the message in our known message format
        if (command == self.NAT_REQUEST_MODELDEF or command == self.NAT_REQUEST_FRAMEOFDATA):
            packetSize = 0
            commandStr = ""
        elif (command == self.NAT_REQUEST):
            packetSize = len(commandStr) + 1
        elif (command == self.NAT_PING):
            commandStr = "Ping"
            packetSize = len(commandStr) + 1

        data = command.to_bytes(2, byteorder='little')
        data += packetSize.to_bytes(2, byteorder='little')

        data += commandStr.encode('utf-8')
        data += b'\0'

        socket.sendto(data, address)

    def setStreamConnectionListener(self, listener):
        self.streamConnectionListener = listener

    def setStreamInterceptListener(self, listener):
        self.streamInterceptListener = listener

    def setModelLoadUpListener(self, listener):
        self.modelLoadUpListener = listener

    def setPredictionModeListener(self, listener):
        self.predictionModeListener = listener

    def setPredictionModel(self, index):
        self.activePredictionModelIndex = index
        print("Set Prediction Model to ", self.modelNames[index])

    # Intercept data stream?
    def setInterceptStatus(self, status):
        self.interceptionStatus = status
        self.streamInterceptListener(status)

        if(self.interceptionStatus == True):
            print("Start Intercepting Data")
        if(self.interceptionStatus == False):
            print("Stop Intercepting Data")

    # Predict Fingers?
    def setPredictionMode(self, status):
        self.predictFingers = status
        self.predictionModeListener(status)

        if (self.predictFingers == True):
            print("Start Predicting Fingers")
        if (self.predictFingers == False):
            print("Stop Predicting Fingers")

    def startLoadModelsThread(self):
        pass
        #self.loadModels()
        #self.preloadModelsThread.start()

    def loadModels(self):
        modelCount = len(self.modelNames)

        for i in range(0, modelCount):
            self.models[i] = load_model(r"model/"+self.modelNames[i])
            self.modelLoadUpListener("" + str(i + 1) + " / " + str(modelCount))

        self.models[6] = load_model(r"model/FingersUnscaled")
        self.modelLoadUpListener(-1)
        #for x in range(0,25):
        #    self.models[x] = load_model(r"model/"+str(x+1)+"")
        #    self.models[x]._make_predict_function()
        #    self.modelLoadUpListener(str(x+1) +" / " "25")

    def getModelNames(self):
        return self.modelNames

    def run(self):

        # Create the data socket
        self.dataSocket = self.__createDataSocket(self.dataPort)
        if (self.dataSocket is None):
            print("Could not open data channel")
            exit

        '''
        # Create the command socket
        self.commandSocket = self.__createCommandSocket()
        if (self.commandSocket is None):
            print("Could not open command channel")
            exit
        '''


        self.redirSocket = self.__createSocketForRedir(self.localInterceptPort)
        if (self.redirSocket is None):
            print("Could not open redir channel")
            exit

        # Create a separate thread for receiving data packets
        self.stopDataThread = False
        self.dataThread = Thread(target=self.__dataThreadFunction, args=(self.dataSocket, lambda : self.stopDataThread))
        self.dataThread.start()

        '''
        # Create a separate thread for receiving command packets
        commandThread = Thread(target=self.__dataThreadFunction, args=(self.commandSocket,))
        commandThread.start()

        self.sendCommand(self.NAT_REQUEST_MODELDEF, "", self.commandSocket,
                         (self.serverIPAddress, self.commandPort))
        '''

        print("NatNet Streaming Client loaded! Listening on Server and Transfering to Client.")
        print("From: ", self.serverIPAddress, ":", self.dataPort)
        print("To: ", self.outgoingTargetIpAddress, ":", self.outgoingTargetPort)

    def stop(self):
        self.stopDataThread = True







