"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013-2017 Alex Forencich

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

class chromaBaseDCPwr(scpi.dcpwr.Base, scpi.dcpwr.Trigger, scpi.dcpwr.SoftwareTrigger,
                scpi.dcpwr.Measurement):
    "Chroma ATE generic IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(chromaBaseDCPwr, self).__init__(*args, **kwargs)
        
        self._output_count = 1

        self._output_spec = [
            {
                'range': {
                    'P600V': (600.0, 120.0)
                },
                'ovp_max': 660.0,
                'ocp_max': 132.0,
                'voltage_max': 600.0,
                'current_max': 120.0
            }
        ]
        
        self._memory_size = 10
        
        self._identity_description = "Chroma ATE generic IVI DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Chroma ATE"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['62006P-100-25', '62012P-80-60', '62012P-100-50', '62012P-600-8',
                                                      '62006P-30-80', '62006P-300-8', '62012P-40-120', '62024P-40-120',
                                                      '62024P-80-60', '62024P-100-50', '62024P-600-8', '62050P-100-100']



        self._init_outputs()

    def _init_outputs(self):
        try:
            super(chromaBaseDCPwr, self)._init_outputs()
        except AttributeError:
            pass

        self._output_name = list()
        self._output_current_limit = list()
        self._output_current_limit_behavior = list()
        self._output_enabled = list()
        self._output_ovp_enabled = list()
        self._output_ovp_limit = list()
        self._output_voltage_level = list()
        self._output_voltage_max = list()
        self._output_slew_rate = list()
        for i in range(self._output_count):
            self._output_name.append("output%d" % (i+1))
            self._output_current_limit.append(self._output_spec[i-1]['current_max'])
            self._output_current_limit.append(0)
            #self._output_current_limit_behavior.append('regulate')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(self._output_spec[i-1]['ovp_max'])
            self._output_voltage_level.append(0)
            self._output_voltage_max.append(self._output_spec[i-1]['voltage_max'])
            self._output_slew_rate.append(0)

        self.outputs._set_list(self._output_name)

    
    
    

