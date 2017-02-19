"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import Gpib
import re

def parse_visa_resource_string(resource_string):
    # valid resource strings:
    # GPIB::10::INSTR
    # GPIB0::10::INSTR
    m = re.match('^(?P<prefix>(?P<type>GPIB)\d*)(::(?P<arg1>[^\s:]+))(::(?P<suffix>INSTR))$',
            resource_string, re.I)

    if m is not None:
        return dict(
                type = m.group('type').upper(),
                prefix = m.group('prefix'),
                arg1 = m.group('arg1'),
                suffix = m.group('suffix'),
        )

# linux-gpib timeout constants, in milliseconds. See self.timeout.
TIMETABLE = (0, 1e-2, 3e-2, 1e-1, 3e-1, 1e0, 3e0, 1e1, 3e1, 1e2, 3e2, 1e3, 3e3,
             1e4, 3e4, 1e5, 3e5, 1e6)

class LinuxGpibInstrument(object):
    "Linux GPIB wrapper instrument interface client"
    def __init__(self, name = 'gpib0', pad = None, sad = 0, timeout = 13, send_eoi = 1, eos_mode = 0):

        if name.upper().startswith('GPIB') and '::' in name:
            res = parse_visa_resource_string(name)

            if res is None:
                raise IOError("Invalid resource string")

            index = res['prefix'][4:]
            if len(index) > 0:
                index = int(index)
            else:
                index = 0

            addr = int(res['arg1'])

            name = index
            pad = addr

        self.gpib = Gpib.Gpib(name, pad, sad, timeout, send_eoi, eos_mode)

    def write_raw(self, data):
        "Write binary data to instrument"
        
        self.gpib.write(data)

    def read_raw(self, num=-1):
        "Read binary data from instrument"
        
        if num < 0:
            num = 512
        
        return self.gpib.read(num)
    
    def ask_raw(self, data, num=-1):
        "Write then read binary data"
        self.write_raw(data)
        return self.read_raw(num)
    
    def write(self, message, encoding = 'utf-8'):
        "Write string to instrument"
        if type(message) is tuple or type(message) is list:
            # recursive call for a list of commands
            for message_i in message:
                self.write(message_i, encoding)
            return

        self.write_raw(str(message).encode(encoding))

    def read(self, num=-1, encoding = 'utf-8'):
        "Read string from instrument"
        return self.read_raw(num).decode(encoding).rstrip('\r\n')

    def ask(self, message, num=-1, encoding = 'utf-8'):
        "Write then read string"
        if type(message) is tuple or type(message) is list:
            # recursive call for a list of commands
            val = list()
            for message_i in message:
                val.append(self.ask(message_i, num, encoding))
            return val

        self.write(message, encoding)
        return self.read(num, encoding)
    
    def read_stb(self):
        "Read status byte"
        raise NotImplementedError()
    
    def trigger(self):
        "Send trigger command"
        
        self.gpib.trigger()
    
    def clear(self):
        "Send clear command"
        
        self.gpib.clear()
    
    def remote(self):
        "Send remote command"
        raise NotImplementedError()
    
    def local(self):
        "Send local command"
        raise NotImplementedError()
    
    def lock(self):
        "Send lock command"
        raise NotImplementedError()
    
    def unlock(self):
        "Send unlock command"
        raise NotImplementedError()

    @property
    def timeout(self):
        # 0x3 is the hexadecimal reference to the IbaTMO (timeout) configuration
        # option in linux-gpib.
        return TIMETABLE[self.gpib.ask(3)] * 1000.

    @timeout.setter
    def timeout(self, value):
        """
        linux-gpib only supports 18 discrete timeout values. If a timeout
        value other than these is requested, it will be rounded up to the closest
        available value. Values greater than the largest available timout value
        will instead be rounded down. The available timeout values are:
        0   Never timeout.
        1   10 microseconds
        2   30 microseconds
        3   100 microseconds
        4   300 microseconds
        5   1 millisecond
        6   3 milliseconds
        7   10 milliseconds
        8   30 milliseconds
        9   100 milliseconds
        10  300 milliseconds
        11  1 second
        12  3 seconds
        13  10 seconds
        14  30 seconds
        15  100 seconds
        16  300 seconds
        17  1000 seconds
        """
        self.gpib.timeout(bisect(TIMETABLE, value/1000.))