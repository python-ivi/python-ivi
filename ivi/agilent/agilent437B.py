"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014 Alex Forencich

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

Units = set(['dBm', 'Watts'])

class agilent437B(ivi.Driver, pwrmeter.Base, pwrmeter.ManualRange,
                pwrmeter.DutyCycleCorrection, pwrmeter.AveragingCount,
                pwrmeter.ZeroCorrection, pwrmeter.Calibration,
                pwrmeter.ReferenceOscillator):
    "Agilent 437B RF power meter"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '437B')
        
        super(agilent437B, self).__init__(*args, **kwargs)

        self._channel_count = 1
        
        self._identity_description = "Agilent 437B RF power meter driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['437B']
        
        self._init_channels()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilent437B, self).initialize(resource, id_query, reset, **keywargs)
        
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
            lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = lst[0]
            self._identity_instrument_model = lst[1]
            self._identity_instrument_firmware_revision = lst[3]
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
            self._write("*RST")
            self._clear()
            self.driver_operation.invalidate_all_attributes()
    
    def _utility_reset_with_defaults(self):
        self._utility_reset()
    
    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            code = int(self._ask("*TST?"))
            if code != 0:
                message = "Self test failed"
        return (code, message)
        raise ivi.OperationNotSupportedException()
    
    def _utility_unlock_object(self):
        pass
    
    
    def _init_channels(self):
        try:
            super(agilent437B, self)._init_channels()
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
        if not self._driver_operation_simulate:
            self._write("FR%eEN" % (value))
        self._channel_correction_frequency[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("OS%eEN" % (value))
        self._channel_offset[index] = value
        self._set_cache_valid(index=index)
    
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
        if not self._driver_operation_simulate:
            if value == 'dBm':
                self._write("LG")
            elif value == 'Watts':
                self._write("LN")
        self._channel_units[index] = value
        self._set_cache_valid(index=index)
    
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
        return float(val)
    
    def _measurement_initiate(self):
        if self._driver_operation_simulate:
            return
        self._write("TR1")
    
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

    def _get_channel_duty_cycle_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_duty_cycle_enabled[index]
    
    def _set_channel_duty_cycle_enabled(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("DC%d" % int(value))
        self._channel_duty_cycle_enabled[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_duty_cycle_value(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_duty_cycle_value[index]
    
    def _set_channel_duty_cycle_value(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("DY%eEN" % (value))
        self._channel_duty_cycle_value[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_averaging_count(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_averaging_count[index]
    
    def _set_channel_averaging_count(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("FM%eEN" % (value))
        self._channel_averaging_count[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_zero_state(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_zero_state[index]
    
    def _channel_zero(self, index):
        index = ivi.get_index(self._channel_name, index)
        if self._driver_operation_simulate:
            return

        self._write("CS")
        self._write("ZE")
        it = 0
        while True:
            val = self._read_stb()
            if val & 2:
                break
            if val & 8 or it > 20:
                return
            time.sleep(0.5)
        
        self._channel_zero_state[index] = 'complete'
    
    def _get_channel_calibration_state(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_calibration_state[index]
    
    def _channel_calibrate(self, index):
        index = ivi.get_index(self._channel_name, index)
        if self._driver_operation_simulate:
            return

        self._write("CS")
        self._write("CLEN")
        it = 0
        while True:
            val = self._read_stb()
            if val & 2:
                break
            if val & 8 or it > 20:
                return
            time.sleep(0.5)

        self._channel_calibration_state[index] = 'complete'

    def _get_reference_oscillator_enabled(self):
        return self._reference_oscillator_enabled
    
    def _set_reference_oscillator_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("OC%d" % int(value))
        self._reference_oscillator_enabled = value
        self._set_cache_valid()
    
    def _get_reference_oscillator_frequency(self):
        return self._reference_oscillator_frequency
    
    def _set_reference_oscillator_frequency(self, value):
        value = float(value)
        value = 50e6 # fixed at 50 MHz
        self._reference_oscillator_frequency = value
    
    def _get_reference_oscillator_level(self):
        return self._reference_oscillator_level
    
    def _set_reference_oscillator_level(self, value):
        value = float(value)
        value = 0.0 # fixed at 1.00 mW (0 dBm)
        self._reference_oscillator_level = value
    
    

