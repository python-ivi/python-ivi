"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2015-2017 Alex Forencich

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
from .. import scpi

import time

Units = set(['dBm', 'Watts'])

class agilentU2000(scpi.common.IdnCommand, scpi.common.ErrorQuery,
                scpi.common.Reset, scpi.common.SelfTest,
                pwrmeter.Base, pwrmeter.ManualRange,
                pwrmeter.DutyCycleCorrection, pwrmeter.AveragingCount,
                pwrmeter.ZeroCorrection,
                ivi.Driver):
    "Agilent U2000 series RF power sensor"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'U200')
        
        super(agilentU2000, self).__init__(*args, **kwargs)

        self._channel_count = 1
        
        self._identity_description = "Agilent U2000 series RF power meter driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['U2000A', 'U2000B', 'U2000H',
                        'U2001A', 'U2001B', 'U2001H', 'U2002A', 'U2002H', 'U2004A']

        self._channel_count = 1
        self._frequency_low = 10e6
        self._frequency_high = 6e9
        self._power_low = -60
        self._power_high = 20
        
        self._init_channels()
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilentU2000, self)._initialize(resource, id_query, reset, **keywargs)
        
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
        
    
    def _utility_disable(self):
        pass
    
    def _utility_lock_object(self):
        pass
    
    def _utility_unlock_object(self):
        pass
    
    
    def _init_channels(self):
        try:
            super(agilentU2000, self)._init_channels()
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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_averaging_count_auto[index] = bool(int(self._ask("sense:average:count:auto?")))
            self._set_cache_valid()
        return self._channel_averaging_count_auto[index]
    
    def _set_channel_averaging_count_auto(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("sense:average:count:auto %i" % int(value))
        self._channel_averaging_count_auto[index] = value
    
    def _get_channel_correction_frequency(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_correction_frequency[index] = float(self._ask("sense:frequency?"))
            self._set_cache_valid()
        return self._channel_correction_frequency[index]
    
    def _set_channel_correction_frequency(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("sense:frequency %g" % (value))
        self._channel_correction_frequency[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_offset[index] = float(self._ask("sense:correction:gain2?"))
            self._set_cache_valid()
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("sense:correction:gain2 %f" % (value))
            self._write("sense:correction:gain2:state 1")
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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_units[index] = 'dBm' if 'DBM' in self._ask("unit:power?") else 'Watts'
            self._set_cache_valid()
        return self._channel_units[index]
    
    def _set_channel_units(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        if value not in Units:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("unit:power %s" % value)
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
        self._write("format ascii")
        val = self._ask("fetch?")
        return float(val)
    
    def _measurement_initiate(self):
        if self._driver_operation_simulate:
            return
        self._write("initiate:immediate")
    
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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_duty_cycle_enabled[index] = bool(int(self._ask("sense:correction:dcyc:state?")))
            self._set_cache_valid()
        return self._channel_duty_cycle_enabled[index]
    
    def _set_channel_duty_cycle_enabled(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("sense:correction:dcyc:state %i" % int(value))
        self._channel_duty_cycle_enabled[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_duty_cycle_value(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_duty_cycle_value[index] = float(self._ask("sense:correction:dcyc?"))
            self._set_cache_valid()
        return self._channel_duty_cycle_value[index]
    
    def _set_channel_duty_cycle_value(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("sense:correction:dcyc %f" % (value))
        self._channel_duty_cycle_value[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_averaging_count(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_averaging_count[index] = int(self._ask("sense:average:count?"))
            self._set_cache_valid()
        return self._channel_averaging_count[index]
    
    def _set_channel_averaging_count(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("sense:average:count %i" % (value))
        self._channel_averaging_count[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_zero_state(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._channel_zero_state[index] = "in_progress" if int(self._ask("status:operation:calibrating:condition?")) else "complete"
        return self._channel_zero_state[index]
    
    def _channel_zero(self, index):
        index = ivi.get_index(self._channel_name, index)
        if self._driver_operation_simulate:
            return

        self._write("calibration:all")
    
    

