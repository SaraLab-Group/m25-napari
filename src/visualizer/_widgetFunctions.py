
import sys
import os
from this import d
import psutil
# import binascii
# import threading
import time
import struct
import mmap
import math
import signal
from PyQt5 import QtWidgets
from PyQt5 import QWaitCondition
from PyQt5 import QMutex
from matplotlib import pyplot as plt
from psutil import Popen
from napari._qt.qt_main_window import _QtMainWindow
from napari._qt.qthreading import thread_worker
import numpy as np
#from StringIO import StringIO
from PIL import *
from PIL import ImageDraw
from PIL import Image
import sys
from datetime import date
from lib2to3.pytree import convert
from struct import unpack
# import socket
from subprocess import call

from ctypes import *
from typing import Any, Tuple

#Import Qt components
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QAction, QWidget, QFileDialog
from PyQt5 import QtGui

from visualizer.Qt import M25GUI
from visualizer._app import M25Communication
import visualizer._constants as _constants

import logging
from napari import Viewer
import visualizer.calibration as calibration

class M25Controls(QWidget):   
    def __init__(self,napari_viewer:Viewer):
        super().__init__()
        
        self.M25app = None
        # self.worker_client = None
        # self.worker_liveV = None 
        self.viewer = napari_viewer
        self.initialize()

        #Init GUI with default
        self.today = date.today()
        self.proName = self.today.strftime("%Y%m%d_M25")  # As Per Request
        #TODO: change to a more default folder later
        self.path = r'H:\Test'
        
         ### Setup the UI and function connections
        self.ui.WritePLineEdit.setText(self.path)
        self.ui.PNameLineEdit.setText(self.proName)
        self.onlyInt = QtGui.QIntValidator()
        self.onlyFloats = QtGui.QDoubleValidator()
        self.ui.radioButton.toggled.connect(self.onClicked)
        self.ui.radioButton.value = 8
        self.ui.radioButton_2.toggled.connect(self.onClicked)
        self.ui.radioButton_2.value = 16
        self.ui.HorzLineEdit.setText(str(self.M25app.horz))
        self.ui.HorzLineEdit.editingFinished.connect(self.sync_HorzLineEdit)
        self.ui.HorzLineEdit.setValidator(self.onlyInt)
        self.ui.VertLineEdit.setText(str(self.M25app.vert))
        self.ui.VertLineEdit.editingFinished.connect(self.sync_VertLineEdit)
        self.ui.VertLineEdit.setValidator(self.onlyInt)
        self.ui.FPSLineEdit.setText(str(self.M25app.fps))
        self.ui.FPSLineEdit.editingFinished.connect(self.sync_FPSLineEdit)
        self.ui.FPSLineEdit.setValidator(self.onlyFloats)
        self.ui.EXPLineEdit.setText(str(self.M25app.exp))
        self.ui.EXPLineEdit.editingFinished.connect(self.sync_EXPLineEdit)
        self.ui.EXPLineEdit.setValidator(self.onlyInt)
        self.ui.CapTimeLineEdit.setText(str(self.M25app.capTime))
        self.ui.CapTimeLineEdit.editingFinished.connect(self.sync_CapTimeLineEdit)
        self.ui.CapTimeLineEdit.setValidator(self.onlyInt)
        # self.ui.MsgLineEdit.setText("Default")
        # self.ui.StatusLineEdit.setText("OFFLINE")
        self.ui.radioButton.setChecked(True)
        self.ui.BrowsePushButton.clicked.connect(self.browseState)
        self.ui.AcquireCamsButton.clicked.connect(self.AcquireState)
        self.ui.ReleaseCamsButton.clicked.connect(self.ReleaseState)
        self.ui.ConfButton.clicked.connect(self.ConfState)
        self.ui.CapturePushButton.clicked.connect(self.CaptureState)
        self.ui.GainlineEdit.setText(str(self.M25app.gain))
        self.ui.GainlineEdit.editingFinished.connect(self.sync_GainLineEdit)
        self.ui.PNameLineEdit.editingFinished.connect(self.sync_PNameLineEdit)
        self.ui.LiveButton.clicked.connect(self.toggleLive)
        self.ui.StackFramesEdit.setText("0")
        self.ui.StackFramesEdit.editingFinished.connect(self.sync_StackFramesEdit)
        # self.ui.ZStackBox = QCheckBox("Button1")
        self.ui.ZStackBox.setChecked(False)
        self.ui.ZStackBox.stateChanged.connect(self.checkClicked)
        self.ui.CamSpinBox.setValue(13)
        self.ui.CamSpinBox.setMinimum(1)
        self.ui.CamSpinBox.setMaximum(25)
        self.M25app.singleCam =self.ui.CamSpinBox.value()
        self.ui.CamSpinBox.valueChanged.connect(self.singleSpinClicked)
        self.ui.SingleCamCheckBox.setChecked(False)
        self.ui.SingleCamCheckBox.stateChanged.connect(self.singleClicked)
        self.ui.exitBtn.clicked.connect(self.cleanup_M25Plugin)
        self.ui.loadBtn.clicked.connect(self.load_dataset)
        self.ui.toggleDM.clicked.connect(self.control_DM)
        self.ui.toggleLED.clicked.connect(self.control_LED)
        # self.start_logging()
    

    
    def initialize(self):
        self.ui = M25GUI.Ui_Form()
        self.ui.setupUi(self)
        self.start_logging()

        #TODO: make sure live thread is paused before M25 initalization
        logging.info('Initializing Comm')
        #Initialize the Qt GUI and the M25 Communications
        self.M25app = M25Communication(self.viewer)
        self._start_cmd()
        self._start_threads()
        # self.M25app._init_threads()

        
        ### Initialize M25 app communication file and globals
        self.M25app.bpp = 8
        
    def start_logging(self):
        ## Logging
        log_box = QtLogger(self.ui.logTextBox)
        log_box.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        self.m25_log = logging.getLogger('m25_logger')
        self.m25_log.addHandler(log_box)
        #Change logging to INFO or DEBUG to see all log (info,debug,warning)
        self.m25_log.setLevel(logging.DEBUG)
        # logging.getLogger().setLevel(logging.INFO)

    def _start_cmd(self):
            # TODO: Make this modular so that we can have the exe path at a fixed folder from installation 
        self.exe_path = r'C:\Users\yoshi\Documents\M25\m25_FLIR\m25_flir\m25_FLIR\bin\x64\Debug'
        # self.exe_path = r'C:\Users\yoshi\Documents\M25\m25_FLIR\m25_flir\m25_FLIR\bin\x64\Release'
        # self.exe_path = os.path.dirname(__file__)
        # self.exe_path = os.path.join(dirname,'')
        self.myEXE = "m25_FLIR.exe"
        self.m25_log.debug(str(self.exe_path))
        self.rc = call("start cmd /K " + self.myEXE, cwd=self.exe_path, shell=True)  # run `cmdline` in `dir`
        # self.rc = Popen("start cmd /K " + self.myEXE, cwd=self.exe_path, shell=True)  # run `cmdline` in `dir`
    
    def _start_threads(self):
        self.M25app.th.start()
        # self.M25app.l_th.finished.connect(self.ui.exitBtn.clicked)
        self.M25app.l_th.start()
        self.M25app.l_th.pause()

               
    ### Define the Signal Functions
    @pyqtSlot(bool)
    def onClicked(self):
        self.M25app.write_mutex.acquire()
        radioButton = self.sender()
        if radioButton.isChecked():
            self.M25app.bpp = (radioButton.value)
            # self.m25_log.debug("Button Value bpp: %d" % (radioButton.value))
        self.M25app.write_mutex.release()
    
    @pyqtSlot()
    def checkClicked(self):
        self.M25app.write_mutex.acquire()
        box = self.sender()
        if box.isChecked():
            self.M25app.zMode = True
        else:
            self.M25app.zMode = False
        self.M25app.write_mutex.release()
    
    @pyqtSlot()
    def singleClicked(self):
        self.M25app.write_mutex.acquire()
        box = self.sender()
        if box.isChecked():
            self.M25app.singleMode = True
        else:
            self.M25app.singleMode = False
        self.M25app.write_mutex.release()
        
    @pyqtSlot()
    def singleSpinClicked(self):
        self.M25app.write_mutex.acquire()
        self.M25app.singleCam = self.ui.CamSpinBox.value()
        self.M25app.write_mutex.release()
        
    @pyqtSlot()
    def sync_HorzLineEdit(self):
        text = self.ui.HorzLineEdit.text()
        self.M25app.write_mutex.acquire()
        if len(text) > 0:
            self.M25app.horz = (int(text))
        else:
            self.M25app.horz = (0)
        self.M25app.write_mutex.release()

    @pyqtSlot()
    def sync_VertLineEdit(self):
        text = self.ui.VertLineEdit.text()
        self.M25app.write_mutex.acquire()
        if len(text) > 0:
            self.M25app.vert = (int(text))
        else:
            self.M25app.vert = (0)
        self.M25app.write_mutex.release()

    @pyqtSlot()
    def sync_FPSLineEdit(self):
        text = self.ui.FPSLineEdit.text()
        self.M25app.write_mutex.acquire()
        if len(text) > 0:
            self.M25app.fps = np.float32(text)
        else:
            self.M25app.fps = np.float32(0)
        self.M25app.write_mutex.release()

    @pyqtSlot()
    def sync_EXPLineEdit(self):
        text = self.ui.EXPLineEdit.text()
        self.M25app.write_mutex.acquire()
        if len(text) > 0:
            self.M25app.exp = int(text)
        else:
            self.M25app.exp = (0)
        self.M25app.write_mutex.release()

    @pyqtSlot()
    def sync_CapTimeLineEdit(self):
        text = self.ui.CapTimeLineEdit.text()
        self.M25app.write_mutex.acquire()
        if len(text) > 0:
            self.M25app.capTime = (int(text))
        else:
            self.M25app.capTime = (0)
        self.M25app.write_mutex.release()
    
    @pyqtSlot()
    def sync_GainLineEdit(self):
        text = self.ui.GainlineEdit.text()
        self.M25app.write_mutex.acquire()
        if len(text) > 0:
            self.M25app.gain = (float(text))
        else:
            self.M25app.gain = float(0.0)
        self.M25app.write_mutex.release()

    @pyqtSlot()
    def sync_PNameLineEdit(self):
        self.acquisition_filename = self.ui.PNameLineEdit.text()
        self.M25app.write_mutex.acquire()
        self.M25app.proName = self.acquisition_filename
        self.M25app.write_mutex.release()
    
    @pyqtSlot()
    def sync_StackFramesEdit(self):
        text = self.ui.StackFramesEdit.text()

        self.M25app.write_mutex.acquire()
        if len(text) > 0:
            self.M25app.z_frames = int(text)
        else:
            self.M25app.z_frames = int(0)
        self.M25app.write_mutex.release()
    
    @pyqtSlot()    
    def browseState(self):
        #TODO: make this open at the default directory
        self.M25app.path = str(QFileDialog.getExistingDirectory(self, "Select Directory",self.path))
        self.path=self.M25app.path
        self.ui.WritePLineEdit.setText(self.M25app.path)
    
    @pyqtSlot()
    def AcquireState(self):
        self.m25_log.debug("Acquire State")
        self.m25_log.debug("flags{}".format(self.M25app.flags))
        self.M25app.write_mutex.acquire()
        if self.M25app.flags & _constants.CAMERAS_ACQUIRED or self.M25app.flags & _constants.CAPTURING:
            pass
        else:
            self.M25app.flags |= _constants.ACQUIRE_CAMERAS
        self.M25app.write_mutex.release()
        
    @pyqtSlot()
    def ConfState(self):
        self.m25_log.debug("Conf State")
        self.m25_log.debug("flags: {}".format(str(hex(self.M25app.flags))))
        self.M25app.write_mutex.acquire()
        if self.M25app.flags & _constants.CAPTURING or self.M25app.flags & _constants.ACQUIRING_CAMERAS or self.M25app.flags & _constants.CAMERAS_ACQUIRED:
            pass
        else:
            self.M25app.flags |= _constants.CHANGE_CONFIG
            self.m25_log.debug("FPS {}, Gain {}, CapTime{}".format( np.float32(self.ui.FPSLineEdit.text()),
                                                                float(self.ui.GainlineEdit.text()),
                                                                int(self.ui.CapTimeLineEdit.text())))
        self.M25app.write_mutex.release()
        
    @pyqtSlot()
    def ReleaseState(self):
        self.M25app.write_mutex.acquire()
        if self.M25app.flags & _constants.CAPTURING:
            pass
        else:
            self.M25app.flags |= _constants.RELEASE_CAMERAS
            self.m25_log.info("Cameras Released")
            self.m25_log.debug("flags: {}".format(str(hex(self.M25app.flags))))

        self.M25app.write_mutex.release()
    
    @pyqtSlot()  
    def CaptureState(self):
        self.m25_log.debug("CAPTURE Pressed")
        self.M25app.write_mutex.acquire()
        if self.M25app.flags & _constants.CAMERAS_ACQUIRED:
            if self.M25app.flags &_constants.CAPTURING:
                pass
            else:
                if self.M25app.zMode == True:
                    self.M25app.flags |= _constants.START_Z_STACK
                else:
                    self.m25_log.info("CAPTURE STARTED")
                    self.M25app.flags |= _constants.START_CAPTURE
        self.M25app.write_mutex.release()
    
    @pyqtSlot()
    def toggleLive(self):
        self.M25app.write_mutex.acquire()
        self.m25_log.debug("LIVE PRESS")
        self.m25_log.info("Live Running %d", self.M25app.live_running)
        if self.M25app.flags & _constants.CAMERAS_ACQUIRED:
            if self.M25app.flags & _constants.CAPTURING:
                pass
            elif self.M25app.live_running:
                self.m25_log.info("STOPPING LIVE")
                self.M25app.live_running = False
                self.M25app.flags |= _constants.STOP_LIVE
                self.M25app.flags &= ~(_constants.LIVE_RUNNING)
                # self.M25app.sleep_mutex.clear()
                #self.M25app.l_th.pause()
                self.m25_log.debug("flags: {}".format(str(hex(self.M25app.flags))))
            else:
                self.M25app.live_running = True
                self.m25_log.info("LIVE RUNNING")
                self.M25app.flags |= _constants.START_LIVE
                # self.M25app.sleep_mutex.set()
                self.M25app.live_sleep.wake_one()
                self.m25_log.debug("flags: {}".format(str(hex(self.M25app.flags))))
        self.M25app.write_mutex.release()
    
    @pyqtSlot()
    def cleanup_M25Plugin(self):
        self.m25_log.info("CLOSING STARTED")
        self.M25app.write_mutex.acquire()
        self.M25app.flags |= _constants.EXIT_THREAD
        self.M25app.write_mutex.release()
        self.m25_log.debug('close event fired')
        time.sleep(0.2)
        self.M25app.run = False
        self.M25app.live_running = False
        # self.M25app.sleep_mutex.set()
        self.M25app.th.join()
        self.M25app.l_th.pause()
        self.M25app.l_th.quit()   #Since it is a Napari Worker then use their cleanup 

        time.sleep(0.2)
        self.viewer.window.remove_dock_widget(self)

    @pyqtSlot()
    def load_dataset(self):
        #TODO Add calibration.py to package or make loading separate package
        loading_path= str(QFileDialog.getExistingDirectory(self, "Select Directory",self.M25app.path))
        # main_folder = os.path.join(self.M25app.path, self.filename)
        try:
            stack = calibration.lazy_dask_stack(loading_path,num_cams=25, px_depth='uint8', height=608, width =808)
        except: 
            stack = calibration.lazy_dask_stack(loading_path,num_cams=25, px_depth='uint16', height=608, width =808)
        self.viewer.add_image(stack)
    
    
    @pyqtSlot()
    def control_LED(self):
        self.m25_log.debug("Toggle LED Pressed")
        self.M25app.write_mutex.acquire()
        self.M25app.flags |= _constants.TOGGLE_LED
        self.M25app.write_mutex.release()

    @pyqtSlot()
    def control_DM(self):
        self.m25_log.debug("Toggle Digital Modulation Pressed")
        self.M25app.write_mutex.acquire()
        self.M25app.flags |= _constants.TOGGLE_DIG_MOD
        self.M25app.write_mutex.release()
        
## Adopted from Todd Vanyo's https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
# Linking Napari Log to our logger
# Adopted from Cam's' RecOrder
class QtLogger(logging.Handler,QObject): 
    appendPlainText = pyqtSignal(str)
    def __init__(self,widget):
        super().__init__()
        QObject.__init__(self)
        self.widget = widget
        self.appendPlainText.connect(self.widget.appendPlainText)
    def emit(self,record):
        msg = self.format(record)
        # self.widget.appendPlainText(msg)
        self.appendPlainText.emit(msg)
