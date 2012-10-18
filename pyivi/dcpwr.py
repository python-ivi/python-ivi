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

# Parameter Values
CurrentLimitBehavior = set(['regulate', 'trip'])
RangeType = set(['current', 'voltage'])
OutputState = set(['constant_voltage', 'constant_current', 'over_voltage',
                'over_current', 'unregulated'])
MeasurementType = set(['current', 'voltage'])


def get_range(range_list, offset, val):
    l = list()
    for i in range(len(range_list)):
        l.append((i, range_list[i][offset]))
    l.sort(key=lambda x: x[1], reverse=True)
    k = -1
    for i in range(len(l)):
        if l[i][1] >= val:
            k = i
    if k < 0:
        return None
    else:
        return range_list[l[k][0]]


class Base(object):
    "Base IVI methods for all DC power supplies"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_outputs calls from other __init__ methods
        self._output_count = 1
        
        super().__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviDCPwrBase')
        
        self._output_current_limit = list()
        self._output_current_limit_behavior = list()
        self._output_enabled = list()
        self._output_ovp_enabled = list()
        self._output_ovp_limit = list()
        self._output_voltage_level = list()
        self._output_name = list()
        self._output_count = 1
        
        self._output_range = [[(0, 0)]]
        self._output_ovp_max = [0]
        self._output_voltage_max = [0]
        self._output_current_max = [0]
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('current_limit',
                        self._get_output_current_limit,
                        self._set_output_current_limit)
        self.outputs._add_property('current_limit_behavior',
                        self._get_output_current_limit_behavior,
                        self._set_output_current_limit_behavior)
        self.outputs._add_property('enabled',
                        self._get_output_enabled,
                        self._set_output_enabled)
        self.outputs._add_property('ovp_enabled',
                        self._get_output_ovp_enabled,
                        self._set_output_ovp_enabled)
        self.outputs._add_property('ovp_limit',
                        self._get_output_ovp_limit,
                        self._set_output_ovp_limit)
        self.outputs._add_property('voltage_level',
                        self._get_output_voltage_level,
                        self._set_output_voltage_level)
        self.outputs._add_property('name',
                        self._get_output_name)
        self.outputs._add_method('configure_current_limit',
                        self._output_configure_current_limit)
        self.outputs._add_method('configure_range',
                        self._output_configure_range)
        self.outputs._add_method('configure_ovp',
                        self._output_configure_ovp)
        self.outputs._add_method('query_current_limit_max',
                        self._output_query_current_limit_max)
        self.outputs._add_method('query_voltage_level_max',
                        self._output_query_voltage_level_max)
        self.outputs._add_method('query_output_state',
                        self._output_query_output_state)
        self.outputs._add_method('reset_output_protection',
                        self._output_reset_output_protection)
        
        self._init_outputs()
    
    
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_name = list()
        self._output_current_limit = list()
        self._output_current_limit_behavior = list()
        self._output_enabled = list()
        self._output_ovp_enabled = list()
        self._output_ovp_limit = list()
        self._output_voltage_level = list()
        for i in range(self._output_count):
            self._output_name.append("output%d" % (i+1))
            self._output_current_limit.append(0)
            self._output_current_limit_behavior.append('regulate')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(0)
            self._output_voltage_level.append(0)
        
        self.outputs._set_list(self._output_name)
    
    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_current_limit[index]
    
    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_current_max[index]:
            raise ivi.OutOfRangeException()
        self._output_current_limit[index] = value
    
    def _get_output_current_limit_behavior(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_current_limit_behavior[index]
    
    def _set_output_current_limit_behavior(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in CurrentLimitBehavior:
            raise ivi.ValueNotSupportedException()
        self._output_current_limit_behavior[index] = value
    
    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_enabled[index]
    
    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_enabled[index] = value
    
    def _get_output_ovp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_ovp_enabled[index]
    
    def _set_output_ovp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_ovp_enabled[index] = value
    
    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_ovp_limit[index]
    
    def _set_output_ovp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_ovp_max[index]:
            raise ivi.OutOfRangeException()
        self._output_ovp_limit[index] = value
    
    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_voltage_level[index]
    
    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_voltage_max[index]:
            raise ivi.OutOfRangeException()
        self._output_voltage_level[index] = value
    
    def _get_output_name(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_name[index]
    
    def _output_configure_current_limit(self, index, behavior, limit):
        self._set_output_current_limit_behavior(index, behavior)
        self._set_output_current_limit(index, limit)
    
    def _output_configure_range(self, index, range_type, range_val):
        index = ivi.get_index(self._output_name, index)
        if range_type not in RangeType:
            raise ivi.ValueNotSupportedException()
        if range_type == 'voltage':
            t = 0
        elif range_type == 'current':
            t = 1
        r = dcpwr.get_range(self._output_range[index], t, range_val)
        if r is None:
            raise ivi.OutOfRangeException()
        self._output_voltage_max[index] = r[0]
        self._output_current_max[index] = r[1]
        pass
    
    def _output_configure_ovp(self, index, enabled, limit):
        self._set_output_ovp_enabled(index, enabled)
        self._set_output_ovp_limit(index, limit)
    
    def _output_query_current_limit_max(self, index, voltage_level):
        index = ivi.get_index(self._output_name, index)
        if voltage_level < 0 or voltage_level > self._output_voltage_max[index]:
            raise ivi.OutOfRangeException()
        return self._output_current_max[index]
    
    def _output_query_voltage_level_max(self, index, current_limit):
        index = ivi.get_index(self._output_name, index)
        if current_limit < 0 or current_limit > self._output_current_max[index]:
            raise ivi.OutOfRangeException()
        return self._output_voltage_max[index]
    
    def _output_query_output_state(self, index, state):
        index = ivi.get_index(self._output_name, index)
        if state not in OutputState:
            raise ivi.ValueNotSupportedException()
        return False
    
    def _output_reset_output_protection(self, index):
        pass
    
    
class Trigger(object):
    "Extension IVI methods for power supplies supporting trigger based output changes"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviDCPwrTrigger')
        
        self._output_trigger_source = list()
        self._output_triggered_current_limit = list()
        self._output_triggered_voltage_level = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger_source',
                        self._get_output_trigger_source,
                        self._set_output_trigger_source)
        self.outputs._add_property('triggered_current_limit',
                        self._get_output_triggered_current_limit,
                        self._set_output_triggered_current_limit)
        self.outputs._add_property('triggered_voltage_level',
                        self._get_output_triggered_voltage_level,
                        self._set_output_triggered_voltage_level)
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger.abort = self._trigger_abort
        self.trigger.initiate = self._trigger_initiate
    
    def _init_outputs(self):
        try:
            super()._init_outputs()
        except AttributeError:
            pass
        
        self._output_trigger_source = list()
        self._output_triggered_current_limit = list()
        self._output_triggered_voltage_level = list()
        for i in range(self._output_count):
            self._output_trigger_source.append('')
            self._output_triggered_current_limit.append(0)
            self._output_triggered_voltage_level.append(0)
    
    def _get_output_trigger_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_trigger_source[index]
    
    def _set_output_trigger_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_trigger_source[index] = value
    
    def _get_output_triggered_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_triggered_current_limit[index]
    
    def _set_output_triggered_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_triggered_current_limit[index] = value
    
    def _get_output_triggered_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_triggered_voltage_level[index]
    
    def _set_output_triggered_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_triggered_voltage_level[index] = value
    
    def _trigger_abort(self):
        pass
    
    def _trigger_initiate(self):
        pass
    
    
class SoftwareTrigger(object):
    "Extension IVI methods for power supplies supporting software triggering"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviDCPwrSoftwareTrigger')
    
    def send_software_trigger(self):
        pass
    
    
class Measurement(object):
    "Extension IVI methods for power supplies supporting measurement of the output signal"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviDCPwrMeasurement')
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_method('measure',
                        self._output_measure)
    
    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in MeasurementType:
            raise ivi.ValueNotSupportedException()
        return 0
    
    

