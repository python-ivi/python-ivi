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
class MarkerNotEnabledException(ivi.IviException): pass
class NotDeltaMarkerException(ivi.IviException): pass

# Parameter Values
AmplitudeUnits = set(['dBm', 'dBmV', 'dBuV', 'volt', 'watt'])
DetectorType = set(['auto_peak', 'average', 'maximum_peak', 'minimum_peak', 'sample', 'rms'])
TraceType = set(['clear_write', 'maximum_hold', 'minimum_hold', 'video_average', 'view', 'store'])
VerticalScale = set(['linear', 'logarithmic'])
AcquisitionStatus = set(['complete', 'in_progress', 'unknown'])

class Base(object):
    "Base IVI methods for all spectrum analyzers"
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__( *args, **kwargs)
        
        cls = 'IviSpecAn'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._trace_count = 1
        
        self._level_amplitude_units = 'dBm'
        self._level_attenuation = 0.0
        self._level_attenuation_auto = False
        self._acquisition_detector_type = 'sample'
        self._acquisition_detector_type_auto = False
        self._frequency_start = 1e3
        self._frequency_stop = 1e9
        self._frequency_offset = 0.0
        self._level_input_impedance = 50
        self._acquisition_number_of_sweeps = 1
        self._level_reference = 0.0
        self._level_reference_offset = 0.0
        self._sweep_coupling_resolution_bandwidth = 1e2
        self._sweep_coupling_resolution_bandwidth_auto = False
        self._acquisition_sweep_mode_continuous = True
        self._sweep_coupling_sweep_time = 1e-1
        self._sweep_coupling_sweep_time_auto = False
        self._trace_name = list()
        self._trace_type = list()
        self._acquisition_vertical_scale = 'logarithmic'
        self._sweep_coupling_video_bandwidth = 1e2
        self._sweep_coupling_video_bandwidth_auto = False
        
        ivi.add_property(self, 'level.amplitude_units',
                        self._get_level_amplitude_units,
                        self._set_level_amplitude_units,
                        None,
                        """
                        Specifies the amplitude units for input, output and display amplitude.
                        """)
        ivi.add_property(self, 'level.attenuation',
                        self._get_level_attenuation,
                        self._set_level_attenuation,
                        None,
                        """
                        Specifies the input attenuation (in positive dB).
                        """)
        ivi.add_property(self, 'level.attenuation_auto',
                        self._get_level_attenuation_auto,
                        self._set_level_attenuation_auto,
                        None,
                        """
                        If set to True, attenuation is automatically selected. If set to False,
                        attenuation is manually selected.
                        """)
        ivi.add_property(self, 'acquisition.detector_type',
                        self._get_acquisition_detector_type,
                        self._set_acquisition_detector_type,
                        None,
                        """
                        Specifies the detection method used to capture and process the signal.
                        This governs the data acquisition for a particular sweep, but does not
                        have any control over how multiple sweeps are processed.
                        """)
        ivi.add_property(self, 'acquisition.detector_type_auto',
                        self._get_acquisition_detector_type_auto,
                        self._set_acquisition_detector_type_auto,
                        None,
                        """
                        If set to True, the detector type is automatically selected. The
                        relationship between Trace Type and Detector Type is not defined by the
                        specification when the Detector Type Auto is set to True. If set to False,
                        the detector type is manually selected.
                        """)
        ivi.add_property(self, 'frequency.start',
                        self._get_frequency_start,
                        self._set_frequency_start,
                        None,
                        """
                        Specifies the left edge of the frequency domain in Hertz. This is used in
                        conjunction with the Frequency Stop attribute to define the frequency
                        domain. If the Frequency Start attribute value is equal to the Frequency
                        Stop attribute value then the spectrum analyzer's horizontal attributes
                        are in time-domain.
                        """)
        ivi.add_property(self, 'frequency.stop',
                        self._get_frequency_stop,
                        self._set_frequency_stop,
                        None,
                        """
                        Specifies the right edge of the frequency domain in Hertz. This is used in
                        conjunction with the Frequency Start attribute to define the frequency
                        domain. If the Frequency Start attribute value is equal to the Frequency
                        Stop attribute value then the spectrum analyzer's horizontal attributes are
                        in time-domain.
                        """)
        ivi.add_property(self, 'frequency.offset',
                        self._get_frequency_offset,
                        self._set_frequency_offset,
                        None,
                        """
                        Specifies an offset value, in Hertz, that is added to the frequency
                        readout. The offset is used to compensate for external frequency
                        conversion. This changes the driver's Frequency Start and Frequency Stop
                        attributes.
                        
                        The equations relating the affected values are:
                        
                          Frequency Start = Actual Start Frequency + Frequency Offset
                          Frequency Stop = Actual Stop Frequency + Frequency Offset
                          Marker Position = Actual Marker Frequency + Frequency Offset
                        """)
        ivi.add_property(self, 'level.input_impedance',
                        self._get_level_input_impedance,
                        self._set_level_input_impedance,
                        None,
                        """
                        Specifies the value of input impedance, in ohms, expected at the active
                        input port. This is typically 50 ohms or 75 ohms.
                        """)
        ivi.add_property(self, 'acquisition.number_of_sweeps',
                        self._get_acquisition_number_of_sweeps,
                        self._set_acquisition_number_of_sweeps,
                        None,
                        """
                        This attribute defines the number of sweeps. This attribute value has no
                        effect if the Trace Type attribute is set to the value Clear Write.
                        """)
        ivi.add_property(self, 'level.reference',
                        self._get_level_reference,
                        self._set_level_reference,
                        None,
                        """
                        The calibrated vertical position of the captured data used as a reference
                        for amplitude measurements. This is typically set to a value slightly
                        higher than the highest expected signal level. The units are determined by
                        the Amplitude Units attribute.
                        """)
        ivi.add_property(self, 'level.reference_offset',
                        self._get_level_reference_offset,
                        self._set_level_reference_offset,
                        None,
                        """
                        Specifies an offset for the Reference Level attribute. This value is used
                        to adjust the reference level for external signal gain or loss. A
                        positive value corresponds to a gain while a negative number corresponds
                        to a loss. The value is in dB.
                        """)
        ivi.add_property(self, 'sweep_coupling.resolution_bandwidth',
                        self._get_sweep_coupling_resolution_bandwidth,
                        self._set_sweep_coupling_resolution_bandwidth,
                        None,
                        """
                        Specifies the width of the IF filter in Hertz. For more information see
                        Section 4.1.1, Sweep Coupling Overview.
                        """)
        ivi.add_property(self, 'sweep_coupling.resolution_bandwidth_auto',
                        self._get_sweep_coupling_resolution_bandwidth_auto,
                        self._set_sweep_coupling_resolution_bandwidth_auto,
                        None,
                        """
                        If set to True, the resolution bandwidth is automatically selected. If set
                        to False, the resolution bandwidth is manually selected.
                        """)
        ivi.add_property(self, 'acquisition.sweep_mode_continuous',
                        self._get_acquisition_sweep_mode_continuous,
                        self._set_acquisition_sweep_mode_continuous,
                        None,
                        """
                        If set to True, the sweep mode is continuous If set to False, the sweep
                        mode is not continuous.
                        """)
        ivi.add_property(self, 'sweep_coupling.sweep_time',
                        self._get_sweep_coupling_sweep_time,
                        self._set_sweep_coupling_sweep_time,
                        None,
                        """
                        Specifies the length of time to sweep from the left edge to the right edge
                        of the current domain. The units are seconds.
                        """)
        ivi.add_property(self, 'sweep_coupling.sweep_time_auto',
                        self._get_sweep_coupling_sweep_time_auto,
                        self._set_sweep_coupling_sweep_time_auto,
                        None,
                        """
                        If set to True, the sweep time is automatically selected If set to False,
                        the sweep time is manually selected.
                        """)
        ivi.add_property(self, 'traces[].name',
                        self._get_trace_name,
                        None,
                        None,
                        """
                        Returns the physical repeated capability identifier defined by the
                        specific driver for the trace that corresponds to the index that the user
                        specifies. If the driver defines a qualified trace name, this property
                        returns the qualified name.
                        """)
        ivi.add_property(self, 'traces[].type',
                        self._get_trace_type,
                        self._set_trace_type,
                        None,
                        """
                        Specifies the representation of the acquired data.
                        """)
        ivi.add_property(self, 'acquisition.vertical_scale',
                        self._get_acquisition_vertical_scale,
                        self._set_acquisition_vertical_scale,
                        None,
                        """
                        Specifies the vertical scale of the measurement hardware (use of log
                        amplifiers versus linear amplifiers).
                        """)
        ivi.add_property(self, 'sweep_coupling.video_bandwidth',
                        self._get_sweep_coupling_video_bandwidth,
                        self._set_sweep_coupling_video_bandwidth,
                        None,
                        """
                        Specifies the video bandwidth of the post-detection filter in Hertz.
                        """)
        ivi.add_property(self, 'sweep_coupling.video_bandwidth_auto',
                        self._get_sweep_coupling_video_bandwidth_auto,
                        self._set_sweep_coupling_video_bandwidth_auto,
                        None,
                        """
                        If set to True, the video bandwidth is automatically selected. If set to
                        False, the video bandwidth is manually selected.
                        """)
        ivi.add_method(self, 'acquisition.abort',
                       self._acquisition_abort,
                       """
                       This function aborts a previously initiated measurement and returns the
                       spectrum analyzer to the idle state. This function does not check
                       instrument status.
                       """)
        ivi.add_method(self, 'acquisition.status',
                       self._acquisition_status,
                       """
                       This function determines and returns the status of an acquisition.
                       """)
        ivi.add_method(self, 'acquisition.configure',
                       self._acquisition_configure,
                       """
                       This function configures the acquisition attributes of the spectrum
                       analyzer.
                       """)
        ivi.add_method(self, 'frequency.configure_center_span',
                       self._frequency_configure_center_span,
                       """
                       This function configures the frequency range defining the center frequency
                       and the frequency span. If the span corresponds to zero Hertz, then the
                       spectrum analyzer operates in time-domain mode. Otherwise, the spectrum
                       analyzer operates in frequency-domain mode.
                       
                       This function modifies the Frequency Start and Frequency Stop attributes as
                       follows:
                       
                         Frequency Start = CenterFrequency - Span / 2
                         Frequency Stop = CenterFrequency + Span / 2
                       """)
        ivi.add_method(self, 'frequency.configure_start_stop',
                       self._frequency_configure_start_stop,
                       """
                       This function configures the frequency range defining its start frequency
                       and its stop frequency. If the start frequency is equal to the stop
                       frequency, then the spectrum analyzer operates in time-domain mode.
                       Otherwise, the spectrum analyzer operates in frequency-domain mode.
                       """)
        ivi.add_method(self, 'level.configure',
                       self._level_configure,
                       """
                       This function configures the vertical attributes of the spectrum analyzer.
                       This corresponds to the Amplitude Units, Input Attenuation, Input
                       Impedance, Reference Level, and Reference Level Offset attributes.
                       """)
        ivi.add_method(self, 'sweep_coupling.configure',
                       self._sweep_coupling_configure,
                       """
                       This function configures the coupling and sweeping attributes. For
                       additional sweep coupling information refer to Section 4.1.1, Sweep
                       Coupling Overview.
                       """)
        ivi.add_method(self, 'traces[].fetch_y',
                       self._trace_fetch_y,
                       """
                       This function returns the trace the spectrum analyzer acquires. The trace
                       is from a previously initiated acquisition. The user calls the Initiate
                       function to start an acquisition. The user calls the Acquisition Status
                       function to determine when the acquisition is complete.
                       
                       The user may call the Read Y Trace function instead of the Initiate
                       function. This function starts an acquisition, waits for the acquisition
                       to complete, and returns the trace in one function call.
                       
                       The Amplitude array returns data that represents the amplitude of the
                       signals obtained by sweeping from the start frequency to the stop frequency
                       (in frequency domain, in time domain the amplitude array is ordered from
                       beginning of sweep to end). The Amplitude Units attribute determines the
                       units of the points in the Amplitude array.
                       
                       This function does not check the instrument status. The user calls the
                       Error Query function at the conclusion of the sequence to check the
                       instrument status.
                       """)
        ivi.add_method(self, 'acquisition.initiate',
                       self._acquisition_initiate,
                       """
                       This function initiates an acquisition. After calling this function, the
                       spectrum analyzer leaves the idle state.
                       
                       This function does not check the instrument status. The user calls the
                       Acquisition Status function to determine when the acquisition is complete.
                       """)
        ivi.add_method(self, 'traces[].read_y',
                       self._trace_read_y,
                       """
                       This function initiates a signal acquisition based on the present
                       instrument configuration. It then waits for the acquisition to complete,
                       and returns the trace as an array of amplitude values. The amplitude array
                       returns data that represent the amplitude of the signals obtained by
                       sweeping from the start frequency to the stop frequency (in frequency
                       domain, in time domain the amplitude array is ordered from beginning of
                       sweep to end). The Amplitude Units attribute determines the units of the
                       points in the amplitude array. This function resets the sweep count.
                       
                       If the spectrum analyzer did not complete the acquisition within the time
                       period the user specified with the MaxTime parameter, the function returns
                       the Max Time Exceeded error.
                       """)
        
        self._init_traces()
    
    def _init_traces(self):
        try:
            super(Base, self)._init_traces()
        except AttributeError:
            pass
        
        self._trace_name = list()
        self._trace_type = list()
        for i in range(self._trace_count):
            self._trace_name.append("trace%d" % (i+1))
            self._trace_type.append('')
        
        self.traces._set_list(self._trace_name)
    
    def _get_level_amplitude_units(self):
        return self._level_amplitude_units
    
    def _set_level_amplitude_units(self, value):
        if value not in AmplitudeUnits:
            raise ivi.ValueNotSupportedException()
        self._level_amplitude_units = value
    
    def _get_level_attenuation(self):
        return self._level_attenuation
    
    def _set_level_attenuation(self, value):
        value = float(value)
        self._level_attenuation = value
    
    def _get_level_attenuation_auto(self):
        return self._level_attenuation_auto
    
    def _set_level_attenuation_auto(self, value):
        value = bool(value)
        self._level_attenuation_auto = value
    
    def _get_acquisition_detector_type(self):
        return self._acquisition_detector_type
    
    def _set_acquisition_detector_type(self, value):
        if value not in DetectorType:
            raise ivi.ValueNotSupportedException()
        self._acquisition_detector_type = value
    
    def _get_acquisition_detector_type_auto(self):
        return self._acquisition_detector_type_auto
    
    def _set_acquisition_detector_type_auto(self, value):
        value = bool(value)
        self._acquisition_detector_type_auto = value
    
    def _get_frequency_start(self):
        return self._frequency_start
    
    def _set_frequency_start(self, value):
        value = float(value)
        self._frequency_start = value
    
    def _get_frequency_stop(self):
        return self._frequency_stop
    
    def _set_frequency_stop(self, value):
        value = float(value)
        self._frequency_stop = value
    
    def _get_frequency_offset(self):
        return self._frequency_offset
    
    def _set_frequency_offset(self, value):
        value = float(value)
        self._frequency_offset = value
    
    def _get_level_input_impedance(self):
        return self._level_input_impedance
    
    def _set_level_input_impedance(self, value):
        value = float(value)
        self._level_input_impedance = value
    
    def _get_acquisition_number_of_sweeps(self):
        return self._acquisition_number_of_sweeps
    
    def _set_acquisition_number_of_sweeps(self, value):
        value = int(value)
        self._acquisition_number_of_sweeps = value
    
    def _get_level_reference(self):
        return self._level_reference
    
    def _set_level_reference(self, value):
        value = float(value)
        self._level_reference = value
    
    def _get_level_reference_offset(self):
        return self._level_reference_offset
    
    def _set_level_reference_offset(self, value):
        value = float(value)
        self._level_reference_offset = value
    
    def _get_sweep_coupling_resolution_bandwidth(self):
        return self._sweep_coupling_resolution_bandwidth
    
    def _set_sweep_coupling_resolution_bandwidth(self, value):
        value = float(value)
        self._sweep_coupling_resolution_bandwidth = value
    
    def _get_sweep_coupling_resolution_bandwidth_auto(self):
        return self._sweep_coupling_resolution_bandwidth_auto
    
    def _set_sweep_coupling_resolution_bandwidth_auto(self, value):
        value = bool(value)
        self._sweep_coupling_resolution_bandwidth_auto = value
    
    def _get_acquisition_sweep_mode_continuous(self):
        return self._acquisition_sweep_mode_continuous
    
    def _set_acquisition_sweep_mode_continuous(self, value):
        value = bool(value)
        self._acquisition_sweep_mode_continuous = value
    
    def _get_sweep_coupling_sweep_time(self):
        return self._sweep_coupling_sweep_time
    
    def _set_sweep_coupling_sweep_time(self, value):
        value = float(value)
        self._sweep_coupling_sweep_time = value
    
    def _get_sweep_coupling_sweep_time_auto(self):
        return self._sweep_coupling_sweep_time_auto
    
    def _set_sweep_coupling_sweep_time_auto(self, value):
        value = bool(value)
        self._sweep_coupling_sweep_time_auto = value
    
    def _get_trace_name(self, index):
        index = ivi.get_index(self._trace_name, index)
        return self._trace_name[index]
    
    def _get_trace_type(self, index):
        index = ivi.get_index(self._trace_name, index)
        return self._trace_type[index]
    
    def _set_trace_type(self, index, value):
        index = ivi.get_index(self._trace_name, index)
        if value not in TraceType:
            raise ivi.ValueNotSupportedException()
        self._trace_type[index] = value
    
    def _get_acquisition_vertical_scale(self):
        return self._acquisition_vertical_scale
    
    def _set_acquisition_vertical_scale(self, value):
        value = float(value)
        self._acquisition_vertical_scale = value
    
    def _get_sweep_coupling_video_bandwidth(self):
        return self._sweep_coupling_video_bandwidth
    
    def _set_sweep_coupling_video_bandwidth(self, value):
        value = float(value)
        self._sweep_coupling_video_bandwidth = value
    
    def _get_sweep_coupling_video_bandwidth_auto(self):
        return self._sweep_coupling_video_bandwidth_auto
    
    def _set_sweep_coupling_video_bandwidth_auto(self, value):
        value = bool(value)
        self._sweep_coupling_video_bandwidth_auto = value
    
    def _acquisition_abort(self):
        pass
    
    def _acquisition_status(self):
        return 'unknown'
    
    def _acquisition_configure(self, sweep_mode_continuous, number_of_sweeps, detector_type, vertical_scale):
        self._set_acquisition_sweep_mode_continuous(sweep_mode_continuous)
        self._set_acquisition_number_of_sweeps(number_of_sweeps)
        if detector_type == 'auto' or not detector_type:
            self._set_acquisition_detector_type_auto(True)
        else:
            self._set_acquisition_detector_type_auto(False)
            self._set_acquisition_detector_type(detector_type)
        self._set_acquisition_vertical_scale(vertical_scale)
    
    def _frequency_configure_center_span(self, center, span):
        self._set_frequency_start(center - span/2)
        self._set_frequency_stop(center + span/2)
    
    def _frequency_configure_start_stop(self, start, stop):
        self._set_frequency_start(start)
        self._set_frequency_stop(stop)
    
    def _level_configure(self, amplitude_units, input_impedance, reference, reference_offset, attenuation):
        self._set_level_amplitude_units(amplitude_units)
        self._set_level_input_impedance(input_impedance)
        self._set_level_reference(reference)
        self._set_level_reference_offset(reference_offset)
        if attenuation == 'auto':
            self._set_level_attenuation_auto(True)
        else:
            self._set_level_attenuation_auto(False)
            self._set_level_attenuation(attenuation)
    
    def _sweep_coupling_configure(self, resolution_bandwidth, video_bandwidth, sweep_time):
        if resolution_bandwidth == 'auto':
            self._set_sweep_coupling_resolution_bandwidth_auto(True)
        else:
            self._set_sweep_coupling_resolution_bandwidth_auto(False)
            self._set_sweep_coupling_resolution_bandwidth(resolution_bandwidth)
        if video_bandwidth == 'auto':
            self._set_sweep_coupling_video_bandwidth_auto(True)
        else:
            self._set_sweep_coupling_video_bandwidth_auto(False)
            self._set_sweep_coupling_video_bandwidth(video_bandwidth)
        if sweep_time == 'auto':
            self._set_sweep_coupling_sweep_time_auto(True)
        else:
            self._set_sweep_coupling_sweep_time_auto(False)
            self._set_sweep_coupling_sweep_time(sweep_time)
    
    def _trace_fetch_y(self, index):
        index = ivi.get_index(self._trace_name, index)
        data = list()
        return data
    
    def _acquisition_initiate(self):
        pass
    
    def _trace_read_y(self, index):
        return self._trace_fetch_y(index)


class Multitrace(object):
    "Extension IVI methods for spectrum analyzers supporting simple mathematical operations on traces"
    
    def __init__(self, *args, **kwargs):
        super(Interpolation, self).__init__( *args, **kwargs)
        
        cls = 'IviSpecAn'
        grp = 'Multitrace'
        ivi.add_group_capability(self, cls+grp)
        
        ivi.add_method(self, 'trace_math.add',
                       self._trace_math_add,
                       """
                       This function modifies a trace to be the point by point sum of two other
                       traces. Any data in the destination trace is deleted.
                       
                         DestinationTrace = Trace1 + Trace2
                       """)
        ivi.add_method(self, 'trace_math.copy',
                       self._trace_math_copy,
                       """
                       This function copies the data array from one trace into another trace. Any
                       data in the Destination Trace is deleted.
                       """)
        ivi.add_method(self, 'trace_math.exchange',
                       self._trace_math_exchange,
                       """
                       This function exchanges the data arrays of two traces.
                       """)
        ivi.add_method(self, 'trace_math.subtract',
                       self._trace_math_subtract,
                       """
                       This function modifies a trace to be the point by point difference between
                       two traces. Any data in the destination trace is deleted.
                       
                         DestinationTrace = Trace1 - Trace2
                       """)
    
    def _trace_math_add(self, dest, trace1, trace2):
        pass
    
    def _trace_math_copy(self, dest, src):
        pass
    
    def _trace_math_exchange(self, trace1, trace2):
        pass
    
    def _trace_math_subtract(self, dest, trace1, trace2):
        pass



# Marker
# Trigger
# ExternalTrigger
# SoftwareTrigger
# VideoTrigger
# Display
# MarkerType
# DeltaMarker
# ExternalMixer
# Preselector

