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

import time

from .. import ivi
from .. import extra

class agilent85644A(ivi.Driver):
    "Agilent 85644A IVI tracking source driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '85644A')

        super(agilent85644A, self).__init__(*args, **kwargs)

        self._rf_frequency = 1e8
        self._rf_level = 0
        self._rf_output_enabled = False
        self._alc_enabled = True

        self._identity_description = "Agilent 85644/5A IVI tracking source driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 2
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['85644A', '85645A'])

        self._frequency_low = 300e3
        self._frequency_high = 6.5e9

        ivi.add_property(self, 'rf.frequency',
                        self._get_rf_frequency,
                        self._set_rf_frequency)
        ivi.add_property(self, 'rf.level',
                        self._get_rf_level,
                        self._set_rf_level)
        ivi.add_property(self, 'rf.output_enabled',
                        self._get_rf_output_enabled,
                        self._set_rf_output_enabled)
        ivi.add_method(self, 'rf.configure',
                        self._rf_configure)
        ivi.add_property(self, 'alc.enabled',
                        self._get_alc_enabled,
                        self._set_alc_enabled)

    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilent85644A, self).initialize(resource, id_query, reset, **keywargs)

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


    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = lst[0]
            self._identity_instrument_model = lst[1]
            self._identity_instrument_firmware_revision = lst[3]
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')

    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid():
            return self._identity_instrument_manufacturer
        self._load_id_string()
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        self._load_id_string()
        return self._identity_instrument_model

    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        self._load_id_string()
        return self._identity_instrument_firmware_revision

    def _utility_disable(self):
        pass

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_code = int(self._ask("OE"))
            if error_code == 0:
                error_code = int(self._ask("OH"))
            if error_code != 0:
                error_message = "Unknown error"
            if error_code in Messages:
                error_message = Messages[error_code]
        return (error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("IP")
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()

    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            self._write("*TST?")
            # wait for test to complete
            time.sleep(30)
            code = int(self._read())
            if code != 0:
                message = "Self test failed"
        return (code, message)

    def _utility_unlock_object(self):
        pass


    def _get_rf_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency = float(self._ask("source:frequency?"))
            self._set_cache_valid()
        return self._rf_frequency

    def _set_rf_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:frequency %e" % value)
        self._rf_frequency = value
        self._set_cache_valid()

    def _get_rf_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level = float(self._ask("source:power:level?"))
            self._set_cache_valid()
        return self._rf_level

    def _set_rf_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:power:level %e" % value)
        self._rf_level = value
        self._set_cache_valid()

    def _get_rf_output_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_output_enabled = bool(int(self._ask("output:state?")))
        return self._rf_output_enabled

    def _set_rf_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("output:state %d" % int(value))
        self._rf_output_enabled = value
        self._set_cache_valid()

    def _rf_configure(self, frequency, level):
        self._set_rf_frequency(frequency)
        self._set_rf_level(level)

    def _get_alc_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._alc_enabled = bool(int(self._ask("power:alc:state?")))
        return self._alc_enabled

    def _set_alc_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("power:alc:state %d" % int(value))
        value = bool(value)
        self._alc_enabled = value

    def _rf_is_settled(self):
        if not self._driver_operation_simulate:
            return self._read_stb() & (1 << 4) != 0
        return True

    def _rf_wait_until_settled(self, maximum_time):
        t = 0
        while not self._rf_is_settled() and t < maximum_time:
            time.sleep(0.01)
            t = t + 0.01


