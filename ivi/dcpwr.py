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
        l.append((i, abs(range_list[i][offset])))
    l.sort(key=lambda x: x[1], reverse=True)
    k = -1
    for i in range(len(l)):
        if l[i][1] >= val:
            k = i
    #if k < 0:
    #    return None
    #else:
    #    return range_list[l[k][0]]
    if k < 0:
        return -1
    else:
        return l[k][0]


class Base(object):
    "Base IVI methods for all DC power supplies"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_outputs calls from other __init__ methods
        self._output_count = 1
        
        super(Base, self).__init__(*args, **kwargs)
        
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
        self._output_range_name = [['P0V']]
        self._output_ovp_max = [0]
        self._output_voltage_max = [0]
        self._output_current_max = [0]
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('current_limit',
                        self._get_output_current_limit,
                        self._set_output_current_limit,
                        None,
                        """
                        Specifies the output current limit. The units are Amps.
                        
                        The value of the Current Limit Behavior attribute determines the behavior
                        of the power supply when the output current is equal to or greater than
                        the value of this attribute.
                        """)
        self.outputs._add_property('current_limit_behavior',
                        self._get_output_current_limit_behavior,
                        self._set_output_current_limit_behavior,
                        None,
                        """
                        Specifies the behavior of the power supply when the output current is
                        equal to or greater than the value of the Current Limit attribute.
                        
                        Values
                        
                        * 'trip' - The power supply disables the output when the output current is
                          equal to or greater than the value of the Current Limit attribute.
                        * 'regulate' - The power supply restricts the output voltage such that the
                          output current is not greater than the value of the Current Limit
                          attribute.
                        """)
        self.outputs._add_property('enabled',
                        self._get_output_enabled,
                        self._set_output_enabled,
                        None,
                        """
                        If true, the signal the power supply produces appears at the output
                        connector. If false, the signal the power supply produces does not appear
                        at the output connector.
                        """)
        self.outputs._add_property('ovp_enabled',
                        self._get_output_ovp_enabled,
                        self._set_output_ovp_enabled,
                        None,
                        """
                        Specifies whether the power supply provides over-voltage protection. If
                        this attribute is set to True, the power supply disables the output when
                        the output voltage is greater than or equal to the value of the OVP
                        Limit attribute.
                        """)
        self.outputs._add_property('ovp_limit',
                        self._get_output_ovp_limit,
                        self._set_output_ovp_limit,
                        None,
                        """
                        Specifies the voltage the power supply allows. The units are Volts.
                        
                        If the OVP Enabled attribute is set to True, the power supply disables the
                        output when the output voltage is greater than or equal to the value of
                        this attribute.
                        
                        If the OVP Enabled is set to False, this attribute does not affect the
                        behavior of the instrument.
                        """)
        self.outputs._add_property('voltage_level',
                        self._get_output_voltage_level,
                        self._set_output_voltage_level,
                        None,
                        """
                        Specifies the voltage level the DC power supply attempts to generate. The
                        units are Volts.
                        """)
        self.outputs._add_property('name',
                        self._get_output_name,
                        None,
                        None,
                        """
                        This attribute returns the repeated capability identifier defined by
                        specific driver for the output channel that corresponds to the index that
                        the user specifies. If the driver defines a qualified Output Channel name,
                        this property returns the qualified name.
                        
                        If the value that the user passes for the Index parameter is less than
                        zero or greater than the value of the Output Channel Count, the attribute
                        returns an empty string for the value and returns an error.
                        """)
        self.outputs._add_method('configure_current_limit',
                        self._output_configure_current_limit,
                        """
                        This function configures the current limit. It specifies the output
                        current limit value and the behavior of the power supply when the output
                        current is greater than or equal to that value.
                        
                        See the definition of the Current Limit Behavior attribute for defined
                        values for the behavior parameter.
                        """)
        self.outputs._add_method('configure_range',
                        self._output_configure_range,
                        """
                        Configures the power supply’s output range on an output. One parameter
                        specifies whether to configure the voltage or current range, and the other
                        parameter is the value to which to set the range.
                        
                        Setting a voltage range can invalidate a previously configured current
                        range. Setting a current range can invalidate a previously configured
                        voltage range.
                        """)
        self.outputs._add_method('configure_ovp',
                        self._output_configure_ovp,
                        """
                        Configures the over-voltage protection. It specifies the over-voltage
                        limit and the behavior of the power supply when the output voltage is
                        greater than or equal to that value.
                        
                        When the Enabled parameter is False, the Limit parameter does not affect
                        the instrument’s behavior, and the driver does not set the OVP Limit
                        attribute.
                        """)
        self.outputs._add_method('query_current_limit_max',
                        self._output_query_current_limit_max,
                        """
                        This function returns the maximum programmable current limit that the
                        power supply accepts for a particular voltage level on an output.
                        """)
        self.outputs._add_method('query_voltage_level_max',
                        self._output_query_voltage_level_max,
                        """
                        This function returns the maximum programmable voltage level that the
                        power supply accepts for a particular current limit on an output.
                        """)
        self.outputs._add_method('query_output_state',
                        self._output_query_output_state,
                        """
                        This function returns whether the power supply is in a particular output
                        state.
                        
                        A constant voltage condition occurs when the output voltage is equal to
                        the value of the Voltage Level attribute and the current is less than or
                        equal to the value of the Current Limit attribute.
                        
                        A constant current condition occurs when the output current is equal to
                        the value of the Current Limit attribute and the Current Limit Behavior
                        attribute is set to the Current Regulate defined value.
                        
                        An unregulated condition occurs when the output voltage is less than the
                        value of the Voltage Level attribute and the current is less than the
                        value of the Current Limit attribute.
                        
                        An over-voltage condition occurs when the output voltage is equal to or
                        greater than the value of the OVP Limit attribute and the OVP Enabled
                        attribute is set to True.
                        
                        An over-current condition occurs when the output current is equal to or
                        greater than the value of the Current Limit attribute and the Current
                        Limit Behavior attribute is set to the Current Trip defined value.
                        
                        When either an over-voltage condition or an over-current condition
                        occurs, the power supply‘s output protection disables the output. If the
                        power supply is in an over-voltage or over-current state, it does not
                        produce power until the output protection is reset. The Reset Output
                        Protection function resets the output protection. Once the output
                        protection is reset, the power supply resumes generating a power signal.
                        
                        Values for output_state:
                        
                        * 'constant_voltage'
                        * 'constant_current'
                        * 'over_voltage'
                        * 'over_current'
                        * 'unregulated'
                        """)
        self.outputs._add_method('reset_output_protection',
                        self._output_reset_output_protection,
                        """
                        This function resets the power supply output protection after an
                        over-voltage or over-current condition occurs.
                        
                        An over-voltage condition occurs when the output voltage is equal to or
                        greater than the value of the OVP Limit attribute and the OVP Enabled
                        attribute is set to True.
                        
                        An over-current condition occurs when the output current is equal to or
                        greater than the value of the Current Limit attribute and the Current
                        Limit Behavior attribute is set to Current Trip.
                        
                        When either an over-voltage condition or an over-current condition
                        occurs, the output protection of the power supply disables the output.
                        Once the output protection is reset, the power supply resumes generating
                        a power signal.
                        
                        Use the Query Output State function to determine if the power supply is in
                        an over-voltage or over-current state.
                        """)
        
        self._init_outputs()
    
    
    
    def _init_outputs(self):
        try:
            super(Base, self)._init_outputs()
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
        k = dcpwr.get_range(self._output_range[index], t, range_val)
        if k < 0:
            raise ivi.OutOfRangeException()
        self._output_voltage_max[index] = self._output_range[index][k][0]
        self._output_current_max[index] = self._output_range[index][k][1]
        pass
    
    def _output_configure_ovp(self, index, enabled, limit):
        self._set_output_ovp_enabled(index, enabled)
        if enabled:
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
        super(Trigger, self).__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviDCPwrTrigger')
        
        self._output_trigger_source = list()
        self._output_triggered_current_limit = list()
        self._output_triggered_voltage_level = list()
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_property('trigger_source',
                        self._get_output_trigger_source,
                        self._set_output_trigger_source,
                        None,
                        """
                        Specifies the trigger source. After an Initiate call, the power supply
                        waits for a trigger event from the source specified with this attribute.
                        After a trigger event occurs, the power supply changes the voltage level
                        to the value of the Triggered Voltage Level attribute and the current
                        limit to the value of the Triggered Current Limit attribute.
                        """)
        self.outputs._add_property('triggered_current_limit',
                        self._get_output_triggered_current_limit,
                        self._set_output_triggered_current_limit,
                        None,
                        """
                        Specifies the value to which the power supply sets the current limit after
                        a trigger event occurs. The units are Amps.
                        
                        After an Initiate call, the power supply waits for a trigger event from
                        the source specified with the Trigger Source attribute. After a trigger
                        event occurs, the power supply sets the current limit to the value of this
                        attribute.
                        
                        After a trigger occurs, the value of the Current Limit attribute reflects
                        the new value to which the current limit has been set.
                        """)
        self.outputs._add_property('triggered_voltage_level',
                        self._get_output_triggered_voltage_level,
                        self._set_output_triggered_voltage_level,
                        None,
                        """
                        Specifies the value to which the power supply sets the voltage level
                        after a trigger event occurs. The units are Volts.
                        
                        After an Initiate call, the power supply waits for a trigger event from
                        the source specified with the Trigger Source attribute. After a trigger
                        event occurs, the power supply sets the voltage level to the value of this
                        attribute.
                        
                        After a trigger occurs, the value of the Voltage Level attribute reflects
                        the new value to which the voltage level has been set.
                        """)
        self.__dict__.setdefault('trigger', ivi.PropertyCollection())
        self.trigger._add_method('abort',
                        self._trigger_abort,
                        """
                        If the power supply is currently waiting for a trigger to change the
                        output signal, this function returns the power supply to the ignore
                        triggers state.
                        
                        If the power supply is not waiting for a trigger, this function does
                        nothing and returns Success.
                        """)
        self.trigger._add_method('initiate',
                        self._trigger_initiate,
                        """
                        If the power supply is not currently waiting for a trigger, this function
                        causes the power supply to wait for a trigger.
                        
                        If the power supply is already waiting for a trigger, this function does
                        nothing and returns Success.
                        """)
    
    def _init_outputs(self):
        try:
            super(Trigger, self)._init_outputs()
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
        super(SoftwareTrigger, self).__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviDCPwrSoftwareTrigger')
        
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
    
    
class Measurement(object):
    "Extension IVI methods for power supplies supporting measurement of the output signal"
    
    def __init__(self, *args, **kwargs):
        super(Measurement, self).__init__(*args, **kwargs)
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviDCPwrMeasurement')
        
        self.__dict__.setdefault('outputs', ivi.IndexedPropertyCollection())
        self.outputs._add_method('measure',
                        self._output_measure,
                        """
                        Takes a measurement on the output signal and returns the measured value.
                        
                        Values for measurement_type:
                        
                        * 'voltage'
                        * 'current'
                        """)
    
    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in MeasurementType:
            raise ivi.ValueNotSupportedException()
        return 0
    
    

