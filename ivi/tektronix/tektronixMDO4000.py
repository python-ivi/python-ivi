"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2016-2017 Alex Forencich

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

from .tektronixMSO4000 import *

class tektronixMDO4000(tektronixMSO4000):
    "Tektronix MDO4000 series IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'MDO4000')
        self._rf_channel_count = 7

        super(tektronixMDO4000, self).__init__(*args, **kwargs)

        self._analog_channel_count = 4
        self._digital_channel_count = 16
        self._rf_channel_name = list()
        self._rf_channel_count = 7
        self._bandwidth = 1e9
        self._rf_bandwidth = 6e9

        self._identity_description = "Tektronix MDO4000 series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['MDO4054', 'MDO4104', 'MDO4014B',
                'MDO4034B', 'MDO4054B', 'MDO4104B']

        self._init_channels()

    def _init_channels(self):
        self._rf_channel_count = 7 if self._rf_channel_count > 0 else 0
        self._channel_count = self._analog_channel_count + self._digital_channel_count + self._rf_channel_count

        try:
            super(tektronixMDO4000, self)._init_channels()
        except AttributeError:
            pass

        # RF channels
        self._rf_channel_name = list()

        if (self._rf_channel_count > 0):
            self._rf_channel_name = ['rf_amplitude', 'rf_average', 'rf_frequency', 'rf_maxhold',
                'rf_minhold', 'rf_normal', 'rf_phase']
            self._channel_label.extend(['']*7)
            self._channel_name.extend(self._rf_channel_name)

        self.channels._set_list(self._channel_name)
        self._channel_name_dict = ivi.get_index_dict(self._channel_name)

    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._channel_name[index].index('rf_') == 0:
                self._channel_label[index] = self._ask(":rf:%s:label?" % self._channel_name[index]).strip('"')
            else:
                self._channel_label[index] = self._ask(":%s:label?" % self._channel_name[index]).strip('"')
            self._set_cache_valid(index=index)
        return self._channel_label[index]

    def _set_channel_label(self, index, value):
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            if self._channel_name[index].index('rf_') == 0:
                self._write(":rf:%s:label \"%s\"" % (self._channel_name[index], value))
            else:
                self._write(":%s:label \"%s\"" % (self._channel_name[index], value))
        self._channel_label[index] = value
        self._set_cache_valid(index=index)
