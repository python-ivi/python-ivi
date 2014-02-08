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

from .. import ivi
from .. import pwrmeter

import time

class agilent436A(ivi.Driver, pwrmeter.Base, pwrmeter.ZeroCorrection, pwrmeter.ManualRange):
    "Agilent 436A RF power meter"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '436A')
        
        super(agilent436A, self).__init__(*args, **kwargs)
        
        self._identity_description = "Agilent 436A RF power meter driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['436A']
        
        self._init_channels()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilent436A, self).initialize(resource, id_query, reset, **keywargs)
        
        # configure interface
        if self._interface is not None:
            self._interface.term_char = '\n'
        
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
            self.utility_reset()
        
    
    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            #lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = "HP"
            self._identity_instrument_model = "436A"
            self._identity_instrument_firmware_revision = "Unknown"
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
        #if not self._driver_operation_simulate:
        #    error_code, error_message = self._ask(":system:error?").split(',')
        #    error_code = int(error_code)
        #    error_message = error_message.strip(' "')
        return (error_code, error_message)
    
    def _utility_lock_object(self):
        pass
    
    def _utility_reset(self):
        if not self._driver_operation_simulate:
            #self._write("*RST")
            self._clear()
            self.driver_operation.invalidate_all_attributes()
    
    def _utility_reset_with_defaults(self):
        self._utility_reset()
    
    def _utility_self_test(self):
        #code = 0
        #message = "Self test passed"
        #if not self._driver_operation_simulate:
        #    code = int(self._ask("*TST?"))
        #    if code != 0:
        #        message = "Self test failed"
        #return (code, message)
        raise ivi.OperationNotSupportedException()
    
    def _utility_unlock_object(self):
        pass
    
    
    def _init_channels(self):
        try:
            super(agilent436A, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_averaging_count_auto = list()
        self._channel_correction_frequency = list()
        self._channel_offset = list()
        self._channel_range_auto = list()
        self._channel_units = list()
        for i in range(self._channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_averaging_count_auto.append(True)
            self._channel_correction_frequency.append(50e6)
            self._channel_offset.append(0.0)
            self._channel_range_auto.append(True)
            self._channel_units.append('dBm')
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_averaging_count_auto(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_averaging_count_auto[index]
    
    def _set_channel_averaging_count_auto(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        if not value:
            raise ivi.ValueNotSupportedException()
        self._channel_averaging_count_auto[index] = value
    
    def _get_channel_correction_frequency(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_correction_frequency[index]
    
    def _set_channel_correction_frequency(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_correction_frequency[index] = value
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_offset[index] = value
    
    def _get_channel_range_auto(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range_auto[index]
    
    def _set_channel_range_auto(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_range_auto[index] = value
    
    def _get_channel_units(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_units[index]
    
    def _set_channel_units(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        if value not in Units:
            raise ivi.ValueNotSupportedException()
        self._channel_units[index] = value
    
    def _get_measurement_measurement_state(self):
        return self._measurement_measurement_state
    
    def _measurement_abort(self):
        self._clear()
        pass
    
    def _measurement_configure(self, operator, operand1, operand2):
        pass
    
    def _measurement_fetch(self):
        if self._driver_operation_simulate:
            return
        val = self._read()
        if val[0] == 'R':
            return float("inf")
        if val[0] == 'Q' or val[0] == 'S':
            return float("-inf")
        f = float(val[3:12])
        return f
    
    def _measurement_initiate(self):
        if self._driver_operation_simulate:
            return
        cmd = "9+AT"
        self._write(cmd)
    
    def _measurement_read(self, maximum_time):
        self._measurement_initiate()
        return self._measurement_fetch()
    
    def _get_channel_range_lower(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range_lower[index]
    
    def _set_channel_range_lower(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_range_lower[index] = value
    
    def _get_channel_range_upper(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range_upper[index]
    
    def _set_channel_range_upper(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_range_upper[index] = value
    
    def _get_channel_zero_state(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_zero_state[index]
    
    def _channel_zero(self, index):
        index = ivi.get_index(self._channel_name, index)
        if self._driver_operation_simulate:
            return
        
        it = 0
        while True:
            val = self._ask("Z1T")
            if (int(val[4:8]) < 2):
                break
            time.sleep(0.5)
            it += 1
            if it > 20:
                return
        
        it = 0
        while True:
            val = self._ask("9+AI")
            if val[0] < 'T':
                break
            time.sleep(0.5)
            it += 1
            if it > 10:
                return
        
        self._channel_zero_state[index] = 'complete'
    
    
    
    

