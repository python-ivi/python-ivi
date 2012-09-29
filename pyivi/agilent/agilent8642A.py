"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012 Alex Forencich

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

class agilent8642A(ivi.Driver, rfsiggen.Base, rfsiggen.ModulateAM,
        rfsiggen.ModulateFM, rfsiggen.ModulatePM, rfsiggen.AnalogModulationSource,
        rfsiggen.ModulatePulse, rfsiggen.LFGenerator, rfsiggen.LFGeneratorOutput,
        rfsiggen.Sweep, rfsiggen.FrequencySweep, rfsiggen.PowerSweep):
    "Agilent 8642A IVI RF signal generator driver"
    
    def __init__(self):
        super(agilent8642A, self).__init__()
        
        self._instrument_id = 'HP8642A'
    
        self._identity_description = "Agilent 8642 IVI RF signal generator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['8642A','8642B'])
        self._identity_group_capabilities = list()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilent8642A, self).initialize(resource, id_query, reset, **keywargs)
        
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
        if 'identity_instrument_model' in self._cache_valid:
            return self._identity_instrument_model
        if self._driver_operation_simulate:
            self._identity_instrument_model = "Not available while simulating"
        else:
            self._identity_instrument_model = self._ask("SP340EN")
            self._cache_valid.append('identity_instrument_model')
        return self._identity_instrument_model
    
    def _get_identity_instrument_firmware_revision(self):
        if 'identity_instrument_firmware_revision' in self._cache_valid:
            return self._identity_instrument_firmware_revision
        if self._driver_operation_simulate:
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            self._identity_instrument_firmware_revision = self._ask("SP249").split(' ')[0]
            self._cache_valid.append('identity_instrument_firmware_revision')
        return self._identity_instrument_firmware_revision
    
    def _utility_disable(self):
        pass
    
    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
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
    
    
    
    def _get_rf_frequency(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._rf_frequency = float(self._ask("FROA").split(' ')[1])
        return self._rf_frequency
    
    def _set_rf_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FR %e HZ" % value)
        self._rf_frequency = value
    
    def _get_rf_level(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._rf_level = float(self._ask("FROA").split(' ')[1])
        return self._rf_level
    
    def _set_rf_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AP %e DM" % value)
        self._rf_level = value
    
    def _get_rf_output_enabled(self):
        return self._rf_output_enabled
    
    def _set_rf_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("R1")
            else:
                self._write("R0")
        self._rf_output_enabled = value
    
    def _get_alc_enabled(self):
        return self._alc_enabled
    
    def _set_alc_enabled(self, value):
        value = bool(value)
        self._alc_enabled = value
    
    def _rf_is_settled(self):
        return True
    
    def _rf_wait_until_settled(self, maximum_time):
        pass
    
    def _get_analog_modulation_am_enabled(self):
        return self._analog_modulation_am_enabled
    
    def _set_analog_modulation_am_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("AMON")
            else:
                self._write("AMOF")
        self._analog_modulation_am_enabled = value
    
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
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._analog_modulation_am_depth = float(self._ask("AMOA").split(' ')[1])
        return self._analog_modulation_am_depth
    
    def _set_analog_modulation_am_depth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AM %e PC" % value)
        self._analog_modulation_am_depth = value
    
    def _get_analog_modulation_fm_enabled(self):
        return self._analog_modulation_fm_enabled
    
    def _set_analog_modulation_fm_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                if (self._analog_modulation_pm_enabled):
                    self._set_analog_modulation_pm_enabled(False)
                self._write("FMON")
            else:
                self._write("FMOF")
        self._analog_modulation_fm_enabled = value
    
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
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._analog_modulation_fm_deviation = float(self._ask("FMOA").split(' ')[1])
        return self._analog_modulation_fm_deviation
    
    def _set_analog_modulation_fm_deviation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FM %e HZ" % value)
        self._analog_modulation_fm_deviation = value
    
    def _get_analog_modulation_pm_enabled(self):
        return self._analog_modulation_pm_enabled
    
    def _set_analog_modulation_pm_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                if (self._analog_modulation_fm_enabled):
                    self._set_analog_modulation_fm_enabled(False)
                self._write("PMON")
            else:
                self._write("PMOF")
        self._analog_modulation_pm_enabled = value
    
    def _get_analog_modulation_pm_source(self):
        return self._analog_modulation_pm_source
    
    def _set_analog_modulation_pm_source(self, value):
        value = str(value)
        self._analog_modulation_pm_source = value
    
    def _get_analog_modulation_pm_external_coupling(self):
        return self._analog_modulation_pm_external_coupling
    
    def _set_analog_modulation_pm_external_coupling(self, value):
        value = int(value)
        self._analog_modulation_pm_external_coupling = value
    
    def _get_analog_modulation_pm_nominal_voltage(self):
        return self._analog_modulation_pm_nominal_voltage
    
    def _set_analog_modulation_pm_nominal_voltage(self, value):
        value = float(value)
        self._analog_modulation_pm_nominal_voltage = value
    
    def _get_analog_modulation_pm_deviation(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._analog_modulation_pm_deviation = float(self._ask("PMOA").split(' ')[1])
        return self._analog_modulation_pm_deviation
    
    def _set_analog_modulation_pm_deviation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("PM %e RD" % value)
        self._analog_modulation_pm_deviation = value
    
    def _get_pulse_modulation_enabled(self):
        return self._pulse_modulation_enabled
    
    def _set_pulse_modulation_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self.rf_disable_all_modulation()
                self._write("PLON")
            else:
                self._write("PLOF")
        self._pulse_modulation_enabled = value
    
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
    
    def _get_lf_generator_active_lf_generator(self):
        return self._lf_generator_active_lf_generator
    
    def _set_lf_generator_active_lf_generator(self, value):
        value = str(value)
        self._lf_generator_active_lf_generator = value
    
    def _get_lf_generator_count(self):
        return self._lf_generator_count
    
    def _get_lf_generator_name(self, index):
        if index < 0 or index >= self._lf_generator_count: raise Exception('Channel out of range')
        return self._lf_generator_name[index]
    
    def _get_lf_generator_frequency(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._lf_generator_frequency = float(self._ask("MFOA").split(' ')[1])
        return self._lf_generator_frequency
    
    def _set_lf_generator_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("MF %e HZ" % value)
        self._lf_generator_frequency = value
    
    def _get_lf_generator_waveform(self):
        return self._lf_generator_waveform
    
    def _set_lf_generator_waveform(self, value):
        value = int(value)
        self._lf_generator_waveform = value
    
    def _get_lf_generator_output_amplitude(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._lf_generator_output_amplitude = float(self._ask("MLOA").split(' ')[1])
        return self._lf_generator_output_amplitude
    
    def _set_lf_generator_output_amplitude(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("ML %e VL" % value)
        self._lf_generator_output_amplitude = value
    
    def _get_lf_generator_output_enabled(self):
        return self._lf_generator_output_enabled
    
    def _set_lf_generator_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("MLON")
            else:
                self._write("MLOF")
        self._lf_generator_output_enabled = value
    
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
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._sweep_frequency_sweep_start = float(self._ask("FAOA").split(' ')[1])
        return self._sweep_frequency_sweep_start
    
    def _set_sweep_frequency_sweep_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FA %e HZ" % value)
        self._sweep_frequency_sweep_start = value
    
    def _get_sweep_frequency_sweep_stop(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._sweep_frequency_sweep_stop = float(self._ask("FBOA").split(' ')[1])
        return self._sweep_frequency_sweep_stop
    
    def _set_sweep_frequency_sweep_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FB %e HZ" % value)
        self._sweep_frequency_sweep_stop = value
    
    def _get_sweep_frequency_sweep_time(self):
        return self._sweep_frequency_sweep_time
    
    def _set_sweep_frequency_sweep_time(self, value):
        value = float(value)
        self._sweep_frequency_sweep_time = value
    
    def _get_sweep_power_sweep_start(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._sweep_power_sweep_start = float(self._ask("AAOA").split(' ')[1])
        return self._sweep_power_sweep_start
    
    def _set_sweep_power_sweep_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AA %e HZ" % value)
        self._sweep_power_sweep_start = value
    
    def _get_sweep_power_sweep_stop(self):
        if not self._driver_operation_simulate and not self._driver_operation_cache:
            self._sweep_power_sweep_stop = float(self._ask("ABOA").split(' ')[1])
        return self._sweep_power_sweep_stop
    
    def _set_sweep_power_sweep_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AB %e HZ" % value)
        self._sweep_power_sweep_stop = value
    
    def _get_sweep_power_sweep_time(self):
        return self._sweep_power_sweep_time
    
    def _set_sweep_power_sweep_time(self, value):
        value = float(value)
        self._sweep_power_sweep_time = value
    
