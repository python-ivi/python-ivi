"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014-2017 Alex Forencich

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

class jdsuTB9(ivi.Driver):
    "JDS Uniphase TB9 Series Optical Grating Filter driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'TB9')

        super(jdsuTB9, self).__init__(*args, **kwargs)

        self._identity_description = "JDS Uniphase TB9 Series Optical Grating Filter driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "JDS Uniphase"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['TB9']

        self._wavelength = 0
        self._driver_enable = False

        self._add_property('wavelength',
                        self._get_wavelength,
                        self._set_wavelength,
                        None,
                        ivi.Doc("""
                        Specifies the center wavelength of the optical grating filter. The units
                        are meters.
                        """))
        self._add_property('driver_enable',
                        self._get_driver_enable,
                        self._set_driver_enable,
                        None,
                        ivi.Doc("""
                        Control relay driver.  Set to True to enable 5v output, False to disable.
                        """))

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(jdsuTB9, self)._initialize(resource, id_query, reset, **keywargs)

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
            self.utility.reset()


    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._ask("IDN?").split(",")
            self._identity_instrument_manufacturer = lst[0].strip()
            self._identity_instrument_model = lst[1].strip()
            self._identity_instrument_firmware_revision = lst[3].strip()
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
            error_message = self._ask("err?").strip('"')
            error_code = 1
            if error_message == '0':
                error_code = 0
        return (error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("RST")
            self._clear()
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()

    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            code = int(self._ask("TST?"))
            if code != 0:
                message = "Self test failed"
        return (code, message)

    def _utility_unlock_object(self):
        pass



    def _get_wavelength(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("wvl?")
            self._wavelength = float(resp)
            self._set_cache_valid()
        return self._wavelength

    def _set_wavelength(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("wvl %e" % (value))
        self._wavelength = value
        self._set_cache_valid()

    def _get_driver_enable(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("xdr?")
            self._driver_enable = bool(int(resp))
            self._set_cache_valid()
        return self._driver_enable

    def _set_driver_enable(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("xdr %d" % (int(value)))
        self._driver_enable = value
        self._set_cache_valid()

