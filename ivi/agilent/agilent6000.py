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
import time
from .agilentBaseInfiniiVision import *

CaptureModes={
    'maximum':'maximum',
    'normal':'normal',
    'raw':'raw'}


class agilent6000(agilentBaseInfiniiVision):
    "Agilent InfiniiVision 6000 series IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(agilent6000, self).__init__(*args, **kwargs)
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9
        
        self._identity_description = "Agilent InfiniiVision 6000 series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DSO6012A','DSO6014A','DSO6032A',
                'DSO6034A','DSO6052A','DSO6054A','DSO6102A','DSO6104A','MSO6012A','MSO6014A',
                'MSO6032A','MSO6034A','MSO6052A','MSO6054A','MSO6102A','MSO6104A']

        self._init_channels()

        self._add_property('acquisition.capture_mode',
                self._get_acquisition_capture_mode,
                self._set_acquisition_capture_mode,
                None,
                ivi.Doc("""
                Choose between the different capture modes on the scope, normal, raw and maximum, raises
                and exception for other modes selected. Using raw capture mode allows all points to be pulled back
                """))
        self._add_method('channels[].measurement.fetch_waveform_single',
                        self._measurement_fetch_waveform_single,
                        ivi.Doc(""" someing
                        """))


    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        self._acquisition_number_of_points_minimum = value
        if not self._driver_operation_simulate:
            self._write(":waveform:points %d" % value)
        self._set_cache_valid()
        self._set_cache_valid(False, 'acquisition_record_length')

    def _set_acquisition_capture_mode(self,value):
        if value not in CaptureModes:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":stop")
            self._write(":acquire:count 1")
            self._write(":waveform:points:mode %s" % value)
        self._set_cache_valid()
        self._set_cache_valid(False, 'acquisition_record_length')

    def _get_acquisition_capture_mode(self):
        if not self._driver_operation_simulate:
            return self._ask(':waveform:points:mode?')

    def _measurement_single_shot_initiate(self):
        self._write(':stop')
        self._write(':single')
        while True:
            if '+1' in self._ask(':AER?'):
                break
            time.sleep(0.001)

    def _measurement_fetch_waveform_single(self, index):
        index = ivi.get_index(self._channel_name, index)

        if self._driver_operation_simulate:
            return list()
        while True:
            if int(self._ask(':OPERegister:CONDition?')) & 8 !=8:
                break
            time.sleep(0.001)
        self._write(":waveform:byteorder msbfirst")
        self._write(":waveform:unsigned 1")
        self._write(":waveform:format word")
        self._write(":waveform:source %s" % self._channel_name[index])

        # Read preamble

        pre = self._ask(":waveform:preamble?").split(',')

        format = int(pre[0])
        type = int(pre[1])
        points = int(pre[2])
        count = int(pre[3])
        xincrement = float(pre[4])
        xorigin = float(pre[5])
        xreference = int(float(pre[6]))
        yincrement = float(pre[7])
        yorigin = float(pre[8])
        yreference = int(float(pre[9]))

        if type == 1:
            raise scope.InvalidAcquisitionTypeException()

        if format != 1:
            raise UnexpectedResponseException()

        self._write(":waveform:data?")

        # Read waveform data
        raw_data = raw_data = self._read_ieee_block()

        # Split out points and convert to time and voltage pairs

        data = list()
        for i in range(points):
            x = ((i - xreference) * xincrement) + xorigin

            yval = struct.unpack(">H", raw_data[i*2:i*2+2])[0]

            if yval == 0:
                # hole value
                y = float('nan')
            else:
                y = ((yval - yreference) * yincrement) + yorigin

            data.append((x, y))

        return data


    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)

        if self._driver_operation_simulate:
            return list()

        self._write(":waveform:byteorder msbfirst")
        self._write(":waveform:unsigned 1")
        self._write(":waveform:format word")
        self._write(":waveform:source %s" % self._channel_name[index])

        # Read preamble

        pre = self._ask(":waveform:preamble?").split(',')

        format = int(pre[0])
        type = int(pre[1])
        points = int(pre[2])
        count = int(pre[3])
        xincrement = float(pre[4])
        xorigin = float(pre[5])
        xreference = int(float(pre[6]))
        yincrement = float(pre[7])
        yorigin = float(pre[8])
        yreference = int(float(pre[9]))

        if type == 1:
            raise scope.InvalidAcquisitionTypeException()

        if format != 1:
            raise UnexpectedResponseException()

        self._write(":waveform:data?")

        # Read waveform data
        raw_data = raw_data = self._read_ieee_block()

        # Split out points and convert to time and voltage pairs

        data = list()
        for i in range(points):
            x = ((i - xreference) * xincrement) + xorigin

            yval = struct.unpack(">H", raw_data[i*2:i*2+2])[0]

            if yval == 0:
                # hole value
                y = float('nan')
            else:
                y = ((yval - yreference) * yincrement) + yorigin

            data.append((x, y))

        return data