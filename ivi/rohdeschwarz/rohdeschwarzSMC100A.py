# coding=utf-8
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) Acconeer AB, 2018

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

from .rohdeschwarzBaseRFSigGen import *


class rohdeschwarzSMC100A(rohdeschwarzBaseRFSigGen):
    "Rohde&Schwarz SMC 100A RF Signal Generator"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'SMC100A')
        
        super(rohdeschwarzSMC100A, self).__init__(*args, **kwargs)

        # frequency limit in Hertz
        self._frequency_low = 9e3
        self._frequency_high = 1100e6        
        # rf level limit in dBm
        self._rf_level_low = -120.0
        self._rf_level_high = 19
        # rf rms voltage level limit in Volt
        self._rf_rms_voltage_level_low = 223.61e-9
        self._rf_rms_voltage_level_high = 1.993

        self._initialize(*args, **kwargs)
