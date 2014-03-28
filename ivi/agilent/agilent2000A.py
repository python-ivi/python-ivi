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

from .. import ivi
from .. import fgen

ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'bmp8': 'bmp8bit',
        'png': 'png',
        'png24': 'png'}

OutputMode = set(['function'])
OperationMode = set(['continuous', 'burst'])
StandardWaveformMapping = {
        'sine': 'sin',
        'square': 'squ',
        #'triangle': 'tri',
        'ramp_up': 'ramp',
        #'ramp_down',
        #'dc'
        'pulse': 'puls',
        'noise': 'nois',
        'dc': 'dc'
        }

class agilent2000A(agilentBaseScope, fgen.Base, fgen.StdFunc, fgen.ModulateAM, fgen.ModulateFM):
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
        
        self._horizontal_divisions = 10
        self._vertical_divisions = 8

        # wavegen option
        self._output_count = 1
        
        self._identity_description = "Agilent InfiniiVision 2000A X-series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DSOX2002A','DSOX2004A','DSOX2012A',
                'DSOX2014A','DSOX2022A','DSOX2024A','MSOX2002A','MSOX2004A','MSOX2012A','MSOX2014A',
                'MSOX2022A','MSOX2024A']

        self._init_outputs()
        
    def _init_outputs(self):
        try:
            super(agilent2000A, self)._init_outputs()
        except AttributeError:
            pass
        self._output_name = list()
        self._output_operation_mode = list()
        self._output_enabled = list()
        self._output_impedance = list()
        self._output_mode = list()
        self._output_reference_clock_source = list()
        for i in range(self._output_count):
            if self._output_count == 1:
                self._output_name.append("wgen")
            else:
                self._output_name.append("wgen%d" % (i+1))
            self._output_operation_mode.append('continuous')
            self._output_enabled.append(False)
            self._output_impedance.append(50)
            self._output_mode.append('function')
            self._output_reference_clock_source.append('')
        
        self.outputs._set_list(self._output_name)

    # wavegen option
    def _get_output_operation_mode(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_operation_mode[index]
    
    def _set_output_operation_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in OperationMode:
            raise ivi.ValueNotSupportedException()
        self._output_operation_mode[index] = value
    
    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:output?" % self._output_name[index])
            self._output_standard_waveform_amplitude[index] = bool(int(resp))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]
    
    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:output %d" % (self._output_name[index], value))
        self._output_enabled[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            val = self._ask(":%s:output:load?" % self._output_name[index])
            if val == 'ONEM':
                self._output_impedance[index] = 1000000
            elif val == 'FIFT':
                self._output_impedance[index] = 50
            self._set_cache_valid(index=index)
        return self._output_impedance[index]
    
    def _set_output_impedance(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if value != 50 and value != 1000000:
            raise Exception('Invalid impedance selection')
        if not self._driver_operation_simulate:
            if value == 1000000:
                self._write(":%s:output:load onemeg" % self._output_name[index])
            elif value == 50:
                self._write(":%s:output:load fifty" % self._output_name[index])
        self._output_impedance[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, 'output_standard_waveform_amplitude', index)
    
    def _get_output_mode(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_mode[index]
    
    def _set_output_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in OutputMode:
            raise ivi.ValueNotSupportedException()
        self._output_mode[index] = value
    
    def _get_output_reference_clock_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_reference_clock_source[index]
    
    def _set_output_reference_clock_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = 'internal'
        self._output_reference_clock_source[index] = value
    
    def abort_generation(self):
        pass
    
    def initiate_generation(self):
        pass

    def _get_output_standard_waveform_amplitude(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:voltage?" % self._output_name[index])
            self._output_standard_waveform_amplitude[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_amplitude[index]
    
    def _set_output_standard_waveform_amplitude(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:voltage %e" % (self._output_name[index], value))
        self._output_standard_waveform_amplitude[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_dc_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:voltage:offset?" % self._output_name[index])
            self._output_standard_waveform_dc_offset[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_dc_offset[index]
    
    def _set_output_standard_waveform_dc_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:voltage:offset %e" % (self._output_name[index], value))
        self._output_standard_waveform_dc_offset[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_duty_cycle_high(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:function:square:dcycle?" % self._output_name[index])
            self._output_standard_waveform_duty_cycle_high[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_duty_cycle_high[index]
    
    def _set_output_standard_waveform_duty_cycle_high(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 20.0 or value > 80.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:function:square:dcycle %e" % (self._output_name[index], value))
        self._output_standard_waveform_duty_cycle_high[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_standard_waveform_start_phase(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_start_phase[index]
    
    def _set_output_standard_waveform_start_phase(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_start_phase[index] = value

    def _get_output_standard_waveform_frequency(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:frequency?" % self._output_name[index])
            self._output_standard_waveform_frequency[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_frequency[index]
    
    def _set_output_standard_waveform_frequency(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:frequency %e" % (self._output_name[index], value))
        self._output_standard_waveform_frequency[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_standard_waveform_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:function?" % self._output_name[index])
            value = resp.lower()
            value = [k for k,v in StandardWaveformMapping.items() if v==value][0]
            self._output_standard_waveform_waveform[index] = value
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_waveform[index]
    
    def _set_output_standard_waveform_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in StandardWaveformMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":%s:function %s" % (self._output_name[index], StandardWaveformMapping[value]))
        self._output_standard_waveform_waveform[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_am_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_am_enabled[index]
    
    def _set_output_am_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_am_enabled[index] = value
    
    def _get_output_am_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_am_source[index]
    
    def _set_output_am_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = 'internal'
        self._output_am_source[index] = value
    
    def _get_am_internal_depth(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask(":%s:modulation:am:depth?" % self._output_name[index])
            self._am_internal_depth = float(resp)
            self._set_cache_valid()
        return self._am_internal_depth
    
    def _set_am_internal_depth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:modulation:am:depth %e" % (self._output_name[index], value))
        self._am_internal_depth = value
        self._set_cache_valid()
    
    def _get_am_internal_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask(":%s:modulation:am:frequency?" % self._output_name[index])
            self._am_internal_frequency = float(resp)
            self._set_cache_valid()
        return self._am_internal_frequency
    
    def _set_am_internal_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:modulation:am:frequency %e" % (self._output_name[index], value))
        self._am_internal_frequency = value
        self._set_cache_valid()

    def _get_am_internal_waveform(self):
        return self._am_internal_waveform
    
    def _set_am_internal_waveform(self, value):
        value = float(value)
        self._am_internal_waveform = value
    
    def _get_output_fm_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_fm_enabled[index]
    
    def _set_output_fm_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_fm_enabled[index] = value
    
    def _get_output_fm_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_fm_source[index]
    
    def _set_output_fm_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = 'internal'
        self._output_fm_source[index] = value
    
    def _get_fm_internal_deviation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask(":%s:modulation:fm:deviation?" % self._output_name[index])
            self._fm_internal_deviation = float(resp)
            self._set_cache_valid()
        return self._fm_internal_deviation
    
    def _set_fm_internal_deviation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:modulation:fm:deviation %e" % (self._output_name[index], value))
        self._fm_internal_deviation = value
        self._set_cache_valid()
    
    def _get_fm_internal_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask(":%s:modulation:fm:frequency?" % self._output_name[index])
            self._fm_internal_frequency = float(resp)
            self._set_cache_valid()
        return self._fm_internal_frequency
    
    def _set_fm_internal_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:modulation:fm:frequency %e" % (self._output_name[index], value))
        self._fm_internal_frequency = value
        self._set_cache_valid()
    
    def _get_fm_internal_waveform(self):
        return self._fm_internal_waveform
    
    def _set_fm_internal_waveform(self, value):
        value = float(value)
        self._fm_internal_waveform = value
    
