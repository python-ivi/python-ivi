"""

Python Interchangeable Virtual Instrument Library - Rigol DS1000Z Driver

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

from .rigolBaseScope import *
import itertools

class rigolDS1054Z(rigolBaseScope):
    "Rigol DS1054Z IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault("_instrument_id", "DS1054Z")
        
        super(rigolDS1054Z, self).__init__(*args, **kwargs)
        
        self._analog_channel_count = 4
        self._digital_channel_count = 0
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 50e6
        
        self._init_channels()

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

    _get_channel_probe, _set_channel_probe = _gen_chan_getset(
            "prob", "_channel_probe", setFormat = lambda x : "%e" % float(x) )

    _get_channel_units, _set_channel_units = _gen_chan_getset(
            "unit", "_channel_units", setFormat = lambda x : x.upper(),
            getFormat = lambda x : x.upper(), allow = ["VOLT", "VOLTAGE",
            "WATT", "AMP", "AMPERE", "UNKN", "UNKNOWN"] )

    _get_channel_vernier, _set_channel_vernier = _gen_chan_getset(
            "vern", "_channel_vernier", setFormat = lambda x : "%d" % bool(x),
            allow = ["0", "1"] )

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


