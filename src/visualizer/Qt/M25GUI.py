# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'M25_Widget2.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(685, 565)
        self.CapturePushButton = QtWidgets.QPushButton(Form)
        self.CapturePushButton.setGeometry(QtCore.QRect(10, 480, 75, 23))
        self.CapturePushButton.setObjectName("CapturePushButton")
        self.ConfButton = QtWidgets.QPushButton(Form)
        self.ConfButton.setGeometry(QtCore.QRect(210, 340, 75, 23))
        self.ConfButton.setObjectName("ConfButton")
        self.WritePLineEdit = QtWidgets.QLineEdit(Form)
        self.WritePLineEdit.setGeometry(QtCore.QRect(220, 50, 251, 20))
        self.WritePLineEdit.setObjectName("WritePLineEdit")
        self.ProjectNameLabel = QtWidgets.QLabel(Form)
        self.ProjectNameLabel.setGeometry(QtCore.QRect(310, 80, 101, 16))
        self.ProjectNameLabel.setObjectName("ProjectNameLabel")
        self.ZStackBox = QtWidgets.QCheckBox(Form)
        self.ZStackBox.setGeometry(QtCore.QRect(130, 160, 81, 31))
        self.ZStackBox.setObjectName("ZStackBox")
        self.WritePLlabel = QtWidgets.QLabel(Form)
        self.WritePLlabel.setGeometry(QtCore.QRect(300, 30, 171, 16))
        self.WritePLlabel.setObjectName("WritePLlabel")
        self.MsgLabel = QtWidgets.QLabel(Form)
        self.MsgLabel.setGeometry(QtCore.QRect(330, 430, 121, 16))
        self.MsgLabel.setObjectName("MsgLabel")
        self.StatusLineEdit = QtWidgets.QLineEdit(Form)
        self.StatusLineEdit.setGeometry(QtCore.QRect(10, 450, 113, 20))
        self.StatusLineEdit.setObjectName("StatusLineEdit")
        self.VertLineEdit = QtWidgets.QLineEdit(Form)
        self.VertLineEdit.setGeometry(QtCore.QRect(110, 50, 81, 20))
        self.VertLineEdit.setObjectName("VertLineEdit")
        self.SingleCamCheckBox = QtWidgets.QCheckBox(Form)
        self.SingleCamCheckBox.setGeometry(QtCore.QRect(200, 470, 121, 41))
        self.SingleCamCheckBox.setObjectName("SingleCamCheckBox")
        self.BPPLabel = QtWidgets.QLabel(Form)
        self.BPPLabel.setGeometry(QtCore.QRect(10, 130, 171, 16))
        self.BPPLabel.setObjectName("BPPLabel")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(10, 150, 131, 18))
        self.radioButton.setObjectName("radioButton")
        self.FPSLabel = QtWidgets.QLabel(Form)
        self.FPSLabel.setGeometry(QtCore.QRect(10, 80, 191, 16))
        self.FPSLabel.setObjectName("FPSLabel")
        self.GainlineEdit = QtWidgets.QLineEdit(Form)
        self.GainlineEdit.setGeometry(QtCore.QRect(130, 220, 113, 20))
        self.GainlineEdit.setObjectName("GainlineEdit")
        self.CapTimeLineEdit = QtWidgets.QLineEdit(Form)
        self.CapTimeLineEdit.setGeometry(QtCore.QRect(10, 300, 91, 20))
        self.CapTimeLineEdit.setObjectName("CapTimeLineEdit")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 170, 151, 18))
        self.radioButton_2.setObjectName("radioButton_2")
        self.ReleaseCamsButton = QtWidgets.QPushButton(Form)
        self.ReleaseCamsButton.setGeometry(QtCore.QRect(110, 340, 75, 23))
        self.ReleaseCamsButton.setObjectName("ReleaseCamsButton")
        self.CaptureLabel = QtWidgets.QLabel(Form)
        self.CaptureLabel.setGeometry(QtCore.QRect(10, 280, 181, 21))
        self.CaptureLabel.setObjectName("CaptureLabel")
        self.CamSelectLabel = QtWidgets.QLabel(Form)
        self.CamSelectLabel.setGeometry(QtCore.QRect(400, 480, 131, 16))
        self.CamSelectLabel.setObjectName("CamSelectLabel")
        self.StatusLabel = QtWidgets.QLabel(Form)
        self.StatusLabel.setGeometry(QtCore.QRect(10, 430, 111, 16))
        self.StatusLabel.setObjectName("StatusLabel")
        self.LiveButton = QtWidgets.QPushButton(Form)
        self.LiveButton.setGeometry(QtCore.QRect(110, 480, 75, 23))
        self.LiveButton.setObjectName("LiveButton")
        self.VertLabel = QtWidgets.QLabel(Form)
        self.VertLabel.setGeometry(QtCore.QRect(130, 30, 71, 20))
        self.VertLabel.setObjectName("VertLabel")
        self.ResolutionLabel = QtWidgets.QLabel(Form)
        self.ResolutionLabel.setGeometry(QtCore.QRect(70, 10, 81, 16))
        self.ResolutionLabel.setObjectName("ResolutionLabel")
        self.CaptureModeLabel = QtWidgets.QLabel(Form)
        self.CaptureModeLabel.setGeometry(QtCore.QRect(130, 140, 101, 16))
        self.CaptureModeLabel.setObjectName("CaptureModeLabel")
        self.GainLabel = QtWidgets.QLabel(Form)
        self.GainLabel.setGeometry(QtCore.QRect(130, 200, 61, 16))
        self.GainLabel.setObjectName("GainLabel")
        self.PNameLineEdit = QtWidgets.QLineEdit(Form)
        self.PNameLineEdit.setGeometry(QtCore.QRect(220, 100, 251, 20))
        self.PNameLineEdit.setObjectName("PNameLineEdit")
        self.HorzLabel = QtWidgets.QLabel(Form)
        self.HorzLabel.setGeometry(QtCore.QRect(20, 30, 71, 20))
        self.HorzLabel.setObjectName("HorzLabel")
        self.EXPLineEdit = QtWidgets.QLineEdit(Form)
        self.EXPLineEdit.setGeometry(QtCore.QRect(10, 220, 91, 20))
        self.EXPLineEdit.setObjectName("EXPLineEdit")
        self.EXPLabel = QtWidgets.QLabel(Form)
        self.EXPLabel.setGeometry(QtCore.QRect(10, 200, 151, 16))
        self.EXPLabel.setObjectName("EXPLabel")
        self.HorzLineEdit = QtWidgets.QLineEdit(Form)
        self.HorzLineEdit.setGeometry(QtCore.QRect(10, 50, 81, 20))
        self.HorzLineEdit.setObjectName("HorzLineEdit")
        self.StackFramesEdit = QtWidgets.QLineEdit(Form)
        self.StackFramesEdit.setGeometry(QtCore.QRect(260, 160, 113, 20))
        self.StackFramesEdit.setObjectName("StackFramesEdit")
        self.BrowsePushButton = QtWidgets.QPushButton(Form)
        self.BrowsePushButton.setGeometry(QtCore.QRect(480, 50, 75, 23))
        self.BrowsePushButton.setObjectName("BrowsePushButton")
        self.FPSLineEdit = QtWidgets.QLineEdit(Form)
        self.FPSLineEdit.setGeometry(QtCore.QRect(10, 100, 91, 20))
        self.FPSLineEdit.setObjectName("FPSLineEdit")
        self.StackFramesLabel = QtWidgets.QLabel(Form)
        self.StackFramesLabel.setGeometry(QtCore.QRect(260, 140, 241, 16))
        self.StackFramesLabel.setObjectName("StackFramesLabel")
        self.MsgLineEdit = QtWidgets.QLineEdit(Form)
        self.MsgLineEdit.setGeometry(QtCore.QRect(160, 450, 401, 20))
        self.MsgLineEdit.setObjectName("MsgLineEdit")
        self.CamSpinBox = QtWidgets.QSpinBox(Form)
        self.CamSpinBox.setGeometry(QtCore.QRect(350, 480, 42, 22))
        self.CamSpinBox.setObjectName("CamSpinBox")
        self.AcquireCamsButton = QtWidgets.QPushButton(Form)
        self.AcquireCamsButton.setGeometry(QtCore.QRect(10, 340, 75, 23))
        self.AcquireCamsButton.setObjectName("AcquireCamsButton")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(10, 530, 561, 141))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 559, 139))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logTextBox = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_3)
        self.logTextBox.setObjectName("logTextBox")
        self.verticalLayout.addWidget(self.logTextBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.CapturePushButton.setText(_translate("Form", "Capture"))
        self.ConfButton.setText(_translate("Form", "SetConf"))
        self.ProjectNameLabel.setText(_translate("Form", "Project Name"))
        self.ZStackBox.setText(_translate("Form", "Z-Stack"))
        self.WritePLlabel.setText(_translate("Form", "Image Write Path"))
        self.MsgLabel.setText(_translate("Form", "Messages:"))
        self.SingleCamCheckBox.setText(_translate("Form", "Single Cam"))
        self.BPPLabel.setText(_translate("Form", "Bits Per Pixel"))
        self.radioButton.setText(_translate("Form", "8 bpp"))
        self.FPSLabel.setText(_translate("Form", "Frames Per Second"))
        self.radioButton_2.setText(_translate("Form", "12 bpp"))
        self.ReleaseCamsButton.setText(_translate("Form", "FreeCams"))
        self.CaptureLabel.setText(_translate("Form", "Capture Time(s)"))
        self.CamSelectLabel.setText(_translate("Form", "Cam Select"))
        self.StatusLabel.setText(_translate("Form", "Status:"))
        self.LiveButton.setText(_translate("Form", "Live"))
        self.VertLabel.setText(_translate("Form", "Vertical"))
        self.ResolutionLabel.setText(_translate("Form", "Resolution"))
        self.CaptureModeLabel.setText(_translate("Form", "Capture Mode"))
        self.GainLabel.setText(_translate("Form", "Gain(dB)"))
        self.HorzLabel.setText(_translate("Form", "Horizontal"))
        self.EXPLabel.setText(_translate("Form", "Exposure(µs)"))
        self.BrowsePushButton.setText(_translate("Form", "Browse"))
        self.StackFramesLabel.setText(_translate("Form", "Stack Frames Count:"))
        self.AcquireCamsButton.setText(_translate("Form", "AcqCams"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
