# coding=utf-8
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) Acconeer AB, 2018

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
from .. import rfsiggen

class rohdeschwarzBaseRFSigGen(scpi.common.IdnCommand, scpi.common.Reset, scpi.common.ErrorQuery,
			       ivi.Driver, rfsiggen.Base):

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(rohdeschwarzBaseRFSigGen, self).__init__(*args, **kwargs)

        self._rf_rms_voltage_level = 0.0

        # frequency limit in Hertz
        self._frequency_low = 9e3
        self._frequency_high = 1100e6        
        # rf level limit in dBm
        self._rf_level_low = -120.0
        self._rf_level_high = 19
        # rf rms voltage level limit in Volt
        self._rf_rms_voltage_level_low = 223.61e-9
        self._rf_rms_voltage_level_high = 1.993

        self._identity_description = "Rohde&Schwarz generic IVI RF signal generator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Rohde&Schwarz"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 1
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['SMC100A'])

        self._add_property('rf.rms_voltage_level',
                        self._get_rf_rms_voltage_level,
                        self._set_rf_rms_voltage_level,
                        None,
                        ivi.Doc("""
                        Rms voltage level of the instrument.
                        """))

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(rohdeschwarzBaseRFSigGen, self)._initialize(resource, id_query, reset, **keywargs)
        
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
        
    def _get_rf_frequency(self):
        "Reads the frequency of the generated RF output signal. The unit is Hertz"
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency = float(self._ask("FREQ?"))
            self._set_cache_valid()
        return self._rf_frequency
    
    def _set_rf_frequency(self, value):
        "Specifies the frequency of the generated RF output signal. The unit is Hertz"
        value = float(value)
        if value < self._frequency_low or value > self._frequency_high:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("FREQ %e HZ" % value)
        self._rf_frequency = value
        self._set_cache_valid()

    def _get_rf_level(self):
        """
        return set value in dBm of rf output level containing offset.
        """
        return self._rf_level
    
    def _set_rf_level(self, value):
        """
        Sets the level of the Level display, i.e. the level containing offset. The unit is dBm
        """
        value = float(value)
        if value < self._rf_level_low or value > self._rf_level_high:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("POW %e dBm" % value)
        self._rf_level = value
        self._rf_rms_voltage_level = self._dbm_to_rms(value)
        self._set_cache_valid()

    def _get_rf_rms_voltage_level(self):
        """
        return set value in volt of rf output level containing offset.
        """
        return self._rf_rms_voltage_level
    
    def _set_rf_rms_voltage_level(self, value):
        """
        Sets the rms voltage level of the Level display, i.e. the level containing offset. The unit is Volt
        """
        value = float(value)
        if value < self._rf_rms_voltage_level_low or value > self._rf_rms_voltage_level_high:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("POW %e V" % value)
        self._rf_rms_voltage_level = value
        self._rf_level = self._rms_to_dbm(value)
        self._set_cache_valid()
    
    def _get_rf_output_enabled(self):
        "Check if RF output is enabled, Returns True if enabled"
        return self._rf_output_enabled
    
    def _set_rf_output_enabled(self, value):
        """
        If value is non zero, the signal the RF signal generator produces appears at the output connector. 
        If it is zero, the signal the RF signal generator produces does not appear at the output connector
        """
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("OUTP ON")
            else:
                self._write("OUTP OFF")
        self._rf_output_enabled = value
        self._set_cache_valid()

    def _rf_disable_all_modulation(self):
        "Disables modulation, similar result as pressing MOD on/off."
        if not self._driver_operation_simulate:
            self._write("MOD OFF")

    def _rf_is_settled(self):
        "Queries if the RF output signal is currently settled. Returns true if settled"
        if not self._driver_operation_simulate:
            return self._read_stb() & (1 << 7) == 0
        return True

    def _rf_wait_until_settled(self, maximum_time):
        "This function waits maximumtime(milli seconds) until the state of the RF output signal has settled."
        t = 0
        while not self._rf_is_settled() and t < maximum_time:
            time.sleep(0.001)
            t = t + 0.001

    def _rms_to_dbm(self, v, r=50):
        "This function converts rms volts v to dBm, r is resistance in ohms."
        return (10 * ivi.np.log10(ivi.np.abs(v** 2.)/r) + 30)

    def _dbm_to_rms(self, p, r=50):
        "This function converts dBm to rms volts, r is resistance in ohms."
        return (ivi.np.sqrt(r*(10.**(p/10.))/1000))

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_msg_list = self._ask("system:error?").split(',')
            error_code = int(error_msg_list[0])
            error_message = ''.join(error_msg_list[1:]).strip(' "')
        return (error_code, error_message)
