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
from .. import dcpwr
from .. import scpi

TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'bus': 'bus'}

class agilentE3600A(scpi.dcpwr.Base, scpi.dcpwr.Trigger, scpi.dcpwr.SoftwareTrigger,
                scpi.dcpwr.Measurement,
                scpi.common.Memory):
    "Agilent E3600A series IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'E3600A')
        
        # don't do standard SCPI init routine
        self._do_scpi_init = False
        
        super(agilentE3600A, self).__init__(*args, **kwargs)
        
        self._output_count = 3
        
        self._output_spec = [
            {
                'range': {
                    'P6V': (7.0, 5.0)
                },
                'ovp_max': 27.0,
                'voltage_max': 7.0,
                'current_max': 5.0
            },
            {
                'range': {
                    'P25V': (26.0, 1.0)
                },
                'ovp_max': 27.0,
                'voltage_max': 26.0,
                'current_max': 1.0
            },
            {
                'range': {
                    'N25V': (-26.0, 1.0)
                },
                'ovp_max': 27.0,
                'voltage_max': -26.0,
                'current_max': 1.0
            }
        ]
        
        self._memory_size = 3
        self._memory_offset = 1
        
        self._output_trigger_delay = list()
        
        self._couple_tracking_enabled = False
        self._couple_tracking_type = 'floating'
        self._couple_trigger = False
        
        self._identity_description = "Agilent E3600A series DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['E3631A','E3632A','E3633A','E3634A',
                        'E3640A','E3641A','E3642A','E3643A','E3644A','E3645A','E3646A',
                        'E3647A','E3648A','E3649A']
        
        ivi.add_property(self, 'outputs.trigger_delay',
                        self._get_output_trigger_delay,
                        self._set_output_trigger_delay)
        
        ivi.add_property(self, 'couple.trigger',
                        self._get_couple_trigger,
                        self._set_couple_trigger)
        ivi.add_property(self, 'couple.tracking.enabled',
                        self._get_couple_tracking_enabled,
                        self._set_couple_tracking_enabled)
        ivi.add_property(self, 'couple.tracking.type',
                        self._get_couple_tracking_type,
                        self._set_couple_tracking_type)
        
        ivi.add_method(self, 'memory.set_name',
                        self._set_memory_name)
        ivi.add_method(self, 'memory.get_name',
                        self._get_memory_name)
        
        self._init_outputs()
    
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilentE3600A, self).initialize(resource, id_query, reset, **keywargs)
        
        # configure interface
        if self._interface is not None:
            if 'dsrdtr' in self._interface.__dict__:
                self._interface.dsrdtr = True
                self._interface.update_settings()
        
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
        
    
    def _get_couple_tracking_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":output:track:state?").lower()
            self._couple_tracking_enabled = (value1 == 'on')
            self._set_cache_valid()
        return self._couple_tracking_enabled
    
    def _set_couple_tracking_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":output:track:state %s" % ('off', 'on')[value])
        self._couple_tracking_enabled = value
        self._set_cache_valid()
    
    def _get_couple_tracking_type(self):
        return self._couple_tracking_type
    
    def _set_couple_tracking_type(self, value):
        value = str(value)
        if value not in TrackingType:
            raise ivi.ValueNotSupportedException()
        self._couple_tracking_type = value
    
    def _get_couple_trigger(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":instrument:couple:trigger?").lower()
            self._couple_trigger = (value == 'on')
            self._set_cache_valid()
        return self._couple_trigger
    
    def _set_couple_trigger(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":instrument:couple:trigger %s" % ('off', 'on')[value])
        self._couple_trigger = value
        self._set_cache_valid()
    
    def _get_memory_name(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            return self._ask(":memory:state:name? %d" % (index+1)).strip(' "')
    
    def _set_memory_name(self, index, value):
        index = int(index)
        value = str(value)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":memory:state:name %d, \"%s\"" % (index+1, value))
    
    
    

