'''
For more information about GCODE take a look at <http://reprap.org/wiki/G-code>.
'''
from __future__ import absolute_import
import array
import ctypes
import fcntl
import logging
import time
import os
import serial
from cmd import Cmd


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SerialCmd(Cmd):
    def __init__(self, printer):
        Cmd.__init__(self)
        self.printer = printer

    def _query(self, msg):
        self.printer.write('%s\r\n' % msg)

        # we need to wait a little bit in order
        # to receive the output
        while self.printer.in_waiting == 0:
            time.sleep(0.5)

        response = ''
        while self.printer.in_waiting > 0:
            response += self.printer.readline()
            #time.sleep(0.5)

        return response

    def do_query(self, args):
        print self._query(args)

    def do_firmware(self, args):
        '''Get firmware version and capabilities'''
        print self._query('M115')

    def do_origin(self, args):
        '''Move to origin the printer head'''
        self.printer.write('G28\n')
        response = self.printer.readline()

        print response

    def do_sdcard(self, args):
        print self._query('M20')

    def do_quit(self, args):
        '''quit the shell'''
        raise SystemExit


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

    shell = SerialCmd(device)
    shell.prompt = 'anet> '
    shell.cmdloop('starting...')

    device.close()
