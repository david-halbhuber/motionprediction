from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFrame)
from PyQt5.QtGui import QColor, QPalette

from NatNetClient import NatNetClient

import sys

class WidgetGallery(QDialog):

    serverIpAddress = "132.199.129.200"
    serverPort = "8205"

    targetIpAddress = "132.199.129.176"
    targetPort = "1511"

    localIpAddress = "132.199.129.200"

    multicastAddress = "239.255.42.99"

    streamStatus = False
    interceptStatus = False
    predictionMode = False



    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.initStreamingClient()

        self.createFirstGroupBox()
        self.createSecondGroupBox()
        self.createThirdGroupBox()
        self.createFourthGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.firstGroupBox, 1, 0)
        mainLayout.addWidget(self.secondGroupBox, 2, 0)
        mainLayout.addWidget(self.thirdGroupBox, 3, 0)
        mainLayout.addWidget(self.fourthGroupBox, 4, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setRowStretch(3, 1)
        mainLayout.setRowStretch(4, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("PS19 Client")

    def initStreamingClient(self):

        # This will create a new NatNet client
        self.streamingClient = NatNetClient()

        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.
        # streamingClient.run()

        self.streamingClient.setStreamConnectionListener(self.onStreamConnectionChanged)
        self.streamingClient.setStreamInterceptListener(self.onInterceptionChanged)
        self.streamingClient.setModelLoadUpListener(self.updateModelLoadUp)
        self.streamingClient.setPredictionModeListener(self.onPredictionModeChanged)


    def createFirstGroupBox(self):

        self.firstGroupBox = QGroupBox("Stream")

        serverIpLabel = QLabel("Server IP")
        serverPortLabel = QLabel("Server Port")
        multicastLabel = QLabel("Multicast Addr")
        localIpLabel = QLabel("Local IP Addr")

        self.serverIpLineEdit = QLineEdit(self.serverIpAddress)
        self.serverPortLineEdit = QLineEdit(self.serverPort)
        self.multicastLineEdit = QLineEdit(self.multicastAddress)
        self.localIpAddressEdit = QLineEdit(self.localIpAddress)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)

        sep.setContentsMargins(10, 100, 10, 100)
        sep2.setContentsMargins(10, 100, 10, 100)

        targetIpLabel = QLabel("Target IP")
        targetPortLabel = QLabel("Target Port")

        self.targetIpLineEdit = QLineEdit(self.targetIpAddress)
        self.targetPortLineEdit = QLineEdit(self.targetPort)

        streamStatusLabel = QLabel("Status")

        self.radioButtonStreamConnected = QRadioButton("Connected")
        self.radioButtonStreamDisconnected = QRadioButton("Disconnected")
        self.radioButtonStreamConnected.setEnabled(False)
        self.radioButtonStreamDisconnected.setEnabled(False)
        self.radioButtonStreamDisconnected.setChecked(True)

        toggleStreamButton = QPushButton("Toggle Stream")
        toggleStreamButton.clicked.connect(self.toggleStream)
        toggleStreamButton.setCheckable(True)
        toggleStreamButton.setChecked(False)

        layout = QGridLayout()

        layout.addWidget(serverIpLabel, 0, 0, 1, 1)
        layout.addWidget(self.serverIpLineEdit, 0, 1, 1, 1)
        layout.addWidget(serverPortLabel, 1, 0, 1, 1)
        layout.addWidget(self.serverPortLineEdit, 1, 1, 1, 1)

        layout.addWidget(multicastLabel, 2, 0, 1, 1)
        layout.addWidget(self.multicastLineEdit, 2, 1, 1, 1)

        layout.addWidget(localIpLabel, 3, 0, 1, 1)
        layout.addWidget(self.localIpAddressEdit, 3, 1, 1, 1)

        layout.addWidget(sep, 4, 0, 1, 2)

        layout.addWidget(targetIpLabel, 5, 0, 1, 1)
        layout.addWidget(self.targetIpLineEdit, 5, 1, 1, 1)
        layout.addWidget(targetPortLabel, 6, 0, 1, 1)
        layout.addWidget(self.targetPortLineEdit, 6, 1, 1, 1)

        layout.addWidget(sep2, 7, 0, 1, 2)

        layout.addWidget(streamStatusLabel, 8, 0, 2, 1)
        layout.addWidget(self.radioButtonStreamConnected, 8, 1, 1, 1)
        layout.addWidget(self.radioButtonStreamDisconnected, 9, 1, 1, 1)
        layout.addWidget(toggleStreamButton, 10, 0, 1, 2)

        layout.setRowStretch(7, 1)

        self.firstGroupBox.setLayout(layout)

    def createSecondGroupBox(self):
        self.secondGroupBox = QGroupBox("")

        modelsLoadUpProgressLabel = QLabel("Models loaded:")

        self.modelsLoadUpProgress = QLabel("")

        layout = QGridLayout()

        layout.addWidget(modelsLoadUpProgressLabel, 0, 0, 1, 1)
        layout.addWidget(self.modelsLoadUpProgress, 0, 1, 1, 1)

        self.secondGroupBox.setLayout(layout)

    def createThirdGroupBox(self):
        self.thirdGroupBox = QGroupBox("Intercept")

        interceptStatusLabel = QLabel("Status")

        self.radioButtonInterceptEnabled = QRadioButton("Enabled")
        self.radioButtonInterceptDisabled = QRadioButton("Disabld")
        self.radioButtonInterceptEnabled.setEnabled(False)
        self.radioButtonInterceptDisabled.setEnabled(False)
        self.radioButtonInterceptDisabled.setChecked(True)

        toggleInterception = QPushButton("Toggle Intercept")
        toggleInterception.clicked.connect(self.toggleIntercept)
        toggleInterception.setCheckable(True)
        toggleInterception.setChecked(False)

        modelDropdownLabel = QLabel("Prediction Model: ")

        modelDropdown = QComboBox()
        modelDropdown.addItems(self.streamingClient.getModelNames())
        modelDropdown.currentIndexChanged.connect(self.predictionModelChanged)

        layout = QGridLayout()

        layout.addWidget(modelDropdownLabel, 1, 0, 1, 1)
        layout.addWidget(modelDropdown, 1, 1, 1, 1)

        layout.addWidget(interceptStatusLabel, 2, 0, 2, 1)

        layout.addWidget(self.radioButtonInterceptEnabled, 2, 1, 1, 1)
        layout.addWidget(self.radioButtonInterceptDisabled, 3, 1, 1, 1)

        layout.addWidget(toggleInterception, 4, 0, 1, 2)
        layout.setRowStretch(5, 1)

        self.thirdGroupBox.setLayout(layout)
        self.thirdGroupBox.setEnabled(False)

    def createFourthGroupBox(self):
        self.fourthGroupBox = QGroupBox("Prediction Mode")

        predictionModeStatusLabel = QLabel("Status")

        self.radioButtonFingersEnabled = QRadioButton("Enabled")
        self.radioButtonFingersDisabled = QRadioButton("Disabld")
        self.radioButtonFingersEnabled.setEnabled(False)
        self.radioButtonFingersDisabled.setEnabled(False)
        self.radioButtonFingersDisabled.setChecked(True)

        togglePredictionMode = QPushButton("Toggle Fingers")
        togglePredictionMode.clicked.connect(self.togglePredictionMode)
        togglePredictionMode.setCheckable(True)
        togglePredictionMode.setChecked(False)

        layout = QGridLayout()

        layout.addWidget(predictionModeStatusLabel, 2, 0, 2, 1)

        layout.addWidget(self.radioButtonFingersEnabled, 2, 1, 1, 1)
        layout.addWidget(self.radioButtonFingersDisabled, 3, 1, 1, 1)

        layout.addWidget(togglePredictionMode, 4, 0, 1, 2)
        layout.setRowStretch(5, 1)

        self.fourthGroupBox.setLayout(layout)
        self.fourthGroupBox.setEnabled(False)

    def toggleStreamEdits(self, status = None):
        self.serverIpLineEdit.setEnabled(status)
        self.serverPortLineEdit.setEnabled(status)
        self.multicastLineEdit.setEnabled(status)
        self.localIpAddressEdit.setEnabled(status)
        self.targetIpLineEdit.setEnabled(status)
        self.targetPortLineEdit.setEnabled(status)

    def onStreamConnectionChanged(self, status):
        if status == True:
            self.radioButtonStreamConnected.setChecked(True)
            self.radioButtonStreamDisconnected.setChecked(False)
            self.toggleStreamEdits(False)
        else:
            self.radioButtonStreamConnected.setChecked(False)
            self.radioButtonStreamDisconnected.setChecked(True)
            self.thirdGroupBox.setEnabled(False)
            self.fourthGroupBox.setEnabled(False)
            self.toggleStreamEdits(True)

    def onInterceptionChanged(self, status):
        if status == True:
            self.radioButtonInterceptEnabled.setChecked(True)
            self.radioButtonInterceptDisabled.setChecked(False)
            self.fourthGroupBox.setEnabled(True)
        else:
            self.radioButtonInterceptEnabled.setChecked(False)
            self.radioButtonInterceptDisabled.setChecked(True)
            self.fourthGroupBox.setEnabled(False)

    def onPredictionModeChanged(self, status):
        if status == True:
            self.radioButtonFingersEnabled.setChecked(True)
            self.radioButtonFingersDisabled.setChecked(False)
        else:
            self.radioButtonFingersEnabled.setChecked(False)
            self.radioButtonFingersDisabled.setChecked(True)

    def updateModelLoadUp(self, progress):
        if(progress == -1):
            self.modelsLoadUpProgress.setText("Finished loading!")
            self.thirdGroupBox.setEnabled(True)
        else:
            self.modelsLoadUpProgress.setText(progress)

    def predictionModelChanged(self, index):
        print(index)
        self.streamingClient.setPredictionModel(index)

    def toggleStream(self):
        self.streamStatus^=True

        # Start client
        if(self.streamStatus == True):

            # Set specs
            self.streamingClient.setServerIpAndPort(self.serverIpLineEdit.text(), self.serverPortLineEdit.text())
            self.streamingClient.setTargetIpAndPort(self.targetIpLineEdit.text(), self.targetPortLineEdit.text())
            self.streamingClient.setMulticastAddress(self.multicastLineEdit.text())
            self.streamingClient.setLocalIpAddress(self.localIpAddressEdit.text())
            self.onStreamConnectionChanged(True)
            self.streamingClient.run()

        # Stop client
        else:
            self.onStreamConnectionChanged(False)
            self.streamingClient.stop()
            self.interceptStatus = False
            self.streamingClient.setInterceptStatus(self.interceptStatus)
            self.predictionMode = False
            self.streamingClient.setPredictionMode(self.predictionMode)

    def togglePredictionMode(self):
        self.predictionMode ^= True
        self.streamingClient.setPredictionMode(self.predictionMode)

    def toggleIntercept(self):
        self.interceptStatus ^= True
        self.streamingClient.setInterceptStatus(self.interceptStatus)
        if( self.interceptStatus == False):
            self.predictionMode = False
            self.streamingClient.setPredictionMode(False)

    def natNetFinishedLoading(self):
        self.topRightGroupBox.setEnabled(True)



if __name__ == '__main__':

    app = QApplication([])
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())










