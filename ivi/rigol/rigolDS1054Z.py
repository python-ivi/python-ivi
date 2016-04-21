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

    def _generic_channel_getset(varName, varSetFmtStr, cacheList,
            setFormatter = lambda x : x, getFormatter = lambda x : x,
            allowed = None):

        setString = (":%%s:%s " % varName) + varSetFmtStr

        def setter(self, index, value):
            index = ivi.get_index(self._channel_name, index)

            if not self._driver_operation_simulate:
                if not allowed is None and not setFormatter(value) in allowed:
                    raise ivi.ValueNotSupportedException()

                self._write( setString % 
                        (self._channel_name[index], setFormatter(value)) )

            self.__dict__[cacheList][index] = setFormatter(value)
            self._set_cache_valid(index=index)

        def getter(self, index):
            index = ivi.get_index(self._channel_name, index)

            if ( not self._driver_operation_simulate and
                 not self._get_cache_valid(index=index) ):
                query = ":%s:%s ?" % (self._channel_name[index], varName)
                res = self._ask( query )
                                 
                if allowed is None or res in allowed:
                    self.__dict__[cacheList][index] = getFormatter(res)
                    self._set_cache_valid(index=index)
                else:
                    raise Exception("Unexpected value from " + query)

            return self.__dict__[cacheList][index]

        return getter, setter

    def _generic_channel_setter(setString, setFormatter, cacheList, setAllowed = None):
        "if setAllowed is None, then we actually allow anything..."

        def ret(self, index, value):
            index = ivi.get_index(self._channel_name, index)

            if not self._driver_operation_simulate:
                if not setAllowed is None and not setFormatter(value) in setAllowed:
                    raise ivi.ValueNotSupportedException()

                self._write( (":%s:" + setString) %
                             (self._channel_name[index], setFormatter(value)) )

            self.__dict__[cacheList][index] = setFormatter(value)
            self._set_cache_valid(index=index)

        return ret

    def _generic_channel_getter(getString, getFormatter, cacheList, getFilter = None):

        def ret(self, index):
            index = ivi.get_index(self._channel_name, index)

            if ( not self._driver_operation_simulate and
                 not self._get_cache_valid(index=index) ):
                query = (":%s:" + getString + "?" ) % self._channel_name[index]
                res = self._ask( query )
                                 
                if getFilter is None or res in getFilter:
                    self.__dict__[cacheList][index] = getFormatter(res)
                    self._set_cache_valid(index=index)
                else:
                    raise Exception("Unexpected value from " + query)

            return self.__dict__[cacheList][index]

        return ret


    _get_channel_offset = _generic_channel_getter(
            "offs", lambda x : x, "_channel_offset" )

    _set_channel_offset = _generic_channel_setter(
            "offs %e", lambda x : float(x), "_channel_offset" )


    _get_channel_enabled = _generic_channel_getter(
            "disp", lambda x : x == "1", "_channel_enabled", ["0", "1"] )

    _set_channel_enabled = _generic_channel_setter(
            "disp %d", lambda x : bool(x), "_channel_enabled" )


    _get_channel_bw_limit, _set_channel_bw_limit = _generic_channel_getset(
            "bwl", "%s", "_channel_bw_limit", lambda x : x.upper(),
            allowed = ["OFF", "20M"] )

    _get_channel_coupling, _set_channel_coupling = _generic_channel_getset(
            "coup", "%s", "_channel_coupling", lambda x: x.upper(),
            allowed = ["AC", "DC", "GND"])


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


