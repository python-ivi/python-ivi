"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013-2014 Alex Forencich

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
ApertureTimeUnits = set(['seconds', 'powerline_cycles'])
Auto = set(['off', 'on', 'once'])
Auto2 = set(['off', 'on'])
MeasurementFunction = set(['dc_volts', 'ac_volts', 'dc_current', 'ac_current',
                'two_wire_resistance', 'four_wire_resistance',
                'ac_plus_dc_volts', 'ac_plus_dc_current', 'frequency',
                'period', 'temperature'])
ThermocoupleReferenceJunctionType = set(['internal', 'fixed'])
ThermocoupleType = set(['b', 'c', 'd', 'e', 'g', 'j', 'k', 'n', 'r', 's', 't', 'u', 'v'])
TemperatureTransducerType = set(['thermocouple', 'thermistor', 'two_wire_rtd', 'four_wire_rtd'])
Slope = set(['positive', 'negative'])

class Base(object):
    "Base IVI methods for DMMs that take a single measurement at a time"
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._measurement_function = 'dc_volts'
        self._range = 0
        self._auto_range = 'off'
        self._resolution = 1
        
        self._trigger_delay = 0
        self._trigger_delay_auto = False
        self._trigger_source = ''
        
        ivi.add_property(self, 'trigger.delay',
                        self._get_trigger_delay,
                        self._set_trigger_delay)
        ivi.add_property(self, 'trigger.delay_auto',
                        self._get_trigger_delay_auto,
                        self._set_trigger_delay_auto)
        ivi.add_property(self, 'trigger.source',
                        self._get_trigger_source,
                        self._set_trigger_source)
        ivi.add_method(self, 'trigger.configure',
                        self._trigger_configure)
        ivi.add_method(self, 'measurement.abort',
                        self._measurement_abort)
        ivi.add_method(self, 'measurement.fetch',
                        self._measurement_fetch)
        ivi.add_method(self, 'measurement.initiate',
                        self._measurement_initiate)
        ivi.add_method(self, 'measurement.is_out_of_range',
                        self._measurement_is_out_of_range)
        ivi.add_method(self, 'measurement.is_over_range',
                        self._measurement_is_over_range)
        ivi.add_method(self, 'measurement.is_under_range',
                        self._measurement_is_under_range)
        ivi.add_method(self, 'measurement.read',
                        self._measurement_read)
    
    def _get_measurement_function(self):
        return self._measurement_function
    
    def _set_measurement_function(self, value):
        if value not in MeasurementFunction:
            raise ivi.ValueNotSupportedException()
        self._measurement_function = value
    
    measurement_function = property(lambda self: self._get_measurement_function(),
                                    lambda self, value: self._set_measurement_function(value))
    
    def _get_range(self):
        return self._range
    
    def _set_range(self, value):
        value = float(value)
        self._range = value
    
    range = property(lambda self: self._get_range(),
                     lambda self, value: self._set_range(value))
    
    def _get_auto_range(self):
        return self._auto_range
    
    def _set_auto_range(self, value):
        if value not in Auto:
            raise ivi.ValueNotSupportedException()
        self._auto_range = value
    
    auto_range = property(lambda self: self._get_auto_range(),
                          lambda self, value: self._set_auto_range(value))
    
    def _get_resolution(self):
        return self._resolution
    
    def _set_resolution(self, value):
        value = float(value)
        self._resolution = value
    
    resolution = property(lambda self: self._get_resolution(),
                          lambda self, value: self._set_resolution(value))
    
    def _get_trigger_delay(self):
        return self._trigger_delay
    
    def _set_trigger_delay(self, value):
        value = float(value)
        self._trigger_delay = value
    
    def _get_trigger_delay_auto(self):
        return self._trigger_delay_auto
    
    def _set_trigger_delay_auto(self, value):
        value = bool(value)
        self._trigger_delay_auto = value
    
    def _get_trigger_source(self):
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        value = str(value)
        self._trigger_source = value
    
    def _measurement_abort(self):
        pass
    
    def configure(self, function, range, resolution):
        self._set_measurement_function(self, function)
        if range in Auto:
            self._set_auto_range(range)
        else:
            self._set_range(range)
        self._set_resolution(resolution)
    
    def _trigger_configure(self, source, delay):
        self._set_trigger_source(source)
        if isinstance(delay, bool):
            self._set_trigger_auto_delay(delay)
        else:
            self._set_trigger_delay(delay)
    
    def _measurement_fetch(self, max_time):
        return 0.0
    
    def _measurement_initiate(self):
        pass
    
    def _measurement_is_out_of_range(self, value):
        return self._measurement_is_over_range(value) or self._measurement_is_under_range(value)
    
    def _measurement_is_over_range(self, value):
        return False
    
    def _measurement_is_under_range(self, value):
        return False
    
    def _measurement_read(self, max_time):
        return 0.0
    
    
class ACMeasurement(object):
    "Extension IVI methods for DMMs that can take AC voltage or AC current measurements"
    
    def __init__(self, *args, **kwargs):
        super(ACMeasurement, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'ACMeasurement'
        ivi.add_group_capability(self, cls+grp)
        
        self._ac_frequency_max = 100
        self._ac_frequency_min = 10
        
        ivi.add_property(self, 'ac.frequency_max',
                        self._get_ac_frequency_max,
                        self._set_ac_frequency_max)
        ivi.add_property(self, 'ac.frequency_min',
                        self._get_ac_frequency_min,
                        self._set_ac_frequency_min)
        ivi.add_method(self, 'ac.configure_bandwidth',
                        self._ac_configure_bandwidth)
        
    
    def _get_ac_frequency_max(self):
        return self._ac_frequency_max
    
    def _set_ac_frequency_max(self, value):
        value = float(value)
        self._ac_frequency_max = value
    
    def _get_ac_frequency_min(self):
        return self._ac_frequency_min
    
    def _set_ac_frequency_min(self, value):
        value = float(value)
        self._ac_frequency_min = value
    
    def _ac_configure_bandwidth(self, min_f, max_f):
        self._set_ac_frequency_min(min_f)
        self._set_ac_frequency_max(max_f)
    
    
class FrequencyMeasurement(object):
    "Extension IVI methods for DMMs that can take frequency measurements"
    
    def __init__(self, *args, **kwargs):
        super(FrequencyMeasurement, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'FrequencyMeasurement'
        ivi.add_group_capability(self, cls+grp)
        
        self._frequency_voltage_range = 1
        self._frequency_voltage_range_auto = False
        
        ivi.add_property(self, 'frequency.voltage_range',
                        self._get_frequency_voltage_range,
                        self._set_frequency_voltage_range)
        ivi.add_property(self, 'frequency.voltage_range_auto',
                        self._get_frequency_voltage_range_auto,
                        self._set_frequency_voltage_range_auto)
        
    
    def _get_frequency_range(self):
        return self._frequency_range
    
    def _set_frequency_range(self, value):
        value = float(value)
        self._frequency_range = value
    
    def _get_frequency_range_auto(self):
        return self._frequency_range_auto
    
    def _set_frequency_range_auto(self, value):
        value = bool(value)
        self._frequency_range_auto = value
    
    
class TemperatureMeasurement(object):
    "Extension IVI methods for DMMs that can take temperature measurements"
    
    def __init__(self, *args, **kwargs):
        super(TemperatureMeasurement, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'TemperatureMeasurement'
        ivi.add_group_capability(self, cls+grp)
        
        self._temperature_transducer_type = ''
        
        ivi.add_property(self, 'temperature.transducer_type',
                        self._get_temperature_transducer_type,
                        self._set_temperature_transducer_type)
        
    
    def _get_temperature_transducer_type(self):
        return self._temperature_transducer_type
    
    def _set_temperature_transducer_type(self, value):
        if value not in TemperatureTransducerType:
            raise ivi.ValueNotSupportedException()
        self._temperature_transducer_type = value
    
    
class Thermocouple(object):
    "Extension IVI methods for DMMs that can take temperature measurements using a thermocouple"
    
    def __init__(self, *args, **kwargs):
        super(Thermocouple, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'Thermocouple'
        ivi.add_group_capability(self, cls+grp)
        
        self._thermocouple_fixed_reference_junction = 25.0
        self._thermocouple_reference_junction_type = ''
        self._thermocouple_type = ''
        
        ivi.add_property(self, 'thermocouple.fixed_reference_junction',
                        self._get_thermocouple_fixed_reference_junction,
                        self._set_thermocouple_fixed_reference_junction)
        ivi.add_property(self, 'thermocouple.reference_junction_type',
                        self._get_thermocouple_reference_junction_type,
                        self._set_thermocouple_reference_junction_type)
        ivi.add_property(self, 'thermocouple.type',
                        self._get_thermocouple_type,
                        self._set_thermocouple_type)
        ivi.add_method(self, 'thermocouple.configure',
                        self._thermocouple_configure)
        
    
    def _get_thermocouple_fixed_reference_junction(self):
        return self._thermocouple_fixed_reference_junction
    
    def _set_thermocouple_fixed_reference_junction(self, value):
        value = float(value)
        self._thermocouple_fixed_reference_junction = value
    
    def _get_thermocouple_reference_junction_type(self):
        return self._thermocouple_reference_junction_type
    
    def _set_thermocouple_reference_junction_type(self, value):
        if value not in ThermocoupleReferenceJunctionType:
            raise ivi.ValueNotSupportedException()
        self._thermocouple_reference_junction_type = value
    
    def _get_thermocouple_type(self):
        return self._thermocouple_type
    
    def _set_thermocouple_type(self, value):
        if value not in ThermocoupleType:
            raise ivi.ValueNotSupportedException()
        self._thermocouple_type = value
    
    def _thermocouple_configure(self, thermocouple_type, reference_junction_type):
        self._set_thermocouple_type(thermocouple_type)
        self._set_thermocouple_reference_junction_type(reference_junction_type)
    
    
class ResistanceTemperatureDevice(object):
    "Extension IVI methods for DMMs that can take temperature measurements using a resistance temperature device (RTD)"
    
    def __init__(self, *args, **kwargs):
        super(ResistanceTemperatureDevice, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'ResistanceTemperatureDevice'
        ivi.add_group_capability(self, cls+grp)
        
        self._rtd_alpha = 0.00385
        self._rtd_resistance = 100
        
        ivi.add_property(self, 'rtd.alpha',
                        self._get_rtd_alpha,
                        self._set_rtd_alpha)
        ivi.add_property(self, 'rtd.resistance',
                        self._get_rtd_resistance,
                        self._set_rtd_resistance)
        ivi.add_method(self, 'rtd.configure',
                        self._rtd_configure)
        
    
    def _get_rtd_alpha(self):
        return self._rtd_alpha
    
    def _set_rtd_alpha(self, value):
        value = float(value)
        self._rtd_alpha = value
    
    def _get_rtd_resistance(self):
        return self._rtd_resistance
    
    def _set_rtd_resistance(self, value):
        value = float(value)
        self._rtd_resistance = value
    
    def _rtd_configure(self, alpha, resistance):
        self._set_rtd_alpha(alpha)
        self._set_rtd_resistance(resistance)
    
    
class Thermistor(object):
    "Extension IVI methods for DMMs that can take temperature measurements using a thermistor"
    
    def __init__(self, *args, **kwargs):
        super(Thermistor, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'Thermistor'
        ivi.add_group_capability(self, cls+grp)
        
        self._thermistor_resistance = 10000
        
        ivi.add_property(self, 'thermistor.resistance',
                        self._get_thermistor_resistance,
                        self._set_thermistor_resistance)
        
    
    def _get_thermistor_resistance(self):
        return self._thermistor_resistance
    
    def _set_thermistor_resistance(self, value):
        value = float(value)
        self._thermistor_resistance = value
    
    
class MultiPoint(object):
    "Extension IVI methods for DMMs capable of acquiring measurements based on multiple triggers"
    
    def __init__(self, *args, **kwargs):
        super(MultiPoint, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'MultiPoint'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_measurement_complete_destination = ""
        self._trigger_multi_point_sample_count = 1
        self._trigger_multi_point_sample_interval = 1.0
        self._trigger_multi_point_sample_trigger = ""
        self._trigger_multi_point_count = 1
        
        ivi.add_property(self, 'trigger.measurement_complete_destination',
                        self._get_trigger_measurement_complete_destination,
                        self._set_trigger_measurement_complete_destination)
        ivi.add_property(self, 'trigger.multi_point.sample_count',
                        self._get_trigger_multi_point_sample_count,
                        self._set_trigger_multi_point_sample_count)
        ivi.add_property(self, 'trigger.multi_point.sample_interval',
                        self._get_trigger_multi_point_sample_interval,
                        self._set_trigger_multi_point_sample_interval)
        ivi.add_property(self, 'trigger.multi_point.sample_trigger',
                        self._get_trigger_multi_point_sample_trigger,
                        self._set_trigger_multi_point_sample_trigger)
        ivi.add_property(self, 'trigger.multi_point.count',
                        self._get_trigger_multi_point_count,
                        self._set_trigger_multi_point_count)
        ivi.add_method(self, 'trigger.multi_point.configure',
                        self._trigger_multi_point_configure)
        ivi.add_method(self, 'measurement.fetch_multi_point',
                        self._measurement_fetch_multi_point)
        ivi.add_method(self, 'measurement.read_multi_point',
                        self._measurement_read_multi_point)
        
    
    def _get_trigger_measurement_complete_destination(self):
        return self._trigger_measurement_complete_destination
    
    def _set_trigger_measurement_complete_destination(self, value):
        value = str(value)
        self._trigger_measurement_complete_destination = value
    
    def _get_trigger_multi_point_sample_count(self):
        return self._trigger_multi_point_sample_count
    
    def _set_trigger_multi_point_sample_count(self, value):
        value = int(value)
        self._trigger_multi_point_sample_count = value
    
    def _get_trigger_multi_point_sample_interval(self):
        return self._trigger_multi_point_sample_interval
    
    def _set_trigger_multi_point_sample_interval(self, value):
        value = int(value)
        self._trigger_multi_point_sample_interval = value
    
    def _get_trigger_multi_point_sample_trigger(self):
        return self._trigger_multi_point_sample_trigger
    
    def _set_trigger_multi_point_sample_trigger(self, value):
        value = str(value)
        self._trigger_multi_point_sample_trigger = value
    
    def _get_trigger_multi_point_count(self):
        return self._trigger_multi_point_count
    
    def _set_trigger_multi_point_count(self, value):
        value = int(value)
        self._trigger_multi_point_count = value
    
    def _trigger_multi_point_configure(self, trigger_count, sample_count, sample_trigger, sample_interval):
        self._set_trigger_multi_point_count(trigger_count)
        self._set_trigger_multi_point_sample_count(sample_count)
        self._set_trigger_multi_point_sample_trigger(sample_trigger)
        self._set_trigger_multi_point_sample_interval(sample_interval)
    
    def _measurement_fetch_multi_point(self, max_time, num_of_measurements = 0):
        pass
    
    def _measurement_read_multi_point(self, max_time, num_of_measurements = 0):
        pass
    
    
class TriggerSlope(object):
    "Extension IVI methods for DMMs that can specify the polarity of the external trigger signal"
    
    def __init__(self, *args, **kwargs):
        super(TriggerSlope, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'TriggerSlope'
        ivi.add_group_capability(self, cls+grp)
        
        self._trigger_slope = 'positive'
        
        ivi.add_property(self, 'trigger.slope',
                        self._get_trigger_slope,
                        self._set_trigger_slope)
        
    
    def _get_trigger_slope(self):
        return self._trigger_slope
    
    def _set_trigger_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_slope = value
    
    
class SoftwareTrigger(object):
    "Extension IVI methods for DMMs that can initiate a measurement based on a software trigger signal"
    
    def __init__(self, *args, **kwargs):
        super(SoftwareTrigger, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'SoftwareTrigger'
        ivi.add_group_capability(self, cls+grp)
        
        self.__dict__.setdefault('_docs', dict())
        self._docs['send_software_trigger'] = ivi.Doc("""
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
                        """, cls, grp, '13.2.1', 'send_software_trigger')
    
    def send_software_trigger(self):
        pass
    
    
class DeviceInfo(object):
    "A set of read-only attributes for DMMs that can be queried to determine how they are presently configured"
    
    def __init__(self, *args, **kwargs):
        super(DeviceInfo, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'DeviceInfo'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_aperture_time = 1.0
        self._advanced_aperture_time_units = 'seconds'
        
        ivi.add_property(self, 'advanced.aperture_time',
                        self._get_advanced_aperture_time)
        ivi.add_property(self, 'advanced.aperture_time_units',
                        self._get_advanced_aperture_time_units)
        
    
    def _get_advanced_aperture_time(self):
        return self._advanced_aperture_time
    
    def _get_advanced_aperture_time_units(self):
        return self._advanced_aperture_time_units
    
    
class AutoRangeValue(object):
    "Extension IVI methods for DMMs that can return the actual range value when auto ranging"
    
    def __init__(self, *args, **kwargs):
        super(AutoRangeValue, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'AutoRangeValue'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_actual_range = 1.0
        
        ivi.add_property(self, 'advanced.actual_range',
                        self._get_advanced_actual_range)
        
    
    def _get_advanced_actual_range(self):
        return self._advanced_actual_range
    
    
class AutoZero(object):
    "Extension IVI methods for DMMs that can take an auto zero reading"
    
    def __init__(self, *args, **kwargs):
        super(AutoZero, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'AutoZero'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_auto_zero = 'off'
        
        ivi.add_property(self, 'advanced.auto_zero',
                        self._get_advanced_auto_zero,
                        self._set_advanced_auto_zero)
        
    
    def _get_advanced_auto_zero(self):
        return self._advanced_auto_zero
    
    def _set_advanced_auto_zero(self, value):
        if value not in Auto:
            return ivi.ValueNotSupportedException
        self._advanced_auto_zero = value
    
    
class PowerLineFrequency(object):
    "Extension IVI methods for DMMs that can specify the power line frequency"
    
    def __init__(self, *args, **kwargs):
        super(PowerLineFrequency, self).__init__(*args, **kwargs)
        
        cls = 'IviDmm'
        grp = 'PowerLineFrequency'
        ivi.add_group_capability(self, cls+grp)
        
        self._advanced_power_line_frequency = 60.0
        
        ivi.add_property(self, 'advanced.power_line_frequency',
                        self._get_advanced_power_line_frequency,
                        self._set_advanced_power_line_frequency)
        
    
    def _get_advanced_power_line_frequency(self):
        return self._advanced_power_line_frequency
    
    def _set_advanced_power_line_frequency(self, value):
        value = float(value)
        self._advanced_power_line_frequency = value
    
    

