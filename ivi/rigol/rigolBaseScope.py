"""

Python Interchangeable Virtual Instrument Library - Rigol Oscilloscope Driver

Copyright (c) 2016 Ian Rees

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

import struct
import itertools

from .. import ivi
from .. import scope
from .. import scpi

class rigolBaseScope( scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset,
                      scpi.common.SelfTest, scpi.common.Memory,
                      scope.Base, 
                      ivi.Driver ):
    "Rigol generic IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_scale = list()
        self._channel_invert = list()
        self._channel_bw_limit = list()
        
        super(rigolBaseScope, self).__init__(*args, **kwargs)
        
        self._self_test_delay = 40
        self._memory_size = 10
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        
        self._timebase_scale = 1e-6
        self._horizontal_divisions = 12
        self._vertical_divisions = 8

        self._trigger_sweep = "AUTO"
        
        self._identity_description = "Rigol generic IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "RIGOL Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = [ "DS1054Z" ]
       
########                 Nonstandard IVI properties                ######## 
# note that member variables are initialised in __init__ above, or 
# _init_channels() below.
        self._add_property( "channels[].bw_limit",
                            self._get_channel_bw_limit,
                            self._set_channel_bw_limit,
                            None,
                            ivi.Doc("20Mhz low-pass filter.  True=enabled.") )
        self._add_property("channels[].invert",
                           self._get_channel_invert,
                           self._set_channel_invert,
                           None,
                           ivi.Doc("""
                           Selects whether or not to invert the channel.
                           """))
        self._add_property("channels[].scale",
                           self._get_channel_scale,
                           self._set_channel_scale,
                           None,
                           ivi.Doc("""
                           Specifies the vertical scale, or units per division,
                           of the channel.  Units are volts.
                           """))
        self._add_property("channels[].tcal",
                           self._get_channel_tcal,
                           self._set_channel_tcal,
                           None,
                           ivi.Doc("""
                           Delay time calibration of the channel.  Only relevant
                           if timebase is less than 10us.
                           """))
        self._add_property("channels[].units",
                           self._get_channel_units,
                           self._set_channel_units,
                           None,
                           ivi.Doc("""
                           Display units for the channel.  Allowed values are:
                           VOLTage, WATT, AMPere, UNKNown
                           """))
        self._add_property("channels[].vernier",
                           self._get_channel_vernier,
                           self._set_channel_vernier,
                           None,
                           ivi.Doc("""
                           Allows for Vernier (fine) adjustment of the vertical
                           scale of each channel.  True = Vernier adjustment ON
                           """))
        self._add_property("timebase.scale",
                           self._get_timebase_scale,
                           self._set_timebase_scale,
                           None,
                           ivi.Doc("""
                           Sets the horizontal scale in seconds per division of 
                           the main window.
                           """))
        self._add_property("trigger.sweep",
                           self._get_trigger_sweep,
                           self._set_trigger_sweep,
                           None,
                           ivi.Doc("Trigger sweep mode; one of AUTO NORMal SINGLe"))

    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        
        super(rigolBaseScope, self)._initialize(resource, id_query, reset, **keywargs)
        
        # interface clear
        if not self._driver_operation_simulate:
            self._clear()
        
        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)
        
        # reset
        if reset:
            self.utility.reset()

    
    def _utility_disable(self):
        pass
    
    def _utility_lock_object(self):
        pass
    
    def _utility_unlock_object(self):
        pass
    
    def _init_channels(self):
        try:
            super(rigolBaseScope, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list() # This seems important TODO: Figure out construction...

        self._channel_bw_limit = list()
        self._channel_invert = list()
        self._channel_scale = list()
        self._channel_tcal = list()
        self._channel_units = list()
        self._channel_vernier = list()
        
        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._analog_channel_name.append("channel%d" % (i+1))

            self._channel_bw_limit.append(False)
            self._channel_invert.append(False)
            self._channel_scale.append(1.0)
            self._channel_tcal.append(0.0)
            self._channel_units.append("VOLT")
            self._channel_vernier.append(False)
        
        # digital channels
        self._digital_channel_name = list()
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("d%d" % i)
            
            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_impedance[i] = 100000
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'dc'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)

    # TODO: Change setFormat and getFormat to behave
    # like the cast and strFormat in _gen_getset()
    def _gen_chan_getset( varName, cacheList, setFormat = lambda x : x,
                          getFormat = lambda x : x, allow = None ):
        """Produces methods for setting and getting channel parameters

        Methods are returned as getter, setter and have signatures:

        getter(self, index)
        setter(self, index, value)

        The setter sets it's parameter to value, in both cases index is the
        channel index.

        varName - SCPI command, the "bwl" in ":channel2:bwl 20M"
        cacheList - The PyIVI cache list associated with the parameter.  Actual
                    passed-in (setter) or response (getter) value gets cached.
        setFormat - Single-argument method producing a string eg '20M' above
        getFormat - Single-argument method scope's reponse is passed through
                    before comparing against allow list.  Ignored if allow is
                    not set.
        allow - List of valid values for the parameter, should be in string
                format that matches the output of setFormat and getFormat.
        """

        def getter(self, index):
            index = ivi.get_index(self._channel_name, index)

            if ( not self._driver_operation_simulate and
                 not self._get_cache_valid(index=index) ):
                query = ":%s:%s?" % (self._channel_name[index], varName)
                res = self._ask( query )

                if allow is None or getFormat(res) in allow:
                    self.__dict__[cacheList][index] = res
                    self._set_cache_valid(index=index)
                else:
                    raise Exception("Unexpected value from " + query)

            return self.__dict__[cacheList][index]

        def setter(self, index, value):
            index = ivi.get_index(self._channel_name, index)

            if not self._driver_operation_simulate:
                if not allow is None and not setFormat(value) in allow:
                    raise ivi.ValueNotSupportedException()

                setString = ":%s:%s " % (self._channel_name[index], varName)
                self._write( setString + setFormat(value) )

            self.__dict__[cacheList][index] = value
            self._set_cache_valid(index=index)

        return getter, setter

    _get_channel_bw_limit, _set_channel_bw_limit = _gen_chan_getset(
            "bwl", "_channel_bw_limit", setFormat = lambda x : x.upper(),
            allow = ["OFF", "20M"] )

    _get_channel_coupling, _set_channel_coupling = _gen_chan_getset(
            "coup", "_channel_coupling", setFormat = lambda x : x.upper(),
            allow = ["AC", "DC", "GND"])

    _get_channel_enabled, _set_channel_enabled = _gen_chan_getset(
            "disp", "_channel_enabled", setFormat = lambda x : "%d" % bool(x),
            allow = ["0", "1"] )

    _get_channel_invert, _set_channel_invert = _gen_chan_getset(
            "inv", "_channel_invert", setFormat = lambda x : "%d" % bool(x),
            allow = ["0", "1"] )

    _get_channel_offset, _set_channel_offset = _gen_chan_getset(
            "offs", "_channel_offset", setFormat = lambda x : "%e" % float(x) )

    # From manual: vertical scale = vertical range/8
    _get_channel_range, _set_channel_range = _gen_chan_getset(
            "rang", "_channel_range", setFormat = lambda x : "%e" % float(x) )

    _get_channel_tcal, _set_channel_tcal = _gen_chan_getset(
            "tcal", "_channel_tcal", setFormat = lambda x : "%e" % float(x) )

    _get_channel_scale, _set_channel_scale = _gen_chan_getset(
            "scal", "_channel_scale", setFormat = lambda x : "%e" % float(x) )

    _get_channel_probe_attenuation, _set_channel_probe_attenuation = _gen_chan_getset(
            "prob", "_channel_probe_attenuation", setFormat = lambda x : "%e" % float(x) )

    _get_channel_units, _set_channel_units = _gen_chan_getset(
            "unit", "_channel_units", setFormat = lambda x : x.upper(),
            getFormat = lambda x : x.upper(), allow = ["VOLT", "VOLTAGE",
            "WATT", "AMP", "AMPERE", "UNKN", "UNKNOWN"] )

    _get_channel_vernier, _set_channel_vernier = _gen_chan_getset(
            "vern", "_channel_vernier", setFormat = lambda x : "%d" % bool(x),
            allow = ["0", "1"] )

    def _gen_getset(scopeVarName, selfVarName, cast = lambda x : x,
            strFormatter = str, allow = None):

        def getter(self):
            if not self._driver_operation_simulate and not self._get_cache_valid():
                resp = cast(self._ask(scopeVarName + '?'))

                if not allow is None and not strFormatter(resp) in allow:
                    raise Exception("Unexpected value from '" + scopeVarName +
                                    "?', " + str(resp))

                self.__dict__[selfVarName] = resp
                self._set_cache_valid()
            return self.__dict__[selfVarName]

        def setter(self, value):
            value = cast(value)
            if not self._driver_operation_simulate:
                if not allow is None and not strFormatter(value) in allow:
                    raise ivi.ValueNotSupportedException()

                self._write(scopeVarName+ " " + strFormatter(value))

            self.__dict__selfVarName = value
            self._set_cache_valid()

        return getter, setter

    _get_timebase_scale, _set_timebase_scale = _gen_getset(":tim:scal",
            "_timebase_scale", cast = float, strFormatter = lambda x: "%e" % x)

    _get_trigger_sweep, _set_trigger_sweep = _gen_getset(":trig:swe",
            "_trigger_sweep", cast = lambda x : str(x).upper(), allow =
            ["AUTO", "NORM", "NORMAL", "SINGL", "SINGLE"])

    _get_trigger_type, _set_trigger_type = _gen_getset(":trig:mode",
            "_trigger_type", cast = lambda x : str(x).upper(), allow = 
            ["EDGE", "PULS", "PULSE", "RUNT", "WIND", "NEDG", "SLOP", "SLOPE",
             "VID", "VIDEO", "PATT", "PATTERN", "DEL", "DELAY", "TIM",
             "TIMEOUT", "DUR", "DURATION", "SHOL", "SHOLD",
             "RS232", "IIC", "SPI"])

    # IVI has some default trigger stuff that only applies to edge triggers:
    _get_trigger_level, _set_trigger_level = _gen_getset(":trig:edg:lev",
            "_trigger_level", cast = float, strFormatter = lambda x: "%e" % x)

    # TODO: Figure out how to do the allow list based on scope params
    _get_trigger_source, _set_trigger_source = _gen_getset(":trig:edg:sour",
            "_trigger_source", cast = lambda x : str(x).upper(), allow =
            ["D%d"%d for d in range(16)] + ["CHAN%d"%c for c in range(1, 5)] +
            ["CHANNEL%d" % c for c in range(1, 5)])

    def _measurement_fetch_waveform(self, index):
        "Returns current waveform as a list of (time, voltage) tuples"

        if self._driver_operation_simulate:
            return list()

        index = ivi.get_index(self._analog_channel_name, index)

        self._write(":wav:sour %s" % self._channel_name[index])
        self._write(":wav:form BYTE")
        self._write(":wav:mode norm ") # TODO: Look in to using MAX with averaging

        preamble = self._ask(":wav:pre?").split(',')

        pointsToGet = int(preamble[2])
        xIncrement = float(preamble[4])
        xOrigin = float(preamble[5])
        xReference = float(preamble[6])
        yIncrement = float(preamble[7])
        yOrigin = float(preamble[8])
        yReference = float(preamble[9])

        #                      byte, word, ascii   data format
        maxPointsPerXfer = [250000, 125000, 15625][int(preamble[0])]

        points = []
        while pointsToGet - len(points) > 0:
            pointsThisXfer = min(pointsToGet - len(points), maxPointsPerXfer)
            startPointNum = len(points) + 1 # 1-indexed

            self._write(":wav:star %d" % startPointNum)
            self._write(":wav:stop %d" % (startPointNum + pointsThisXfer - 1) )

            self._write(":wav:data?")
            thisData = self._read_ieee_block()

            for x, y in zip(itertools.count(len(points)), thisData):
                x = (x - xReference) * xIncrement + xOrigin
                y = (y - yReference) * yIncrement + yOrigin
                points.append((x, y))

        return points


