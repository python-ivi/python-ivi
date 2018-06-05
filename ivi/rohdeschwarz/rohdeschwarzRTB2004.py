"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2017-2018 Acconeer AB

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

from .rohdeschwarzBaseScope import *

BandwidthMapping = {
        100e6: 'full',
        20e6:  'b20'}

class rohdeschwarzRTB2004(rohdeschwarzBaseScope):
    "Rohde&Schwarz RTB2004 IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'RTB2004')
        
        super(rohdeschwarzRTB2004, self).__init__(*args, **kwargs)
        
        self._analog_channel_count = 4
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 70e6
        self._horizontal_divisions = 12
        self._vertical_divisions = 10
        self._trigger_holdoff_min = 51.2e-9
        self._channel_offset_max = 1.2
        
        self._init_channels()
