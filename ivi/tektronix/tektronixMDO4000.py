"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2016 Alex Forencich

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

        super(tektronixMDO4000, self).__init__(*args, **kwargs)

        self._analog_channel_count = 4
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9

        self._identity_description = "Tektronix MDO4000 series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['MDO4054', 'MDO4104', 'MDO4014B',
                'MDO4034B', 'MDO4054B', 'MDO4104B']

        self._init_channels()

    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)

        if self._driver_operation_simulate:
            return list()

        self._write(":wfmoutpre:encdg binary")
        if sys.byteorder == 'little':
            self._write(":wfmoutpre:byt_or lsb")
        else:
            self._write(":wfmoutpre:byt_or msb")
        self._write(":wfmoutpre:byt_nr 2")
        self._write(":wfmoutpre:bn_fmt rp")
        self._write(":wfmoutpre:pt_fmt y")
        self._write(":wfmoutpre:domain time")
        self._write(":data:source %s" % self._channel_name[index])

        # Read preamble

        pre = self._ask(":wfmoutpre?").split(';')

        format = pre[7].strip()
        points = int(pre[6])
        xincr = float(pre[10])
        xzero = float(pre[11])
        ymult = float(pre[14])
        yoff = float(pre[15])
        yzero = int(float(pre[16]))

        if type == 1:
            raise scope.InvalidAcquisitionTypeException()

        if format != 'Y':
            raise UnexpectedResponseException()

        # Read waveform data
        raw_data = self._ask_for_ieee_block(":curve?")

        # Split out points and convert to time and voltage pairs
        y_data = array.array('H', raw_data)

        data = [((i * xincr) + xzero, ((y - yoff) * ymult) + yzero) for i, y in enumerate(y_data)]

        return data
