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

from .agilent2000A import *

OutputMode = set(['function', 'arbitrary'])
StandardWaveformMapping = {
        'sine': 'sin',
        'square': 'squ',
        #'triangle': 'tri',
        'ramp_up': 'ramp',
        #'ramp_down',
        #'dc'
        'pulse': 'puls',
        'noise': 'nois',
        'dc': 'dc',
        'sinc': 'sinc',
        'exprise': 'expr',
        'expfall': 'expf',
        'cardiac': 'card',
        'gaussian': 'gaus'
        }

class agilent3000A(agilent2000A):
    "Agilent InfiniiVision 3000A series IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(agilent3000A, self).__init__(*args, **kwargs)
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9
        
        self._horizontal_divisions = 10
        self._vertical_divisions = 8

        # wavegen option
        self._output_count = 1
        
        self._identity_description = "Agilent InfiniiVision 3000A X-series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DSOX3012A','DSOX3014A','DSOX3024A',
                'DSOX3032A','DSOX3034A','DSOX3052A','DSOX3054A','DSOX3104A','MSOX3012A','MSOX3014A',
                'MSOX3024A','MSOX3032A','MSOX3034A','MSOX3052A','MSOX3054A','MSOX3104A']

        self._init_outputs()
        
    
    
