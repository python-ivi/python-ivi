"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013-2017 Alex Forencich

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

from .agilentBase8590 import *

class agilentBase8590A(agilentBase8590):
    "Agilent 8590A series IVI spectrum analyzer driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(agilentBase8590A, self).__init__(*args, **kwargs)

        self._identity_description = "Agilent 8590 series IVI spectrum analyzer driver"
        self._identity_supported_instrument_models = ['8590A', '8590B', '8591A', '8592A', '8592B',
                                                      '8593A', '8594A', '8595A']


    def _display_fetch_screenshot(self, format='bmp', invert=False):
        if self._driver_operation_simulate:
            return b''

        #if format not in ScreenshotImageFormatMapping:
        #    raise ivi.ValueNotSupportedException()

        #format = ScreenshotImageFormatMapping[format]

        self._write("PRINT 1")

        rtl = io.BytesIO(self._read_raw())

        img = hprtl.parse_hprtl(rtl)

        # rescale to get white background
        # presuming background of (90, 88, 85)
        img[:,:,0] *= 255/90
        img[:,:,1] *= 255/88
        img[:,:,2] *= 255/85

        bmp = hprtl.generate_bmp(img)

        return bmp

