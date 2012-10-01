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
from .. import scope

MeasurementFunction = set(['rise_time', 'fall_time', 'frequency', 'period',
        'voltage_rms', 'voltage_peak_to_peak', 'voltage_max', 'voltage_min',
        'voltage_high', 'voltage_low', 'voltage_average', 'width_negative',
        'width_positive', 'duty_cycle_positive', 'amplitude','voltage_cycle_rms',
        'voltage_cycle_average', 'overshoot', 'preshoot'])
MeasurementFunctionMapping = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'voltage_rms': 'vrms display',
        'voltage_peak_to_peak': 'vpp',
        'voltage_max': 'vmax',
        'voltage_min': 'vmin',
        'voltage_high': 'vtop',
        'voltage_low': 'vbase',
        'voltage_average': 'vaverage display',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle',
        'amplitude': 'vamplitude',
        'voltage_cycle_rms': 'vrms cycle',
        'voltage_cycle_average': 'vaverage cycle',
        'overshoot': 'overshoot',
        'preshoot': 'preshoot'}
MeasurementFunctionMappingDigital = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle'}

class agilent7000A(ivi.Driver, scope.Base, scope.WaveformMeasurement,
                scope.MinMaxWaveform, scope.AutoSetup):
    "Agilent Infiniivision 7000A series IVI oscilloscope driver"
    
    def __init__(self):
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_label = list()
        self._channel_probe_skew = list()
        
        super(agilent7000A, self).__init__()
        
        self._instrument_id = 'AGILENT TECHNOLOGIES'
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = 20
        self._bandwidth = 1e9
        
        self._identity_description = "Agilent Infiniivision 7000A series IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['DSO7012A','DSO7014A','DSO7032A',
                'DSO7034A','DSO7052A','DSO7054A','DSO7104A','MSO7012A','MSO7014A','MSO7032A',
                'MSO7034A','MSO7052A','MSO7054A','MSO7104A'])
        
        self.channels._add_property('label',
                        self._get_channel_label,
                        self._set_channel_label)
        self.channels._add_property('probe_skew',
                        self._get_channel_probe_skew,
                        self._set_channel_probe_skew)
        
        self._init_channels()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        
        super(agilent7000A, self).initialize(resource, id_query, reset, **keywargs)
        
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
            error_code, error_message = self._ask(":system:error?").split(',')
            error_code = int(error_code)
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
            code = int(self._ask("*TST?"))
            if code != 0:
                message = "Self test failed"
        return (code, message)
    
    def _utility_unlock_object(self):
        pass
    
    def _init_channels(self):
        super(agilent7000A, self)._init_channels()
        
        self._channel_name = list()
        self._channel_label = list()
        self._channel_probe_skew = list()
        
        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_label.append("%d" % (i+1))
            self._analog_channel_name.append("channel%d" % (i+1))
            self._channel_probe_skew.append(0)
        
        # digital channels
        self._digital_channel_name = list()
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("digital%d" % i)
                self._channel_label.append("D%d" % i)
                self._digital_channel_name.append("digital%d" % i)
            
            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_impedance[i] = 100000
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'dc'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1
        
        self.channels._set_list(self._channel_name)
    
    def _get_acquisition_start_time(self):
        pos = 0
        if not self._driver_operation_simulate and not self._get_cache_valid():
            pos = float(self._ask(":timebase:position?"))
            self._set_cache_valid()
        self._acquisition_start_time = pos - self._get_acquisition_time_per_record() * 5 / 10
        return self._acquisition_start_time
    
    def _set_acquisition_start_time(self, value):
        value = float(value)
        value = value + self._get_acquisition_time_per_record() * 5 / 10
        if not self._driver_operation_simulate:
            self._write(":timebase:position %e" % value)
        self._acquisition_start_time = value
        self._set_cache_valid()
    
    def _get_acquisition_type(self):
        return self._acquisition_type
    
    def _set_acquisition_type(self, value):
        if value not in scope.AcquisitionType:
            raise ivi.ValueNotSupportedException()
        self._acquisition_type = value
    
    def _get_acquisition_number_of_points_minimum(self):
        return self._acquisition_number_of_points_minimum
    
    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        self._acquisition_number_of_points_minimum = value
    
    def _get_acquisition_record_length(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_record_length = int(self._ask(":waveform:points?"))
            self._set_cache_valid()
        return self._acquisition_record_length
    
    def _get_acquisition_time_per_record(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_time_per_record = float(self._ask(":timebase:range?"))
            self._set_cache_valid()
        return self._acquisition_time_per_record
    
    def _set_acquisition_time_per_record(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":timebase:range %e" % value)
        self._acquisition_time_per_record = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'acquisition_start_time')
    
    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask(":%s:label?" % self._channel_name[index]).strip('"')
            self._set_cache_valid(index=index)
        return self._channel_label[index]
    
    def _set_channel_label(self, index, value):
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write(":%s:label \"%s\"" % (self._channel_name[index], value))
        self._channel_label[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_enabled[index] = bool(int(self._ask(":%s:display?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_enabled[index]
    
    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            if value:
                self._write(":%s:display on" % self._channel_name[index])
            else:
                self._write(":%s:display off" % self._channel_name[index])
        self._channel_enabled[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            val = float(self._ask(":%s:impedance?" % self._channel_name[index]))
            if val == 'ONEM':
                self._channel_input_impedance[index] = 1000000
            elif val == 'FIFT':
                self._channel_input_impedance[index] = 50
            self._set_cache_valid(index=index)
        return self._channel_input_impedance[index]
    
    def _set_channel_input_impedance(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if value != 50 and value != 1000000:
            raise Exception('Invalid impedance selection')
        if not self._driver_operation_simulate:
            if value == 1000000:
                self._write(":%s:impedance onemeg" % self._channel_name[index])
            elif value == 50:
                self._write(":%s:impedance fifty" % self._channel_name[index])
        self._channel_input_impedance[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_input_frequency_max(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        return self._channel_input_frequency_max[index]
    
    def _set_channel_input_frequency_max(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            if value < 25e6:
                self._write(":%s:bwlimit on" % self._channel_name[index])
            else:
                self._write(":%s:bwlimit off" % self._channel_name[index])
        self._channel_input_frequency_max[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_attenuation[index] = float(self._ask(":%s:probe?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_attenuation[index]
    
    def _set_channel_probe_attenuation(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:probe %e" % (self._channel_name[index], value))
        self._channel_probe_attenuation[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_probe_skew(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_skew[index] = float(self._ask(":%s:probe:skew?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_skew[index]
    
    def _set_channel_probe_skew(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:probe:skew %e" % (self._channel_name[index], value))
        self._channel_probe_skew[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_enabled[index] = self._ask(":%s:coupling?" % self._channel_name[index]).lower()
            self._set_cache_valid(index=index)
        return self._channel_coupling[index]
    
    def _set_channel_coupling(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in scope.VerticalCoupling:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":%s:coupling %s" % (self._channel_name[index], value))
        self._channel_coupling[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_offset[index] = float(self._ask(":%s:offset?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:offset %e" % (self._channel_name[index], value))
        self._channel_offset[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_range[index] = float(self._ask(":%s:range?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_range[index]
    
    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:range %e" % (self._channel_name[index], value))
        self._channel_range[index] = value
        self._set_cache_valid(index=index)
    
    def _get_measurement_status(self):
        return self._measurement_status
    
    def _get_trigger_coupling(self):
        return self._trigger_coupling
    
    def _set_trigger_coupling(self, value):
        if value not in scope.TriggerCoupling:
            raise ivi.ValueNotSupportedException()
        self._trigger_coupling = value
    
    def _get_trigger_holdoff(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_holdoff = float(self._ask(":trigger:holdoff?"))
            self._set_cache_valid()
        return self._trigger_holdoff
    
    def _set_trigger_holdoff(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:holdoff %e" % value)
        self._trigger_holdoff = value
        self._set_cache_valid(index=index)
    
    def _get_trigger_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_level = float(self._ask(":trigger:level?"))
            self._set_cache_valid()
        return self._trigger_level
    
    def _set_trigger_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:level %e" % value)
        self._trigger_level = value
        self._set_cache_valid(index=index)
    
    def _get_trigger_edge_slope(self):
        return self._trigger_edge_slope
    
    def _set_trigger_edge_slope(self, value):
        if value not in scope.Slope:
            raise ivi.ValueNotSupportedException()
        self._trigger_edge_slope = value
    
    def _get_trigger_source(self):
        return self._trigger_source
    
    def _set_trigger_source(self, value):
        value = str(value)
        self._trigger_source = value
    
    def _get_trigger_type(self):
        return self._trigger_type
    
    def _set_trigger_type(self, value):
        if value not in scope.TriggerType:
            raise ivi.ValueNotSupportedException()
        self._trigger_type = value
    
    def _measurement_abort(self):
        pass
    
    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        if self._driver_operation_simulate:
            return list()
        
        self._write(":waveform:byteorder msbfirst")
        self._write(":waveform:unsigned 1")
        self._write(":waveform:format word")
        self._write(":waveform:points normal")
        self._write(":waveform:source %s" % self._channel_name[index])
        
        # Read preamble
        
        pre = self._ask(":waveform:preamble?").split(',')
        
        format = int(pre[0])
        type = int(pre[1])
        points = int(pre[2])
        count = int(pre[3])
        xincrement = float(pre[4])
        xorigin = float(pre[5])
        xreference = int(pre[6])
        yincrement = float(pre[7])
        yorigin = float(pre[8])
        yreference = int(pre[9])
        
        if type == 1:
            raise scope.InvalidAcquisitionTypeException()
        
        if format != 1:
            raise UnexpectedResponseException()
        
        self._write(":waveform:data?")
        
        # Waveform data is prefixed with #lnnnnnnnn
        # where l is number of n (8) and n represent the
        # length of the data
        # ex: #800002000 prefixes 2000 data bytes
        
        ch = self._read(1)
        
        while ch != '#':
            ch = self._read(1)
        
        l = int(self._read(1))
        num = int(self._read(l))
        
        # Read waveform data
        
        raw_data = self._read_raw(num)
        
        self._read()
        
        # Split out points and convert to time and voltage pairs
        
        data = list()
        for i in range(points):
            x = ((i - xreference) * xincrement) + xorigin
            
            yval = raw_data[i*2] * 256 + raw_data[i*2+1]
            y = ((yval - yreference) * yincrement) + yorigin
            
            data.append((x, y))
        
        return data
    
    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)
    
    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(":digitize")
    
    def _get_reference_level_high(self):
        return self._reference_level_high
    
    def _set_reference_level_high(self, value):
        value = float(value)
        if value < 5: value = 5
        if value > 95: value = 95
        self._reference_level_high = value
        if not self._driver_operation_simulate:
            self._write(":measure:define thresholds, %e, %e, %e" %
                        (self._reference_level_high,
                        self._reference_level_middle,
                        self._reference_level_low))
    
    def _get_reference_level_low(self):
        return self._reference_level_low
    
    def _set_reference_level_low(self, value):
        value = float(value)
        if value < 5: value = 5
        if value > 95: value = 95
        self._reference_level_low = value
        if not self._driver_operation_simulate:
            self._write(":measure:define thresholds, %e, %e, %e" %
                        (self._reference_level_high,
                        self._reference_level_middle,
                        self._reference_level_low))
    
    def _get_reference_level_middle(self):
        return self._reference_level_middle
    
    def _set_reference_level_middle(self, value):
        value = float(value)
        if value < 5: value = 5
        if value > 95: value = 95
        self._reference_level_middle = value
        if not self._driver_operation_simulate:
            self._write(":measure:define thresholds, %e, %e, %e" %
                        (self._reference_level_high,
                        self._reference_level_middle,
                        self._reference_level_low))
    
    def _measurement_fetch_waveform_measurement(self, index, measurement_function):
        index = ivi.get_index(self._channel_name, index)
        if index < self._analog_channel_count:
            if measurement_function not in MeasurementFunctionMapping:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMapping[measurement_function]
        else:
            if measurement_function not in MeasurementFunctionMappingDigital:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMappingDigital[measurement_function]
        if not self._driver_operation_simulate:
            l = func.split(' ')
            l[0] = l[0] + '?'
            if len(l) > 1:
                l[-1] = l[-1] + ','
            func = ' '.join(l)
            return float(self._ask(":measure:%s %s" % (func, self._channel_name[index])))
        return 0
    
    def _measurement_read_waveform_measurement(self, index, measurement_function, maximum_time):
        return self._measurement_fetch_waveform_measurement(index, measurement_function)
    
    def _get_acquisition_number_of_envelopes(self):
        return self._acquisition_number_of_envelopes
    
    def _set_acquisition_number_of_envelopes(self, value):
        self._acquisition_number_of_envelopes = value
    
    def _measurement_fetch_waveform_min_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        data = list()
        return data
    
    def _measurement_read_waveform_min_max(self, index, maximum_time):
        return _measurement_fetch_waveform_min_max(index)
    
    def _measurement_auto_setup(self):
        if not self._driver_operation_simulate:
            self._write(":autoscale")
    
    
    


