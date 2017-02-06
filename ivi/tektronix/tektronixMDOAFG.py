"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2016-2017 Alex Forencich

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

import numpy as np
import struct

from .. import ivi
from .. import fgen

OutputMode = set(['function', 'arbitrary'])
OperationMode = set(['continuous'])
StandardWaveformMapping = {
        'sine': 'sine',
        'square': 'square',
        'triangle': 'ramp',
        'ramp_up': 'ramp',
        'ramp_down': 'ramp',
        'dc': 'dc',
        'pulse': 'pulse',
        'noise': 'noise',
        'dc': 'dc',
        'sinc': 'sinc',
        'exprise': 'erise',
        'expfall': 'edecay',
        'cardiac': 'cardiac',
        'gaussian': 'gaussian',
        'lorentz': 'lorentz',
        'haversine': 'haversine'
        }

class tektronixMDOAFG(fgen.Base, fgen.StdFunc, fgen.ArbWfm, fgen.ArbFrequency,
                fgen.ArbChannelWfm):
    "Tektronix MDO series AFG option IVI function generator driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'MDO3000')

        self._output_standard_waveform_pulse_width = list()
        self._output_standard_waveform_symmetry = list()
        self._output_noise_enabled = list()
        self._output_noise_percent = list()

        super(tektronixMDOAFG, self).__init__(*args, **kwargs)

        # AFG option
        self._output_count = 1
        self._arbitrary_sample_rate = 0
        self._arbitrary_waveform_number_waveforms_max = 0
        self._arbitrary_waveform_size_max = 131072
        self._arbitrary_waveform_size_min = 2
        self._arbitrary_waveform_quantum = 1

        self._add_property('outputs[].standard_waveform.pulse_width',
                        self._get_output_standard_waveform_pulse_width,
                        self._set_output_standard_waveform_pulse_width,
                        None,
                        """
                        Specifies the pulse width for a pulse waveform. This attribute affects
                        function generator behavior only when the Waveform attribute is set to
                        Waveform Pulse. The units are seconds.
                        """)
        self._add_property('outputs[].standard_waveform.symmetry',
                        self._get_output_standard_waveform_symmetry,
                        self._set_output_standard_waveform_symmetry,
                        None,
                        """
                        Specifies the symmetry for a ramp or triangle waveform. This attribute
                        affects function generator behavior only when the Waveform attribute is
                        set to Waveform Triangle, Ramp Up, or Ramp Down. The value is expressed
                        as a percentage.
                        """)
        self._add_property('outputs[].noise.enabled',
                        self._get_output_noise_enabled,
                        self._set_output_noise_enabled,
                        None,
                        """
                        Enables additive noise on the selected channel.
                        """)
        self._add_property('outputs[].noise.percent',
                        self._get_output_noise_percent,
                        self._set_output_noise_percent,
                        None,
                        """
                        Specifies the level of the added noise in percent of the amplitude.
                        """)

        self._identity_description = "Tektronix MDO series AFG option IVI function generator driver"
        self._identity_supported_instrument_models = ['MDO3012', 'MDO3014', 'MDO3022',
                'MDO3024', 'MDO3032', 'MDO3034', 'MDO3052', 'MDO3054', 'MDO3102', 'MDO3104']

        self._init_outputs()

    def _init_outputs(self):
        try:
            super(tektronixMDOAFG, self)._init_outputs()
        except AttributeError:
            pass
        self._output_name = list()
        self._output_operation_mode = list()
        self._output_enabled = list()
        self._output_impedance = list()
        self._output_mode = list()
        self._output_reference_clock_source = list()
        self._output_standard_waveform_pulse_width = list()
        self._output_standard_waveform_ramp_symmetry = list()
        self._output_noise_enabled = list()
        self._output_noise_percent = list()
        for i in range(self._output_count):
            if self._output_count == 1:
                self._output_name.append("afg")
            else:
                self._output_name.append("afg%d" % (i+1))
            self._output_operation_mode.append('continuous')
            self._output_enabled.append(False)
            self._output_impedance.append(50)
            self._output_mode.append('function')
            self._output_reference_clock_source.append('internal')
            self._output_standard_waveform_pulse_width.append(100e-6)
            self._output_standard_waveform_symmetry.append(50.0)
            self._output_noise_enabled.append(False)
            self._output_noise_percent.append(10.0)

        self.outputs._set_list(self._output_name)

    # AFG option
    def _get_output_operation_mode(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_operation_mode[index]

    def _set_output_operation_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in OperationMode:
            raise ivi.ValueNotSupportedException()
        self._output_operation_mode[index] = value

    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:output:state?" % self._output_name[index])
            self._output_enabled[index] = bool(int(resp))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]

    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:output:state %d" % (self._output_name[index], value))
        self._output_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_output_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            val = self._ask(":%s:output:load:impedance?" % self._output_name[index])
            if val == 'HIGHZ':
                self._output_impedance[index] = 1000000
            elif val == 'FIF':
                self._output_impedance[index] = 50
            self._set_cache_valid(index=index)
        return self._output_impedance[index]

    def _set_output_impedance(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if value != 50 and value != 1000000:
            raise Exception('Invalid impedance selection')
        if not self._driver_operation_simulate:
            if value == 1000000:
                self._write(":%s:output:load:impedance highz" % self._output_name[index])
            elif value == 50:
                self._write(":%s:output:load:impedance fifty" % self._output_name[index])
        self._output_impedance[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, 'output_standard_waveform_amplitude', index)

    def _get_output_mode(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:function?" % self._output_name[index]).lower()
            if resp == 'arbitrary':
                self._output_mode[index] = 'arbitrary'
            else:
                self._output_mode[index] = 'function'
            self._set_cache_valid(index=index)
        return self._output_mode[index]

    def _set_output_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in OutputMode:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if value == 'arbitrary':
                self._write(":%s:function arbitrary" % self._output_name[index])
            else:
                if self._get_cache_valid('output_standard_waveform_waveform', index=index):
                    self._set_output_standard_waveform_waveform(index, self._output_standard_waveform_waveform[index])
                else:
                    self._set_output_standard_waveform_waveform(index, 'sine')
        self._output_mode[index] = value
        self._set_cache_valid(index=index)

    def _get_output_reference_clock_source(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_reference_clock_source[index]

    def _set_output_reference_clock_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = 'internal'
        self._output_reference_clock_source[index] = value

    def abort_generation(self):
        pass

    def initiate_generation(self):
        pass

    def _get_output_standard_waveform_amplitude(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:amplitude?" % self._output_name[index])
            self._output_standard_waveform_amplitude[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_amplitude[index]

    def _set_output_standard_waveform_amplitude(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0.01 or value > 5.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:amplitude %e" % (self._output_name[index], value))
        self._output_standard_waveform_amplitude[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_dc_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:offset?" % self._output_name[index])
            self._output_standard_waveform_dc_offset[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_dc_offset[index]

    def _set_output_standard_waveform_dc_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:offset %e" % (self._output_name[index], value))
        self._output_standard_waveform_dc_offset[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_duty_cycle_high(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:square:duty?" % self._output_name[index])
            self._output_standard_waveform_duty_cycle_high[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_duty_cycle_high[index]

    def _set_output_standard_waveform_duty_cycle_high(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 10.0 or value > 90.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:square:duty %e" % (self._output_name[index], value))
        self._output_standard_waveform_duty_cycle_high[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_pulse_width(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:pulse:width?" % self._output_name[index])
            self._output_standard_waveform_pulse_width[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_pulse_width[index]

    def _set_output_standard_waveform_pulse_width(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:pulse:width %e" % (self._output_name[index], value))
        self._output_standard_waveform_pulse_width[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_symmetry(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:ramp:symmetry?" % self._output_name[index])
            self._output_standard_waveform_symmetry[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_symmetry[index]

    def _set_output_standard_waveform_symmetry(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0.0 or value > 100.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:ramp:symmetry %e" % (self._output_name[index], value))
        self._output_standard_waveform_symmetry[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_start_phase(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:phase?" % self._output_name[index])
            self._output_standard_waveform_start_phase[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_start_phase[index]

    def _set_output_standard_waveform_start_phase(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < -180.0 or value > 180.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:phase %e" % (self._output_name[index], value))
        self._output_standard_waveform_start_phase[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_frequency(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:frequency?" % self._output_name[index])
            self._output_standard_waveform_frequency[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_frequency[index]

    def _set_output_standard_waveform_frequency(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0.1 or value > 50e6:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:frequency %e" % (self._output_name[index], value))
        self._output_standard_waveform_frequency[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:function?" % self._output_name[index]).lower()
            if resp == 'arbitrary':
                resp = 'sine'
            resp = [k for k,v in StandardWaveformMapping.items() if v==resp][0]
            if resp == 'ramp_up':
                if self._get_output_standard_waveform_symmetry(index) <= 10.0:
                    resp = 'ramp_down'
                elif self._get_output_standard_waveform_symmetry(index) >= 90.0:
                    resp = 'ramp_up'
                else:
                    resp = 'triangle'
            self._output_standard_waveform_waveform[index] = resp
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_waveform[index]

    def _set_output_standard_waveform_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in StandardWaveformMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":%s:function %s" % (self._output_name[index], StandardWaveformMapping[value]))
            if value == 'triangle':
                if self._get_output_standard_waveform_symmetry(index) <= 10.0 or self._get_output_standard_waveform_symmetry(index) >= 90:
                    self._set_output_standard_waveform_symmetry(index, 50.0)
            elif value == 'ramp_up':
                self._set_output_standard_waveform_symmetry(index, 100.0)
            elif value == 'ramp_down':
                self._set_output_standard_waveform_symmetry(index, 0.0)
        self._output_standard_waveform_waveform[index] = value
        self._set_cache_valid(index=index)
        self._output_mode[index] = 'function'
        self._set_cache_valid(True, 'output_mode', index=index)

    def _get_output_noise_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:noiseadd:state?" % self._output_name[index])
            self._output_noise_enabled[index] = bool(int(resp))
            self._set_cache_valid(index=index)
        return self._output_noise_enabled[index]

    def _set_output_noise_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:noiseadd:state %d" % (self._output_name[index], value))
        self._output_noise_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_output_noise_percent(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:noiseadd:percent?" % self._output_name[index])
            self._output_noise_percent[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_noise_percent[index]

    def _set_output_noise_percent(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0.0 or value > 100.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:noiseadd:percent %e" % (self._output_name[index], value))
        self._output_noise_percent[index] = value
        self._set_cache_valid(index=index)

    def _get_output_arbitrary_gain(self, index):
        return self._get_output_standard_waveform_amplitude(index)

    def _set_output_arbitrary_gain(self, index, value):
        self._set_output_standard_waveform_amplitude(index, value)

    def _get_output_arbitrary_offset(self, index):
        return self._get_output_standard_waveform_dc_offset(index)

    def _set_output_arbitrary_offset(self, index, value):
        self._set_output_standard_waveform_dc_offset(index, value)

    def _get_output_arbitrary_waveform(self, index):
        index = ivi.get_index(self._output_name, index) 
        return self._output_arbitrary_waveform[index]

    def _set_output_arbitrary_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value)
        self._output_arbitrary_waveform[index] = value

    def _get_arbitrary_sample_rate(self):
        return self._arbitrary_sample_rate

    def _set_arbitrary_sample_rate(self, value):
        value = float(value)
        self._arbitrary_sample_rate = value

    def _get_arbitrary_waveform_number_waveforms_max(self):
        return self._arbitrary_waveform_number_waveforms_max

    def _get_arbitrary_waveform_size_max(self):
        return self._arbitrary_waveform_size_max

    def _get_arbitrary_waveform_size_min(self):
        return self._arbitrary_waveform_size_min

    def _get_arbitrary_waveform_quantum(self):
        return self._arbitrary_waveform_quantum

    def _arbitrary_waveform_clear(self, handle):
        pass

    def _arbitrary_waveform_configure(self, index, handle, gain, offset):
        self._set_output_arbitrary_waveform(index, handle)
        self._set_output_arbitrary_gain(index, gain)
        self._set_output_arbitrary_offset(index, offset)

    def _arbitrary_waveform_create(self, data):
        return "handle"

    def _get_output_arbitrary_frequency(self, index):
        return self._get_output_standard_waveform_frequency(index)

    def _set_output_arbitrary_frequency(self, index, value):
        self._set_output_standard_waveform_frequency(index, value)

    def _arbitrary_waveform_create_channel_waveform(self, index, data):
        y = None
        x = None
        if type(data) == list and type(data[0]) == float:
            # list
            y = array(data)
        elif type(data) == np.ndarray and len(data.shape) == 1:
            # 1D array
            y = data
        elif type(data) == np.ndarray and len(data.shape) == 2 and data.shape[0] == 1:
            # 2D array, hieght 1
            y = data[0]
        elif type(data) == np.ndarray and len(data.shape) == 2 and data.shape[1] == 1:
            # 2D array, width 1
            y = data[:,0]
        else:
            x, y = ivi.get_sig(data)

        if len(y) % self._arbitrary_waveform_quantum != 0:
            raise ivi.ValueNotSupportedException()

        # clip on [-1,1]
        yc = y.clip(-1, 1)

        raw_data = yc.astype('<f').tobytes()

        self._write(':%s:arbitrary:emem:points:encdg binary' % self._output_name[index])
        self._write_ieee_block(raw_data, ':%s:arbitrary:emem:points ' % self._output_name[index])

        return self._output_name[index]
