"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013-2014 Alex Forencich

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
import struct

from .. import ivi
from .. import specan

AmplitudeUnitsMapping = {'dBm' : 'dbm',
                         'dBmV' : 'dbmv',
                         'dBuV' : 'dbuv',
                         'volt' : 'v',
                         'watt' : 'w'}
DetectorTypeMapping = {'maximum_peak' : 'pos',
                       'minimum_peak' : 'neg',
                       'sample' : 'smp'}
#TraceType = set(['clear_write', 'maximum_hold', 'minimum_hold', 'video_average', 'view', 'store'])
#VerticalScale = set(['linear', 'logarithmic'])
#AcquisitionStatus = set(['complete', 'in_progress', 'unknown'])

class agilent8590E(ivi.Driver, specan.Base):
    "Agilent 8590E series IVI spectrum analyzer driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(agilent8590E, self).__init__(*args, **kwargs)
        
        self._frequency_low = 9e3
        self._frequency_high = 1.8e9
        
        self._identity_description = "Agilent 8590E series IVI spectrum analyzer driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['8590L', '8591C', '8591E', '8591EM', '8592L', '8593E',
                        '8593EM', '8594E', '8594EM', '8594L', '8594Q', '8595E', '8595EM', '8596E', '8596EM']
        
        self._init_traces()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilent8590E, self).initialize(resource, id_query, reset, **keywargs)
        
        # interface clear
        if not self._driver_operation_simulate:
            self._clear()
        
        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)
        
        # reset
        if reset:
            self.utility.reset()
        
    
    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            #lst = self._ask("*IDN?").split(",")
            #self._identity_instrument_manufacturer = lst[0]
            #self._identity_instrument_model = lst[1]
            #self._identity_instrument_firmware_revision = lst[3]
            
            self._identity_instrument_manufacturer = "Agilent Technologies"
            self._identity_instrument_model = self._ask("ID?")
            self._identity_instrument_firmware_revision = self._ask("REV?")
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')
    
    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid():
            return self._identity_instrument_manufacturer
        self._load_id_string()
        return self._identity_instrument_manufacturer
    
    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        self._load_id_string()
        return self._identity_instrument_model
    
    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        self._load_id_string()
        return self._identity_instrument_firmware_revision
    
    def _utility_disable(self):
        pass
    
    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_code, error_message = self._ask(":system:error?").split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (error_code, error_message)
    
    def _utility_lock_object(self):
        pass
    
    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("*RST")
            self.driver_operation.invalidate_all_attributes()
    
    def _utility_reset_with_defaults(self):
        self._utility_reset()
    
    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            self._write("CNF?")
            # wait for test to complete
            time.sleep(40)
            # TODO any way to check status?
            code = int(self._read())
            if code != 0:
                message = "Self test failed"
        return (code, message)
    
    def _utility_unlock_object(self):
        pass
    
    def _get_level_amplitude_units(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("aunits?").lower()
            self._level_amplitude_units = [k for k,v in AmplitudeUnitsMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._level_amplitude_units
    
    def _set_level_amplitude_units(self, value):
        if value not in AmplitudeUnitsMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("aunits %s" % AmplitudeUnitsMapping[value])
        self._level_amplitude_units = value
        self._set_cache_valid()
    
    def _get_level_attenuation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._level_attenuation = float(self._ask("at?"))
            self._set_cache_valid()
        return self._level_attenuation
    
    def _set_level_attenuation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("at %e" % value)
        self._level_attenuation = value
        self._set_cache_valid()
    
    def _get_level_attenuation_auto(self):
        # TODO is it possible to read this?
        return self._level_attenuation_auto
    
    def _set_level_attenuation_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("at %s" % ('auto' if value else 'man'))
        self._level_attenuation_auto = value
        self._set_cache_valid()
    
    def _get_acquisition_detector_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("det?").lower()
            self._acquisition_detector_type = [k for k,v in DetectorTypeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._acquisition_detector_type
    
    def _set_acquisition_detector_type(self, value):
        if value not in DetectorTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":det %s" % DetectorTypeMapping[value])
        self._acquisition_detector_type = value
        self._set_cache_valid()
    
    def _get_acquisition_detector_type_auto(self):
        return self._acquisition_detector_type_auto
    
    def _set_acquisition_detector_type_auto(self, value):
        value = bool(value)
        self._acquisition_detector_type_auto = value
    
    def _get_frequency_start(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_start = float(self._ask("fa?"))
            self._set_cache_valid()
        return self._frequency_start
    
    def _set_frequency_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("fa %e" % value)
        self._frequency_start = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')
        self._set_cache_valid(False, 'sweep_coupling_sweep_time')
        self._set_cache_valid(False, 'sweep_coupling_video_bandwidth')
    
    def _get_frequency_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_stop = float(self._ask("fb?"))
            self._set_cache_valid()
        return self._frequency_stop
    
    def _set_frequency_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("fb %e" % value)
        self._frequency_stop = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')
        self._set_cache_valid(False, 'sweep_coupling_sweep_time')
        self._set_cache_valid(False, 'sweep_coupling_video_bandwidth')
    
    def _get_frequency_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_stop = float(self._ask("foffset?"))
            self._set_cache_valid()
        return self._frequency_offset
    
    def _set_frequency_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("foffset %e" % value)
        self._frequency_offset = value
        self._set_cache_valid()
    
    def _get_level_input_impedance(self):
        return self._level_input_impedance
    
    def _set_level_input_impedance(self, value):
        value = float(value)
        self._level_input_impedance = value
    
    def _get_acquisition_number_of_sweeps(self):
        return self._acquisition_number_of_sweeps
    
    def _set_acquisition_number_of_sweeps(self, value):
        value = int(value)
        self._acquisition_number_of_sweeps = value
    
    def _get_level_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._level_reference = float(self._ask("rl?"))
            self._set_cache_valid()
        return self._level_reference
    
    def _set_level_reference(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("rl %e" % value)
        self._level_reference = value
        self._set_cache_valid()
    
    def _get_level_reference_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._level_reference = float(self._ask("roffset?"))
            self._set_cache_valid()
        return self._level_reference_offset
    
    def _set_level_reference_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("roffset %e" % value)
        self._level_reference_offset = value
        self._set_cache_valid()
    
    def _get_sweep_coupling_resolution_bandwidth(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_resolution_bandwidth = float(self._ask("rb?"))
            self._set_cache_valid()
        return self._sweep_coupling_resolution_bandwidth
    
    def _set_sweep_coupling_resolution_bandwidth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("rb %e" % value)
        self._sweep_coupling_resolution_bandwidth = value
        self._set_cache_valid()
    
    def _get_sweep_coupling_resolution_bandwidth_auto(self):
        return self._sweep_coupling_resolution_bandwidth_auto
    
    def _set_sweep_coupling_resolution_bandwidth_auto(self, value):
        value = bool(value)
        self._sweep_coupling_resolution_bandwidth_auto = value
    
    def _get_acquisition_sweep_mode_continuous(self):
        return self._acquisition_sweep_mode_continuous
    
    def _set_acquisition_sweep_mode_continuous(self, value):
        value = bool(value)
        self._acquisition_sweep_mode_continuous = value
    
    def _get_sweep_coupling_sweep_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_sweep_time = float(self._ask("st?"))
            self._set_cache_valid()
        return self._sweep_coupling_sweep_time
        self._set_cache_valid()
    
    def _set_sweep_coupling_sweep_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("st %e" % value)
        self._sweep_coupling_sweep_time = value
    
    def _get_sweep_coupling_sweep_time_auto(self):
        return self._sweep_coupling_sweep_time_auto
    
    def _set_sweep_coupling_sweep_time_auto(self, value):
        value = bool(value)
        self._sweep_coupling_sweep_time_auto = value
    
    def _get_trace_type(self, index):
        index = ivi.get_index(self._trace_name, index)
        return self._trace_type[index]
    
    def _set_trace_type(self, index, value):
        index = ivi.get_index(self._trace_name, index)
        if value not in TraceType:
            raise ivi.ValueNotSupportedException()
        self._trace_type[index] = value
    
    def _get_acquisition_vertical_scale(self):
        return self._acquisition_vertical_scale
    
    def _set_acquisition_vertical_scale(self, value):
        value = float(value)
        self._acquisition_vertical_scale = value
    
    def _get_sweep_coupling_video_bandwidth(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_resolution_bandwidth = float(self._ask("vb?"))
            self._set_cache_valid()
        return self._sweep_coupling_video_bandwidth
    
    def _set_sweep_coupling_video_bandwidth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("vb %e" % value)
            self._set_cache_valid()
        self._sweep_coupling_video_bandwidth = value
    
    def _get_sweep_coupling_video_bandwidth_auto(self):
        return self._sweep_coupling_video_bandwidth_auto
    
    def _set_sweep_coupling_video_bandwidth_auto(self, value):
        value = bool(value)
        self._sweep_coupling_video_bandwidth_auto = value
    
    def _acquisition_abort(self):
        pass
    
    def _acquisition_status(self):
        return 'unknown'
    
    def _trace_fetch_y(self, index):
        index = ivi.get_index(self._trace_name, index)
        
        if self._driver_operation_simulate:
            return list()
        
        cmd = ''
        
        if index == 0:
            cmd = 'tra?'
        elif index == 1:
            cmd = 'trb?'
        elif index == 2:
            cmd = 'trc?'
        else:
            return list()
        
        self._write('tdf p')
        l = self._ask(cmd)
        
        data = list()
        
        for p in l.split(','):
            data.append(float(p))
        
        return data
    
    def _acquisition_initiate(self):
        pass
    
    def _trace_read_y(self, index):
        return self._trace_fetch_y(index)
    
    