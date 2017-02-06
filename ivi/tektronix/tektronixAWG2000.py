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

import time
import struct
from numpy import *

from .. import ivi
from .. import fgen

StandardWaveformMapping = {
        'sine': 'sin',
        'square': 'squ',
        'triangle': 'tri',
        'ramp_up': 'ramp',
        #'ramp_down',
        #'dc'
        }

class tektronixAWG2000(ivi.Driver, fgen.Base, fgen.StdFunc, fgen.ArbWfm,
                fgen.ArbSeq, fgen.SoftwareTrigger, fgen.Burst,
                fgen.ArbChannelWfm):
    "Tektronix AWG2000 series arbitrary waveform generator driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(tektronixAWG2000, self).__init__(*args, **kwargs)
        
        self._output_count = 1
        
        self._arbitrary_sample_rate = 0
        self._arbitrary_waveform_number_waveforms_max = 0
        self._arbitrary_waveform_size_max = 256*1024
        self._arbitrary_waveform_size_min = 64
        self._arbitrary_waveform_quantum = 8
        
        self._arbitrary_sequence_number_sequences_max = 0
        self._arbitrary_sequence_loop_count_max = 0
        self._arbitrary_sequence_length_max = 0
        self._arbitrary_sequence_length_min = 0
        
        self._catalog_names = list()
        
        self._arbitrary_waveform_n = 0
        self._arbitrary_sequence_n = 0
        
        self._identity_description = "Tektronix AWG2000 series arbitrary waveform generator driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Tektronix"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 5
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['AWG2005','AWG2020','AWG2021','AWG2040','AWG2041']
        
        self._init_outputs()
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(tektronixAWG2000, self)._initialize(resource, id_query, reset, **keywargs)
        
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
            error_code, error_message = self._ask(":evmsg?").split(',')
            error_code = int(error_code.split(' ', 1)[1])
            if error_code == 1:
                self._ask("*esr?")
                error_code, error_message = self._ask(":evmsg?").split(',')
                error_code = int(error_code.split(' ', 1)[1])
            error_message = error_message.strip(' "')
        return (error_code, error_message)
    
    def _utility_lock_object(self):
        pass
    
    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("*RST")
            self.driver_operation.invalidate_all_attributes()
    
    def _utility_reset_with_defaults(self):
        self._utility_reset()
    
    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            self._write("*TST?")
            # wait for test to complete
            time.sleep(60)
            code = int(self._read())
            if code != 0:
                message = "Self test failed"
        return (code, message)
    
    def _utility_unlock_object(self):
        pass
    
    
    
    def _init_outputs(self):
        try:
            super(tektronixAWG2000, self)._init_outputs()
        except AttributeError:
            pass
        
        self._output_enabled = list()
        for i in range(self._output_count):
            self._output_enabled.append(False)
    
    
    def _load_catalog(self):
        self._catalog = list()
        self._catalog_names = list()
        if not self._driver_operation_simulate:
            raw = self._ask(":memory:catalog:all?").lower()
            raw = raw.split(' ', 1)[1]
            
            l = raw.split(',')
            l = [s.strip('"') for s in l]
            self._catalog = [l[i:i+3] for i in range(0, len(l), 3)]
            self._catalog_names = [l[0] for l in self._catalog]
    
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
            resp = self._ask(":output:ch%d:state?" % (index+1)).split(' ', 1)[1]
            self._output_enabled[index] = bool(int(resp))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]
    
    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":output:ch%d:state %d" % (index+1, value))
        self._output_enabled[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_impedance(self, index):
        index = ivi.get_index(self._output_name, index)
        self._output_impedance[index] = 50
        return self._output_impedance[index]
    
    def _set_output_impedance(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = 50
        self._output_impedance[index] = value
    
    def _get_output_mode(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":fg:state?").split(' ', 1)[1]
            if int(resp):
                self._output_mode[index] = 'function'
            else:
                self._output_mode[index] = 'arbitrary'
            self._set_cache_valid(index=index)
        return self._output_mode[index]
    
    def _set_output_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in fgen.OutputMode:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if value == 'function':
                self._write(":fg:state 1")
            elif value == 'arbitrary':
                self._write(":fg:state 0")
        self._output_mode[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
    
    def _get_output_reference_clock_source(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":clock:source?").split(' ', 1)[1]
            value = resp.lower()
            self._output_reference_clock_source[index] = value
            self._set_cache_valid(index=index)
        return self._output_reference_clock_source[index]
    
    def _set_output_reference_clock_source(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in fgen.SampleClockSource:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":clock:source %s" % value)
        self._output_reference_clock_source[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
    
    def abort_generation(self):
        pass
    
    def initiate_generation(self):
        pass
    
    def _get_output_standard_waveform_amplitude(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":fg:ch%d:amplitude?" % (index+1)).split(' ', 1)[1]
            self._output_standard_waveform_amplitude[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_amplitude[index]
    
    def _set_output_standard_waveform_amplitude(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":fg:ch%d:amplitude %e" % (index+1, value))
        self._output_standard_waveform_amplitude[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_standard_waveform_dc_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":fg:ch%d:offset?" % (index+1)).split(' ', 1)[1]
            self._output_standard_waveform_dc_offset[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_dc_offset[index]
    
    def _set_output_standard_waveform_dc_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":fg:ch%d:offset %e" % (index+1, value))
        self._output_standard_waveform_dc_offset[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_standard_waveform_duty_cycle_high(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_duty_cycle_high[index]
    
    def _set_output_standard_waveform_duty_cycle_high(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_duty_cycle_high[index] = value
    
    def _get_output_standard_waveform_start_phase(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_standard_waveform_start_phase[index]
    
    def _set_output_standard_waveform_start_phase(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        self._output_standard_waveform_start_phase[index] = value
    
    def _get_output_standard_waveform_frequency(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":fg:frequency?").split(' ', 1)[1]
            self._output_standard_waveform_frequency[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_frequency[index]
    
    def _set_output_standard_waveform_frequency(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":fg:frequency %e" % value)
        self._output_standard_waveform_frequency[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
    
    def _get_output_standard_waveform_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":fg:ch%d:shape?" % (index+1)).split(' ', 1)[1]
            value = resp.lower()
            value = [k for k,v in StandardWaveformMapping.items() if v==value][0]
            self._output_standard_waveform_waveform[index] = value
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_waveform[index]
    
    def _set_output_standard_waveform_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in StandardWaveformMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":fg:ch%d:shape %s" % (index+1, StandardWaveformMapping[value]))
        self._output_standard_waveform_waveform[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_arbitrary_gain(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":ch%d:amplitude?" % (index+1)).split(' ', 1)[1]
            self._output_arbitrary_gain[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_arbitrary_gain[index]
    
    def _set_output_arbitrary_gain(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":ch%d:amplitude %e" % (index+1, value))
        self._output_arbitrary_gain[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_arbitrary_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":ch%d:offset?" % (index+1)).split(' ', 1)[1]
            self._output_arbitrary_offset[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_arbitrary_offset[index]
    
    def _set_output_arbitrary_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":ch%d:offset %e" % (index+1, value))
        self._output_arbitrary_offset[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_arbitrary_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":ch%d:waveform?" % (index+1)).split(' ', 1)[1]
            self._output_arbitrary_waveform[index] = resp.strip('"').lower()
            self._set_cache_valid(index=index)
        return self._output_arbitrary_waveform[index]
    
    def _set_output_arbitrary_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = str(value).lower()
        # extension must be wfm
        ext = value.split('.').pop()
        if ext != 'wfm':
            raise ivi.ValueNotSupportedException()
        # waveform must exist on arb
        self._load_catalog()
        if value not in self._catalog_names:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":ch%d:waveform \"%s\"" % (index+1, value))
        self._output_arbitrary_waveform[index] = value
    
    def _get_arbitrary_sample_rate(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask(":clock:frequency?").split(' ', 1)[1]
            self._arbitrary_sample_rate = float(resp)
            self._set_cache_valid()
        return self._arbitrary_sample_rate
    
    def _set_arbitrary_sample_rate(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":clock:frequency %e" % value)
        self._arbitrary_sample_rate = value
        self._set_cache_valid()
    
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
    
    def _arbitrary_waveform_create(self, data):
        y = None
        x = None
        if type(data) == list and type(data[0]) == float:
            # list
            y = array(data)
        elif type(data) == ndarray and len(data.shape) == 1:
            # 1D array
            y = data
        elif type(data) == ndarray and len(data.shape) == 2 and data.shape[0] == 1:
            # 2D array, hieght 1
            y = data[0]
        elif type(data) == ndarray and len(data.shape) == 2 and data.shape[1] == 1:
            # 2D array, width 1
            y = data[:,0]
        else:
            x, y = ivi.get_sig(data)
        
        if x is None:
            x = arange(0,len(y)) / 10e6
        
        if len(y) % self._arbitrary_waveform_quantum != 0:
            raise ivi.ValueNotSupportedException()
        
        xincr = ivi.rms(diff(x))
        
        # get unused handle
        self._load_catalog()
        have_handle = False
        while not have_handle:
            self._arbitrary_waveform_n += 1
            handle = "w%04d.wfm" % self._arbitrary_waveform_n
            have_handle = handle not in self._catalog_names
        self._write(":data:destination \"%s\"" % handle)
        self._write(":wfmpre:bit_nr 12")
        self._write(":wfmpre:bn_fmt rp")
        self._write(":wfmpre:byt_nr 2")
        self._write(":wfmpre:byt_or msb")
        self._write(":wfmpre:encdg bin")
        self._write(":wfmpre:pt_fmt y")
        self._write(":wfmpre:yzero 0")
        self._write(":wfmpre:ymult %e" % (2/(1<<12)))
        self._write(":wfmpre:xincr %e" % xincr)
        
        raw_data = b''
        
        for f in y:
            # clip at -1 and 1
            if f > 1.0: f = 1.0
            if f < -1.0: f = -1.0
            
            f = (f + 1) / 2
            
            # scale to 12 bits
            i = int(f * ((1 << 12) - 2) + 0.5) & 0x000fffff
            
            # add to raw data, MSB first
            raw_data = raw_data + struct.pack('>H', i)
        
        self._write_ieee_block(raw_data, ':curve ')
        
        return handle
    
    def _get_arbitrary_sequence_number_sequences_max(self):
        return self._arbitrary_sequence_number_sequences_max
    
    def _get_arbitrary_sequence_loop_count_max(self):
        return self._arbitrary_sequence_loop_count_max
    
    def _get_arbitrary_sequence_length_max(self):
        return self._arbitrary_sequence_length_max
    
    def _get_arbitrary_sequence_length_min(self):
        return self._arbitrary_sequence_length_min
    
    def _arbitrary_clear_memory(self):
        pass
    
    def _arbitrary_sequence_clear(self, handle):
        pass
    
    def _arbitrary_sequence_configure(self, index, handle, gain, offset):
        pass
    
    def _arbitrary_sequence_create(self, handle_list, loop_count_list):
        return "handle"
    
    def send_software_trigger(self):
        if not self._driver_operation_simulate:
            self._write("*TRG")
    
    def _get_output_burst_count(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_burst_count[index]
    
    def _set_output_burst_count(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = int(value)
        self._output_burst_count[index] = value
    
    def _arbitrary_waveform_create_channel_waveform(self, index, data):
        handle = self._arbitrary_waveform_create(data)
        self._set_output_arbitrary_waveform(index, handle)
        return handle
    
    

