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

# Parameter Values
InternalTriggerSlope = set(['negative', 'positive'])
Units = set(['dBm', 'dBmV', 'dBuV', 'Watts'])
Operator = set(['none', 'difference', 'sum', 'quotient'])
RangeType = set(['in_range', 'under_range', 'over_range'])
OperationState = set(['complete', 'in_progress', 'unknown'])


class Base(object):
    "Base IVI methods for all RF power meters"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(Base, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_name = list()
        self._channel_averaging_count_auto = list()
        self._channel_correction_frequency = list()
        self._channel_offset = list()
        self._channel_range_auto = list()
        self._channel_units = list()
        
        self._measurement_measurement_state = 'unknown'
        
        ivi.add_property(self, 'channels[].averaging.count_auto',
                        self._get_channel_averaging_count_auto,
                        self._set_channel_averaging_count_auto)
        ivi.add_property(self, 'channels[].correction_frequency',
                        self._get_channel_correction_frequency,
                        self._set_channel_correction_frequency)
        ivi.add_property(self, 'channels[].offset',
                        self._get_channel_offset,
                        self._set_channel_offset)
        ivi.add_property(self, 'channels[].range_auto',
                        self._get_channel_range_auto,
                        self._set_channel_range_auto)
        ivi.add_property(self, 'channels[].units',
                        self._get_channel_units,
                        self._set_channel_units)
        ivi.add_property(self, 'measurement.measurement_state',
                        self._get_measurement_measurement_state)
        ivi.add_method(self, 'measurement.abort',
                        self._measurement_abort)
        ivi.add_method(self, 'measurement.configure',
                        self._measurement_configure)
        ivi.add_method(self, 'measurement.fetch',
                        self._measurement_fetch)
        ivi.add_method(self, 'measurement.initiate',
                        self._measurement_initiate)
        ivi.add_method(self, 'measurement.read',
                        self._measurement_read)
        
        self._init_channels()
    
    
    
    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_averaging_count_auto = list()
        self._channel_correction_frequency = list()
        self._channel_offset = list()
        self._channel_range_auto = list()
        self._channel_units = list()
        for i in range(self._channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_averaging_count_auto.append(True)
            self._channel_correction_frequency.append(10e6)
            self._channel_offset.append(0.0)
            self._channel_range_auto.append(True)
            self._channel_units.append('dBm')
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_averaging_count_auto(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_averaging_count_auto[index]
    
    def _set_channel_averaging_count_auto(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_averaging_count_auto[index] = value
    
    def _get_channel_correction_frequency(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_correction_frequency[index]
    
    def _set_channel_correction_frequency(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_correction_frequency[index] = value
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_offset[index] = value
    
    def _get_channel_range_auto(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range_auto[index]
    
    def _set_channel_range_auto(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_range_auto[index] = value
    
    def _get_channel_units(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_units[index]
    
    def _set_channel_units(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        if value not in Units:
            raise ivi.ValueNotSupportedException()
        self._channel_units[index] = value
    
    def _get_measurement_measurement_state(self):
        return self._measurement_measurement_state
    
    def _measurement_abort(self):
        pass
    
    def _measurement_configure(self, operator, operand1, operand2):
        pass
    
    def _measurement_fetch(self):
        return 0
    
    def _measurement_initiate(self):
        pass
    
    def _measurement_read(self, maximum_time):
        self._measurement_initiate()
        return self._measurement_fetch()
    
    
class ChannelAcquisition(object):
    "Extension IVI methods for RF power meters supporting simultaneous measurements on two or more channels"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(ChannelAcquisition, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'ChannelAcquisition'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_enabled = list()
        
        ivi.add_property(self, 'channels[].enabled',
                        self._get_channel_enabled,
                        self._set_channel_enabled)
        ivi.add_method(self, 'channels[].fetch',
                        self._measurement_fetch_channel)
        ivi.add_method(self, 'channels[].read',
                        self._measurement_read_channel)
        ivi.add_method(self, 'measurement.fetch_channel',
                        self._measurement_fetch_channel)
        ivi.add_method(self, 'measurement.read_channel',
                        self._measurement_read_channel)
        
        self._init_channels()
    
    def _init_channels(self):
        try:
            super(ChannelAcquisition, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_enabled = list()
        for i in range(self._channel_count):
            self._channel_enabled.append(True)
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_enabled[index]
    
    def _set_channel_enabled(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_enabled[index] = value
    
    def _measurement_fetch_channel(self, index):
        index = ivi.get_index(self._channel_name, index)
        return 0
    
    def _measurement_read_channel(self, index, maximum_time):
        index = ivi.get_index(self._channel_name, index)
        pass
    
    
class ManualRange(object):
    "Extension IVI methods for RF power meters supporting manual range selection"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(ManualRange, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'ManualRange'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_range_lower = list()
        self._channel_range_upper = list()
        
        ivi.add_property(self, 'channels[].range.lower',
                        self._get_channel_range_lower,
                        self._set_channel_range_lower)
        ivi.add_property(self, 'channels[].range.upper',
                        self._get_channel_range_upper,
                        self._set_channel_range_upper)
        ivi.add_method(self, 'channels[].range.configure',
                        self._channel_range_configure)
        
        self._init_channels()
    
    def _init_channels(self):
        try:
            super(ManualRange, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_range_lower = list()
        self._channel_range_upper = list()
        for i in range(self._channel_count):
            self._channel_range_lower.append(0.0)
            self._channel_range_upper.append(0.0)
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_range_lower(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range_lower[index]
    
    def _set_channel_range_lower(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_range_lower[index] = value
    
    def _get_channel_range_upper(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_range_upper[index]
    
    def _set_channel_range_upper(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_range_upper[index] = value
    
    def _channel_range_configure(self, index, lower, upper):
        self._set_channel_range_lower(index, lower)
        self._set_channel_range_lower(index, upper)
    
    
class TriggerSource(object):
    "Extension IVI methods for RF power meters supporting triggering"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(TriggerSource, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'TriggerSource'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_source = ''
        
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        ivi.add_property(self, 'trigger.source',
                        self._get_trigger_source,
                        self._set_trigger_source)
    
    def _get_trigger_source(self):
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        value = str(value)
        self._trigger_source = value
    
    
class InternalTrigger(object):
    "Extension IVI methods for RF power meters supporting internal triggering"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(InternalTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'InternalTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_internal_event_source = ''
        self._trigger_internal_level = 0.0
        self._trigger_internal_slope = 'positive'
        
        ivi.add_property(self, 'trigger.internal.event_source',
                        self._get_trigger_internal_event_source,
                        self._set_trigger_internal_event_source)
        ivi.add_property(self, 'trigger.internal.level',
                        self._get_trigger_internal_level,
                        self._set_trigger_internal_level)
        ivi.add_property(self, 'trigger.internal.slope',
                        self._get_trigger_internal_slope,
                        self._set_trigger_internal_slope)
        ivi.add_method(self, 'trigger.internal.configure',
                        self._trigger_internal_configure)
    
    def _get_trigger_internal_event_source(self):
        return self._trigger_internal_event_source
    
    def _set_trigger_internal_event_source(self, value):
        value = str(value)
        self._trigger_internal_event_source = value
    
    def _get_trigger_internal_level(self):
        return self._trigger_internal_level
    
    def _set_trigger_internal_level(self, value):
        value = float(value)
        self._trigger_internal_level = value
    
    def _get_trigger_internal_slope(self):
        return self._trigger_internal_slope
    
    def _set_trigger_internal_slope(self, value):
        if value not in InternalTriggerSlope:
            raise ivi.ValueNotSupportedException()
        self._trigger_internal_slope = value
    
    def _trigger_internal_configure(self, event_source, slope):
        self._set_trigger_internal_event_source(event_source)
        self._set_trigger_internal_event_source(slope)
    
    
class SoftwareTrigger(object):
    "Extension IVI methods for RF power meters supporting software triggering"
    
    def __init__(self, *args, **kwargs):
        super(SoftwareTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'SoftwareTrigger'
        ivi.add_group_capability(self, cls+grp)
    
    def send_software_trigger(self):
        pass
    
    
class DutyCycleCorrection(object):
    "Extension IVI methods for RF power meters supporting duty cycle correction of pulse modulated signals"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(DutyCycleCorrection, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'DutyCycleCorrection'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_duty_cycle_enabled = list()
        self._channel_duty_cycle_value = list()
        
        ivi.add_property(self, 'channels[].duty_cycle.enabled',
                        self._get_channel_duty_cycle_enabled,
                        self._set_channel_duty_cycle_enabled)
        ivi.add_property(self, 'channels[].duty_cycle.value',
                        self._get_channel_duty_cycle_value,
                        self._set_channel_duty_cycle_value)
        ivi.add_method(self, 'channels[].duty_cycle.configure',
                        self._channel_duty_cycle_configure)
        
        self._init_channels()
    
    def _init_channels(self):
        try:
            super(DutyCycleCorrection, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_duty_cycle_enabled = list()
        self._channel_duty_cycle_value = list()
        for i in range(self._channel_count):
            self._channel_duty_cycle_enabled.append(True)
            self._channel_duty_cycle_value.append(50.0)
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_duty_cycle_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_duty_cycle_enabled[index]
    
    def _set_channel_duty_cycle_enabled(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_duty_cycle_enabled[index] = value
    
    def _get_channel_duty_cycle_value(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_duty_cycle_value[index]
    
    def _set_channel_duty_cycle_value(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        self._channel_duty_cycle_value[index] = value
    
    def _channel_duty_cycle_configure(self, index, enabled, correction):
        self._set_channel_duty_cycle_enabled(enabled)
        self._set_channel_duty_cycle_value(correction)
    
    
class AveragingCount(object):
    "Extension IVI methods for RF power meters supporting averaging"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(AveragingCount, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'AveragingCount'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_averaging_count = list()
        
        ivi.add_property(self, 'channels[].averaging.count',
                        self._get_channel_averaging_count,
                        self._set_channel_averaging_count)
        
        self._init_channels()
    
    def _init_channels(self):
        try:
            super(AveragingCount, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_averaging_count = list()
        for i in range(self._channel_count):
            self._channel_averaging_count.append(1)
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_averaging_count(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_averaging_count[index]
    
    def _set_channel_averaging_count(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = int(value)
        self._channel_averaging_count[index] = value
    
    
class ZeroCorrection(object):
    "Extension IVI methods for RF power meters supporting zero correction"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(ZeroCorrection, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'ZeroCorrection'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_zero_state = list()
        
        ivi.add_property(self, 'channels[].zero_state',
                        self._get_channel_zero_state)
        ivi.add_method(self, 'channels[].zero',
                        self._channel_zero)
        
        self._init_channels()
    
    def _init_channels(self):
        try:
            super(ZeroCorrection, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_zero_state = list()
        for i in range(self._channel_count):
            self._channel_zero_state.append('unknown')
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_zero_state(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_zero_state[index]
    
    def _channel_zero(self, index):
        index = ivi.get_index(self._channel_name, index)
        pass
    
    def zero_all_channels(self):
        for i in range(self._channel_count):
            self._channel_zero(i)
    
    
class Calibration(object):
    "Extension IVI methods for RF power meters supporting calibration"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(Calibration, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'Calibration'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_calibration_state = list()
        
        ivi.add_property(self, 'channels[].calibration_state',
                        self._get_channel_calibration_state)
        ivi.add_method(self, 'channels[].calibrate',
                        self._channel_calibrate)
        
        self._init_channels()
    
    def _init_channels(self):
        try:
            super(Calibration, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_calibration_state = list()
        for i in range(self._channel_count):
            self._channel_calibration_state.append('unknown')
        
        self.channels._set_list(self._channel_name)
    
    def _get_channel_calibration_state(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_calibration_state[index]
    
    def _channel_calibrate(self, index):
        index = ivi.get_index(self._channel_name, index)
        pass
    
    
class ReferenceOscillator(object):
    "Extension IVI methods for RF power meters with built-in reference oscillators"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(ReferenceOscillator, self).__init__(*args, **kwargs)
        
        cls = 'IviPwrMeter'
        grp = 'ReferenceOscillator'
        ivi.add_group_capability(self, cls+grp)
        
        self._reference_oscillator_enabled = False
        self._reference_oscillator_frequency = 10e6
        self._reference_oscillator_level = 0.0
        
        self.__dict__.setdefault('reference_oscillator', ivi.PropertyCollection())
        ivi.add_property(self, 'reference_oscillator.enabled',
                        self._get_reference_oscillator_enabled,
                        self._set_reference_oscillator_enabled)
        ivi.add_property(self, 'reference_oscillator.frequency',
                        self._get_reference_oscillator_frequency,
                        self._set_reference_oscillator_frequency)
        ivi.add_property(self, 'reference_oscillator.level',
                        self._get_reference_oscillator_level,
                        self._set_reference_oscillator_level)
        ivi.add_method(self, 'reference_oscillator.configure',
                        self._reference_oscillator_configure)
    
    def _get_reference_oscillator_enabled(self):
        return self._reference_oscillator_enabled
    
    def _set_reference_oscillator_enabled(self, value):
        value = bool(value)
        self._reference_oscillator_enabled = value
    
    def _get_reference_oscillator_frequency(self):
        return self._reference_oscillator_frequency
    
    def _set_reference_oscillator_frequency(self, value):
        value = float(value)
        self._reference_oscillator_frequency = value
    
    def _get_reference_oscillator_level(self):
        return self._reference_oscillator_level
    
    def _set_reference_oscillator_level(self, value):
        value = float(value)
        self._reference_oscillator_level = value
    
    def _reference_oscillator_configure(self, frequency, level):
        self._set_reference_oscillator_frequency(frequency)
        self._set_reference_oscillator_level(level)
    
    


