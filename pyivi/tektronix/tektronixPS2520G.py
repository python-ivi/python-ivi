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
from .. import dcpwr

class tektronixPS2520G(ivi.Driver, dcpwr.Base, dcpwr.Measurement):
    "Tektronix PS2520G DC power supply driver"
    
    def __init__(self):
        super(tektronixPS2520G, self).__init__()
        
        self._instrument_id = 'PS2520G'
        
        self._output_count = 3
        
        self._output_range = [[(37.0, 1.5)], [(37.0, 1.5)], [(6.5, 3.0)]]
        self._output_ovp_max = [38.5, 38.5, 7.0]
        self._output_voltage_max = [37.0, 37.0, 6.5]
        self._output_current_max = [1.5, 1.5, 5.0]
        
        self._identity_description = "Tektronix PS2520G DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Tektronix"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PS2520G','PS2521G']
        
        self._init_outputs()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(tektronixPS2520G, self).initialize(resource, id_query, reset, **keywargs)
        
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
    
    
    
    def _init_outputs(self):
        super(tektronixPS2520G, self)._init_outputs()
        
        self._output_current_limit = list()
        self._output_current_limit_behavior = list()
        self._output_enabled = list()
        self._output_ovp_enabled = list()
        self._output_ovp_limit = list()
        self._output_voltage_level = list()
        for i in range(self._output_count):
            self._output_current_limit.append(0)
            self._output_current_limit_behavior.append('trip')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(0)
            self._output_voltage_level.append(0)
    
    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._write(":instrument:nselect %d" % (index+1))
            self._output_current_limit[index] = float(self._ask(":source:current:level?"))
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]
    
    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_current_max[index]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":instrument:nselect %d" % (index+1))
            self._write(":source:current:level %e" % value)
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_current_limit_behavior(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._write(":instrument:nselect %d" % (index+1))
            value = bool(int(self._ask(":source:current:protection:state?")))
            if value:
                self._output_current_limit_behavior[index] = 'trip'
            else:
                self._output_current_limit_behavior[index] = 'regulate'
            self._set_cache_valid(index=index)
        return self._output_current_limit_behavior[index]
    
    def _set_output_current_limit_behavior(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in dcpwr.CurrentLimitBehavior:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":instrument:nselect %d" % (index+1))
            self._write(":source:current:protection:state %d" % int(value == 'trip'))
        self._output_current_limit_behavior[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
    
    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._write(":instrument:nselect %d" % (index+1))
            self._output_enabled[index] = bool(int(self._ask(":output:state?")))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]
    
    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":instrument:nselect %d" % (index+1))
            self._write(":output:state %d" % int(value))
        self._output_enabled[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
    
    def _get_output_ovp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        # Cannot disable OVP
        self._output_ovp_enabled[index] = True
        return self._output_ovp_enabled[index]
    
    def _set_output_ovp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        # Cannot disable OVP, so set limit to max instead
        if not value and not self._driver_operation_simulate:
            self._write(":instrument:nselect %d" % (index+1))
            self._write(":source:voltage:protection:level max")
            self._set_cache_valid(valid=False,tag='output_ovp_limit',index=index)
        value = True
        self._output_ovp_enabled[index] = value
    
    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._write(":instrument:nselect %d" % (index+1))
            self._output_ovp_limit[index] = float(self._ask(":source:voltage:protection:level?"))
            self._set_cache_valid(index=index)
        return self._output_ovp_limit[index]
    
    def _set_output_ovp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_ovp_max[index]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":instrument:nselect %d" % (index+1))
            self._write(":source:voltage:protection:level %e" % value)
        self._output_ovp_limit[index] = value
        self._set_cache_valid(index=index)
    
    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._write(":instrument:nselect %d" % (index+1))
            self._output_voltage_level[index] = float(self._ask(":source:voltage:level?"))
            self._set_cache_valid(index=index)
        return self._output_voltage_level[index]
    
    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_voltage_max[index]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":instrument:nselect %d" % (index+1))
            self._write(":source:voltage:level %e" % value)
        self._output_voltage_level[index] = value
        self._set_cache_valid(index=index)
    
    def _output_configure_range(self, index, range_type, range_val):
        index = ivi.get_index(self._output_name, index)
        if range_type not in dcpwr.RangeType:
            raise ivi.ValueNotSupportedException()
        if range_type == 'voltage':
            t = 0
        elif range_type == 'current':
            t = 1
        r = dcpwr.get_range(self._output_range[index], t, range_val)
        if r is None:
            raise ivi.OutOfRangeException()
        self._output_voltage_max[index] = r[0]
        self._output_current_max[index] = r[1]
        pass
    
    def _output_query_current_limit_max(self, index, voltage_level):
        index = ivi.get_index(self._output_name, index)
        if voltage_level < 0 or voltage_level > self._output_voltage_max[index]:
            raise ivi.OutOfRangeException()
        return self._output_current_max[index]
    
    def _output_query_voltage_level_max(self, index, current_limit):
        index = ivi.get_index(self._output_name, index)
        if current_limit < 0 or current_limit > self._output_current_max[index]:
            raise ivi.OutOfRangeException()
        return self._output_voltage_max[index]
    
    def _output_query_output_state(self, index, state):
        index = ivi.get_index(self._output_name, index)
        if state not in dcpwr.OutputState:
            raise ivi.ValueNotSupportedException()
        status = 0
        if not self._driver_operation_simulate:
            status = int(self._ask(":stat:ques:inst:isum%d:cond?" % (index+1)))
        if state == 'constant_voltage':
            return status & (1 << 1) != 0
        elif state == 'constant_current':
            return status & (1 << 0) != 0
        elif state == 'over_voltage':
            return status & (1 << 9) != 0
        elif state == 'over_current':
            return status & (1 << 10) != 0
        elif state == 'unregulated':
            return status & (3 << 0) != 0
        return False
    
    def _output_reset_output_protection(self, index):
        if not self._driver_operation_simulate:
            self._write(":instrument:nselect %d" % (index+1))
            self._write(":output:protection:clear")
    
    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in dcpwr.MeasurementType:
            raise ivi.ValueNotSupportedException()
        if type == 'voltage':
            if not self._driver_operation_simulate:
                self._write(":instrument:nselect %d" % (index+1))
                return float(self._ask(":measure:voltage?"))
        elif type == 'current':
            if not self._driver_operation_simulate:
                self._write(":instrument:nselect %d" % (index+1))
                return float(self._ask(":measure:current?"))
        return 0
    
    

