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

CurrentLimitBehavior = set([None, 'trip'])
TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'bus': 'bus'}
MeasurementTypeMapping = {
        'voltage': "VOLT",
        'current': "CURR",
        'none': "NONE"}


class agilentN6700(scpi.dcpwr.Base, scpi.dcpwr.Trigger, scpi.dcpwr.SoftwareTrigger,
                scpi.dcpwr.Measurement,
                scpi.common.Memory):
    "Keysight N6700 series IVI modular power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'E3600A')
        
        # don't do standard SCPI init routine
        self._do_scpi_init = False
        
        super(agilentN6700, self).__init__(*args, **kwargs)
        
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
                'current_max': 1.0,
                'ocp_max': 1
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
        self._identity_supported_instrument_models = ['N6700','N6700C']

        self._add_property('outputs[].trace_points',
                        self._get_output_trace_points,
                        self._set_output_trace_points)

        self._add_method('trigger.initiate',
                        self._trigger_initiate)

        self._add_method('trigger.abort',
                        self._trigger_abort)

        self._add_property('outputs[].measurement_type',
                        self._get_output_measurement_type,
                        self._set_output_measurement_type)
        
        self._init_outputs()
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
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

        self._output_trace_points = list()
        self._output_measurement_type = list()
        for i in range(self._output_count):
            self._output_trace_points.append(1024)
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
            self._write("source:current:protection:state %s, (@%s)" % (int(value=='trip'), index+1))
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
            self._output_ocp_limit[index] = float(self._ask("source:current:protection:level? (@%s)" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_ocp_limit[index]

    def _set_output_ocp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['ocp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source:current:protection:level %s, (@%s)" % (value, index+1))
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
            self._output_measurement_range[index] = float(self._ask("sense:%s:range? (@%s)" % (self._output_measurement_type[index], index+1))) #TODO: add auto range
        self._set_cache_valid(index=index)
        return self._output_measurement_range[index]

    def _set_output_measurement_range(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("sense%d:%s:range %s, (@%s)" % (self._output_measurement_type[index], value, index+1))
        self._output_measurement_range[index] = value
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

    def _get_output_measurement_type(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            # Find which measurement types are selected, if any
            types = []
            if self._ask("sense:function:voltage? (@%s)" % (index+1)) == '1':
                types.append('voltage')
            if self._ask("sense:function:current? (@%s)" % (index+1)) == '1':
                types.append('current')
            elif self._ask("sense:function? (@%s)" % (index+1)) == '"NONE"':
                types = None
            self._set_cache_valid(index=index)
        self._output_measurement_type[index] = types
        return self._output_measurement_type[index]

    def _set_output_measurement_type(self, index, types):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            # Reset measurement types
            self._write("sense:function \"NONE\", (@%s)" % (index+1))
            # If we want to set multiple measurement types, i.e. both voltage and current
            if not isinstance(types, str):
                for type in types:
                    if type not in MeasurementTypeMapping:
                        raise ivi.ValueNotSupportedException()
                    self._write("sense:function:%s 1, (@%s)" % (type, index+1))
            # If we want to set only one measurement type, e.g. current
            else:
                if types not in MeasurementTypeMapping:
                    raise ivi.ValueNotSupportedException()
                self._write("sense:function:%s 1, (@%s)" % (types, index+1))

        self._output_measurement_type[index] = types
        self._set_cache_valid(index=index)

    # Trigger functions

    def _trigger_abort(self):
        if not self._driver_operation_simulate:
            self._write("abort")

    def _trigger_initiate(self):
        if not self._driver_operation_simulate:
            self._write("initiate")