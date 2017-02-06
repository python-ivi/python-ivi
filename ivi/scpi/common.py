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

from .. import ivi
from .. import extra


class IdnCommand(extra.common.SerialNumber):
    "Implementation of standard SCPI instrument identity query"

    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_serial_number = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = lst[0].strip()
            self._identity_instrument_model = lst[1].strip()
            self._identity_instrument_serial_number = lst[2].strip()
            self._identity_instrument_firmware_revision = lst[3].strip()
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_serial_number')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')

    def _get_identity_instrument_manufacturer(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_model

    def _get_identity_instrument_serial_number(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_serial_number

    def _get_identity_instrument_firmware_revision(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_firmware_revision


class ErrorQuery(object):
    "Implementation of standard SCPI error query"

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_code, error_message = self._ask("system:error?").split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (error_code, error_message)


class Reset(object):
    "Implementation of standard SCPI reset"

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("*RST")
            self._clear()
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()


class SelfTest(object):
    "Implementation of standard SCPI self test"

    def __init__(self, *args, **kwargs):
        super(SelfTest, self).__init__(*args, **kwargs)

        self._self_test_delay = 10

    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            self._write("*TST?")
            # wait for test to complete
            time.sleep(self._self_test_delay)
            code = int(self._read())
            if code != 0:
                message = "Self test failed"
        return (code, message)


class Memory(extra.common.Memory):
    "Extension IVI methods for instruments that support storing configurations in internal memory"
    
    def __init__(self, *args, **kwargs):
        super(Memory, self).__init__(*args, **kwargs)
        
        self._memory_size = 10
        self._memory_offset = 0
    
    def _memory_save(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*sav %d" % (index + self._memory_offset))
    
    def _memory_recall(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*rcl %d" % (index + self._memory_offset))
            self.driver_operation.invalidate_all_attributes()


class SystemSetup(extra.common.SystemSetup):
    "Extension IVI methods for instruments that support fetching and reloading of the system setup"
    
    def _system_fetch_setup(self):
        if self._driver_operation_simulate:
            return b''
        
        self._write("*lrn?")
        
        return self._read_raw()
    
    def _system_load_setup(self, data):
        if self._driver_operation_simulate:
            return
        
        self._write_raw(data)
        
        self.driver_operation.invalidate_all_attributes()
