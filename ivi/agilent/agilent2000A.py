"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

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

from .agilentBaseScope import *

ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'bmp8': 'bmp8bit',
        'png': 'png',
        'png24': 'png'}

class agilent2000A(agilentBaseScope):
    "Agilent InfiniiVision 2000A series IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(agilent2000A, self).__init__(*args, **kwargs)
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 200e6
        
        self._identity_description = "Agilent InfiniiVision 2000A X-series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DSOX2002A','DSOX2004A','DSOX2012A',
                'DSOX2014A','DSOX2022A','DSOX2024A','MSOX2002A','MSOX2004A','MSOX2012A','MSOX2014A',
                'MSOX2022A','MSOX2024A']
        
    
    
