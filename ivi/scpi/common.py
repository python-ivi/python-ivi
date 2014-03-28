"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

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
from .. import extra

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
