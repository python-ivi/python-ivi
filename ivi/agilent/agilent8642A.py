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
from .. import rfsiggen

Messages = {0: 'No message',
        2001: 'Frequency sweep with pulse modulation turned off',
        2002: 'Amplitude reference set to 1.00 uV',
        2003: 'Adjusted 0.002uV resolution',
        2004: 'Increment and amplitude reference changed',
        2011: 'Amplitude modulation turned off',
        2012: 'Frequency modulation turned off',
        2013: 'Phase modulation turned off',
        2014: 'Pulse modulation turned off',
        2021: 'Sweep time adjusted',
        2022: 'Frequency sweep turned off',
        2023: 'Frequency sweeep with amplitude modulation turned off',
        2031: 'Amplitude sweep turned off',
        2032: 'AA off, 30 dB max span',
        2033: 'AB off, 30 dB max span',
        2041: 'Increment adjusted',
        2042: 'Amplitude reference adjusted',
        4001: 'Next step not possible',
        4002: 'Not possible, above max',
        4003: 'Not possible, below min',
        4004: 'Select modulation type first',
        4005: 'Select sweep type first',
        4006: 'Please select function',
        4007: 'SP6 prevents int+ext FM',
        4008: 'SP123 turn off sweep first',
        4009: 'SP9 AM limit max amplitude',
        4010: 'Function off, no step',
        4011: 'Function disallows off/on',
        4012: 'Only off/on is active',
        4013: 'No active function',
        4014: 'Nothing to backspace',
        4015: 'No cursor to move',
        4016: 'Invalid shift function',
        4017: 'Invalid terminator',
        4018: 'Bad prefix received',
        4019: 'Maximum of 10 digits',
        4020: 'Number out of range',
        4024: 'Amplitude limits max AM',
        4025: 'AM limits max amplitude',
        4026: 'Only int/ext DC pulse',
        4027: 'Pulse mod only off/on',
        4028: 'AM prevents pulse mod',
        4029: 'Pulse mod prevents AM',
        4030: 'Turn off EMF for dBm',
        4031: 'No relative amplitude sweep',
        4032: 'No relative frequency sweep',
        4033: 'Only frequency/amplitude relative',
        4034: 'Amplitude reference disallows dBuV',
        4035: 'Amplitude sweep disallows dBuV',
        4038: 'FM coupled function limit',
        4039: 'Int+ext FM prevents SP6',
        4040: 'PM limits min frequency',
        4041: 'PM limits max frequency',
        4042: 'Frequency limits max PM',
        4045: 'Frequency sweep auto sweep limitation',
        4046: 'Turn off sweep first',
        4047: 'Frequency sweep with SP8 limitation',
        4048: 'Frequency sweep with SP223 limit',
        4049: 'Frequency sweep with sweep time limit',
        4050: 'SP123 limits min time',
        4051: 'SP123 limits max time',
        4052: 'Amplitude sweep prevents frequency sweep',
        4053: 'FM prevents auto sweep',
        4054: 'Auto sweep prevents FM',
        4055: 'Frequency sweep with FM limit',
        4056: 'DCFM with SP117 and SP216 limit',
        4057: 'Phase modulation prevents auto sweep',
        4058: 'Auto sweep prevents phase modulation',
        4059: 'Frequency sweep with phase modulation limit',
        4063: 'Amplitude span 30dB max',
        4064: 'Amplitude sweep limits min time',
        4065: 'Amplitude sweep prevents SP9',
        4066: 'SP9 prevents amplitude sweep',
        4068: 'Amplitude modulation prevents amplitude sweep',
        4069: 'Amplitude sweep prevents amplitude',
        4070: 'Amplitude sweep prevents amplitude modulation',
        4071: 'Amplitude sweep prevents amplitude off',
        4072: 'Amplitude sweep prevents pulse',
        4073: 'Amplitude sweep prevents SP4',
        4074: 'SP4 prevents amplitude sweep',
        4075: 'SP9 limits min amplitude',
        4076: 'SP9 limits max amplitude',
        4077: 'Amplitude and SP9 limit max AM',
        4078: 'SP9 prevents pulse modulation',
        4079: 'Pulse modulation prevents SP9',
        4080: 'SP9 prevents SP4',
        4081: 'SP4 prevents SP9',
        4082: 'Amplitude modulation prevents SP4',
        4083: 'Pulse prevents SP4',
        4084: 'SP4 prevents amplitude modulation',
        4085: 'SP4 prevents pulse modulation',
        4086: 'Invalid special function',
        4087: 'Some specials stayed on',
        4088: '0.9 Hz limit reached',
        4092: 'Save/recall max = 50',
        4093: 'Recall not defined',
        4094: 'Seq not set, 4 digits required',
        4095: 'Address valid 0-30 only',
        4096: 'Mask valid 0-255 only',
        7001: 'Hit amplitude to clear reverse power protection',
        7002: 'Reverse power protection cleared',
        7010: 'Recall error found',
        7011: 'Message buffer overflowed',
        7020: '10 MHz reference oven cold',
        3000: 'A19 out of lock error',
        3001: 'A19 transient failure',
        5000: 'A6A2 out of lock error',
        5001: 'A6A2 transient failure',
        5002: 'A6A1 out of lock error',
        5003: 'A6A1 transient failure',
        14000: 'A13 out of lock error',
        14001: 'A13 transient failure',
        17000: 'A11 out of lock error',
        17001: 'A11 transient failure',
        18000: 'A12 out of lock error',
        18001: 'A12 transient failure',
        19000: 'A9 out of lock error',
        19001: 'A9 transient failure',
        23000: 'A14 out of lock error',
        23001: 'A14 transient failure',
        25000: 'A7 out of lock error',
        25001: 'A7 transient failure'}

class agilent8642A(ivi.Driver, rfsiggen.Base, rfsiggen.ModulateAM,
        rfsiggen.ModulateFM, rfsiggen.ModulatePM, rfsiggen.AnalogModulationSource,
        rfsiggen.ModulatePulse, rfsiggen.LFGenerator, rfsiggen.LFGeneratorOutput,
        rfsiggen.Sweep, rfsiggen.FrequencySweep, rfsiggen.PowerSweep):
    "Agilent 8642A IVI RF signal generator driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'HP8642A')
        
        super(agilent8642A, self).__init__(*args, **kwargs)
    
        self._identity_description = "Agilent 8642 IVI RF signal generator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 2
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['8642A','8642B'])
        
        self._frequency_low = 10e3
        self._frequency_high = 1050e6
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilent8642A, self).initialize(resource, id_query, reset, **keywargs)
        
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
            self._identity_instrument_model = self._ask("SP340EN")
            self._set_cache_valid()
        return self._identity_instrument_model
    
    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        if self._driver_operation_simulate:
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            self._identity_instrument_firmware_revision = self._ask("SP249").split(' ')[0]
            self._set_cache_valid()
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
        return (code, message)
    
    def _utility_unlock_object(self):
        pass
    
    
    
    def _get_rf_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency = float(self._ask("FROA").split(' ')[1])
            self._set_cache_valid()
        return self._rf_frequency
    
    def _set_rf_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FR %e HZ" % value)
        self._rf_frequency = value
        self._set_cache_valid()
    
    def _get_rf_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level = float(self._ask("APOA").split(' ')[1])
            self._set_cache_valid()
        return self._rf_level
    
    def _set_rf_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AP %e DM" % value)
        self._rf_level = value
        self._set_cache_valid()
    
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
        return self._analog_modulation_am_enabled
    
    def _set_analog_modulation_am_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("AMON")
            else:
                self._write("AMOF")
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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._analog_modulation_am_depth = float(self._ask("AMOA").split(' ')[1])
            self._set_cache_valid()
        return self._analog_modulation_am_depth
    
    def _set_analog_modulation_am_depth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AM %e PC" % value)
        self._analog_modulation_am_depth = value
        self._set_cache_valid()
    
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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._analog_modulation_fm_deviation = float(self._ask("FMOA").split(' ')[1])
            self._set_cache_valid()
        return self._analog_modulation_fm_deviation
    
    def _set_analog_modulation_fm_deviation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FM %e HZ" % value)
        self._analog_modulation_fm_deviation = value
        self._set_cache_valid()
    
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
        self._set_cache_valid()
    
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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._analog_modulation_pm_deviation = float(self._ask("PMOA").split(' ')[1])
            self._set_cache_valid()
        return self._analog_modulation_pm_deviation
    
    def _set_analog_modulation_pm_deviation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("PM %e RD" % value)
        self._analog_modulation_pm_deviation = value
        self._set_cache_valid()
    
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
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._lf_generator_frequency = float(self._ask("MFOA").split(' ')[1])
            self._set_cache_valid()
        return self._lf_generator_frequency
    
    def _set_lf_generator_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("MF %e HZ" % value)
        self._lf_generator_frequency = value
        self._set_cache_valid()
    
    def _get_lf_generator_waveform(self):
        return self._lf_generator_waveform
    
    def _set_lf_generator_waveform(self, value):
        value = int(value)
        self._lf_generator_waveform = value
    
    def _get_lf_generator_output_amplitude(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._lf_generator_output_amplitude = float(self._ask("MLOA").split(' ')[1])
            self._set_cache_valid()
        return self._lf_generator_output_amplitude
    
    def _set_lf_generator_output_amplitude(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("ML %e VL" % value)
        self._lf_generator_output_amplitude = value
        self._set_cache_valid()
    
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
        self._set_cache_valid()
    
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
            self._sweep_frequency_sweep_start = float(self._ask("FAOA").split(' ')[1])
            self._set_cache_valid()
        return self._sweep_frequency_sweep_start
    
    def _set_sweep_frequency_sweep_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FA %e HZ" % value)
        self._sweep_frequency_sweep_start = value
        self._set_cache_valid()
    
    def _get_sweep_frequency_sweep_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_sweep_stop = float(self._ask("FBOA").split(' ')[1])
            self._set_cache_valid()
        return self._sweep_frequency_sweep_stop
    
    def _set_sweep_frequency_sweep_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("FB %e HZ" % value)
        self._sweep_frequency_sweep_stop = value
        self._set_cache_valid()
    
    def _get_sweep_frequency_sweep_time(self):
        return self._sweep_frequency_sweep_time
    
    def _set_sweep_frequency_sweep_time(self, value):
        value = float(value)
        self._sweep_frequency_sweep_time = value
    
    def _get_sweep_power_sweep_start(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_power_sweep_start = float(self._ask("AAOA").split(' ')[1])
            self._set_cache_valid()
        return self._sweep_power_sweep_start
    
    def _set_sweep_power_sweep_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AA %e HZ" % value)
        self._sweep_power_sweep_start = value
        self._set_cache_valid()
    
    def _get_sweep_power_sweep_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_power_sweep_stop = float(self._ask("ABOA").split(' ')[1])
            self._set_cache_valid()
        return self._sweep_power_sweep_stop
    
    def _set_sweep_power_sweep_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("AB %e HZ" % value)
        self._sweep_power_sweep_stop = value
        self._set_cache_valid()
    
    def _get_sweep_power_sweep_time(self):
        return self._sweep_power_sweep_time
    
    def _set_sweep_power_sweep_time(self, value):
        value = float(value)
        self._sweep_power_sweep_time = value
    
