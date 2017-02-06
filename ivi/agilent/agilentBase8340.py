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
from .. import rfsiggen
from .. import extra

class agilentBase8340(rfsiggen.Base, rfsiggen.ModulateAM, rfsiggen.ModulateFM,
        rfsiggen.ModulatePulse, rfsiggen.Sweep, rfsiggen.FrequencySweep, rfsiggen.PowerSweep,
        extra.common.Memory,
        extra.common.SystemSetup,
        ivi.Driver):
    "Agilent 8340A IVI RF sweep generator driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(agilentBase8340, self).__init__(*args, **kwargs)

        self._identity_description = "Agilent 8340 IVI RF sweep generator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 2
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['8340A','8340B', '8341A', '8341B'])

        self._frequency_low = 10e6
        self._frequency_high = 26.5e9

        self._memory_size = 8

        self._add_property('sweep.frequency_sweep.center',
                        self._get_sweep_frequency_sweep_center,
                        self._set_sweep_frequency_sweep_center)
        self._add_property('sweep.frequency_sweep.span',
                        self._get_sweep_frequency_sweep_span,
                        self._set_sweep_frequency_sweep_span)

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilentBase8340, self)._initialize(resource, id_query, reset, **keywargs)

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


    def _get_identity_instrument_manufacturer(self):
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        if self._driver_operation_simulate:
            self._identity_instrument_model = "Not available while simulating"
        else:
            self._identity_instrument_model = self._ask("OI").split('REV')[0]
            self._set_cache_valid()
        return self._identity_instrument_model

    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        if self._driver_operation_simulate:
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            self._identity_instrument_firmware_revision = self._ask("OI").split('REV')[1]
            self._set_cache_valid()
        return self._identity_instrument_firmware_revision

    def _utility_disable(self):
        pass

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        #if not self._driver_operation_simulate:
        #    error_code = int(self._ask("OE"))
        #    if error_code == 0:
        #        error_code = int(self._ask("OH"))
        #    if error_code != 0:
        #        error_message = "Unknown error"
        #    if error_code in Messages:
        #        error_message = Messages[error_code]
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
        return (code, message)

    def _utility_unlock_object(self):
        pass


    def _memory_save(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("SV %d" % (index+1))

    def _memory_recall(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("RC %d" % (index+1))

    def _system_fetch_setup(self):
        if self._driver_operation_simulate:
            return b''

        self._write("OL?")

        return self._read_raw()

    def _system_load_setup(self, data):
        if self._driver_operation_simulate:
            return

        self._write_raw(b'IL'+data)

        self.driver_operation.invalidate_all_attributes()

    def _get_rf_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency = float(self._ask("OPCW"))
            self._set_cache_valid()
        return self._rf_frequency

    def _set_rf_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("CW%eHZ" % value)
        self._rf_frequency = value
        self._set_cache_valid()

    def _get_rf_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level = float(self._ask("OPPL"))
            self._set_cache_valid()
        return self._rf_level

    def _set_rf_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("PL%eDB" % value)
        self._rf_level = value
        self._set_cache_valid()

    def _get_rf_output_enabled(self):
        #if not self._driver_operation_simulate and not self._get_cache_valid():
        #    self._rf_output_enabled = bool(int(self._ask("OPRF")))
        #    self._set_cache_valid()
        return self._rf_output_enabled

    def _set_rf_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("RF%d" % int(value))
        self._rf_output_enabled = value
        self._set_cache_valid()

    def _get_alc_enabled(self):
        return self._alc_enabled

    def _set_alc_enabled(self, value):
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

    def _get_analog_modulation_am_enabled(self):
        #if not self._driver_operation_simulate and not self._get_cache_valid():
        #    self._analog_modulation_am_enabled = bool(int(self._ask("OPAM")))
        #    self._set_cache_valid()
        return self._analog_modulation_am_enabled

    def _set_analog_modulation_am_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("AM%d" % int(value))
        self._analog_modulation_am_enabled = value
        self._set_cache_valid()

    def _get_analog_modulation_am_source(self):
        return self._analog_modulation_am_source

    def _set_analog_modulation_am_source(self, value):
        value = str(value)
        self._analog_modulation_am_source = value

    def _get_analog_modulation_am_scaling(self):
        return self._analog_modulation_am_scaling

    def _set_analog_modulation_am_scaling(self, value):
        value = int(value)
        self._analog_modulation_am_scaling = value

    def _get_analog_modulation_am_external_coupling(self):
        return self._analog_modulation_am_external_coupling

    def _set_analog_modulation_am_external_coupling(self, value):
        value = int(value)
        self._analog_modulation_am_external_coupling = value

    def _get_analog_modulation_am_nominal_voltage(self):
        return self._analog_modulation_am_nominal_voltage

    def _set_analog_modulation_am_nominal_voltage(self, value):
        value = float(value)
        self._analog_modulation_am_nominal_voltage = value

    def _get_analog_modulation_am_depth(self):
        return self._analog_modulation_am_depth

    def _set_analog_modulation_am_depth(self, value):
        value = float(value)
        self._analog_modulation_am_depth = value

    def _get_analog_modulation_fm_enabled(self):
        return self._analog_modulation_fm_enabled

    def _set_analog_modulation_fm_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("FM%d" % int(value))
        self._analog_modulation_fm_enabled = value
        self._set_cache_valid()

    def _get_analog_modulation_fm_source(self):
        return self._analog_modulation_fm_source

    def _set_analog_modulation_fm_source(self, value):
        value = str(value)
        self._analog_modulation_fm_source = value

    def _get_analog_modulation_fm_external_coupling(self):
        return self._analog_modulation_fm_external_coupling

    def _set_analog_modulation_fm_external_coupling(self, value):
        value = int(value)
        self._analog_modulation_fm_external_coupling = value

    def _get_analog_modulation_fm_nominal_voltage(self):
        return self._analog_modulation_fm_nominal_voltage

    def _set_analog_modulation_fm_nominal_voltage(self, value):
        value = float(value)
        self._analog_modulation_fm_nominal_voltage = value

    def _get_analog_modulation_fm_deviation(self):
        return self._analog_modulation_fm_deviation

    def _set_analog_modulation_fm_deviation(self, value):
        value = float(value)
        #if not self._driver_operation_simulate:
        #    self._write("FM %e HZ" % value)
        self._analog_modulation_fm_deviation = value
        #self._set_cache_valid()

    def _get_pulse_modulation_enabled(self):
        return self._pulse_modulation_enabled

    def _set_pulse_modulation_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("PM%d" % int(value))
        self._pulse_modulation_enabled = value
        self._set_cache_valid()

    def _get_pulse_modulation_source(self):
        return self._pulse_modulation_source

    def _set_pulse_modulation_source(self, value):
        value = str(value)
        self._pulse_modulation_source = value

    def _get_pulse_modulation_external_polarity(self):
        return self._pulse_modulation_external_polarity

    def _set_pulse_modulation_external_polarity(self, value):
        value = int(value)
        self._pulse_modulation_external_polarity = value

    def _get_sweep_mode(self):
        return self._sweep_mode

    def _set_sweep_mode(self, value):
        value = int(value)
        self._sweep_mode = value

    def _get_sweep_trigger_source(self):
        return self._sweep_trigger_source

    def _set_sweep_trigger_source(self, value):
        value = str(value)
        self._sweep_trigger_source = value

    def _get_sweep_frequency_sweep_start(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_sweep_start = float(self._ask("OPFA"))
            self._set_cache_valid()
        return self._sweep_frequency_sweep_start

    def _set_sweep_frequency_sweep_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FA%fHZ" % value)
        self._sweep_frequency_sweep_start = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_frequency_sweep_center')
        self._set_cache_valid(False, 'sweep_frequency_sweep_span')

    def _get_sweep_frequency_sweep_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_sweep_stop = float(self._ask("OPFB"))
            self._set_cache_valid()
        return self._sweep_frequency_sweep_stop

    def _set_sweep_frequency_sweep_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FB%fHZ" % value)
        self._sweep_frequency_sweep_stop = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_frequency_sweep_center')
        self._set_cache_valid(False, 'sweep_frequency_sweep_span')

    def _get_sweep_frequency_sweep_center(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_sweep_center = float(self._ask("OPCF"))
            self._set_cache_valid()
        return self._sweep_frequency_sweep_center

    def _set_sweep_frequency_sweep_center(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("CF%fHZ" % value)
        self._sweep_frequency_sweep_center = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_frequency_sweep_start')
        self._set_cache_valid(False, 'sweep_frequency_sweep_stop')

    def _get_sweep_frequency_sweep_span(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_sweep_span = float(self._ask("OPDF"))
            self._set_cache_valid()
        return self._sweep_frequency_sweep_span

    def _set_sweep_frequency_sweep_span(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("DF%fHZ" % value)
        self._sweep_frequency_sweep_span = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'sweep_frequency_sweep_start')
        self._set_cache_valid(False, 'sweep_frequency_sweep_stop')

    def _get_sweep_frequency_sweep_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_sweep_time = float(self._ask("OPST"))
            self._set_cache_valid()
        return self._sweep_frequency_sweep_time

    def _set_sweep_frequency_sweep_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("ST%fSC" % value)
        self._sweep_frequency_sweep_time = value

    def _get_sweep_power_sweep_start(self):
        return self._get_rf_level()

    def _set_sweep_power_sweep_start(self, value):
        self._set_rf_level(value)

    def _get_sweep_power_sweep_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_power_sweep_stop = float(self._ask("OPPS"))
            self._set_cache_valid()
        return self._sweep_power_sweep_stop

    def _set_sweep_power_sweep_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("PS%fDB" % value)
        self._sweep_power_sweep_stop = value
        self._set_cache_valid()

    def _get_sweep_power_sweep_time(self):
        return self._get_sweep_frequency_sweep_time()

    def _set_sweep_power_sweep_time(self, value):
        self._set_sweep_frequency_sweep_time(value)

