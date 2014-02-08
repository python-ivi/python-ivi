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

class Base(object):
    "Base IVI methods for all oscilloscpes"
    
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
        
        ivi.add_property(self, 'acquisition.start_time',
                        self._get_acquisition_start_time,
                        self._set_acquisition_start_time)
        ivi.add_property(self, 'acquisition.type',
                        self._get_acquisition_type,
                        self._set_acquisition_type)
        ivi.add_property(self, 'acquisition.number_of_points_minimum',
                        self._get_acquisition_number_of_points_minimum,
                        self._set_acquisition_number_of_points_minimum)
        ivi.add_property(self, 'acquisition.record_length',
                        self._get_acquisition_record_length)
        ivi.add_property(self, 'acquisition.sample_rate',
                        self._get_acquisition_sample_rate)
        ivi.add_property(self, 'acquisition.time_per_record',
                        self._get_acquisition_time_per_record,
                        self._set_acquisition_time_per_record)
        ivi.add_method(self, 'acquisition.configure_record',
                        self._acquisition_configure_record)
        ivi.add_property(self, 'channels[].name',
                        self._get_channel_name)
        ivi.add_property(self, 'channels[].enabled',
                        self._get_channel_enabled,
                        self._set_channel_enabled)
        ivi.add_property(self, 'channels[].input_impedance',
                        self._get_channel_input_impedance,
                        self._set_channel_input_impedance)
        ivi.add_property(self, 'channels[].input_frequency_max',
                        self._get_channel_input_frequency_max,
                        self._set_channel_input_frequency_max)
        ivi.add_property(self, 'channels[].probe_attenuation',
                        self._get_channel_probe_attenuation,
                        self._set_channel_probe_attenuation)
        ivi.add_property(self, 'channels[].coupling',
                        self._get_channel_coupling,
                        self._set_channel_coupling)
        ivi.add_property(self, 'channels[].offset',
                        self._get_channel_offset,
                        self._set_channel_offset)
        ivi.add_property(self, 'channels[].range',
                        self._get_channel_range,
                        self._set_channel_range)
        ivi.add_method(self, 'channels[].configure',
                        self._channel_configure)
        ivi.add_method(self, 'channels[].configure_characteristics',
                        self._channel_configure_characteristics)
        ivi.add_method(self, 'channels[].measurement.fetch_waveform',
                        self._measurement_fetch_waveform)
        ivi.add_method(self, 'channels[].measurement.read_waveform',
                        self._measurement_read_waveform)
        ivi.add_property(self, 'measurement.status',
                        self._get_measurement_status)
        ivi.add_method(self, 'measurement.abort',
                        self._measurement_abort)
        ivi.add_method(self, 'measurement.initiate',
                        self._measurement_initiate)
        ivi.add_property(self, 'trigger.coupling',
                        self._get_trigger_coupling,
                        self._set_trigger_coupling)
        ivi.add_property(self, 'trigger.holdoff',
                        self._get_trigger_holdoff,
                        self._set_trigger_holdoff)
        ivi.add_property(self, 'trigger.level',
                        self._get_trigger_level,
                        self._set_trigger_level)
        ivi.add_property(self, 'trigger.edge.slope',
                        self._get_trigger_edge_slope,
                        self._set_trigger_edge_slope)
        ivi.add_method(self, 'trigger.edge.configure',
                        self._trigger_edge_configure)
        ivi.add_property(self, 'trigger.source',
                        self._get_trigger_source,
                        self._set_trigger_source)
        ivi.add_property(self, 'trigger.type',
                        self._get_trigger_type,
                        self._set_trigger_type)
        ivi.add_method(self, 'trigger.configure',
                        self._trigger_configure)
        
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


class Interpolation(object):
    "Extension IVI methods for oscilloscopes supporting interpolation"
    
    def __init__(self, *args, **kwargs):
        super(Interpolation, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'Interpolation'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_interpolation = 'none'
        
        ivi.add_property(self, 'acquisition.interpolation',
                        self._get_acquisition_interpolation,
                        self._set_acquisition_interpolation)
    
    def _get_acquisition_interpolation(self):
        return self._acquisition_interpolation
    
    def _set_acquisition_interpolation(self, value):
        self._acquisition_interpolation = value


class TVTrigger(object):
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
        
        ivi.add_property(self, 'trigger.tv.trigger_event',
                        self._get_trigger_tv_trigger_event,
                        self._set_trigger_tv_trigger_event)
        ivi.add_property(self, 'trigger.tv.line_number',
                        self._get_trigger_tv_line_number,
                        self._set_trigger_tv_line_number)
        ivi.add_property(self, 'trigger.tv.polarity',
                        self._get_trigger_tv_polarity,
                        self._set_trigger_tv_polarity)
        ivi.add_property(self, 'trigger.tv.signal_format',
                        self._get_trigger_tv_signal_format,
                        self._set_trigger_tv_signal_format)
        ivi.add_method(self, 'trigger.tv.configure',
                        self._trigger_tv_configure)
    
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


class RuntTrigger(object):
    "Extension IVI methods for oscilloscopes supporting runt triggering"
    
    def __init__(self, *args, **kwargs):
        super(RuntTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'RuntTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_runt_threshold_high = 0
        self._trigger_runt_threshold_low = 0
        self._trigger_runt_polarity = 'positive'
        
        ivi.add_property(self, 'trigger.runt.threshold_high',
                        self._get_trigger_runt_threshold_high,
                        self._set_trigger_runt_threshold_high)
        ivi.add_property(self, 'trigger.runt.threshold_low',
                        self._get_trigger_runt_threshold_low,
                        self._set_trigger_runt_threshold_low)
        ivi.add_property(self, 'trigger.runt.polarity',
                        self._get_trigger_runt_polarity,
                        self._set_trigger_runt_polarity)
        ivi.add_method(self, 'trigger.runt.configure',
                        self._trigger_runt_configure)
    
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


class GlitchTrigger(object):
    "Extension IVI methods for oscilloscopes supporting glitch triggering"
    
    def __init__(self, *args, **kwargs):
        super(GlitchTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'GlitchTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_glitch_condition = 'less_than'
        self._trigger_glitch_polarity = 'positive'
        self._trigger_glitch_width = 0
        
        ivi.add_property(self, 'trigger.glitch.condition',
                        self._get_trigger_glitch_condition,
                        self._set_trigger_glitch_condition)
        ivi.add_property(self, 'trigger.glitch.polarity',
                        self._get_trigger_glitch_polarity,
                        self._set_trigger_glitch_polarity)
        ivi.add_property(self, 'trigger.glitch.width',
                        self._get_trigger_glitch_width,
                        self._set_trigger_glitch_width)
        ivi.add_method(self, 'trigger.glitch.configure',
                        self._trigger_glitch_configure)
    
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


class WidthTrigger(object):
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
        
        ivi.add_property(self, 'trigger.width.condition',
                        self._get_trigger_width_condition,
                        self._set_trigger_width_condition)
        ivi.add_property(self, 'trigger.width.threshold_high',
                        self._get_trigger_width_threshold_high,
                        self._set_trigger_width_threshold_high)
        ivi.add_property(self, 'trigger.width.threshold_low',
                        self._get_trigger_width_threshold_low,
                        self._set_trigger_width_threshold_low)
        ivi.add_property(self, 'trigger.width.polarity',
                        self._get_trigger_width_polarity,
                        self._set_trigger_width_polarity)
        ivi.add_method(self, 'trigger.width.configure',
                        self._trigger_width_configure)
    
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


class AcLineTrigger(object):
    "Extension IVI methods for oscilloscopes supporting AC line triggering"
    
    def __init__(self, *args, **kwargs):
        super(AcLineTrigger, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'AcLineTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_ac_line_slope = 'positive'
        
        ivi.add_property(self, 'trigger.ac_line.slope',
                        self._get_trigger_ac_line_slope,
                        self._set_trigger_ac_line_slope)
    
    def _get_trigger_ac_line_slope(self):
        return self._trigger_ac_line_slope
    
    def _set_trigger_ac_line_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_ac_line_slope = value
    

class WaveformMeasurement(object):
    "Extension IVI methods for oscilloscopes supporting waveform measurements"
    
    def __init__(self, *args, **kwargs):
        super(WaveformMeasurement, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'WaveformMeasurement'
        ivi.add_group_capability(self, cls+grp)
        
        self._reference_level_high = 90
        self._reference_level_low = 10
        self._reference_level_middle = 50
        
        ivi.add_property(self, 'reference_level.high',
                        self._get_reference_level_high,
                        self._set_reference_level_high)
        ivi.add_property(self, 'reference_level.middle',
                        self._get_reference_level_middle,
                        self._set_reference_level_middle)
        ivi.add_property(self, 'reference_level.low',
                        self._get_reference_level_low,
                        self._set_reference_level_low)
        ivi.add_method(self, 'reference_level.configure',
                        self._reference_level_configure)
        ivi.add_method(self, 'channels[].measurement.fetch_waveform_measurement',
                        self._measurement_fetch_waveform_measurement)
        ivi.add_method(self, 'channels[].measurement.read_waveform_measurement',
                        self._measurement_read_waveform_measurement)
    
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


class MinMaxWaveform(object):
    "Extension IVI methods for oscilloscopes supporting minimum and maximum waveform acquisition"
    
    def __init__(self, *args, **kwargs):
        super(MinMaxWaveform, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'MinMaxWaveform'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_number_of_envelopes = 0
        
        ivi.add_property(self, 'acquisition.number_of_envelopes',
                        self._get_acquisition_number_of_envelopes,
                        self._set_acquisition_number_of_envelopes)
        ivi.add_method(self, 'channels[].measurement.fetch_waveform_min_max',
                        self._measurement_fetch_waveform_min_max)
        ivi.add_method(self, 'channels[].measurement.read_waveform_min_max',
                        self._measurement_read_waveform_min_max)
    
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


class ProbeAutoSense(object):
    "Extension IVI methods for oscilloscopes supporting probe attenuation sensing"
    def __init__(self, *args, **kwargs):
        super(ProbeAutoSense, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'ProbeAutoSense'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_probe_attenuation_auto = list()
        self._channel_probe_sense = list()
        
        ivi.add_property(self, 'channels[].probe_attenuation_auto',
                        self._get_channel_probe_attenuation_auto,
                        self._set_channel_probe_attenuation_auto)
        ivi.add_property(self, 'channels[].probe_sense',
                        self._get_channel_probe_sense)
    
    def init_channels(self):
        try:
            super(ProbeAutoSense, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_probe_attenuation_auto = list()
        self._channel_probe_sense = list()
        for i in range(self._channel_count):
            self._channel_probe_attenuation_auto.append(True)
            self._channel_probe_sense.append(1)
    
    def _get_channel_probe_attenuation_auto(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_probe_attenuation_auto[index]
    
    def _set_channel_probe_attenuation_auto(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        self._channel_probe_attenuation_auto[index] = value
    
    def _get_channel_probe_sense(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_probe_sense[index]


class ContinuousAcquisition(object):
    "Extension IVI methods for oscilloscopes supporting continuous acquisition"
    
    def __init__(self, *args, **kwargs):
        super(ContinuousAcquisition, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'ContinuousAcquisition'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_continuous = False
        
        ivi.add_property(self, 'trigger.continuous',
                        self._get_trigger_continuous,
                        self._set_trigger_continuous)
    
    def _get_trigger_continuous(self):
        return self._trigger_continuous
    
    def _set_trigger_continuous(self, value):
        self._trigger_continuous = value


class AverageAcquisition(object):
    "Extension IVI methods for oscilloscopes supporting average acquisition"
    
    def __init__(self, *args, **kwargs):
        super(AverageAcquisition, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'AverageAcquisition'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_number_of_averages = 1
        
        ivi.add_property(self, 'acquisition.number_of_averages',
                        self._get_acquisition_number_of_averages,
                        self._set_acquisition_number_of_averages)
    
    def _get_acquisition_number_of_averages(self):
        return self._acquisition_number_of_averages
    
    def _set_acquisition_number_of_averages(self, value):
        self._acquisition_number_of_averages = value


class SampleMode(object):
    "Extension IVI methods for oscilloscopes supporting equivalent and real time acquisition"
    
    def __init__(self, *args, **kwargs):
        super(SampleMode, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'SampleMode'
        ivi.add_group_capability(self, cls+grp)
        
        self._acquisition_sample_mode = 'real_time'
        
        ivi.add_property(self, 'acquisition.sample_mode',
                        self._get_acquisition_sample_mode,
                        self._set_acquisition_sample_mode)
    
    def _get_acquisition_sample_mode(self):
        return self._acquisition_sample_mode
    
    def _set_acquisition_sample_mode(self, value):
        if value not in AcquisitionSampleMode:
            raise ivi.ValueNotSupportedException()
        self._acquisition_sample_mode = value


class TriggerModifier(object):
    "Extension IVI methods for oscilloscopes supporting specific triggering subsystem behavior in the absence of a trigger"
    
    def __init__(self, *args, **kwargs):
        super(TriggerModifier, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'TriggerModifier'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_modifier = 'none'
        
        ivi.add_property(self, 'trigger.modifier',
                        self._get_trigger_modifier,
                        self._set_trigger_modifier)
    
    def _get_trigger_modifier(self):
        return self._trigger_modifier
    
    def _set_trigger_modifier(self, value):
        if value not in TriggerModifier:
            raise ivi.ValueNotSupportedException()
        self._trigger_modifier = value


class AutoSetup(object):
    "Extension IVI methods for oscilloscopes supporting automatic _setup"
    
    def __init__(self, *args, **kwargs):
        super(AutoSetup, self).__init__( *args, **kwargs)
        
        cls = 'IviScope'
        grp = 'AutoSetup'
        ivi.add_group_capability(self, cls+grp)
        
        ivi.add_method(self, 'measurement.auto_setup',
                        self._measurement_auto_setup)
    
    def _measurement_auto_setup(self):
        pass

