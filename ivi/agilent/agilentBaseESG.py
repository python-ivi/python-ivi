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
from .. import scpi

LFGeneratorWaveformMapping = {
    'sine': 'sine',
    'dual_sine': 'dual',
    'swept_sine': 'swep',
    'square': 'squ',
    'triangle': 'tri',
    'ramp_up': 'ramp',
    #'ramp_down',
    'pulse': 'puls',
    'noise': 'nois',
    'dc': 'dc'
    }

class agilentBaseESG(scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset,
                     scpi.common.SelfTest,
                     rfsiggen.Base, rfsiggen.ModulateAM,
                     rfsiggen.ModulateFM, rfsiggen.ModulatePM, rfsiggen.AnalogModulationSource,
                     rfsiggen.ModulatePulse, rfsiggen.LFGenerator, rfsiggen.LFGeneratorOutput,
                     rfsiggen.Sweep, rfsiggen.FrequencyStep, rfsiggen.PowerStep, rfsiggen.List,
                     extra.common.Memory, ivi.Driver):
    "Agilent ESG series IVI RF signal generator driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(agilentBaseESG, self).__init__(*args, **kwargs)

        self._self_test_delay = 40
        self._memory_size = 1000

        self._rf_frequency_multiplier = 1
        self._rf_frequency_offset = 0.0
        self._rf_frequency_reference = 0.0
        self._rf_frequency_reference_enabled = False
        self._rf_level_offset = 0.0
        self._rf_level_reference = 0.0
        self._rf_level_reference_enabled = False
        self._sweep_frequency_step_points = 2
        self._sweep_power_step_points = 2

        self._frequency_low = 250e3
        self._frequency_high = 4e9

        self._identity_description = "Agilent ESG series IVI RF signal generator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 2
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['E4400B', 'E4420B', 'E4421B', 'E4422B',
                'E4423B', 'E4424B', 'E4425B', 'E4426B', 'E4430B', 'E4431B', 'E4432B', 'E4433B',
                'E4434B', 'E4435B', 'E4436B', 'E4437B'])

        self._add_property('rf.frequency_multiplier',
                        self._get_rf_frequency_multiplier,
                        self._set_rf_frequency_multiplier)
        self._add_property('rf.frequency_offset',
                        self._get_rf_frequency_offset,
                        self._set_rf_frequency_offset)
        self._add_property('rf.frequency_reference',
                        self._get_rf_frequency_reference,
                        self._set_rf_frequency_reference)
        self._add_property('rf.frequency_reference_enabled',
                        self._get_rf_frequency_reference_enabled,
                        self._set_rf_frequency_reference_enabled)
        self._add_property('sweep.frequency_step.points',
                        self._get_sweep_frequency_step_points,
                        self._set_sweep_frequency_step_points)
        self._add_property('sweep.power_step.points',
                        self._get_sweep_power_step_points,
                        self._set_sweep_power_step_points)


    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilentBaseESG, self)._initialize(resource, id_query, reset, **keywargs)

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

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass


    def _load_catalog(self):
        self._catalog = list()
        self._catalog_names = list()
        if not self._driver_operation_simulate:
            raw = self._ask("memory:catalog:all?").lower()

            l = raw.split(',')
            l = [s.strip('"') for s in l]
            self._catalog = [l[i:i+3] for i in range(2, len(l), 3)]
            self._catalog_names = [l[0] for l in self._catalog]

    def _memory_save(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        reg = index % 100
        seq = int(index/100)
        if not self._driver_operation_simulate:
            self._write("*sav %d, %d" % (reg, seq))

    def _memory_recall(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        reg = index % 100
        seq = int(index/100)
        if not self._driver_operation_simulate:
            self._write("*rcl %d, %d" % (reg, seq))
            self.driver_operation.invalidate_all_attributes()

    def _get_rf_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency = float(self._ask("frequency?"))
            self._set_cache_valid()
        return self._rf_frequency

    def _set_rf_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("frequency %e" % value)
        self._rf_frequency = value
        self._set_cache_valid()

    def _get_rf_frequency_multiplier(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency_multiplier = int(self._ask("frequency:multiplier?"))
            self._set_cache_valid()
        return self._rf_frequency_multiplier

    def _set_rf_frequency_multiplier(self, value):
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("frequency:multiplier %d" % value)
        self._rf_frequency_multiplier = value
        self._set_cache_valid()

    def _get_rf_frequency_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency_offset = float(self._ask("frequency:offset?"))
            self._set_cache_valid()
        return self._rf_frequency_offset

    def _set_rf_frequency_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("frequency:offset %e" % value)
        self._rf_frequency_offset = value
        self._set_cache_valid()

    def _get_rf_frequency_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency_reference = float(self._ask("frequency:reference?"))
            self._set_cache_valid()
        return self._rf_frequency_reference

    def _set_rf_frequency_reference(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("frequency:reference %e" % value)
        self._rf_frequency_reference = value
        self._set_cache_valid()

    def _get_rf_frequency_reference_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency_reference_enabled = bool(int(self._ask("frequency:reference:state?")))
            self._set_cache_valid()
        return self._rf_frequency_reference_enabled

    def _set_rf_frequency_reference_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("frequency:reference:state %e" % int(value))
        self._rf_frequency_reference_enabled = value
        self._set_cache_valid()

    def _get_rf_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level = float(self._ask("power:level?"))
            self._set_cache_valid()
        return self._rf_level

    def _set_rf_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("power:level %e" % value)
        self._rf_level = value
        self._set_cache_valid()

    def _get_rf_level_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level_offset = float(self._ask("power:offset?"))
            self._set_cache_valid()
        return self._rf_level_offset

    def _set_rf_level_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("power:offset %e" % value)
        self._rf_level_offset = value
        self._set_cache_valid()

    def _get_rf_level_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level_reference = float(self._ask("power:reference?"))
            self._set_cache_valid()
        return self._rf_level_reference

    def _set_rf_level_reference(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("power:reference %e" % value)
        self._rf_level_reference = value
        self._set_cache_valid()

    def _get_rf_level_reference_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level_reference_enabled = bool(int(self._ask("power:reference:state?")))
            self._set_cache_valid()
        return self._rf_level_reference_enabled

    def _set_rf_level_reference_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("power:reference:state %e" % int(value))
        self._rf_level_reference_enabled = value
        self._set_cache_valid()

    def _get_rf_output_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_output_enabled = bool(int(self._ask("output:state?")))
            self._set_cache_valid()
        return self._rf_output_enabled

    def _set_rf_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("output:state %d" % int(value))
        self._rf_output_enabled = value
        self._set_cache_valid()

    def _get_alc_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._alc_enabled = bool(int(self._ask("power:alc:state?")))
            self._set_cache_valid()
        return self._alc_enabled

    def _set_alc_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("power:alc:state %d" % int(value))
            self._set_cache_valid()
        self._alc_enabled = value

    def _rf_is_settled(self):
        if not self._driver_operation_simulate:
            return int(self._ask("status:questionable:power:condition?")) & (1 << 1) == 0
        return True

    def _rf_wait_until_settled(self, maximum_time):
        t = 0
        while not self._rf_is_settled() and t < maximum_time:
            time.sleep(0.01)
            t = t + 0.01

    def _get_analog_modulation_am_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._analog_modulation_am_enabled = bool(int(self._ask("am:state?")))
            self._set_cache_valid()
        return self._analog_modulation_am_enabled

    def _set_analog_modulation_am_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("am:state %d" % int(value))
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
            self._analog_modulation_am_depth = float(self._ask("am:depth?"))
            self._set_cache_valid()
        return self._analog_modulation_am_depth

    def _set_analog_modulation_am_depth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("am:depth %e" % value)
        self._analog_modulation_am_depth = value
        self._set_cache_valid()

    def _get_analog_modulation_fm_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._analog_modulation_fm_enabled = bool(int(self._ask("fm:state?")))
            self._set_cache_valid()
        return self._analog_modulation_fm_enabled

    def _set_analog_modulation_fm_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("fm:state %d" % int(value))
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
            self._analog_modulation_fm_deviation = float(self._ask("fm:deviation?"))
            self._set_cache_valid()
        return self._analog_modulation_fm_deviation

    def _set_analog_modulation_fm_deviation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("fm:deviation %e" % value)
        self._analog_modulation_fm_deviation = value
        self._set_cache_valid()

    def _get_analog_modulation_pm_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._analog_modulation_pm_enabled = bool(int(self._ask("pm:state?")))
            self._set_cache_valid()
        return self._analog_modulation_pm_enabled

    def _set_analog_modulation_pm_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("pm:state %d" % int(value))
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
            self._analog_modulation_pm_deviation = float(self._ask("pm:deviation?"))
            self._set_cache_valid()
        return self._analog_modulation_pm_deviation

    def _set_analog_modulation_pm_deviation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("pm:deviation %e" % value)
        self._analog_modulation_pm_deviation = value
        self._set_cache_valid()

    def _get_pulse_modulation_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._pulse_modulation_enabled = bool(int(self._ask("pmod:state?")))
            self._set_cache_valid()
        return self._pulse_modulation_enabled

    def _set_pulse_modulation_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("pmod:state %d" % int(value))
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
            self._lf_generator_frequency = float(self._ask("lfoutput:function:frequency?"))
            self._set_cache_valid()
        return self._lf_generator_frequency

    def _set_lf_generator_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("lfoutput:function:frequency %e" % value)
        self._lf_generator_frequency = value
        self._set_cache_valid()

    def _get_lf_generator_waveform(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("lfoutput:function:shape?").lower()
            self._lf_generator_waveform = [k for k,v in LFGeneratorWaveformMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._lf_generator_waveform

    def _set_lf_generator_waveform(self, value):
        if value not in LFGeneratorWaveformMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("lfoutput:function:shape %s" % LFGeneratorWaveformMapping[value])
        self._lf_generator_waveform = value
        self._set_cache_valid()

    def _get_lf_generator_output_amplitude(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._lf_generator_output_amplitude = float(self._ask("lfoutput:amplitude?"))
            self._set_cache_valid()
        return self._lf_generator_output_amplitude

    def _set_lf_generator_output_amplitude(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("lfoutput:amplitude %e" % value)
        self._lf_generator_output_amplitude = value
        self._set_cache_valid()

    def _get_lf_generator_output_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._lf_generator_output_enabled = bool(int(self._ask("lfoutput:state?")))
            self._set_cache_valid()
        return self._lf_generator_output_enabled

    def _set_lf_generator_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("lfoutput:state %d" % int(value))
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

    def _get_sweep_frequency_step_start(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_step_start = float(self._ask("frequency:start?"))
            self._set_cache_valid()
        return self._sweep_frequency_step_start

    def _set_sweep_frequency_step_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("frequency:start %e" % value)
        self._sweep_frequency_step_start = value
        self._set_cache_valid()

    def _get_sweep_frequency_step_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_step_stop = float(self._ask("frequency:stop?"))
            self._set_cache_valid()
        return self._sweep_frequency_step_stop

    def _set_sweep_frequency_step_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("frequency:stop %e" % value)
        self._sweep_frequency_step_stop = value
        self._set_cache_valid()

    def _get_sweep_frequency_step_scaling(self):
        return self._sweep_frequency_step_scaling

    def _set_sweep_frequency_step_scaling(self, value):
        if value not in Scaling:
            raise ivi.ValueNotSupportedException()
        self._sweep_frequency_step_scaling = value

    def _get_sweep_frequency_step_size(self):
        self._sweep_frequency_step_size = abs((self.sweep.frequency_step.stop - self.sweep.frequency_step.start) / (self.sweep.frequency_step.points-1))
        return self._sweep_frequency_step_size

    def _set_sweep_frequency_step_size(self, value):
        value = float(value)
        self.sweep.frequency_step.points = max(int(abs((self.sweep.frequency_step.stop - self.sweep.frequency_step.start) / value))+1, 2)
        self._sweep_frequency_step_size = value

    def _get_sweep_frequency_step_points(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_step_points = int(self._ask("sweep:points?"))
            self._sweep_power_step_points = self._sweep_frequency_step_points
            self._set_cache_valid()
            self._set_cache_valid(True, 'sweep_frequency_step_points')
        return self._sweep_frequency_step_points

    def _set_sweep_frequency_step_points(self, value):
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("sweep:points %d" % value)
        self._sweep_frequency_step_points = value
        self._sweep_power_step_points = value
        self._set_cache_valid()
        self._set_cache_valid(True, 'sweep_frequency_step_points')

    def _get_sweep_frequency_step_single_step_enabled(self):
        return self._sweep_frequency_step_single_step_enabled

    def _set_sweep_frequency_step_single_step_enabled(self, value):
        value = bool(value)
        self._sweep_frequency_step_single_step_enabled = value

    def _get_sweep_frequency_step_dwell(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_frequency_step_dwell = float(self._ask("sweep:dwell?"))
            self._sweep_power_step_dwell = self._sweep_frequency_step_dwell
            self._set_cache_valid()
            self._set_cache_valid(True, 'sweep_power_step_dwell')
        return self._sweep_frequency_step_dwell

    def _set_sweep_frequency_step_dwell(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("sweep:dwell %e" % value)
        self._sweep_frequency_step_dwell = value
        self._sweep_power_step_dwell = value
        self._set_cache_valid()
        self._set_cache_valid(True, 'sweep_power_step_dwell')

    def _sweep_frequency_step_reset(self):
        pass

    def _get_sweep_power_step_start(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_power_step_start = float(self._ask("power:start?"))
            self._set_cache_valid()
        return self._sweep_power_step_start

    def _set_sweep_power_step_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("power:start %e" % value)
        self._sweep_power_step_start = value
        self._set_cache_valid()

    def _get_sweep_power_step_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_power_step_stop = float(self._ask("power:stop?"))
            self._set_cache_valid()
        return self._sweep_power_step_stop

    def _set_sweep_power_step_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("power:stop %e" % value)
        self._sweep_power_step_stop = value
        self._set_cache_valid()

    def _get_sweep_power_step_size(self):
        self._sweep_power_step_size = abs((self.sweep.power_step.stop - self.sweep.power_step.start) / (self.sweep.power_step.points-1))
        return self._sweep_power_step_size

    def _set_sweep_power_step_size(self, value):
        value = float(value)
        self.sweep.power_step.points = max(int(abs((self.sweep.power_step.stop - self.sweep.power_step.start) / value))+1, 2)
        self._sweep_power_step_size = value

    def _get_sweep_power_step_points(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_power_step_points = int(self._ask("sweep:points?"))
            self._sweep_frequency_step_points = self._sweep_power_step_points
            self._set_cache_valid()
            self._set_cache_valid(True, 'sweep_frequency_step_points')
        return self._sweep_power_step_points

    def _set_sweep_power_step_points(self, value):
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("sweep:points %d" % value)
        self._sweep_power_step_points = value
        self._sweep_frequency_step_points = value
        self._set_cache_valid()
        self._set_cache_valid(True, 'sweep_frequency_step_points')

    def _get_sweep_power_step_single_step_enabled(self):
        return self._sweep_power_step_single_step_enabled

    def _set_sweep_power_step_single_step_enabled(self, value):
        value = bool(value)
        self._sweep_power_step_single_step_enabled = value

    def _get_sweep_power_step_dwell(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_power_step_dwell = float(self._ask("sweep:dwell?"))
            self._sweep_frequency_step_dwell = self._sweep_power_step_dwell
            self._set_cache_valid()
            self._set_cache_valid(True, 'sweep_frequency_step_dwell')
        return self._sweep_power_step_dwell

    def _set_sweep_power_step_dwell(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("sweep:dwell %e" % value)
        self._sweep_power_step_dwell = value
        self._sweep_frequency_step_dwell = value
        self._set_cache_valid()
        self._set_cache_valid(True, 'sweep_frequency_step_dwell')

    def _sweep_power_step_reset(self):
        pass

    def _get_sweep_list_selected_list(self):
        return self._sweep_list_selected_list

    def _set_sweep_list_selected_list(self, value):
        value = str(value)
        self._sweep_list_selected_list = value

    def _get_sweep_list_single_step_enabled(self):
        return self._sweep_list_single_step_enabled

    def _set_sweep_list_single_step_enabled(self, value):
        value = bool(value)
        self._sweep_list_single_step_enabled = value

    def _get_sweep_list_dwell(self):
        return self._sweep_list_dwell

    def _set_sweep_list_dwell(self, value):
        value = float(value)
        self._sweep_list_dwell = value

    def _sweep_list_create_frequency(self, name, frequency):
        pass

    def _sweep_list_create_power(self, name, power):
        pass

    def _sweep_list_create_frequency_power(self, name, frequency, power):
        pass

    def _sweep_list_clear_all(self):
        pass

    def _sweep_list_reset(self):
        pass

