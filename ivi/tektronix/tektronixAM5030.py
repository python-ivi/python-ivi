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

Coupling = set(['ac', 'dc', 'ref'])
DegaussType = set(['normal', 'force_gain', 'gain_only'])

class tektronixAM5030(ivi.Driver):
    "Tektronix AM5030 current probe amplifier driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'AM5030')

        super(tektronixAM5030, self).__init__(*args, **kwargs)

        self._identity_description = "Tektronix AM5030 current probe amplifier driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Tektronix"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['AM5030']

        self._amps = 0.001
        self._bw_limit = False
        self._coupling = 'ref'
        self._dc_level = 0.0
        self._overload = False
        self._probe_open = False
        self._probe_trim = 1.0
        self._probe_type = ''

        self._add_property('amps',
                        self._get_amps,
                        self._set_amps,
                        None,
                        ivi.Doc("""
                        Specifies the resolution of the current measurement in amps per 10 mV.
                        """))
        self._add_property('bw_limit',
                        self._get_bw_limit,
                        self._set_bw_limit,
                        None,
                        ivi.Doc("""
                        Sets the 20 MHz bandwidth limit switch.
                        """))
        self._add_property('coupling',
                        self._get_coupling,
                        self._set_coupling,
                        None,
                        ivi.Doc("""
                        Specifies the input coupling of the amplifier.

                        Values:

                        * 'ac'
                        * 'dc'
                        * 'ref'
                        """))
        self._add_property('dc_level',
                        self._get_dc_level,
                        self._set_dc_level,
                        None,
                        ivi.Doc("""
                        Specifies the DC offset level of the amplifier.  This is the current level
                        that will be displayed at the oscilloscope ground reference level.
                        """))
        self._add_property('overload',
                        self._get_overload,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the state of the overload indicator.
                        """))
        self._add_property('probe_open',
                        self._get_probe_open,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the state of the probe open indicator.
                        """))
        self._add_property('probe_trim',
                        self._get_probe_trim,
                        self._set_probe_trim,
                        None,
                        ivi.Doc("""
                        Lets you specify a multiplicative gain factor (trim adjustment) for probe
                        compensation. There is a trim adjustment value for each type of probe (for
                        example, A6302/A6312, A6302XL, A6303, A6303XL, or A6304XL). This command
                        will set or query only the trim adjustment for the type of current probe
                        currently connected to the AM 5030. If no probe is connected, executing
                        this command or query will cause error 264, "No probe connected."

                        Probe trim is used to perform an optional fine-tune calibration of the
                        A6303 Current Probe.
                        """))
        self._add_property('probe_type',
                        self._get_probe_type,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the type (model) of current probe connected to the AM 5030 INPUT
                        connector. The return string NOPROBE indicates that no current probe is
                        connected.
                        """))
        self._add_method('degauss',
                        self._degauss,
                        ivi.Doc("""
                        Initializes the probe degauss/autobalance sequence.

                        Argument:

                        * 'normal' (default)
                        * 'force_gain'
                        * 'gain_only'
                        """))


    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(tektronixAM5030, self)._initialize(resource, id_query, reset, **keywargs)

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
            s = self._ask("ID?").split(" ")[1]
            lst = s.split(",", 1)
            self._identity_instrument_model = lst[0].split('/')[1]
            self._identity_instrument_firmware_revision = lst[1]
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
            self._write("init")
            self._clear()
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()

    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            code = int(self._ask("test"))
            if code != 0:
                message = "Self test failed"
        return (code, message)

    def _utility_unlock_object(self):
        pass



    def _get_amps(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("amps?").split(' ')[1]
            self._amps = float(resp)
            self._set_cache_valid()
        return self._amps

    def _set_amps(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("amps %e" % (value))
        self._amps = value
        self._set_cache_valid()

    def _get_bw_limit(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("bwlimit?").split(' ')[1].lower()
            self._bw_limit = resp == 'on'
            self._set_cache_valid()
        return self._bw_limit

    def _set_bw_limit(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("bwlimit %s" % ('on' if value else 'off'))
        self._bw_limit = value
        self._set_cache_valid()

    def _get_coupling(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("coupling?").split(' ')[1].lower()
            self._coupling = resp
            self._set_cache_valid()
        return self._coupling

    def _set_coupling(self, value):
        if value not in Coupling:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("coupling %s" % (value))
        self._coupling = value
        self._set_cache_valid()

    def _get_dc_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("dclevel?").split(' ')[1]
            self._dc_level = float(resp)
            self._set_cache_valid()
        return self._dc_level

    def _set_dc_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("dclevel %e" % (value))
        self._dc_level = value
        self._set_cache_valid()

    def _get_overload(self):
        if not self._driver_operation_simulate:
            resp = self._ask("overload?").split(' ')[1].lower()
            self._overload = resp == 'on'
        return self._overload

    def _get_probe_open(self):
        if not self._driver_operation_simulate:
            resp = self._ask("probeopen?").split(' ')[1].lower()
            self._probe_open = resp == 'on'
        return self._probe_open

    def _get_probe_trim(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("probetrim?").split(' ')[1]
            self._probe_trim = float(resp)
            self._set_cache_valid()
        return self._probe_trim

    def _set_probe_trim(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("probetrim %e" % (value))
        self._probe_trim = value
        self._set_cache_valid()

    def _get_probe_type(self):
        if not self._driver_operation_simulate:
            resp = self._ask("probetype?").split(' ')[1]
            self._probe_type = resp
        return self._probe_type

    def _degauss(self, value = 'normal'):
        if value not in DegaussType:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if value == 'normal':
                value = 0
            elif value == 'force_gain':
                value = 1
            elif value == 'gain_only':
                value = 2
            self._write("degauss %e" % (value))

