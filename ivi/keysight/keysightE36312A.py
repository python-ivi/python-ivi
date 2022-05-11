"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2022 Acconeer AB

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

from .. import agilent
from .. import ivi
from .. import scpi

class keysightE36312A(scpi.dcpwr.OCP, agilent.agilentE3600A.agilentE3600A):
    "Keysight E36312A IVI DC power supply driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'E3631A')

        super(keysightE36312A, self).__init__(*args, **kwargs)

        self._identity_description = "Keysight E36312A series DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Keysight Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = ""
        self._identity_specification_minor_version = ""
        self._identity_supported_instrument_models = ['E36312A']
        self._output_count = 3

        self._output_spec = [
            {
                'range': {
                    'P6V': (6.0, 5.0)
                },
                'ovp_max': 6.0,
                'voltage_max': 6.0,
                'current_max': 5.0
            },
            {
                'range': {
                    'P25V': (25.0, 1.0)
                },
                'ovp_max': 0,
                'voltage_max': 25.0,
                'current_max': 1.0
            },
            {
                'range': {
                    'N25V': (25.0, 1.0)
                },
                'ovp_max': 25.0,
                'voltage_max': 25.0,
                'current_max': 1.0
            }
        ]

        self._memory_size = 3

        self._init_outputs()

    def _get_output_ocp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_ocp_limit[index] = float(self._ask("source:current:level?"))
            self._set_cache_valid(index=index)
        return self._output_ocp_limit[index]

    def _set_output_ocp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_ocp_limit[index] = float(self._ask("source:current:level?"))
        if abs(value) != abs(self._output_ocp_limit[index]):
            raise ivi.OutOfRangeException()
        self._set_cache_valid(index=index)
