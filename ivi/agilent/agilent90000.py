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

VerticalCoupling = set(['dc'])
ScreenshotImageFormatMapping = {
        'tif': 'tif',
        'tiff': 'tif',
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'png': 'png',
        'png24': 'png',
        'jpg': 'jpg',
        'jpeg': 'jpg',
        'gif': 'gif'}

class agilent90000(agilentBaseScope):
    "Agilent Infiniium 90000A/90000X series IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_common_mode = list()
        self._channel_differential = list()
        self._channel_differential_skew = list()
        
        super(agilent90000, self).__init__(*args, **kwargs)
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 13e9
        
        self._identity_description = "Agilent Infiniium 90000A/90000X series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DSO90254A','DSO90404A','DSO90604A',
                'DSO90804A','DSO91204A','DSO91304A','DSOX91304A','DSOX91604A','DSOX92004A',
                'DSOX92504A','DSOX92804A','DSOX93204A','DSA90254A','DSA90404A','DSA90604A',
                'DSA90804A','DSA91204A','DSA91304A','DSAX91304A','DSAX91604A','DSAX92004A',
                'DSAX92504A','DSAX92804A','DSAX93204A','MSOX91304A','MSOX91604A','MSOX92004A',
                'MSOX92504A','MSOX92804A','MSOX93204A']
        
        ivi.add_property(self, 'channels[].common_mode',
                        self._get_channel_common_mode,
                        self._set_channel_common_mode)
        ivi.add_property(self, 'channels[].differential',
                        self._get_channel_differential,
                        self._set_channel_differential)
        ivi.add_property(self, 'channels[].differential_skew',
                        self._get_channel_differential_skew,
                        self._set_channel_differential_skew)
        
        self._init_channels()
        
    
    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_code = self._ask(":system:error?")
            error_code = int(error_code)
            if error_code != 0:
                error_message = "Unknown"
        return (error_code, error_message)
    
    def _init_channels(self):
        super(agilent90000, self)._init_channels()
        
        self._channel_common_mode = list()
        self._channel_differential = list()
        self._channel_differential_skew = list()
        
        for i in range(self._analog_channel_count):
            self._channel_common_mode.append(False)
            self._channel_differential.append(False)
            self._channel_differential_skew.append(0)
    
    
    def _display_fetch_screenshot(self, format='png', invert=False):
        if self._driver_operation_simulate:
            return b''
        
        if format not in ScreenshotImageFormatMapping:
            raise ivi.ValueNotSupportedException()
        
        format = ScreenshotImageFormatMapping[format]
        
        self._write(":display:data? %s, screen, on, %s" % (format, 'invert' if invert else 'normal'))
        
        return self._read_ieee_block()
    
    def _get_channel_common_mode(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_common_mode[index] = bool(int(self._ask(":%s:commonmode?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_common_mode[index]
    
    def _set_channel_common_mode(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:commonmode %d" % (self._channel_name[index], int(value)))
        self._channel_common_mode[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_differential(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_differential[index] = bool(int(self._ask(":%s:differential?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_differential[index]
    
    def _set_channel_differential(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:differential %d" % (self._channel_name[index], int(value)))
        self._channel_differential[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_differential_skew(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_differential_skew[index] = float(self._ask(":%s:differential:skew?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_differential_skew[index]
    
    def _set_channel_differential_skew(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:differential:skew %e" % (self._channel_name[index], value))
        self._channel_differential_skew[index] = value
        self._set_cache_valid(index=index)
    
    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        if self._driver_operation_simulate:
            return list()
        
        self._write(":waveform:byteorder msbfirst")
        self._write(":waveform:unsigned 1")
        self._write(":waveform:format word")
        self._write(":waveform:points normal")
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
        
        if format != 2:
            raise UnexpectedResponseException()
        
        self._write(":waveform:data?")
        
        # Read waveform data
        raw_data = self._read_ieee_block()
        
        # Split out points and convert to time and voltage pairs
        
        data = list()
        for i in range(points):
            x = ((i - xreference) * xincrement) + xorigin
            
            yval = struct.unpack(">h", raw_data[i*2:i*2+2])[0]
            y = ((yval - yreference) * yincrement) + yorigin
            
            data.append((x, y))
        
        return data
    
    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)
    
    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(":acquire:complete 100")
            self._write(":digitize")
            self._set_cache_valid(False, 'trigger_continuous')
    
    
    


