"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2017 Alex Forencich

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
from .. import scpi

CurrentLimitBehavior = set(['regulate'])
TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'bus': 'bus'}

class agilentU2722A(scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset,
                scpi.common.SelfTest,
                dcpwr.Base, dcpwr.Measurement,
                extra.dcpwr.OCP,
                ivi.Driver):
    "Agilent U2722A IVI modular source measure unit driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'U2722A')

        super(agilentU2722A, self).__init__(*args, **kwargs)

        self._self_test_delay = 10

        self._output_count = 3

        self._output_spec = [
            {
                'current_range': {
                    'R1uA': 1e-6,
                    'R10uA': 10e-6,
                    'R100uA': 100e-6,
                    'R1mA': 1e-3,
                    'R10mA': 10e-3,
                    'R120mA': 120e-3,
                },
                'voltage_range': {
                    'R2V': 2.0,
                    'R20V': 20.0,
                },
                'ocp_max': 120e-3,
                'ovp_max': 20.0,
                'voltage_max': 20.0,
                'current_max': 120e-3
            }
        ]*3

        self._output_trigger_delay = list()

        self._identity_description = "Agilent U2722A modular source measure unit driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['U2722A', 'U2723A']

        self._init_outputs()

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilentU2722A, self)._initialize(resource, id_query, reset, **keywargs)

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

    def _init_outputs(self):
        try:
            super(agilentU2722A, self)._init_outputs()
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
            self._output_current_limit_behavior.append('regulate')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(0)
            self._output_voltage_level.append(0)
            self._output_trigger_source.append('bus')
            self._output_trigger_delay.append(0)

    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_current_limit[index] = float(self._ask("source:current:level? (@%d)" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]

    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source:current:level %.6g, (@%d)" % (value, index+1))
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_output_current_limit_behavior(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_current_limit_behavior[index] = 'regulate'
            self._set_cache_valid(index=index)
        return self._output_current_limit_behavior[index]

    def _set_output_current_limit_behavior(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in CurrentLimitBehavior:
            raise ivi.ValueNotSupportedException()
        self._set_cache_valid(index=index)

    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_enabled[index] = bool(int(self._ask("output? (@%d)" % (index+1))))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]

    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("output %d, (@%d)" % (int(value), index+1))
        self._output_enabled[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)

    def _get_output_ovp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ovp_enabled[index] = True
            self._set_cache_valid(index=index)
        return self._output_ovp_enabled[index]

    def _set_output_ovp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not value:
            raise ivi.ValueNotSupportedException()
        self._output_ovp_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ovp_limit[index] = float(self._ask("source:voltage:limit? (@%d)" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_ovp_limit[index]

    def _set_output_ovp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['ovp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source:voltage:limit %.6g, (@%d)" % (value, index+1))
        self._output_ovp_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_output_ocp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ocp_enabled[index] = True
            self._set_cache_valid(index=index)
        return self._output_ocp_enabled[index]

    def _set_output_ocp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not value:
            raise ivi.ValueNotSupportedException()
        self._output_ocp_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_output_ocp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ocp_limit[index] = float(self._ask("source:current:limit? (@%d)" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_ocp_limit[index]

    def _set_output_ocp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['ocp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source:current:limit %.6g, (@%d)" % (value, index+1))
        self._output_ocp_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_voltage_level[index] = float(self._ask("source:voltage:level? (@%d)" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_voltage_level[index]

    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['voltage_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source:voltage:level %.6g,  (@%d)" % (value, index+1))
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
        range_val = abs(range_val)
        if len(self._output_spec[index][range_type+'_range']) < 2:
            # do not set range if there is only one range
            return
        k = dcpwr.get_range(self._output_spec[index][range_type+'_range'], None, range_val)
        if k is None:
            raise ivi.OutOfRangeException()
        if range_type == 'voltage':
            self._output_spec[index]['voltage_max'] = self._output_spec[index]['voltage_range'][k]
        elif range_type == 'current':
            self._output_spec[index]['current_max'] = self._output_spec[index]['current_range'][k]
        if not self._driver_operation_simulate:
            if range_type == 'voltage':
                self._write("source:voltage:range %s, (@%d)" % (k, index+1))
            elif range_type == 'current':
                self._write("source:current:range %s, (@%d)" % (k, index+1))

    def _output_query_current_limit_max(self, index, voltage_level):
        index = ivi.get_index(self._output_name, index)
        if abs(voltage_level) > self._output_spec[index]['voltage_max']:
            raise ivi.OutOfRangeException()
        return self._output_spec[index]['current_max']

    def _output_query_voltage_level_max(self, index, current_limit):
        index = ivi.get_index(self._output_name, index)
        if abs(current_limit) > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        return self._output_spec[index]['voltage_max']

    def _output_query_output_state(self, index, state):
        index = ivi.get_index(self._output_name, index)
        raise ivi.ValueNotSupportedException()
        return False

    def _output_reset_output_protection(self, index):
        pass

    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in dcpwr.MeasurementType:
            raise ivi.ValueNotSupportedException()
        if type == 'voltage':
            if not self._driver_operation_simulate:
                return float(self._ask("measure:voltage? (@%d)" % (index+1)))
        elif type == 'current':
            if not self._driver_operation_simulate:
                return float(self._ask("measure:current? (@%d)" % (index+1)))
        return 0
