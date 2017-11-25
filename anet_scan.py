#!/usr/bin/env python
'''
TODO: try https://github.com/duanhongyi/pyv4l2
'''
import sys
import array
import fcntl
import ctypes
import v4l2
import os
import logging
import pygame
import pygame.camera
import pygame.image
from pygame.locals import *
import time
import serial
import struct


SLEEP_BEFORE = 1
SLEEP_AFTER = 1
STEP = 2

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


pygame.init()
pygame.camera.init()

pcb_size = (int(sys.argv[2]), int(sys.argv[3]))

class VideoCapture(object):
    '''
    This is a class for capturing images using the V4L2 APIs via python binding
    but doesn't work :P
    '''
    # see <https://linuxtv.org/downloads/v4l-dvb-apis/uapi/v4l/capture.c.html>
    # https://jayrambhia.wordpress.com/2013/07/03/capture-images-using-v4l2-on-linux/
    # https://linuxtv.org/downloads/v4l-dvb-apis/
    def __init__(self, devicepath):
        self.devicepath = devicepath

        self.v4l2_init_cam()
        self.v4l2_init_mmap()
        self.v4l2_start_capture()

    def v4l2_init_cam(self):
        self.vd = open(self.devicepath, "rw")
        self.cp = v4l2.v4l2_capability()

        if fcntl.ioctl(self.vd, v4l2.VIDIOC_QUERYCAP, self.cp) != 0:
            raise ValueError(ctypes.get_errno())

        logger.info('found \'%s\'' % self.cp.card)

        if not (self.cp.capabilities & self.cp.capabilities & v4l2.V4L2_CAP_VIDEO_CAPTURE):
            raise ValueError('no video capture device')

        if not (self.cp.capabilities & v4l2.V4L2_MEMORY_MMAP):
            raise ValueError('no read API')

        self.fmt = v4l2.v4l2_format()
        self.fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE

        fcntl.ioctl(self.vd, v4l2.VIDIOC_G_FMT, self.fmt)

        logger.info('microscope format: %dx%d %s' % (self.fmt.fmt.pix.width, self.fmt.fmt.pix.height, struct.unpack('<cccc', self.fmt.fmt.pix.pixelformat.to_bytes(4))))

    def v4l2_init_mmap(self):
        self.req = v4l2.v4l2_requestbuffers()
        self.req.count = 1
        self.req.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        self.req.memory = v4l2.V4L2_MEMORY_MMAP

        logger.info(fcntl.ioctl(self.vd, v4l2.VIDIOC_REQBUFS, self.req))

        logger.info('req.count = %d' % self.req.count)

        self.buf = v4l2.v4l2_buffer()
        self.buf.type = self.req.type
        self.buf.memory = v4l2.V4L2_MEMORY_MMAP
        self.buf.index = 0
        logger.info(fcntl.ioctl(self.vd, v4l2.VIDIOC_QUERYBUF, self.buf))

        import mmap

        # import ipdb;ipdb.set_trace()
        # https://docs.python.org/3/library/mmap.html#mmap.mmap
        mmap.mmap(
            self.vd.fileno(),
            self.buf.length,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
            flags=mmap.MAP_SHARED,
            offset=self.buf.m.offset)

    def v4l2_start_capture():
        logger.info(fcntl.ioctl(self.vd, v4l2.VIDIOC_STREAMON, buf.type))

    def save_frame(self, output_filepath):
        with open('/tmp/stocazzo.raw', "w") as f:
            logger.info(fcntl.ioctl(self.vd, v4l2.VIDIOC_DQBUF, self.buf))

# http://www.pygame.org/docs/tut/CameraIntro.html
class Capture(object):
    '''
    This captures frames using the pygame's API.
    '''
    def __init__(self):
        self.size = (640,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)

        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def save_frame(self, filepath):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        #if self.cam.query_image():
        self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()
        pygame.image.save(self.snapshot, filepath)

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.get_and_flip()

def read_until_ok(s):
    lines = ""
    msg = None
    while msg != 'ok\n':
        msg = s.readline()

        logger.debug('read_until_ok:%s' % repr(msg))

        lines += msg

    return lines.rstrip()

# from /usr/lib/python2.7/site-packages/serial/serialposix.py
# /usr/include/asm-generic/termbits.h for struct termios2
#  [2]c_cflag [9]c_ispeed [10]c_ospeed
def set_special_baudrate(fd, baudrate):
    TCGETS2 = 0x802C542A
    TCSETS2 = 0x402C542B
    BOTHER = 0o010000
    CBAUD = 0o010017
    buf = array.array('i', [0] * 64) # is 44 really
    fcntl.ioctl(fd, TCGETS2, buf)
    buf[2] &= ~CBAUD
    buf[2] |= BOTHER
    buf[9] = buf[10] = baudrate
    assert(fcntl.ioctl(fd, TCSETS2, buf)==0)
    fcntl.ioctl(fd, TCGETS2, buf)
    if buf[9] != baudrate or buf[10] != baudrate:
        print("failed. speed is %d %d" % (buf[9],buf[10]))
        sys.exit(1)

#cam = VideoCapture('/dev/video0')
#cam.save_frame('miao')
cam = Capture()

# open the serial port
device_path = sys.argv[1]
baudrate = 250000

fd = os.open(device_path, os.O_RDWR)
#printer = os.fdopen(fd, "ra")

set_special_baudrate(fd, baudrate)

printer = serial.Serial(device_path, 250000)

# give the webcam to adjust the brightness and focus
time.sleep(5)

banner = ""
while printer.in_waiting > 0:
    banner += printer.readline()

logger.info('init: %s' % banner.rstrip())

for x in xrange(pcb_size[0]/STEP):
    for y in xrange(pcb_size[1]/STEP):

        logger.info('%d:%d' % (x, y))
        events = pygame.event.get()

        #raw_input('just before the G command')
        #printer.write('M114\n')
        printer.write('G1 X%d Y%d\n' % (x*STEP, y*STEP))

        logger.info('Merlin:%s' % read_until_ok(printer))
        #raw_input('just before the M400 command')
        printer.write('M400\n') # wait until the operation is done
        logger.info('Merlin:%s' % read_until_ok(printer))

        time.sleep(SLEEP_BEFORE)

        #raw_input('just before the photo')
        cam.save_frame('shoots/frame_%02d_%02d.png' % (x, y))
        cam.save_frame('shoots/frame_%02d_%02d.png' % (x, y))
        cam.save_frame('shoots/frame_%02d_%02d.png' % (x, y))
        time.sleep(SLEEP_AFTER)

printer.write('G1 X0 Y0\n')
printer.write('M400\n') # wait until the operation is done
logger.info('Merlin:%s' % read_until_ok(printer))
pygame.camera.quit()
