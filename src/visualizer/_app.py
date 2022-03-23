# import sys
# import binascii
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

class M25Communication:
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 27015  # The port used by the server
    run = True
    path = ""
    today = date.today()
    proName = today.strftime("%Y%m%d_M25")  #As Per Request
    live_running = False
    zMode = False
    singleMode = False
    singleCam = 13
    
    #Camera Globals
    horz: int = 960
    vert: int = 600
    fps: int = 2
    exp: int = 250000
    bpp: int = 8
    capTime: int = 10
    z_frames: int = 0
    gain: float = 0.0
    flags: int = 0
    
    #Threading events
    sleep_mutex = threading.Event()
    write_mutex = threading.Lock()
    
    th = None
    l_th = None

    def __init__(self,napari_viewer:Viewer):  
        super().__init__()
        self.napari_viewer = napari_viewer   
        
        logging.debug("initiating threads and workers")
        self.th = threading.Thread(target=self.client_thread)        
        #Calling it Napari way
        self.l_th = self.liveView_napari()
        self.l_th.yielded.connect(self.update_layer)
        #Initialize Threads
        # self.th = threading.Thread(target=self.client_thread)
        # self.l_th = threading.Thread(target=self.liveView_thread)
    def _init_threads(self):
        pass        
        # self.l_th = threading.Thread(target=self.liveView_thread, args =(napari_viewer,))
    
    def client_thread(self):
    #time.sleep(2)
        prevFlag = 0
        logging.debug("Client Thread")
        logging.debug("Run Flag {}".format(self.run))
        while self.run:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.HOST, self.PORT))
                self.write_mutex.acquire()
                values = (self.horz, self.vert, self.fps, self.exp, self.bpp, self.z_frames, self.capTime, self.path.encode(), self.proName.encode(), self.flags, self.gain)
                packer = struct.Struct('L L L L L L L 255s 255s L d')
                packed_data = packer.pack(*values)
                s.sendall(packed_data)
                # logging.debug('flags: %d' % int(self.flags))                    
                if self.flags & _constants.EXIT_THREAD:
                    self.write_mutex.release()
                    logging.debug('Closing Socket')
                    self.run = False
                    s.close()
                else:
                    self.flags = 0
                    self.write_mutex.release()
                    data: bytes = s.recv(1024)
                    (rec_horz, rec_vert, rec_fps, rec_exp, rec_bpp, rec_z_frames, rec_capTime,
                        rec_path, rec_proName,
                        rec_flags, rec_gain) = unpack(
                        'L L L L L L L'
                        '255s'
                        '255s'
                        'L'
                        'd',
                        data
                    )
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
                    logging.debug('Received flags: {}'.format(str(hex(rec_flags))))

                self.flags = self.flags | rec_flags
                prevFlag = rec_flags
                self.write_mutex.release()
                #logging.debug('Received ' + repr(data))
                time.sleep(0.1)
                
    @thread_worker
    def liveView_napari(self):
        while self.run:
            self.sleep_mutex.wait(None)
            if self.run:
                logging.debug("IT's ALIVEEEEEE")
                self.live_running = True
                # Create Memory Maps
                imageSize = np.uint64((self.horz * self.vert) / 8 * self.bpp)
                # adhearing to sector aligned memory
                if imageSize % 512 != 0:
                    imageSize += (512 - (imageSize % 512))
                imgObj = np.dtype(np.uint8, imageSize)
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
                    logging.debug("SINGLE MODE INIT")
                    # myimg = plt.imshow(np.zeros([self.vert, self.horz]))
                    dst = Image.new('L', imgshape)
                    # layer = napari_viewer.add_image(np.zeros(imgshape))
                    yield np.array(dst)
                else:
                    if self.horz < 960:
                        # myimg = plt.imshow(np.zeros([self.vert*5, self.horz*5]))
                        myimg = np.zeros(imgshape)
                    else:
                        myimg = np.zeros(imgshape_960)
                    dst = Image.new('L', imgshape_960)
                    yield np.array(dst)
                    
                logging.debug("CHeck if live running")
                while self.live_running:
                    # logging.debug("LIVE RUNNING SETUP")
                    # start = time.time()
                    read_flags = RW_flags.read_byte()
                    # logging.debug("FLAG"+ str(read_flags))
                    RW_flags.seek(0)
                    if read_flags & _constants.WRITING_BUFF1:
                        # logging.debug("BUFF2")
                        read_flags |= _constants.READING_BUFF2
                        #read_flags &= ~(READING_BUFF1)
                        RW_flags.write_byte(read_flags)
                        for i in range(25):
                            frameVect.append(buff2.read(int(imageSize)))
                    else:
                        # logging.debug("BUFF1")
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
                        dst = Image.frombuffer("L", [self.horz, self.vert],
                                                    frameVect[self.singleCam - 1],
                                                    'raw', 'L', 0, 1)
                        # myimg.set_data(dst)
                        yield np.array(dst)
                        
                    else:
                        for i in range(25):
                            image_conv = Image.frombuffer("L", [self.horz, self.vert],
                                                        frameVect[i],
                                                        'raw', 'L', 0, 1)
                            dst.paste(image_conv, [self.horz * (i % 5), self.vert * ((i // 5 % 5))])
                        yield np.array(dst)
                                                                    
                    if not self.live_running:
                        dst=[]  

                    frameVect.clear()
                    #time.sleep(0.001)
                    # logging.debug("total time taken this loop:{}".format(str(time.time() - start)))
                
                # Send blank layer
                dst =[]
                yield np.array(dst)
    
    def update_layer(self, image):
        """[summary]

        Args:
            image ([type]): [description]
        """
        try:
            self.napari_viewer.layers['M25_cam'].data = image
            time.sleep(0.003)
        except KeyError:
            self.napari_viewer.add_image(image, name='M25_cam')

    # def liveView_func(self):
    #     if self.run:
    #         self.live_running = True
    #         # Create Memory Maps
    #         imageSize = np.uint64((self.horz * self.vert) / 8 * self.bpp)
    #         # adhearing to sector aligned memory
    #         if imageSize % 512 != 0:
    #             imageSize += (512 - (imageSize % 512))
    #         imgObj = np.dtype(np.uint8, imageSize)
    #         RW_flags = mmap.mmap(0, 8, "Local\\Flags")  # for basic signaling
    #         buff1 = mmap.mmap(0, int(imageSize * 25), "Local\\buff1")
    #         buff2 = mmap.mmap(0, int(imageSize * 25), "Local\\buff2")
    #         frameVect = []
    #         read_flags = np.uint8
    #         #fig = plt.figure(figsize=(10, 7))
    #         #fig, ax_list = plt.subplots(1,1)

    #         ##Preload
    # #        img_x = []
    # #        ax_list = ax_list.ravel()
    # #
    # #        for i in range(25):
    # #            frameVect.append(buff2.read(int(imageSize)))
    # #
    # #        for i in range(25):
    # #            image_conv = Image.frombuffer("L", [horz, vert],
    # #                                         frameVect[i],
    # #                                         'raw', 'L', 0, 1)
    # #           # fig.add_subplot(5, 5, i + 1)
    # #           img_x.append(ax_list[i].imshow(image_conv))
    #         frameVect.clear()
    #         plt.ion()
    #         buff1.seek(0)
    #         buff2.seek(0)

    #         if self.singleMode:
    #             myimg = plt.imshow(np.zeros([self.vert, self.horz]))
    #             dst = Image.new('L', [self.horz, self.vert])
    #         else:
    #             if self.horz < 960:
    #                 myimg = plt.imshow(np.zeros([self.vert*5, self.horz*5]))
    #             else:
    #                 myimg = plt.imshow(np.zeros([self.vert*2, self.horz*2]))
    #             dst = Image.new('L', [self.horz * 5, self.vert * 5])

    #         while self.live_running:
    #             start = time.time()
    #             # do stuff
    #             read_flags = RW_flags.read_byte()
    #             RW_flags.seek(0)
    #             if read_flags & _constants.WRITING_BUFF1:
    #                 logging.debug("BUFF2")
    #                 read_flags |= _constants.READING_BUFF2
    #                 #read_flags &= ~(READING_BUFF1)
    #                 RW_flags.write_byte(read_flags)
    #                 for i in range(25):
    #                     frameVect.append(buff2.read(int(imageSize)))
    #             else:
    #                 logging.debug("BUFF1")
    #                 read_flags |= _constants.READING_BUFF1
    #                 #read_flags &= ~(READING_BUFF2)
    #                 RW_flags.write_byte(read_flags)
    #                 for i in range(25):
    #                     frameVect.append(buff2.read(int(imageSize)))
    #             RW_flags.seek(0)
    #             read_flags &= ~(_constants.READING_BUFF1 | _constants.READING_BUFF2)
    #             RW_flags.write_byte(read_flags)
    #             RW_flags.seek(0)
    #             buff1.seek(0)
    #             buff2.seek(0)
    #             logging.debug("Then length: ", len(frameVect[i]))
    #             # RW_flags &= ~( READING_BUFF1 | READING_BUFF2 )

    #             if self.singleMode:
    #                 dst = Image.frombuffer("L", [self.horz, self.vert],
    #                                               frameVect[self.singleCam - 1],
    #                                               'raw', 'L', 0, 1)
    #                 myimg.set_data(dst)
    #             else:
    #                 for i in range(25):
    #                     image_conv = Image.frombuffer("L", [self.horz, self.vert],
    #                                                   frameVect[i],
    #                                                   'raw', 'L', 0, 1)
    #                     dst.paste(image_conv, [self.horz * (i % 5), self.vert * ((i // 5 % 5))])

    #                 if self.horz < 960:
    #                     myimg.set_data(dst)
    #                 else:
    #                     myimg.set_data(dst.resize((self.horz*2, self.vert*2)))

    #             #plt.axis('off')
    #             #plt.show()
    #             plt.pause(0.001)

    #             if not self.live_running:
    #                 plt.close()

    #             frameVect.clear()
    #             #time.sleep(0.001)
    #             logging.debug("total time taken this loop: ", time.time() - start)
    #         plt.close()