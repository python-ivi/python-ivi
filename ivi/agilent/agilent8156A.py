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

class agilent8156A(ivi.Driver):
    "Agilent 8156A optical attenuator driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(agilent8156A, self).__init__(*args, **kwargs)

        self._identity_description = "Agilent 8156A optical attenuator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['8156A']

        self._attenuation = 0.0
        self._offset = 0.0
        self._wavelength = 1300.0
        self._disable = False

        self._add_property('attenuation',
                        self._get_attenuation,
                        self._set_attenuation,
                        None,
                        ivi.Doc("""
                        Specifies the attenuation of the optical path.  The units are dB. 
                        """))
        self._add_property('offset',
                        self._get_offset,
                        self._set_offset,
                        None,
                        ivi.Doc("""
                        Specifies the offset level for the attenuation setting. The units are dB.
                        """))
        self._add_property('wavelength',
                        self._get_wavelength,
                        self._set_wavelength,
                        None,
                        ivi.Doc("""
                        Specifies the wavelength of light used for accurate attenuation.  The
                        units are meters.
                        """))
        self._add_property('disable',
                        self._get_disable,
                        self._set_disable,
                        None,
                        ivi.Doc("""
                        Controls a shutter in the optical path.  Shutter is closed when disable is
                        set to True.
                        """))

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilent8156A, self)._initialize(resource, id_query, reset, **keywargs)

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
            error_code, error_message = self._ask(":system:error?").split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("*RST")
            self._clear()
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()

    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            code = int(self._ask("*TST?"))
            if code != 0:
                message = "Self test failed"
        return (code, message)

    def _utility_unlock_object(self):
        pass



    def _get_attenuation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("input:attenuation?")
            self._attenuation = float(resp)
            self._set_cache_valid()
        return self._attenuation

    def _set_attenuation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("input:attenuation %e" % (value))
        self._attenuation = value
        self._set_cache_valid()

    def _get_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("input:offset?")
            self._offset = float(resp)
            self._set_cache_valid()
        return self._offset

    def _set_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("input:offset %e" % (value))
        self._offset = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'attenuation')

    def _get_wavelength(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("input:wavelength?")
            self._wavelength = float(resp)
            self._set_cache_valid()
        return self._wavelength

    def _set_wavelength(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("input:wavelength %e" % (value))
        self._wavelength = value
        self._set_cache_valid()

    def _get_disable(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("output:state?")
            self._disable = bool(int(not resp))
            self._set_cache_valid()
        return self._disable

    def _set_disable(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("output:state %d" % (int(not value)))
        self._disable = value
        self._set_cache_valid()

