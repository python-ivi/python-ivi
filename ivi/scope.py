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

from . import ivi

# Exceptions
class ChannelNotEnabledException(ivi.IviException): pass
class InvalidAcquisitionTypeException(ivi.IviException): pass
class UnableToPerformMeasurementException(ivi.IviException): pass

# Parameter Values
AcquisitionType = set(['normal', 'peak_detect', 'high_resolution', 'average'])
VerticalCoupling = set(['ac', 'dc', 'gnd'])
TriggerCoupling = set(['ac', 'dc', 'hf_reject', 'lf_reject', 'noise_reject'])
Slope = set(['positive', 'negative', 'either'])
Trigger = set(['edge', 'width', 'runt', 'glitch', 'tv', 'immediate', 'ac_line'])
Interpolation = set(['none', 'sinex', 'linear'])
TVTriggerEvent = set(['field1', 'field2', 'any_field', 'any_line', 'line_number'])
TVTriggerFormat = set(['ntsc', 'pal', 'secam'])
Polarity = set(['positive', 'negative'])
Polarity3 = set(['positive', 'negative', 'either'])
GlitchCondition = set(['less_than', 'greater_than'])
WidthCondition = set(['within', 'outside'])
AcquisitionSampleMode = set(['real_time', 'equivalent_time'])
TriggerModifier = set(['none', 'auto', 'auto_level'])
MeasurementFunction = set(['rise_time', 'fall_time', 'frequency', 'period',
        'voltage_rms', 'voltage_peak_to_peak', 'voltage_max', 'voltage_min',
        'voltage_high', 'voltage_low', 'voltage_average', 'width_negative',
        'width_positive', 'duty_cycle_negative', 'duty_cycle_positive',
        'amplitude', 'voltage_cycle_rms', 'voltage_cycle_average',
        'overshoot', 'preshoot'])
AcquisitionStatus = set(['complete', 'in_progress', 'unknown'])

class Base(ivi.IviContainer):
    "Base IVI methods for all oscilloscopes"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(Base, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_start_time = 0
        self._acquisition_type = 'normal'
        self._acquisition_number_of_points_minimum = 0
        self._acquisition_record_length = 1000
        self._acquisition_time_per_record = 1e-3
        self._channel_name = list()
        self._channel_enabled = list()
        self._channel_input_impedance = list()
        self._channel_input_frequency_max = list()
        self._channel_probe_attenuation = list()
        self._channel_coupling = list()
        self._channel_offset = list()
        self._channel_range = list()
        self._channel_count = 1
        self._measurement_status = 'unknown'
        self._trigger_coupling = 'dc'
        self._trigger_holdoff = 0
        self._trigger_level = 0
        self._trigger_edge_slope = 'positive'
        self._trigger_source = ""
        self._trigger_type = 'edge'
        
        self._add_property('acquisition.start_time',
                        self._get_acquisition_start_time,
                        self._set_acquisition_start_time,
                        None,
                        ivi.Doc("""
                        Specifies the length of time from the trigger event to the first point in
                        the waveform record. If the value is positive, the first point in the
                        waveform record occurs after the trigger event. If the value is negative,
                        the first point in the waveform record occurs before the trigger event.
                        The units are seconds.
                        """, cls, grp, '4.2.1'))
        self._add_property('acquisition.type',
                        self._get_acquisition_type,
                        self._set_acquisition_type,
                        None,
                        ivi.Doc("""
                        Specifies how the oscilloscope acquires data and fills the waveform
                        record.
                        
                        Values:
                        * 'normal'
                        * 'high_resolution'
                        * 'average'
                        * 'peak_detect'
                        * 'envelope'
                        """, cls, grp, '4.2.3'))
        self._add_property('acquisition.number_of_points_minimum',
                        self._get_acquisition_number_of_points_minimum,
                        self._set_acquisition_number_of_points_minimum,
                        None,
                        ivi.Doc("""
                        Specifies the minimum number of points the end-user requires in the
                        waveform record for each channel. The instrument driver uses the value the
                        end-user specifies to configure the record length that the oscilloscope
                        uses for waveform acquisition. If the instrument cannot support the
                        requested record length, the driver shall configure the instrument to the
                        closest bigger record length. The Horizontal Record Length attribute
                        returns the actual record length.
                        """, cls, grp, '4.2.8'))
        self._add_property('acquisition.record_length',
                        self._get_acquisition_record_length,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the actual number of points the oscilloscope acquires for each
                        channel. The value is equal to or greater than the minimum number of
                        points the end-user specifies with the Horizontal Minimum Number of Points
                        attribute.
                        
                        Note: Oscilloscopes may use different size records depending on the value
                        the user specifies for the Acquisition Type attribute.
                        """, cls, grp, '4.2.9'))
        self._add_property('acquisition.sample_rate',
                        self._get_acquisition_sample_rate,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the effective sample rate of the acquired waveform using the
                        current configuration. The units are samples per second.
                        """, cls, grp, '4.2.10'))
        self._add_property('acquisition.time_per_record',
                        self._get_acquisition_time_per_record,
                        self._set_acquisition_time_per_record,
                        None,
                        ivi.Doc("""
                        Specifies the length of time that corresponds to the record length. The
                        units are seconds.
                        """, cls, grp, '4.2.11'))
        self._add_method('acquisition.configure_record',
                        self._acquisition_configure_record,
                        ivi.Doc("""
                        This function configures the most commonly configured attributes of the
                        oscilloscope acquisition sub-system. These attributes are the time per
                        record, minimum record length, and the acquisition start time.
                        """, cls, grp, '4.3.4'))
        self._add_property('channels[].name',
                        self._get_channel_name,
                        None,
                        None,
                        ivi.Doc("""
                        This attribute returns the repeated capability identifier defined by
                        specific driver for the channel that corresponds to the index that the
                        user specifies. If the driver defines a qualified channel name, this
                        property returns the qualified name.
                        
                        If the value that the user passes for the Index parameter is less than
                        zero or greater than the value of the channel count, the attribute raises
                        a SelectorRangeException.
                        """, cls, grp, '4.2.7'))
        self._add_property('channels[].enabled',
                        self._get_channel_enabled,
                        self._set_channel_enabled,
                        None,
                        ivi.Doc("""
                        If set to True, the oscilloscope acquires a waveform for the channel. If
                        set to False, the oscilloscope does not acquire a waveform for the
                        channel.
                        """, cls, grp, '4.2.5'))
        self._add_property('channels[].input_impedance',
                        self._get_channel_input_impedance,
                        self._set_channel_input_impedance,
                        None,
                        ivi.Doc("""
                        Specifies the input impedance for the channel in Ohms.
                        
                        Common values are 50.0, 75.0, and 1,000,000.0.
                        """, cls, grp, '4.2.12'))
        self._add_property('channels[].input_frequency_max',
                        self._get_channel_input_frequency_max,
                        self._set_channel_input_frequency_max,
                        None,
                        ivi.Doc("""
                        Specifies the maximum frequency for the input signal you want the
                        instrument to accommodate without attenuating it by more than 3dB. If the
                        bandwidth limit frequency of the instrument is greater than this maximum
                        frequency, the driver enables the bandwidth limit. This attenuates the
                        input signal by at least 3dB at frequencies greater than the bandwidth
                        limit.
                        """, cls, grp, '4.2.13'))
        self._add_property('channels[].probe_attenuation',
                        self._get_channel_probe_attenuation,
                        self._set_channel_probe_attenuation,
                        None,
                        ivi.Doc("""
                        Specifies the scaling factor by which the probe the end-user attaches to
                        the channel attenuates the input. For example, for a 10:1 probe, the
                        end-user sets this attribute to 10.0.
                        
                        Note that if the probe is changed to one with a different attenuation, and
                        this attribute is not set, the amplitude calculations will be incorrect.
                        
                        Querying this value will return the probe attenuation corresponding to the
                        instrument's actual probe attenuation. Setting this property sets Probe
                        Attenuation Auto to False Negative values are not valid.
                        """, cls, grp, '4.2.16'))
        self._add_property('channels[].coupling',
                        self._get_channel_coupling,
                        self._set_channel_coupling,
                        None,
                        ivi.Doc("""
                        Specifies how the oscilloscope couples the input signal for the channel.
                        
                        Values:
                        
                        * 'ac'
                        * 'dc'
                        * 'gnd'
                        """, cls, grp, '4.2.23'))
        self._add_property('channels[].offset',
                        self._get_channel_offset,
                        self._set_channel_offset,
                        None,
                        ivi.Doc("""
                        Specifies the location of the center of the range that the Vertical Range
                        attribute specifies. The value is with respect to ground and is in volts.
                        
                        For example, to acquire a sine wave that spans between on 0.0 and 10.0
                        volts, set this attribute to 5.0 volts.
                        """, cls, grp, '4.2.24'))
        self._add_property('channels[].range',
                        self._get_channel_range,
                        self._set_channel_range,
                        None,
                        ivi.Doc("""
                        Specifies the absolute value of the full-scale input range for a channel.
                        The units are volts.
                        
                        For example, to acquire a sine wave that spans between -5.0 and 5.0 volts,
                        set the Vertical Range attribute to 10.0 volts.
                        """, cls, grp, '4.2.25'))
        self._add_method('channels[].configure',
                        self._channel_configure,
                        ivi.Doc("""
                        This function configures the most commonly configured attributes of the
                        oscilloscope channel sub-system. These attributes are the range, offset,
                        coupling, probe attenuation, and whether the channel is enabled.
                        """, cls, grp, '4.3.6'))
        self._add_method('channels[].configure_characteristics',
                        self._channel_configure_characteristics,
                        ivi.Doc("""
                        This function configures the attributes that control the electrical
                        characteristics of the channel. These attributes are the input impedance
                        and the maximum frequency of the input signal.
                        """, cls, grp, '4.3.8'))
        self._add_method('channels[].measurement.fetch_waveform',
                        self._measurement_fetch_waveform,
                        ivi.Doc("""
                        This function returns the waveform the oscilloscope acquires for the
                        specified channel. The waveform is from a previously initiated
                        acquisition.
                        
                        You use the Initiate Acquisition function to start an acquisition on the
                        channels that the end-user configures with the Configure Channel function.
                        The oscilloscope acquires waveforms on the concurrently enabled channels.
                        If the channel is not enabled for the acquisition, this function returns
                        the Channel Not Enabled error.
                        
                        Use this function only when the acquisition mode is Normal, Hi Res, or
                        Average. If the acquisition type is not one of the listed types, the
                        function returns the Invalid Acquisition Type error.
                        
                        You use the Acquisition Status function to determine when the acquisition
                        is complete. You must call this function separately for each enabled
                        channel to obtain the waveforms.
                        
                        You can call the Read Waveform function instead of the Initiate
                        Acquisition function. The Read Waveform function starts an acquisition on
                        all enabled channels, waits for the acquisition to complete, and returns
                        the waveform for the specified channel. You call this function to obtain
                        the waveforms for each of the remaining channels.
                        
                        The return value is a list of (x, y) tuples that represent the time and
                        voltage of each data point.  The y point may be NaN in the case that the
                        oscilloscope could not sample the voltage.
                        
                        The end-user configures the interpolation method the oscilloscope uses
                        with the Acquisition.Interpolation property. If interpolation is disabled,
                        the oscilloscope does not interpolate points in the waveform. If the
                        oscilloscope cannot sample a value for a point in the waveform, the driver
                        sets the corresponding element in the waveformArray to an IEEE-defined NaN
                        (Not a Number) value. Check for this value with math.isnan() or
                        numpy.isnan().
                        
                        This function does not check the instrument status. Typically, the
                        end-user calls this function only in a sequence of calls to other
                        low-level driver functions. The sequence performs one operation. The
                        end-user uses the low-level functions to optimize one or more aspects of
                        interaction with the instrument. Call the Error Query function at the
                        conclusion of the sequence to check the instrument status.
                        """, cls, grp, '4.3.13'))
        self._add_method('channels[].measurement.read_waveform',
                        self._measurement_read_waveform,
                        ivi.Doc("""
                        This function initiates an acquisition on the channels that the end-user
                        configures with the Configure Channel function. If the channel is not
                        enabled for the acquisition, this function returns Channel Not Enabled
                        error. It then waits for the acquisition to complete, and returns the
                        waveform for the channel the end-user specifies. If the oscilloscope did
                        not complete the acquisition within the time period the user specified
                        with the max_time parameter, the function returns the Max Time Exceeded
                        error.
                        
                        Use this function only when the acquisition mode is Normal, Hi Res, or
                        Average. If the acquisition type is not one of the listed types, the
                        function returns the Invalid Acquisition Type error.
                        
                        You call the Fetch Waveform function to obtain the waveforms for each of
                        the remaining enabled channels without initiating another acquisition.
                        After this function executes, each element in the WaveformArray parameter
                        is either a voltage or a value indicating that the oscilloscope could not
                        sample a voltage.
                        
                        
                        The end-user configures the interpolation method the oscilloscope uses
                        with the Acquisition.Interpolation property. If interpolation is disabled,
                        the oscilloscope does not interpolate points in the waveform. If the
                        oscilloscope cannot sample a value for a point in the waveform, the driver
                        sets the corresponding element in the waveformArray to an IEEE-defined NaN
                        (Not a Number) value. Check for this value with math.isnan() or
                        numpy.isnan(). Check an entire array with
                        
                        any(any(math.isnan(b) for b in a) for a in waveform)
                        """, cls, grp, '4.3.16'))
        self._add_property('measurement.status',
                        self._get_measurement_status,
                        None,
                        None,
                        ivi.Doc("""
                        Acquisition status indicates whether an acquisition is in progress,
                        complete, or if the status is unknown.
                        
                        Acquisition status is not the same as instrument status, and does not
                        necessarily check for instrument errors. To make sure that the instrument
                        is checked for errors after getting the acquisition status, call the Error
                        Query method. (Note that the end user may want to call Error Query at the
                        end of a sequence of other calls which include getting the acquisition
                        status - it does not necessarily need to be called immediately.)
                        
                        If the driver cannot determine whether the acquisition is complete or not,
                        it returns the Acquisition Status Unknown value.
                        
                        Values:
                        * 'compete'
                        * 'in_progress'
                        * 'unknown'
                        """, cls, grp, '4.2.2'))
        self._add_method('measurement.abort',
                        self._measurement_abort,
                        ivi.Doc("""
                        This function aborts an acquisition and returns the oscilloscope to the
                        Idle state. This function does not check the instrument status.
                        
                        Typically, the end-user calls this function only in a sequence of calls to
                        other low-level driver functions. The sequence performs one operation. The
                        end-user uses the low-level functions to optimize one or more aspects of
                        interaction with the instrument. Call the Error Query function at the
                        conclusion of the sequence to check the instrument status.
                        
                        If the instrument cannot abort an initiated acquisition, the driver shall
                        return the Function Not Supported error.
                        """, cls, grp, '4.3.1'))
        self._add_method('measurement.initiate',
                        self._measurement_initiate,
                        ivi.Doc("""
                        This function initiates a waveform acquisition. After calling this
                        function, the oscilloscope leaves the idle state and waits for a trigger.
                        The oscilloscope acquires a waveform for each channel the end-user has
                        enabled with the Configure Channel function.
                        
                        This function does not check the instrument status. Typically, the
                        end-user calls this function only in a sequence of calls to other
                        low-level driver functions. The sequence performs one operation. The
                        end-user uses the low-level functions to optimize one or more aspects of
                        interaction with the instrument. Call the Error Query function at the
                        conclusion of the sequence to check the instrument status.
                        """, cls, grp, '4.3.14'))
        self._add_property('trigger.coupling',
                        self._get_trigger_coupling,
                        self._set_trigger_coupling,
                        None,
                        ivi.Doc("""
                        Specifies how the oscilloscope couples the trigger source.
                        
                        Values:
                        
                        * 'ac'
                        * 'dc'
                        * 'lf_reject'
                        * 'hf_reject'
                        * 'noise_reject'
                        """, cls, grp, '4.2.17'))
        self._add_property('trigger.holdoff',
                        self._get_trigger_holdoff,
                        self._set_trigger_holdoff,
                        None,
                        ivi.Doc("""
                        Specifies the length of time the oscilloscope waits after it detects a
                        trigger until the oscilloscope enables the trigger subsystem to detect
                        another trigger. The units are seconds. The Trigger Holdoff attribute
                        affects instrument operation only when the oscilloscope requires multiple
                        acquisitions to build a complete waveform. The oscilloscope requires
                        multiple waveform acquisitions when it uses equivalent-time sampling or
                        when the Acquisition Type attribute is set to Envelope or Average.
                        
                        Note: Many scopes have a small, non-zero value as the minimum value for
                        this attribute. To configure the instrument to use the shortest trigger
                        hold-off, the user can specify a value of zero for this attribute.
                        
                        Therefore, the IVI Class-Compliant specific driver shall coerce any value
                        between zero and the minimum value to the minimum value. No other coercion
                        is allowed on this attribute.
                        """, cls, grp, '4.2.18'))
        self._add_property('trigger.level',
                        self._get_trigger_level,
                        self._set_trigger_level,
                        None,
                        ivi.Doc("""
                        Specifies the voltage threshold for the trigger sub-system. The units are
                        volts. This attribute affects instrument behavior only when the Trigger
                        Type is set to one of the following values: Edge Trigger, Glitch Trigger,
                        or Width Trigger.
                        
                        This attribute, along with the Trigger Slope, Trigger Source, and Trigger
                        Coupling attributes, defines the trigger event when the Trigger Type is
                        set to Edge Trigger.
                        """, cls, grp, '4.2.19'))
        self._add_property('trigger.edge.slope',
                        self._get_trigger_edge_slope,
                        self._set_trigger_edge_slope,
                        None,
                        ivi.Doc("""
                        Specifies whether a rising or a falling edge triggers the oscilloscope.
                        
                        This attribute affects instrument operation only when the Trigger Type
                        attribute is set to Edge Trigger.
                        
                        Values:
                         * 'positive'
                         * 'negative'
                        """, cls, grp, '4.2.20'))
        self._add_method('trigger.edge.configure',
                        self._trigger_edge_configure,
                        ivi.Doc("""
                        This function sets the edge triggering attributes. An edge trigger occurs
                        when the trigger signal that the end-user specifies with the Source
                        parameter passes through the voltage threshold that the end-user
                        specifies with the level parameter and has the slope that the end-user
                        specifies with the Slope parameter.
                        
                        This function affects instrument behavior only if the Trigger Type is Edge
                        Trigger. Set the Trigger Type and Trigger Coupling before calling this
                        function.
                        
                        If the trigger source is one of the analog input channels, an application
                        program should configure the vertical range, vertical offset, vertical
                        coupling, probe attenuation, and the maximum input frequency before
                        calling this function.
                        """, cls, grp, '4.3.9'))
        self._add_property('trigger.source',
                        self._get_trigger_source,
                        self._set_trigger_source,
                        None,
                        ivi.Doc("""
                        Specifies the source the oscilloscope monitors for the trigger event. The 
                        value can be a channel name alias, a driver-specific channel string, or
                        one of the values below.
                        
                        This attribute affects the instrument operation only when the Trigger Type
                        is set to one of the following values: Edge Trigger, TV Trigger, Runt
                        Trigger, Glitch Trigger, or Width Trigger.
                        """, cls, grp, '4.2.21'))
        self._add_property('trigger.type',
                        self._get_trigger_type,
                        self._set_trigger_type,
                        None,
                        ivi.Doc("""
                        Specifies the event that triggers the oscilloscope.
                        
                        Values:
                        
                        * 'edge'
                        * 'tv'
                        * 'runt'
                        * 'glitch'
                        * 'width'
                        * 'immediate'
                        * 'ac_line'
                        """, cls, grp, '4.2.22'))
        self._add_method('trigger.configure',
                        self._trigger_configure,
                        ivi.Doc("""
                        This function configures the common attributes of the trigger subsystem.
                        These attributes are the trigger type and trigger holdoff.
                        
                        When the end-user calls Read Waveform, Read Waveform Measurement, Read Min
                        Max Waveform, or Initiate Acquisition, the oscilloscope waits for a
                        trigger. The end-user specifies the type of trigger for which the
                        oscilloscope waits with the TriggerType parameter.
                        
                        If the oscilloscope requires multiple waveform acquisitions to build a
                        complete waveform, it waits for the length of time the end-user specifies
                        with the Holdoff parameter to elapse since the previous trigger. The
                        oscilloscope then waits for the next trigger. Once the oscilloscope
                        acquires a complete waveform, it returns to the idle state.
                        """, cls, grp, '4.3.10'))
        
        self._init_channels()
    
    
    
    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_enabled = list()
        self._channel_input_impedance = list()
        self._channel_input_frequency_max = list()
        self._channel_probe_attenuation = list()
        self._channel_coupling = list()
        self._channel_offset = list()
        self._channel_range = list()
        for i in range(self._channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_enabled.append(False)
            self._channel_input_impedance.append(1000000)
            self._channel_input_frequency_max.append(1e9)
            self._channel_probe_attenuation.append(1)
            self._channel_coupling.append('dc')
            self._channel_offset.append(0)
            self._channel_range.append(1)
        
        self.channels._set_list(self._channel_name)
    
    def _get_acquisition_start_time(self):
        return self._acquisition_start_time
    
    def _set_acquisition_start_time(self, value):
        value = float(value)
        self._acquisition_start_time = value
    
    def _get_acquisition_type(self):
        return self._acquisition_type
    
    def _set_acquisition_type(self, value):
        if value not in AcquisitionType:
            raise ivi.ValueNotSupportedException()
        self._acquisition_type = value
    
    def _get_acquisition_number_of_points_minimum(self):
        return self._acquisition_number_of_points_minimum
    
    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        self._acquisition_number_of_points_minimum = value
    
    def _get_acquisition_record_length(self):
        return self._acquisition_record_length
    
    def _get_acquisition_sample_rate(self):
        return self._get_acquisition_record_length() / self._get_acquisition_time_per_record()
    
    def _get_acquisition_time_per_record(self):
        return self._acquisition_time_per_record
    
    def _set_acquisition_time_per_record(self, value):
        value = float(value)
        self._acquisition_time_per_record = value
    
    def _get_channel_count(self):
        return self._channel_count
    
    def _get_channel_name(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_name[index]
    
    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_enabled[index]
    
    def _set_channel_enabled(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_enabled[index] = value
    
    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_input_impedance[index]
    
    def _set_channel_input_impedance(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_input_impedance[index] = value
    
    def _get_channel_input_frequency_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_input_frequency_max[index]
    
    def _set_channel_input_frequency_max(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_input_frequency_max[index] = value
    
    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_probe_attenuation[index]
    
    def _set_channel_probe_attenuation(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_probe_attenuation[index] = value
    
    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_coupling[index]
    
    def _set_channel_coupling(self, index, value):
        if value not in VerticalCoupling:
            raise ivi.ValueNotSupportedException()
        index = ivi.get_index(self._channel_name, index)
        self._channel_coupling[index] = value
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_offset[index] = value
    
    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range[index]
    
    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_range[index] = value
    
    def _get_measurement_status(self):
        return self._measurement_status
    
    def _get_trigger_coupling(self):
        return self._trigger_coupling
    
    def _set_trigger_coupling(self, value):
        if value not in TriggerCoupling:
            raise ivi.ValueNotSupportedException()
        self._trigger_coupling = value
    
    def _get_trigger_holdoff(self):
        return self._trigger_holdoff
    
    def _set_trigger_holdoff(self, value):
        value = float(value)
        self._trigger_holdoff = value
    
    def _get_trigger_level(self):
        return self._trigger_level
    
    def _set_trigger_level(self, value):
        value = float(value)
        self._trigger_level = value
    
    def _get_trigger_edge_slope(self):
        return self._trigger_edge_slope
    
    def _set_trigger_edge_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_edge_slope = value
    
    def _get_trigger_source(self):
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        self._trigger_source = value
    
    def _get_trigger_type(self):
        return self._trigger_type
    
    def _set_trigger_type(self, value):
        if value not in Trigger:
            raise ivi.ValueNotSupportedException()
        self._trigger_type = value
    
    def _measurement_abort(self):
        pass
    
    def _acquisition_configure_record(self, time_per_record, minimum_number_of_points, acquisition_start_time):
        self._set_acquisition_time_per_record(time_per_record)
        self._set_acquisition_number_of_points_minimum(minimum_number_of_points)
        self._set_acquisition_start_time(acquisition_start_time)
    
    def _channel_configure(self, index, range, offset, coupling, probe_attenuation, enabled):
        self._set_channel_range(index, range)
        self._set_channel_offset(index, offset)
        self._set_channel_coupling(index, coupling)
        self._set_channel_probe_attenuation(index, probe_attenuation)
        self._set_channel_enabled(index, enabled)
    
    def _channel_configure_characteristics(self, index, input_impedance, input_frequency_maximum):
        self._set_channel_input_impedance(index, input_impedance)
        self._set_channel_input_frequency_max(index, input_frequency_maximum)
    
    def _trigger_edge_configure(self, source, level, slope):
        self._set_trigger_source(source)
        self._set_trigger_level(level)
        self._set_trigger_edge_slope(slope)
    
    def _trigger_configure(self, type, holdoff):
        self._set_trigger_type(type)
        self._set_trigger_holdoff(holdoff)
    
    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)
        data = list()
        return data
    
    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)
    
    def _measurement_initiate(self):
        pass


class Interpolation(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting interpolation"
    
    def __init__(self, *args, **kwargs):
        super(Interpolation, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'Interpolation'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_interpolation = 'none'
        
        self._add_property('acquisition.interpolation',
                        self._get_acquisition_interpolation,
                        self._set_acquisition_interpolation,
                        None,
                        ivi.Doc("""
                        Specifies the interpolation method the oscilloscope uses when it cannot
                        resolve a voltage for every point in the waveform record.
                        
                        Values:
                        * 'none'
                        * 'sinex'
                        * 'linear'
                        """, cls, grp, '5.2.1'))
    
    def _get_acquisition_interpolation(self):
        return self._acquisition_interpolation
    
    def _set_acquisition_interpolation(self, value):
        self._acquisition_interpolation = value


class TVTrigger(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting TV triggering"
    
    def __init__(self, *args, **kwargs):
        super(TVTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'TVTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_tv_trigger_event = 'any_line'
        self._trigger_tv_line_number = 0
        self._trigger_tv_polarity = 'positive'
        self._trigger_tv_signal_format = 'ntsc'
        
        self._add_property('trigger.tv.trigger_event',
                        self._get_trigger_tv_trigger_event,
                        self._set_trigger_tv_trigger_event,
                        None,
                        ivi.Doc("""
                        Specifies the event on which the oscilloscope triggers.
                        
                        Values:
                        * 'field1'
                        * 'field2'
                        * 'any_field'
                        * 'any_line'
                        * 'line_number'
                        """, cls, grp, '6.2.1'))
        self._add_property('trigger.tv.line_number',
                        self._get_trigger_tv_line_number,
                        self._set_trigger_tv_line_number,
                        None,
                        ivi.Doc("""
                        Specifies the line on which the oscilloscope triggers. The driver uses
                        this attribute when the TV Trigger Event is set to TV Event Line Number.
                        The line number setting is independent of the field. This means that to
                        trigger on the first line of the second field, the user must configure
                        the line number to the value of 263 (if we presume that field one had 262
                        lines).
                        """, cls, grp, '6.2.2'))
        self._add_property('trigger.tv.polarity',
                        self._get_trigger_tv_polarity,
                        self._set_trigger_tv_polarity,
                        None,
                        ivi.Doc("""
                        Specifies the polarity of the TV signal.
                        
                        Values:
                        * 'positive'
                        * 'negative'
                        """, cls, grp, '6.2.3'))
        self._add_property('trigger.tv.signal_format',
                        self._get_trigger_tv_signal_format,
                        self._set_trigger_tv_signal_format,
                        None,
                        ivi.Doc("""
                        Specifies the format of TV signal on which the oscilloscope triggers.
                        
                        Values:
                        * 'ntsc'
                        * 'pal'
                        * 'secam'
                        """, cls, grp, '6.2.4'))
        self._add_method('trigger.tv.configure',
                        self._trigger_tv_configure,
                        ivi.Doc("""
                        This function configures the oscilloscope for TV triggering. It configures
                        the TV signal format, the event and the signal polarity.
                        
                        This function affects instrument behavior only if the trigger type is TV
                        Trigger. Set the Trigger Type and Trigger Coupling before calling this
                        function.
                        """, cls, grp, '6.3.2'))
    
    def _get_trigger_tv_trigger_event(self):
        return self._trigger_tv_trigger_event
    
    def _set_trigger_tv_trigger_event(self, value):
        if value not in TVTriggerEvent:
            raise ivi.ValueNotSupportedException()
        self._trigger_tv_trigger_event = value
    
    def _get_trigger_tv_line_number(self):
        return self._trigger_tv_line_number
    
    def _set_trigger_tv_line_number(self, value):
        self._trigger_tv_line_number = value
    
    def _get_trigger_tv_polarity(self):
        return self._trigger_tv_polarity
    
    def _set_trigger_tv_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_tv_polarity = value
    
    def _get_trigger_tv_signal_format(self):
        return self._trigger_tv_signal_format
    
    def _set_trigger_tv_signal_format(self, value):
        if value not in TVTriggerFormat:
            raise ivi.ValueNotSupportedException()
        self._trigger_tv_signal_format = value
    
    def _trigger_tv_configure(self, source, signal_format, event, polarity):
        self._set_trigger_source(source)
        self._set_trigger_tv_signal_format(signal_format)
        self._set_trigger_tv_trigger_event(event)
        self._set_trigger_tv_polarity(polarity)


class RuntTrigger(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting runt triggering"
    
    def __init__(self, *args, **kwargs):
        super(RuntTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'RuntTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_runt_threshold_high = 0
        self._trigger_runt_threshold_low = 0
        self._trigger_runt_polarity = 'positive'
        
        self._add_property('trigger.runt.threshold_high',
                        self._get_trigger_runt_threshold_high,
                        self._set_trigger_runt_threshold_high,
                        None,
                        ivi.Doc("""
                        Specifies the high threshold the oscilloscope uses for runt triggering.
                        The units are volts.
                        """, cls, grp, '7.2.1'))
        self._add_property('trigger.runt.threshold_low',
                        self._get_trigger_runt_threshold_low,
                        self._set_trigger_runt_threshold_low,
                        None,
                        ivi.Doc("""
                        Specifies the low threshold the oscilloscope uses for runt triggering.
                        The units are volts.
                        """, cls, grp, '7.2.2'))
        self._add_property('trigger.runt.polarity',
                        self._get_trigger_runt_polarity,
                        self._set_trigger_runt_polarity,
                        None,
                        ivi.Doc("""
                        Specifies the polarity of the runt that triggers the oscilloscope.
                        
                        Values:
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """, cls, grp, '7.2.3'))
        self._add_method('trigger.runt.configure',
                        self._trigger_runt_configure,
                        ivi.Doc("""
                        This function configures the runt trigger. A runt trigger occurs when the
                        trigger signal crosses one of the runt thresholds twice without crossing
                        the other runt threshold. The end-user specifies the runt thresholds with
                        the RuntLowThreshold and RuntHighThreshold parameters. The end-user
                        specifies the polarity of the runt with the RuntPolarity parameter.
                        
                        This function affects instrument behavior only if the trigger type is Runt
                        Trigger. Set the trigger type and trigger coupling before calling this
                        function.
                        """, cls, grp, '7.3.1'))
    
    def _get_trigger_runt_threshold_high(self):
        return self._trigger_runt_threshold_high
    
    def _set_trigger_runt_threshold_high(self, value):
        value = float(value)
        self._trigger_runt_threshold_high = value
    
    def _get_trigger_runt_threshold_low(self):
        return self._trigger_runt_threshold_low
    
    def _set_trigger_runt_threshold_low(self, value):
        value = float(value)
        self._trigger_runt_threshold_low = value
    
    def _get_trigger_runt_polarity(self):
        return self._trigger_runt_polarity
    
    def _set_trigger_runt_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_runt_polarity = value
    
    def _trigger_runt_configure(self, source, threshold_high, threshold_low, polarity):
        self._set_trigger_source(source)
        self._set_trigger_runt_threshold_high(threshold_high)
        self._set_trigger_runt_threshold_low(threshold_low)
        self._set_trigger_runt_polarity(polarity)


class GlitchTrigger(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting glitch triggering"
    
    def __init__(self, *args, **kwargs):
        super(GlitchTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'GlitchTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_glitch_condition = 'less_than'
        self._trigger_glitch_polarity = 'positive'
        self._trigger_glitch_width = 0
        
        self._add_property('trigger.glitch.condition',
                        self._get_trigger_glitch_condition,
                        self._set_trigger_glitch_condition,
                        None,
                        ivi.Doc("""
                        Specifies the glitch condition. This attribute determines whether the
                        glitch trigger happens when the oscilloscope detects a pulse with a
                        width less than or greater than the width value.
                        
                        Values:
                        * 'greater_than'
                        * 'less_than'
                        """, cls, grp, '8.2.1'))
        self._add_property('trigger.glitch.polarity',
                        self._get_trigger_glitch_polarity,
                        self._set_trigger_glitch_polarity,
                        None,
                        ivi.Doc("""
                        Specifies the polarity of the glitch that triggers the oscilloscope.
                        
                        Values:
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """, cls, grp, '8.2.2'))
        self._add_property('trigger.glitch.width',
                        self._get_trigger_glitch_width,
                        self._set_trigger_glitch_width,
                        None,
                        ivi.Doc("""
                        Specifies the glitch width. The units are seconds. The oscilloscope
                        triggers when it detects a pulse with a width less than or greater than
                        this value, depending on the Glitch Condition attribute.
                        """, cls, grp, '8.2.3'))
        self._add_method('trigger.glitch.configure',
                        self._trigger_glitch_configure,
                        ivi.Doc("""
                        This function configures the glitch trigger. A glitch trigger occurs when
                        the trigger signal has a pulse with a width that is less than or greater
                        than the glitch width. The end user specifies which comparison criterion
                        to use with the GlitchCondition parameter. The end-user specifies the
                        glitch width with the GlitchWidth parameter. The end-user specifies the
                        polarity of the pulse with the GlitchPolarity parameter. The trigger does
                        not actually occur until the edge of a pulse that corresponds to the
                        GlitchWidth and GlitchPolarity crosses the threshold the end-user
                        specifies in the TriggerLevel parameter.
                        
                        This function affects instrument behavior only if the trigger type is
                        Glitch Trigger. Set the trigger type and trigger coupling before calling
                        this function.
                        """, cls, grp, '8.3.1'))
    
    def _get_trigger_glitch_condition(self):
        return self._trigger_glitch_condition
    
    def _set_trigger_glitch_condition(self, value):
        if value not in GlitchCondition:
            raise ivi.ValueNotSupportedException()
        self._trigger_glitch_condition = value
    
    def _get_trigger_glitch_polarity(self):
        return self._trigger_glitch_polarity
    
    def _set_trigger_glitch_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_glitch_polarity = value
    
    def _get_trigger_glitch_width(self):
        return self._trigger_glitch_width
    
    def _set_trigger_glitch_width(self, value):
        value = float(value)
        self._trigger_glitch_width = value
    
    def _trigger_glitch_configure(self, source, level, width, polarity, condition):
        self._set_trigger_source(source)
        self._set_trigger_level(level)
        self._set_trigger_glitch_width(width)
        self._set_trigger_glitch_polarity(polarity)
        self._set_trigger_glitch_condition(condition)


class WidthTrigger(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting width triggering"
    
    def __init__(self, *args, **kwargs):
        super(WidthTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'WidthTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_width_condition = 'within'
        self._trigger_width_threshold_high = 0
        self._trigger_width_threshold_low = 0
        self._trigger_width_polarity = 'positive'
        
        self._add_property('trigger.width.condition',
                        self._get_trigger_width_condition,
                        self._set_trigger_width_condition,
                        None,
                        ivi.Doc("""
                        Specifies whether a pulse that is within or outside the high and low
                        thresholds triggers the oscilloscope. The end-user specifies the high and
                        low thresholds with the Width High Threshold and Width Low Threshold
                        attributes.
                        
                        Values:
                        * 'within'
                        * 'outside'
                        """, cls, grp, '9.2.1'))
        self._add_property('trigger.width.threshold_high',
                        self._get_trigger_width_threshold_high,
                        self._set_trigger_width_threshold_high,
                        None,
                        ivi.Doc("""
                        Specifies the high width threshold time. Units are seconds.
                        """, cls, grp, '9.2.2'))
        self._add_property('trigger.width.threshold_low',
                        self._get_trigger_width_threshold_low,
                        self._set_trigger_width_threshold_low,
                        None,
                        ivi.Doc("""
                        Specifies the low width threshold time. Units are seconds.
                        """, cls, grp, '9.2.3'))
        self._add_property('trigger.width.polarity',
                        self._get_trigger_width_polarity,
                        self._set_trigger_width_polarity,
                        None,
                        ivi.Doc("""
                        Specifies the polarity of the pulse that triggers the oscilloscope.
                        
                        Values:
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """, cls, grp, '9.2.4'))
        self._add_method('trigger.width.configure',
                        self._trigger_width_configure,
                        ivi.Doc("""
                        This function configures the width trigger. A width trigger occurs when
                        the oscilloscope detects a positive or negative pulse with a width
                        between, or optionally outside, the width thresholds. The end-user
                        specifies the width thresholds with the WidthLowThreshold and
                        WidthHighThreshold parameters. The end-user specifies whether the
                        oscilloscope triggers on pulse widths that are within or outside the width
                        thresholds with the WidthCondition parameter. The end-user specifies the
                        polarity of the pulse with the WidthPolarity parameter. The trigger does
                        not actually occur until the edge of a pulse that corresponds to the
                        WidthLowThreshold, WidthHighThreshold, WidthCondition, and WidthPolarity
                        crosses the threshold the end-user specifies with the TriggerLevel
                        parameter.
                        
                        This function affects instrument behavior only if the trigger type is
                        Width Trigger. Set the trigger type and trigger coupling before calling
                        this function.
                        """, cls, grp, '9.3.1'))
    
    def _get_trigger_width_condition(self):
        return self._trigger_width_condition
    
    def _set_trigger_width_condition(self, value):
        if value not in WidthCondition:
            raise ivi.ValueNotSupportedException()
        self._trigger_width_condition = value
    
    def _get_trigger_width_threshold_high(self):
        return self._trigger_width_threshold_high
    
    def _set_trigger_width_threshold_high(self, value):
        value = float(value)
        self._trigger_width_threshold_high = value
    
    def _get_trigger_width_threshold_low(self):
        return self._trigger_width_threshold_low
    
    def _set_trigger_width_threshold_low(self, value):
        value = float(value)
        self._trigger_width_threshold_low = value
    
    def _get_trigger_width_polarity(self):
        return self._trigger_width_polarity
    
    def _set_trigger_width_polarity(self, value):
        if value not in Polarity:
            raise ivi.ValueNotSupportedException()
        self._trigger_width_polarity = value
    
    def _trigger_width_configure(self, source, level, threshold_low, threshold_high, polarity, condition):
        self._set_trigger_source(source)
        self._set_trigger_level(level)
        self._set_trigger_width_threshold_low(threshold_low)
        self._set_trigger_width_threshold_high(threshold_high)
        self._set_trigger_width_polarity(polarity)
        self._set_trigger_width_condition(condition)


class AcLineTrigger(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting AC line triggering"
    
    def __init__(self, *args, **kwargs):
        super(AcLineTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'AcLineTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_ac_line_slope = 'positive'
        
        self._add_property('trigger.ac_line.slope',
                        self._get_trigger_ac_line_slope,
                        self._set_trigger_ac_line_slope,
                        None,
                        ivi.Doc("""
                        Specifies the slope of the zero crossing upon which the scope triggers.
                        
                        Values:
                        * 'positive'
                        * 'negative'
                        * 'either'
                        """, cls, grp, '10.2.1'))
    
    def _get_trigger_ac_line_slope(self):
        return self._trigger_ac_line_slope
    
    def _set_trigger_ac_line_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_ac_line_slope = value
    

class WaveformMeasurement(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting waveform measurements"
    
    def __init__(self, *args, **kwargs):
        super(WaveformMeasurement, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'WaveformMeasurement'
        ivi.add_group_capability(self, cls+grp)
        
        self._reference_level_high = 90
        self._reference_level_low = 10
        self._reference_level_middle = 50
        
        self._add_property('reference_level.high',
                        self._get_reference_level_high,
                        self._set_reference_level_high,
                        None,
                        ivi.Doc("""
                        Specifies the high reference the oscilloscope uses for waveform
                        measurements. The value is a percentage of the difference between the
                        Voltage High and Voltage Low.
                        """, cls, grp, '11.2.1'))
        self._add_property('reference_level.middle',
                        self._get_reference_level_middle,
                        self._set_reference_level_middle,
                        None,
                        ivi.Doc("""
                        Specifies the middle reference the oscilloscope uses for waveform
                        measurements. The value is a percentage of the difference between the
                        Voltage High and Voltage Low.
                        """, cls, grp, '11.2.3'))
        self._add_property('reference_level.low',
                        self._get_reference_level_low,
                        self._set_reference_level_low,
                        None,
                        ivi.Doc("""
                        Specifies the low reference the oscilloscope uses for waveform
                        measurements. The value is a percentage of the difference between the
                        Voltage High and Voltage Low.
                        """, cls, grp, '11.2.2'))
        self._add_method('reference_level.configure',
                        self._reference_level_configure,
                        ivi.Doc("""
                        This function configures the reference levels for waveform measurements.
                        Call this function before calling the Read Waveform Measurement or Fetch
                        Waveform Measurement to take waveform measurements.
                        """, cls, grp, '11.3.1'))
        self._add_method('channels[].measurement.fetch_waveform_measurement',
                        self._measurement_fetch_waveform_measurement,
                        ivi.Doc("""
                        This function fetches a specified waveform measurement from a specific
                        channel from a previously initiated waveform acquisition. If the channel
                        is not enabled for the acquisition, this function returns the Channel Not
                        Enabled error.
                        
                        This function obtains a waveform measurement and returns the measurement
                        value. The end-user specifies a particular measurement type, such as rise
                        time, frequency, and voltage peak-to-peak. The waveform on which the
                        oscilloscope calculates the waveform measurement is from an acquisition
                        that was previously initiated.
                        
                        Use the Initiate Acquisition function to start an acquisition on the
                        channels that were enabled with the Configure Channel function. The
                        oscilloscope acquires waveforms for the enabled channels concurrently. Use
                        the Acquisition Status function to determine when the acquisition is
                        complete. Call this function separately for each waveform measurement on a
                        specific channel.
                        
                        The end-user can call the Read Waveform Measurement function instead of
                        the Initiate Acquisition function. The Read Waveform Measurement function
                        starts an acquisition on all enabled channels. It then waits for the
                        acquisition to complete, obtains a waveform measurement on the specified
                        channel, and returns the measurement value. Call this function separately
                        to obtain any other waveform measurements on a specific channel.
                        
                        Configure the appropriate reference levels before calling this function to
                        take a rise time, fall time, width negative, width positive, duty cycle
                        negative, or duty cycle positive measurement.
                        
                        The end-user can configure the low, mid, and high references either by
                        calling the Configure Reference Levels function or by setting the
                        following attributes.
                        
                        * Measurement High Reference
                        * Measurement Low Reference
                        * Measurement Mid Reference
                        
                        This function does not check the instrument status. Typically, the
                        end-user calls this function only in a sequence of calls to other
                        low-level driver functions. The sequence performs one operation. The
                        end-user uses the low-level functions to optimize one or more aspects of
                        interaction with the instrument. Call the Error Query function at the
                        conclusion of the sequence to check the instrument status.
                        
                        Values for measurement_function:
                        * 'rise_time'
                        * 'fall_time'
                        * 'frequency'
                        * 'period'
                        * 'voltage_rms'
                        * 'voltage_peak_to_peak'
                        * 'voltage_max'
                        * 'voltage_min'
                        * 'voltage_high'
                        * 'voltage_low'
                        * 'voltage_average'
                        * 'width_negative'
                        * 'width_positive'
                        * 'duty_cycle_negative'
                        * 'duty_cycle_positive'
                        * 'amplitude'
                        * 'voltage_cycle_rms'
                        * 'voltage_cycle_average'
                        * 'overshoot'
                        * 'preshoot'
                        """, cls, grp, '11.3.2'))
        self._add_method('channels[].measurement.read_waveform_measurement',
                        self._measurement_read_waveform_measurement,
                        ivi.Doc("""
                        This function initiates a new waveform acquisition and returns a specified
                        waveform measurement from a specific channel.
                        
                        This function initiates an acquisition on the channels that the end-user
                        enables with the Configure Channel function. If the channel is not enabled
                        for the acquisition, this function returns Channel Not Enabled error. It
                        then waits for the acquisition to complete, obtains a waveform measurement
                        on the channel the end-user specifies, and returns the measurement value.
                        The end-user specifies a particular measurement type, such as rise time,
                        frequency, and voltage peak-to-peak.
                        
                        If the oscilloscope did not complete the acquisition within the time
                        period the user specified with the MaxTimeMilliseconds parameter, the
                        function returns the Max Time Exceeded error.
                        
                        The end-user can call the Fetch Waveform Measurement function separately
                        to obtain any other waveform measurement on a specific channel without
                        initiating another acquisition.
                        
                        The end-user must configure the appropriate reference levels before
                        calling this function. Configure the low, mid, and high references either
                        by calling the Configure Reference Levels function or by setting the
                        following attributes.
                        following attributes.
                        
                        * Measurement High Reference
                        * Measurement Low Reference
                        * Measurement Mid Reference
                        """, cls, grp, '11.3.3'))
    
    def _get_reference_level_high(self):
        return self._reference_level_high
    
    def _set_reference_level_high(self, value):
        value = float(value)
        self._reference_level_high = value
    
    def _get_reference_level_low(self):
        return self._reference_level_low
    
    def _set_reference_level_low(self, value):
        value = float(value)
        self._reference_level_low = value
    
    def _get_reference_level_middle(self):
        return self._reference_level_middle
    
    def _set_reference_level_middle(self, value):
        value = float(value)
        self._reference_level_middle = value
    
    def _reference_level_configure(self, low, middle, high):
        self._set_reference_level_low(low)
        self._set_reference_level_middle(middle)
        self._set_reference_level_high(high)
    
    def _measurement_fetch_waveform_measurement(self, index, measurement_function):
        index = ivi.get_index(self._channel_name, index)
        if measurement_function not in MeasurementFunction:
            raise ivi.ValueNotSupportedException()
        return 0
    
    def _measurement_read_waveform_measurement(self, index, measurement_function, maximum_time):
        return self._measurement_fetch_waveform_measurement(index, measurement_function)


class MinMaxWaveform(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting minimum and maximum waveform acquisition"
    
    def __init__(self, *args, **kwargs):
        super(MinMaxWaveform, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'MinMaxWaveform'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_number_of_envelopes = 0
        
        self._add_property('acquisition.number_of_envelopes',
                        self._get_acquisition_number_of_envelopes,
                        self._set_acquisition_number_of_envelopes,
                        None,
                        ivi.Doc("""
                        When the end-user sets the Acquisition Type attribute to Envelope, the
                        oscilloscope acquires multiple waveforms. After each waveform acquisition,
                        the oscilloscope keeps the minimum and maximum values it finds for each
                        point in the waveform record. This attribute specifies the number of
                        waveforms the oscilloscope acquires and analyzes to create the minimum and
                        maximum waveforms. After the oscilloscope acquires as many waveforms as
                        this attribute specifies, it returns to the idle state. This attribute
                        affects instrument operation only when the Acquisition Type attribute is
                        set to Envelope.
                        """, cls, grp, '12.2.1'))
        self._add_method('channels[].measurement.fetch_waveform_min_max',
                        self._measurement_fetch_waveform_min_max,
                        ivi.Doc("""
                        This function returns the minimum and maximum waveforms that the
                        oscilloscope acquires for the specified channel. If the channel is not
                        enabled for the acquisition, this function returns the Channel Not Enabled
                        error.
                        
                        The waveforms are from a previously initiated acquisition. Use this
                        function to fetch waveforms when the acquisition type is set to Peak
                        Detect or Envelope. If the acquisition type is not one of the listed
                        types, the function returns the Invalid Acquisition Type error.
                        
                        Use the Initiate Acquisition function to start an acquisition on the
                        enabled channels. The oscilloscope acquires the min/max waveforms for the
                        enabled channels concurrently. Use the Acquisition Status function to
                        determine when the acquisition is complete. The end-user must call this
                        function separately for each enabled channel to obtain the min/max
                        waveforms.
                        
                        The end-user can call the Read Min Max Waveform function instead of the
                        Initiate Acquisition function. The Read Min Max Waveform function starts
                        an acquisition on all enabled channels, waits for the acquisition to
                        complete, and returns the min/max waveforms for the specified channel. You
                        call this function to obtain the min/max waveforms for each of the
                        remaining channels.
                        
                        After this function executes, each element in the MinWaveform and
                        MaxWaveform parameters is either a voltage or a value indicating that the
                        oscilloscope could not sample a voltage.
                        
                        The return value is a list of (x, y_min, y_max) tuples that represent the
                        time and voltage of each data point.  Either of the y points may be NaN in
                        the case that the oscilloscope could not sample the voltage.
                        
                        The end-user configures the interpolation method the oscilloscope uses
                        with the Acquisition.Interpolation property. If interpolation is disabled,
                        the oscilloscope does not interpolate points in the waveform. If the
                        oscilloscope cannot sample a value for a point in the waveform, the driver
                        sets the corresponding element in the waveformArray to an IEEE-defined NaN
                        (Not a Number) value. Check for this value with math.isnan() or
                        numpy.isnan(). Check an entire array with
                        
                        any(any(math.isnan(b) for b in a) for a in waveform)
                        
                        This function does not check the instrument status. Typically, the
                        end-user calls this function only in a sequence of calls to other
                        low-level driver functions. The sequence performs one operation. The
                        end-user uses the low-level functions to optimize one or more aspects of
                        interaction with the instrument. Call the Error Query function at the
                        conclusion of the sequence to check the instrument status.
                        """, cls, grp, '12.3.2'))
        self._add_method('channels[].measurement.read_waveform_min_max',
                        self._measurement_read_waveform_min_max,
                        ivi.Doc("""
                        This function initiates new waveform acquisition and returns minimum and
                        maximum waveforms from a specific channel. If the channel is not enabled
                        for the acquisition, this function returns the Channel Not Enabled error.
                        
                        This function is used when the Acquisition Type is Peak Detect or
                        Envelope. If the acquisition type is not one of the listed types, the
                        function returns the Invalid Acquisition Type error.
                        
                        This function initiates an acquisition on the enabled channels. It then
                        waits for the acquisition to complete, and returns the min/max waveforms
                        for the specified channel. Call the Fetch Min Max Waveform function to
                        obtain the min/max waveforms for each of the remaining enabled channels
                        without initiating another acquisition. If the oscilloscope did not
                        complete the acquisition within the time period the user specified with
                        the max_time parameter, the function returns the Max Time Exceeded error.
                        
                        The return value is a list of (x, y_min, y_max) tuples that represent the
                        time and voltage of each data point.  Either of the y points may be NaN in
                        the case that the oscilloscope could not sample the voltage.
                        
                        The end-user configures the interpolation method the oscilloscope uses
                        with the Acquisition.Interpolation property. If interpolation is disabled,
                        the oscilloscope does not interpolate points in the waveform. If the
                        oscilloscope cannot sample a value for a point in the waveform, the driver
                        sets the corresponding element in the waveformArray to an IEEE-defined NaN
                        (Not a Number) value. Check for this value with math.isnan() or
                        numpy.isnan(). Check an entire array with
                        
                        any(any(math.isnan(b) for b in a) for a in waveform)
                        
                        This function does not check the instrument status. Typically, the
                        end-user calls this function only in a sequence of calls to other
                        low-level driver functions. The sequence performs one operation. The
                        end-user uses the low-level functions to optimize one or more aspects of
                        interaction with the instrument. Call the Error Query function at the
                        conclusion of the sequence to check the instrument status.
                        """, cls, grp, '12.3.3'))
    
    def _get_acquisition_number_of_envelopes(self):
        return self._acquisition_number_of_envelopes
    
    def _set_acquisition_number_of_envelopes(self, value):
        self._acquisition_number_of_envelopes = value
    
    def _measurement_fetch_waveform_min_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        data = list()
        return data
    
    def _measurement_read_waveform_min_max(self, index, maximum_time):
        return _measurement_fetch_waveform_min_max(index)


class ProbeAutoSense(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting probe attenuation sensing"
    def __init__(self, *args, **kwargs):
        super(ProbeAutoSense, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'ProbeAutoSense'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_probe_attenuation_auto = list()
        
        self._add_property('channels[].probe_attenuation_auto',
                        self._get_channel_probe_attenuation_auto,
                        self._set_channel_probe_attenuation_auto,
                        None,
                        ivi.Doc("""
                        If this attribute is True, the driver configures the oscilloscope to sense
                        the attenuation of the probe automatically.
                        
                        If this attribute is False, the driver disables the automatic probe sense
                        and configures the oscilloscope to use the value of the Probe Attenuation
                        attribute.
                        
                        The actual probe attenuation the oscilloscope is currently using can be
                        determined from the Probe Attenuation attribute.
                        
                        Setting the Probe Attenuation attribute also sets the Probe Attenuation
                        Auto attribute to false.
                        """, cls, grp, '13.2.1'))
    
    def init_channels(self):
        try:
            super(ProbeAutoSense, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_probe_attenuation_auto = list()
        for i in range(self._channel_count):
            self._channel_probe_attenuation_auto.append(True)
    
    def _get_channel_probe_attenuation_auto(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_probe_attenuation_auto[index]
    
    def _set_channel_probe_attenuation_auto(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        self._channel_probe_attenuation_auto[index] = value


class ContinuousAcquisition(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting continuous acquisition"
    
    def __init__(self, *args, **kwargs):
        super(ContinuousAcquisition, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'ContinuousAcquisition'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_continuous = False
        
        self._add_property('trigger.continuous',
                        self._get_trigger_continuous,
                        self._set_trigger_continuous,
                        None,
                        ivi.Doc("""
                        Specifies whether the oscilloscope continuously initiates waveform
                        acquisition. If the end-user sets this attribute to True, the oscilloscope
                        immediately waits for another trigger after the previous waveform
                        acquisition is complete. Setting this attribute to True is useful when the
                        end-user requires continuous updates of the oscilloscope display. This
                        specification does not define the behavior of the read waveform and fetch
                        waveform functions when this attribute is set to True. The behavior of
                        these functions is instrument specific.
                        """, cls, grp, '14.2.1'))
    
    def _get_trigger_continuous(self):
        return self._trigger_continuous
    
    def _set_trigger_continuous(self, value):
        self._trigger_continuous = value


class AverageAcquisition(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting average acquisition"
    
    def __init__(self, *args, **kwargs):
        super(AverageAcquisition, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'AverageAcquisition'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_number_of_averages = 1
        
        self._add_property('acquisition.number_of_averages',
                        self._get_acquisition_number_of_averages,
                        self._set_acquisition_number_of_averages,
                        None,
                        ivi.Doc("""
                        Specifies the number of waveform the oscilloscope acquires and averages.
                        After the oscilloscope acquires as many waveforms as this attribute
                        specifies, it returns to the idle state. This attribute affects instrument
                        behavior only when the Acquisition Type attribute is set to Average.
                        """, cls, grp, '15.2.1'))
    
    def _get_acquisition_number_of_averages(self):
        return self._acquisition_number_of_averages
    
    def _set_acquisition_number_of_averages(self, value):
        self._acquisition_number_of_averages = value


class SampleMode(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting equivalent and real time acquisition"
    
    def __init__(self, *args, **kwargs):
        super(SampleMode, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'SampleMode'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_sample_mode = 'real_time'
        
        self._add_property('acquisition.sample_mode',
                        self._get_acquisition_sample_mode,
                        self._set_acquisition_sample_mode,
                        None,
                        ivi.Doc("""
                        Returns the sample mode the oscilloscope is currently using.
                        
                        Values:
                        * 'real_time'
                        * 'equivalent_time'
                        """, cls, grp, '16.2.1'))
    
    def _get_acquisition_sample_mode(self):
        return self._acquisition_sample_mode
    
    def _set_acquisition_sample_mode(self, value):
        if value not in AcquisitionSampleMode:
            raise ivi.ValueNotSupportedException()
        self._acquisition_sample_mode = value


class TriggerModifier(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting specific triggering subsystem behavior in the absence of a trigger"
    
    def __init__(self, *args, **kwargs):
        super(TriggerModifier, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'TriggerModifier'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_modifier = 'none'
        
        self._add_property('trigger.modifier',
                        self._get_trigger_modifier,
                        self._set_trigger_modifier,
                        None,
                        ivi.Doc("""
                        Specifies the trigger modifier. The trigger modifier determines the
                        oscilloscope's behavior in the absence of the configured trigger.
                        
                        Values:
                        * 'none'
                        * 'auto'
                        * 'auto_level'
                        """, cls, grp, '17.2.1'))
    
    def _get_trigger_modifier(self):
        return self._trigger_modifier
    
    def _set_trigger_modifier(self, value):
        if value not in TriggerModifier:
            raise ivi.ValueNotSupportedException()
        self._trigger_modifier = value


class AutoSetup(ivi.IviContainer):
    "Extension IVI methods for oscilloscopes supporting automatic setup"
    
    def __init__(self, *args, **kwargs):
        super(AutoSetup, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'AutoSetup'
        ivi.add_group_capability(self, cls+grp)
        
        self._add_method('measurement.auto_setup',
                        self._measurement_auto_setup,
                        ivi.Doc("""
                        This function performs an auto-setup on the instrument.
                        """, cls, grp, '18.2.1'))
    
    def _measurement_auto_setup(self):
        pass

