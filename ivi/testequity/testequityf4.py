"""

Python Interchangeable Virtual Instrument Library
Driver for Test Equity Model 140

Copyright (c) 2014 Jeff Wurzbach

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

from .. import ivi
from .. import ics

class testequityf4(ivi.IviContainer)::
    "Watlow F4 controller used in TestEquity Enviromental Chambers"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(testequityf4, self).__init__(*args, **kwargs)

        self._add_property('chambertemp', self._get_chambertemp, self_set_chambertemp)
        self._add_property('chambertemp', self._get_chambertemp, self_set_chambertemp)
    
    
    
     def _get_temperature_decimal_config(self):
       if not self._driver_operation_simulate and not self._get_cache_valid():
           self._temperature_decimal_config = self._read_register(606)
           self._set_cache_valid()
       return self._temperature_decimal_config
    def _get_humidity_decimal_config(self):
       if not self._driver_operation_simulate and not self._get_cache_valid():
           self._humidity_decimal_config = self._read_register(616)
           self._set_cache_valid()
       return self._humidity_decimal_config
    def _get_part_temperature_decimal_config(self):
       if not self._driver_operation_simulate and not self._get_cache_valid():
           self._part_temperature_decimal_config = self._read_register(626)
           self._set_cache_valid()
       return self._part_temperature_decimal_config       
    
    def _get_decimal_config(register):
        return self._read_register(register)
    
    def _get_temperature():
        return self._read_register(100)
        



