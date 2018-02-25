from __future__ import absolute_import
import array
import ctypes
import fcntl
import logging
import os
import serial


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


def open_serial(device_path='/dev/ttyACM0', baudrate=250000):
    logger.info('opening serial device \'%s\' with baudrate set to %d' % (device_path, baudrate))
    fd = os.open(device_path, os.O_RDWR)
    set_special_baudrate(fd, baudrate)

    device = serial.Serial(device_path, baudrate)

    logger.info('please wait, the device will reset in a few seconds')
    # we need to wait a little bit to allow the port to be opened
    # and the device to be reset
    import time;time.sleep(5)

    banner = "\n"
    while device.in_waiting > 0:
        banner += device.readline()

    logger.info('BANNER: %s' % banner)

    return device

if __name__ == '__main__':
    device = open_serial()

    device.close()
