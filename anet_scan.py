#!/usr/bin/env python3
'''
TODO: try https://github.com/duanhongyi/pyv4l2
'''
import argparse
import pathlib
import sys
# import v4l2
import os
import logging
import pygame
import pygame.camera
import pygame.image
from pygame.locals import *
import time
import serial
import struct
import tqdm
import anet


SLEEP_BEFORE = 1
SLEEP_AFTER = 1


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
class Capture:
    '''
    This captures frames using the pygame's API.
    '''
    def __init__(self, video=None, resolution=None):
        self.size = resolution or (640, 480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)

        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()

        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")

        video = video or self.clist[0]

        self.cam = pygame.camera.Camera(video, self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def wait(self, count=5):
        """Wait a couple of seconds grabbing images"""
        for _ in range(count):
            self.get_snapshot()

    def get_snapshot(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        #if self.cam.query_image():
        return self.cam.get_image(self.snapshot)

    def save_frame(self, filepath):
        self.snapshot = self.get_snapshot()

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
    lines = b""
    msg = None
    while msg != b'ok\n':
        msg = s.readline()

        logger.debug('read_until_ok:%s' % repr(msg))

        lines += msg

    return lines.rstrip()


def argparse_size(value):
    x, y = value.split("x")

    return int(x), int(y)


def parse_args():
    args = argparse.ArgumentParser(description='Scan PCB')

    args.add_argument('project', type=str,
        help="None of the capture (primarly used to create `shoots_<project name>` directory)")

    args.add_argument(
        '--video',
        type=str,
        required=True,
        help="device node of the camera")
    args.add_argument(
        '--printer',
        type=str,
        required=True,
        help="serial port of the printer")
    args.add_argument('--size',
        required=True,
        type=argparse_size,
        help="dimensions in millimeters of the board, indicated as XxY")
    args.add_argument('--steps',
        required=True,
        type=argparse_size,
        help="steps in millimeters of the board, indicated as XxY")
    args.add_argument('--resolution',
        type=argparse_size,
        help="resolution of the captured images indicated as XxY")

    return args.parse_args()

if __name__ == '__main__':
    pygame.init()
    pygame.camera.init()

    args = parse_args()

    project_name = args.project

    path_output = pathlib.Path("shoots_{}".format(project_name))

    if not path_output.exists():
        logger.info("creating directory %s" % str(path_output))
        path_output.mkdir()

    if path_output.exists() and not path_output.is_dir():
        logger.error("%s exists but is not a directory")
        sys.exit(1)

    pcb_size = args.size
    cam = Capture(video=args.video, resolution=args.resolution)

    # open the serial port
    device_path = args.printer
    baudrate = 250000

    # fd = os.open(device_path, os.O_RDWR)

    printer = serial.Serial(device_path, 250000)

    # give the webcam to adjust the brightness and focus
    logger.info("please wait a little bit, the camera is focusing right now :)")
    cam.wait()

    banner = b""
    while printer.in_waiting > 0:
        banner += printer.readline()

    logger.info('init: %s' % banner.rstrip())

    # set acceleration to the minimum possible to avoid board moving
    printer.write(b"M201 X50 Y50")
    printer.write(b"G21")  # set units to millimeters

    STEP_X, STEP_Y = args.steps
    """
    The movements follow a matrix, first moves by X, completes a columns and moves
    one step in the Y direction and repeats the Xs.
    """
    n_xs = int(pcb_size[0]/STEP_X)
    n_ys = int(pcb_size[1]/STEP_Y)

    logger.info("The process is starting: the final  matrix will be (%d, %d)" % (n_xs, n_ys))
    logger.warning(" ##### THERE ARE NO CHECK THAT THE MOVEMENTS WILL STEP OVER THE PHYSICAL BOUNDARIES OF THE PRINTER!!!!")

    # to follow the convention of xy-stitch we reverse the Y numbering
    # so that the (0, 0) is the left-upper corner
    for x in tqdm.tqdm(range(n_xs)):
        for y in tqdm.tqdm(reversed(range(n_ys))):

            logger.debug('x=%d y=%d' % (x, y))
            events = pygame.event.get()

            #raw_input('just before the G command')
            #printer.write('M114\n')
            printer.write(b'G1 X%d Y%d\n' % (x * STEP_X, ((n_ys - 1) - y) * STEP_Y))

            logger.debug('Merlin:%s' % read_until_ok(printer))
            #raw_input('just before the M400 command')
            printer.write(b'M400\n') # wait until the operation is done
            logger.debug('Merlin:%s' % read_until_ok(printer))

            time.sleep(SLEEP_BEFORE)

            #raw_input('just before the photo')
            # FIXME: seems that without taking multiple images
            # they are "out of focus"
            path_frame = path_output / ('c%03d_r%03d.png' % (x, y))
            cam.save_frame(path_frame)
            cam.save_frame(path_frame)
            cam.save_frame(path_frame)
            time.sleep(SLEEP_AFTER)

    printer.write(b'G1 X0 Y0\n')
    printer.write(b'M400\n') # wait until the operation is done
    logger.info('Merlin:%s' % read_until_ok(printer))
    pygame.camera.quit()
