"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013 Alex Forencich

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
Auto = set(['Off', 'On', 'Once'])
Auto2 = set(['Off', 'On'])
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
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviDmmBase')
        
        self._measurement_function = 'dc_volts'
        self._range = 0
        self._auto_range = 'off'
        self._resolution = 1
        
        self._trigger_delay = 0
        self._trigger_auto_delay = False
        self._trigger_source = ''
        
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger._add_property('delay',
                        self._get_trigger_delay,
                        self._set_trigger_delay)
        self.trigger._add_property('delay_auto',
                        self._get_trigger_delay_auto,
                        self._set_trigger_delay_auto)
        self.trigger.configure = self._trigger_configure
        
        self.__dict__.setdefault('measurement', ivi.PropertyCollection())
        self.measurement.abort = self._measurement_abort
        self.measurement.fetch = self._measurement_fetch
        self.measurement.initiate = self._measurement_initiate
        self.measurement.is_out_of_range = self._measurement_is_out_of_range
        self.measurement.is_over_range = self._measurement_is_over_range
        self.measurement.is_under_range = self._measurement_is_under_range
        self.measurement.read = self._measurement_read
    
    def _get_measurement_function(self):
        return self._measurement_function
    
    def _set_measurement_function(self, value):
        if value not in MeasurementFunction:
            raise ivi.ValueNotSupportedException()
        self._measurement_function = value
    
    measurement_function = property(_get_measurement_function, _set_measurement_function)
    
    def _get_range(self):
        return self._range
    
    def _set_range(self, value):
        value = float(value)
        self._range = value
    
    range = property(_get_range, _set_range)
    
    def _get_auto_range(self):
        return self._auto_range
    
    def _set_auto_range(self, value):
        if value not in Auto:
            raise ivi.ValueNotSupportedException()
        self._auto_range = value
    
    auto_range = property(_get_auto_range, _set_auto_range)
    
    def _get_resolution(self):
        return self._resolution
    
    def _set_resolution(self, value):
        value = float(value)
        self._resolution = value
    
    resolution = property(_get_resolution, _set_resolution)
    
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
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviDmmACMeasurement')
        
        self._ac_frequency_max = 100
        self._ac_frequency_min = 10
        
        self.__dict__.setdefault('ac', ivi.PropertyCollection())
        self.ac._add_property('frequency_max',
                        self._get_ac_frequency_max,
                        self._set_ac_frequency_max)
        self.ac._add_property('frequency_min',
                        self._get_ac_frequency_min,
                        self._set_ac_frequency_min)
        self.ac.configure_bandwidth = self._ac_configure_bandwidth
        
    
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
        super().__init__(*args, **kwargs)
        
        self._add_group_capability('IviDmmFrequencyMeasurement')
        
        self._frequency_voltage_range = 1
        self._frequency_voltage_range_auto = False
        
        self.__dict__.setdefault('frequency', ivi.PropertyCollection())
        self.frequency._add_property('voltage_range',
                        self._get_frequency_voltage_range,
                        self._set_frequency_voltage_range)
        self.frequency._add_property('voltage_range_auto',
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
    
    
# TemperatureMeasurement
# Thermocouple
# ResistanceTemperatureDevice
# Thermistor
# MultiPoint
# TriggerSlope
# SoftwareTrigger
# DeviceInfo
# AutoRangeValue
# AutoZero
# PowerLineFrequency

