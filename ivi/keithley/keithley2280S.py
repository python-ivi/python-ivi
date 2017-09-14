"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2017 Acconeer Ab

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
from .. import scpi
from .. import dcpwr
from .. import extra

TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'external': 'ext',
        'manual': 'man'}
RangeType = set(['voltage','current'])
MeasurementType = set(['voltage', 'current', 'concurrent'])
MeasurementTypeMapping = {
        'voltage': "volt:dc",
        'current': "curr:dc",
        'concurrent': "conc:dc"}
#MeasurementFunctionMapping = {
#        'minimum': 'min',
#        'maximum': 'max',
#        'average': 'mean',
#        'peak_to_peak': 'pkpk',
#        'standard_deviation': 'sdev'}

class keithley2280S(scpi.dcpwr.Base, scpi.dcpwr.SoftwareTrigger,
                    dcpwr.Measurement,
                    extra.dcpwr.OCP):
    "Keithley (Tektronix) 2280S series precision measurement DC supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'keithley2280S')

        super(keithley2280S, self).__init__(*args, **kwargs)

        self._output_count = 1
        
        self._output_spec = [
            {
                'range': {
                    'P32V': (32.0, 6.0)
                },
                'ovp_max': 33.0,
                'ocp_max': 6.1,
                'voltage_max': 32.0,
                'current_max': 6.0
            }
        ]

        
        self._memory_size = 2500
        self._memory_offset = 0


        self._output_trigger_delay = list()

        self._identity_description = "Keithley (Tektronix) 2280S series precision measurement DC supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Keithley (Tektronix)"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['2280S-32-6', '2280S-60-3']

        self._add_property('outputs[].auto_zero',
                        self._get_output_auto_zero,
                        self._set_output_auto_zero)

        self._add_property('outputs[].number_of_digits',
                        self._get_output_number_of_digits,
                        self._set_output_number_of_digits)

        self._add_property('outputs[].number_of_power_line_cycles',
                        self._get_output_number_of_power_line_cycles,
                        self._set_output_number_of_power_line_cycles)

        self._add_property('outputs[].trigger_count',
                        self._get_output_trigger_count,
                        self._set_output_trigger_count)

        self._add_property('outputs[].trigger_sample_count',
                        self._get_output_trigger_sample_count,
                        self._set_output_trigger_sample_count)

        self._add_method('trigger.initiate',
                        self._trigger_initiate)

        self._add_method('trigger.abort',
                        self._trigger_abort)

        self._add_property('outputs[].trigger_source',
                        self._get_output_trigger_source,
                        self._set_output_trigger_source)

        self._add_property('outputs[].measurement_type',
                        self._get_output_measurement_type,
                        self._set_output_measurement_type)

        self._add_property('outputs[].measurement_range',
                        self._get_output_measurement_range,
                        self._set_output_measurement_range)

        self._add_method('outputs[].configure_measurement',
                         self._output_configure_measurement)

        self._init_outputs()

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        "Opens an I/O session to the instrument."

        super(keithley2280S, self)._initialize(resource, id_query, reset, **keywargs)

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

    def _init_outputs(self):
        try:
            super(keithley2280S, self)._init_outputs()
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
        self._output_trigger_count = list()
        self._output_trigger_sample_count = list()
        self._output_number_of_power_line_cycles = list()
        self._output_number_of_digits = list()
        self._output_measurement_type = list()
        self._output_measurement_range = list()
        self._output_auto_zero = list()
        for i in range(self._output_count):
            self._output_current_limit.append(0)
            self._output_current_limit_behavior.append('regulate')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(0)
            self._output_voltage_level.append(0)
            self._output_trigger_source.append('bus')
            self._output_trigger_delay.append(0)
            self._output_trigger_count.append(1)
            self._output_trigger_sample_count.append(1)
            self._output_number_of_power_line_cycles.append(1)
            self._output_number_of_digits.append(6)
            self._output_measurement_type.append('concurrent')
            self._output_measurement_range.append(0.01)
            self._output_auto_zero.append(True)


    def _get_output_auto_zero(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_auto_zero = (self._ask("system:azero%d:state?" % (index+1)) == '1')
            self._set_cache_valid(index=index)
        return self._output_auto_zero

    def _set_output_auto_zero(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("system:azero%d:state %s" % (index+1,('off', 'on')[value]))
            self._set_cache_valid(index=index)
        self._output_auto_zero = value

    def _get_output_number_of_power_line_cycles(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            # Need to write initialized measurement type for the operation to be processed
            self._output_number_of_power_line_cycles = self._ask(":sense%d:%s:nplcycles?" % (index+1, self._output_measurement_type[index]))
            self._set_cache_valid(index=index)
        return self._output_number_of_power_line_cycles

    def _set_output_number_of_power_line_cycles(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            # Need to write initialized measurement type for the operation to be processed
            self._write(":sense%d:%s:nplcycles %f" % (index+1, self._output_measurement_type[index], float(value)))
            self._set_cache_valid(index=index)
        self._output_number_of_power_line_cycles = value

    def _get_output_number_of_digits(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            # Need to write initialized measurement type for the operation to be processed
            self._output_number_of_digits = self._ask(":sense%d:%s:digits?" % (index+1, self._output_measurement_type[index]))
            self._set_cache_valid(index=index)
        return self._output_number_of_digits

    def _set_output_number_of_digits(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if (value < 4) or (value > 6):
            raise ivi.OutOfRangeException('Number of measurement digits must be between 4 and 6')
        if not self._driver_operation_simulate:
            # Need to write initialized measurement type for the operation to be processed
            self._write(":sense%d:%s:digits %d" % (index+1, self._output_measurement_type[index], value))
            self._set_cache_valid(index=index)
        self._output_number_of_power_line_cycles = value

    def _get_output_current_limit_behavior(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_current_limit_behavior[index] = 'regulate'
            self._set_cache_valid(index=index)
        return self._output_current_limit_behavior[index]

    def _set_output_current_limit_behavior(self, index, value):
        raise ivi.ValueNotSupportedException()

    def _get_output_ovp_enabled(self, index):
        # Alwayas enabled by default
        return True
    
    def _set_output_ovp_enabled(self, index, value):
        # Alwayas enabled by default
        raise ivi.ValueNotSupportedException()

    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ovp_limit[index] = float(self._ask("source%d:voltage:protection:level?" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_ovp_limit[index]

    def _set_output_ovp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['ovp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source%d:voltage:protection:level %f" % (index+1, float(value)))
        self._output_ovp_limit[index] = value
        self._set_cache_valid(index=index)
        
    def _get_output_ocp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ocp_limit[index] = float(self._ask("source%d:current:protection:level?" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_ocp_limit[index]

    def _set_output_ocp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['ocp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("source%d:current:protection:level %f" % (index+1,float(value)))
        self._output_ocp_limit[index] = value
        self._set_cache_valid(index=index)

    def _output_reset_output_protection(self):
        if not self._driver_operation_simulate:
            self._write("output:protection:clear")

    def _get_output_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("trigger:sequence%d:source?" % (index+1)).lower()
            self._output_trigger_source[index] = [k for k,v in TriggerSourceMapping.items() if v==value][0]
        return self._output_trigger_source[index]
    
    def _set_output_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        if value not in TriggerSourceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("trigger:sequence%d:source %s" % (index+1, TriggerSourceMapping[value]))
        self._output_trigger_source = value
        self._set_cache_valid()

    def _get_output_trigger_count(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_count[index] = int(self._ask("trigger:sequence%d:count?" % (index+1)))
        self._set_cache_valid()
        return self._output_trigger_count[index]
        

    def _set_output_trigger_count(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if (value < 0) or (value > 2500):
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("trigger:sequence%d:count %d" % (index+1, value))
        self._output_trigger_count[index] = value
        self._set_cache_valid(index=index)

    def _get_output_trigger_sample_count(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_trigger_sample_count[index] = int(self._ask("trigger:sequence%d:sample:count?" % (index+1)))
            self._set_cache_valid(index=index)
        return self._output_trigger_sample_count[index]

    def _set_output_trigger_sample_count(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if (value < 0) or (value > 2500):
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("trigger:sequence%d:sample:count %d" % (index+1, value))
        self._output_trigger_sample_count[index] = value
        self._set_cache_valid(index=index)

    def _trigger_abort(self):
        if not self._driver_operation_simulate:
            self._write("abort") # TODO: output dependent trigger abort
    
    def _trigger_initiate(self):
        if not self._driver_operation_simulate:
            self._write("initiate") #TODO: Output dependent trigger initiate

    def _get_output_measurement_type(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            value = self._ask("sense%d:function?" % (index+1)).lower()[1:-1]
            self._output_measurement_type[index] = [k for k,v in MeasurementTypeMapping.items() if v==value][0]
            self._set_cache_valid(index=index)
        return self._output_measurement_type[index]

    def _set_output_measurement_type(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("sense%d:function \"%s\"" % (index+1, type))
        self._output_measurement_type[index] = type
        self._set_cache_valid(index=index)

    def _get_output_measurement_range(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._output_measurement_range[index] = float(self._ask("sense%d:%s:range?" % (index+1, self._output_measurement_type[index]))) #TODO: add auto range
        self._set_cache_valid(index=index)
        return self._output_measurement_range[index]

    def _set_output_measurement_range(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("sense%d:%s:range %s" % (index+1, self._output_measurement_type[index], value)) #TODO: add auto range
        self._output_measurement_range[index] = value
        self._set_cache_valid(index=index)

    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in set(['voltage', 'current']):
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("FORM:ELEM \"READ\"")
        if type == 'voltage':
            if not self._driver_operation_simulate:
                return float(self._ask("measure:voltage?"))
        if type == 'current':
                return float(self._ask("measure:current?"))
        return 0
    
    def _output_configure_measurement(self, index, type, sample_count=1, NPLC=1, measurement_digits=6, measurement_range=0.01, auto_zero=True):
        index = ivi.get_index(self._output_name, index)
        if type not in MeasurementType:
            raise ivi.ValueNotSupportedException()

        if not self._driver_operation_simulate:
            # extend buffer memory size if sample_count exceeds configured buffer size
            if int(self._ask(":trace:points?")) < sample_count:
                self._write(":trace:points %d" % sample_count)

        self._set_output_measurement_type(index, type)
        self._set_output_measurement_range(index, measurement_range)
        self._set_output_number_of_digits(index, measurement_digits)
        self._set_output_trigger_sample_count(index, sample_count)
        self._set_output_number_of_power_line_cycles(index, NPLC)
        self._set_output_auto_zero(index, auto_zero)


#    def _output_measure_statistics(self, index, type):
#        index = ivi.get_index(self._output_name, index)
#        if type not in MeasurementType:
#            raise ivi.ValueNotSupportedException()
#        if type == 'voltage':
#            if not self._driver_operation_simulate:
#                self._write("calculate2:function \"voltage\"")
#                return [float(v) for v in self._ask("measure:voltage?").split(',')]
#        if type == 'current':
#            if not self._driver_operation_simulate:
#                self._write("calculate2:function \"current\"")
#                return float(self._ask("measure:current?").split(',')[0][:-1])
#        elif type == 'concurrent': # Measure both current and voltage at the same time
#            if not self._driver_operation_simulate:
#                self._write("calculate2:function concurrent")
#        return 0