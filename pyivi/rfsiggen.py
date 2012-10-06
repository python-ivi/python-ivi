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

from . import ivi

# Exceptions
class FrequencyListUnknownException(ivi.IviException): pass

# Parameter Values
Scaling = set(['linear', 'logarithmic'])
ExternalCoupling = set(['ac', 'dc'])
Source = set(['internal', 'external'])
Polarity = set(['normal', 'inverse'])
Slope = set(['positive', 'negative'])
LFGeneratorWaveform = set(['sine', 'square', 'triangle', 'ramp_up', 'ramp_down'])
SweepMode = set(['none', 'frequency_sweep', 'power_sweep', 'frequency_step', 'power_step', 'list'])
TriggerSource = set(['immediate', 'external', 'software'])
IQSource = set(['digital_modulation_base', 'cdma_base', 'tdma_base', 'arb_generator', 'external'])
DigitalModulationBaseDataSource = set(['external', 'prbs', 'bit_sequence'])
DigitalModulationBasePRBSType = set(['prbs9', 'prbs11', 'prbs15', 'prbs16', 'prbs20', 'prbs21', 'prbs23'])
ClockType = set(['bit', 'symbol'])

class Base(object):
    "Base IVI methods for all RF signal generators"
    
    def __init__(self):
        super(Base, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenBase')
        
        self._rf_frequency = 1e8
        self._rf_level = 0
        self._rf_output_enabled = False
        self._alc_enabled = False
        
        self.__dict__.setdefault('rf', ivi.PropertyCollection())
        self.rf._add_property('frequency',
                        self._get_rf_frequency,
                        self._set_rf_frequency)
        self.rf._add_property('level',
                        self._get_rf_level,
                        self._set_rf_level)
        self.rf._add_property('output_enabled',
                        self._get_rf_output_enabled,
                        self._set_rf_output_enabled)
        self.rf.configure = self._rf_configure
        self.rf.disable_all_modulation = self._rf_disable_all_modulation
        self.rf.is_settled = self._rf_is_settled
        self.rf.wait_until_settled = self._rf_wait_until_settled
        self.__dict__.setdefault('alc', ivi.PropertyCollection())
        self.alc._add_property('enabled',
                        self._get_alc_enabled,
                        self._set_alc_enabled)
    
    def _get_rf_frequency(self):
        return self._rf_frequency
    
    def _set_rf_frequency(self, value):
        value = float(value)
        self._rf_frequency = value
    
    def _get_rf_level(self):
        return self._rf_level
    
    def _set_rf_level(self, value):
        value = float(value)
        self._rf_level = value
    
    def _get_rf_output_enabled(self):
        return self._rf_output_enabled
    
    def _set_rf_output_enabled(self, value):
        value = bool(value)
        self._rf_output_enabled = value
    
    def _get_alc_enabled(self):
        return self._alc_enabled
    
    def _set_alc_enabled(self, value):
        value = bool(value)
        self._alc_enabled = value
    
    def _rf_configure(self, frequency, level):
        self._set_rf_frequency(frequency)
        self._set_rf_level(level)
    
    def _rf_disable_all_modulation(self):
        try:
            self._set_analog_modulation_am_enabled(False)
        except:
            pass
        try:
            self._set_analog_modulation_fm_enabled(False)
        except:
            pass
        try:
            self._set_analog_modulation_pm_enabled(False)
        except:
            pass
        try:
            self._set_pulse_modulation_enabled(False)
        except:
            pass
    
    def _rf_is_settled(self):
        return True
    
    def _rf_wait_until_settled(self, maximum_time):
        pass
    
    
class ModulateAM(object):
    "Extension IVI methods for generators supporting amplitude modulation"
    
    def __init__(self):
        super(ModulateAM, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenModulateAM')
        
        self._analog_modulation_am_enabled = False
        self._analog_modulation_am_source = ""
        self._analog_modulation_am_scaling = 0
        self._analog_modulation_am_external_coupling = 0
        self._analog_modulation_am_nominal_voltage = 0
        self._analog_modulation_am_depth = 0
        
        self.__dict__.setdefault('analog_modulation', ivi.PropertyCollection())
        self.analog_modulation.__dict__.setdefault('am', ivi.PropertyCollection())
        self.analog_modulation.am._add_property('enabled',
                        self._get_analog_modulation_am_enabled,
                        self._set_analog_modulation_am_enabled)
        self.analog_modulation.am._add_property('source',
                        self._get_analog_modulation_am_source,
                        self._set_analog_modulation_am_source)
        self.analog_modulation.am._add_property('scaling',
                        self._get_analog_modulation_am_scaling,
                        self._set_analog_modulation_am_scaling)
        self.analog_modulation.am._add_property('external_coupling',
                        self._get_analog_modulation_am_external_coupling,
                        self._set_analog_modulation_am_external_coupling)
        self.analog_modulation.am._add_property('nominal_voltage',
                        self._get_analog_modulation_am_nominal_voltage,
                        self._set_analog_modulation_am_nominal_voltage)
        self.analog_modulation.am._add_property('depth',
                        self._get_analog_modulation_am_depth,
                        self._set_analog_modulation_am_depth)
        self.analog_modulation.am.configure = self._analog_modulation_am_configure
    
    def _get_analog_modulation_am_enabled(self):
        return self._analog_modulation_am_enabled
    
    def _set_analog_modulation_am_enabled(self, value):
        value = bool(value)
        self._analog_modulation_am_enabled = value
    
    def _get_analog_modulation_am_source(self):
        return self._analog_modulation_am_source
    
    def _set_analog_modulation_am_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
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
    
    def _analog_modulation_am_configure(self, source, scaling, depth):
        self._set_analog_modulation_am_source(source)
        self._set_analog_modulation_am_scaling(scaling)
        self._set_analog_modulation_am_depth(depth)
    
    
class ModulateFM(object):
    "Extension IVI methods for generators supporting frequency modulation"
    
    def __init__(self):
        super(ModulateFM, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenModulateFM')
        
        self._analog_modulation_fm_enabled = False
        self._analog_modulation_fm_source = ""
        self._analog_modulation_fm_external_coupling = 0
        self._analog_modulation_fm_nominal_voltage = 0
        self._analog_modulation_fm_deviation = 0
        
        self.__dict__.setdefault('analog_modulation', ivi.PropertyCollection())
        self.analog_modulation.__dict__.setdefault('fm', ivi.PropertyCollection())
        self.analog_modulation.fm._add_property('enabled',
                        self._get_analog_modulation_fm_enabled,
                        self._set_analog_modulation_fm_enabled)
        self.analog_modulation.fm._add_property('source',
                        self._get_analog_modulation_fm_source,
                        self._set_analog_modulation_fm_source)
        self.analog_modulation.fm._add_property('external_coupling',
                        self._get_analog_modulation_fm_external_coupling,
                        self._set_analog_modulation_fm_external_coupling)
        self.analog_modulation.fm._add_property('nominal_voltage',
                        self._get_analog_modulation_fm_nominal_voltage,
                        self._set_analog_modulation_fm_nominal_voltage)
        self.analog_modulation.fm._add_property('deviation',
                        self._get_analog_modulation_fm_deviation,
                        self._set_analog_modulation_fm_deviation)
        self.analog_modulation.fm.configure = self._analog_modulation_fm_configure
    
    def _get_analog_modulation_fm_enabled(self):
        return self._analog_modulation_fm_enabled
    
    def _set_analog_modulation_fm_enabled(self, value):
        value = bool(value)
        self._analog_modulation_fm_enabled = value
    
    def _get_analog_modulation_fm_source(self):
        return self._analog_modulation_fm_source
    
    def _set_analog_modulation_fm_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
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
        self._analog_modulation_fm_deviation = value
    
    def _analog_modulation_fm_configure(self, source, deviation):
        self._set_analog_modulation_fm_source(source)
        self._set_analog_modulation_fm_deviation(deviation)
    
    
class ModulatePM(object):
    "Extension IVI methods for generators supporting phase modulation"
    
    def __init__(self):
        super(ModulatePM, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenModulatePM')
        
        self._analog_modulation_pm_enabled = False
        self._analog_modulation_pm_source = ""
        self._analog_modulation_pm_external_coupling = 0
        self._analog_modulation_pm_nominal_voltage = 0
        self._analog_modulation_pm_deviation = 0
        
        self.__dict__.setdefault('analog_modulation', ivi.PropertyCollection())
        self.analog_modulation.__dict__.setdefault('pm', ivi.PropertyCollection())
        self.analog_modulation.pm._add_property('enabled',
                        self._get_analog_modulation_pm_enabled,
                        self._set_analog_modulation_pm_enabled)
        self.analog_modulation.pm._add_property('source',
                        self._get_analog_modulation_pm_source,
                        self._set_analog_modulation_pm_source)
        self.analog_modulation.pm._add_property('external_coupling',
                        self._get_analog_modulation_pm_external_coupling,
                        self._set_analog_modulation_pm_external_coupling)
        self.analog_modulation.pm._add_property('nominal_voltage',
                        self._get_analog_modulation_pm_nominal_voltage,
                        self._set_analog_modulation_pm_nominal_voltage)
        self.analog_modulation.pm._add_property('deviation',
                        self._get_analog_modulation_pm_deviation,
                        self._set_analog_modulation_pm_deviation)
        self.analog_modulation.pm.configure = self._analog_modulation_pm_configure
    
    def _get_analog_modulation_pm_enabled(self):
        return self._analog_modulation_pm_enabled
    
    def _set_analog_modulation_pm_enabled(self, value):
        value = bool(value)
        self._analog_modulation_pm_enabled = value
    
    def _get_analog_modulation_pm_source(self):
        return self._analog_modulation_pm_source
    
    def _set_analog_modulation_pm_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
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
        return self._analog_modulation_pm_deviation
    
    def _set_analog_modulation_pm_deviation(self, value):
        value = float(value)
        self._analog_modulation_pm_deviation = value
    
    def _analog_modulation_pm_configure(self, source, deviation):
        self._set_analog_modulation_pm_source(source)
        self._set_analog_modulation_pm_deviation(deviation)
    
    
class AnalogModulationSource(object):
    "Extension IVI methods for generators supporting analog modulation"
    
    def __init__(self):
        super(AnalogModulationSource, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenAnalogModulationSource')
        
        self._analog_modulation_source_count = 0
        self._analog_modulation_source_name = list()
    
    def _get_analog_modulation_source_count(self):
        return self._analog_modulation_source_count
    
    def _get_analog_modulation_source_name(self, index):
        if index < 0 or index >= self._analog_modulation_source_count: raise Exception('Channel out of range')
        return self._analog_modulation_source_name[index]
    
    
class ModulatePulse:
    "Extension IVI methods for generators supporting pulse modulation"
    
    def __init__(self):
        super(ModulatePulse, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenModulatePulse')
        
        self._pulse_modulation_enabled = False
        self._pulse_modulation_source = ""
        self._pulse_modulation_external_polarity = 0
        
        self.__dict__.setdefault('pulse_modulation', ivi.PropertyCollection())
        self.pulse_modulation._add_property('enabled',
                        self._get_pulse_modulation_enabled,
                        self._set_pulse_modulation_enabled)
        self.pulse_modulation._add_property('source',
                        self._get_pulse_modulation_source,
                        self._set_pulse_modulation_source)
        self.pulse_modulation._add_property('external_polarity',
                        self._get_pulse_modulation_external_polarity,
                        self._set_pulse_modulation_external_polarity)
    
    def _get_pulse_modulation_enabled(self):
        return self._pulse_modulation_enabled
    
    def _set_pulse_modulation_enabled(self, value):
        value = bool(value)
        self._pulse_modulation_enabled = value
    
    def _get_pulse_modulation_source(self):
        return self._pulse_modulation_source
    
    def _set_pulse_modulation_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._pulse_modulation_source = value
    
    def _get_pulse_modulation_external_polarity(self):
        return self._pulse_modulation_external_polarity
    
    def _set_pulse_modulation_external_polarity(self, value):
        value = int(value)
        self._pulse_modulation_external_polarity = value
    
    
class LFGenerator(object):
    "Extension IVI methods for generators with internal analog modulation sources"
    
    def __init__(self):
        super(LFGenerator, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenLFGenerator')
        
        self._lf_generator_active_lf_generator = ""
        self._lf_generator_count = 0
        self._lf_generator_name = list()
        self._lf_generator_frequency = 0
        self._lf_generator_waveform = 0
        
        self.__dict__.setdefault('lf_generator', ivi.PropertyCollection())
        self.lf_generator._add_property('active_lf_generator',
                        self._get_lf_generator_active_lf_generator,
                        self._set_lf_generator_active_lf_generator)
        self.lf_generator._add_property('frequency',
                        self._get_lf_generator_frequency,
                        self._set_lf_generator_frequency)
        self.lf_generator._add_property('waveform',
                        self._get_lf_generator_waveform,
                        self._set_lf_generator_waveform)
        self.lf_generator.configure = self._lf_generator_configure
    
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
        return self._lf_generator_frequency
    
    def _set_lf_generator_frequency(self, value):
        value = float(value)
        self._lf_generator_frequency = value
    
    def _get_lf_generator_waveform(self):
        return self._lf_generator_waveform
    
    def _set_lf_generator_waveform(self, value):
        value = int(value)
        self._lf_generator_waveform = value
    
    def _lf_generator_configure(self, frequency, waveform):
        self._set_lf_generator_frequency(frequency)
        self._set_lf_generator_waveform(waveform)
    
    
class LFGeneratorOutput(object):
    "Extension IVI methods for generators with internal analog modulation sources"
    
    def __init__(self):
        super(LFGeneratorOutput, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenLFGeneratorOutput')
        
        self._lf_generator_output_amplitude = 0
        self._lf_generator_output_enabled = 0
        
        self.__dict__.setdefault('lf_generator', ivi.PropertyCollection())
        self.lf_generator.__dict__.setdefault('output', ivi.PropertyCollection())
        self.lf_generator.output._add_property('enabled',
                        self._get_lf_generator_output_enabled,
                        self._set_lf_generator_output_enabled)
        self.lf_generator.output._add_property('amplitude',
                        self._get_lf_generator_output_amplitude,
                        self._set_lf_generator_output_amplitude)
        self.lf_generator.output.configure = self._lf_generator_output_configure
    
    def _get_lf_generator_output_amplitude(self):
        return self._lf_generator_output_amplitude
    
    def _set_lf_generator_output_amplitude(self, value):
        value = float(value)
        self._lf_generator_output_amplitude = value
    
    def _get_lf_generator_output_enabled(self):
        return self._lf_generator_output_enabled
    
    def _set_lf_generator_output_enabled(self, value):
        value = bool(value)
        self._lf_generator_output_enabled = value
    
    def _lf_generator_output_configure(self, amplitude, enabled):
        self._set_lf_generator_output_amplitude(amplitude)
        self._set_lf_generator_output_enabled(enabled)
    
    
class PulseGenerator(object):
    "Extension IVI methods for generators with internal pulse modulation sources"
    
    def __init__(self):
        super(ModulatePulse, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenPulseGenerator')
        
        self._pulse_generator_internal_trigger_period = 0
        self._pulse_generator_width = 0
        self._pulse_generator_gating_enabled = False
        self._pulse_generator_trigger_source = ""
        self._pulse_generator_external_trigger_slope = 0
        self._pulse_generator_external_trigger_delay = 0
        
        self.__dict__.setdefault('pulse_generator', ivi.PropertyCollection())
        self.pulse_generator._add_property('internal_trigger_period',
                        self._get_pulse_generator_internal_trigger_period,
                        self._set_pulse_generator_internal_trigger_period)
        self.pulse_generator._add_property('width',
                        self._get_pulse_generator_width,
                        self._set_pulse_generator_width)
        self.pulse_generator._add_property('gating_enabled',
                        self._get_pulse_generator_gating_enabled,
                        self._set_pulse_generator_gating_enabled)
        self.pulse_generator._add_property('trigger_source',
                        self._get_pulse_generator_trigger_source,
                        self._set_pulse_generator_trigger_source)
        self.pulse_generator._add_property('external_trigger_slope',
                        self._get_pulse_generator_external_trigger_slope,
                        self._set_pulse_generator_external_trigger_slope)
        self.pulse_generator._add_property('external_trigger_delay',
                        self._get_pulse_generator_external_trigger_delay,
                        self._set_pulse_generator_external_trigger_delay)
        self.pulse_generator.configure_external_trigger = self._pulse_generator_configure_external_trigger
        self.pulse_generator.configure = self._pulse_generator_configure
    
    def _get_pulse_generator_internal_trigger_period(self):
        return self._pulse_generator_internal_trigger_period
    
    def _set_pulse_generator_internal_trigger_period(self, value):
        value = float(value)
        self._pulse_generator_internal_trigger_period = value
    
    def _get_pulse_generator_width(self):
        return self._pulse_generator_width
    
    def _set_pulse_generator_width(self, value):
        value = float(value)
        self._pulse_generator_width = value
    
    def _get_pulse_generator_gating_enabled(self):
        return self._pulse_generator_gating_enabled
    
    def _set_pulse_generator_gating_enabled(self, value):
        value = bool(value)
        self._pulse_generator_gating_enabled = value
    
    def _get_pulse_generator_trigger_source(self):
        return self._pulse_generator_trigger_source
    
    def _set_pulse_generator_trigger_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._pulse_generator_trigger_source = value
    
    def _get_pulse_generator_external_trigger_slope(self):
        return self._pulse_generator_external_trigger_slope
    
    def _set_pulse_generator_external_trigger_slope(self, value):
        value = int(value)
        self._pulse_generator_external_trigger_slope = value
    
    def _get_pulse_generator_external_trigger_delay(self):
        return self._pulse_generator_external_trigger_delay
    
    def _set_pulse_generator_external_trigger_delay(self, value):
        value = float(value)
        self._pulse_generator_external_trigger_delay = value
    
    def _pulse_generator_configure_external_trigger(self, slope, delay):
        self._set_pulse_generator_external_trigger_slope(slope)
        self._set_pulse_generator_external_trigger_delay(delay)
    
    def _pulse_generator_configure(self, trigger_source, pulse_width, gating_enabled):
        self._set_pulse_generator_trigger_source(trigger_source)
        self._set_pulse_generator_width(pulse_width)
        self._set_pulse_generator_gating_enabled(gating_enabled)
    
    
class PulseDoubleGenerator(object):
    "Extension IVI methods for generators with internal double pulse modulation sources"
    
    def __init__(self):
        super(PulseDoubleGenerator, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenPulseDoubleGenerator')
        
        self._pulse_generator_double_pulse_enabled = False
        self._pulse_generator_double_pulse_delay = 0
        
        self.__dict__.setdefault('pulse_generator', ivi.PropertyCollection())
        self.pulse_generator.__dict__.setdefault('double_pulse', ivi.PropertyCollection())
        self.pulse_generator.double_pulse._add_property('enabled',
                        self._get_pulse_generator_double_pulse_enabled,
                        self._set_pulse_generator_double_pulse_enabled)
        self.pulse_generator.double_pulse._add_property('delay',
                        self._get_pulse_generator_double_pulse_delay,
                        self._set_pulse_generator_double_pulse_delay)
        self.pulse_generator.double_pulse.configure = self._pulse_generator_double_pulse_configure
    
    def _get_pulse_generator_double_pulse_enabled(self):
        return self._pulse_generator_double_pulse_enabled
    
    def _set_pulse_generator_double_pulse_enabled(self, value):
        value = bool(value)
        self._pulse_generator_double_pulse_enabled = value
    
    def _get_pulse_generator_double_pulse_delay(self):
        return self._pulse_generator_double_pulse_delay
    
    def _set_pulse_generator_double_pulse_delay(self, value):
        value = float(value)
        self._pulse_generator_double_pulse_delay = value
    
    def _pulse_generator_double_pulse_configure(self, enabled, delay):
        self._set_pulse_generator_double_pulse_enabled(enabled)
        self._set_pulse_generator_double_pulse_delay(delay)
    
    
class PulseGeneratorOutput(object):
    "Extension IVI methods for generators with internal pulse modulation sources"
    
    def __init__(self):
        super(PulseGenerator, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenPulseGeneratorOutput')
        
        self._pulse_generator_output_polarity = 0
        self._pulse_generator_output_enabled = 0
        
        self.__dict__.setdefault('pulse_generator', ivi.PropertyCollection())
        self.pulse_generator.__dict__.setdefault('output', ivi.PropertyCollection())
        self.pulse_generator.output._add_property('polarity',
                        self._get_pulse_generator_output_polarity,
                        self._set_pulse_generator_output_polarity)
        self.pulse_generator.output._add_property('enabled',
                        self._get_pulse_generator_output_enabled,
                        self._set_pulse_generator_output_enabled)
        self.pulse_generator.output.configure = self._pulse_generator_output_configure
    
    def _get_pulse_generator_output_polarity(self):
        return self._pulse_generator_output_polarity
    
    def _set_pulse_generator_output_polarity(self, value):
        value = int(value)
        self._pulse_generator_output_polarity = value
    
    def _get_pulse_generator_output_enabled(self):
        return self._pulse_generator_output_enabled
    
    def _set_pulse_generator_output_enabled(self, value):
        value = bool(value)
        self._pulse_generator_output_enabled = value
    
    def _pulse_generator_output_configure(self, polarity, enabled):
        self._set_pulse_generator_output_polarity(polarity)
        self._set_pulse_generator_output_enabled(enabled)
    
    
class Sweep(object):
    "Extension IVI methods for generators that support sweeping"
    
    def __init__(self):
        super(Sweep, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenSweep')
        
        self._sweep_mode = 0
        self._sweep_trigger_source = ""
        
        self.__dict__.setdefault('sweep', ivi.PropertyCollection())
        self.sweep._add_property('mode',
                        self._get_sweep_mode,
                        self._set_sweep_mode)
        self.sweep._add_property('trigger_source',
                        self._get_sweep_trigger_source,
                        self._set_sweep_trigger_source)
        self.sweep.configure = self._sweep_configure
    
    def _get_sweep_mode(self):
        return self._sweep_mode
    
    def _set_sweep_mode(self, value):
        value = int(value)
        self._sweep_mode = value
    
    def _get_sweep_trigger_source(self):
        return self._sweep_trigger_source
    
    def _set_sweep_trigger_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._sweep_trigger_source = value
    
    def _sweep_configure(self, mode, trigger_source):
        self._set_sweep_mode(mode)
        self._set_sweep_trigger_source(trigger_source)
    
    
class FrequencySweep(object):
    "Extension IVI methods for generators that support frequency sweeping"
    
    def __init__(self):
        super(FrequencySweep, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenFrequencySweep')
        
        self._sweep_frequency_sweep_start = 0
        self._sweep_frequency_sweep_stop = 0
        self._sweep_frequency_sweep_time = 0
        
        self.__dict__.setdefault('sweep', ivi.PropertyCollection())
        self.sweep.__dict__.setdefault('frequency_sweep', ivi.PropertyCollection())
        self.sweep.frequency_sweep._add_property('start',
                        self._get_sweep_frequency_sweep_start,
                        self._set_sweep_frequency_sweep_start)
        self.sweep.frequency_sweep._add_property('stop',
                        self._get_sweep_frequency_sweep_stop,
                        self._set_sweep_frequency_sweep_stop)
        self.sweep.frequency_sweep._add_property('time',
                        self._get_sweep_frequency_sweep_time,
                        self._set_sweep_frequency_sweep_time)
        self.sweep.frequency_sweep.configure_start_stop = self._sweep_frequency_sweep_configure_start_stop
        self.sweep.frequency_sweep.configure_center_span = self._sweep_frequency_sweep_configure_center_span
    
    def _get_sweep_frequency_sweep_start(self):
        return self._sweep_frequency_sweep_start
    
    def _set_sweep_frequency_sweep_start(self, value):
        value = float(value)
        self._sweep_frequency_sweep_start = value
    
    def _get_sweep_frequency_sweep_stop(self):
        return self._sweep_frequency_sweep_stop
    
    def _set_sweep_frequency_sweep_stop(self, value):
        value = float(value)
        self._sweep_frequency_sweep_stop = value
    
    def _get_sweep_frequency_sweep_time(self):
        return self._sweep_frequency_sweep_time
    
    def _set_sweep_frequency_sweep_time(self, value):
        value = float(value)
        self._sweep_frequency_sweep_time = value
    
    def _sweep_frequency_sweep_configure_start_stop(self, start, stop):
        self._set_sweep_frequency_sweep_start(start)
        self._set_sweep_frequency_sweep_stop(stop)
    
    def _sweep_frequency_sweep_configure_center_span(self, center, span):
        self._set_sweep_frequency_sweep_start(center - span/2)
        self._set_sweep_frequency_sweep_stop(center + span/2)
    
    
class PowerSweep(object):
    "Extension IVI methods for generators that support power sweeping"
    
    def __init__(self):
        super(PowerSweep, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenPowerSweep')
        
        self._sweep_power_sweep_start = 0
        self._sweep_power_sweep_stop = 0
        self._sweep_power_sweep_time = 0
        
        self.__dict__.setdefault('sweep', ivi.PropertyCollection())
        self.sweep.__dict__.setdefault('power_sweep', ivi.PropertyCollection())
        self.sweep.power_sweep._add_property('start',
                        self._get_sweep_power_sweep_start,
                        self._set_sweep_power_sweep_start)
        self.sweep.power_sweep._add_property('stop',
                        self._get_sweep_power_sweep_stop,
                        self._set_sweep_power_sweep_stop)
        self.sweep.power_sweep._add_property('time',
                        self._get_sweep_power_sweep_time,
                        self._set_sweep_power_sweep_time)
        self.sweep.power_sweep.configure_start_stop = self._sweep_power_sweep_configure_start_stop
    
    def _get_sweep_power_sweep_start(self):
        return self._sweep_power_sweep_start
    
    def _set_sweep_power_sweep_start(self, value):
        value = float(value)
        self._sweep_power_sweep_start = value
    
    def _get_sweep_power_sweep_stop(self):
        return self._sweep_power_sweep_stop
    
    def _set_sweep_power_sweep_stop(self, value):
        value = float(value)
        self._sweep_power_sweep_stop = value
    
    def _get_sweep_power_sweep_time(self):
        return self._sweep_power_sweep_time
    
    def _set_sweep_power_sweep_time(self, value):
        value = float(value)
        self._sweep_power_sweep_time = value
    
    def _sweep_power_sweep_configure_start_stop(self, start, stop):
        self._set_sweep_power_sweep_start(start)
        self._set_sweep_power_sweep_stop(stop)
    
    
class FrequencyStep(object):
    "Extension IVI methods for generators that support frequency sweeping in steps"
    
    def __init__(self):
        super(FrequencyStep, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenFrequencyStep')
        
        self._sweep_frequency_step_start = 0
        self._sweep_frequency_step_stop = 0
        self._sweep_frequency_step_scaling = 'linear'
        self._sweep_frequency_step_size = 0
        self._sweep_frequency_step_single_step_enabled = False
        self._sweep_frequency_step_dwell = 0
        
        self.__dict__.setdefault('sweep', ivi.PropertyCollection())
        self.sweep.__dict__.setdefault('frequency_step', ivi.PropertyCollection())
        self.sweep.frequency_step._add_property('start',
                        self._get_sweep_frequency_step_start,
                        self._set_sweep_frequency_step_start)
        self.sweep.frequency_step._add_property('stop',
                        self._get_sweep_frequency_step_stop,
                        self._set_sweep_frequency_step_stop)
        self.sweep.frequency_step._add_property('scaling',
                        self._get_sweep_frequency_step_scaling,
                        self._set_sweep_frequency_step_scaling)
        self.sweep.frequency_step._add_property('size',
                        self._get_sweep_frequency_step_size,
                        self._set_sweep_frequency_step_size)
        self.sweep.frequency_step._add_property('single_step_enabled',
                        self._get_sweep_frequency_step_single_step_enabled,
                        self._set_sweep_frequency_step_single_step_enabled)
        self.sweep.frequency_step._add_property('dwell',
                        self._get_sweep_frequency_step_dwell,
                        self._set_sweep_frequency_step_dwell)
        self.sweep.frequency_step.configure_start_stop = self._sweep_frequency_step_configure_start_stop
        self.sweep.frequency_step.configure_dwell = self._sweep_frequency_step_configure_dwell
        self.sweep.frequency_step.reset = self._sweep_frequency_step_reset
    
    def _get_sweep_frequency_step_start(self):
        return self._sweep_frequency_step_start
    
    def _set_sweep_frequency_step_start(self, value):
        value = float(value)
        self._sweep_frequency_step_start = value
    
    def _get_sweep_frequency_step_stop(self):
        return self._sweep_frequency_step_stop
    
    def _set_sweep_frequency_step_stop(self, value):
        value = float(value)
        self._sweep_frequency_step_stop = value
    
    def _get_sweep_frequency_step_scaling(self):
        return self._sweep_frequency_step_scaling
    
    def _set_sweep_frequency_step_scaling(self, value):
        if value not in Scaling:
            raise ivi.ValueNotSupportedException()
        self._sweep_frequency_step_scaling = value
    
    def _get_sweep_frequency_step_size(self):
        return self._sweep_frequency_step_size
    
    def _set_sweep_frequency_step_size(self, value):
        value = float(value)
        self._sweep_frequency_step_size = value
    
    def _get_sweep_frequency_step_single_step_enabled(self):
        return self._sweep_frequency_step_single_step_enabled
    
    def _set_sweep_frequency_step_single_step_enabled(self, value):
        value = bool(value)
        self._sweep_frequency_step_single_step_enabled = value
    
    def _get_sweep_frequency_step_dwell(self):
        return self._sweep_frequency_step_dwell
    
    def _set_sweep_frequency_step_dwell(self, value):
        value = float(value)
        self._sweep_frequency_step_dwell = value
    
    def _sweep_frequency_step_configure_start_stop(self, start, stop, scaling, size):
        self._set_sweep_frequency_step_start(start)
        self._set_sweep_frequency_step_stop(stop)
        self._set_sweep_frequency_step_scaling(scaling)
        self._set_sweep_frequency_step_size(size)
    
    def _sweep_frequency_step_configure_dwell(self, single_step_enabled, dwell):
        self._set_sweep_frequency_step_single_step_enabled(single_step_enabled)
        self._set_sweep_frequency_step_dwell(dwell)
    
    def _sweep_frequency_step_reset(self):
        pass
    
    
class PowerStep(object):
    "Extension IVI methods for generators that support power sweeping in steps"
    
    def __init__(self):
        super(PowerStep, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenPowerStep')
        
        self._sweep_power_step_start = 0
        self._sweep_power_step_stop = 0
        self._sweep_power_step_size = 0
        self._sweep_power_step_single_step_enabled = False
        self._sweep_power_step_dwell = 0
        
        self.__dict__.setdefault('sweep', ivi.PropertyCollection())
        self.sweep.__dict__.setdefault('power_step', ivi.PropertyCollection())
        self.sweep.power_step._add_property('start',
                        self._get_sweep_power_step_start,
                        self._set_sweep_power_step_start)
        self.sweep.power_step._add_property('stop',
                        self._get_sweep_power_step_stop,
                        self._set_sweep_power_step_stop)
        self.sweep.power_step._add_property('size',
                        self._get_sweep_power_step_size,
                        self._set_sweep_power_step_size)
        self.sweep.power_step._add_property('single_step_enabled',
                        self._get_sweep_power_step_single_step_enabled,
                        self._set_sweep_power_step_single_step_enabled)
        self.sweep.power_step._add_property('dwell',
                        self._get_sweep_power_step_dwell,
                        self._set_sweep_power_step_dwell)
        self.sweep.power_step.configure_start_stop = self._sweep_power_step_configure_start_stop
        self.sweep.power_step.configure_dwell = self._sweep_power_step_configure_dwell
        self.sweep.power_step.reset = self._sweep_power_step_reset
    
    def _get_sweep_power_step_start(self):
        return self._sweep_power_step_start
    
    def _set_sweep_power_step_start(self, value):
        value = float(value)
        self._sweep_power_step_start = value
    
    def _get_sweep_power_step_stop(self):
        return self._sweep_power_step_stop
    
    def _set_sweep_power_step_stop(self, value):
        value = float(value)
        self._sweep_power_step_stop = value
    
    def _get_sweep_power_step_size(self):
        return self._sweep_power_step_size
    
    def _set_sweep_power_step_size(self, value):
        value = float(value)
        self._sweep_power_step_size = value
    
    def _get_sweep_power_step_single_step_enabled(self):
        return self._sweep_power_step_single_step_enabled
    
    def _set_sweep_power_step_single_step_enabled(self, value):
        value = bool(value)
        self._sweep_power_step_single_step_enabled = value
    
    def _get_sweep_power_step_dwell(self):
        return self._sweep_power_step_dwell
    
    def _set_sweep_power_step_dwell(self, value):
        value = float(value)
        self._sweep_power_step_dwell = value
    
    def _sweep_power_step_configure_start_stop(self, start, stop, size):
        self._set_sweep_power_step_start(start)
        self._set_sweep_power_step_stop(stop)
        self._set_sweep_power_step_size(size)
    
    def _sweep_power_step_configure_dwell(self, single_step_enabled, dwell):
        self._set_sweep_power_step_single_step_enabled(single_step_enabled)
        self._set_sweep_power_step_dwell(dwell)
    
    def _sweep_power_step_reset(self):
        pass
    
    
class List(object):
    "Extension IVI methods for generators that support frequency and power selection a list"
    
    def __init__(self):
        super(List, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenList')
        
        self._sweep_list_selected_list = ''
        self._sweep_list_single_step_enabled = False
        self._sweep_list_dwell = 0
        
        self.__dict__.setdefault('sweep', ivi.PropertyCollection())
        self.sweep.__dict__.setdefault('list', ivi.PropertyCollection())
        self.sweep.list._add_property('selected_list',
                        self._get_sweep_list_selected_list,
                        self._set_sweep_list_selected_list)
        self.sweep.list._add_property('single_step_enabled',
                        self._get_sweep_list_single_step_enabled,
                        self._set_sweep_list_single_step_enabled)
        self.sweep.list._add_property('dwell',
                        self._get_sweep_list_dwell,
                        self._set_sweep_list_dwell)
        self.sweep.list.create_frequency = self._sweep_list_create_frequency
        self.sweep.list.create_power = self._sweep_list_create_power
        self.sweep.list.create_frequency_power = self._sweep_list_create_frequency_power
        self.sweep.list.clear_all = self._sweep_list_clear_all
        self.sweep.list.configure_dwell = self._sweep_list_configure_dwell
        self.sweep.list.reset = self._sweep_list_reset
    
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
    
    def _sweep_list_configure_dwell(self, single_step_enabled, dwell):
        self._set_sweep_list_single_step_enabled(single_step_enabled)
        self._set_sweep_list_dwell(dwell)
    
    def _sweep_list_reset(self):
        pass
    
    
class ALC(object):
    "Extension IVI methods for generators that support automatic level control"
    
    def __init__(self):
        super(ALC, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenALC')
        
        self._alc_source = 'internal'
        self._alc_bandwidth = 0
        
        self.__dict__.setdefault('alc', ivi.PropertyCollection())
        self.alc._add_property('source',
                        self._get_alc_source,
                        self._set_alc_source)
        self.alc._add_property('bandwidth',
                        self._get_alc_bandwidth,
                        self._set_alc_bandwidth)
        self.alc.configure = self._alc_configure
    
    def _get_alc_source(self):
        return self._alc_source
    
    def _set_alc_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._alc_source = value
    
    def _get_alc_bandwidth(self):
        return self._alc_bandwidth
    
    def _set_alc_bandwidth(self, bandwidth):
        value = float(value)
        self._alc_bandwidth = value
    
    def _alc_configure(self, source, bandwidth):
        self._set_alc_source = source
        self._set_alc_bandwidth = bandwidth
    
    
class ReferenceOscillator(object):
    "Extension IVI methods for generators that support a configurable frequency reference"
    
    def __init__(self):
        super(ReferenceOscillator, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenReferenceOscillator')
        
        self._reference_oscillator_source = 'internal'
        self._reference_oscillator_external_frequency = 0
        
        self.__dict__.setdefault('reference_oscillator', ivi.PropertyCollection())
        self.reference_oscillator._add_property('source',
                        self._get_reference_oscillator_source,
                        self._set_reference_oscillator_source)
        self.reference_oscillator._add_property('external_frequency',
                        self._get_reference_oscillator_external_frequency,
                        self._set_reference_oscillator_external_frequency)
        self.reference_oscillator.configure = self._reference_oscillator_configure
    
    def _get_reference_oscillator_source(self):
        return self._reference_oscillator_source
    
    def _set_reference_oscillator_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._reference_oscillator_source = value
    
    def _get_reference_oscillator_external_frequency(self):
        return self._reference_oscillator_external_frequency
    
    def _set_reference_oscillator_external_frequency(self, external_frequency):
        value = float(value)
        self._reference_oscillator_external_frequency = value
    
    def _reference_oscillator_configure(self, source, external_frequency):
        self._set_reference_oscillator_source = source
        self._set_reference_oscillator_external_frequency = external_frequency
    
    
class SoftwareTrigger(object):
    "Extension IVI methods for generators that support software triggering"
    
    def __init__(self):
        super(SoftwareTrigger, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenSoftwareTrigger')
        
    
    
class ModulateIQ(object):
    "Extension IVI methods for generators supporting IQ (vector) modulation"
    
    def __init__(self):
        super(ModulateIQ, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenModulateIQ')
        
        self._iq_enabled = False
        self._iq_source = 'digital_modulation_base'
        self._iq_nominal_voltage = 0
        self._iq_swap_enabled = False
        
        self.__dict__.setdefault('iq', ivi.PropertyCollection())
        self.iq._add_property('enabled',
                        self._get_iq_enabled,
                        self._set_iq_enabled)
        self.iq._add_property('source',
                        self._get_iq_source,
                        self._set_iq_source)
        self.iq._add_property('nominal_voltage',
                        self._get_iq_nominal_voltage,
                        self._set_iq_nominal_voltage)
        self.iq._add_property('swap_enabled',
                        self._get_iq_swap_enabled,
                        self._set_iq_swap_enabled)
        self.iq.configure = self._iq_configure
        self.iq.calibrate = self._iq_calibrate
    
    def _get_iq_enabled(self):
        return self._iq_enabled
    
    def _set_iq_enabled(self, value):
        value = bool(value)
        self._iq_enabled = value
    
    def _get_iq_source(self):
        return self._iq_source
    
    def _set_iq_source(self, value):
        if value not in IQSource:
            raise ivi.ValueNotSupportedException()
        self._iq_source = value
    
    def _get_iq_nominal_voltage(self):
        return self._iq_nominal_voltage
    
    def _set_iq_nominal_voltage(self, value):
        value = float(value)
        self._iq_nominal_voltage = value
    
    def _get_iq_swap_enabled(self):
        return self._iq_swap_enabled
    
    def _set_iq_swap_enabled(self, value):
        value = bool(value)
        self._iq_swap_enabled = value
    
    def _iq_configure(self, source, swap_enabled):
        self._set_iq_source(source)
        self._set_iq_swap_enabled(swap_enabled)
    
    def _iq_calibrate(self):
        pass
    
    
class IQImpairment(object):
    "Extension IVI methods for generators supporting IQ modulation simulation or correction of IQ impairment"
    
    def __init__(self):
        super(IQImpairment, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenIQImpairment')
        
        self._iq_impairment_enabled = False
        self._iq_impairment_i_offset = 0
        self._iq_impairment_q_offset = 0
        self._iq_impairment_iq_ratio = 0
        self._iq_impairment_iq_skew = 0
        
        self.__dict__.setdefault('iq', ivi.PropertyCollection())
        self.iq.__dict__.setdefault('impairment', ivi.PropertyCollection())
        self.iq.impairment._add_property('enabled',
                        self._get_iq_impairment_enabled,
                        self._set_iq_impairment_enabled)
        self.iq.impairment._add_property('i_offset',
                        self._get_iq_impairment_i_offset,
                        self._set_iq_impairment_i_offset)
        self.iq.impairment._add_property('q_offset',
                        self._get_iq_impairment_q_offset,
                        self._set_iq_impairment_q_offset)
        self.iq.impairment._add_property('iq_ratio',
                        self._get_iq_impairment_iq_ratio,
                        self._set_iq_impairment_iq_ratio)
        self.iq.impairment._add_property('iq_skew',
                        self._get_iq_impairment_iq_skew,
                        self._set_iq_impairment_iq_skew)
        self.iq.impairment.configure = self._iq_impairment_configure
    
    def _get_iq_impairment_enabled(self):
        return self._iq_impairment_enabled
    
    def _set_iq_impairment_enabled(self, value):
        value = bool(value)
        self._iq_impairment_enabled = value
    
    def _get_iq_impairment_i_offset(self):
        return self._iq_impairment_i_offset
    
    def _set_iq_impairment_i_offset(self, value):
        value = float(value)
        self._iq_impairment_i_offset = value
    
    def _get_iq_impairment_q_offset(self):
        return self._iq_impairment_q_offset
    
    def _set_iq_impairment_q_offset(self, value):
        value = float(value)
        self._iq_impairment_q_offset = value
    
    def _get_iq_impairment_iq_ratio(self):
        return self._iq_impairment_iq_ratio
    
    def _set_iq_impairment_iq_ratio(self, value):
        value = float(value)
        self._iq_impairment_iq_ratio = value
    
    def _get_iq_impairment_iq_skew(self):
        return self._iq_impairment_iq_skew
    
    def _set_iq_impairment_iq_skew(self, value):
        value = float(value)
        self._iq_impairment_iq_skew = value
    
    def _iq_impairment_configure(self, i_offset, q_offset, iq_ratio, iq_skew):
        self._set_iq_impairment_i_offset(i_offset)
        self._set_iq_impairment_q_offset(q_offset)
        self._set_iq_impairment_iq_ratio(iq_ratio)
        self._set_iq_impairment_iq_skew(iq_skew)
    
    
class ArbGenerator(object):
    "Extension IVI methods for generators with internal arbitrary waveform generators"
    
    def __init__(self):
        super(ArbGenerator, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenArbGenerator')
        
        self._digital_modulation_arb_selected_waveform = ''
        self._digital_modulation_arb_clock_frequency = 0
        self._digital_modulation_arb_filter_frequency = 0
        self._digital_modulation_arb_max_number_waveforms = 0
        self._digital_modulation_arb_waveform_quantum = 0
        self._digital_modulation_arb_waveform_size_min = 0
        self._digital_modulation_arb_waveform_size_max = 0
        self._digital_modulation_arb_trigger_source = 'immediate'
        self._digital_modulation_arb_external_trigger_slope = 'positive'
        
        self.__dict__.setdefault('digital_modulation', ivi.PropertyCollection())
        self.digital_modulation.__dict__.setdefault('arb', ivi.PropertyCollection())
        self.digital_modulation.arb._add_property('selected_waveform',
                        self._get_digital_modulation_arb_selected_waveform,
                        self._set_digital_modulation_arb_selected_waveform)
        self.digital_modulation.arb._add_property('clock_frequency',
                        self._get_digital_modulation_arb_clock_frequency,
                        self._set_digital_modulation_arb_clock_frequency)
        self.digital_modulation.arb._add_property('filter_frequency',
                        self._get_digital_modulation_arb_filter_frequency,
                        self._set_digital_modulation_arb_filter_frequency)
        self.digital_modulation.arb._add_property('max_number_waveforms',
                        self._get_digital_modulation_arb_max_number_waveforms)
        self.digital_modulation.arb._add_property('waveform_quantum',
                        self._get_digital_modulation_arb_waveform_quantum)
        self.digital_modulation.arb._add_property('waveform_size_min',
                        self._get_digital_modulation_arb_waveform_size_min)
        self.digital_modulation.arb._add_property('waveform_size_max',
                        self._get_digital_modulation_arb_waveform_size_max)
        self.digital_modulation.arb._add_property('trigger_source',
                        self._get_digital_modulation_arb_trigger_source,
                        self._set_digital_modulation_arb_trigger_source)
        self.digital_modulation.arb._add_property('external_trigger_slope',
                        self._get_digital_modulation_arb_external_trigger_slope,
                        self._set_digital_modulation_arb_external_trigger_slope)
        self.digital_modulation.arb.configure = self._digital_modulation_arb_configure
        self.digital_modulation.arb.write_waveform = self._digital_modulation_arb_write_waveform
        self.digital_modulation.arb.clear_all_waveforms = self._digital_modulation_arb_clear_all_waveforms
    
    def _get_digital_modulation_arb_selected_waveform(self):
        return self._digital_modulation_arb_selected_waveform
    
    def _set_digital_modulation_arb_selected_waveform(self, value):
        value = str(value)
        self._digital_modulation_arb_selected_waveform = value
    
    def _get_digital_modulation_arb_clock_frequency(self):
        return self._digital_modulation_arb_clock_frequency
    
    def _set_digital_modulation_arb_clock_frequency(self, value):
        value = float(value)
        self._digital_modulation_arb_clock_frequency = value
    
    def _get_digital_modulation_arb_filter_frequency(self):
        return self._digital_modulation_arb_filter_frequency
    
    def _set_digital_modulation_arb_filter_frequency(self, value):
        value = float(value)
        self._digital_modulation_arb_filter_frequency = value
    
    def _get_digital_modulation_arb_max_number_waveforms(self):
        return self._digital_modulation_arb_max_number_waveforms
    
    def _get_digital_modulation_arb_waveform_quantum(self):
        return self._digital_modulation_arb_waveform_quantum
    
    def _get_digital_modulation_arb_waveform_size_min(self):
        return self._digital_modulation_arb_waveform_size_min
    
    def _get_digital_modulation_arb_waveform_size_max(self):
        return self._digital_modulation_arb_waveform_size_max
    
    def _get_digital_modulation_arb_trigger_source(self):
        return self._digital_modulation_arb_trigger_source
    
    def _set_digital_modulation_arb_trigger_source(self, value):
        if value not in TriggerSource:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_arb_trigger_source = value
    
    def _get_digital_modulation_arb_external_trigger_slope(self):
        return self._digital_modulation_arb_external_trigger_slope
    
    def _set_digital_modulation_arb_external_trigger_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_arb_external_trigger_slope = value
    
    def _digital_modulation_arb_configure(self, clock_frequency, filter_frequency):
        self._set_digital_modulation_arb_clock_frequency(clock_frequency)
        self._set_digital_modulation_arb_filter_frequency(filter_frequency)
    
    def _digital_modulation_arb_write_waveform(self, name, idata, qdata, more_data_pending):
        pass
    
    def _digital_modulation_arb_clear_all_waveforms(self):
        pass
    
    
class DigitalModulationBase(object):
    "Extension IVI methods for generators supporting generation of standard wireless communication signals"
    
    def __init__(self):
        super(DigitalModulationBase, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenDigitalModulationBase')
        
        self._digital_modulation_base_standard_names = list()
        self._digital_modulation_base_selected_standard = ''
        self._digital_modulation_base_data_source = 'prbs'
        self._digital_modulation_base_prbs_type = 'prbs9'
        self._digital_modulation_base_selected_bit_sequence = ''
        self._digital_modulation_base_clock_source = 'internal'
        self._digital_modulation_base_external_clock_type = 'bit'
        
        self.__dict__.setdefault('digital_modulation', ivi.PropertyCollection())
        self.digital_modulation.__dict__.setdefault('base', ivi.PropertyCollection())
        self.digital_modulation.base._add_property('standard_names',
                        self._get_digital_modulation_base_standard_names)
        self.digital_modulation.base._add_property('selected_standard',
                        self._get_digital_modulation_base_selected_standard,
                        self._set_digital_modulation_base_selected_standard)
        self.digital_modulation.base._add_property('data_source',
                        self._get_digital_modulation_base_data_source,
                        self._set_digital_modulation_base_data_source)
        self.digital_modulation.base._add_property('prbs_type',
                        self._get_digital_modulation_base_prbs_type,
                        self._set_digital_modulation_base_prbs_type)
        self.digital_modulation.base._add_property('selected_bit_sequence',
                        self._get_digital_modulation_base_selected_bit_sequence,
                        self._set_digital_modulation_base_selected_bit_sequence)
        self.digital_modulation.base._add_property('clock_source',
                        self._get_digital_modulation_base_clock_source,
                        self._set_digital_modulation_base_clock_source)
        self.digital_modulation.base._add_property('external_clock_type',
                        self._get_digital_modulation_base_external_clock_type,
                        self._set_digital_modulation_base_external_clock_type)
        self.digital_modulation.base.configure_clock_source = self._digital_modulation_base_configure_clock_source
        self.digital_modulation.base.create_bit_sequence = self._digital_modulation_base_create_bit_sequence
        self.digital_modulation.base.clear_all_bit_sequences = self._digital_modulation_base_clear_all_bit_sequences
    
    def _get_digital_modulation_base_standard_names(self):
        return self._digital_modulation_base_standard_names
    
    def _get_digital_modulation_base_selected_standard(self):
        return self._digital_modulation_base_selected_standard
    
    def _set_digital_modulation_base_selected_standard(self, value):
        value = str(value)
        self._digital_modulation_base_selected_standard = value
    
    def _get_digital_modulation_base_data_source(self):
        return self._digital_modulation_base_data_source
    
    def _set_digital_modulation_base_data_source(self, value):
        if value not in DigitalModulationBaseDataSource:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_base_data_source = value
    
    def _get_digital_modulation_base_prbs_type(self):
        return self._digital_modulation_base_prbs_type
    
    def _set_digital_modulation_base_prbs_type(self, value):
        if value not in DigitalModulationBasePRBSType:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_base_prbs_type = value
    
    def _get_digital_modulation_base_selected_bit_sequence(self):
        return self._digital_modulation_base_selected_bit_sequence
    
    def _set_digital_modulation_base_selected_bit_sequence(self, value):
        value = str(value)
        self._digital_modulation_base_selected_bit_sequence = value
    
    def _get_digital_modulation_base_clock_source(self):
        return self._digital_modulation_base_clock_source
    
    def _set_digital_modulation_base_clock_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_base_clock_source = value
    
    def _get_digital_modulation_base_external_clock_type(self):
        return self._digital_modulation_base_external_clock_type
    
    def _set_digital_modulation_base_external_clock_type(self, value):
        if value not in ClockType:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_base_external_clock_type = value
    
    def _digital_modulation_base_configure_clock_source(self, source, type):
        self._set_digital_modulation_base_clock_source(source)
        self._set_digital_modulation_base_external_clock_type(type)
    
    def _digital_modulation_base_create_bit_sequence(self, name, bit_count, sequence, more_data_pending):
        pass
    
    def _digital_modulation_base_clear_all_bit_sequences(self):
        pass
    
    
class CDMABase(object):
    "Extension IVI methods for generators supporting generation of CDMA wireless communication signals"
    
    def __init__(self):
        super(CDMABase, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenCDMABase')
        
        self._digital_modulation_cdma_standard_names = list()
        self._digital_modulation_cdma_selected_standard = ''
        self._digital_modulation_cdma_trigger_source = 'immediate'
        self._digital_modulation_cdma_external_trigger_slope = 'positive'
        self._digital_modulation_cdma_test_model_names = list()
        self._digital_modulation_cdma_selected_test_model = ''
        self._digital_modulation_cdma_clock_source = 'internal'
        
        self.__dict__.setdefault('digital_modulation', ivi.PropertyCollection())
        self.digital_modulation.__dict__.setdefault('cdma', ivi.PropertyCollection())
        self.digital_modulation.cdma._add_property('standard_names',
                        self._get_digital_modulation_cdma_standard_names)
        self.digital_modulation.cdma._add_property('selected_standard',
                        self._get_digital_modulation_cdma_selected_standard,
                        self._set_digital_modulation_cdma_selected_standard)
        self.digital_modulation.cdma._add_property('trigger_source',
                        self._get_digital_modulation_cdma_trigger_source,
                        self._set_digital_modulation_cdma_trigger_source)
        self.digital_modulation.cdma._add_property('external_trigger_slope',
                        self._get_digital_modulation_cdma_external_trigger_slope,
                        self._set_digital_modulation_cdma_external_trigger_slope)
        self.digital_modulation.cdma._add_property('test_model_names',
                        self._get_digital_modulation_cdma_test_model_names)
        self.digital_modulation.cdma._add_property('selected_test_model',
                        self._get_digital_modulation_cdma_selected_test_model,
                        self._set_digital_modulation_cdma_selected_test_model)
        self.digital_modulation.cdma._add_property('clock_source',
                        self._get_digital_modulation_cdma_clock_source,
                        self._set_digital_modulation_cdma_clock_source)
    
    def _get_digital_modulation_cdma_standard_names(self):
        return self._digital_modulation_cdma_standard_names
    
    def _get_digital_modulation_cdma_selected_standard(self):
        return self._digital_modulation_cdma_selected_standard
    
    def _set_digital_modulation_cdma_selected_standard(self, value):
        value = str(value)
        self._digital_modulation_cdma_selected_standard = value
    
    def _get_digital_modulation_cdma_trigger_source(self):
        return self._digital_modulation_cdma_trigger_source
    
    def _set_digital_modulation_cdma_trigger_source(self, value):
        if value not in TriggerSource:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_cdma_trigger_source = value
    
    def _get_digital_modulation_cdma_external_trigger_slope(self):
        return self._digital_modulation_cdma_external_trigger_slope
    
    def _set_digital_modulation_cdma_external_trigger_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_cdma_external_trigger_slope = value
    
    def _get_digital_modulation_cdma_test_model_names(self):
        return self._digital_modulation_cdma_test_model_names
    
    def _get_digital_modulation_cdma_selected_test_model(self):
        return self._digital_modulation_cdma_selected_test_model
    
    def _set_digital_modulation_cdma_selected_test_model(self, value):
        value = str(value)
        self._digital_modulation_cdma_selected_test_model = value
    
    def _get_digital_modulation_cdma_clock_source(self):
        return self._digital_modulation_cdma_clock_source
    
    def _set_digital_modulation_cdma_clock_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_cdma_clock_source = value
    
    
class TDMABase(object):
    "Extension IVI methods for generators supporting generation of TDMA wireless communication signals"
    
    def __init__(self):
        super(TDMABase, self).__init__()
        
        self.__dict__.setdefault('_identity_group_capabilities', list())
        self._identity_group_capabilities.insert(0, 'IviRFSigGenTDMABase')
        
        self._digital_modulation_tdma_standard_names = list()
        self._digital_modulation_tdma_selected_standard = ''
        self._digital_modulation_tdma_trigger_source = 'immediate'
        self._digital_modulation_tdma_external_trigger_slope = 'positive'
        self._digital_modulation_tdma_frame_names = list()
        self._digital_modulation_tdma_selected_frame = ''
        self._digital_modulation_tdma_clock_source = 'internal'
        self._digital_modulation_tdma_external_clock_type = 'bit'
        
        self.__dict__.setdefault('digital_modulation', ivi.PropertyCollection())
        self.digital_modulation.__dict__.setdefault('tdma', ivi.PropertyCollection())
        self.digital_modulation.tdma._add_property('standard_names',
                        self._get_digital_modulation_tdma_standard_names)
        self.digital_modulation.tdma._add_property('selected_standard',
                        self._get_digital_modulation_tdma_selected_standard,
                        self._set_digital_modulation_tdma_selected_standard)
        self.digital_modulation.tdma._add_property('trigger_source',
                        self._get_digital_modulation_tdma_trigger_source,
                        self._set_digital_modulation_tdma_trigger_source)
        self.digital_modulation.tdma._add_property('external_trigger_slope',
                        self._get_digital_modulation_tdma_external_trigger_slope,
                        self._set_digital_modulation_tdma_external_trigger_slope)
        self.digital_modulation.tdma._add_property('frame_names',
                        self._get_digital_modulation_tdma_frame_names)
        self.digital_modulation.tdma._add_property('selected_frame',
                        self._get_digital_modulation_tdma_selected_frame,
                        self._set_digital_modulation_tdma_selected_frame)
        self.digital_modulation.tdma._add_property('clock_source',
                        self._get_digital_modulation_tdma_clock_source,
                        self._set_digital_modulation_tdma_clock_source)
        self.digital_modulation.tdma._add_property('external_clock_type',
                        self._get_digital_modulation_tdma_external_clock_type,
                        self._set_digital_modulation_tdma_external_clock_type)
        self.digital_modulation.tdma.configure_clock_source = self._digital_modulation_tdma_configure_clock_source
    
    def _get_digital_modulation_tdma_standard_names(self):
        return self._digital_modulation_tdma_standard_names
    
    def _get_digital_modulation_tdma_selected_standard(self):
        return self._digital_modulation_tdma_selected_standard
    
    def _set_digital_modulation_tdma_selected_standard(self, value):
        value = str(value)
        self._digital_modulation_tdma_selected_standard = value
    
    def _get_digital_modulation_tdma_trigger_source(self):
        return self._digital_modulation_tdma_trigger_source
    
    def _set_digital_modulation_tdma_trigger_source(self, value):
        if value not in TriggerSource:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_tdma_trigger_source = value
    
    def _get_digital_modulation_tdma_external_trigger_slope(self):
        return self._digital_modulation_tdma_external_trigger_slope
    
    def _set_digital_modulation_tdma_external_trigger_slope(self, value):
        if value not in Slope:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_tdma_external_trigger_slope = value
    
    def _get_digital_modulation_tdma_frame_names(self):
        return self._digital_modulation_tdma_frame_names
    
    def _get_digital_modulation_tdma_selected_frame(self):
        return self._digital_modulation_tdma_selected_frame
    
    def _set_digital_modulation_tdma_selected_frame(self, value):
        value = str(value)
        self._digital_modulation_tdma_selected_frame = value
    
    def _get_digital_modulation_tdma_clock_source(self):
        return self._digital_modulation_tdma_clock_source
    
    def _set_digital_modulation_tdma_clock_source(self, value):
        if value not in Source:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_tdma_clock_source = value
    
    def _get_digital_modulation_tdma_external_clock_type(self):
        return self._digital_modulation_tdma_external_clock_type
    
    def _set_digital_modulation_tdma_external_clock_type(self, value):
        if value not in ClockType:
            raise ivi.ValueNotSupportedException()
        self._digital_modulation_tdma_external_clock_type = value
    
    def _digital_modulation_tdma_configure_clock_source(self, source, type):
        self._set_digital_modulation_tdma_clock_source(source)
        self._set_digital_modulation_tdma_external_clock_type(type)
    
    

