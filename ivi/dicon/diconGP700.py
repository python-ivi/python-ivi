"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014 Alex Forencich

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
import time

class diconGP700(ivi.Driver):
    "DiCon Fiberoptics GP700 Programmable Fiberoptic Instrument"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'GP700')
        
        super(diconGP700, self).__init__(*args, **kwargs)
        
        self._identity_description = "DiCon Fiberoptics GP700 Programmable Fiberoptic Instrument"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "DiCon Fiberoptics Inc"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 0
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['GP700']
        
        self._memory_size = 9
        
        self._config = ""
        
        self._attenuator_count = 0
        self._attenuator_name = list()
        self._attenuator_level = list()
        self._attenuator_level_max = list()
        
        self._filter_count = 0
        self._filter_name = list()
        self._filter_wavelength = list()
        self._filter_wavelength_max = list()
        self._filter_wavelength_min = list()
        
        self._matrix_input_count = 0
        self._matrix_input_name = list()
        self._matrix_output_count = 0
        self._matrix_input_output = list()
        
        self._switch_count = 0
        self._switch_name = list()
        self._switch_output = list()
        self._switch_input = list()
        self._switch_output_count = list()
        self._switch_input_count = list()
        
        ivi.add_property(self, 'attenuators[].level',
                        self._get_attenuator_level,
                        self._set_attenuator_level,
                        None,
                        ivi.Doc("""
                        Specifies the level of the attenuator module.  The units are dB.  
                        """))
        ivi.add_property(self, 'attenuators[].level_max',
                        self._get_attenuator_level_max,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the maximum attenuation level supported.  The units are dB. 
                        """))
        ivi.add_property(self, 'attenuators[].name',
                        self._get_attenuator_name,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the name of the attenuator module.
                        """))
        ivi.add_property(self, 'filters[].wavelength',
                        self._get_filter_wavelength,
                        self._set_filter_wavelength,
                        None,
                        ivi.Doc("""
                        Specifies the center wavelength of the filter module.  The units are nm.
                        """))
        ivi.add_property(self, 'filters[].wavelength_max',
                        self._get_filter_wavelength_max,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the maximum center wavelength of the filter.  The units are nm.
                        """))
        ivi.add_property(self, 'filters[].wavelength_min',
                        self._get_filter_wavelength_min,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the minimum center wavelength of the filter.  The units are nm.
                        """))
        ivi.add_property(self, 'filters[].name',
                        self._get_filter_name,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the name of the filter module.
                        """))
        ivi.add_property(self, 'switches[].output',
                        self._get_switch_output,
                        self._set_switch_output,
                        None,
                        ivi.Doc("""
                        Specify switch output connection.
                        """))
        ivi.add_property(self, 'switches[].output_count',
                        self._get_switch_output_count,
                        None,
                        None,
                        ivi.Doc("""
                        Query number of outputs supported by switch.
                        """))
        ivi.add_property(self, 'switches[].input',
                        self._get_switch_input,
                        self._set_switch_input,
                        None,
                        ivi.Doc("""
                        Specify switch input connection.
                        """))
        ivi.add_property(self, 'switches[].input_count',
                        self._get_switch_input_count,
                        None,
                        None,
                        ivi.Doc("""
                        Query number of inputs supported by switch.
                        """))
        ivi.add_method(self, 'switches[].get',
                        self._switch_get,
                        ivi.Doc("""
                        Get current switch input and output configuration.
                        """))
        ivi.add_method(self, 'switches[].set',
                        self._switch_set,
                        ivi.Doc("""
                        Set switch input and output configuration.
                        """))
        ivi.add_property(self, 'switches[].name',
                        self._get_switch_name,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the name of the switch module.
                        """))
        
        ivi.add_method(self, 'memory.save',
                        self._memory_save,
                        ivi.Doc("""
                        Save device configuration to the specified memory slot.
                        """))
        ivi.add_method(self, 'memory.recall',
                        self._memory_recall,
                        ivi.Doc("""
                        Recall device configuration from the specified memory slot.
                        """))
        
        if self._initialized_from_constructor:
            self._init_channels()
        
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(diconGP700, self).initialize(resource, id_query, reset, **keywargs)
        
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
        
        if not self._initialized_from_constructor:
            self._init_channels()
    
    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = lst[0].strip()
            self._identity_instrument_model = lst[1].strip()
            self._identity_instrument_firmware_revision = lst[3].strip()
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
            error_message = self._ask("err?").strip('"')
            error_code = 1
            if error_message == '0':
                error_code = 0
        return (error_code, error_message)
    
    def _utility_lock_object(self):
        pass
    
    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("*RST")
            time.sleep(0.1)
            self._clear()
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
        try:
            super(diconGP700, self)._init_channels()
        except AttributeError:
            pass
        
        config = self._get_config()
        
        self._attenuator_count = 0
        self._attenuator_name = list()
        self._attenuator_level = list()
        self._attenuator_level_max = list()
        
        self._filter_count = 0
        self._filter_name = list()
        self._filter_wavelength = list()
        self._filter_wavelength_max = list()
        self._filter_wavelength_min = list()
        
        self._matrix_input_count = 0
        self._matrix_input_name = list()
        self._matrix_output_count = 0
        self._matrix_input_output = list()
        
        self._switch_count = 0
        self._switch_name = list()
        self._switch_output = list()
        self._switch_input = list()
        self._switch_output_count = list()
        self._switch_input_count = list()
        
        lst = config.split(",")
        lst = [x.strip() for x in lst]
        lst.sort()
        
        for itm in lst:
            v = itm.split(" ")
            
            if len(itm) == 0:
                continue
            
            if v[0] == 'MATRIX':
                self._matrix_input_count = int(v[1][5:])
                self._matrix_output_count = int(v[2][6:])
            elif itm[0] == 'A':
                if v[0] not in self._attenuator_name:
                    self._attenuator_count += 1
                    self._attenuator_name.append(v[0])
                    self._attenuator_level.append(0.0)
                    self._attenuator_level_max.append(0.0)
                
                i = ivi.get_index(self._attenuator_name, v[0])
                
                self._attenuator_level[i] = 0.0
                self._attenuator_level_max[i] = float(v[1])
            elif itm[0] == 'F':
                if v[0] not in self._filter_name:
                    self._filter_count += 1
                    self._filter_name.append(v[0])
                    self._filter_wavelength.append(0.0)
                    self._filter_wavelength_min.append(0.0)
                    self._filter_wavelength_max.append(0.0)
                
                i = ivi.get_index(self._filter_name, v[0])
                
                self._filter_wavelength[i] = 0.0
                self._filter_wavelength_min[i] = float(v[1][3:])
                self._filter_wavelength_max[i] = float(v[2][3:])
            elif itm[0] == 'M':
                if v[0] not in self._switch_name:
                    self._switch_count += 1
                    self._switch_name.append(v[0])
                    self._switch_input.append(0)
                    self._switch_output.append(0)
                    self._switch_input_count.append(0)
                    self._switch_output_count.append(0)
                
                i = ivi.get_index(self._switch_name, v[0])
                
                self._switch_input[i] = 1
                self._switch_output[i] = 0
                self._switch_input_count[i] = int(v[2][1:])
                self._switch_output_count[i] = int(v[1][1:])
            elif itm[0] == 'P':
                if v[0] not in self._switch_name:
                    self._switch_count += 1
                    self._switch_name.append(v[0])
                    self._switch_input.append(0)
                    self._switch_output.append(0)
                    self._switch_input_count.append(0)
                    self._switch_output_count.append(0)
                
                i = ivi.get_index(self._switch_name, v[0])
                
                self._switch_input[i] = 1
                self._switch_output[i] = 0
                self._switch_input_count[i] = 1
                self._switch_output_count[i] = int(v[1][7:])
            elif itm[0] == 'S':
                cnt = int(v[0][1:])
                
                for i in range(cnt):
                    n = 'S%02d' % (i+1)
                    
                    if n not in self._switch_name:
                        self._switch_count += 1
                        self._switch_name.append(n)
                        self._switch_input.append(0)
                        self._switch_output.append(0)
                        self._switch_input_count.append(0)
                        self._switch_output_count.append(0)
                    
                    i = ivi.get_index(self._switch_name, n)
                    
                    self._switch_input[i] = 1
                    self._switch_output[i] = 1
                    self._switch_input_count[i] = 1
                    self._switch_output_count[i] = 2
        
        self.attenuators._set_list(self._attenuator_name)
        self.filters._set_list(self._filter_name)
        self.switches._set_list(self._switch_name)
    
    def _get_config(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._config = self._ask("system:config?")
            self._set_cache_valid()
        return self._config
    
    def _get_attenuator_level(self, index):
        index = ivi.get_index(self._attenuator_name, index)
        name = self._attenuator_name[index]
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("%s?" % (name))
            self._attenuator_level = float(resp)
            self._set_cache_valid()
        return self._attenuator_level[index]
    
    def _set_attenuator_level(self, index, value):
        index = ivi.get_index(self._attenuator_name, index)
        name = self._attenuator_name[index]
        value = float(value)
        if value < 0 or value > self._attenuator_level_max[index]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("%s %f" % (name, value))
        self._attenuator_level[index] = value
        self._set_cache_valid()
    
    def _get_attenuator_level_max(self, index):
        index = ivi.get_index(self._attenuator_name, index)
        return self._attenuator_level_max[index]
    
    def _get_attenuator_name(self, index):
        index = ivi.get_index(self._attenuator_name, index)
        return self._attenuator_name[index]
    
    def _get_filter_wavelength(self, index):
        index = ivi.get_index(self._filter_name, index)
        name = self._filter_name[index]
        if not self._driver_operation_simulate and not self._get_cache_valid():
            resp = self._ask("%s?" % (name))
            self._filter_wavelength = float(resp)
            self._set_cache_valid()
        return self._filter_wavelength[index]
    
    def _set_filter_wavelength(self, index, value):
        index = ivi.get_index(self._filter_name, index)
        name = self._filter_name[index]
        value = float(value)
        if value < self._filter_wavelength_min[index] or value > self._filter_wavelength_max[index]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("%s %f" % (name, value))
        self._filter_wavelength[index] = value
        self._set_cache_valid()
    
    def _get_filter_wavelength_max(self, index):
        index = ivi.get_index(self._filter_name, index)
        return self._filter_wavelength[index]
    
    def _get_filter_wavelength_min(self, index):
        index = ivi.get_index(self._filter_name, index)
        return self._filter_wavelength[index]
    
    def _get_filter_name(self, index):
        index = ivi.get_index(self._filter_name, index)
        return self._filter_name[index]
    
    def _get_switch_output(self, index):
        return self._switch_get(index)[0]
    
    def _set_switch_output(self, index, value):
        self._switch_set(index, value)
    
    def _get_switch_output_count(self, index):
        index = ivi.get_index(self._switch_name, index)
        return self._switch_output_count[index]
    
    def _get_switch_input(self, index):
        return self._switch_get(index)[1]
    
    def _set_switch_input(self, index, value):
        index = ivi.get_index(self._switch_name, index)
        self._switch_set(index, self._switch_output[index], value)
    
    def _get_switch_input_count(self, index):
        index = ivi.get_index(self._switch_name, index)
        return self._switch_input_count[index]
    
    def _switch_get(self, index):
        index = ivi.get_index(self._switch_name, index)
        name = self._switch_name[index]
        
        if name[0] == 'M':
            if not self._driver_operation_simulate:
                if not self._get_cache_valid('switch_output', index) or not self._get_cache_valid('switch_input', index):
                #if True:
                    resp = self._ask("%s?" % name)
                    lst = resp.split(',')
                    self._switch_output[index] = int(lst[0].strip())
                    self._switch_input[index] = int(lst[1].strip())
                    self._set_cache_valid(True, 'switch_output', index)
                    self._set_cache_valid(True, 'switch_input', index)
            return (self._switch_output[index], self._switch_input[index])
        elif name[0] == 'P' or name[0] == 'S':
            if not self._driver_operation_simulate:
                if not self._get_cache_valid('switch_output', index):
                #if True:
                    resp = self._ask("%s?" % name)
                    self._switch_output[index] = int(resp.strip())
                    self._switch_input[index] = 1
                    self._set_cache_valid(True, 'switch_output', index)
                    self._set_cache_valid(True, 'switch_input', index)
            return (self._switch_output[index], self._switch_input[index])
    
    def _switch_set(self, index, output, input=None):
        index = ivi.get_index(self._switch_name, index)
        name = self._switch_name[index]
        
        output = int(output)
        if input is not None:
            input = int(input)
        
        if name[0] == 'M':
            if output < 0 or output > self._switch_output_count[index]:
                raise ivi.OutOfRangeException()
            if input is not None and (input < 1 or input > self._switch_input_count[index]):
                raise ivi.OutOfRangeException()
            if not self._driver_operation_simulate:
                if input is None:
                    self._write("%s %d" % (name, output))
                else:
                    self._write("%s %d, %d" % (name, output, input))
            else:
                self._switch_output[index] = output
                self._set_cache_valid(True, 'switch_output', index)
                if input is not None:
                    self._switch_input[index] = input
                    self._set_cache_valid(True, 'switch_input', index)
        elif name[0] == 'P' or name[0] == 'S':
            if output < 1 or output > self._switch_output_count[index]:
                raise ivi.OutOfRangeException()
            if input is not None and input != 1:
                raise ivi.OutOfRangeException()
            if not self._driver_operation_simulate:
                self._write("%s %d" % (name, output))
            else:
                self._switch_output[index] = output
                self._switch_input[index] = 1
                self._set_cache_valid(True, 'switch_output', index)
                self._set_cache_valid(True, 'switch_input', index)
    
    def _get_switch_name(self, index):
        index = ivi.get_index(self._switch_name, index)
        return self._switch_name[index]
    
    def _memory_save(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*sav %d" % index)
    
    def _memory_recall(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*rcl %d" % index)
    
    
