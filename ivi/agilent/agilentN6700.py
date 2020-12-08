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
from .. import scpi
from .. import extra

CurrentLimitBehavior = set([None, 'trip'])
TrackingType = set(['floating'])
TriggerSourceMapping = {
        'bus': 'bus',
        'current1': 'curr1',
        'current2': 'curr2',
        'current3': 'curr3',
        'current4': 'curr4',
        'external': 'ext',
        'pin1': 'pin1',
        'pin2': 'pin2',
        'pin3': 'pin3',
        'pin4': 'pin4',
        'pin5': 'pin5',
        'pin6': 'pin6',
        'pin7': 'pin7',
        'transient1': 'tran1',
        'transient2': 'tran2',
        'transient3': 'tran3',
        'transient4': 'tran4',
        'voltage1': 'volt1',
        'voltage2': 'volt2',
        'voltage3': 'volt3',
        'voltage4': 'volt4'}
MeasurementTypeMapping = {
        'voltage': "VOLT",
        'current': "CURR",
        'none': "NONE"}
BufferDataTypeMapping = {
        'current': ['read', float],
        'voltage': ['sour', float],
        'relative_time_seconds': ['rel', float]}
TriggerDirection = {
        'rise': 'POS',
        'fall': 'NEG'}


class agilentN6700(scpi.dcpwr.Base, scpi.dcpwr.Trigger,
                   scpi.dcpwr.SoftwareTrigger,
                   scpi.dcpwr.Measurement,
                   scpi.common.Memory,
                   extra.dcpwr.OCP):
    "Keysight N6700 series IVI modular power supply driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'agilentN6700')

        # don't do standard SCPI init routine
        self._do_scpi_init = False

        try:
            super(agilentN6700, self).__init__(*args, **kwargs)
        except AttributeError:
            pass

        self._output_count = 4

        self._output_spec = [
            {
                'range': {
                    'N6731B': (5, 10.0)
                },
                'voltage_max': 5.0,
                'ovp_max': 5.0,
                'current_max': 10.0,
                'ocp_max': 10
            },
            {
                'range': {
                    'N6732B': (8, 6.25)
                },
                'voltage_max': 8.0,
                'ovp_max': 8.0,
                'current_max': 6.25,
                'ocp_max': 6.25
            },
            {
                'range': {
                    'N6733B': (20, 2.5)
                },
                'voltage_max': 20.0,
                'ovp_max': 20.0,
                'current_max': 2.5,
                'ocp_max': 2.5
            },
            {
                'range': {
                    'N6761A': (50, 1.0)
                },
                'voltage_max': 50.0,
                'ovp_max': 50.0,
                'current_max': 1.5,
                'ocp_max': 1.5
            }
        ]

        self._memory_size = 3
        self._memory_offset = 1
        self._power_modules = []

        self._output_trigger_delay = list()

        self._couple_tracking_enabled = False
        self._couple_tracking_type = 'floating'
        self._couple_trigger = False

        self._identity_description = "Keysight N6700 series IVI modular power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Keysight Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['N6700', 'N6700C']

        self._add_property('outputs[].measurement_type',
                           self._get_output_measurement_type,
                           self._set_output_measurement_type)

        self._add_property('outputs[].measurement_range',
                           self._get_output_measurement_range,
                           self._set_output_measurement_range)

        self._add_property('outputs[].trace_points',
                           self._get_output_trace_points,
                           self._set_output_trace_points)

        self._add_property('outputs[].sweep_interval',
                           self._get_output_sweep_interval,
                           self._set_output_sweep_interval)

        self._add_property('outputs[].sweep_offset_points',
                           self._get_output_sweep_offset_points,
                           self._set_output_sweep_offset_points)

        self._add_property('outputs[].trigger_count',
                           self._get_output_trigger_count,
                           self._set_output_trigger_count)

        self._add_property('outputs[].trigger_current_level',
                           self._get_output_trigger_current_level,
                           self._set_output_trigger_current_level)

        self._add_property('outputs[].trigger_voltage_level',
                           self._get_output_trigger_voltage_level,
                           self._set_output_trigger_voltage_level)

        self._add_property('outputs[].trigger_current_direction',
                           self._get_output_trigger_current_direction,
                           self._set_output_trigger_current_direction)

        self._add_property('outputs[].trigger_voltage_direction',
                           self._get_output_trigger_voltage_direction,
                           self._set_output_trigger_voltage_direction)

        self._add_property('outputs[].trigger_current_state',
                           self._get_output_trigger_current_state,
                           self._set_output_trigger_current_state)

        self._add_property('outputs[].trigger_voltage_state',
                           self._get_output_trigger_voltage_state,
                           self._set_output_trigger_voltage_state)

        self._add_property('outputs[].trigger_sample_count',
                           self._get_output_trigger_sample_count,
                           self._set_output_trigger_sample_count)

        self._add_property('outputs[].trigger_continuous',
                           self._get_output_trigger_continuous,
                           self._set_output_trigger_continuous)

        self._add_property('outputs[].current_compensate',
                           self._get_output_current_compensate,
                           self._set_output_current_compensate)

        self._add_method('outputs[].fetch_measurement',
                         self._output_fetch_measurement,
                         ivi.Doc("""
                         Fetch measurement data from buffer memory. Either fetch all measurement data or
                         a specific interval.
                         """))

        self._add_method('outputs[].trigger_initiate',
                         self._output_trigger_initiate)

        self._add_method('outputs[].trigger_acquire_immediate',
                         self._output_trigger_acquire_immediate)

        self._add_method('outputs[].clear_buffer',
                         self._output_clear_buffer)

        self._add_method('trigger.initiate',
                         self._trigger_initiate)

        self._add_method('trigger.acquire_immediate',
                         self._trigger_acquire_immediate)

        self._add_method('trigger.abort',
                         self._trigger_abort)

        self._init_outputs()

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilentN6700, self)._initialize(resource, id_query, reset, **keywargs)

        # configure interface
        if self._interface is not None:
            if 'dsrdtr' in self._interface.__dict__:
                self._interface.dsrdtr = True
                self._interface.update_settings()

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

        # find initialized power modules
        self._get_number_of_channels()
        self._get_power_modules()

    def _init_outputs(self):
        try:
            super(agilentN6700, self)._init_outputs()
        except AttributeError:
            pass

        self._output_current_compensate = list()
        self._output_sweep_interval = list()
        self._output_trace_points = list()
        self._output_sweep_offset_points = list()
        self._output_trigger_continuous = list()
        self._output_trigger_count = list()
        self._output_trigger_current_level = list()
        self._output_trigger_current_direction = list()
        self._output_trigger_current_state = list()
        self._output_trigger_source = list()
        self._output_trigger_voltage_level = list()
        self._output_trigger_voltage_direction = list()
        self._output_trigger_voltage_state = list()
        self._output_trigger_sample_count = list()
        self._output_measurement_range = list()
        self._output_measurement_type = list()
        for i in range(self._output_count):
            self._output_current_compensate.append(False)
            self._output_sweep_interval.append(0.00002048)
            self._output_trace_points.append(1024)
            self._output_sweep_offset_points.append(0)
            self._output_trigger_continuous.append(True)
            self._output_trigger_count.append(1)
            self._output_trigger_current_level.append(0.0)
            self._output_trigger_current_direction.append('rise')
            self._output_trigger_current_state.append(False)
            self._output_trigger_source.append('bus')
            self._output_trigger_voltage_level.append(0.0)
            self._output_trigger_voltage_direction.append('rise')
            self._output_trigger_voltage_state.append(False)
            self._output_trigger_sample_count.append(1)
            self._output_measurement_range.append(0.01)
            self._output_measurement_type.append('voltage')

    def _get_number_of_channels(self):
        if not self._driver_operation_simulate:
            self._output_count = int(self._ask("system:channel:count?"))
            print("Detected %s power module(s)" % self._output_count)

    def _get_power_modules(self):
        self._power_modules = []
        if not self._driver_operation_simulate:
            for k in range(self._output_count):
                self._power_modules.append(self._ask("system:channel:model? (@%s)" % (k+1)))
                print("Detected channel %s power module: %s" % (k+1, self._power_modules[k]))

    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_current_limit[index] = float(self._ask("source:current:level? (@%s)" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]

    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source:current:level %f, (@%s)" % (value, index+1))
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_output_current_limit_behavior(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            value = self._ask("source:current:protection:state? (@%s)" % (index+1)) == '1'
            if value:
                self._output_current_limit_behavior[index] = 'trip'
            else:
                self._output_current_limit_behavior[index] = None
            self._set_cache_valid(index=index)
        return self._output_current_limit_behavior[index]

    def _set_output_current_limit_behavior(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in dcpwr.CurrentLimitBehavior:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("source:current:protection:state %s, (@%s)" % (int(value == 'trip'), index + 1))
        self._output_current_limit_behavior[index] = value
        self._set_cache_valid(index=index)

    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_enabled[index] = bool(int(self._ask("output? (@%s)" % (index+1))))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]

    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("output %s, (@%s)" % (int(value), index+1))
        self._output_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_output_ovp_enabled(self, index):
        # Output voltage protection is always enabled and at least limited by the maximum output voltage
        return True

    def _set_output_ovp_enabled(self, index, value):
        raise ivi.InvalidOptionValueException("Output voltage protection always enabled, and at least limited by the maximum output voltage")

    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ovp_limit[index] = float(self._ask("source:voltage:protection:level? (@%s)" % (index+1)))
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
            self._write("source:voltage:protection:level %s , (@%s)" % (value, index+1))
        self._output_ovp_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_output_ocp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ocp_limit[index] = float(self._get_output_trigger_current_level(index))
            self._set_cache_valid(index=index)
        return self._output_ocp_limit[index]

    def _set_output_ocp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['ocp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._set_output_trigger_current_level(index, value)
            if value == 0:
                self._write("source:current:protection:state OFF, (@%s)" % (index+1))
            else:
                self._write("source:current:protection:state ON, (@%s)" % (index+1))
        self._output_ocp_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_voltage_level[index] = float(self._ask("source:voltage:level? (@%s)" % (index+1)))
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
            self._write("source:voltage:level %s, (@%s)" % (value, index+1))
        self._output_voltage_level[index] = value
        self._set_cache_valid(index=index)

    # Measurement settings

    def _get_output_measurement_range(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_measurement_range[index] = float(self._ask("sense:%s:range? (@%s)" % (self._output_measurement_type[index], index+1)))
        self._set_cache_valid(index=index)
        return self._output_measurement_range[index]

    def _set_output_measurement_range(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("sense:%s:range %s, (@%s)" % (self._output_measurement_type[index], value, index+1))
        self._output_measurement_range[index] = value
        self._set_cache_valid(index=index)

    def _get_output_measurement_type(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            value = self._ask("sense:function? (@%s)" % (index+1))[1:-1]
            self._output_measurement_type[index] = [k for k, v in MeasurementTypeMapping.items() if v == value][0]
            self._set_cache_valid(index=index)
        return self._output_measurement_type[index]

    def _set_output_measurement_type(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("sense:function \"%s\", (@%s)" % (type, index+1))
        self._output_measurement_type[index] = type
        self._set_cache_valid(index=index)

    def _get_output_trace_points(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trace_points[index] = int(self._ask("sense:sweep:points? (@%s)" % (index+1)))
        self._get_cache_valid(index=index)
        return self._output_trace_points[index]

    def _set_output_trace_points(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            if value > 524288 or value < 0:
                raise ivi.OutOfRangeException()
            self._write("sense:sweep:points %s, (@%s)" % (int(value), index+1))
        self._output_trace_points[index] = int(value)
        self._set_cache_valid(index=index)

    def _get_output_sweep_interval(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_sweep_interval[index] = float(self._ask("sense:sweep:tinterval? (@%s)" % (index+1)))
        self._get_cache_valid(index=index)
        return self._output_sweep_interval[index]

    def _set_output_sweep_interval(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("sense:sweep:tinterval %f, (@%s)" % (float(value), index+1))
        self._output_sweep_interval[index] = float(value)
        self._set_cache_valid(index=index)

    def _get_output_sweep_offset_points(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_sweep_offset_points[index] = int(self._ask("sense:sweep:offset:points? (@%s)" % (index+1)))
        self._get_cache_valid(index=index)
        return self._output_sweep_offset_points[index]

    def _set_output_sweep_offset_points(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            if value > 2e9 or value < -524287:
                raise ivi.OutOfRangeException()
            self._write("sense:sweep:offset:points %s, (@%s)" % (int(value), index+1))
        self._output_sweep_offset_points[index] = int(value)
        self._set_cache_valid(index=index)

    def _get_output_trigger_count(self, index):
        index = ivi.get_index(self._output_name, index)
        # Not supported, do nothing
        self._set_cache_valid()
        return self._output_trigger_count[index]

    def _set_output_trigger_count(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if (value < 0) or (value > 2500):
            raise ivi.OutOfRangeException()
        # Not supported, do nothing
        self._output_trigger_count[index] = value
        self._set_cache_valid(index=index)

    def _get_output_trigger_current_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_current_level[index] = float(self._ask("trigger:acquire:current:level? (@%s)" % (index+1)))
        self._get_cache_valid()
        return self._output_trigger_current_level[index]

    def _set_output_trigger_current_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("trigger:acquire:current:level %f, (@%s)" % (float(value), index+1))
        self._output_trigger_current_level[index] = float(value)
        self._set_cache_valid()

    def _get_output_trigger_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_voltage_level[index] = float(self._ask("trigger:acquire:voltage:level? (@%s)" % (index+1)))
        self._get_cache_valid()
        return self._output_trigger_voltage_level[index]

    def _set_output_trigger_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("trigger:acquire:voltage:level %f, (@%s)" % (float(value), index+1))
        self._output_trigger_voltage_level[index] = float(value)
        self._set_cache_valid()

    def _get_output_trigger_current_direction(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            value = self._ask("trigger:acquire:current:slope? (@%s)" % (index+1))
            self._output_trigger_current_direction[index] = [k for k, v in TriggerDirection.items() if v == value][0]
        self._get_cache_valid()
        return self._output_trigger_current_direction[index]

    def _set_output_trigger_current_direction(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TriggerDirection:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            new_value = [v for k, v in TriggerDirection.items() if k == value][0]
            self._write("trigger:acquire:current:slope %s, (@%s)" % (new_value, index+1))
        self._output_trigger_current_direction[index] = new_value.lower()
        self._set_cache_valid()

    def _get_output_trigger_voltage_direction(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            value = self._ask("trigger:acquire:voltage:slope? (@%s)" % (index+1))
            self._output_trigger_voltage_direction[index] = [k for k, v in TriggerDirection.items() if v == value][0]
        self._get_cache_valid()
        return self._output_trigger_voltage_direction[index]

    def _set_output_trigger_voltage_direction(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TriggerDirection:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            new_value = [v for k, v in TriggerDirection.items() if k == value][0]
            self._write("trigger:acquire:voltage:slope %s, (@%s)" % (new_value, index+1))
        self._output_trigger_voltage_level[index] = new_value.lower()
        self._set_cache_valid()

    def _get_output_trigger_current_state(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_current_state[index] = bool(float(self._ask("trigger:acquire:current:level? (@%s)" % (index+1))))
        self._get_cache_valid()
        return self._output_trigger_current_state[index]

    def _set_output_trigger_current_state(self, index, value):
        index = ivi.get_index(self._output_name, index)
        # Set through current trigger level, do nothing

    def _get_output_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("trigger:acquire:source? (@%s)" % (index+1)).lower()
            self._output_trigger_source[index] = [k for k, v in TriggerSourceMapping.items() if v == value][0]
        return self._output_trigger_source[index]

    def _set_output_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        if value not in TriggerSourceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("trigger:acquire:source %s, (@%s)" % (TriggerSourceMapping[value], index + 1))
        self._output_trigger_source = value
        self._set_cache_valid()

    def _get_output_trigger_voltage_state(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_voltage_state[index] = bool(float(self._ask("trigger:acquire:voltage:level? (@%s)" % (index + 1))))
        self._get_cache_valid()
        return self._output_trigger_voltage_state[index]

    def _set_output_trigger_voltage_state(self, index, value):
        index = ivi.get_index(self._output_name, index)
        # Set through voltage trigger level, do nothing

    def _get_output_trigger_sample_count(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_sample_count[index] = int(self._ask("sense:sweep:points? (@%s)" % (index + 1)))
            self._set_cache_valid(index=index)
        return self._output_trigger_sample_count[index]

    def _set_output_trigger_sample_count(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            if value > 524288 or value < 0:
                raise ivi.OutOfRangeException()
            self._write("sense:sweep:points %s, (@%s)" % (int(value), index + 1))
        self._output_trigger_sample_count[index] = value
        self._set_cache_valid(index=index)

    def _get_output_trigger_continuous(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_continuous[index] = bool(int(self._ask("initiate:continuous:transient? (@%s)" % (index + 1))))
        self._set_cache_valid()
        return self._output_trigger_continuous[index]

    def _set_output_trigger_continuous(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("initiate:continuous:transient %s, (@%s)" % (('OFF', 'ON')[value], index + 1))
        self._output_trigger_continuous[index] = bool(value)
        self._set_cache_valid(index=index)

    def _get_output_current_compensate(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_current_compensate[index] = self._ask("sense:current:ccompensate? (@%s)" % (index + 1)) == '1'
        self._set_cache_valid()
        return self._output_current_compensate[index]

    # Enables/disables the capacitive current compensation. (not on N678xA SMU, N679xA)
    # On Models N676xA this command only applies in the High current range
    def _set_output_current_compensate(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("sense:current:ccompensate %s, (@%s)" % (('OFF', 'ON')[value], index + 1))
        self._output_current_compensate[index] = bool(value)
        self._set_cache_valid(index=index)

    def _output_fetch_measurement(self, index, measurement_type, buffer_range=None):
        index = ivi.get_index(self._output_name, index)
        # type can be multiple elements so need to check that all are valid
        if type(measurement_type) in (tuple, list):
            for t in measurement_type:
                if t not in BufferDataTypeMapping:
                    raise ivi.ValueNotSupportedException()
        elif type(measurement_type) is str:
            if measurement_type not in BufferDataTypeMapping:
                raise ivi.ValueNotSupportedException()
            # make measurement_type a list so that we do not loop through the characters
            measurement_type = [measurement_type]
        else:
            raise ivi.InvalidOptionValueException()

        # Check that buffer_range is a valid tuple or list
        if buffer_range is not None:
            if type(buffer_range) not in (tuple, list):
                raise ivi.ValueNotSupportedException("buffer_range must be tuple or list of length 2")
            if buffer_range[1] > self._memory_size:
                raise ivi.ValueNotSupportedException("buffer_range buffer size is %d" % self._memory_size)

        for m in measurement_type:
            if m == 'current':
                buffer_raw_data = self._ask("fetch:array:current? (@%s)" % (index + 1)).split(',')
            if m == 'voltage':
                buffer_raw_data = self._ask("fetch:array:voltage? (@%s)" % (index + 1)).split(',')

        buffer_data = []

        # Fetch data
        for m in measurement_type:
            if m == 'current' or m == 'voltage':
                buffer_data_i = [float(k) for k in buffer_raw_data]
            else:
                buffer_data_i = [0 + x * len(buffer_raw_data)*self._output_sweep_interval[index]/len(buffer_raw_data) for x in range(len(buffer_raw_data))]
            # If multiple data types where requested, return a list of measurement sequences
            if len(measurement_type) > 1:
                buffer_data.append(buffer_data_i)
            else:
                return buffer_data_i

        return buffer_data

    def _output_clear_buffer(self, index):
        index = ivi.get_index(self._output_name, index)
        # Not supported, do nothing

    # Trigger functions
    def _output_trigger_initiate(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("initiate:acquire (@%s)" % (index + 1))

    def _output_trigger_acquire_immediate(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("initiate:immediate:acquire (@%s)" % (index + 1))
            # Wait until WTG_meas (bit 3) bit is set to know when the instrument is
            # ready to receive a trigger after initiating, or maximum 10 times
            # to not block indefinitely
            wtg_meas_set = False
            for loop_count in range(20):
                operation = int(self._ask("stat:oper? (@%s)" % (index+1)))
                if (operation & 8) == 8:
                    wtg_meas_set = True
                    break;

            if not wtg_meas_set:
                print("WTG_meas bit not set in status register")

            self._write("trigger:acquire:immediate (@%s)" % (index + 1))

    def _trigger_abort(self):
        if not self._driver_operation_simulate:
            self._write("abort")

    def _trigger_initiate(self):
        if not self._driver_operation_simulate:
            self._write("initiate:acquire (@1:%s)" % (self._output_count))

    def _trigger_acquire_immediate(self):
        if not self._driver_operation_simulate:
            self._write("initiate:immediate:acquire (@1:%s)" % (self._output_count))
            self._write("trigger:acquire:immediate (@1:%s)" % (self._output_count))
