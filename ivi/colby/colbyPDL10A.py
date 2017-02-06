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

from .. import ivi
from .. import scpi

Mode = set(['312.5ps', '625ps'])

class colbyPDL10A(scpi.common.IdnCommand, scpi.common.Reset,
                  scpi.common.SelfTest,
                  ivi.Driver):
    "Colby Instruments PDL10A Programmable Delay Line driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'PDL 10A')

        super(colbyPDL10A, self).__init__(*args, **kwargs)

        self._identity_description = "Colby Instruments PDL10A Programmable Delay Line driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Colby Instruments"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PDL10A']

        self._delay = 0
        self._mode = ''

        self._add_property('delay',
                        self._get_delay,
                        self._set_delay,
                        None,
                        ivi.Doc("""
                        Specifies the delay of the delay line.  The units are seconds.  
                        """))
        self._add_property('mode',
                        self._get_mode,
                        self._set_mode,
                        None,
                        ivi.Doc("""
                        Specifies the mode of the delay line.  If the segments are cascaded, then
                        the mode should be set to '625ps'.  If the segments are not cascaded, then
                        the mode should be set to '312.5ps'.  
                        """))

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(colbyPDL10A, self)._initialize(resource, id_query, reset, **keywargs)

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

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_message = self._ask("err?").strip('"')
            error_code = 1
            if error_message == '0':
                error_code = 0
        return (error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass

    def _get_delay(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("del?")
            self._delay = float(resp)
            self._set_cache_valid()
        return self._delay

    def _set_delay(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("del %e" % (value))
        self._delay = value
        self._set_cache_valid()

    def _get_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("mode?")
            self._mode = resp.strip('"')
            self._set_cache_valid()
        return self._mode

    def _set_mode(self, value):
        if value not in Mode:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("mode %s" % (value))
        self._mode = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'delay')

