"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2013-2014 Alex Forencich

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

from .rigolDP800 import *

class rigolDP832A(rigolDP800):
    "Rigol DP832A IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'DP832A')
        
        super(rigolDP832A, self).__init__(*args, **kwargs)
        
        self._output_count = 3
        
        self._output_spec = [
            {
                'range': {
                    'P30V': (30.0, 3.0)
                },
                'ovp_max': 33.0,
                'ocp_max': 3.3,
                'voltage_max': 30.0,
                'current_max': 3.0
            },
            {
                'range': {
                    'P30V': (30.0, 3.0)
                },
                'ovp_max': 33.0,
                'ocp_max': 3.3,
                'voltage_max': 30.0,
                'current_max': 3.0
            },
            {
                'range': {
                    'P5V': (5.0, 3.0)
                },
                'ovp_max': 5.5,
                'ocp_max': 3.3,
                'voltage_max': 5.0,
                'current_max': 3.0
            }
        ]
        
        self._init_outputs()
    
    
