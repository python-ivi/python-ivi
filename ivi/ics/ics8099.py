"""

Python Interchangeable Virtual Instrument Library
Driver for ICS Electronics Model 8099

Copyright (c) 2014-2017 Jeff Wurzbach

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
from .. import scpi

class ics8099(scpi.common.IdnCommand, scpi.common.Reset,
              scpi.common.SelfTest,  scpi.common.ErrorQuery,
              ivi.Driver):
    "ICS Electronics 8099 Ethernet to Modbus Bridge"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '8099')

        super(ics8099, self).__init__(*args, **kwargs)

        self._identity_description = "ICS Electronics 8099 Ethernet to Modbus Bridge driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "ICS Electronics"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['8099']

        self._add_method('read_register',
                         self._read_register,
                         "Read Modbus register")
        self._add_method('write_register',
                         self._write_register,
                         "Write Modbus register")

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(ics8099, self)._initialize(resource, id_query, reset, **keywargs)

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
            self.utility_reset()


    def _utility_disable(self):
        pass

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass
    
    
    def _read_register(self, register):
        #read 16 bit registers
        if not self._driver_operation_simulate and not self._get_cache_valid():
            return int(self._ask("R? %d, %d" % (register, 1)).strip())
        return 0

    def _write_register(self, register, value):
        #write 16 bit registers
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._write("W %d, %d" % (register, value))

