"""

Python Interchangeable Virtual Instrument Library
Driver for Test Equity Model 140

Copyright (c) 2014-2017 Jeff Wurzbach

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

from .. import ivi
from .. import ics
from .testequityf4 import *



class testequity140(testequityf4, ics.ics8099):
    "TestEquity Model 140 Thermal Chamber"

    def __init__(self, *args, **kwargs):
        #self.__dict__.setdefault('_instrument_id', '8099')

        super(testequity140, self).__init__(*args, **kwargs)

        self._identity_description = "TestEquity Model 140 Thermal Chamber"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = "TestEquity"
        self._identity_instrument_manufacturer = "TestEquity"
        self._identity_instrument_model = "140"
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['140']
        
        """
        self._add_method('read_register',
                         self._read_register,
                         "Read Modbus register")
        self._add_method('write_register',
                         self._write_register,
                         "Write Modbus register")

        """


