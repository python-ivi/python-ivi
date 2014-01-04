"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014 Alex Forencich

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
class InvalidScanListException(ivi.IviException): pass
class InvalidSwitchPathException(ivi.IviException): pass
class EmptyScanListException(ivi.IviException): pass
class EmptySwitchPathException(ivi.IviException): pass
class ScanInProgressException(ivi.IviException): pass
class NoScanInProgressException(ivi.IviException): pass
class NoSuchPathException(ivi.IviException): pass
class IsConfigurationChannelException(ivi.IviException): pass
class NotAConfigurationChannelException(ivi.IviException): pass
class AttemptToConnectSourcesException(ivi.IviException): pass
class ExplicitConnectionExistsException(ivi.IviException): pass
class LegMissingFirstChannelException(ivi.IviException): pass
class LegMissingSecondChannelException(ivi.IviException): pass
class ChannelDuplicatedInLegException(ivi.IviException): pass
class ChannelDuplicatedInPathException(ivi.IviException): pass
class PathNotFoundException(ivi.IviException): pass
class DiscontinuousPathException(ivi.IviException): pass
class CannotConnectDirectlyException(ivi.IviException): pass
class ChannelsAlreadyConnectedException(ivi.IviException): pass
class CannotConnectToItselfException(ivi.IviException): pass

# Parameter Values
ScanMode = set(['none', 'break_before_make', 'break_after_make'])
ScanActionType = set(['connect_path', 'disconnect_path', 'wait_for_trigger'])
Path = set(['available', 'exists', 'unsupported', 'resource_in_use',
            'source_conflict', 'channel_not_available'])

class Base(object):
    "Base IVI methods for all switch modules"
    
    def __init__(self, *args, **kwargs):
        # needed for _init_channels calls from other __init__ methods
        self._channel_count = 1
        
        super(Base, self).__init__( *args, **kwargs)
        
        cls = 'IviSwtch'
        grp = 'Base'
        ivi.add_group_capability(self, cls+grp)
        
        self._channel_name = list()
        self._channel_characteristics_ac_current_carry_max = list()
        self._channel_characteristics_ac_current_switching_max = list()
        self._channel_characteristics_ac_power_carry_max = list()
        self._channel_characteristics_ac_power_switching_max = list()
        self._channel_characteristics_ac_voltage_max = list()
        self._channel_characteristics_bandwidth = list()
        self._channel_characteristics_impedance = list()
        self._channel_characteristics_dc_current_carry_max = list()
        self._channel_characteristics_dc_current_switching_max = list()
        self._channel_characteristics_dc_power_carry_max = list()
        self._channel_characteristics_dc_power_switching_max = list()
        self._channel_characteristics_dc_voltage_max = list()
        self._channel_is_configuration_channel = list()
        self._channel_is_source_channel = list()
        self._channel_characteristics_settling_time = list()
        self._channel_characteristics_wire_mode = list()
        self._path_is_debounced = False
        
        ivi.add_property(self, 'channels[].characteristics.ac_current_carry_max',
                        self._get_channel_characteristics_ac_current_carry_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum AC current the channel can carry, in amperes RMS.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.1'))
        ivi.add_property(self, 'channels[].characteristics.ac_current_switching_max',
                        self._get_channel_characteristics_ac_current_switching_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum AC current the channel can switch, in amperes RMS.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.2'))
        ivi.add_property(self, 'channels[].characteristics.ac_power_carry_max',
                        self._get_channel_characteristics_ac_power_carry_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum AC power the channel can handle, in volt-amperes.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.3'))
        ivi.add_property(self, 'channels[].characteristics.ac_power_switching_max',
                        self._get_channel_characteristics_ac_power_switching_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum AC power the channel can switch, in volt-amperes.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.4'))
        ivi.add_property(self, 'channels[].characteristics.ac_voltage_max',
                        self._get_channel_characteristics_ac_voltage_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum AC voltage the channel can handle, in volts RMS.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.5'))
        ivi.add_property(self, 'channels[].characteristics.bandwidth',
                        self._get_channel_characteristics_bandwidth,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum frequency signal, in Hertz, that can pass through the channel.
                        without attenuating it by more than 3dB.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.6'))
        ivi.add_property(self, 'channels[].name',
                        self._get_channel_name,
                        None,
                        None,
                        ivi.Doc("""
                        This attribute returns the physical name identifier defined by the
                        specific driver for the Channel that corresponds to the one-based index
                        that the user specifies. If the driver defines a qualified channel name,
                        this property returns the qualified name. If the value that the user
                        passes for the Index parameter is less than one or greater than the value
                        of the Channel Count, the attribute returns an empty string for the value
                        and returns an error.
                        """, cls, grp, '4.2.9'))
        ivi.add_property(self, 'channels[].characteristics.impedance',
                        self._get_channel_characteristics_impedance,
                        None,
                        None,
                        ivi.Doc("""
                        The characteristic impedance of the channel, in ohms.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.10'))
        ivi.add_property(self, 'channels[].characteristics.dc_current_carry_max',
                        self._get_channel_characteristics_dc_current_carry_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum DC current the channel can carry, in amperes.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.11'))
        ivi.add_property(self, 'channels[].characteristics.dc_current_switching_max',
                        self._get_channel_characteristics_dc_current_switching_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum DC current the channel can switch, in amperes
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.12'))
        ivi.add_property(self, 'channels[].characteristics.dc_power_carry_max',
                        self._get_channel_characteristics_dc_power_carry_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum DC power the channel can handle, in watts.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.13'))
        ivi.add_property(self, 'channels[].characteristics.dc_power_switching_max',
                        self._get_channel_characteristics_dc_power_switching_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum DC power the channel can switch, in watts.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.14'))
        ivi.add_property(self, 'channels[].characteristics.dc_voltage_max',
                        self._get_channel_characteristics_dc_voltage_max,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum DC voltage the channel can handle, in volts.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        """, cls, grp, '4.2.15'))
        ivi.add_property(self, 'channels[].is_configuration_channel',
                        self._get_channel_is_configuration_channel,
                        self._set_channel_is_configuration_channel,
                        None,
                        ivi.Doc("""
                        Specifies whether the specific driver uses the channel for internal path
                        creation. If set to True, the channel is no longer accessible to the user
                        and can be used by the specific driver for path creation. If set to False,
                        the channel is considered a standard channel and can be explicitly
                        connected to another channel.
                        
                        For example, if the user specifies a column-to-column connection in a
                        matrix, it typically must use at least one row channel to make the
                        connection. Specifying a channel as a configuration channel allows the
                        instrument driver to use it to create the path.
                        
                        Notice that once a channel has been configured as a configuration channel,
                        then no operation can be performed on that channel, except for reading and
                        writing the Is Configuration Channel attribute.
                        """, cls, grp, '4.2.16'))
        ivi.add_property(self, 'path.is_debounced',
                        self._get_path_is_debounced,
                        None,
                        None,
                        ivi.Doc("""
                        This attribute indicates whether the switch module has settled from the
                        switching commands and completed the debounce. If True, the switch module
                        has settled from the switching commands and completed the debounce. It
                        indicates that the signal going through the switch module is valid,
                        assuming that the switches in the path have the correct characteristics.
                        If False, the switch module has not settled.
                        """, cls, grp, '4.2.17'))
        ivi.add_property(self, 'channels[].is_source_channel',
                        self._get_channel_is_source_channel,
                        self._set_channel_is_source_channel,
                        None,
                        ivi.Doc("""
                        Allows the user to declare a particular channel as a source channel. If
                        set to True, the channel is a source channel. If set to False, the channel
                        is not a source channel.
                        
                        If a user ever attempts to connect two channels that are either sources or
                        have their own connections to sources, the path creation operation returns
                        an error. Notice that the term source can be from either the instrument or
                        the UUT perspective. This requires the driver to ensure with each
                        connection that another connection within the switch module does not
                        connect to another source.
                        
                        The intention of this attribute is to prevent channels from being
                        connected that may cause damage to the channels, devices, or system.
                        Notice that GROUND can be considered a source in some circumstances.
                        """, cls, grp, '4.2.18'))
        ivi.add_property(self, 'channels[].characteristics.settling_time',
                        self._get_channel_characteristics_settling_time,
                        None,
                        None,
                        ivi.Doc("""
                        The maximum total settling time for the channel before the signal going
                        through it is considered stable. This includes both the activation time
                        for the channel as well as any debounce time.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        
                        The units are seconds.
                        """, cls, grp, '4.2.19'))
        ivi.add_property(self, 'channels[].characteristics.wire_mode',
                        self._get_channel_characteristics_wire_mode,
                        None,
                        None,
                        ivi.Doc("""
                        This attribute describes the number of conductors in the current channel.
                        
                        Notice that values for this attribute are on per-channel basis and may not
                        take into account the other switches that make up a path to or from this
                        channel.
                        
                        For example, this attribute returns 2 if the channel has two conductors.
                        """, cls, grp, '4.2.20'))
        ivi.add_method(self, 'path.can_connect',
                        self._path_can_connect,
                        ivi.Doc("""
                        The purpose of this function is to allow the user to verify whether the
                        switch module can create a given path without the switch module actually
                        creating the path. In addition, the operation indicates whether the switch
                        module can create the path at the moment based on the current paths in
                        existence.
                        
                        Notice that while this operation is available for the end user, the
                        primary purpose of this operation is to allow higher-level switch drivers
                        to incorporate IviSwtch drivers into higher level switching systems.
                        
                        If the implicit connection exists between the two specified channels, this
                        functions returns the warning Implicit Connection Exists.
                        """, cls, grp, '4.3.1'))
        ivi.add_method(self, 'path.connect',
                        self._path_connect,
                        ivi.Doc("""
                        This function takes two channel names and, if possible, creates a path
                        between the two channels. If the path already exists, the operation does
                        not count the number of calls. For example, it does not remember that
                        there were two calls to connect, thus requiring two calls to disconnect,
                        but instead returns an error, regardless of whether the order of the two
                        channels is the same or different on the two calls. This is true because
                        paths are assumed to be bi-directional. This class does not handle
                        unidirectional paths. Notice that the IVI spec does not specify the
                        default names for the channels because this depends on the architecture
                        of the switch module. The user can specify aliases for the vendor defined
                        channel names in the IVI Configuration Store.
                        
                        This function returns as soon as the command is given to the switch module
                        and the switch module is ready for another command. This may be before or
                        after the switches involved settle. Use the Is Debounced function to
                        determine if the switch module has settled. Use the Wait For Debounce
                        function if you want to wait until the switch has debounced.
                        
                        If an explicit connection already exists between the two specified
                        channels, this function returns the error Explicit Connection Exists
                        without performing any connection operation.
                        
                        If one of the specified channels is a configuration channel, this function
                        returns the error Is Configuration Channel without performing any
                        connection operation.
                        
                        If the two specified channels are both connected to a different source,
                        this function returns the error Attempt To Connect Sources without
                        performing any connection operation.
                        
                        If the two specified channels are the same, this function returns the
                        error Cannot Connect To Itself without performing any connection
                        operation.
                        
                        If a path cannot be found between the two specified channels, this
                        function returns the error Path Not Found without performing any
                        connection operation.
                        """, cls, grp, '4.3.2'))
        ivi.add_method(self, 'path.disconnect',
                        self._path_disconnect,
                        ivi.Doc("""
                        This function takes two channel names and, if possible, destroys the path
                        between the two channels. The order of the two channels in the operation
                        does not need to be the same as the connect operation. Notice that the IVI
                        specification does not specify what the default names are for the channels
                        as this depends on the architecture of the switch module. The user can
                        specify aliases for the vendor defined channel names in the IVI
                        Configuration Store.
                        
                        This function returns as soon as the command is given to the switch module
                        and the switch module is ready for another command. This may be before or
                        after the switches involved settle. Use the Is Debounced attribute to see
                        if the switch has settled. Use the Wait For Debounce function if you want
                        to wait until the switch has debounced.
                        
                        If some connections remain after disconnecting the two specified channels,
                        this function returns the warning Path Remains.
                        
                        If no explicit path exists between the two specified channels, this
                        function returns the error No Such Path without performing any
                        disconnection operation.
                        """, cls, grp, '4.3.3'))
        ivi.add_method(self, 'path.disconnect_all',
                        self._path_disconnect_all,
                        ivi.Doc("""
                        The purpose of this function is to allow the user to disconnect all paths
                        created since Initialize or Reset have been called. This can be used as
                        the test program goes from one sub-test to another to ensure there are no
                        side effects in the switch module.
                        
                        Notice that some switch modules may not be able to disconnect all paths
                        (such as a scanner that must keep at least one path). In these cases, this
                        function returns the warning Path Remains.
                        """, cls, grp, '4.3.4'))
        ivi.add_method(self, 'path.get_path',
                        self._path_get_path,
                        ivi.Doc("""
                        This function returns a list of channels (see the Set Path function for a
                        description on the syntax of path list) that have been connected in order
                        to create the path between the specified channels. The names of the
                        switches as well as the internal configuration of the switch module are
                        vendor specific. This function can be used to return the list of the
                        switches in order to better understand the signal characteristics of the
                        path and to provide the path list for the Set Path function.
                        
                        The first and last names in the list are the channel names of the path.
                        All channels other than the first and the last channel in the path list
                        are configuration channels. No other channel can be used to generate the
                        path between the two channels.
                        
                        The only valid paths that can be returned are ones that have been
                        explicitly set via Connect and Set Path functions.
                        
                        If no explicit path exists between the two specified channels, this
                        function returns the error No Such Path.
                        """, cls, grp, '4.3.6'))
        ivi.add_method(self, 'path.set_path',
                        self._path_set_path,
                        ivi.Doc("""
                        The IVI Switch is designed to provide automatic routing from channel to
                        channel. However, due to such issues as calibration, it may be necessary
                        to have deterministic control over the path that is created between two
                        channels. This function allows the user to specify the exact path, in
                        terms of the configuration channels used, to create. Notice that the end
                        channel names are the first and last entries in the Path List parameter.
                        
                        The driver makes a connection between the channels using the configuration
                        channels. The intermediary steps are called legs of the path.
                        
                        The path list syntax is a string array of channels. Path lists obey the
                        following rules:

                        * In the array, elements n and n+1 create a path leg.
                        * Every channel in the path list other than the first and the last must be
                          a configuration channel.
                        * Driver channel strings as well as virtual channel names may be used to
                          describe a path leg in a path list.
                        
                        An example of creating a path list is:
                        
                            path_list = ['ch1', 'conf1', 'ch2']
                        
                        It should be noticed that, even if users utilize virtual channel names,
                        path_list is not interchangeable since the names of switches within the
                        switch module are not required to be interchangeable and depend on the
                        internal architecture of the switch module. However, it is possible to use
                        the Connect and then Get Path functions to retrieve an already existing
                        path. This allows the user to guarantee that the routing can be recreated
                        exactly.
                        
                        If the specified path list is empty, this function returns the error Empty
                        Switch Path without performing any connection operation.
                        
                        If one of the channels in the path list is a configuration channel that is
                        currently in use, this function returns the error Resource In Use without
                        performing any connection operation.
                        
                        If an explicit connection is made to a configuration channel, this
                        function returns the error Is Configuration Channel without performing any
                        connection operation.
                        
                        If one of the non-terminal channels in the path list is not a
                        configuration channel, this function returns the error Not A Configuration
                        Channel without performing any connection operation.
                        
                        If the path list attempts to connect between two different source
                        channels, this function returns the error Attempt To Connect Sources
                        without performing any connection operation.
                        
                        If the path list attempts to connect between channels that already have an
                        explicit connection, this function returns the error Explicit Connection
                        Exists without performing any connection operation.
                        
                        If the first and the second channels in the leg are the same, this
                        function returns the error Channel Duplicated In Leg without performing
                        any connection operation.
                        
                        If a channel name is duplicated in the path list, this function returns
                        the error Channel Duplicated In Path without performing any connection
                        operation.
                        
                        If the path list contains a leg with two channels that cannot be directly
                        connected, this function returns the error Cannot Connect Directly without
                        performing any connection operation. If a leg in the path contains two
                        channels that are already directly connected, this function returns the
                        error Channels Already Connected without performing any connection
                        operation.
                        """, cls, grp, '4.3.8'))
        ivi.add_method(self, 'path.wait_for_debounce',
                        self._path_wait_for_debounce,
                        ivi.Doc("""
                        The purpose of this function is to wait until the path through the switch
                        is stable (debounced). If the signals did not settle within the time
                        period the user specified with the maximum_time parameter, the function
                        returns the Max Time Exceeded error.
                        """, cls, grp, '4.3.9'))
        
        self._init_channels()
    
    
    
    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_characteristics_ac_current_carry_max = list()
        self._channel_characteristics_ac_current_switching_max = list()
        self._channel_characteristics_ac_power_carry_max = list()
        self._channel_characteristics_ac_power_switching_max = list()
        self._channel_characteristics_ac_voltage_max = list()
        self._channel_characteristics_bandwidth = list()
        self._channel_characteristics_impedance = list()
        self._channel_characteristics_dc_current_carry_max = list()
        self._channel_characteristics_dc_current_switching_max = list()
        self._channel_characteristics_dc_power_carry_max = list()
        self._channel_characteristics_dc_power_switching_max = list()
        self._channel_characteristics_dc_voltage_max = list()
        self._channel_is_configuration_channel = list()
        self._channel_is_source_channel = list()
        self._channel_characteristics_settling_time = list()
        self._channel_characteristics_wire_mode = list()
        for i in range(self._channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_characteristics_ac_current_carry_max.append(0.1)
            self._channel_characteristics_ac_current_switching_max.append(0.1)
            self._channel_characteristics_ac_power_carry_max.append(1)
            self._channel_characteristics_ac_power_switching_max.append(1)
            self._channel_characteristics_ac_voltage_max.append(100)
            self._channel_characteristics_bandwidth.append(1e6)
            self._channel_characteristics_impedance.append(50)
            self._channel_characteristics_dc_current_carry_max.append(0.1)
            self._channel_characteristics_dc_current_switching_max.append(0.1)
            self._channel_characteristics_dc_power_carry_max.append(1)
            self._channel_characteristics_dc_power_switching_max.append(1)
            self._channel_characteristics_dc_voltage_max.append(100)
            self._channel_is_configuration_channel.append(False)
            self._channel_is_source_channel.append(False)
            self._channel_characteristics_settling_time.append(0.1)
            self._channel_characteristics_wire_mode.append(1)
        
        self.channels._set_list(self._channel_name)
    
    
    def _get_channel_characteristics_ac_current_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_current_carry_max[index]
    
    def _get_channel_characteristics_ac_current_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_current_switching_max[index]
    
    def _get_channel_characteristics_ac_power_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_power_carry_max[index]
    
    def _get_channel_characteristics_ac_power_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_power_switching_max[index]
    
    def _get_channel_characteristics_ac_voltage_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_voltage_max[index]
    
    def _get_channel_characteristics_bandwidth(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_bandwidth[index]
    
    def _get_channel_name(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_name[index]
    
    def _get_channel_characteristics_impedance(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_impedance[index]
    
    def _get_channel_characteristics_dc_current_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_current_carry_max[index]
    
    def _get_channel_characteristics_dc_current_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_current_switching_max[index]
    
    def _get_channel_characteristics_dc_power_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_power_carry_max[index]
    
    def _get_channel_characteristics_dc_power_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_power_switching_max[index]
    
    def _get_channel_characteristics_dc_voltage_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_voltage_max[index]
    
    def _get_channel_is_configuration_channel(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_is_configuration_channel[index]
    
    def _set_channel_is_configuration_channel(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_is_configuration_channel[index] = value
    
    def _get_path_is_debounced(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._path_is_debounced[index]
    
    def _get_channel_is_source_channel(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_is_source_channel[index]
    
    def _set_channel_is_source_channel(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_is_source_channel[index] = value
    
    def _get_channel_characteristics_settling_time(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_settling_time[index]
    
    def _get_channel_characteristics_wire_mode(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_wire_mode[index]
    
    def _path_can_connect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)
        return False
    
    def _path_connect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)
    
    def _path_disconnect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)
    
    def _path_disconnect_all(self):
        pass
    
    def _path_get_path(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)
        return []
    
    def _path_set_path(self, path):
        pass
    
    def _path_wait_for_debounce(self, maximum_time):
        pass
    
    
# Scanner
# SoftwareTrigger

