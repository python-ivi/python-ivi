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

# Parameter Values
Coupling = set(['ac', 'dc'])
Slope = set(['negative', 'positive'])
MeasurementFunction = set(['frequency', 'frequency_with_aperture', 'period',
                           'period_with_aperture', 'pulse_width', 'duty_cycle',
                           'edge_time', 'frequency_ratio', 'time_interval',
                           'phase', 'totalize_continuous', 'totalize_gated',
                           'totalize_timed', 'dc_voltage', 'maximum_voltage',
                           'minimum_voltage', 'rms_voltage', 'peak_to_peak_voltage'])
ArmType = set(['immediate', 'external'])
ReferenceType = set(['voltage', 'percent'])
MeasurementStatus = set(['complete', 'in_progress', 'unknown'])

class Base(object):
    "Base IVI methods for all frequency counters"
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__( *args, **kwargs)
        
        cls = 'IviCounter'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._measurement_function = 'frequency'
        self._channel_name = list()
        self._channel_impedance = list()
        self._channel_coupling = list()
        self._channel_attenuation = list()
        self._channel_level = list()
        self._channel_hysteresis = list()
        self._channel_slope = list()
        self._channel_filter_enabled = list()
        self._channel_count = 1
        self._frequency_channel = 0
        self._frequency_estimate = 1000.0
        self._frequency_resolution = 1.0
        self._frequency_aperture_time = 1.0
        self._frequency_estimate_auto = True
        self._frequency_resolution_auto = True
        self._period_channel = 0
        self._period_estimate = 1.0
        self._period_resolution = 1e-6
        self._period_aperture_time = 1.0
        self._pulse_width_channel = 0
        self._pulse_width_estimate = 1.0
        self._pulse_width_resolution = 1e-6
        self._duty_cycle_channel = 0
        self._duty_cycle_frequency_estimate = 1000.0
        self._duty_cycle_resolution = 0.01
        self._edge_time_channel = 0
        self._edge_time_reference_type = 'voltage'
        self._edge_time_estimate = 1e-3
        self._edge_time_resolution = 1e-6
        self._edge_time_high_reference = 4.0
        self._edge_time_low_reference = 1.0
        self._frequency_ratio_numerator_channel = 0
        self._frequency_ratio_denominator_channel = 0
        self._frequency_ratio_numerator_frequency_estimate = 1000.0
        self._frequency_ratio_estimate = 10.0
        self._frequency_ratio_resolution = 0.01
        self._time_interval_start_channel = 0
        self._time_interval_stop_channel = 0
        self._time_interval_estimate = 1.0
        self._time_interval_resolution = 0.01
        self._phase_input_channel = 0
        self._phase_reference_channel = 0
        self._phase_frequency_estimate = 1000.0
        self._phase_resolution = 0.01
        self._totalize_continuous_channel = 0
        self._totalize_gated_channel = 0
        self._totalize_gated_gate_source = ''
        self._totalize_gated_gate_slope = 'positive'
        self._totalize_timed_channel = 0
        self._totalize_timed_gate_time = 1.0
        self._arm_start_type = 'immediate'
        self._arm_start_external_source = ''
        self._arm_start_external_level = 1.0
        self._arm_start_external_slope = 'positive'
        self._arm_start_external_delay = 0.0
        self._arm_stop_type = 'immediate'
        self._arm_stop_external_source = ''
        self._arm_stop_external_level = 1.0
        self._arm_stop_external_slope = 'positive'
        self._arm_stop_external_delay = 0.0
        
        self.__dict__.setdefault('_docs', dict())
        self._docs['measurement_function'] = ivi.Doc("""
                        Specifies the current measurement function of the Counter. The user sets
                        the function by calling one of the configure measurement functions or the
                        set attribute function. See configure measurement functions for details on
                        setting up a measurement. See the behavior model for proper usage of the
                        Measurement Function attribute.
                        
                        Values
                        
                        * 'frequency'
                        * 'frequency_with_aperture'
                        * 'period'
                        * 'period_with_aperture'
                        * 'pulse_width'
                        * 'duty_cycle'
                        * 'edge_time'
                        * 'frequency_ratio'
                        * 'time_interval'
                        * 'phase'
                        * 'continuous_totalize'
                        * 'gated_totalize'
                        * 'timed_totalize'
                        * 'dc_voltage'
                        * 'maximum_voltage'
                        * 'minimum_voltage'
                        * 'rms_voltage'
                        * 'peak_to_peak_voltage'
                        """, cls, grp, '4.2.1')
        
        ivi.add_property(self, 'channels[].name',
                        self._get_channel_name,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the physical repeated capability identifier defined by the
                        specific driver for the channel that corresponds to the one-based index
                        that the user specifies. Valid values for the Index parameter are between
                        one and the value of the Channel Count attribute. If the user passes an
                        invalid value for the Index parameter, the value of this attribute is an
                        empty string.
                        """, cls, grp, '4.2.3'))
        ivi.add_property(self, 'channels[].impedance',
                        self._get_channel_impedance,
                        self._set_channel_impedance,
                        None,
                        ivi.Doc("""
                        Specifies the input impedance of the channel in Ohms.
                        
                        Common values are 50, 75, and 1,000,000.
                        """, cls, grp, '4.2.5'))
        ivi.add_property(self, 'channels[].coupling',
                        self._get_channel_coupling,
                        self._set_channel_coupling,
                        None,
                        ivi.Doc("""
                        Specifies the electrical coupling method used on the input channel.
                        
                        Values
                        
                        * 'ac'
                        * 'dc'
                        """, cls, grp, '4.2.6'))
        ivi.add_property(self, 'channels[].attenuation',
                        self._get_channel_attenuation,
                        self._set_channel_attenuation,
                        None,
                        ivi.Doc("""
                        Specifies the scale factor by which the channel attenuates the input.
                        Increasing this value decreases the sensitivity. For instance, setting
                        this value to 10 attenuates the input by a factor of 10.
                        """, cls, grp, '4.2.7'))
        ivi.add_property(self, 'channels[].level',
                        self._get_channel_level,
                        self._set_channel_level,
                        None,
                        ivi.Doc("""
                        Specifies the voltage level the input signal must pass through to produce
                        a count. Level is specified as the voltage at the input terminals and is
                        independent of attenuation.
                        """, cls, grp, '4.2.8'))
        ivi.add_property(self, 'channels[].hysteresis',
                        self._get_channel_hysteresis,
                        self._set_channel_hysteresis,
                        None,
                        ivi.Doc("""
                        Specifies the Hysteresis value in volts. Hysteresis sets how far a signal
                        must fall below the level before a rising edge can again be detected, and
                        how far a signal must rise above the level before a falling edge can again
                        be detected. Its function is to eliminate false events caused by signal
                        noise. Hysteresis is specified as the voltage at the input terminals and
                        is independent of attenuation.
                        """, cls, grp, '4.2.9'))
        ivi.add_property(self, 'channels[].slope',
                        self._get_channel_slope,
                        self._set_channel_slope,
                        None,
                        ivi.Doc("""
                        Specifies whether a rising (positive) or a falling (negative) edge
                        triggers the counter.
                        
                        Values
                        
                        * 'positive'
                        * 'negative'
                        """, cls, grp, '4.2.10'))
        ivi.add_property(self, 'channels[].filter_enabled',
                        self._get_channel_filter_enabled,
                        self._set_channel_filter_enabled,
                        None,
                        ivi.Doc("""
                        Specifies if the filter on the selected channel is enabled.
                        """, cls, grp, '4.2.11'))
        ivi.add_property(self, 'frequency.channel',
                        self._get_frequency_channel,
                        self._set_frequency_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the frequency is measured on.
                        """, cls, grp, '4.2.12'))
        ivi.add_property(self, 'frequency.estimate',
                        self._get_frequency_estimate,
                        self._set_frequency_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated frequency, in hertz, for the frequency function.
                        The driver uses this to optimize the configuration of the instrument for
                        the input signal. The driver typically use this to set the duration of the
                        measurement.
                        
                        Setting this attribute overrides the Frequency Aperture Time and sets the
                        Frequency Estimate Auto to false.
                        """, cls, grp, '4.2.13'))
        ivi.add_property(self, 'frequency.resolution',
                        self._get_frequency_resolution,
                        self._set_frequency_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the measurement, in hertz, for the frequency
                        function.
                        
                        Setting this attribute overrides the Frequency Aperture Time and sets the
                        Frequency Resolution Auto to false.
                        """, cls, grp, '4.2.14'))
        ivi.add_property(self, 'frequency.aperture_time',
                        self._get_frequency_aperture_time,
                        self._set_frequency_aperture_time,
                        None,
                        ivi.Doc("""
                        Specifies the aperture time for the frequency with aperture time function.
                        The units are seconds.
                        
                        Setting this attribute overrides the Frequency Estimate and Frequency
                        Resolution. This attribute can be read to determine the value of aperture
                        time selected by the driver based on the Frequency Estimate and Frequency
                        Resolution.
                        """, cls, grp, '4.2.15'))
        ivi.add_property(self, 'frequency.estimate_auto',
                        self._get_frequency_estimate_auto,
                        self._set_frequency_estimate_auto,
                        None,
                        ivi.Doc("""
                        Specifies if the Counter Frequency Estimate Auto is enabled. Use the
                        Frequency Estimate Auto attribute to enable auto frequency selection. If
                        this attribute is set to True, the instrument automatically determines the
                        best frequency estimate for the measurement. If this attribute is set to 
                        False, the user specifies the frequency estimate of the measurement by
                        explicitly setting the Frequency Estimate attribute.
                        """, cls, grp, '4.2.16'))
        ivi.add_property(self, 'frequency.resolution_auto',
                        self._get_frequency_resolution_auto,
                        self._set_frequency_resolution_auto,
                        None,
                        ivi.Doc("""
                        Specifies if the Counter Frequency Resolution Auto is enabled. Use the
                        Frequency Resolution Auto attribute to enable auto resolution selection.
                        If this attribute is set to True, the instrument automatically determines
                        the best frequency resolution for the measurement. If this attribute is
                        set to False, the user specifies the frequency resolution of the
                        measurement by explicitly setting the Frequency Resolution attribute.
                        """, cls, grp, '4.2.17'))
        ivi.add_property(self, 'period.channel',
                        self._get_period_channel,
                        self._set_period_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the period is measured on.
                        """, cls, grp, '4.2.18'))
        ivi.add_property(self, 'period.estimate',
                        self._get_period_estimate,
                        self._set_period_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated period for the period function. The driver uses
                        this to optimize the configuration of the instrument for the input signal.
                        The driver typically use this to set the duration of the measurement. The
                        units are seconds.
                        """, cls, grp, '4.2.19'))
        ivi.add_property(self, 'period.resolution',
                        self._get_period_resolution,
                        self._set_period_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the measurement for the period function. The
                        units are seconds.
                        """, cls, grp, '4.2.20'))
        ivi.add_property(self, 'period.aperture_time',
                        self._get_period_aperture_time,
                        self._set_period_aperture_time,
                        None,
                        ivi.Doc("""
                        Specifies the aperture time for the period with aperture time function. 
                        The units are seconds.
                        
                        Setting this attribute overrides the Period Estimate and Period
                        Resolution. This attribute can be read to determine the value of aperture
                        time selected by the driver based on the Estimate and Period Resolution.
                        """, cls, grp, '4.2.21'))
        ivi.add_property(self, 'pulse_width.channel',
                        self._get_pulse_width_channel,
                        self._set_pulse_width_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the pulse width is measured on.
                        """, cls, grp, '4.2.22'))
        ivi.add_property(self, 'pulse_width.estimate',
                        self._get_pulse_width_estimate,
                        self._set_pulse_width_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated pulse width for the pulse width function. The
                        driver uses this to optimize the configuration of the instrument for the
                        input signal. The driver typically use this to set the duration of the
                        measurement. The units are seconds.
                        """, cls, grp, '4.2.23'))
        ivi.add_property(self, 'pulse_width.resolution',
                        self._get_pulse_width_resolution,
                        self._set_pulse_width_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the measurement for the pulse width function.
                        The units are seconds.
                        """, cls, grp, '4.2.24'))
        ivi.add_property(self, 'duty_cycle.channel',
                        self._get_duty_cycle_channel,
                        self._set_duty_cycle_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the duty cycle is measured on.
                        """, cls, grp, '4.2.25'))
        ivi.add_property(self, 'duty_cycle.frequency_estimate',
                        self._get_duty_cycle_frequency_estimate,
                        self._set_duty_cycle_frequency_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated frequency, in hertz, for the duty cycle function.
                        The driver uses this to optimize the configuration of the instrument for
                        the input signal. The driver typically use this to set the duration of the
                        measurement.
                        """, cls, grp, '4.2.26'))
        ivi.add_property(self, 'duty_cycle.resolution',
                        self._get_duty_cycle_resolution,
                        self._set_duty_cycle_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution for the duty cycle function. Duty Cycle
                        Resolution is a unitless value.
                        """, cls, grp, '4.2.27'))
        ivi.add_property(self, 'edge_time.channel',
                        self._get_edge_time_channel,
                        self._set_edge_time_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the edge time is measured on.
                        """, cls, grp, '4.2.28'))
        ivi.add_property(self, 'edge_time.reference_type',
                        self._get_edge_time_reference_type,
                        self._set_edge_time_reference_type,
                        None,
                        ivi.Doc("""
                        Specifies the current reference type of the Counter. That is if the Edge
                        Time High Referenace and Edge Time Low Reference are interpretted as
                        percentage of peak-peak or absolute volts.
                        
                        Values
                        
                        * 'voltage'
                        * 'percent'
                        """, cls, grp, '4.2.29'))
        ivi.add_property(self, 'edge_time.estimate',
                        self._get_edge_time_estimate,
                        self._set_edge_time_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated edge time for the edge time function. The units
                        are seconds.
                        """, cls, grp, '4.2.30'))
        ivi.add_property(self, 'edge_time.resolution',
                        self._get_edge_time_resolution,
                        self._set_edge_time_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the measurement for the edge time function.
                        The units are seconds.
                        """, cls, grp, '4.2.31'))
        ivi.add_property(self, 'edge_time.high_reference',
                        self._get_edge_time_high_reference,
                        self._set_edge_time_high_reference,
                        None,
                        ivi.Doc("""
                        Specifies the high reference level for the edge time function. For a Rise
                        Time measurement, this is the level where the measurement stops and for a
                        Fall Time measurements, this is the level where the measurement starts.
                        """, cls, grp, '4.2.32'))
        ivi.add_property(self, 'edge_time.low_reference',
                        self._get_edge_time_low_reference,
                        self._set_edge_time_low_reference,
                        None,
                        ivi.Doc("""
                        Specifies the low reference level for the edge time function. For a Rise
                        Time measurement, this is the level where the measurement starts and for a
                        Fall Time measurements, this is the level where the measurement stops.
                        """, cls, grp, '4.2.33'))
        ivi.add_property(self, 'frequency_ratio.numerator_channel',
                        self._get_frequency_ratio_numerator_channel,
                        self._set_frequency_ratio_numerator_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the frequency ratio is measured on.
                        """, cls, grp, '4.2.34'))
        ivi.add_property(self, 'frequency_ratio.denominator_channel',
                        self._get_frequency_ratio_denominator_channel,
                        self._set_frequency_ratio_denominator_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input denominator channel the frequency ratio is measured on.
                        """, cls, grp, '4.2.35'))
        ivi.add_property(self, 'frequency_ratio.numerator_frequency_estimate',
                        self._get_frequency_ratio_numerator_frequency_estimate,
                        self._set_frequency_ratio_numerator_frequency_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated numerator frequency, in hertz, for the frequency
                        ratio function. The driver uses this to optimize the configuration of the
                        instrument for the input signal. The driver typically use this to set the
                        duration of the measurement.
                        """, cls, grp, '4.2.36'))
        ivi.add_property(self, 'frequency_ratio.estimate',
                        self._get_frequency_ratio_estimate,
                        self._set_frequency_ratio_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated frequency ratio for the frequency ratio function.
                        Frequency Ratio Estimate is unitless value.
                        """, cls, grp, '4.2.37'))
        ivi.add_property(self, 'frequency_ratio.resolution',
                        self._get_frequency_ratio_resolution,
                        self._set_frequency_ratio_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the frequency ratio resolution of the frequency ratio function.
                        Frequency Ratio Resolution is unitless value.
                        """, cls, grp, '4.2.38'))
        ivi.add_property(self, 'time_interval.start_channel',
                        self._get_time_interval_start_channel,
                        self._set_time_interval_start_channel,
                        None,
                        ivi.Doc("""
                        Specifies the start channel used to perform the time interval function.
                        """, cls, grp, '4.2.39'))
        ivi.add_property(self, 'time_interval.stop_channel',
                        self._get_time_interval_stop_channel,
                        self._set_time_interval_stop_channel,
                        None,
                        ivi.Doc("""
                        Specifies the stop channel used to perform the time interval function.
                        """, cls, grp, '4.2.40'))
        ivi.add_property(self, 'time_interval.estimate',
                        self._get_time_interval_estimate,
                        self._set_time_interval_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated time interval for the time interval function. The
                        units are seconds.
                        """, cls, grp, '4.2.41'))
        ivi.add_property(self, 'time_interval.resolution',
                        self._get_time_interval_resolution,
                        self._set_time_interval_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the measurement for the time interval
                        function. The units are seconds.
                        """, cls, grp, '4.2.42'))
        ivi.add_property(self, 'phase.input_channel',
                        self._get_phase_input_channel,
                        self._set_phase_input_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the phase is measured on.
                        """, cls, grp, '4.2.43'))
        ivi.add_property(self, 'phase.reference_channel',
                        self._get_phase_reference_channel,
                        self._set_phase_reference_channel,
                        None,
                        ivi.Doc("""
                        Specifies the reference channel for the phase measurement.
                        """, cls, grp, '4.2.44'))
        ivi.add_property(self, 'phase.frequency_estimate',
                        self._get_phase_frequency_estimate,
                        self._set_phase_frequency_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated frequency, in hertz, for the phase function
                        reference channel. The driver uses this to optimize the configuration of
                        the instrument for the input signal. The driver typically use this to set
                        the duration of the measurement.
                        """, cls, grp, '4.2.45'))
        ivi.add_property(self, 'phase.resolution',
                        self._get_phase_resolution,
                        self._set_phase_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the measurement, in degrees, for the phase
                        function reference channel.
                        """, cls, grp, '4.2.46'))
        ivi.add_property(self, 'totalize_continuous.channel',
                        self._get_totalize_continuous_channel,
                        self._set_totalize_continuous_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel for the continuous totalize function.
                        """, cls, grp, '4.2.47'))
        ivi.add_property(self, 'totalize_gated.channel',
                        self._get_totalize_gated_channel,
                        self._set_totalize_gated_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel for the gated totalize function.
                        """, cls, grp, '4.2.48'))
        ivi.add_property(self, 'totalize_gated.gate_source',
                        self._get_totalize_gated_gate_source,
                        self._set_totalize_gated_gate_source,
                        None,
                        ivi.Doc("""
                        Specifies the gate source for the gated totalize function.
                        """, cls, grp, '4.2.49'))
        ivi.add_property(self, 'totalize_gated.gate_slope',
                        self._get_totalize_gated_gate_slope,
                        self._set_totalize_gated_gate_slope,
                        None,
                        ivi.Doc("""
                        Specifies the gate slope that enables the gated totalize function.
                        
                        Values
                        
                        * 'positive'
                        * 'negative'
                        """, cls, grp, '4.2.50'))
        ivi.add_property(self, 'totalize_timed.channel',
                        self._get_totalize_timed_channel,
                        self._set_totalize_timed_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel for the timed totalize function.
                        """, cls, grp, '4.2.51'))
        ivi.add_property(self, 'totalize_timed.gate_time',
                        self._get_totalize_timed_gate_time,
                        self._set_totalize_timed_gate_time,
                        None,
                        ivi.Doc("""
                        Specifies the gate time for the timed totalize function. The units are
                        seconds.
                        """, cls, grp, '4.2.52'))
        ivi.add_property(self, 'arm.start.type',
                        self._get_arm_start_type,
                        self._set_arm_start_type,
                        None,
                        ivi.Doc("""
                        Specifies the start arm type for armed measurements.
                        """, cls, grp, '4.2.53'))
        ivi.add_property(self, 'arm.start.external.source',
                        self._get_arm_start_external_source,
                        self._set_arm_start_external_source,
                        None,
                        ivi.Doc("""
                        Specifies the start arm source for external armed measurements.
                        """, cls, grp, '4.2.54'))
        ivi.add_property(self, 'arm.start.external.level',
                        self._get_arm_start_external_level,
                        self._set_arm_start_external_level,
                        None,
                        ivi.Doc("""
                        Specifies the voltage level in volts that starts external armed measurements.
                        """, cls, grp, '4.2.55'))
        ivi.add_property(self, 'arm.start.external.slope',
                        self._get_arm_start_external_slope,
                        self._set_arm_start_external_slope,
                        None,
                        ivi.Doc("""
                        Specifies the signal slope that starts external armed measurements.
                        
                        Values
                        
                        * 'positive'
                        * 'negative'
                        """, cls, grp, '4.2.56'))
        ivi.add_property(self, 'arm.start.external.delay',
                        self._get_arm_start_external_delay,
                        self._set_arm_start_external_delay,
                        None,
                        ivi.Doc("""
                        Specifies the delay used after an external armed measurement has been
                        armed. The units are seconds.
                        """, cls, grp, '4.2.57'))
        ivi.add_property(self, 'arm.stop.type',
                        self._get_arm_stop_type,
                        self._set_arm_stop_type,
                        None,
                        ivi.Doc("""
                        Specifies the stop arm type for armed measurements.
                        """, cls, grp, '4.2.58'))
        ivi.add_property(self, 'arm.stop.external.source',
                        self._get_arm_stop_external_source,
                        self._set_arm_stop_external_source,
                        None,
                        ivi.Doc("""
                        Specifies the stop arm source for external armed measurements.
                        """, cls, grp, '4.2.59'))
        ivi.add_property(self, 'arm.stop.external.level',
                        self._get_arm_stop_external_level,
                        self._set_arm_stop_external_level,
                        None,
                        ivi.Doc("""
                        Specifies the voltage level in volts that stops external armed
                        measurements. The External Stop Arm Delay, if non-zero, is applied before
                        the measurement stops.
                        """, cls, grp, '4.2.60'))
        ivi.add_property(self, 'arm.stop.external.slope',
                        self._get_arm_stop_external_slope,
                        self._set_arm_stop_external_slope,
                        None,
                        ivi.Doc("""
                        Specifies the signal slope that stops external armed measurements. The
                        External Stop Arm Delay, if non-zero, is applied before the measurements
                        stops.
                        
                        Values
                        
                        * 'positive'
                        * 'negative'
                        """, cls, grp, '4.2.61'))
        ivi.add_property(self, 'arm.stop.external.delay',
                        self._get_arm_stop_external_delay,
                        self._set_arm_stop_external_delay,
                        None,
                        ivi.Doc("""
                        Specifies the delay after the External Arm Stop event has occurred until
                        the measurement stops. The units are seconds.
                        """, cls, grp, '4.2.62'))
        ivi.add_method(self, 'measurement.abort',
                        self._measurement_abort,
                        ivi.Doc("""
                        Aborts a previously initiated measurement.
                        """, cls, grp, '4.3.1'))
        ivi.add_method(self, 'measurement.is_measurement_complete',
                        self._measurement_is_measurement_complete,
                        ivi.Doc("""
                        Returns whether a measurement is in progress, complete, or if the status
                        is unknown.
                        """, cls, grp, '4.3.2'))
        ivi.add_method(self, 'channels[].configure',
                        self._channel_configure,
                        ivi.Doc("""
                        Configures the Impedance, Coupling, and Attenuation attributes of the
                        counter channel.
                        """, cls, grp, '4.3.4'))
        ivi.add_method(self, 'channels[].configure_level',
                        self._channel_configure_level,
                        ivi.Doc("""
                        Configures the Level and Hysteresis attributes for a channel.
                        """, cls, grp, '4.3.5'))
        ivi.add_method(self, 'frequency.configure',
                        self._frequency_configure,
                        ivi.Doc("""
                        These functions provide both manual and auto frequency configuration. The
                        Configure Manual function configures the Estimate and Resolution
                        attributes for a frequency measurement for a particular channel. The
                        Configure function configures the instrument to determine the best
                        estimate and resolution for the selected channel.
                        
                        The Configure function sets Frequency Estimate Auto and Frequency
                        Resolution Auto true. When the Frequency Estimate Auto or Frequency
                        Resolution Auto are true, the Aperture Time attribute can be read to
                        determine the Aperture Time selected by the driver.
                        
                        The default conditions for automatic measurements are:
                        
                        * Mode: Frequency
                        * Trigger Level: Auto
                        * Trigger Slope: Positive
                        * Impedance: 1 MOhm
                        * Attenuation: 1X
                        * Coupling: AC
                        * Filter: Off
                        """, cls, grp, '4.3.8'))
        ivi.add_method(self, 'frequency.configure_manual',
                        self._frequency_configure_manual,
                        ivi.Doc("""
                        These functions provide both manual and auto frequency configuration. The
                        Configure Manual function configures the Estimate and Resolution
                        attributes for a frequency measurement for a particular channel. The
                        Configure function configures the instrument to determine the best
                        estimate and resolution for the selected channel.
                        
                        The Configure function sets Frequency Estimate Auto and Frequency
                        Resolution Auto true. When the Frequency Estimate Auto or Frequency
                        Resolution Auto are true, the Aperture Time attribute can be read to
                        determine the Aperture Time selected by the driver.
                        
                        The default conditions for automatic measurements are:
                        
                        * Mode: Frequency
                        * Trigger Level: Auto
                        * Trigger Slope: Positive
                        * Impedance: 1 MOhm
                        * Attenuation: 1X
                        * Coupling: AC
                        * Filter: Off
                        """, cls, grp, '4.3.8'))
        ivi.add_method(self, 'frequency.configure_with_aperture',
                        self._frequency_configure_with_aperture,
                        ivi.Doc("""
                        Configures a frequency measurement based on the specified aperture time.
                        """, cls, grp, '4.3.9'))
        ivi.add_method(self, 'period.configure',
                        self._period_configure,
                        ivi.Doc("""
                        Configures the estimate and resolution attributes for a period
                        measurement.
                        """, cls, grp, '4.3.10'))
        ivi.add_method(self, 'period.configure_with_aperture',
                        self._period_configure_with_aperture,
                        ivi.Doc("""
                        Configures a period measurement based on the specified aperture time.
                        """, cls, grp, '4.3.11'))
        ivi.add_method(self, 'pulse_width.configure',
                        self._pulse_width_configure,
                        ivi.Doc("""
                        Configures the estimate and resolution attributes for a pulse width
                        measurement.
                        """, cls, grp, '4.3.12'))
        ivi.add_method(self, 'duty_cycle.configure',
                        self._duty_cycle_configure,
                        ivi.Doc("""
                        Configures the frequency estimate and resolution attributes for a duty
                        cycle measurement.
                        """, cls, grp, '4.3.13'))
        ivi.add_method(self, 'edge_time.configure',
                        self._edge_time_configure,
                        ivi.Doc("""
                        Configures an edge time measurement. The estimate and resolution
                        attributes are set to the values specified. The edge time reference type
                        is set to percentage, and the edge time low reference and edge time high
                        reference are set to 10% and 90% respectively. If the channel slope is
                        positive a rise-time measurement is performed, if the channel slope is
                        negative, a fall-time measurement is performed.
                        """, cls, grp, '4.3.14'))
        ivi.add_method(self, 'edge_time.configure',
                        self._edge_time_configure_reference_levels,
                        ivi.Doc("""
                        Configures the reference type, estimate, resolution, high reference level,
                        and low reference level attributes for an edge time measurement. If the
                        channel slope is positive a rise-time measurement is performed, if the
                        channel slope is negative, a fall-time measurement is performed.
                        """, cls, grp, '4.3.15'))
        ivi.add_method(self, 'frequency_ratio.configure',
                        self._frequency_ratio_configure,
                        ivi.Doc("""
                        Configures the estimated frequencies, and resolution attributes and
                        specifies the numerator and denominator channels for a frequency ratio
                        measurement.
                        """, cls, grp, '4.3.16'))
        ivi.add_method(self, 'time_interval.configure',
                        self._time_interval_configure,
                        ivi.Doc("""
                        Configures the estimate and resolution attributes and specifies the start
                        and stop channels for a time interval measurement.
                        """, cls, grp, '4.3.17'))
        ivi.add_method(self, 'phase.configure',
                        self._phase_configure,
                        ivi.Doc("""
                        Configures the estimate and resolution attributes and specifies the input
                        and reference channels for a phase measurement.
                        """, cls, grp, '4.3.18'))
        ivi.add_method(self, 'totalize_continuous.configure',
                        self._totalize_continuous_configure,
                        ivi.Doc("""
                        Configures the counter for a continuous totalize measurement. Start
                        continuous totalize clears the count and starts the accumulation of
                        counts. Stop continuous totalize stops the accumulation of counts. Fetch
                        continuous totalize can be called if the count is accumulating or stopped
                        to retrieve the current count.
                        """, cls, grp, '4.3.19'))
        ivi.add_method(self, 'totalize_continuous.start',
                        self._totalize_continuous_start,
                        ivi.Doc("""
                        Clears the count and starts the counter for a continuous totalize
                        measurement. Refer to Section 4.3.19, Configure Continuous Totalize for
                        details.
                        """, cls, grp, '4.3.20'))
        ivi.add_method(self, 'totalize_continuous.stop',
                        self._totalize_continuous_stop,
                        ivi.Doc("""
                        Stops the accumulation of counts for a continuous totalize measurement.
                        Refer to Section 4.3.19, Configure Continuous Totalize for details.
                        """, cls, grp, '4.3.21'))
        ivi.add_method(self, 'totalize_continuous.fetch_count',
                        self._totalize_continuous_fetch_count,
                        ivi.Doc("""
                        Retrieves the current count while the counter is continuously totalizing.
                        Refer to Section 4.3.19, Configure Continuous Totalize for details.
                        """, cls, grp, '4.3.22'))
        ivi.add_method(self, 'totalize_gated.configure',
                        self._totalize_gated_configure,
                        ivi.Doc("""
                        Specifies the channel to use for the gate source and configures the gate
                        slope attribute for a gated totalize measurement.
                        """, cls, grp, '4.3.23'))
        ivi.add_method(self, 'totalize_timed.configure',
                        self._totalize_timed_configure,
                        ivi.Doc("""
                        Sets the measurement function to Timed Totalize and configures the gate
                        time attribute.
                        """, cls, grp, '4.3.24'))
        ivi.add_method(self, 'arm.start.external.configure',
                        self._arm_start_external_configure,
                        ivi.Doc("""
                        Specifies the External Start Arm Source and configures the Level, Slope
                        and Delay attributes.
                        """, cls, grp, '4.3.26'))
        ivi.add_method(self, 'arm.stop.external.configure',
                        self._arm_stop_external_configure,
                        ivi.Doc("""
                        Specifies the External Stop Arm Source and configures the Level, Slope and
                        Delay attributes.
                        """, cls, grp, '4.3.28'))
        ivi.add_method(self, 'measurement.fetch',
                        self._measurement_fetch,
                        ivi.Doc("""
                        Retrieves the result from a previously initiated measurement.
                        
                        Use the Initiate function to start a measurement. The Is Measurement
                        Complete function may be used to determine when the measurement is
                        complete.
                        
                        You can call the Read function instead of the Initiate function. The Read
                        function starts a measurement. It then waits for the measurement to
                        complete, obtains the measured value, and returns the measured value. You
                        call this function separately for any other measurements that you want to
                        obtain on a specific channel.
                        
                        This function does not check the instrument status. Typically, you call
                        this function only in a sequence of calls to other low-level driver
                        functions. The sequence performs one operation. You use the low-level
                        functions to optimize one or more aspects of interaction with the
                        instrument. If you want to check the instrument status, call the Error
                        Query function at the conclusion of the sequence.
                        """, cls, grp, '4.3.29'))
        ivi.add_method(self, 'measurement.initiate',
                        self._measurement_initiate,
                        ivi.Doc("""
                        Initiates a measurement based on the current configuration. You must
                        configure the measurement type and input channel before calling this
                        function. After you call this function, if the arm type is immediate the
                        measurement commences immediately; if the arm type is external the Counter
                        leaves the Idle state and waits for a start arm. To retrieve the
                        measurement, call the Fetch function.
                        
                        This function does not check the instrument status. Typically, you call
                        this function only in a sequence of calls to other low-level driver
                        functions. The sequence performs one operation. You use the low-level
                        functions to optimize one or more aspects of interaction with the
                        instrument. If you want to check the instrument status, call the
                        IviCounter_error_query function at the conclusion of the sequence.
                        """, cls, grp, '4.3.30'))
        ivi.add_method(self, 'measurement.read',
                        self._measurement_read,
                        ivi.Doc("""
                        Initiates and fetches a measurement based on the current configuration.
                        Read waits a maximum of MaxTimeMilliseconds (C/COM) or maxTime (.NET) for
                        the imstrument to return a measurement. Read generates an error if it
                        exceeds the MaxTimeMilliseconds or maxTime.
                        """, cls, grp, '4.3.31'))
        
        self._init_channels()
    
    
    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_impedance = list()
        self._channel_coupling = list()
        self._channel_attenuation = list()
        self._channel_level = list()
        self._channel_hysteresis = list()
        self._channel_slope = list()
        self._channel_filter_enabled = list()
        for i in range(self._channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_impedance.append(50.0)
            self._channel_coupling.append('dc')
            self._channel_attenuation.append(1.0)
            self._channel_level.append(2.0)
            self._channel_hysteresis.append(1.0)
            self._channel_slope.append('positive')
            self._channel_filter_enabled.append(False)
        
        self.channels._set_list(self._channel_name)
    
    
    def _get_measurement_function(self):
        return self._measurement_function
    
    def _set_measurement_function(self, value):
        if value not in MeasurementFunction:
            raise ivi.ValueNotSupportedException()
        self._measurement_function = value
    
    measurement_function = property(lambda self: self._get_measurement_function(),
                                    lambda self, value: self._set_measurement_function(value))
    
    def _get_channel_count(self):
        return self._channel_count
    
    def _get_channel_name(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_name[index]
    
    def _get_channel_impedance(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_impedance[index]
    
    def _set_channel_impedance(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_impedance[index] = value
    
    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_coupling[index]
    
    def _set_channel_coupling(self, index, value):
        if value not in Coupling:
            raise ivi.ValueNotSupportedException()
        self._channel_coupling[index] = value
    
    def _get_channel_attenuation(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_attenuation[index]
    
    def _set_channel_attenuation(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_attenuation[index] = value
    
    def _get_channel_level(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_level[index]
    
    def _set_channel_level(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_level[index] = value
    
    def _get_channel_hysteresis(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_hysteresis[index]
    
    def _set_channel_hysteresis(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_hysteresis[index] = value
    
    def _get_channel_slope(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_slope[index]
    
    def _set_channel_slope(self, index, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._channel_slope[index] = value
    
    def _get_channel_filter_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_filter_enabled[index]
    
    def _set_channel_filter_enabled(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_filter_enabled[index] = value
    
    def _get_frequency_channel(self):
        return self._frequency_channel
    
    def _set_frequency_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._frequency_channel = index
    
    def _get_frequency_estimate(self):
        return self._frequency_estimate
    
    def _set_frequency_estimate(self, value):
        value = float(value)
        self._frequency_estimate = value
    
    def _get_frequency_resolution(self):
        return self._frequency_resolution
    
    def _set_frequency_resolution(self, value):
        value = float(value)
        self._frequency_resolution = value
    
    def _get_frequency_aperture_time(self):
        return self._frequency_aperture_time
    
    def _set_frequency_aperture_time(self, value):
        value = float(value)
        self._frequency_aperture_time = value
    
    def _get_frequency_estimate_auto(self):
        return self._frequency_estimate_auto
    
    def _set_frequency_estimate_auto(self, value):
        value = bool(value)
        self._frequency_estimate_auto = value
    
    def _get_frequency_resolution_auto(self):
        return self._frequency_resolution_auto
    
    def _set_frequency_resolution_auto(self, value):
        value = bool(value)
        self._frequency_resolution_auto = value
    
    def _get_period_channel(self):
        return self._period_channel
    
    def _set_period_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._period_channel = index
    
    def _get_period_estimate(self):
        return self._period_estimate
    
    def _set_period_estimate(self, value):
        value = float(value)
        self._period_estimate = value
    
    def _get_period_resolution(self):
        return self._period_resolution
    
    def _set_period_resolution(self, value):
        value = float(value)
        self._period_resolution = value
    
    def _get_period_aperture_time(self):
        return self._period_aperture_time
    
    def _set_period_aperture_time(self, value):
        value = float(value)
        self._period_aperture_time = value
    
    def _get_pulse_width_channel(self):
        return self._pulse_width_channel
    
    def _set_pulse_width_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._pulse_width_channel = index
    
    def _get_pulse_width_estimate(self):
        return self._pulse_width_estimate
    
    def _set_pulse_width_estimate(self, value):
        value = float(value)
        self._pulse_width_estimate = value
    
    def _get_pulse_width_resolution(self):
        return self._pulse_width_resolution
    
    def _set_pulse_width_resolution(self, value):
        value = float(value)
        self._pulse_width_resolution = value
    
    def _get_duty_cycle_channel(self):
        return self._duty_cycle_channel
    
    def _set_duty_cycle_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._duty_cycle_channel = index
    
    def _get_duty_cycle_frequency_estimate(self):
        return self._duty_cycle_frequency_estimate
    
    def _set_duty_cycle_frequency_estimate(self, value):
        value = float(value)
        self._duty_cycle_frequency_estimate = value
    
    def _get_duty_cycle_resolution(self):
        return self._duty_cycle_resolution
    
    def _set_duty_cycle_resolution(self, value):
        value = float(value)
        self._duty_cycle_resolution = value
    
    def _get_edge_time_channel(self):
        return self._edge_time_channel
    
    def _set_edge_time_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._edge_time_channel = index
    
    def _get_edge_time_reference_type(self):
        return self._edge_time_reference_type
    
    def _set_edge_time_reference_type(self, value):
        if value not in ReferenceType:
            raise ivi.ValueNotSupportedException()
        self._edge_time_reference_type = value
    
    def _get_edge_time_estimate(self):
        return self._edge_time_estimate
    
    def _set_edge_time_estimate(self, value):
        value = float(value)
        self._edge_time_estimate = value
    
    def _get_edge_time_resolution(self):
        return self._edge_time_resolution
    
    def _set_edge_time_resolution(self, value):
        value = float(value)
        self._edge_time_resolution = value
    
    def _get_edge_time_high_reference(self):
        return self._edge_time_high_reference
    
    def _set_edge_time_high_reference(self, value):
        value = float(value)
        self._edge_time_high_reference = value
    
    def _get_edge_time_low_reference(self):
        return self._edge_time_low_reference
    
    def _set_edge_time_low_reference(self, value):
        value = float(value)
        self._edge_time_low_reference = value
    
    def _get_frequency_ratio_numerator_channel(self):
        return self._frequency_ratio_numerator_channel
    
    def _set_frequency_ratio_numerator_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._frequency_ratio_numerator_channel = index
    
    def _get_frequency_ratio_denominator_channel(self):
        return self._frequency_ratio_denominator_channel
    
    def _set_frequency_ratio_denominator_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._frequency_ratio_denominator_channel = index
    
    def _get_frequency_ratio_numerator_frequency_estimate(self):
        return self._frequency_ratio_numerator_frequency_estimate
    
    def _set_frequency_ratio_numerator_frequency_estimate(self, value):
        value = float(value)
        self._frequency_ratio_numerator_frequency_estimate = value
    
    def _get_frequency_ratio_estimate(self):
        return self._frequency_ratio_estimate
    
    def _set_frequency_ratio_estimate(self, value):
        value = float(value)
        self._frequency_ratio_estimate = value
    
    def _get_frequency_ratio_resolution(self):
        return self._frequency_ratio_resolution
    
    def _set_frequency_ratio_resolution(self, value):
        value = float(value)
        self._frequency_ratio_resolution = value
    
    def _get_time_interval_start_channel(self):
        return self._time_interval_start_channel
    
    def _set_time_interval_start_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._time_interval_start_channel = index
    
    def _get_time_interval_stop_channel(self):
        return self._time_interval_stop_channel
    
    def _set_time_interval_stop_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._time_interval_stop_channel = index
    
    def _get_time_interval_estimate(self):
        return self._time_interval_estimate
    
    def _set_time_interval_estimate(self, value):
        value = float(value)
        self._time_interval_estimate = value
    
    def _get_time_interval_resolution(self):
        return self._time_interval_resolution
    
    def _set_time_interval_resolution(self, value):
        value = float(value)
        self._time_interval_resolution = value
    
    def _get_phase_input_channel(self):
        return self._phase_input_channel
    
    def _set_phase_input_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._phase_input_channel = index
    
    def _get_phase_reference_channel(self):
        return self._phase_reference_channel
    
    def _set_phase_reference_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._phase_reference_channel = index
    
    def _get_phase_frequency_estimate(self):
        return self._phase_frequency_estimate
    
    def _set_phase_frequency_estimate(self, value):
        value = float(value)
        self._phase_frequency_estimate = value
    
    def _get_phase_resolution(self):
        return self._phase_resolution
    
    def _set_phase_resolution(self, value):
        value = float(value)
        self._phase_resolution = value
    
    def _get_totalize_continuous_channel(self):
        return self._totalize_continuous_channel
    
    def _set_totalize_continuous_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._totalize_continuous_channel = index
    
    def _get_totalize_gated_channel(self):
        return self._totalize_gated_channel
    
    def _set_totalize_gated_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._totalize_gated_channel = index
    
    def _get_totalize_gated_gate_source(self):
        return self._totalize_gated_gate_source
    
    def _set_totalize_gated_gate_source(self, value):
        self._totalize_gated_gate_source = value
    
    def _get_totalize_gated_gate_slope(self):
        return self._totalize_gated_gate_slope
    
    def _set_totalize_gated_gate_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._totalize_gated_gate_slope = value
    
    def _get_totalize_timed_channel(self):
        return self._totalize_timed_channel
    
    def _set_totalize_timed_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._totalize_timed_channel = index
    
    def _get_totalize_timed_gate_time(self):
        return self._totalize_timed_gate_time
    
    def _set_totalize_timed_gate_time(self, value):
        value = float(value)
        self._totalize_timed_gate_time = value
    
    def _get_arm_start_type(self):
        return self._arm_start_type
    
    def _set_arm_start_type(self, value):
        if value not in ArmType:
            raise ivi.ValueNotSupportedException()
        self._arm_start_type = value
    
    def _get_arm_start_external_source(self):
        return self._arm_start_external_source
    
    def _set_arm_start_external_source(self, value):
        self._arm_start_external_source = value
    
    def _get_arm_start_external_level(self):
        return self._arm_start_external_level
    
    def _set_arm_start_external_level(self, value):
        value = float(value)
        self._arm_start_external_level = value
    
    def _get_arm_start_external_slope(self):
        return self._arm_start_external_slope
    
    def _set_arm_start_external_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._arm_start_external_slope = value
    
    def _get_arm_start_external_delay(self):
        return self._arm_start_external_delay
    
    def _set_arm_start_external_delay(self, value):
        value = float(value)
        self._arm_start_external_delay = value
    
    def _get_arm_stop_type(self):
        return self._arm_stop_type
    
    def _set_arm_stop_type(self, value):
        if value not in ArmType:
            raise ivi.ValueNotSupportedException()
        self._arm_stop_type = value
    
    def _get_arm_stop_external_source(self):
        return self._arm_stop_external_source
    
    def _set_arm_stop_external_source(self, value):
        self._arm_stop_external_source = value
    
    def _get_arm_stop_external_level(self):
        return self._arm_stop_external_level
    
    def _set_arm_stop_external_level(self, value):
        value = float(value)
        self._arm_stop_external_level = value
    
    def _get_arm_stop_external_slope(self):
        return self._arm_stop_external_slope
    
    def _set_arm_stop_external_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._arm_stop_external_slope = value
    
    def _get_arm_stop_external_delay(self):
        return self._arm_stop_external_delay
    
    def _set_arm_stop_external_delay(self, value):
        value = float(value)
        self._arm_stop_external_delay = value
    
    def _measurement_abort(self):
        pass
    
    def _measurement_is_measurement_complete(self):
        return True
    
    def _channel_configure(self, index, impedance, coupling, attenuation):
        self._set_channel_impedance(index, impedance)
        self._set_channel_coupling(index, coupling)
        self._set_channel_attenuation(index, attenuation)
    
    def _channel_configure_level(self, index, trigger_level, hysteresis):
        self._set_channel_level(index, trigger_level)
        self._set_channel_hysteresis(index, hysteresis)
    
    def _frequency_configure(self, channel, estimate = None, resolution = None):
        self._set_measurement_function('frequency')
        self._set_frequency_channel(channel)
        if estimate is None:
            self._set_frequency_estimate_auto(True)
        else:
            self._set_frequency_estimate(estimate)
            self._set_frequency_estimate_auto(False)
        if resolution is None:
            self._set_frequency_resolution_auto(True)
        else:
            self._set_frequency_resolution(resolution)
            self._set_frequency_resolution_auto(False)
    
    def _frequency_configure_manual(self, channel, estimate, resolution):
        self._set_measurement_function('frequency')
        self._frequency_configure(channel, estimate, resolution)
    
    def _frequency_configure_with_aperture(self, channel, aperture_time):
        self._set_measurement_function('frequency_with_aperture')
        self._set_frequency_channel(channel)
        self._set_frequency_aperture_time(aperture_time)
    
    def _period_configure(self, channel, estimate, resolution):
        self._set_measurement_function('period')
        self._set_period_channel(channel)
        self._set_period_estimate(estimate)
        self._set_period_resolution(resolution)
    
    def _period_configure_with_aperture(self, channel, aperture_time):
        self._set_measurement_function('period_with_aperture')
        self._set_period_channel(channel)
        self._set_period_aperture_time(aperture_time)
    
    def _pulse_width_configure(self, channel, estimate, resolution):
        self._set_measurement_function('pulse_width')
        self._set_pulse_width_channel(channel)
        self._set_pulse_width_estimate(estimate)
        self._set_pulse_width_resolution(resolution)
    
    def _duty_cycle_configure(self, channel, frequency_estimate, resolution):
        self._set_measurement_function('duty_cycle')
        self._set_duty_cycle_channel(channel)
        self._set_duty_cycle_frequency_estimate(frequency_estimate)
        self._set_duty_cycle_resolution(resolution)
    
    def _edge_time_configure(self, channel, estimate, resolution):
        self._set_measurement_function('edge_time')
        self._set_edge_time_channel(channel)
        self._set_edge_time_estimate(estimate)
        self._set_edge_time_resolution(resolution)
    
    def _edge_time_configure_reference_levels(self, channel, reference_type, estimate, resolution, high_reference, low_reference):
        self._set_measurement_function('edge_time')
        self._set_edge_time_channel(channel)
        self._set_edge_time_reference_type(reference_type)
        self._set_edge_time_estimate(estimate)
        self._set_edge_time_resolution(resolution)
        self._set_edge_time_high_reference(high_reference)
        self._set_edge_time_low_reference(low_reference)
    
    def _frequency_ratio_configure(self, numerator_channel, denominator_channel, numerator_frequency_estimate, estimate, resolution):
        self._set_measurement_function('frequency_ratio')
        self._set_frequency_ratio_numerator_channel(numerator_channel)
        self._set_frequency_ratio_denominator_channel(denominator_channel)
        self._set_frequency_ratio_numerator_frequency_estimate(numerator_frequency_estimate)
        self._set_frequency_ratio_estimate(estimate)
        self._set_frequency_ratio_resolution(resolution)
    
    def _time_interval_configure(self, start_channel, stop_channel, estimate, resolution):
        self._set_measurement_function('time_interval')
        self._set_time_interval_start_channel(start_channel)
        self._set_time_interval_stop_channel(stop_channel)
        self._set_time_interval_estimate(estimate)
        self._set_time_interval_resolution(resolution)
    
    def _phase_configure(self, input_channel, reference_channel, frequency_estimate, resolution):
        self._set_measurement_function('phase')
        self._set_phase_input_channel(input_channel)
        self._set_phase_reference_channel(reference_channel)
        self._set_phase_frequency_estimate(frequency_estimate)
        self._set_phase_resolution(resolution)
    
    def _totalize_continuous_configure(self, channel):
        self._set_measurement_function('totalize_continuous')
        self._set_totalize_continuous_channel(channel)
    
    def _totalize_continuous_start(self):
        pass
    
    def _totalize_continuous_stop(self):
        pass
    
    def _totalize_continuous_fetch_count(self):
        return 0
    
    def _totalize_gated_configure(self, channel, gate_source, gate_slope):
        self._set_measurement_function('totalize_gated')
        self._set_totalize_gated_channel(channel)
        self._set_totalize_gated_gate_source(gate_source)
        self._set_totalize_gated_gate_slope(gate_slope)
    
    def _totalize_timed_configure(self, channel, estimate, resolution):
        self._set_measurement_function('totalize_timed')
        self._set_totalize_timed_channel(channel)
        self._set_totalize_timed_estimate(estimate)
        self._set_totalize_timed_resolution(resolution)
    
    def _arm_start_external_configure(self, source, level, slope, delay):
        self._set_arm_start_type('external')
        self._set_arm_start_external_source(source)
        self._set_arm_start_external_level(level)
        self._set_arm_start_external_slope(slope)
        self._set_arm_start_external_delay(delay)
    
    def _arm_stop_external_configure(self, source, level, slope, delay):
        self._set_arm_stop_type('external')
        self._set_arm_stop_external_source(source)
        self._set_arm_stop_external_level(level)
        self._set_arm_stop_external_slope(slope)
        self._set_arm_stop_external_delay(delay)
    
    def _measurement_fetch(self):
        return None
    
    def _measurement_initiate(self):
        pass
    
    def _measurement_read(self, maximum_time):
        return self._measurement_fetch()
    
    
class Filter(object):
    "Extension IVI methods for frequency counters that support filtering the input frequency"
    
    def __init__(self, *args, **kwargs):
        super(Filter, self).__init__(*args, **kwargs)
        
        cls = 'IviCounter'
        grp = 'Filter'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_minimum_frequency = list()
        self._channel_maximum_frequency = list()
        
        ivi.add_property(self, 'channels[].minimum_frequency',
                        self._get_channel_minimum_frequency,
                        self._set_channel_minimum_frequency,
                        None,
                        ivi.Doc("""
                        Specifies the low cutoff frequency for the filter in hertz. Set to zero to
                        disable low frequency filtering.
                        """, cls, grp, '5.2.1'))
        ivi.add_property(self, 'channels[].maximum_frequency',
                        self._get_channel_maximum_frequency,
                        self._set_channel_maximum_frequency,
                        None,
                        ivi.Doc("""
                        Specifies the high cutoff frequency for the filter in hertz. Set to
                        positive infinity to disable high frequency filtering.
                        """, cls, grp, '5.2.2'))
        ivi.add_method(self, 'channels[].filter.configure',
                        self._channel_filter_configure,
                        ivi.Doc("""
                        
                        """, cls, grp, '5.3.1'))
        
    def _init_channels(self):
        try:
            super(Filter, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_minimum_frequency = list()
        self._channel_maximum_frequency = list()
        for i in range(self._channel_count):
            self._channel_minimum_frequency.append(0.0)
            self._channel_maximum_frequency.append(1e9)
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_minimum_frequency(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_minimum_frequency[index]
    
    def _set_channel_minimum_frequency(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = int(value)
        self._channel_minimum_frequency[index] = value
    
    def _get_channel_maximum_frequency(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_maximum_frequency[index]
    
    def _set_channel_maximum_frequency(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = int(value)
        self._channel_maximum_frequency[index] = value
    
    def _channel_filter_configure(self, index, minimum, maximum):
        self._set_channel_minimum_frequency(index, minimum)
        self._set_channel_maximum_frequency(index, maximum)
    
    
class TimeIntervalStopHoldoff(object):
    "Extension IVI methods for frequency counters that support setting a delay time for the time interval functions"
    
    def __init__(self, *args, **kwargs):
        super(TimeIntervalStopHoldoff, self).__init__(*args, **kwargs)
        
        cls = 'IviCounter'
        grp = 'TimeIntervalStopHoldoff'
        ivi.add_group_capability(self, cls+grp)
        
        self._time_interval_stop_holdoff = 0.0
        
        ivi.add_property(self, 'time_interval.stop_holdoff',
                        self._get_time_interval_stop_holdoff,
                        self._set_time_interval_stop_holdoff,
                        None,
                        ivi.Doc("""
                        Specifies the stop holdoff time for a Time Interval measurement. The stop
                        holdoff time is the time from the Time Interval Start Channel Trigger
                        until the Time Interval Stop Channel Trigger is enabled. The units are
                        seconds.
                        
                        Note: Many counters have a small, non-zero value as the minimum value for
                        this attribute. To configure the instrument to use the shortest stop
                        hold-off, the user can specify a value of zero for this attribute.
                        Therefore, the IVI Class-Compliant specific driver shall coerce any value
                        between zero and the minimum value to the minimum value. No other coercion
                        is allowed on this attribute.
                        """, cls, grp, '6.2.1'))
        
    def _get_time_interval_stop_holdoff(self):
        return self._time_interval_stop_holdoff
    
    def _set_time_interval_stop_holdoff(self, value):
        index = ivi.get_index(self._channel_name)
        self._time_interval_stop_holdoff[index] = value
    
    
class VoltageMeasurement(object):
    "Extension IVI methods for frequency counters that support taking voltage measurements on the input signal"
    
    def __init__(self, *args, **kwargs):
        super(VoltageMeasurement, self).__init__(*args, **kwargs)
        
        cls = 'IviCounter'
        grp = 'VoltageMeasurement'
        ivi.add_group_capability(self, cls+grp)
        
        self._voltage_channel = 0
        self._voltage_estimate = 0
        self._voltage_resolution = 0.01
        
        ivi.add_property(self, 'voltage.channel',
                        self._get_voltage_channel,
                        self._set_voltage_channel,
                        None,
                        ivi.Doc("""
                        Specifies the input channel the voltage is measured on.
                        """, cls, grp, '7.2.1'))
        ivi.add_property(self, 'voltage.estimate',
                        self._get_voltage_estimate,
                        self._set_voltage_estimate,
                        None,
                        ivi.Doc("""
                        Specifies the estimated voltage, in volts, for the voltage function.
                        """, cls, grp, '7.2.2'))
        ivi.add_property(self, 'voltage.resolution',
                        self._get_voltage_resolution,
                        self._set_voltage_resolution,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the measurement, in volts, for the voltage
                        function.
                        """, cls, grp, '7.2.3'))
        ivi.add_method(self, 'voltage.configure',
                        self._voltage_configure,
                        ivi.Doc("""
                        Configures the voltage function, the estimate, and the resolution
                        attributes for a voltage measurement.
                        """, cls, grp, '7.3.1'))
    
    def _get_voltage_channel(self):
        return self._voltage_channel
    
    def _set_voltage_channel(self, value):
        index = ivi.get_index(self._channel_name, value)
        self._voltage_channel = index
    
    def _get_voltage_estimate(self):
        return self._voltage_estimate
    
    def _set_voltage_estimate(self, value):
        value = float(value)
        self._voltage_estimate = value
    
    def _get_voltage_resolution(self):
        return self._voltage_resolution
    
    def _set_voltage_resolution(self, value):
        value = float(value)
        self._voltage_resolution = value
    
    def _voltage_configure(self, channel, measurement_function, estimate, resolution):
        self._set_measurement_function(measurement_function)
        self._set_voltage_channel(channel)
        self._set_voltage_estimate(estimate)
        self._set_voltage_resolution(resolution)


class EdgeTimeReferenceLevels(object):
    "Extension IVI methods for frequency counters that support taking percentage based edge time measurements"
    
    def __init__(self, *args, **kwargs):
        super(EdgeTimeReferenceLevels, self).__init__(*args, **kwargs)
        
        cls = 'IviCounter'
        grp = 'EdgeTimeReferenceLevels'
        ivi.add_group_capability(self, cls+grp)


