# import sys
# import binascii
from queue import Empty
import threading
import time
import struct
import mmap
import math
import numpy as np
#from StringIO import StringIO
from PIL import *
# from PIL import ImageDraw
from PIL import Image

from datetime import date
# from lib2to3.pytree import convert
from struct import unpack
import socket
# from subprocess import call

from ctypes import *
# from typing import Any, Tuple
import visualizer._constants as _constants
import logging

import napari
from napari.qt.threading import thread_worker
from napari import Viewer
# from PyQt5.QtCore import QMutex, QWaitCondition

class M25Communication:
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 27015  # The port used by the server
    run = False
    path = ""
    today = date.today()
    proName = today.strftime("%Y%m%d_M25")  #As Per Request
    live_running = False
    zMode = False
    singleMode = False
    singleCam = 13
    timeLapseMode = False
    
    #Camera Globals
    horz: int = 608
    vert: int = 608
    fps: np.float32 = 40
    exp: int = 20000
    bpp: int = 8
    capTime: int = 15
    z_frames: int = 0
    gain: float = 15.0
    flags: int = 0
    lapse_count: int = 100
    lapse_min: float = 1

    
    #Threading events
    # sleep_mutex = threading.Event()
    write_mutex = threading.Lock()
    # sleep_mtx = QMutex() # For the live thread wait condition
    # live_sleep = QWaitCondition()
    
    th = None
    l_th = None

    def __init__(self,napari_viewer:Viewer):  
        super().__init__()
        self.napari_viewer = napari_viewer   
        hdlr = logging.StreamHandler()
        hdlr.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        self.m25_log = logging.getLogger('m25_logger')
        self.m25_log.addHandler(hdlr)
        self.m25_log.setLevel(logging.DEBUG)

        self.m25_log.debug("Initiating threads and workers")
        self.th = threading.Thread(target=self.client_thread)        
        #Calling it Napari way
        self.l_th = self.liveView_func()
        self.l_th.yielded.connect(self.update_layer)

    # def _init_threads(self):
    #     pass        
    #     # self.l_th = threading.Thread(target=self.liveView_thread, args =(napari_viewer,))
    
    def client_thread(self):
    #time.sleep(2)
        prevFlag = 0
        self.m25_log.debug("Client Thread")
        self.m25_log.debug("Run Flag {}".format(self.run))
        time.sleep(1)
        while self.run:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    
                    s.connect((self.HOST, self.PORT))
                    self.write_mutex.acquire()
                    # values = (self.horz, self.vert, self.fps, self.exp, self.bpp, self.z_frames, self.capTime, self.path.encode(), self.proName.encode(), self.flags, self.gain)
                    # packer = struct.Struct('L L f L L L L 255s 255s L d')
                    values = (self.horz, self.vert, self.fps, self.exp, self.bpp, self.z_frames, self.capTime, self.lapse_min,self.lapse_count, self.path.encode(), self.proName.encode(), self.flags, self.gain)
                    packer = struct.Struct('L L f L L L L f L 256s 256s L d')
                    packed_data = packer.pack(*values)
                    s.sendall(packed_data)
                    # logging.debug('flags: %d' % int(self.flags))                    
                    if self.flags & _constants.EXIT_THREAD:
                        self.write_mutex.release()
                        self.m25_log.debug('Closing Socket')
                        self.run = False
                        s.close()
                    else:
                        self.flags = 0
                        self.write_mutex.release()
                        # data: bytes = s.recv(1024)
                        # (rec_horz, rec_vert, rec_fps, rec_exp, rec_bpp, rec_z_frames, rec_capTime,
                        #     rec_path, rec_proName,
                        #     rec_flags, rec_gain) = unpack(
                        #     'L L f L L L L'
                        #     '255s'
                        #     '255s'
                        #     'L'
                        #     'd',
                        #     data
                        # )                   
                        data: bytes = s.recv(1024)
                        (rec_horz, rec_vert, rec_fps, rec_exp, rec_bpp, rec_z_frames, rec_capTime,
                            rec_lapse_min, rec_lapse_count,
                            rec_path, rec_proName,
                            rec_flags, rec_gain) = unpack(
                            'L L f L L L L f L'
                            '256s'
                            '256s'
                            'L'
                            'd',
                            data
                        )
                        
                        # self.m25_log.debug(len(data))
                    #pathStr = convert(rec_path)
                    # logging.debug('Received horz: %d' % int(rec_horz))
                    # logging.debug('Received vert: %d' % int(rec_vert))
                    # logging.debug('Received fps: %d' % int(rec_fps))
                    # logging.debug('Received exp: %d' % int(rec_exp))
                    # logging.debug('Received bpp: %d' % int(rec_bpp))
                    # logging.debug('Received capTime: %d' % int(rec_capTime))
                    # logging.debug('Received path: %s' % rec_path)
                                
                    self.write_mutex.acquire()
                    if prevFlag != rec_flags:
                        self.m25_log.debug('Received flags: {}'.format(str(hex(rec_flags))))

                    self.flags = self.flags | rec_flags
                    prevFlag = rec_flags
                    self.write_mutex.release()
                    #logging.debug('Received ' + repr(data))
                    time.sleep(0.1)
                except ConnectionRefusedError:
                    self.m25_log.info('Connection to microcontroller/cameras could not be made.')
                    # break the while loop, Connection to camera does not exist
                    break
 
    #live_sleep = QWaitCondtion()
    @thread_worker
    def liveView_func(self):
        while self.run:
            # self.sleep_mtx.lock()
            # self.live_sleep.wait(self.sleep_mtx)
            # self.sleep_mtx.unlock()
            
            if self.run and self.live_running:
                self.m25_log.debug("IT's ALIVEEEEEE")
                self.live_running = True
                # Create Memory Maps
                imageSize = np.uint64(((self.horz * self.vert) / 8 )* self.bpp)
                # adhearing to sector aligned memory
                if imageSize % 512 != 0:
                    imageSize += (512 - (imageSize % 512))
                # imgObj = np.dtype(np.uint8, imageSize)
                RW_flags = mmap.mmap(0, 8, "Local\\Flags")  # for basic signaling
                buff1 = mmap.mmap(0, int(imageSize * 25), "Local\\buff1")
                buff2 = mmap.mmap(0, int(imageSize * 25), "Local\\buff2")
                frameVect = []
                read_flags = np.uint8
                frameVect.clear()
                buff1.seek(0)
                buff2.seek(0)
                # layer = None
                imgshape = [self.horz, self.vert]
                imgshape_960 = [self.horz * 5, self.vert * 5]
                if self.singleMode:
                    self.m25_log.debug("SINGLE MODE INIT")
                    # myimg = plt.imshow(np.zeros([self.vert, self.horz]))
                    dst = Image.new('L', imgshape)
                    # layer = napari_viewer.add_image(np.zeros(imgshape))
                    # yield np.array(dst)
                else:
                    self.m25_log.debug("MULTICAM MODE INIT")
                    if self.horz < 808:
                        # myimg = plt.imshow(np.zeros([self.vert*5, self.horz*5]))
                        myimg = np.zeros(imgshape)
                    else:
                        myimg = np.zeros(imgshape_960)
                    dst = Image.new('L', imgshape_960)
                    # yield np.array(dst)

                while self.live_running:
                    self.m25_log.debug("LIVE RUNNING SETUP")
                    # self.m25_log.debug("live_running flag: {}".format(self.live_running))
                    # start = time.time()
                    read_flags = RW_flags.read_byte()
                    # logging.debug("FLAG"+ str(read_flags))
                    RW_flags.seek(0)
                    if read_flags & _constants.WRITING_BUFF1:
                        self.m25_log.debug("BUFF2")
                        read_flags |= _constants.READING_BUFF2
                        #read_flags &= ~(READING_BUFF1)
                        RW_flags.write_byte(read_flags)
                        for i in range(25):
                            frameVect.append(buff2.read(int(imageSize)))
                    else:
                        self.m25_log.debug("BUFF1")
                        read_flags |= _constants.READING_BUFF1
                        #read_flags &= ~(READING_BUFF2)
                        RW_flags.write_byte(read_flags)
                        for i in range(25):
                            frameVect.append(buff2.read(int(imageSize)))
                    RW_flags.seek(0)
                    read_flags &= ~(_constants.READING_BUFF1 | _constants.READING_BUFF2)
                    RW_flags.write_byte(read_flags)
                    RW_flags.seek(0)
                    buff1.seek(0)
                    buff2.seek(0)
                    # logging.debug("Then length: ", len(frameVect[i]))
                    # RW_flags &= ~( READING_BUFF1 | READING_BUFF2 )
                    if self.singleMode:
                        # self.m25_log.debug("DIsplayingCam: {}".format(self.singleCam))
                        dst = Image.frombuffer("L", [self.horz, self.vert],
                                                    frameVect[self.singleCam - 1],
                                                    'raw', 'L', 0, 1)
                        # myimg.set_data(dst)
                        time.sleep(0.016)
                        yield np.array(dst)

                    else:
                        for i in range(25):
                            image_conv = Image.frombuffer("L", [self.horz, self.vert],
                                                        frameVect[i],
                                                        'raw', 'L', 0, 1)
                            dst.paste(image_conv, [self.horz * (i % 5), self.vert * ((i // 5 % 5))])
                        self.m25_log.debug("before yield")

                        yield np.array(dst)

                    if not self.live_running:
                        dst=[]  

                    frameVect.clear()
                    #time.sleep(0.001)
                    # logging.debug("total time taken this loop:{}".format(str(time.time() - start)))
                
                RW_flags.close()
                buff1.close()
                buff2.close()
                
                # Send blank layer
                # dst =[]
                # yield np.array(dst)
    
    def update_layer(self, image):
        """[summary]

        Args:
            image ([type]): [description]
        """
        try:
            self.napari_viewer.layers['M25_cam'].data = image
            time.sleep(0.003)
            # self.m25_log.debug("NEW FRAME IN")
        except KeyError:
            self.napari_viewer.add_image(image, name='M25_cam',multiscale=False)
            # self.m25_log.debug("ADDING IMAGE. LAYER DIDNT EXIST")