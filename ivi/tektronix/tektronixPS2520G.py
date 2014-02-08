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

TrackingType = set(['parallel', 'series'])

class tektronixPS2520G(scpi.dcpwr.Base, scpi.dcpwr.Measurement):
    "Tektronix PS2520G DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'PS2520G')
        
        super(tektronixPS2520G, self).__init__(*args, **kwargs)
        
        self._output_count = 3
        
        self._output_spec = [
            {
                'range': {
                    'P36V': (37.0, 1.5)
                },
                'ovp_max': 38.5,
                'voltage_max': 37.0,
                'current_max': 1.5
            },
            {
                'range': {
                    'P36V': (37.0, 1.5)
                },
                'ovp_max': 38.5,
                'voltage_max': 37.0,
                'current_max': 1.5
            },
            {
                'range': {
                    'P6V': (6.5, 3.0)
                },
                'ovp_max': 7.0,
                'voltage_max': 6.5,
                'current_max': 3.0
            }
        ]
        
        self._couple_tracking_enabled = False
        self._couple_tracking_type = 'series'
        
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
        
        ivi.add_property(self, 'couple.tracking.enabled',
                        self._get_couple_tracking_enabled,
                        self._set_couple_tracking_enabled)
        ivi.add_property(self, 'couple.tracking.type',
                        self._get_couple_tracking_type,
                        self._set_couple_tracking_type)
        
        self._init_outputs()
    
    def _get_tracking(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":instrument:couple:tracking?").lower()
            if value == 'none':
                self._couple_tracking_enabled = False
            else:
                self._couple_tracking_enabled = True
                self._couple_tracking_type = value
            self._set_cache_valid()
    
    def _set_tracking(self):
        if not self._driver_operation_simulate:
            value = self._couple_tracking_type
            if not self._couple_tracking_enabled:
                value = 'none'
            self._write(":instrument:couple:tracking %s" % value)
        self._set_cache_valid()
    
    def _get_couple_tracking_enabled(self):
        self._get_tracking()
        return self._couple_tracking_enabled
    
    def _set_couple_tracking_enabled(self, value):
        value = bool(value)
        self._couple_tracking_enabled = value
        self._set_tracking()
    
    def _get_couple_tracking_type(self):
        self._get_tracking()
        return self._couple_tracking_type
    
    def _set_couple_tracking_type(self, value):
        value = str(value)
        if value not in TrackingType:
            raise ivi.ValueNotSupportedException()
        self._couple_tracking_type = value
        self._set_tracking()
    
    

