"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2015-2017 Hermann Kraus

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

from .agilent34401A import *
from .. import ivi
from .. import extra

class agilent34461A(agilent34401A, extra.common.Title):
    "Agilent 34461A IVI DMM driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '34401A')
        
        super(agilent34461A, self).__init__(*args, **kwargs)

        self._add_method('system.display_string',
            self._system_display_string,
            ivi.Doc("""
            Writes a string to the instrument display.  Send None
            or an empty string to return to normal operation.
            """))

    def _system_display_string(self, string=None):
        if self._driver_operation_simulate:
            return
        if string:
            self._write("DISP:TEXT \"%s\"" % string)
        else:
            self._write("DISP:TEXT:CLEAR")

    def _set_display_title(self, string):
        super(agilent34461A, self)._set_display_title(string)
        if not self._driver_operation_simulate:
            self._write("SYST:LABEL \"%s\"" % string)

