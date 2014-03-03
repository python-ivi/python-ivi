"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

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
        
        super(Base, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_name = list()
        self._output_operation_mode = list()
        self._output_enabled = list()
        self._output_impedance = list()
        self._output_mode = list()
        self._output_reference_clock_source = list()
        self._output_count = 1
        
        ivi.add_property(self, 'outputs[].name',
                        self._get_output_name,
                        None,
                        None,
                        """
                        This property returns the physical name defined by the specific driver for
                        the output channel that corresponds to the 0-based index that the user
                        specifies. If the driver defines a qualified channel name, this property
                        returns the qualified name. If the value that the user passes for the
                        Index parameter is less than zero or greater than the value of Output
                        Count, the property returns an empty string and returns an error.
                        """)
        ivi.add_property(self, 'outputs[].operation_mode',
                        self._get_output_operation_mode,
                        self._set_output_operation_mode,
                        None,
                        """
                        Specifies how the function generator produces output on a channel.
                        
                        Values for operation_mode:
                        
                        * 'continuous'
                        * 'burst'
                        """)
        ivi.add_property(self, 'outputs[].enabled',
                        self._get_output_enabled,
                        self._set_output_enabled,
                        None,
                        """
                        If set to True, the signal the function generator produces appears at the
                        output connector. If set to False, the signal the function generator
                        produces does not appear at the output connector.
                        """)
        ivi.add_property(self, 'outputs[].impedance',
                        self._get_output_impedance,
                        self._set_output_impedance,
                        None,
                        """
                        Specifies the impedance of the output channel. The units are Ohms.
                        """)
        ivi.add_property(self, 'outputs[].output_mode',
                        self._get_output_mode,
                        self._set_output_mode,
                        None,
                        """
                        Determines how the function generator produces waveforms. This attribute
                        determines which extension group's functions and attributes are used to
                        configure the waveform the function generator produces.
                        
                        Values for output_mode:
                        
                        * 'function'
                        * 'arbitrary'
                        * 'sequence'
                        """)
        ivi.add_property(self, 'outputs[].reference_clock_source',
                        self._get_output_reference_clock_source,
                        self._set_output_reference_clock_source,
                        None,
                        """
                        Specifies the source of the reference clock. The function generator
                        derives frequencies and sample rates that it uses to generate waveforms
                        from the reference clock.
                        
                        The source of the reference clock is a string. If an IVI driver supports a
                        reference clock source and the reference clock source is listed in IVI-3.3
                        Cross Class Capabilities Specification, Section 3, then the IVI driver
                        shall accept the standard string for that reference clock. This attribute
                        is case insensitive, but case preserving. That is, the setting is case
                        insensitive but when reading it back the programmed case is returned. IVI
                        specific drivers may define new reference clock source strings for
                        reference clock sources that are not defined by IVI-3.3 Cross Class
                        Capabilities Specification if needed.
                        """)
        
        self.__dict__.setdefault('_docs', dict())
        self._docs['abort_generation'] = """
                        Aborts a previously initiated signal generation. If the function generator
                        is in the Output Generation State, this function moves the function
                        generator to the Configuration State. If the function generator is already
                        in the Configuration State, the function does nothing and returns Success.
                        
                        This specification requires that the user be able to configure the output
                        of the function generator regardless of whether the function generator is
                        in the Configuration State or the Generation State. This means that the
                        user is not required to call Abort Generation prior to configuring the
                        output of the function generator.
                        
                        Many function generators constantly generate an output signal, and do not
                        require the user to abort signal generation prior to configuring the
                        instrument. If a function generator's output cannot be aborted (i.e., the
                        function generator cannot stop generating a signal) this function does
                        nothing and returns Success.
                        
                        Some function generators require that the user abort signal generation
                        prior to configuring the instrument. The specific drivers for these types
                        of instruments must compensate for this restriction and allow the user to
                        configure the instrument without requiring the user to call Abort
                        Generation. For these types of instruments, there is often a significant
                        performance increase if the user configures the output while the
                        instrument is not generating a signal.
                        
                        The user is not required to call Abort Generation or Initiate Generation.
                        Whether the user chooses to call these functions in an application
                        program has no impact on interchangeability. The user can choose to use
                        these functions if they want to optimize their application for instruments
                        that exhibit increased performance when output configuration is performed
                        while the instrument is not generating a signal.
                        """
        self._docs['initiate_generation'] = """
                        Initiates signal generation. If the function generator is in the
                        Configuration State, this function moves the function generator to the
                        Output Generation State. If the function generator is already in the
                        Output Generation State, this function does nothing and returns Success.
                        
                        This specification requires that the instrument be in the Generation State
                        after the user calls the Initialize or Reset functions. This specification
                        also requires that the user be able to configure the output of the
                        function generator regardless of whether the function generator is in the
                        Configuration State or the Generation State. This means that the user is
                        only required to call Initiate Generation if they abort signal generation
                        by calling Abort Generation.
                        
                        Many function generators constantly generate an output signal, and do not
                        require the user to abort signal generation prior to configuring the
                        instrument. If a function generator's output cannot be aborted (i.e., the
                        function generator cannot stop generating a signal) this function does
                        nothing and returns Success.
                        
                        Some function generators require that the user abort signal generation
                        prior to configuring the instrument. The specific drivers for these types
                        of instruments must compensate for this restriction and allow the user to
                        configure the instrument without requiring the user to call Abort
                        Generation. For these types of instruments, there is often a significant
                        performance increase if the user configures the output while the
                        instrument is not generating a signal.
                        
                        The user is not required to call Abort Generation or Initiate Generation.
                        Whether the user chooses to call these functions in an application
                        program has no impact on interchangeability. The user can choose to use
                        these functions if they want to optimize their application for instruments
                        that exhibit increased performance when output configuration is performed
                        while the instrument is not generating a signal.
                        """
        
        self._init_outputs()
    
    def _init_outputs(self):
        try:
            super(Base, self)._init_outputs()
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
        super(StdFunc, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'StdFunc'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_standard_waveform_amplitude = list()
        self._output_standard_waveform_dc_offset = list()
        self._output_standard_waveform_duty_cycle_high = list()
        self._output_standard_waveform_frequency = list()
        self._output_standard_waveform_start_phase = list()
        self._output_standard_waveform_waveform = list()
        
        ivi.add_property(self, 'outputs[].standard_waveform.amplitude',
                        self._get_output_standard_waveform_amplitude,
                        self._set_output_standard_waveform_amplitude,
                        None,
                        """
                        Specifies the amplitude of the standard waveform the function generator
                        produces. When the Waveform attribute is set to Waveform DC, this
                        attribute does not affect signal output. The units are volts.
                        """)
        ivi.add_property(self, 'outputs[].standard_waveform.dc_offset',
                        self._get_output_standard_waveform_dc_offset,
                        self._set_output_standard_waveform_dc_offset,
                        None,
                        """
                        Specifies the DC offset of the standard waveform the function generator
                        produces. If the Waveform attribute is set to Waveform DC, this attribute
                        specifies the DC level the function generator produces. The units are
                        volts.
                        """)
        ivi.add_property(self, 'outputs[].standard_waveform.duty_cycle_high',
                        self._get_output_standard_waveform_duty_cycle_high,
                        self._set_output_standard_waveform_duty_cycle_high,
                        None,
                        """
                        Specifies the duty cycle for a square waveform. This attribute affects
                        function generator behavior only when the Waveform attribute is set to
                        Waveform Square. The value is expressed as a percentage.
                        """)
        ivi.add_property(self, 'outputs[].standard_waveform.start_phase',
                        self._get_output_standard_waveform_start_phase,
                        self._set_output_standard_waveform_start_phase,
                        None,
                        """
                        Specifies the start phase of the standard waveform the function generator
                        produces. When the Waveform attribute is set to Waveform DC, this
                        attribute does not affect signal output. The units are degrees.
                        """)
        ivi.add_property(self, 'outputs[].standard_waveform.frequency',
                        self._get_output_standard_waveform_frequency,
                        self._set_output_standard_waveform_frequency,
                        None,
                        """
                        Specifies the frequency of the standard waveform the function generator
                        produces. When the Waveform attribute is set to Waveform DC, this
                        attribute does not affect signal output. The units are Hertz.
                        """)
        ivi.add_property(self, 'outputs[].standard_waveform.waveform',
                        self._get_output_standard_waveform_waveform,
                        self._set_output_standard_waveform_waveform,
                        None,
                        """
                        Specifies which standard waveform the function generator produces.
                        
                        Values for waveform:
                        
                        * 'sine'
                        * 'square'
                        * 'triangle'
                        * 'ramp_up'
                        * 'ramp_down'
                        * 'dc'
                        """)
        ivi.add_method(self, 'outputs[].standard_waveform.configure',
                        self._output_standard_waveform_configure,
                        """
                        This function configures the attributes of the function generator that
                        affect standard waveform generation. These attributes are the Waveform,
                        Amplitude, DC Offset, Frequency, and Start Phase.
                        
                        When the Waveform parameter is set to Waveform DC, this function ignores
                        the Amplitude, Frequency, and Start Phase parameters and does not set the
                        Amplitude, Frequency, and Start Phase attributes.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(StdFunc, self)._init_outputs()
        except AttributeError:
            pass
        
        self._output_standard_waveform_amplitude = list()
        self._output_standard_waveform_dc_offset = list()
        self._output_standard_waveform_duty_cycle_high = list()
        self._output_standard_waveform_frequency = list()
        self._output_standard_waveform_start_phase = list()
        self._output_standard_waveform_waveform = list()
        for i in range(self._output_count):
            self._output_standard_waveform_amplitude.append(0)
            self._output_standard_waveform_dc_offset.append(0)
            self._output_standard_waveform_duty_cycle_high.append(0)
            self._output_standard_waveform_frequency.append(0)
            self._output_standard_waveform_start_phase.append(0)
            self._output_standard_waveform_waveform.append('sine')
        
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
    
    def _get_output_standard_waveform_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_waveform[index]
    
    def _set_output_standard_waveform_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in StandardWaveform:
            raise ivi.ValueNotSupportedException()
        self._output_standard_waveform_waveform[index] = value
    
    def _output_standard_waveform_configure(self, index, function, amplitude, dc_offset, frequency, start_phase):
        self._set_output_standard_waveform_waveform(index, function)
        self._set_output_standard_waveform_dc_offset(index, dc_offset)
        if function != 'dc':
            self._set_output_standard_waveform_amplitude(index, amplitude)
            self._set_output_standard_waveform_frequency(index, frequency)
            self._set_output_standard_waveform_start_phase(index, start_phase)
    
    
class ArbWfm(object):
    "Extension IVI methods for function generators that can produce arbitrary waveforms"
    
    def __init__(self, *args, **kwargs):
        super(ArbWfm, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ArbWfm'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_arbitrary_gain = list()
        self._output_arbitrary_offset = list()
        self._output_arbitrary_waveform = list()
        self._arbitrary_sample_rate = 0
        self._arbitrary_waveform_number_waveforms_max = 0
        self._arbitrary_waveform_size_max = 0
        self._arbitrary_waveform_size_min = 0
        self._arbitrary_waveform_quantum = 0
        
        ivi.add_property(self, 'outputs[].arbitrary.gain',
                        self._get_output_arbitrary_gain,
                        self._set_output_arbitrary_gain,
                        None,
                        """
                        Specifies the gain of the arbitrary waveform the function generator
                        produces. This value is unitless.
                        """)
        ivi.add_property(self, 'outputs[].arbitrary.offset',
                        self._get_output_arbitrary_offset,
                        self._set_output_arbitrary_offset,
                        None,
                        """
                        Specifies the offset of the arbitrary waveform the function generator
                        produces. The units are volts.
                        """)
        ivi.add_property(self, 'outputs[].arbitrary.waveform',
                        self._get_output_arbitrary_waveform,
                        self._set_output_arbitrary_waveform,
                        None,
                        """
                        """)
        ivi.add_method(self, 'outputs[].arbitrary.configure',
                        self._arbitrary_waveform_configure,
                        """
                        Configures the attributes of the function generator that affect arbitrary
                        waveform generation. These attributes are the arbitrary waveform handle,
                        gain, and offset.
                        """)
        ivi.add_property(self, 'arbitrary.sample_rate',
                        self._get_arbitrary_sample_rate,
                        self._set_arbitrary_sample_rate,
                        None,
                        """
                        Specifies the sample rate of the arbitrary waveforms the function
                        generator produces. The units are samples per second.
                        """)
        ivi.add_property(self, 'arbitrary.waveform.number_waveforms_max',
                        self._get_arbitrary_waveform_number_waveforms_max,
                        None,
                        None,
                        """
                        Returns the maximum number of arbitrary waveforms that the function
                        generator allows.
                        """)
        ivi.add_property(self, 'arbitrary.waveform.size_max',
                        self._get_arbitrary_waveform_size_max,
                        None,
                        None,
                        """
                        Returns the maximum number of points the function generator allows in an
                        arbitrary waveform.
                        """)
        ivi.add_property(self, 'arbitrary.waveform.size_min',
                        self._get_arbitrary_waveform_size_min,
                        None,
                        None,
                        """
                        Returns the minimum number of points the function generator allows in an
                        arbitrary waveform.
                        """)
        ivi.add_property(self, 'arbitrary.waveform.quantum',
                        self._get_arbitrary_waveform_quantum,
                        None,
                        None,
                        """
                        The size of each arbitrary waveform shall be a multiple of a quantum
                        value. This attribute returns the quantum value the function generator
                        allows. For example, if this attribute returns a value of 8, all waveform
                        sizes must be a multiple of 8.
                        """)
        ivi.add_method(self, 'arbitrary.waveform.configure',
                        self._arbitrary_waveform_configure,
                        """
                        Configures the attributes of the function generator that affect arbitrary
                        waveform generation. These attributes are the arbitrary waveform handle,
                        gain, and offset.
                        """)
        ivi.add_method(self, 'arbitrary.waveform.clear',
                        self._arbitrary_waveform_clear,
                        """
                        Removes a previously created arbitrary waveform from the function
                        generator's memory and invalidates the waveform's handle.
                        
                        If the waveform cannot be cleared because it is currently being generated,
                        or it is specified as part of an existing arbitrary waveform sequence,
                        this function returns the Waveform In Use error.
                        """)
        ivi.add_method(self, 'arbitrary.waveform.create',
                        self._arbitrary_waveform_create,
                        """
                        Creates an arbitrary waveform from an array of data points. The function
                        returns a handlethat identifies the waveform. You pass a waveform handle
                        to the Handle parameter of the Configure Arbitrary Waveform function to
                        produce that waveform.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(ArbWfm, self)._init_outputs()
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
        super(ArbFrequency, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ArbFrequency'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_arbitrary_frequency = list()
        
        ivi.add_property(self, 'outputs[].arbitrary.frequency',
                        self._get_output_arbitrary_frequency,
                        self._set_output_arbitrary_frequency,
                        None,
                        """
                        Specifies the rate in Hertz at which an entire arbitrary waveform is
                        generated.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(ArbFrequency, self)._init_outputs()
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
        super(ArbSeq, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ArbSeq'
        ivi.add_group_capability(self, cls+grp)
        
        self._arbitrary_sequence_number_sequences_max = 0
        self._arbitrary_sequence_loop_count_max = 0
        self._arbitrary_sequence_length_max = 0
        self._arbitrary_sequence_length_min = 0
        
        ivi.add_property(self, 'arbitrary.sequence.number_sequences_max',
                        self._get_arbitrary_sequence_number_sequences_max,
                        None,
                        None,
                        """
                        Returns the maximum number of arbitrary sequences that the function
                        generator allows.
                        """)
        ivi.add_property(self, 'arbitrary.sequence.loop_count_max',
                        self._get_arbitrary_sequence_loop_count_max,
                        None,
                        None,
                        """
                        Returns the maximum number of times that the function generator can repeat
                        a waveform in a sequence.
                        """)
        ivi.add_property(self, 'arbitrary.sequence.length_max',
                        self._get_arbitrary_sequence_length_max,
                        None,
                        None,
                        """
                        Returns the maximum number of arbitrary waveforms that the function
                        generator allows in an arbitrary sequence.
                        """)
        ivi.add_property(self, 'arbitrary.sequence.length_min',
                        self._get_arbitrary_sequence_length_min,
                        None,
                        None,
                        """
                        Returns the minimum number of arbitrary waveforms that the function
                        generator allows in an arbitrary sequence.
                        """)
        ivi.add_method(self, 'arbitrary.clear_memory',
                        self._arbitrary_clear_memory,
                        """
                        Removes all previously created arbitrary waveforms and sequences from the
                        function generator's memory and invalidates all waveform and sequence
                        handles.
                        
                        If a waveform cannot be cleared because it is currently being generated,
                        this function returns the error Waveform In Use.
                        
                        If a sequence cannot be cleared because it is currently being generated,
                        this function returns the error Sequence In Use.
                        """)
        ivi.add_method(self, 'arbitrary.sequence.clear',
                        self._arbitrary_sequence_clear,
                        """
                        Removes a previously created arbitrary sequence from the function
                        generator's memory and invalidates the sequence's handle.
                        
                        If the sequence cannot be cleared because it is currently being generated,
                        this function returns the error Sequence In Use.
                        """)
        ivi.add_method(self, 'arbitrary.sequence.configure',
                        self._arbitrary_sequence_configure,
                        """
                        Configures the attributes of the function generator that affect arbitrary
                        sequence generation. These attributes are the arbitrary sequence handle,
                        gain, and offset.
                        """)
        ivi.add_method(self, 'arbitrary.sequence.create',
                        self._arbitrary_sequence_create,
                        """
                        Creates an arbitrary waveform sequence from an array of waveform handles
                        and a corresponding array of loop counts. The function returns a handle
                        that identifies the sequence. You pass a sequence handle to the Handle
                        parameter of the Configure Arbitrary Sequence function to produce that
                        sequence.
                        
                        If the function generator cannot store any more arbitrary sequences, this
                        function returns the error No Sequences Available.
                        """)
        ivi.add_method(self, 'outputs[].arbitrary.sequence.configure',
                        self._arbitrary_sequence_configure,
                        """
                        Configures the attributes of the function generator that affect arbitrary
                        sequence generation. These attributes are the arbitrary sequence handle,
                        gain, and offset.
                        """)
    
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
        super(Trigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'Trigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_trigger_source = list()
        
        ivi.add_property(self, 'outputs[].trigger.source',
                        self._get_output_trigger_source,
                        self._set_output_trigger_source,
                        None,
                        """
                        Specifies the trigger source. After the function generator receives a
                        trigger from this source, it produces a signal.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(Trigger, self)._init_outputs()
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
        super(StartTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'StartTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_start_trigger_delay = list()
        self._output_start_trigger_slope = list()
        self._output_start_trigger_source = list()
        self._output_start_trigger_threshold = list()
        
        ivi.add_property(self, 'outputs[].trigger.start.delay',
                        self._get_output_start_trigger_delay,
                        self._set_output_start_trigger_delay,
                        None,
                        """
                        Specifies an additional length of time to delay from the start trigger to
                        the first point in the waveform generation. The units are seconds.  
                        """)
        ivi.add_property(self, 'outputs[].trigger.start.slope',
                        self._get_output_start_trigger_slope,
                        self._set_output_start_trigger_slope,
                        None,
                        """
                        Specifies the slope of the trigger that starts the generator.
                        
                        Values for slope:
                        
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """)
        ivi.add_property(self, 'outputs[].trigger.start.source',
                        self._get_output_start_trigger_source,
                        self._set_output_start_trigger_source,
                        None,
                        """
                        Specifies the source of the start trigger.
                        """)
        ivi.add_property(self, 'outputs[].trigger.start.threshold',
                        self._get_output_start_trigger_threshold,
                        self._set_output_start_trigger_threshold,
                        None,
                        """
                        Specifies the voltage threshold for the start trigger. The units are
                        volts.
                        """)
        ivi.add_method(self, 'outputs[].trigger.start.configure',
                        self._output_start_trigger_configure,
                        """
                        This function configures the start trigger properties.
                        """)
        ivi.add_method(self, 'trigger.start.configure',
                        self._output_start_trigger_configure,
                        """
                        This function configures the start trigger properties.
                        """)
        ivi.add_method(self, 'trigger.start.send_software_trigger',
                        self._start_trigger_send_software_trigger,
                        """
                        This function sends a software-generated start trigger to the instrument.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(StartTrigger, self)._init_outputs()
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
        super(StopTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'StopTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_stop_trigger_delay = list()
        self._output_stop_trigger_slope = list()
        self._output_stop_trigger_source = list()
        self._output_stop_trigger_threshold = list()
        
        ivi.add_property(self, 'outputs[].trigger.stop.delay',
                        self._get_output_stop_trigger_delay,
                        self._set_output_stop_trigger_delay,
                        None,
                        """
                        Specifies an additional length of time to delay from the stop trigger to
                        the termination of the generation. The units are seconds.
                        """)
        ivi.add_property(self, 'outputs[].trigger.stop.slope',
                        self._get_output_stop_trigger_slope,
                        self._set_output_stop_trigger_slope,
                        None,
                        """
                        Specifies the slope of the stop trigger.
                        
                        Values for slope:
                        
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """)
        ivi.add_property(self, 'outputs[].trigger.stop.source',
                        self._get_output_stop_trigger_source,
                        self._set_output_stop_trigger_source,
                        None,
                        """
                        Specifies the source of the stop trigger.
                        """)
        ivi.add_property(self, 'outputs[].trigger.stop.threshold',
                        self._get_output_stop_trigger_threshold,
                        self._set_output_stop_trigger_threshold,
                        None,
                        """
                        Specifies the voltage threshold for the stop trigger. The units are volts.
                        """)
        ivi.add_method(self, 'outputs[].trigger.stop.configure',
                        self._output_stop_trigger_configure,
                        None,
                        """
                        This function configures the stop trigger properties.
                        """)
        ivi.add_method(self, 'trigger.stop.configure',
                        self._output_stop_trigger_configure,
                        """
                        This function configures the stop trigger properties.
                        """)
        ivi.add_method(self, 'trigger.stop.send_software_trigger',
                        self._stop_trigger_send_software_trigger,
                        """
                        This function sends a software-generated stop trigger to the instrument.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(StopTrigger, self)._init_outputs()
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
        super(HoldTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'HoldTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_hold_trigger_delay = list()
        self._output_hold_trigger_slope = list()
        self._output_hold_trigger_source = list()
        self._output_hold_trigger_threshold = list()
        
        ivi.add_property(self, 'outputs[].trigger.hold.delay',
                        self._get_output_hold_trigger_delay,
                        self._set_output_hold_trigger_delay,
                        None,
                        """
                        Specifies an additional length of time to delay from the hold trigger to
                        the pause of the generation. The units are seconds.
                        """)
        ivi.add_property(self, 'outputs[].trigger.hold.slope',
                        self._get_output_hold_trigger_slope,
                        self._set_output_hold_trigger_slope,
                        None,
                        """
                        Specifies the slope of the hold trigger.
                        
                        Values for slope:
                        
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """)
        ivi.add_property(self, 'outputs[].trigger.hold.source',
                        self._get_output_hold_trigger_source,
                        self._set_output_hold_trigger_source,
                        None,
                        """
                        Specifies the source of the hold trigger.
                        """)
        ivi.add_property(self, 'outputs[].trigger.hold.threshold',
                        self._get_output_hold_trigger_threshold,
                        self._set_output_hold_trigger_threshold,
                        None,
                        """
                        Specifies the voltage threshold for the hold trigger. The units are volts.
                        """)
        ivi.add_method(self, 'outputs[].trigger.hold.configure',
                        self._output_hold_trigger_configure,
                        """
                        This function configures the hold trigger properties.
                        """)
        ivi.add_method(self, 'trigger.hold.configure',
                        self._output_hold_trigger_configure,
                        """
                        This function configures the hold trigger properties.
                        """)
        ivi.add_method(self, 'trigger.hold.send_software_trigger',
                        self._hold_trigger_send_software_trigger,
                        """
                        This function sends a software-generated hold trigger to the instrument.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(HoldTrigger, self)._init_outputs()
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
        super(ResumeTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ResumeTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_resume_trigger_delay = list()
        self._output_resume_trigger_slope = list()
        self._output_resume_trigger_source = list()
        self._output_resume_trigger_threshold = list()
        
        ivi.add_property(self, 'outputs[].trigger.resume.delay',
                        self._get_output_resume_trigger_delay,
                        self._set_output_resume_trigger_delay,
                        None,
                        """
                        Specifies an additional length of time to delay from the resume trigger to
                        the resumption of the generation. The units are seconds.
                        """)
        ivi.add_property(self, 'outputs[].trigger.resume.slope',
                        self._get_output_resume_trigger_slope,
                        self._set_output_resume_trigger_slope,
                        None,
                        """
                        Specifies the slope of the resume trigger.
                        
                        Values for slope:
                        
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """)
        ivi.add_property(self, 'outputs[].trigger.resume.source',
                        self._get_output_resume_trigger_source,
                        self._set_output_resume_trigger_source,
                        None,
                        """
                        Specifies the source of the resume trigger.
                        """)
        ivi.add_property(self, 'outputs[].trigger.resume.threshold',
                        self._get_output_resume_trigger_threshold,
                        self._set_output_resume_trigger_threshold,
                        None,
                        """
                        Specifies the voltage threshold for the resume trigger. The units are
                        volts.
                        """)
        ivi.add_method(self, 'outputs[].trigger.resume.configure',
                        self._output_resume_trigger_configure,
                        """
                        This function configures the resume trigger properties.
                        """)
        ivi.add_method(self, 'trigger.resume.configure',
                        self._output_resume_trigger_configure,
                        """
                        This function configures the resume trigger properties.
                        """)
        ivi.add_method(self, 'trigger.resume.send_software_trigger',
                        self._resume_trigger_send_software_trigger,
                        """
                        This function sends a software-generated resume trigger to the instrument.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(ResumeTrigger, self)._init_outputs()
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
        super(AdvanceTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'AdvanceTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_advance_trigger_delay = list()
        self._output_advance_trigger_slope = list()
        self._output_advance_trigger_source = list()
        self._output_advance_trigger_threshold = list()
        
        ivi.add_property(self, 'outputs[].trigger.advance.delay',
                        self._get_output_advance_trigger_delay,
                        self._set_output_advance_trigger_delay,
                        None,
                        """
                        Specifies an additional length of time to delay from the advance trigger
                        to the advancing to the end of the current waveform. Units are seconds.
                        """)
        ivi.add_property(self, 'outputs[].trigger.advance.slope',
                        self._get_output_advance_trigger_slope,
                        self._set_output_advance_trigger_slope,
                        None,
                        """
                        Specifies the slope of the advance trigger.
                        
                        Values for slope:
                        
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """)
        ivi.add_property(self, 'outputs[].trigger.advance.source',
                        self._get_output_advance_trigger_source,
                        self._set_output_advance_trigger_source,
                        None,
                        """
                        Specifies the source of the advance trigger.
                        """)
        ivi.add_property(self, 'outputs[].trigger.advance.threshold',
                        self._get_output_advance_trigger_threshold,
                        self._set_output_advance_trigger_threshold,
                        None,
                        """
                        Specifies the voltage threshold for the advance trigger. The units are
                        volts.
                        """)
        ivi.add_method(self, 'outputs[].trigger.advance.configure',
                        self._output_advance_trigger_configure,
                        """
                        This function configures the advance trigger properties.
                        """)
        ivi.add_method(self, 'trigger.advance.configure',
                        self._output_advance_trigger_configure,
                        """
                        This function configures the advance trigger properties.
                        """)
        ivi.add_method(self, 'trigger.advance.send_software_trigger',
                        self._advance_trigger_send_software_trigger,
                        """
                        This function sends a software-generated advance trigger to the
                        instrument.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(AdvanceTrigger, self)._init_outputs()
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
        super(InternalTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'InternalTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._internal_trigger_rate = 0
        
        ivi.add_property(self, 'trigger.internal_rate',
                        self._get_internal_trigger_rate,
                        self._set_internal_trigger_rate,
                        None,
                        """
                        Specifies the rate at which the function generator's internal trigger
                        source produces a trigger, in triggers per second.
                        """)
    
    def _get_internal_trigger_rate(self):
        return self._internal_trigger_rate
    
    def _set_internal_trigger_rate(self, value):
        value = float(value)
        self._internal_trigger_rate = value
    
    
class SoftwareTrigger(object):
    "Extension IVI methods for function generators that support software triggering"
    
    def __init__(self, *args, **kwargs):
        super(SoftwareTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'SoftwareTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self.__dict__.setdefault('_docs', dict())
        self._docs['send_software_trigger'] = """
                        This function sends a software-generated trigger to the instrument. It is
                        only applicable for instruments using interfaces or protocols which
                        support an explicit trigger function. For example, with GPIB this function
                        could send a group execute trigger to the instrument. Other
                        implementations might send a ``*TRG`` command.
                        
                        Since instruments interpret a software-generated trigger in a wide variety
                        of ways, the precise response of the instrument to this trigger is not
                        defined. Note that SCPI details a possible implementation.
                        
                        This function should not use resources which are potentially shared by
                        other devices (for example, the VXI trigger lines). Use of such shared
                        resources may have undesirable effects on other devices.
                        
                        This function should not check the instrument status. Typically, the
                        end-user calls this function only in a sequence of calls to other
                        low-level driver functions. The sequence performs one operation. The
                        end-user uses the low-level functions to optimize one or more aspects of
                        interaction with the instrument. To check the instrument status, call the
                        appropriate error query function at the conclusion of the sequence.
                        
                        The trigger source attribute must accept Software Trigger as a valid
                        setting for this function to work. If the trigger source is not set to
                        Software Trigger, this function does nothing and returns the error Trigger
                        Not Software.
                        """
    
    def send_software_trigger(self):
        pass
    
    
class Burst(object):
    "Extension IVI methods for function generators that support triggered burst output"
    
    def __init__(self, *args, **kwargs):
        super(Burst, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'Burst'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_burst_count = list()
        
        ivi.add_property(self, 'outputs[].burst_count',
                        self._get_output_burst_count,
                        self._set_output_burst_count,
                        None,
                        """
                        Specifies the number of waveform cycles that the function generator
                        produces after it receives a trigger.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(Burst, self)._init_outputs()
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
        super(ModulateAM, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ModulateAM'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_am_enabled = list()
        self._am_internal_depth = 0
        self._am_internal_frequency = 0
        self._am_internal_waveform = 0
        self._output_am_source = list()
        
        ivi.add_property(self, 'outputs[].am.enabled',
                        self._get_output_am_enabled,
                        self._set_output_am_enabled,
                        None,
                        """
                        Specifies whether the function generator applies amplitude modulation to
                        the signal that the function generator produces with the IviFgenStdFunc,
                        IviFgenArbWfm, or IviFgenArbSeq capability groups. If set to True, the
                        function generator applies amplitude modulation to the output signal. If
                        set to False, the function generator does not apply amplitude modulation
                        to the output signal.
                        """)
        ivi.add_property(self, 'outputs[].am.source',
                        self._get_output_am_source,
                        self._set_output_am_source,
                        None,
                        """
                        Specifies the source of the signal that the function generator uses as the
                        modulating waveform.
                        
                        This attribute affects instrument behavior only when the AM Enabled
                        attribute is set to True.
                        """)
        ivi.add_property(self, 'am.internal_depth',
                        self._get_am_internal_depth,
                        self._set_am_internal_depth,
                        None,
                        """
                        Specifies the extent of modulation the function generator applies to the
                        carrier waveform when the AM Source attribute is set to AM Internal. The
                        unit is percentage.
                        
                        This attribute affects the behavior of the instrument only when the AM 
                        ource attribute is set to AM Internal.
                        """)
        ivi.add_property(self, 'am.internal_frequency',
                        self._get_am_internal_frequency,
                        self._set_am_internal_frequency,
                        None,
                        """
                        Specifies the frequency of the internal modulating waveform source. The
                        units are Hertz.
                        
                        This attribute affects the behavior of the instrument only when the AM 
                        ource attribute is set to AM Internal.
                        """)
        ivi.add_property(self, 'am.internal_waveform',
                        self._get_am_internal_waveform,
                        self._set_am_internal_waveform,
                        None,
                        """
                        Specifies the waveform of the internal modulating waveform source.
                        
                        This attribute affects the behavior of the instrument only when the AM 
                        ource attribute is set to AM Internal.
                        
                        Values for internal_waveform:
                        
                        * 'sine'
                        * 'square'
                        * 'triangle'
                        * 'ramp_up'
                        * 'ramp_down'
                        * 'dc'
                        """)
        ivi.add_method(self, 'am.configure_internal',
                        self._am_configure_internal,
                        """
                        Configures the attributes that control the function generator's internal
                        amplitude modulating waveform source. These attributes are the modulation
                        depth, waveform, and frequency.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(ModulateAM, self)._init_outputs()
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
    
    def _get_am_internal_waveform(self):
        return self._am_internal_waveform
    
    def _set_am_internal_waveform(self, value):
        value = float(value)
        self._am_internal_waveform = value
    
    def _am_configure_internal(self, depth, waveform, frequency):
        self._set_am_internal_depth(depth)
        self._set_am_internal_waveform(waveform)
        self._set_am_internal_frequency(frequency)
    
    
class ModulateFM(object):
    "Extension IVI methods for function generators that support frequency modulation"
    
    def __init__(self, *args, **kwargs):
        super(ModulateFM, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ModulateFM'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_fm_enabled = list()
        self._fm_internal_deviation = 0
        self._fm_internal_frequency = 0
        self._fm_internal_waveform = 0
        self._output_fm_source = list()
        
        ivi.add_property(self, 'outputs[].fm.enabled',
                        self._get_output_fm_enabled,
                        self._set_output_fm_enabled,
                        None,
                        """
                        Specifies whether the function generator applies amplitude modulation to
                        the carrier waveform. If set to True, the function generator applies
                        frequency modulation to the output signal. If set to False, the function
                        generator does not apply frequency modulation to the output signal.
                        """)
        ivi.add_property(self, 'outputs[].fm.source',
                        self._get_output_fm_source,
                        self._set_output_fm_source,
                        None,
                        """
                        """)
        ivi.add_property(self, 'fm.internal_deviation',
                        self._get_fm_internal_deviation,
                        self._set_fm_internal_deviation,
                        None,
                        """
                        Specifies the maximum frequency deviation, in Hertz, that the function
                        generator applies to the carrier waveform when the FM Source attribute is
                        set to FM Internal.
                        
                        This attribute affects the behavior of the instrument only when the FM
                        Source attribute is set to FM Internal.
                        """)
        ivi.add_property(self, 'fm.internal_frequency',
                        self._get_fm_internal_frequency,
                        self._set_fm_internal_frequency,
                        None,
                        """
                        Specifies the frequency of the internal modulating waveform source. The
                        units are hertz.
                        
                        This attribute affects the behavior of the instrument only when the FM
                        Source attribute is set to FM Internal.
                        """)
        ivi.add_property(self, 'fm.internal_waveform',
                        self._get_fm_internal_waveform,
                        self._set_fm_internal_waveform,
                        None,
                        """
                        Specifies the waveform of the internal modulating waveform source.
                        
                        This attribute affects the behavior of the instrument only when the FM
                        Source attribute is set to FM Internal.
                        
                        Values for internal_waveform:
                        
                        * 'sine'
                        * 'square'
                        * 'triangle'
                        * 'ramp_up'
                        * 'ramp_down'
                        * 'dc'
                        """)
        ivi.add_method(self, 'fm.configure_internal',
                        self._fm_configure_internal,
                        """
                        Specifies the source of the signal that the function generator uses as the
                        modulating waveform.
                        
                        This attribute affects instrument behavior only when the FM Enabled
                        attribute is set to True.
                        """)
        
    
    def _init_outputs(self):
        try:
            super(ModulateFM, self)._init_outputs()
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
    
    def _get_fm_internal_waveform(self):
        return self._fm_internal_waveform
    
    def _set_fm_internal_waveform(self, value):
        value = float(value)
        self._fm_internal_waveform = value
    
    def _fm_configure_internal(self, deviation, waveform, frequency):
        self._set_fm_internal_deviation(deviation)
        self._set_fm_internal_waveform(waveform)
        self._set_fm_internal_frequency(frequency)
    
    
class SampleClock(object):
    "Extension IVI methods for function generators that support external sample clocks"
    
    def __init__(self, *args, **kwargs):
        super(SampleClock, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'SampleClock'
        ivi.add_group_capability(self, cls+grp)
        
        self._sample_clock_source = 'internal'
        self._sample_clock_output_enabled = ''
        
        ivi.add_property(self, 'sample_clock.source',
                        self._get_sample_clock_source,
                        self._set_sample_clock_source,
                        None,
                        """
                        Specifies the clock used for the waveform generation. Note that when using
                        an external sample clock, the Arbitrary Sample Rate attribute must be set
                        to the corresponding frequency of the external sample clock.
                        """)
        ivi.add_property(self, 'sample_clock.output_enabled',
                        self._get_sample_clock_output_enabled,
                        self._set_sample_clock_output_enabled,
                        None,
                        """
                        Specifies whether or not the sample clock appears at the sample clock
                        output of the generator.
                        """)
        
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
        super(TerminalConfiguration, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'TerminalConfiguration'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_terminal_configuration = list()
        
        ivi.add_property(self, 'outputs[].terminal_configuration',
                        self._get_output_terminal_configuration,
                        self._set_output_terminal_configuration,
                        None,
                        """
                        Determines whether the generator will run in single-ended or differential
                        mode, and whether the output gain and offset values will be analyzed
                        based on single-ended or differential operation.
                        
                        Values for terminal_configuration:
                        
                        * 'single_ended'
                        * 'differential'
                        """)
        
    
    def _init_outputs(self):
        try:
            super(TerminalConfiguration, self)._init_outputs()
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
        super(ArbChannelWfm, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ArbChannelWfm'
        ivi.add_group_capability(self, cls+grp)
        
        ivi.add_method(self, 'outputs[].arbitrary.create_waveform',
                        self._arbitrary_waveform_create_channel_waveform,
                        """
                        Creates a channel-specific arbitrary waveform and returns a handle that
                        identifies that waveform. You pass a waveform handle as the waveformHandle
                        parameter of the Configure Arbitrary Waveform function to produce that
                        waveform. You also use the handles this function returns to create a
                        sequence of arbitrary waveforms with the Create Arbitrary Sequence
                        function.
                        
                        If the instrument has multiple channels, it is possible to create
                        multi-channel waveforms: the channel names are passed as a
                        comma-separated list of channel names, and the waveform arrays are
                        concatenated into a single array. In this case, all waveforms must be of
                        the same length.
                        
                        If the function generator cannot store any more arbitrary waveforms, this
                        function returns the error No Waveforms Available.
                        """)
        ivi.add_method(self, 'arbitrary.waveform.create_channel_waveform',
                        self._arbitrary_waveform_create_channel_waveform,
                        """
                        Creates a channel-specific arbitrary waveform and returns a handle that
                        identifies that waveform. You pass a waveform handle as the waveformHandle
                        parameter of the Configure Arbitrary Waveform function to produce that
                        waveform. You also use the handles this function returns to create a
                        sequence of arbitrary waveforms with the Create Arbitrary Sequence
                        function.
                        
                        If the instrument has multiple channels, it is possible to create
                        multi-channel waveforms: the channel names are passed as a
                        comma-separated list of channel names, and the waveform arrays are
                        concatenated into a single array. In this case, all waveforms must be of
                        the same length.
                        
                        If the function generator cannot store any more arbitrary waveforms, this
                        function returns the error No Waveforms Available.
                        """)
    
    def _arbitrary_waveform_create_channel_waveform(self, index, data):
        handle = self._arbitrary_waveform_create(data)
        self._set_output_arbitrary_waveform(index, handle)
        return handle
    
    
class ArbWfmBinary(object):
    "Extension IVI methods for function generators that support user-defined arbitrary binary waveform generation"
    
    def __init__(self, *args, **kwargs):
        super(ArbWfmBinary, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ArbWfmBinary'
        ivi.add_group_capability(self, cls+grp)
        
        self._arbitrary_binary_alignment = 'right'
        self._arbitrary_sample_bit_resolution = 16
        
        ivi.add_method(self, 'outputs[].arbitrary.waveform.create_channel_waveform_int16',
                        self._arbitrary_waveform_create_channel_waveform_int16,
                        """
                        Creates a channel-specific arbitrary waveform and returns a handle that
                        identifies that waveform. Data is passed in as 16-bit binary data. If the
                        arbitrary waveform generator supports formats less than 16 bits, call the
                        BinaryAlignment property to determine whether to left or right justify the
                        data before passing it to this call. You pass a waveform handle as the
                        waveformHandle parameter of the Configure Arbitrary Waveform function to
                        produce that waveform. You also use the handles this function returns to
                        create a sequence of arbitrary waveforms with the Create Arbitrary
                        Sequence function.
                        
                        If the instrument has multiple channels, it is possible to create
                        multi-channel waveforms: the channel names are passed as a
                        comma-separated list of channel names, and the waveform arrays
                        are concatenated into a single array. In this case, all waveforms
                        must be of the same length.
                        
                        If the function generator cannot store any more arbitrary waveforms, this
                        function returns the error No Waveforms Available.
                        """)
        ivi.add_method(self, 'outputs[].arbitrary.waveform.create_channel_waveform_int32',
                        self._arbitrary_waveform_create_channel_waveform_int32,
                        """
                        Creates a channel-specific arbitrary waveform and returns a handle that
                        identifies that waveform. Data is passed in as 32-bit binary data. If the
                        arbitrary waveform generator supports formats less than 32 bits, call the
                        BinaryAlignment property to determine whether to left or right justify the
                        data before passing it to this call. You pass a waveform handle as the
                        waveformHandle parameter of the Configure Arbitrary Waveform function to
                        produce that waveform. You also use the handles this function returns to
                        create a sequence of arbitrary waveforms with the Create Arbitrary
                        Sequence function.
                        
                        If the instrument has multiple channels, it is possible to create
                        multi-channel waveforms: the channel names are passed as a
                        comma-separated list of channel names, and the waveform arrays
                        are concatenated into a single array. In this case, all waveforms
                        must be of the same length.
                        
                        If the function generator cannot store any more arbitrary waveforms, this
                        function returns the error No Waveforms Available.
                        """)
        ivi.add_property(self, 'arbitrary.binary_alignment',
                        self._get_arbitrary_binary_alignment,
                        None,
                        None,
                        """
                        Identifies whether the arbitrary waveform generator treats binary data
                        provided to the Create Channel Arbitrary Waveform Int16 or Create Channel
                        Arbitrary Waveform Int32 functions as left-justified or right-justified.
                        Binary Alignment is only relevant if the generator supports bit-depths
                        less than the size of the binarydata type of the create waveform function
                        being used. For a 16-bit or a 32-bit generator, this function can return
                        either value.
                        """)
        ivi.add_property(self, 'arbitrary.sample_bit_resolution',
                        self._get_arbitrary_sample_bit_resolution,
                        None,
                        None,
                        """
                        Returns the number of significant bits that the generator supports in an
                        arbitrary waveform. Together with the binary alignment, this allows the
                        user to know the range and resolution of the integers in the waveform.
                        """)
        ivi.add_method(self, 'arbitrary.waveform.create_channel_waveform_int16',
                        self._arbitrary_waveform_create_channel_waveform_int16,
                        """
                        Creates a channel-specific arbitrary waveform and returns a handle that
                        identifies that waveform. Data is passed in as 16-bit binary data. If the
                        arbitrary waveform generator supports formats less than 16 bits, call the
                        BinaryAlignment property to determine whether to left or right justify the
                        data before passing it to this call. You pass a waveform handle as the
                        waveformHandle parameter of the Configure Arbitrary Waveform function to
                        produce that waveform. You also use the handles this function returns to
                        create a sequence of arbitrary waveforms with the Create Arbitrary
                        Sequence function.
                        
                        If the instrument has multiple channels, it is possible to create
                        multi-channel waveforms: the channel names are passed as a
                        comma-separated list of channel names, and the waveform arrays
                        are concatenated into a single array. In this case, all waveforms
                        must be of the same length.
                        
                        If the function generator cannot store any more arbitrary waveforms, this
                        function returns the error No Waveforms Available.
                        """)
        ivi.add_method(self, 'arbitrary.waveform.create_channel_waveform_int32',
                        self._arbitrary_waveform_create_channel_waveform_int32,
                        """
                        Creates a channel-specific arbitrary waveform and returns a handle that
                        identifies that waveform. Data is passed in as 32-bit binary data. If the
                        arbitrary waveform generator supports formats less than 32 bits, call the
                        BinaryAlignment property to determine whether to left or right justify the
                        data before passing it to this call. You pass a waveform handle as the
                        waveformHandle parameter of the Configure Arbitrary Waveform function to
                        produce that waveform. You also use the handles this function returns to
                        create a sequence of arbitrary waveforms with the Create Arbitrary
                        Sequence function.
                        
                        If the instrument has multiple channels, it is possible to create
                        multi-channel waveforms: the channel names are passed as a
                        comma-separated list of channel names, and the waveform arrays
                        are concatenated into a single array. In this case, all waveforms
                        must be of the same length.
                        
                        If the function generator cannot store any more arbitrary waveforms, this
                        function returns the error No Waveforms Available.
                        """)
    
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
        super(DataMarker, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'DataMarker'
        ivi.add_group_capability(self, cls+grp)
        
        self._data_marker_count = 1
        self._data_marker_name = list()
        self._data_marker_amplitude = list()
        self._data_marker_bit_position = list()
        self._data_marker_delay = list()
        self._data_marker_destination = list()
        self._data_marker_polarity = list()
        self._data_marker_source_channel = list()
        
        ivi.add_property(self, 'data_markers[].name',
                        self._get_data_marker_name,
                        None,
                        None,
                        """
                        This attribute returns the repeated capability identifier defined by
                        specific driver for the data marker that corresponds to the index that the
                        user specifies. If the driver defines a qualified Data Marker name, this
                        property returns the qualified name.
                        
                        If the value that the user passes for the Index parameter is less than
                        zero or greater than the value of the Data Marker Count, the attribute
                        returns an empty string for the value and returns an error.
                        """)
        ivi.add_property(self, 'data_markers[].amplitude',
                        self._get_data_marker_amplitude,
                        self._set_data_marker_amplitude,
                        None,
                        """
                        Specifies the amplitude of the data marker output. The units are volts.
                        """)
        ivi.add_property(self, 'data_markers[].bit_position',
                        self._get_data_marker_bit_position,
                        self._set_data_marker_bit_position,
                        None,
                        """
                        Specifies the bit position of the binary representation of the waveform
                        data that will be output as a data marker. A value of 0 indicates the
                        least significant bit.
                        """)
        ivi.add_property(self, 'data_markers[].delay',
                        self._get_data_marker_delay,
                        self._set_data_marker_delay,
                        None,
                        """
                        Specifies the amount of delay applied to the data marker output with
                        respect to the analog data output. A value of zero indicates the marker is
                        aligned with the analog data output.  The units are seconds.
                        """)
        ivi.add_property(self, 'data_markers[].destination',
                        self._get_data_marker_destination,
                        self._set_data_marker_destination,
                        None,
                        """
                        Specifies the destination terminal for the data marker output.
                        """)
        ivi.add_property(self, 'data_markers[].polarity',
                        self._get_data_marker_polarity,
                        self._set_data_marker_polarity,
                        None,
                        """
                        Specifies the polarity of the data marker output.
                        
                        Values for polarity:
                        
                        * 'active_high'
                        * 'active_low'
                        """)
        ivi.add_property(self, 'data_markers[].source_channel',
                        self._get_data_marker_source_channel,
                        self._set_data_marker_source_channel,
                        None,
                        """
                        Specifies the channel whose data bit will be output as a marker.
                        """)
        ivi.add_method(self, 'data_markers[].configure',
                        self._data_marker_configure,
                        """
                        Configures some of the common data marker attributes.
                        """)
        ivi.add_method(self, 'data_markers[].clear',
                        self._data_marker_clear,
                        """
                        Disables all of the data markers by setting their Data Marker Destination
                        attribute to None.
                        """)
        
        
    def _init_data_markers(self):
        try:
            super(DataMarker, self)._init_data_markers()
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
        
        self.data_markers._set_list(self._data_marker_name)
    
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
        super(ArbDataMask, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ArbDataMask'
        ivi.add_group_capability(self, cls+grp)
        
        self._arbitrary_data_mask = 0xffffffff
        
        ivi.add_property(self, 'arbitrary.data_mask',
                        self._get_arbitrary_data_mask,
                        self._set_arbitrary_data_mask,
                        None,
                        """
                        Determines which bits of the output data are masked out. This is
                        especially useful when combined with Data Markers so that the bits
                        embedded with the data to be used for markers are not actually output by
                        the generator.
                        
                        A value of 1 for a particular bit indicates that the data bit should be
                        output. A value of 0 indicates that the data bit should be masked out. For
                        example, if the value of this property is 0xFFFFFFFF (all bits are 1), no
                        masking is applied.
                        """)
    
    def _get_arbitrary_data_mask(self):
        return self._arbitrary_data_mask
    
    def _set_arbitrary_data_mask(self, value):
        value = int(value)
        self._arbitrary_data_mask = value
    
    
class SparseMarker(object):
    "Extension IVI methods for function generators that support output of markers associated with output data samples"
    
    def __init__(self, *args, **kwargs):
        super(SparseMarker, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'SparseMarker'
        ivi.add_group_capability(self, cls+grp)
        
        self._sparse_marker_count = 1
        self._sparse_marker_name = list()
        self._sparse_marker_amplitude = list()
        self._sparse_marker_delay = list()
        self._sparse_marker_destination = list()
        self._sparse_marker_polarity = list()
        self._sparse_marker_waveform_handle = list()
        
        ivi.add_property(self, 'sparse_markers[].name',
                        self._get_sparse_marker_name,
                        None,
                        None,
                        """
                        This attribute returns the repeated capability identifier defined by
                        specific driver for the sparse marker that corresponds to the index that
                        the user specifies. If the driver defines a qualified Sparse Marker name,
                        this property returns the qualified name.
                        
                        If the value that the user passes for the Index parameter is less than one
                        or greater than the value of the Sparse Marker Count, the attribute
                        returns an empty string for the value and returns an error.
                        """)
        ivi.add_property(self, 'sparse_markers[].amplitude',
                        self._get_sparse_marker_amplitude,
                        self._set_sparse_marker_amplitude,
                        None,
                        """
                        Specifies the amplitude of the sparse marker output. The units are volts.
                        """)
        ivi.add_property(self, 'sparse_markers[].delay',
                        self._get_sparse_marker_delay,
                        self._set_sparse_marker_delay,
                        None,
                        """
                        Specifies the amount of delay applied to the sparse marker output with
                        respect to the analog data output. A value of zero indicates the marker is
                        aligned with the analog data output. The units are seconds.
                        """)
        ivi.add_property(self, 'sparse_markers[].destination',
                        self._get_sparse_marker_destination,
                        self._set_sparse_marker_destination,
                        None,
                        """
                        Specifies the destination terminal for the sparse marker output.
                        """)
        ivi.add_property(self, 'sparse_markers[].polarity',
                        self._get_sparse_marker_polarity,
                        self._set_sparse_marker_polarity,
                        None,
                        """
                        Specifies the polarity of the sparse marker output.
                        
                        Values for polarity:
                        
                        * 'active_high'
                        * 'active_low'
                        """)
        ivi.add_property(self, 'sparse_markers[].waveform_handle',
                        self._get_sparse_marker_waveform_handle,
                        self._set_sparse_marker_waveform_handle,
                        None,
                        """
                        Specifies the waveform whose indexes the sparse marker refers to.
                        """)
        ivi.add_method(self, 'sparse_markers[].configure',
                        self._sparse_marker_configure,
                        """
                        Configures some of the common sparse marker attributes.
                        """)
        ivi.add_method(self, 'sparse_markers[].get_indexes',
                        self._sparse_marker_get_indexes,
                        """
                        Gets the coerced indexes associated with the sparse marker. These indexes
                        are specified by either the Configure SparseMarker function or the Set
                        Sparse Marker Indexes function.
                        """)
        ivi.add_method(self, 'sparse_markers[].set_indexes',
                        self._sparse_marker_set_indexes,
                        """
                        Sets the indexes associated with the sparse marker. These indexes may be
                        coerced by the driver. Use the Get Sparse Marker Indexes function to find
                        the coerced values.
                        """)
        ivi.add_method(self, 'sparse_markers[].clear',
                        self._sparse_marker_clear,
                        """
                        Disables all of the sparse markers by setting their Sparse Marker
                        Destination attribute to None.
                        """)
        
        
    def _init_sparse_markers(self):
        try:
            super(SparseMarker, self)._init_sparse_markers()
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
        
        self.sparse_markers._set_list(self._sparse_marker_name)
    
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
        super(ArbSeqDepth, self).__init__(*args, **kwargs)
        
        cls = 'IviFgen'
        grp = 'ArbSeqDepth'
        ivi.add_group_capability(self, cls+grp)
        
        self._arbitrary_sequence_depth_max = 1
        
        ivi.add_property(self, 'arbitrary.sequence.depth_max',
                        self._get_arbitrary_sequence_depth_max,
                        None,
                        None,
                        """
                        Returns the maximum sequence depth - that is, the number of times a
                        sequence can include other sequences recursively. A depth of zero
                        indicates the generator supports waveforms only. A depth of 1 indicates a
                        generator supports sequences of waveforms, but not sequences of sequences.
                        A depth of 2 or greater indicates that the generator supports sequences of
                        sequences. Note that if the MaxSequenceDepth is 2 or greater, the driver
                        must return unique handles for waveforms and sequences so that a sequence
                        may contain both waveform and sequence handles.
                        """)
    
    def _get_arbitrary_sequence_depth_max(self):
        return self._arbitrary_sequence_depth_max
    
    

