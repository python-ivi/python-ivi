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
        super().__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviFgenBase')
        
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
        if state not in OperationMode:
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
        if state not in OutputMode:
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
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviFgenStdFunc')
        
        self._output_standard_waveform_amplitude = list()
        self._output_standard_waveform_dc_offset = list()
        self._output_standard_waveform_duty_cycle_high = list()
        self._output_standard_waveform_frequency = list()
        self._output_standard_waveform_start_phase = list()
        self._output_standard_waveform_waveform_function = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_sub_property('standard_waveform', 'amplitude',
                        self._get_output_standard_waveform_amplitude,
                        self._set_output_standard_waveform_amplitude)
        self.outputs._add_sub_property('standard_waveform', 'dc_offset',
                        self._get_output_standard_waveform_dc_offset,
                        self._set_output_standard_waveform_dc_offset)
        self.outputs._add_sub_property('standard_waveform', 'duty_cycle_high',
                        self._get_output_standard_waveform_duty_cycle_high,
                        self._set_output_standard_waveform_duty_cycle_high)
        self.outputs._add_sub_property('standard_waveform', 'start_phase',
                        self._get_output_standard_waveform_start_phase,
                        self._set_output_standard_waveform_start_phase)
        self.outputs._add_sub_property('standard_waveform', 'frequency',
                        self._get_output_standard_waveform_frequency,
                        self._set_output_standard_waveform_frequency)
        self.outputs._add_sub_property('standard_waveform', 'waveform_function',
                        self._get_output_standard_waveform_waveform_function,
                        self._set_output_standard_waveform_waveform_function)
        self.outputs._add_sub_method('standard_waveform', 'configure',
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
        if state not in StandardWaveform:
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
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviFgenArbWfm')
        
        self._output_arbitrary_gain = list()
        self._output_arbitrary_offset = list()
        self._output_arbitrary_waveform = list()
        self._arbitrary_sample_rate = list()
        self._arbitrary_waveform_number_waveforms_max = list()
        self._arbitrary_waveform_size_max = list()
        self._arbitrary_waveform_size_min = list()
        self._arbitrary_waveform_quantum = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_sub_property('arbitrary', 'gain',
                        self._get_output_arbitrary_gain,
                        self._set_output_arbitrary_gain)
        self.outputs._add_sub_property('arbitrary', 'offset',
                        self._get_output_arbitrary_offset,
                        self._set_output_arbitrary_offset)
        self.outputs._add_sub_property('arbitrary', 'waveform',
                        self._get_output_arbitrary_waveform,
                        self._set_output_arbitrary_waveform)
        self.outputs._add_sub_method('arbitrary', 'configure',
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
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviFgenArbFrequency')
        
        self._output_arbitrary_frequency = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_sub_property('arbitrary', 'frequency',
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
    
    
    

