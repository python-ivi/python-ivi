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

class tektronixOA5000(ivi.Driver):
    "Tektronix OA5000 series optical attenuator driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(tektronixOA5000, self).__init__(*args, **kwargs)
        
        self._identity_description = "Tektronix OA5000 series optical attenuator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Tektronix"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['OA5002', 'OA5012', 'OA5022', 'OA5032']
        
        self._attenuation = 0.0
        self._reference = 0.0
        self._wavelength = 1300.0
        self._disable = False
        
        self.__dict__.setdefault('_docs', dict())
        self._docs['attenuation'] = ivi.Doc("""
                        Specifies the attenuation of the optical path.  The units are dB. 
                        """)
        self._docs['reference'] = ivi.Doc("""
                        Specifies the zero dB reference level for the attenuation setting. The
                        units are dB.
                        """)
        self._docs['wavelength'] = ivi.Doc("""
                        Specifies the wavelength of light used for accurate attenuation.  The
                        units are nm.
                        """)
        self._docs['disable'] = ivi.Doc("""
                        Controls a shutter in the optical path.  Shutter is closed when disable is
                        set to True.
                        """)
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(tektronixOA5000, self).initialize(resource, id_query, reset, **keywargs)
        
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
            error_message = self._ask("err?").strip('"')
            error_code = 1
            if error_message == '0':
                error_code = 0
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
    
    
    
    attenuation = property(lambda self: self._get_attenuation(),
                           lambda self, value: self._set_attenuation(value))
    
    def _get_attenuation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("attenuation:dbr?").split(' ')[1]
            self._attenuation = float(resp)
            self._set_cache_valid()
        return self._attenuation
    
    def _set_attenuation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("attenuation:dbr %e" % (value))
        self._attenuation = value
        self._set_cache_valid()
    
    reference = property(lambda self: self._get_reference(),
                           lambda self, value: self._set_reference(value))
    
    def _get_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("reference?").split(' ')[1]
            self._reference = float(resp)
            self._set_cache_valid()
        return self._reference
    
    def _set_reference(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("reference %e" % (value))
        self._reference = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'attenuation')
    
    wavelength = property(lambda self: self._get_wavelength(),
                           lambda self, value: self._set_wavelength(value))
    
    def _get_wavelength(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("wavelength?").split(' ')[1]
            self._wavelength = float(resp)
            self._set_cache_valid()
        return self._wavelength
    
    def _set_wavelength(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("wavelength %e" % (value))
        self._wavelength = value
        self._set_cache_valid()
    
    disable = property(lambda self: self._get_disable(),
                       lambda self, value: self._set_disable(value))
    
    def _get_disable(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("disable?").split(' ')[1]
            self._disable = bool(int(resp))
            self._set_cache_valid()
        return self._disable
    
    def _set_disable(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("disable %d" % (int(value)))
        self._disable = value
        self._set_cache_valid()
    
    
    
    
    
    
    

