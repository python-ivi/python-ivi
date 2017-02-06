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

import math

from .. import ivi
from .. import dmm
from . import common

MeasurementFunctionMapping = {
        'dc_volts': 'volt',
        'ac_volts': 'volt:ac',
        'dc_current': 'curr',
        'ac_current': 'curr:ac',
        'two_wire_resistance': 'res',
        'four_wire_resistance': 'fres',
        'frequency': 'freq',
        'period': 'per',
        'temperature': 'temp',
        'capacitance': 'cap',
        'continuity': 'cont',
        'diode': 'diod'}

MeasurementRangeMapping = {
        'dc_volts': 'volt:dc:range',
        'ac_volts': 'volt:ac:range',
        'dc_current': 'curr:dc:range',
        'ac_current': 'curr:ac:range',
        'two_wire_resistance': 'res:range',
        'four_wire_resistance': 'fres:range',
        'frequency': 'freq:range:lower',
        'period': 'per:range:lower',
        'capacitance': 'cap:range'}

MeasurementAutoRangeMapping = {
        'dc_volts': 'volt:dc:range:auto',
        'ac_volts': 'volt:ac:range:auto',
        'dc_current': 'curr:dc:range:auto',
        'ac_current': 'curr:ac:range:auto',
        'two_wire_resistance': 'res:range:auto',
        'four_wire_resistance': 'fres:range:auto',
        'capacitance': 'cap:range:auto'}

MeasurementResolutionMapping = {
        'dc_volts': 'volt:dc:resolution',
        'ac_volts': 'volt:ac:resolution',
        'dc_current': 'curr:dc:resolution',
        'ac_current': 'curr:ac:resolution',
        'two_wire_resistance': 'res:resolution',
        'four_wire_resistance': 'fres:resolution'}

TriggerSourceMapping = {
        'bus': 'bus',
        'external': 'ext',
        'immediate': 'imm'}

class Base(common.IdnCommand, common.ErrorQuery, common.Reset, common.SelfTest,
           ivi.Driver,
           dmm.Base):
    "Generic SCPI IVI DMM driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        # early define of _do_scpi_init
        self.__dict__.setdefault('_do_scpi_init', True)
        
        super(Base, self).__init__(*args, **kwargs)

        self._self_test_delay = 40
        
        self._identity_description = "Generic SCPI IVI DMM driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = ""
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['DMM']
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(Base, self)._initialize(resource, id_query, reset, **keywargs)
        
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
        
    
    def _utility_disable(self):
        pass
    
    def _utility_lock_object(self):
        pass
    
    def _utility_unlock_object(self):
        pass
    
    def _get_measurement_function(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":sense:function?").lower().strip('"')
            value = [k for k,v in MeasurementFunctionMapping.items() if v==value][0]
            self._measurement_function = value
            self._set_cache_valid()
        return self._measurement_function
    
    def _set_measurement_function(self, value):
        if value not in MeasurementFunctionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":sense:function '%s'" % MeasurementFunctionMapping[value])
        self._measurement_function = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'range')
        self._set_cache_valid(False, 'auto_range')
        self._set_cache_valid(False, 'resolution')
    
    def _get_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            func = self._get_measurement_function()
            if func in MeasurementRangeMapping:
                cmd = MeasurementRangeMapping[func]
                value = float(self._ask("%s?" % (cmd)))
                self._range = value
                self._set_cache_valid()
        return self._range
    
    def _set_range(self, value):
        value = float(value)
        # round up to even power of 10
        value = math.pow(10, math.ceil(math.log10(value)))
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementRangeMapping:
                cmd = MeasurementRangeMapping[func]
                self._write("%s %g" % (cmd, value))
        self._range = value
        self._set_cache_valid()
    
    def _get_auto_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            func = self._get_measurement_function()
            if func in MeasurementAutoRangeMapping:
                cmd = MeasurementAutoRangeMapping[func]
                value = int(self._ask("%s?" % (cmd)))
                if value == 0:
                    value = 'off'
                elif value == 1:
                    value = 'on'
                self._auto_range = value
                self._set_cache_valid()
        return self._auto_range
    
    def _set_auto_range(self, value):
        if value not in dmm.Auto2:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementAutoRangeMapping:
                cmd = MeasurementAutoRangeMapping[func]
                self._write("%s %d" % (cmd, int(value == 'on')))
        self._auto_range = value
        self._set_cache_valid()
    
    def _get_resolution(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            func = self._get_measurement_function()
            if func in MeasurementResolutionMapping:
                cmd = MeasurementResolutionMapping[func]
                value = float(self._ask("%s?" % (cmd)))
                self._resolution = value
                self._set_cache_valid()
        return self._resolution
    
    def _set_resolution(self, value):
        value = float(value)
        # round up to even power of 10
        value = math.pow(10, math.ceil(math.log10(value)))
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementResolutionMapping:
                cmd = MeasurementResolutionMapping[func]
                self._write("%s %g" % (cmd, value))
        self._resolution = value
        self._set_cache_valid()
    
    def _get_trigger_delay(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = float(self._ask("trigger:delay?"))
            self._trigger_delay = value
            self._set_cache_valid()
        return self._trigger_delay
    
    def _set_trigger_delay(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write('trigger:delay %g' % value)
        self._trigger_delay = value
        self._set_cache_valid()
    
    def _get_trigger_delay_auto(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = bool(int(self._ask("trigger:delay:auto?")))
            self._trigger_delay_auto = value
            self._set_cache_valid()
        return self._trigger_delay_auto
    
    def _set_trigger_delay_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write('trigger:delay:auto %d' % int(value))
        self._trigger_delay_auto = value
        self._set_cache_valid()
    
    def _get_trigger_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("trigger:source?").lower()
            value = [k for k,v in TriggerSourceMapping.items() if v==value][0]
            self._trigger_source = value
            self._set_cache_valid()
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        if value not in TriggerSourceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:source %s" % TriggerSourceMapping[value])
        self._trigger_source = value
    
    def _measurement_abort(self):
        if not self._driver_operation_simulate:
            self._write(":abort")
    
    def _measurement_fetch(self, max_time):
        if not self._driver_operation_simulate:
            return float(self._ask(":fetch?"))
        return 0.0
    
    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(":initiate")
    
    def _measurement_is_out_of_range(self, value):
        return self._measurement_is_over_range(value) or self._measurement_is_under_range(value)
    
    def _measurement_is_over_range(self, value):
        return value == 9.9e+37
    
    def _measurement_is_under_range(self, value):
        return value == -9.9e+37
    
    def _measurement_read(self, max_time):
        if not self._driver_operation_simulate:
            return float(self._ask(":read?"))
        return 0.0
    
    
class MultiPoint(dmm.MultiPoint):
    "Extension IVI methods for DMMs capable of acquiring measurements based on multiple triggers"
    
    def _get_trigger_measurement_complete_destination(self):
        return self._trigger_measurement_complete_destination
    
    def _set_trigger_measurement_complete_destination(self, value):
        value = str(value)
        self._trigger_measurement_complete_destination = value
    
    def _get_trigger_multi_point_sample_count(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = int(self._ask("sample:count?"))
            self._trigger_multi_point_sample_count = value
            self._set_cache_valid()
        return self._trigger_multi_point_sample_count
    
    def _set_trigger_multi_point_sample_count(self, value):
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("sample:count %d" % value)
        self._trigger_multi_point_sample_count = value
        self._set_cache_valid()
    
    def _get_trigger_multi_point_sample_interval(self):
        return self._trigger_multi_point_sample_interval
    
    def _set_trigger_multi_point_sample_interval(self, value):
        value = int(value)
        self._trigger_multi_point_sample_interval = value
    
    def _get_trigger_multi_point_sample_trigger(self):
        return self._trigger_multi_point_sample_trigger
    
    def _set_trigger_multi_point_sample_trigger(self, value):
        value = str(value)
        self._trigger_multi_point_sample_trigger = value
    
    def _get_trigger_multi_point_count(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("trigger:count?")
            if float(value) >= 9.9e37:
                value = float('inf')
            else:
                value = int(float(value))
            self._trigger_multi_point_count = value
            self._set_cache_valid()
        return self._trigger_multi_point_count
    
    def _set_trigger_multi_point_count(self, value):
        if float(value) >= 9.9e37 or float(value) == float('inf'):
            value = float('inf')
        else:
            value = int(value)
        if not self._driver_operation_simulate:
            if value == float('inf'):
                self._write("trigger:count inf")
            else:
                self._write("trigger:count %d" % value)
        self._trigger_multi_point_count = value
        self._set_cache_valid()
    
    def _measurement_fetch_multi_point(self, max_time, num_of_measurements = 0):
        if not self._driver_operation_simulate:
            return self._ask_for_values(":fetch?", array=False)
        return [0.0 for i in range(self._trigger_multi_point_count*self._trigger_multi_point_sample_count)]
    
    def _measurement_read_multi_point(self, max_time, num_of_measurements = 0):
        if not self._driver_operation_simulate:
            return self._ask_for_values(":read?", array=False)
        return [0.0 for i in range(self._trigger_multi_point_count*self._trigger_multi_point_sample_count)]
    
    
class SoftwareTrigger(dmm.SoftwareTrigger):
    "Extension IVI methods for DMMs that can initiate a measurement based on a software trigger signal"
    
    def _send_software_trigger(self):
        if not self._driver_operation_simulate:
            self._write("*trg")

