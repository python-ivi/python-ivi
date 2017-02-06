"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014-2017 Alex Forencich

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

class OCP(ivi.IviContainer):
    "Extension IVI methods for power supplies supporting overcurrent protection"
    
    def __init__(self, *args, **kwargs):
        super(OCP, self).__init__(*args, **kwargs)
        
        cls = 'IviDCPwr'
        grp = 'OCP'
        ivi.add_group_capability(self, cls+grp)
        
        self._output_ocp_enabled = list()
        self._output_ocp_limit = list()
        
        self._output_spec = [
            {
                'range': {
                    'P8V': (9.0, 20.0),
                    'P20V': (21.0, 10.0)
                },
                'ovp_max': 22.0,
                'ocp_max': 22.0,
                'voltage_max': 9.0,
                'current_max': 20.0
            }
        ]
        
        self._add_property('outputs[].ocp_enabled',
                        self._get_output_ocp_enabled,
                        self._set_output_ocp_enabled,
                        None,
                        ivi.Doc("""
                        Specifies whether the power supply provides over-current protection. If
                        this attribute is set to True, the power supply disables the output when
                        the output current is greater than or equal to the value of the OCP
                        Limit attribute.
                        """))
        self._add_property('outputs[].ocp_limit',
                        self._get_output_ocp_limit,
                        self._set_output_ocp_limit,
                        None,
                        ivi.Doc("""
                        Specifies the current the power supply allows. The units are Amps.
                        
                        If the OCP Enabled attribute is set to True, the power supply disables the
                        output when the output current is greater than or equal to the value of
                        this attribute.
                        
                        If the OCP Enabled is set to False, this attribute does not affect the
                        behavior of the instrument.
                        """))
        
        self._init_outputs()
   
    def _init_outputs(self):
        try:
            super(OCP, self)._init_outputs()
        except AttributeError:
            pass
        
        self._output_ocp_enabled = list()
        self._output_ocp_limit = list()
        for i in range(self._output_count):
            self._output_ocp_enabled.append(True)
            self._output_ocp_limit.append(0)
    
    def _get_output_ocp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_ocp_enabled[index]
    
    def _set_output_ocp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        self._output_ocp_enabled[index] = value
    
    def _get_output_ocp_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_ocp_limit[index]
    
    def _set_output_ocp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['ocp_max']:
            raise ivi.OutOfRangeException()
        self._output_ocp_limit[index] = value
    
    def _output_reset_output_protection(self, index):
        pass
    
    

