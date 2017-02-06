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

from .agilent2000A import *

import numpy as np
import struct

from .. import ivi
from .. import fgen

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

class agilent3000A(agilent2000A, fgen.ArbWfm, fgen.ArbFrequency,
                fgen.ArbChannelWfm):
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
        self._output_standard_waveform_mapping = StandardWaveformMapping
        self._output_mode_list = OutputMode
        self._arbitrary_sample_rate = 0
        self._arbitrary_waveform_number_waveforms_max = 0
        self._arbitrary_waveform_size_max = 8192
        self._arbitrary_waveform_size_min = 2
        self._arbitrary_waveform_quantum = 1
        
        self._identity_description = "Agilent InfiniiVision 3000A X-series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DSOX3012A','DSOX3014A','DSOX3024A',
                'DSOX3032A','DSOX3034A','DSOX3052A','DSOX3054A','DSOX3104A','MSOX3012A','MSOX3014A',
                'MSOX3024A','MSOX3032A','MSOX3034A','MSOX3052A','MSOX3054A','MSOX3104A']

        self._init_outputs()
        self._init_channels()
        
    
    def _get_output_arbitrary_gain(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_gain[index]

    def _set_output_arbitrary_gain(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_arbitrary_gain[index] = value

    def _get_output_arbitrary_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_offset[index]

    def _set_output_arbitrary_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_arbitrary_offset[index] = value

    def _get_output_arbitrary_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_waveform[index]

    def _set_output_arbitrary_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_arbitrary_waveform[index] = value

    def _get_arbitrary_sample_rate(self):
        return self._arbitrary_sample_rate

    def _set_arbitrary_sample_rate(self, value):
        value = float(value)
        self._arbitrary_sample_rate = value

    def _get_arbitrary_waveform_number_waveforms_max(self):
        return self._arbitrary_waveform_number_waveforms_max

    def _get_arbitrary_waveform_size_max(self):
        return self._arbitrary_waveform_size_max

    def _get_arbitrary_waveform_size_min(self):
        return self._arbitrary_waveform_size_min

    def _get_arbitrary_waveform_quantum(self):
        return self._arbitrary_waveform_quantum

    def _arbitrary_waveform_clear(self, handle):
        pass

    def _arbitrary_waveform_configure(self, index, handle, gain, offset):
        self._set_output_arbitrary_waveform(index, handle)
        self._set_output_arbitrary_gain(index, gain)
        self._set_output_arbitrary_offset(index, offset)

    def _arbitrary_waveform_create(self, data):
        return "handle"

    def _get_output_arbitrary_frequency(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_frequency[index]

    def _set_output_arbitrary_frequency(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_arbitrary_frequency[index] = value

    def _arbitrary_waveform_create_channel_waveform(self, index, data):
        y = None
        x = None
        if type(data) == list and type(data[0]) == float:
            # list
            y = array(data)
        elif type(data) == np.ndarray and len(data.shape) == 1:
            # 1D array
            y = data
        elif type(data) == np.ndarray and len(data.shape) == 2 and data.shape[0] == 1:
            # 2D array, hieght 1
            y = data[0]
        elif type(data) == np.ndarray and len(data.shape) == 2 and data.shape[1] == 1:
            # 2D array, width 1
            y = data[:,0]
        else:
            x, y = ivi.get_sig(data)

        if len(y) % self._arbitrary_waveform_quantum != 0:
            raise ivi.ValueNotSupportedException()

        raw_data = b''

        for f in y:
            # clip at -1 and 1
            if f > 1.0: f = 1.0
            if f < -1.0: f = -1.0

            raw_data = raw_data + struct.pack('<f', f)

        self._write_ieee_block(raw_data, ':%s:arbitrary:data ' % self._output_name[index])

        return self._output_name[index]


    
