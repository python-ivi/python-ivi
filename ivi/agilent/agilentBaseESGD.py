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

import math
import struct
import numpy as np

from .. import ivi
from .. import rfsiggen

from .agilentBaseESG import *

IQSource = set(['digital_modulation_base', 'cdma_base', 'tdma_base', 'arb_generator', 'external'])

class agilentBaseESGD(agilentBaseESG, rfsiggen.ModulateIQ, rfsiggen.IQImpairment,
        rfsiggen.ArbGenerator, rfsiggen.DigitalModulationBase, rfsiggen.CDMABase,
        rfsiggen.TDMABase):
    "Agilent ESG-D series IVI RF signal generator driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(agilentBaseESGD, self).__init__(*args, **kwargs)

        self._digital_modulation_arb_clock_frequency = 10e6
        self._digital_modulation_arb_filter_frequency = 2.5e6
        self._digital_modulation_arb_max_number_waveforms = 1024
        self._digital_modulation_arb_waveform_quantum = 2
        self._digital_modulation_arb_waveform_size_min = 16
        self._digital_modulation_arb_waveform_size_max = 10240

        self._identity_description = "Agilent ESG-D series IVI RF signal generator driver"
        self._identity_supported_instrument_models = list(['E4430B', 'E4431B', 'E4432B', 'E4433B',
                'E4434B', 'E4435B', 'E4436B', 'E4437B'])

    def _load_arb_catalog(self):
        self._arb_catalog = list()
        self._arb_catalog_names = list()
        if not self._driver_operation_simulate:
            raw = self._ask("mmemory:catalog? \"arbi:\"").lower()

            l = raw.split(',')
            l = [s.strip('"') for s in l]
            self._arb_catalog = [l[i:i+3] for i in range(2, len(l), 3)]
            self._arb_catalog_names = [l[0] for l in self._arb_catalog]

    def _get_iq_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._iq_enabled = bool(int(self._ask("dm:state?")))
            self._set_cache_valid()
        return self._iq_enabled

    def _set_iq_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("dm:state %d" % int(value))
        self._iq_enabled = value
        self._set_cache_valid()

    def _get_iq_source(self):
        return self._iq_source

    def _set_iq_source(self, value):
        if value not in IQSource:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if value == 'arb_generator':
                self._write("radio:arb:state 1")
        self._iq_source = value

    def _get_iq_nominal_voltage(self):
        return self._iq_nominal_voltage

    def _set_iq_nominal_voltage(self, value):
        value = float(value)
        self._iq_nominal_voltage = value

    def _get_iq_swap_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._iq_swap_enabled = self._ask("dm:polarity?").lower() == 'inv'
            self._set_cache_valid()
        return self._iq_swap_enabled

    def _set_iq_swap_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("dm:polarity %s" % ('inverted' if value else 'normal'))
        self._iq_swap_enabled = value
        self._set_cache_valid()

    def _iq_calibrate(self):
        if not self._driver_operation_simulate:
            self._write("calibration:iq")

    def _get_iq_impairment_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._iq_impairment_enabled = bool(int(self._ask("dm:iqadjustment:state?")))
            self._set_cache_valid()
        return self._iq_impairment_enabled

    def _set_iq_impairment_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("dm:iqadjustment:state %d" % int(value))
        self._iq_impairment_enabled = value
        self._set_cache_valid()

    def _get_iq_impairment_i_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._iq_impairment_i_offset = float(self._ask("dm:iqadjustment:ioffset?"))
            self._set_cache_valid()
        return self._iq_impairment_i_offset

    def _set_iq_impairment_i_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("dm:iqadjustment:ioffoset %e" % value)
        self._iq_impairment_i_offset = value
        self._set_cache_valid()

    def _get_iq_impairment_q_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._iq_impairment_q_offset = float(self._ask("dm:iqadjustment:qoffset?"))
            self._set_cache_valid()
        return self._iq_impairment_q_offset

    def _set_iq_impairment_q_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("dm:iqadjustment:qoffoset %e" % value)
        self._iq_impairment_q_offset = value
        self._set_cache_valid()

    def _get_iq_impairment_iq_ratio(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            # instrument value is in dB, but driver value is in percent
            value = float(self._ask("dm:iqadjustment:gain?"))
            self._iq_impairment_iq_ratio = math.copysign(100*(10**(abs(value)/10)-1), value)
            self._set_cache_valid()
        return self._iq_impairment_iq_ratio

    def _set_iq_impairment_iq_ratio(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("dm:iqadjustment:gain %e" % math.copysign(10*math.log10(1+(abs(value)/100))), value)
        self._iq_impairment_iq_ratio = value
        self._set_cache_valid()

    def _get_iq_impairment_iq_skew(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._iq_impairment_q_offset = float(self._ask("dm:iqadjustment:qskew?"))
            self._set_cache_valid()
        return self._iq_impairment_iq_skew

    def _set_iq_impairment_iq_skew(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("dm:iqadjustment:qskew %e" % value)
        self._iq_impairment_iq_skew = value
        self._set_cache_valid()

    def _get_digital_modulation_arb_selected_waveform(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._digital_modulation_arb_selected_waveform = self._ask("radio:arb:waveform?").lower().strip('"')[5:]
        return self._digital_modulation_arb_selected_waveform

    def _set_digital_modulation_arb_selected_waveform(self, value):
        value = str(value).lower()
        if not self._driver_operation_simulate:
            self._write("radio:arb:waveform \"ARBI:%s\"" % value)
        self._digital_modulation_arb_selected_waveform = value

    def _get_digital_modulation_arb_clock_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._digital_modulation_arb_clock_frequency = float(self._ask("radio:arb:clock:srate?"))
            self._set_cache_valid()
        return self._digital_modulation_arb_clock_frequency

    def _set_digital_modulation_arb_clock_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("radio:arb:clock:srate %e" % value)
        self._digital_modulation_arb_clock_frequency = value
        self._set_cache_valid()

    def _get_digital_modulation_arb_filter_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._digital_modulation_arb_filter_frequency = float(self._ask("radio:arb:clock:rfilter?"))
            self._set_cache_valid()
        return self._digital_modulation_arb_filter_frequency

    def _set_digital_modulation_arb_filter_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("radio:arb:clock:rfilter %e" % value)
        self._digital_modulation_arb_filter_frequency = value
        self._set_cache_valid()

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

    def _digital_modulation_arb_write_waveform(self, name, idata, qdata, more_data_pending=False):
        yi = None
        yq = None

        if type(idata) == list and type(idata[0]) == float:
            # list
            yi = np.array(idata)
        elif type(idata) == np.ndarray and len(idata.shape) == 1:
            # 1D array
            yi = idata
        elif type(idata) == np.ndarray and len(idata.shape) == 2 and idata.shape[0] == 1:
            # 2D array, hieght 1
            yi = idata[0]
        elif type(idata) == np.ndarray and len(idata.shape) == 2 and idata.shape[1] == 1:
            # 2D array, width 1
            yi = idata[:,0]
        else:
            xi, yi = ivi.get_sig(idata)

        if type(qdata) == list and type(qdata[0]) == float:
            # list
            yq = np.array(qdata)
        elif type(qdata) == np.ndarray and len(qdata.shape) == 1:
            # 1D array
            yq = qdata
        elif type(qdata) == np.ndarray and len(qdata.shape) == 2 and qdata.shape[0] == 1:
            # 2D array, hieght 1
            yq = qdata[0]
        elif type(qdata) == np.ndarray and len(qdata.shape) == 2 and qdata.shape[1] == 1:
            # 2D array, width 1
            yq = qdata[:,0]
        else:
            xq, yq = ivi.get_sig(qdata)

        if more_data_pending:
            # TODO: implement this flag
            raise ivi.ValueNotSupportedException()

        if len(yi) != len(yq):
            raise ivi.ValueNotSupportedException()
        if len(yi) % self._digital_modulation_arb_waveform_quantum != 0:
            raise ivi.ValueNotSupportedException()

        # clip on [-1,1] and rescale to [0,1]
        yic = (yi.clip(-1, 1)+1)/2
        yqc = (yq.clip(-1, 1)+1)/2

        # scale to 14 bits
        yib = np.rint(yic * ((1 << 14)-1)).astype(int) & 0x00003fff
        yqb = np.rint(yqc * ((1 << 14)-1)).astype(int) & 0x00003fff

        raw_i_data = yib.astype('>i2').tobytes()
        raw_q_data = yqb.astype('>i2').tobytes()

        self._write_ieee_block(raw_i_data, 'mmemory:data "ARBI:%s", ' % name)
        self._write_ieee_block(raw_q_data, 'mmemory:data "ARBQ:%s", ' % name)

    def _digital_modulation_arb_clear_all_waveforms(self):
        pass

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

