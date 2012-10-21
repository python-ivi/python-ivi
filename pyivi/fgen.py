"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012 Alex Forencich

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

from . import ivi

# Exceptions
class InvalidWaveformChannelException(ivi.IviException): pass
class NoSequencesAvailableException(ivi.IviException): pass
class NoWaveformsAvailableException(ivi.IviException): pass
class SequenceInUseException(ivi.IviException): pass
class WaveformInUseException(ivi.IviException): pass

# Parameter Values
OutputMode = set(['function', 'arbitrary', 'sequence'])
OperationMode = set(['continuous', 'burst'])
StandardWaveform = set(['sine', 'square', 'triangle', 'ramp_up', 'ramp_down', 'dc'])
SampleClockSource = set(['internal', 'external'])
MarkerPolarity = set(['active_high', 'active_low'])
AMSource = set(['internal', 'external'])
FMSource = set(['internal', 'external'])
BinaryAlignment = set(['left', 'right'])
TerminalConfiguration = set(['single_ended', 'differential'])
TriggerSlope = set(['positive', 'negative', 'either'])


class Base(object):
    "Base IVI methods for all function generators"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_outputs calls from other __init__ methods
        self._output_count = 1
        
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenBase')
        
        self._output_name = list()
        self._output_operation_mode = list()
        self._output_enabled = list()
        self._output_impedance = list()
        self._output_mode = list()
        self._output_reference_clock_source = list()
        self._output_count = 1
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('name',
                        self._get_output_name)
        self.outputs._add_property('operation_mode',
                        self._get_output_operation_mode,
                        self._set_output_operation_mode)
        self.outputs._add_property('enabled',
                        self._get_output_enabled,
                        self._set_output_enabled)
        self.outputs._add_property('impedance',
                        self._get_output_impedance,
                        self._set_output_impedance)
        self.outputs._add_property('mode',
                        self._get_output_mode,
                        self._set_output_mode)
        self.outputs._add_property('reference_clock_source',
                        self._get_output_reference_clock_source,
                        self._set_output_reference_clock_source)
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        self._output_name = list()
        self._output_operation_mode = list()
        self._output_enabled = list()
        self._output_impedance = list()
        self._output_mode = list()
        self._output_reference_clock_source = list()
        for i in range(self._output_count):
            self._output_name.append("output%d" % (i+1))
            self._output_operation_mode.append('continuous')
            self._output_enabled.append(False)
            self._output_impedance.append(0)
            self._output_mode.append('function')
            self._output_reference_clock_source.append('')
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_name(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_name[index]
    
    def _get_output_operation_mode(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_operation_mode[index]
    
    def _set_output_operation_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in OperationMode:
            raise ivi.ValueNotSupportedException()
        self._output_operation_mode[index] = value
    
    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_enabled[index]
    
    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_enabled[index] = value
    
    def _get_output_impedance(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_impedance[index]
    
    def _set_output_impedance(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_impedance[index] = value
    
    def _get_output_mode(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_mode[index]
    
    def _set_output_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in OutputMode:
            raise ivi.ValueNotSupportedException()
        self._output_mode[index] = value
    
    def _get_output_reference_clock_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_reference_clock_source[index]
    
    def _set_output_reference_clock_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_reference_clock_source[index] = value
    
    def abort_generation(self):
        pass
    
    def initiate_generation(self):
        pass
    
    
class StdFunc(object):
    "Extension IVI methods for function generators that can produce manufacturer-supplied periodic waveforms"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenStdFunc')
        
        self._output_standard_waveform_amplitude = list()
        self._output_standard_waveform_dc_offset = list()
        self._output_standard_waveform_duty_cycle_high = list()
        self._output_standard_waveform_frequency = list()
        self._output_standard_waveform_start_phase = list()
        self._output_standard_waveform_waveform_function = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('standard_waveform.amplitude',
                        self._get_output_standard_waveform_amplitude,
                        self._set_output_standard_waveform_amplitude)
        self.outputs._add_property('standard_waveform.dc_offset',
                        self._get_output_standard_waveform_dc_offset,
                        self._set_output_standard_waveform_dc_offset)
        self.outputs._add_property('standard_waveform.duty_cycle_high',
                        self._get_output_standard_waveform_duty_cycle_high,
                        self._set_output_standard_waveform_duty_cycle_high)
        self.outputs._add_property('standard_waveform.start_phase',
                        self._get_output_standard_waveform_start_phase,
                        self._set_output_standard_waveform_start_phase)
        self.outputs._add_property('standard_waveform.frequency',
                        self._get_output_standard_waveform_frequency,
                        self._set_output_standard_waveform_frequency)
        self.outputs._add_property('standard_waveform.waveform_function',
                        self._get_output_standard_waveform_waveform_function,
                        self._set_output_standard_waveform_waveform_function)
        self.outputs._add_method('standard_waveform.configure',
                        self._output_standard_waveform_configure)
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_standard_waveform_amplitude = list()
        self._output_standard_waveform_dc_offset = list()
        self._output_standard_waveform_duty_cycle_high = list()
        self._output_standard_waveform_frequency = list()
        self._output_standard_waveform_start_phase = list()
        self._output_standard_waveform_waveform_function = list()
        for i in range(self._output_count):
            self._output_standard_waveform_amplitude.append(0)
            self._output_standard_waveform_dc_offset.append(0)
            self._output_standard_waveform_duty_cycle_high.append(0)
            self._output_standard_waveform_frequency.append(0)
            self._output_standard_waveform_start_phase.append(0)
            self._output_standard_waveform_waveform_function.append('sine')
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_standard_waveform_amplitude(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_amplitude[index]
    
    def _set_output_standard_waveform_amplitude(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_amplitude[index] = value
    
    def _get_output_standard_waveform_dc_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_dc_offset[index]
    
    def _set_output_standard_waveform_dc_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_dc_offset[index] = value
    
    def _get_output_standard_waveform_duty_cycle_high(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_duty_cycle_high[index]
    
    def _set_output_standard_waveform_duty_cycle_high(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_duty_cycle_high[index] = value
    
    def _get_output_standard_waveform_start_phase(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_start_phase[index]
    
    def _set_output_standard_waveform_start_phase(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_start_phase[index] = value
    
    def _get_output_standard_waveform_frequency(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_frequency[index]
    
    def _set_output_standard_waveform_frequency(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_frequency[index] = value
    
    def _get_output_standard_waveform_waveform_function(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_waveform_function[index]
    
    def _set_output_standard_waveform_waveform_function(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in StandardWaveform:
            raise ivi.ValueNotSupportedException()
        self._output_standard_waveform_waveform_function[index] = value
    
    def _output_standard_waveform_configure(self, index, function, amplitude, dc_offset, frequency, start_phase):
        self._set_output_standard_waveform_waveform_function(index, function)
        self._set_output_standard_waveform_amplitude(index, amplitude)
        self._set_output_standard_waveform_dc_offset(index, dc_offset)
        self._set_output_standard_waveform_frequency(index, frequency)
        self._set_output_standard_waveform_start_phase(index, start_phase)
    
    
class ArbWfm(object):
    "Extension IVI methods for function generators that can produce arbitrary waveforms"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenArbWfm')
        
        self._output_arbitrary_gain = list()
        self._output_arbitrary_offset = list()
        self._output_arbitrary_waveform = list()
        self._arbitrary_sample_rate = 0
        self._arbitrary_waveform_number_waveforms_max = 0
        self._arbitrary_waveform_size_max = 0
        self._arbitrary_waveform_size_min = 0
        self._arbitrary_waveform_quantum = 0
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('arbitrary.gain',
                        self._get_output_arbitrary_gain,
                        self._set_output_arbitrary_gain)
        self.outputs._add_property('arbitrary.offset',
                        self._get_output_arbitrary_offset,
                        self._set_output_arbitrary_offset)
        self.outputs._add_property('arbitrary.waveform',
                        self._get_output_arbitrary_waveform,
                        self._set_output_arbitrary_waveform)
        self.outputs._add_method('arbitrary.configure',
                        self._arbitrary_waveform_configure)
        self.__dict__.setdefault('arbitrary', ivi.PropertyCollection())
        self.arbitrary._add_property('sample_rate',
                        self._get_arbitrary_sample_rate,
                        self._set_arbitrary_sample_rate)
        self.arbitrary.__dict__.setdefault('waveform', ivi.PropertyCollection())
        self.arbitrary.waveform._add_property('number_waveforms_max',
                        self._get_arbitrary_waveform_number_waveforms_max)
        self.arbitrary.waveform._add_property('size_max',
                        self._get_arbitrary_waveform_size_max)
        self.arbitrary.waveform._add_property('size_min',
                        self._get_arbitrary_waveform_size_min)
        self.arbitrary.waveform._add_property('quantum',
                        self._get_arbitrary_waveform_quantum)
        self.arbitrary.waveform.configure = self._arbitrary_waveform_configure
        self.arbitrary.waveform.clear = self._arbitrary_waveform_clear
        self.arbitrary.waveform.create = self._arbitrary_waveform_create
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_arbitrary_gain = list()
        self._output_arbitrary_offset = list()
        for i in range(self._output_count):
            self._output_arbitrary_gain.append(0)
            self._output_arbitrary_offset.append(0)
            self._output_arbitrary_waveform.append('')
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_arbitrary_gain(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_gain[index]
    
    def _set_output_arbitrary_gain(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_arbitrary_gain[index] = value
    
    def _get_output_arbitrary_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_offset[index]
    
    def _set_output_arbitrary_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_arbitrary_offset[index] = value
    
    def _get_output_arbitrary_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_waveform[index]
    
    def _set_output_arbitrary_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_arbitrary_waveform[index] = value
    
    def _get_arbitrary_sample_rate(self):
        return self._arbitrary_sample_rate
    
    def _set_arbitrary_sample_rate(self, value):
        value = float(value)
        self._arbitrary_sample_rate = value
    
    def _get_arbitrary_waveform_number_waveforms_max(self):
        return self._arbitrary_waveform_number_waveforms_max
    
    def _get_arbitrary_waveform_size_max(self):
        return self._arbitrary_waveform_size_max
    
    def _get_arbitrary_waveform_size_min(self):
        return self._arbitrary_waveform_size_min
    
    def _get_arbitrary_waveform_quantum(self):
        return self._arbitrary_waveform_quantum
    
    def _arbitrary_waveform_clear(self, handle):
        pass
    
    def _arbitrary_waveform_configure(self, index, handle, gain, offset):
        self._set_output_arbitrary_waveform(index, handle)
        self._set_output_arbitrary_gain(index, gain)
        self._set_output_arbitrary_offset(index, offset)
    
    def _arbitrary_waveform_create(self, data):
        return "handle"
    
    
class ArbFrequency(object):
    "Extension IVI methods for function generators that can produce arbitrary waveforms with variable rate"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenArbFrequency')
        
        self._output_arbitrary_frequency = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('arbitrary.frequency',
                        self._get_output_arbitrary_frequency,
                        self._set_output_arbitrary_frequency)
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_arbitrary_frequency = list()
        for i in range(self._output_count):
            self._output_arbitrary_frequency.append(0)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_arbitrary_frequency(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_arbitrary_frequency[index]
    
    def _set_output_arbitrary_frequency(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_arbitrary_frequency[index] = value
    
    
class ArbSeq(object):
    "Extension IVI methods for function generators that can produce sequences of arbitrary waveforms"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenArbSeq')
        
        self._arbitrary_sequence_number_sequences_max = 0
        self._arbitrary_sequence_loop_count_max = 0
        self._arbitrary_sequence_length_max = 0
        self._arbitrary_sequence_length_min = 0
        
        self.__dict__.setdefault('arbitrary', ivi.PropertyCollection())
        self.arbitrary.__dict__.setdefault('sequence', ivi.PropertyCollection())
        self.arbitrary.sequence._add_property('number_sequences_max',
                        self._get_arbitrary_sequence_number_sequences_max)
        self.arbitrary.sequence._add_property('loop_count_max',
                        self._get_arbitrary_sequence_loop_count_max)
        self.arbitrary.sequence._add_property('length_max',
                        self._get_arbitrary_sequence_length_max)
        self.arbitrary.sequence._add_property('length_min',
                        self._get_arbitrary_sequence_length_min)
        self.arbitrary.clear_memory = self._arbitrary_clear_memory
        self.arbitrary.sequence.clear = self._arbitrary_sequence_clear
        self.arbitrary.sequence.configure = self._arbitrary_sequence_configure
        self.arbitrary.sequence.create = self._arbitrary_sequence_create
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_method('arbitrary.sequence.configure',
                        self._arbitrary_sequence_configure)
    
    def _get_arbitrary_sequence_number_sequences_max(self):
        return self._arbitrary_sequence_number_sequences_max
    
    def _get_arbitrary_sequence_loop_count_max(self):
        return self._arbitrary_sequence_loop_count_max
    
    def _get_arbitrary_sequence_length_max(self):
        return self._arbitrary_sequence_length_max
    
    def _get_arbitrary_sequence_length_min(self):
        return self._arbitrary_sequence_length_min
    
    def _arbitrary_clear_memory(self):
        pass
    
    def _arbitrary_sequence_clear(self, handle):
        pass
    
    def _arbitrary_sequence_configure(self, index, handle, gain, offset):
        pass
    
    def _arbitrary_sequence_create(self, handle_list, loop_count_list):
        return "handle"
    
    
class Trigger(object):
    "Extension IVI methods for function generators that support triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenTrigger')
        
        self._output_trigger_source = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger.source',
                        self._get_output_trigger_source,
                        self._set_output_trigger_source)
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_trigger_source = list()
        for i in range(self._output_count):
            self._output_trigger_source.append('')
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_trigger_source[index]
    
    def _set_output_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_trigger_source[index] = value
    
    
class StartTrigger(object):
    "Extension IVI methods for function generators that support start triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenStartTrigger')
        
        self._output_start_trigger_delay = list()
        self._output_start_trigger_slope = list()
        self._output_start_trigger_source = list()
        self._output_start_trigger_threshold = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger.start.delay',
                        self._get_output_start_trigger_delay,
                        self._set_output_start_trigger_delay)
        self.outputs._add_property('trigger.start.slope',
                        self._get_output_start_trigger_slope,
                        self._set_output_start_trigger_slope)
        self.outputs._add_property('trigger.start.source',
                        self._get_output_start_trigger_source,
                        self._set_output_start_trigger_source)
        self.outputs._add_property('trigger.start.threshold',
                        self._get_output_start_trigger_threshold,
                        self._set_output_start_trigger_threshold)
        self.outputs._add_method('trigger.start.configure',
                        self._output_start_trigger_configure)
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger.__dict__.setdefault('start', ivi.PropertyCollection())
        self.trigger.start.configure = _output_start_trigger_configure
        self.trigger.start.send_software_trigger = _start_trigger_send_software_trigger
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_start_trigger_delay = list()
        self._output_start_trigger_slope = list()
        self._output_start_trigger_source = list()
        self._output_start_trigger_threshold = list()
        for i in range(self._output_count):
            self._output_start_trigger_delay.append(0)
            self._output_start_trigger_slope.append('positive')
            self._output_start_trigger_source.append('')
            self._output_start_trigger_threshold.append(0)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_start_trigger_delay(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_start_trigger_delay[index]
    
    def _set_output_start_trigger_delay(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_start_trigger_delay[index] = value
    
    def _get_output_start_trigger_slope(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_start_trigger_slope[index]
    
    def _set_output_start_trigger_slope(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TriggerSlope:
            raise ivi.ValueNotSupportedException()
        self._output_start_trigger_slope[index] = value
    
    def _get_output_start_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_start_trigger_source[index]
    
    def _set_output_start_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_start_trigger_source[index] = value
    
    def _get_output_start_trigger_threshold(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_start_trigger_threshold[index]
    
    def _set_output_start_trigger_threshold(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_start_trigger_threshold[index] = value
    
    def _output_start_trigger_configure(self, index, source, slope):
        self._set_output_start_trigger_source(index, source)
        self._set_output_start_trigger_slope(index, slope)
    
    def _start_trigger_send_software_trigger(self):
        pass
    
    
class StopTrigger(object):
    "Extension IVI methods for function generators that support stop triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenStopTrigger')
        
        self._output_stop_trigger_delay = list()
        self._output_stop_trigger_slope = list()
        self._output_stop_trigger_source = list()
        self._output_stop_trigger_threshold = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger.stop.delay',
                        self._get_output_stop_trigger_delay,
                        self._set_output_stop_trigger_delay)
        self.outputs._add_property('trigger.stop.slope',
                        self._get_output_stop_trigger_slope,
                        self._set_output_stop_trigger_slope)
        self.outputs._add_property('trigger.stop.source',
                        self._get_output_stop_trigger_source,
                        self._set_output_stop_trigger_source)
        self.outputs._add_property('trigger.stop.threshold',
                        self._get_output_stop_trigger_threshold,
                        self._set_output_stop_trigger_threshold)
        self.outputs._add_method('trigger.stop.configure',
                        self._output_stop_trigger_configure)
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger.__dict__.setdefault('stop', ivi.PropertyCollection())
        self.trigger.stop.configure = _output_stop_trigger_configure
        self.trigger.stop.send_software_trigger = _stop_trigger_send_software_trigger
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_stop_trigger_delay = list()
        self._output_stop_trigger_slope = list()
        self._output_stop_trigger_source = list()
        self._output_stop_trigger_threshold = list()
        for i in range(self._output_count):
            self._output_stop_trigger_delay.append(0)
            self._output_stop_trigger_slope.append('positive')
            self._output_stop_trigger_source.append('')
            self._output_stop_trigger_threshold.append(0)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_stop_trigger_delay(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_stop_trigger_delay[index]
    
    def _set_output_stop_trigger_delay(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_stop_trigger_delay[index] = value
    
    def _get_output_stop_trigger_slope(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_stop_trigger_slope[index]
    
    def _set_output_stop_trigger_slope(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TriggerSlope:
            raise ivi.ValueNotSupportedException()
        self._output_stop_trigger_slope[index] = value
    
    def _get_output_stop_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_stop_trigger_source[index]
    
    def _set_output_stop_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_stop_trigger_source[index] = value
    
    def _get_output_stop_trigger_threshold(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_stop_trigger_threshold[index]
    
    def _set_output_stop_trigger_threshold(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_stop_trigger_threshold[index] = value
    
    def _output_stop_trigger_configure(self, index, source, slope):
        self._set_output_stop_trigger_source(index, source)
        self._set_output_stop_trigger_slope(index, slope)
    
    def _stop_trigger_send_software_trigger(self):
        pass
    
    
class HoldTrigger(object):
    "Extension IVI methods for function generators that support hold triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenHoldTrigger')
        
        self._output_hold_trigger_delay = list()
        self._output_hold_trigger_slope = list()
        self._output_hold_trigger_source = list()
        self._output_hold_trigger_threshold = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger.hold.delay',
                        self._get_output_hold_trigger_delay,
                        self._set_output_hold_trigger_delay)
        self.outputs._add_property('trigger.hold.slope',
                        self._get_output_hold_trigger_slope,
                        self._set_output_hold_trigger_slope)
        self.outputs._add_property('trigger.hold.source',
                        self._get_output_hold_trigger_source,
                        self._set_output_hold_trigger_source)
        self.outputs._add_property('trigger.hold.threshold',
                        self._get_output_hold_trigger_threshold,
                        self._set_output_hold_trigger_threshold)
        self.outputs._add_method('trigger.hold.configure',
                        self._output_hold_trigger_configure)
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger.__dict__.setdefault('hold', ivi.PropertyCollection())
        self.trigger.hold.configure = _output_hold_trigger_configure
        self.trigger.hold.send_software_trigger = _hold_trigger_send_software_trigger
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_hold_trigger_delay = list()
        self._output_hold_trigger_slope = list()
        self._output_hold_trigger_source = list()
        self._output_hold_trigger_threshold = list()
        for i in range(self._output_count):
            self._output_hold_trigger_delay.append(0)
            self._output_hold_trigger_slope.append('positive')
            self._output_hold_trigger_source.append('')
            self._output_hold_trigger_threshold.append(0)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_hold_trigger_delay(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_hold_trigger_delay[index]
    
    def _set_output_hold_trigger_delay(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_hold_trigger_delay[index] = value
    
    def _get_output_hold_trigger_slope(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_hold_trigger_slope[index]
    
    def _set_output_hold_trigger_slope(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TriggerSlope:
            raise ivi.ValueNotSupportedException()
        self._output_hold_trigger_slope[index] = value
    
    def _get_output_hold_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_hold_trigger_source[index]
    
    def _set_output_hold_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_hold_trigger_source[index] = value
    
    def _get_output_hold_trigger_threshold(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_hold_trigger_threshold[index]
    
    def _set_output_hold_trigger_threshold(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_hold_trigger_threshold[index] = value
    
    def _output_hold_trigger_configure(self, index, source, slope):
        self._set_output_hold_trigger_source(index, source)
        self._set_output_hold_trigger_slope(index, slope)
    
    def _hold_trigger_send_software_trigger(self):
        pass
    
    
class ResumeTrigger(object):
    "Extension IVI methods for function generators that support resume triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenResumeTrigger')
        
        self._output_resume_trigger_delay = list()
        self._output_resume_trigger_slope = list()
        self._output_resume_trigger_source = list()
        self._output_resume_trigger_threshold = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger.resume.delay',
                        self._get_output_resume_trigger_delay,
                        self._set_output_resume_trigger_delay)
        self.outputs._add_property('trigger.resume.slope',
                        self._get_output_resume_trigger_slope,
                        self._set_output_resume_trigger_slope)
        self.outputs._add_property('trigger.resume.source',
                        self._get_output_resume_trigger_source,
                        self._set_output_resume_trigger_source)
        self.outputs._add_property('trigger.resume.threshold',
                        self._get_output_resume_trigger_threshold,
                        self._set_output_resume_trigger_threshold)
        self.outputs._add_method('trigger.resume.configure',
                        self._output_resume_trigger_configure)
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger.__dict__.setdefault('resume', ivi.PropertyCollection())
        self.trigger.resume.configure = _output_resume_trigger_configure
        self.trigger.resume.send_software_trigger = _resume_trigger_send_software_trigger
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_resume_trigger_delay = list()
        self._output_resume_trigger_slope = list()
        self._output_resume_trigger_source = list()
        self._output_resume_trigger_threshold = list()
        for i in range(self._output_count):
            self._output_resume_trigger_delay.append(0)
            self._output_resume_trigger_slope.append('positive')
            self._output_resume_trigger_source.append('')
            self._output_resume_trigger_threshold.append(0)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_resume_trigger_delay(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_resume_trigger_delay[index]
    
    def _set_output_resume_trigger_delay(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_resume_trigger_delay[index] = value
    
    def _get_output_resume_trigger_slope(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_resume_trigger_slope[index]
    
    def _set_output_resume_trigger_slope(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TriggerSlope:
            raise ivi.ValueNotSupportedException()
        self._output_resume_trigger_slope[index] = value
    
    def _get_output_resume_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_resume_trigger_source[index]
    
    def _set_output_resume_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_resume_trigger_source[index] = value
    
    def _get_output_resume_trigger_threshold(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_resume_trigger_threshold[index]
    
    def _set_output_resume_trigger_threshold(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_resume_trigger_threshold[index] = value
    
    def _output_resume_trigger_configure(self, index, source, slope):
        self._set_output_resume_trigger_source(index, source)
        self._set_output_resume_trigger_slope(index, slope)
    
    def _resume_trigger_send_software_trigger(self):
        pass
    
    
class AdvanceTrigger(object):
    "Extension IVI methods for function generators that support advance triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenAdvanceTrigger')
        
        self._output_advance_trigger_delay = list()
        self._output_advance_trigger_slope = list()
        self._output_advance_trigger_source = list()
        self._output_advance_trigger_threshold = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger.advance.delay',
                        self._get_output_advance_trigger_delay,
                        self._set_output_advance_trigger_delay)
        self.outputs._add_property('trigger.advance.slope',
                        self._get_output_advance_trigger_slope,
                        self._set_output_advance_trigger_slope)
        self.outputs._add_property('trigger.advance.source',
                        self._get_output_advance_trigger_source,
                        self._set_output_advance_trigger_source)
        self.outputs._add_property('trigger.advance.threshold',
                        self._get_output_advance_trigger_threshold,
                        self._set_output_advance_trigger_threshold)
        self.outputs._add_method('trigger.advance.configure',
                        self._output_advance_trigger_configure)
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger.__dict__.setdefault('advance', ivi.PropertyCollection())
        self.trigger.advance.configure = _output_advance_trigger_configure
        self.trigger.advance.send_software_trigger = _advance_trigger_send_software_trigger
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_advance_trigger_delay = list()
        self._output_advance_trigger_slope = list()
        self._output_advance_trigger_source = list()
        self._output_advance_trigger_threshold = list()
        for i in range(self._output_count):
            self._output_advance_trigger_delay.append(0)
            self._output_advance_trigger_slope.append('positive')
            self._output_advance_trigger_source.append('')
            self._output_advance_trigger_threshold.append(0)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_advance_trigger_delay(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_advance_trigger_delay[index]
    
    def _set_output_advance_trigger_delay(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_advance_trigger_delay[index] = value
    
    def _get_output_advance_trigger_slope(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_advance_trigger_slope[index]
    
    def _set_output_advance_trigger_slope(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TriggerSlope:
            raise ivi.ValueNotSupportedException()
        self._output_advance_trigger_slope[index] = value
    
    def _get_output_advance_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_advance_trigger_source[index]
    
    def _set_output_advance_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_advance_trigger_source[index] = value
    
    def _get_output_advance_trigger_threshold(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_advance_trigger_threshold[index]
    
    def _set_output_advance_trigger_threshold(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_advance_trigger_threshold[index] = value
    
    def _output_advance_trigger_configure(self, index, source, slope):
        self._set_output_advance_trigger_source(index, source)
        self._set_output_advance_trigger_slope(index, slope)
    
    def _advance_trigger_send_software_trigger(self):
        pass
    
    
class InternalTrigger(object):
    "Extension IVI methods for function generators that support internal triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenInternalTrigger')
        
        self._internal_trigger_rate = 0
        
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger._add_property('internal_rate',
                        self._get_internal_trigger_rate,
                        self._set_internal_trigger_rate)
    
    def _get_internal_trigger_rate(self):
        return self._internal_trigger_rate
    
    def _set_internal_trigger_rate(self, value):
        value = float(value)
        self._internal_trigger_rate = value
    
    
class SoftwareTrigger(object):
    "Extension IVI methods for function generators that support software triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenSoftwareTrigger')
    
    def send_software_trigger(self):
        pass
    
    
class Burst(object):
    "Extension IVI methods for function generators that support triggered burst output"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenBurst')
        
        self._output_burst_count = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('burst_count',
                        self._get_output_burst_count,
                        self._set_output_burst_count)
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_burst_count = list()
        for i in range(self._output_count):
            self._output_burst_count.append(1)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_burst_count(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_burst_count[index]
    
    def _set_output_burst_count(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = int(value)
        self._output_burst_count[index] = value
    
    
class ModulateAM(object):
    "Extension IVI methods for function generators that support amplitude modulation"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenModulateAM')
        
        self._output_am_enabled = list()
        self._am_internal_depth = 0
        self._am_internal_frequency = 0
        self._am_internal_waveform_function = 0
        self._output_am_source = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('am.enabled',
                        self._get_output_am_enabled,
                        self._set_output_am_enabled)
        self.outputs._add_property('am.source',
                        self._get_output_am_source,
                        self._set_output_am_source)
        
        self.__dict__.setdefault('am', ivi.PropertyCollection())
        self.am._add_property('internal_depth',
                        self._get_am_internal_depth,
                        self._set_am_internal_depth)
        self.am._add_property('internal_frequency',
                        self._get_am_internal_frequency,
                        self._set_am_internal_frequency)
        self.am._add_property('internal_waveform_function',
                        self._get_am_internal_waveform_function,
                        self._set_am_internal_waveform_function)
        self.am.configure_internernal = self._am_configure_internal
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_am_enabled = list()
        for i in range(self._output_count):
            self._output_am_enabled.append(False)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_am_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_am_enabled[index]
    
    def _set_output_am_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_am_enabled[index] = value
    
    def _get_output_am_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_am_source[index]
    
    def _set_output_am_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_am_source[index] = value
    
    def _get_am_internal_depth(self):
        return self._am_internal_depth
    
    def _set_am_internal_depth(self, value):
        value = float(value)
        self._am_internal_depth = value
    
    def _get_am_internal_frequency(self):
        return self._am_internal_frequency
    
    def _set_am_internal_frequency(self, value):
        value = float(value)
        self._am_internal_frequency = value
    
    def _get_am_internal_waveform_function(self):
        return self._am_internal_waveform_function
    
    def _set_am_internal_waveform_function(self, value):
        value = float(value)
        self._am_internal_waveform_function = value
    
    def _am_configure_internal(self, depth, waveform_function, frequency):
        self._set_am_internal_depth(depth)
        self._set_am_internal_waveform_function(waveform_function)
        self._set_am_internal_frequency(frequency)
    
    
class ModulateFM(object):
    "Extension IVI methods for function generators that support frequency modulation"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenModulateAM')
        
        self._output_fm_enabled = list()
        self._fm_internal_deviation = 0
        self._fm_internal_frequency = 0
        self._fm_internal_waveform_function = 0
        self._output_fm_source = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('fm.enabled',
                        self._get_output_fm_enabled,
                        self._set_output_fm_enabled)
        self.outputs._add_property('fm.source',
                        self._get_output_fm_source,
                        self._set_output_fm_source)
        
        self.__dict__.setdefault('fm', ivi.PropertyCollection())
        self.fm._add_property('internal_deviation',
                        self._get_fm_internal_deviation,
                        self._set_fm_internal_deviation)
        self.fm._add_property('internal_frequency',
                        self._get_fm_internal_frequency,
                        self._set_fm_internal_frequency)
        self.fm._add_property('internal_waveform_function',
                        self._get_fm_internal_waveform_function,
                        self._set_fm_internal_waveform_function)
        self.fm.configure_internernal = self._fm_configure_internal
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_fm_enabled = list()
        for i in range(self._output_count):
            self._output_fm_enabled.append(False)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_fm_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_fm_enabled[index]
    
    def _set_output_fm_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_fm_enabled[index] = value
    
    def _get_output_fm_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_fm_source[index]
    
    def _set_output_fm_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_fm_source[index] = value
    
    def _get_fm_internal_deviation(self):
        return self._fm_internal_deviation
    
    def _set_fm_internal_deviation(self, value):
        value = float(value)
        self._fm_internal_deviation = value
    
    def _get_fm_internal_frequency(self):
        return self._fm_internal_frequency
    
    def _set_fm_internal_frequency(self, value):
        value = float(value)
        self._fm_internal_frequency = value
    
    def _get_fm_internal_waveform_function(self):
        return self._fm_internal_waveform_function
    
    def _set_fm_internal_waveform_function(self, value):
        value = float(value)
        self._fm_internal_waveform_function = value
    
    def _fm_configure_internal(self, deviation, waveform_function, frequency):
        self._set_fm_internal_deviation(deviation)
        self._set_fm_internal_waveform_function(waveform_function)
        self._set_fm_internal_frequency(frequency)
    
    
class SampleClock(object):
    "Extension IVI methods for function generators that support external sample clocks"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenSampleClock')
        
        self._sample_clock_source = 'internal'
        self._sample_clock_output_enabled = ''
        
        self.__dict__.setdefault('sample_clock', ivi.PropertyCollection())
        self.sample_clock._add_property('source',
                        self._get_sample_clock_source,
                        self._set_sample_clock_source)
        self.sample_clock._add_property('output_enabled',
                        self._get_sample_clock_output_enabled,
                        self._set_sample_clock_output_enabled)
        
    def _get_sample_clock_source(self):
        return self._sample_clock_source
    
    def _set_sample_clock_source(self, value):
        if value not in SampleClockSource:
            raise ivi.ValueNotSupportedException()
        self._sample_clock_source = value
    
    def _get_sample_clock_output_enabled(self):
        return self._sample_clock_output_enabled
    
    def _set_sample_clock_output_enabled(self, value):
        value = bool(value)
        self._sample_clock_output_enabled = value
    
    
class TerminalConfiguration(object):
    "Extension IVI methods for function generators that support single ended or differential output selection"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenTerminalConfiguration')
        
        self._output_terminal_configuration = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('terminal_configuration',
                        self._get_output_terminal_configuration,
                        self._set_output_terminal_configuration)
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_terminal_configuration = list()
        for i in range(self._output_count):
            self._output_terminal_configuration.append('single_ended')
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_terminal_configuration(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_terminal_configuration[index]
    
    def _set_output_terminal_configuration(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in TerminalConfiguration:
            return ivi.ValueNotSupportedException()
        self._output_terminal_configuration[index] = value
    
    
class ArbChannelWfm(object):
    "Extension IVI methods for function generators that support user-defined arbitrary waveform generation"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenArbChannelWfm')
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_method('arbitrary.waveform.create_channel_waveform',
                        self._arbitrary_waveform_create_channel_waveform)
        self.__dict__.setdefault('arbitrary', ivi.PropertyCollection())
        self.arbitrary.__dict__.setdefault('waveform', ivi.PropertyCollection())
        self.arbitrary.waveform.create_channel_waveform = self._arbitrary_waveform_create_channel_waveform
    
    def _arbitrary_waveform_create_channel_waveform(self, index, data):
        index = ivi.get_index(self._output_name, index)
        return 'handle'
    
    
class ArbWfmBinary(object):
    "Extension IVI methods for function generators that support user-defined arbitrary binary waveform generation"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenArbWfmBinary')
        
        self._arbitrary_binary_alignment = 'right'
        self._arbitrary_sample_bit_resolution = 16
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_method('arbitrary.waveform.create_channel_waveform_int16',
                        self._arbitrary_waveform_create_channel_waveform_int16)
        self.outputs._add_method('arbitrary.waveform.create_channel_waveform_int32',
                        self._arbitrary_waveform_create_channel_waveform_int32)
        self.__dict__.setdefault('arbitrary', ivi.PropertyCollection())
        self.arbitrary._add_property('binary_alignment',
                        self._get_arbitrary_binary_alignment)
        self.arbitrary._add_property('sample_bit_resolution',
                        self._get_arbitrary_sample_bit_resolution)
        self.arbitrary.__dict__.setdefault('waveform', ivi.PropertyCollection())
        self.arbitrary.waveform.create_channel_waveform_int16 = self._arbitrary_waveform_create_channel_waveform_int16
        self.arbitrary.waveform.create_channel_waveform_int32 = self._arbitrary_waveform_create_channel_waveform_int32
    
    def _get_arbitrary_binary_alignment(self):
        return self._arbitrary_binary_alignment
    
    def _get_arbitrary_sample_bit_resolution(self):
        return self._arbitrary_sample_bit_resolution
    
    def _arbitrary_waveform_create_channel_waveform_int16(self, index, data):
        index = ivi.get_index(self._output_name, index)
        return 'handle'
    
    def _arbitrary_waveform_create_channel_waveform_int32(self, index, data):
        index = ivi.get_index(self._output_name, index)
        return 'handle'
    
    
class DataMarker(object):
    "Extension IVI methods for function generators that support output of particular waveform data bits as markers"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenDataMarker')
        
        self._data_marker_count = 1
        self._data_marker_name = list()
        self._data_marker_amplitude = list()
        self._data_marker_bit_position = list()
        self._data_marker_delay = list()
        self._data_marker_destination = list()
        self._data_marker_polarity = list()
        self._data_marker_source_channel = list()
        
        self.__dict__.setdefault('data_markers', ivi.IndexedPropertyCollection())
        self.data_markers._add_property('name',
                        self._get_data_marker_name)
        self.data_markers._add_property('amplitude',
                        self._get_data_marker_amplitude,
                        self._set_data_marker_amplitude)
        self.data_markers._add_property('bit_position',
                        self._get_data_marker_bit_position,
                        self._set_data_marker_bit_position)
        self.data_markers._add_property('delay',
                        self._get_data_marker_delay,
                        self._set_data_marker_delay)
        self.data_markers._add_property('destination',
                        self._get_data_marker_destination,
                        self._set_data_marker_destination)
        self.data_markers._add_property('polarity',
                        self._get_data_marker_polarity,
                        self._set_data_marker_polarity)
        self.data_markers._add_property('source_channel',
                        self._get_data_marker_source_channel,
                        self._set_data_marker_source_channel)
        self.data_markers._add_method('configure',
                        self._data_marker_configure)
        self.data_markers.clear = self._data_marker_clear
        
        self._init_data_markers()
        
    def _init_data_markers(self):
        try:
            super()._init_data_markers()
        except AttributeError:
            pass
        
        self._data_marker_name = list()
        self._data_marker_amplitude = list()
        self._data_marker_bit_position = list()
        self._data_marker_delay = list()
        self._data_marker_destination = list()
        self._data_marker_polarity = list()
        self._data_marker_source_channel = list()
        
        for i in range(self._data_marker_count):
            self._data_marker_name.append('marker%d' % (i+1))
            self._data_marker_amplitude.append(0)
            self._data_marker_bit_position.append(0)
            self._data_marker_delay.append(0)
            self._data_marker_destination.append('')
            self._data_marker_polarity.append('active_high')
            self._data_marker_source_channel.append(self._output_name[0])
    
    def _get_data_marker_name(self, index):
        index = ivi.get_index(self._data_marker_name, index)
        return self._data_marker_name[index]
    
    def _get_data_marker_amplitude(self, index):
        index = ivi.get_index(self._data_marker_name, index)
        return self._data_marker_amplitude[index]
    
    def _set_data_marker_amplitude(self, index, value):
        index = ivi.get_index(self._data_marker_name, index)
        value = float(value)
        self._data_marker_amplitude[index] = value
    
    def _get_data_marker_bit_position(self, index):
        index = ivi.get_index(self._data_marker_name, index)
        return self._data_marker_bit_position[index]
    
    def _set_data_marker_bit_position(self, index, value):
        index = ivi.get_index(self._data_marker_name, index)
        value = int(value)
        self._data_marker_bit_position[index] = value
    
    def _get_data_marker_delay(self, index):
        index = ivi.get_index(self._data_marker_name, index)
        return self._data_marker_delay[index]
    
    def _set_data_marker_delay(self, index, value):
        index = ivi.get_index(self._data_marker_name, index)
        value = float(value)
        self._data_marker_delay[index] = value
    
    def _get_data_marker_destination(self, index):
        index = ivi.get_index(self._data_marker_name, index)
        return self._data_marker_destination[index]
    
    def _set_data_marker_destination(self, index, value):
        index = ivi.get_index(self._data_marker_name, index)
        value = str(value)
        self._data_marker_destination[index] = value
    
    def _get_data_marker_polarity(self, index):
        index = ivi.get_index(self._data_marker_name, index)
        return self._data_marker_polarity[index]
    
    def _set_data_marker_polarity(self, index, value):
        index = ivi.get_index(self._data_marker_name, index)
        if value not in MarkerPolarity:
            raise ivi.ValueNotSupportedException()
        self._data_marker_polarity[index] = value
    
    def _get_data_marker_source_channel(self, index):
        index = ivi.get_index(self._data_marker_name, index)
        return self._data_marker_source_channel[index]
    
    def _set_data_marker_source_channel(self, index, value):
        index = ivi.get_index(self._data_marker_name, index)
        value = ivi.get_index(self._output_name, value)
        value = self._output_name[value]
        self._data_marker_source_channel[index] = value
    
    def _data_marker_configure(self, index, source_channel, bit_position, destination):
        self._set_data_marker_source_channel(index, source_channel)
        self._set_data_marker_bit_position(index, bit_position)
        self._set_data_marker_destination(index, destination)
    
    def _data_marker_clear(self):
        for i in range(self._data_marker_count):
            self._set_data_marker_destination(i, '')
    
    
class ArbDataMask(object):
    "Extension IVI methods for function generators that support masking of waveform data bits"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenArbDataMask')
        
        self._arbitrary_data_mask = 0xffffffff
        
        self.__dict__.setdefault('arbitrary', ivi.PropertyCollection())
        self.arbitrary._add_property('data_mask',
                        self._get_arbitrary_data_mask,
                        self._set_arbitrary_data_mask)
    
    def _get_arbitrary_data_mask(self):
        return self._arbitrary_data_mask
    
    def _set_arbitrary_data_mask(self, value):
        value = int(value)
        self._arbitrary_data_mask = value
    
    
class SparseMarker(object):
    "Extension IVI methods for function generators that support output of markers associated with output data samples"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenSparseMarker')
        
        self._sparse_marker_count = 1
        self._sparse_marker_name = list()
        self._sparse_marker_amplitude = list()
        self._sparse_marker_delay = list()
        self._sparse_marker_destination = list()
        self._sparse_marker_polarity = list()
        self._sparse_marker_waveform_handle = list()
        
        self.__dict__.setdefault('sparse_markers', ivi.IndexedPropertyCollection())
        self.sparse_markers._add_property('name',
                        self._get_sparse_marker_name)
        self.sparse_markers._add_property('amplitude',
                        self._get_sparse_marker_amplitude,
                        self._set_sparse_marker_amplitude)
        self.sparse_markers._add_property('delay',
                        self._get_sparse_marker_delay,
                        self._set_sparse_marker_delay)
        self.sparse_markers._add_property('destination',
                        self._get_sparse_marker_destination,
                        self._set_sparse_marker_destination)
        self.sparse_markers._add_property('polarity',
                        self._get_sparse_marker_polarity,
                        self._set_sparse_marker_polarity)
        self.sparse_markers._add_property('waveform_handle',
                        self._get_sparse_marker_waveform_handle,
                        self._set_sparse_marker_waveform_handle)
        self.sparse_markers._add_method('configure',
                        self._sparse_marker_configure)
        self.sparse_markers._add_method('get_indexes',
                        self._sparse_marker_get_indexes)
        self.sparse_markers._add_method('set_indexes',
                        self._sparse_marker_set_indexes)
        self.sparse_markers.clear = self._sparse_marker_clear
        
        self._init_sparse_markers()
        
    def _init_sparse_markers(self):
        try:
            super()._init_sparse_markers()
        except AttributeError:
            pass
        
        self._sparse_marker_name = list()
        self._sparse_marker_amplitude = list()
        self._sparse_marker_delay = list()
        self._sparse_marker_destination = list()
        self._sparse_marker_polarity = list()
        self._sparse_marker_waveform_handle = list()
        
        for i in range(self._sparse_marker_count):
            self._sparse_marker_name.append('marker%d' % (i+1))
            self._sparse_marker_amplitude.append(0)
            self._sparse_marker_delay.append(0)
            self._sparse_marker_destination.append('')
            self._sparse_marker_polarity.append('active_high')
            self._sparse_marker_waveform_handle.append('')
    
    def _get_sparse_marker_name(self, index):
        index = ivi.get_index(self._sparse_marker_name, index)
        return self._sparse_marker_name[index]
    
    def _get_sparse_marker_amplitude(self, index):
        index = ivi.get_index(self._sparse_marker_name, index)
        return self._sparse_marker_amplitude[index]
    
    def _set_sparse_marker_amplitude(self, index, value):
        index = ivi.get_index(self._sparse_marker_name, index)
        value = float(value)
        self._sparse_marker_amplitude[index] = value
    
    def _get_sparse_marker_delay(self, index):
        index = ivi.get_index(self._sparse_marker_name, index)
        return self._sparse_marker_delay[index]
    
    def _set_sparse_marker_delay(self, index, value):
        index = ivi.get_index(self._sparse_marker_name, index)
        value = float(value)
        self._sparse_marker_delay[index] = value
    
    def _get_sparse_marker_destination(self, index):
        index = ivi.get_index(self._sparse_marker_name, index)
        return self._sparse_marker_destination[index]
    
    def _set_sparse_marker_destination(self, index, value):
        index = ivi.get_index(self._sparse_marker_name, index)
        value = str(value)
        self._sparse_marker_destination[index] = value
    
    def _get_sparse_marker_polarity(self, index):
        index = ivi.get_index(self._sparse_marker_name, index)
        return self._sparse_marker_polarity[index]
    
    def _set_sparse_marker_polarity(self, index, value):
        index = ivi.get_index(self._sparse_marker_name, index)
        if value not in MarkerPolarity:
            raise ivi.ValueNotSupportedException()
        self._sparse_marker_polarity[index] = value
    
    def _get_sparse_marker_waveform_handle(self, index):
        index = ivi.get_index(self._sparse_marker_name, index)
        return self._sparse_marker_waveform_handle[index]
    
    def _set_sparse_marker_waveform_handle(self, index, value):
        index = ivi.get_index(self._sparse_marker_name, index)
        value = str(value)
        self._sparse_marker_waveform_handle[index] = value
    
    def _sparse_marker_configure(self, index, waveform_handle, indexes, destination):
        self._set_sparse_marker_waveform_handle(index, waveform_handle)
        self._set_sparse_marker_set_indexes(index, indexes)
        self._set_sparse_marker_destination(index, destination)
    
    def _sparse_marker_get_indexes(self, index):
        index = ivi.get_index(self._sparse_marker_name, index)
        return list()
    
    def _sparse_marker_set_indexes(self, index, indexes):
        index = ivi.get_index(self._sparse_marker_name, index)
        pass
    
    def _sparse_marker_clear(self):
        for i in range(self._sparse_marker_count):
            self._set_sparse_marker_destination(i, '')
    
    
class ArbSeqDepth(object):
    "Extension IVI methods for function generators that support producing sequences of sequences of waveforms"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviFgenArbSeqDepth')
        
        self._arbitrary_sequence_depth_max = 1
        
        self.__dict__.setdefault('arbitrary', ivi.PropertyCollection())
        self.arbitrary.__dict__.setdefault('sequence', ivi.PropertyCollection())
        self.arbitrary.sequence._add_property('depth_max',
                        self._get_arbitrary_sequence_depth_max)
    
    def _get_arbitrary_sequence_depth_max(self):
        return self._arbitrary_sequence_depth_max
    
    

