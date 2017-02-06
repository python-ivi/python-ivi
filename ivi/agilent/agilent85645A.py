"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2017 Alex Forencich

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

import time

from .agilent85644A import *

OutputCoupling = set(['ac', 'dc'])

class agilent85645A(agilent85644A):
    "Agilent 85645A IVI tracking source driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '85645A')

        self._rf_output_coupling = 'ac'

        super(agilent85645A, self).__init__(*args, **kwargs)

        self._frequency_low = 300e3
        self._frequency_high = 26.5e9

        self._add_property('rf.output_coupling',
                        self._get_rf_output_coupling,
                        self._set_rf_output_coupling)
        self._add_method('rf.ytm_peak',
                        self._rf_ytm_peak)


    def _get_rf_output_coupling(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_output_coupling = self._ask("output:coupling?").lower()
        return self._rf_output_coupling

    def _set_rf_output_coupling(self, value):
        if value not in OutputCoupling:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("output:coupling %s" % value)
        self._rf_output_coupling = value
        self._set_cache_valid()

    def _rf_ytm_peak(self):
        if not self._driver_operation_simulate:
            self._write("calibration:peaking:execute")
            for i in range(30):
                time.sleep(1)
                if (int(self._ask("status:operation:condition?")) & (1 << 0)) == 0:
                    break
