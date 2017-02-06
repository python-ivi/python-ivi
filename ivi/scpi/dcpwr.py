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

from .. import ivi
from .. import dcpwr
from .. import extra
from . import common

TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'bus': 'bus'}

class Base(common.IdnCommand, common.ErrorQuery, common.Reset, common.SelfTest,
           dcpwr.Base,
           ivi.Driver):
    "Generic SCPI IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        # early define of _do_scpi_init
        self.__dict__.setdefault('_do_scpi_init', True)

        super(Base, self).__init__(*args, **kwargs)

        self._self_test_delay = 5

        self._output_count = 1

        self._output_spec = [
            {
                'range': {
                    'P8V': (9.0, 20.0),
                    'P20V': (21.0, 10.0)
                },
                'ovp_max': 22.0,
                'voltage_max': 9.0,
                'current_max': 20.0
            }
        ]

        self._identity_description = "Generic SCPI DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = ""
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PSU']

        self._init_outputs()

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(Base, self)._initialize(resource, id_query, reset, **keywargs)

        if not self._do_scpi_init:
            return

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

    def _get_bool_str(self, value):
        """
        Provides string to use in reading and writing boolean values.
        """
        # TODO - Move to location where it isn't defined in multiple places.
        if bool(value):
            return '1'
        return '0'

    def _utility_disable(self):
        pass

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass

    def _init_outputs(self):
        try:
            super(Base, self)._init_outputs()
        except AttributeError:
            pass
        
        self._output_current_limit = list()
        self._output_current_limit_behavior = list()
        self._output_enabled = list()
        self._output_ovp_enabled = list()
        self._output_ovp_limit = list()
        self._output_voltage_level = list()
        self._output_trigger_source = list()
        self._output_trigger_delay = list()
        for i in range(self._output_count):
            self._output_current_limit.append(0)
            self._output_current_limit_behavior.append('trip')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(0)
            self._output_voltage_level.append(0)
            self._output_trigger_source.append('bus')
            self._output_trigger_delay.append(0)
    
    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_current_limit[index] = float(self._ask("source:current:level?"))
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]
    
    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:current:level %.6f" % value)
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_current_limit_behavior(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            value = self._ask("source:current:protection:state?") == self._get_bool_str(True)
            if value:
                self._output_current_limit_behavior[index] = 'trip'
            else:
                self._output_current_limit_behavior[index] = 'regulate'
            self._set_cache_valid(index=index)
        return self._output_current_limit_behavior[index]
    
    def _set_output_current_limit_behavior(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in dcpwr.CurrentLimitBehavior:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:current:protection:state %s" % self._get_bool_str(value == 'trip'))
        self._output_current_limit_behavior[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
    
    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_enabled[index] = self._ask("output?") == self._get_bool_str(True)
            self._set_cache_valid(index=index)
        return self._output_enabled[index]
    
    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("output %s" % self._get_bool_str(value))
        self._output_enabled[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
    
    def _get_output_ovp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_ovp_enabled[index] = self._ask("source:voltage:protection:state?") == self._get_bool_str(True)
            self._set_cache_valid(index=index)
        return self._output_ovp_enabled[index]
    
    def _set_output_ovp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:voltage:protection:state %s" % self._get_bool_str(value))
        self._output_ovp_enabled[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_ovp_limit[index] = float(self._ask("source:voltage:protection:level?"))
            self._set_cache_valid(index=index)
        return self._output_ovp_limit[index]
    
    def _set_output_ovp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if self._output_spec[index]['ovp_max'] >= 0:
            if value < 0 or value > self._output_spec[index]['ovp_max']:
                raise ivi.OutOfRangeException()
        else:
            if value > 0 or value < self._output_spec[index]['ovp_max']:
                raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:voltage:protection:level %.6f" % value)
        self._output_ovp_limit[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_voltage_level[index] = float(self._ask("source:voltage:level?"))
            self._set_cache_valid(index=index)
        return self._output_voltage_level[index]
    
    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if self._output_spec[index]['voltage_max'] >= 0:
            if value < 0 or value > self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        else:
            if value > 0 or value < self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:voltage:level %.6f" % value)
        self._output_voltage_level[index] = value
        self._set_cache_valid(index=index)
    
    def _output_configure_range(self, index, range_type, range_val):
        index = ivi.get_index(self._output_name, index)
        if range_type not in dcpwr.RangeType:
            raise ivi.ValueNotSupportedException()
        if range_type == 'voltage':
            t = 0
        elif range_type == 'current':
            t = 1
        if len(self._output_spec[index]['range']) < 2:
            # do not set range if there is only one range
            return
        k = dcpwr.get_range(self._output_spec[index]['range'], t, range_val)
        if k is None:
            raise ivi.OutOfRangeException()
        self._output_spec[index]['voltage_max'] = self._output_spec[index]['range'][k][0]
        self._output_spec[index]['current_max'] = self._output_spec[index]['range'][k][1]
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:voltage:range %s" % k)
    
    def _output_query_current_limit_max(self, index, voltage_level):
        index = ivi.get_index(self._output_name, index)
        if self._output_spec[index]['voltage_max'] >= 0:
            if voltage_level < 0 or voltage_level > self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        else:
            if voltage_level > 0 or voltage_level < self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        return self._output_spec[index]['current_max']
    
    def _output_query_voltage_level_max(self, index, current_limit):
        index = ivi.get_index(self._output_name, index)
        if current_limit < 0 or current_limit > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        return self._output_spec[index]['voltage_max']
    
    def _output_query_output_state(self, index, state):
        index = ivi.get_index(self._output_name, index)
        if state not in dcpwr.OutputState:
            raise ivi.ValueNotSupportedException()
        status = 0
        if not self._driver_operation_simulate:
            status = int(self._ask("stat:ques:inst:isum%d:cond?" % (index+1)))
        if state == 'constant_voltage':
            return status & (1 << 1) != 0
        elif state == 'constant_current':
            return status & (1 << 0) != 0
        elif state == 'over_voltage':
            return status & (1 << 9) != 0
        elif state == 'over_current':
            return status & (1 << 10) != 0
        elif state == 'unregulated':
            return status & (3 << 0) != 0
        return False
    
    def _output_reset_output_protection(self, index):
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:voltage:protection:clear")

class OCP(extra.dcpwr.OCP):

    def _get_bool_str(self, value):
        """
        return string based bool for write and read operations
        """
        # TODO - Move to location where it isn't defined in multiple places.
        if bool(value):
            return '1'
        return '0'

    def _get_output_ocp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_ocp_enabled[index] = self._ask("source:current:protection:state?") == self._get_bool_str(True)
            self._set_cache_valid(index=index)
        return self._output_ocp_enabled[index]
    
    def _set_output_ocp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:current:protection:state %s" % self._get_bool_str(value))
        self._output_ocp_enabled[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_ocp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_ocp_limit[index] = float(self._ask("source:current:protection:level?"))
            self._set_cache_valid(index=index)
        return self._output_ocp_limit[index]
    
    def _set_output_ocp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['ocp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:current:protection:level %.6f" % value)
        self._output_ocp_limit[index] = value
        self._set_cache_valid(index=index)
    
    def _output_reset_output_protection(self, index):
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:voltage:protection:clear")
            self._write("source:current:protection:clear")

class Trigger(dcpwr.Trigger):
    def _get_output_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid():
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            value = self._ask("trigger:source?").lower()
            self._output_trigger_source[index] = [k for k,v in TriggerSourceMapping.items() if v==value][0]
        return self._output_trigger_source[index]
    
    def _set_output_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        if value not in TriggerSourceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("trigger:source %s" % TriggerSourceMapping[value])
        self._output_trigger_source[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_triggered_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_triggered_current_limit[index] = float(self._ask("source:current:level:triggered?"))
            self._set_cache_valid(index=index)
        return self._output_triggered_current_limit[index]
    
    def _set_output_triggered_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:current:level:triggered %.6f" % value)
        self._output_triggered_current_limit[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_triggered_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_triggered_voltage_level[index] = float(self._ask("source:voltage:level:triggered?"))
            self._set_cache_valid(index=index)
        return self._output_triggered_voltage_level[index]
    
    def _set_output_triggered_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if self._output_spec[index]['voltage_max'] >= 0:
            if value < 0 or value > self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        else:
            if value > 0 or value < self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("source:voltage:level:triggered %.6f" % value)
        self._output_triggered_voltage_level[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_trigger_delay(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_trigger_delay[index] = float(self._ask("trigger:delay?"))
            self._set_cache_valid(index=index)
        return self._output_trigger_delay[index]
    
    def _set_output_trigger_delay(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("trigger:delay %.6f" % value)
        self._output_trigger_delay[index] = value
        self._set_cache_valid(index=index)
    
    def _trigger_abort(self):
        pass
    
    def _trigger_initiate(self):
        if not self._driver_operation_simulate:
            self._write("initiate")
    
class SoftwareTrigger(dcpwr.SoftwareTrigger):
    def _send_software_trigger(self):
        if not self._driver_operation_simulate:
            self._write("*trg")

class Measurement(dcpwr.Measurement):
    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in dcpwr.MeasurementType:
            raise ivi.ValueNotSupportedException()
        if type == 'voltage':
            if not self._driver_operation_simulate:
                if self._output_count > 1:
                    self._write("instrument:nselect %d" % (index+1))
                return float(self._ask("measure:voltage?"))
        elif type == 'current':
            if not self._driver_operation_simulate:
                if self._output_count > 1:
                    self._write("instrument:nselect %d" % (index+1))
                return float(self._ask("measure:current?"))
        return 0
