"""

Python Interchangeable Virtual Instrument Library
Driver for Test Equity Model 140

Copyright (c) 2014-2017 Jeff Wurzbach

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
from .. import ics

class testequityf4(ivi.IviContainer):
    "Watlow F4 controller used in TestEquity Enviromental Chambers"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(testequityf4, self).__init__(*args, **kwargs)

        self._add_property('chamber_temperature', self._get_temperature)
        self._add_property('chamber_temperature_setpoint', self._get_temperature_setpoint, self._set_temperature_setpoint )
        self._add_property('chamber_humidity', self._get_humidity)
        self._add_property('chamber_humidity_setpoint', self._get_humidity_setpoint, self._set_humidity_setpoint)
        self._add_property('temperature_decimal_config', self._get_temperature_decimal_config)
        self._add_property('humidity_decimal_config', self._get_humidity_decimal_config)
        self._add_property('part_temperature_decimal_config', self._get_part_temperature_decimal_config)
        self._add_property('temperature_unit', self._get_temperature_unit_config)
        self._temperature_decimal_config = 1 #default to 500 means 50.0degC
        self._humidity_decimal_config = 1 #default to 500 means 50.0%RH
        self._part_temperature_decimal_config = 1 #default to 500 means 50.0degC
        self._temperature_unit = 1 #default to degC
    
    
    #grab the decimal configrutions for the controller and chache them.  provide a method to change them if allowed (i.e. if someone changes the defualt config from TestEquity).
    def _get_temperature_decimal_config(self):
       if not self._driver_operation_simulate and not self._get_cache_valid():
           self._temperature_decimal_config = self._read_register(606)
           self._set_cache_valid()
       return self._temperature_decimal_config
    
    def _get_humidity_decimal_config(self):
       if not self._driver_operation_simulate and not self._get_cache_valid():
           self._humidity_decimal_config = self._read_register(616)
           self._set_cache_valid()
       return self._humidity_decimal_config
    
    def _get_part_temperature_decimal_config(self):
       if not self._driver_operation_simulate and not self._get_cache_valid():
           self._part_temperature_decimal_config = self._read_register(626)
           self._set_cache_valid()
       return self._part_temperature_decimal_config       
    
    def _set_temperature_decimal_config(self, value):
       value = int(value)
       if not self._driver_operation_simulate:
           self._write_register(606,value)
       self._temperature_decimal_config= value

    def _set_humidity_decimal_config(self, value):
       value = int(value)
       if not self._driver_operation_simulate:
           self._write_register(616,value)
       self._humidity_decimal_config= value    
    
    def _set_part_temperature_decimal_config(self, value):
       value = int(value)
       if not self._driver_operation_simulate:
           self._write_register(626,value)
       self._part_temperature_decimal_config= value
    
    #Provide ability to read and write the config on the UOM for temperature.  Cache results to make sure things work nicely
    def _get_temperature_unit_config(self):
       if not self._driver_operation_simulate and not self._get_cache_valid():
           self._temperature_unit = self._read_register(901)
           self._set_cache_valid()
       return self._temperature_unit
       
    def _set_temperature_unit_config(self, unit_of_measure="c"):
        self.driver_operation.invalidate_all_attributes()
        if unit_of_measure=="f":
            value = 0
        else:
            value = 1
        value = int(value)
        if not self._driver_operation_simulate:
            self._write_register(901,value)
        self._temperature_unit= value
    
    
    
    #_get_temperature(), _get_humidity(), and _get_part_temperature() are not cached so that the reads are accruate.    
    def _get_temperature(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(100))
            if self._temperature_decimal_config==1:
                temperature=float(resp)/10
            else:
                temperature=float(resp)
            return temperature
        return 0
    
    def _get_humidity(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(104))
            if self._humidity_decimal_config==1:
                humidity=float(resp)/10
            else:
                humidity=float(resp)
            return humidity
        return 0
        
    def _get_part_temperature(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(108))
            if self._part_temperature_decimal_config==1:
                part_temperature=float(resp)/10
            else:
                part_temperature=float(resp)
            return part_temperature
        return 0
     
    #get the compressor state
    def _get_compressor_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2070))
            return resp
        return 0
    
    #get the event 1 register state
    def _get_event_one_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2000))
            return resp
        return 0        
   
   #get the event 2 register state
    def _get_event_two_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2010))
            return resp
        return 0
    
    #get the event 3 register state
    def _get_event_three_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2020))
            return resp
        return 0  
        
    #get the event 4 register state
    def _get_event_four_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2030))
            return resp
        return 0 

    #get the event 5 register state
    def _get_event_five_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2040))
            return resp
        return 0 

        
    #get the event 6 register state
    def _get_event_six_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2050))
            return resp
        return 0 
    
    #get the event 7 register state
    def _get_event_seven_state(self):
        if not self._driver_operation_simulate: 
            resp=int(self._read_register(2060))
            return resp
        return 0
        
    #set the event 1 register state
    def _set_event_one_state(self, state):
        value=int(bool(state))
        if not self._driver_operation_simulate: 
            self._write_register(2000, value)
            
                
   
   #set the event 2 register state
    def _set_event_two_state(self, state):
        value=int(bool(state))
        if not self._driver_operation_simulate: 
            self._write_register(2010, value)
           
    
    #set the event 3 register state
    def _set_event_three_state(self, state):
        value=int(bool(state))
        if not self._driver_operation_simulate: 
            self._write_register(2020, value)
 
        
    #set the event 4 register state
    def _set_event_four_state(self, state):
        value=int(bool(state))
        if not self._driver_operation_simulate: 
            self._write_register(2030, value)


    #set the event 5 register state
    def _set_event_five_state(self, state):
        value=int(bool(state))
        if not self._driver_operation_simulate: 
            self._write_register(2040, value)
 

        
    #set the event 6 register state
    def _set_event_six_state(self, state):
        value=int(bool(state))
        if not self._driver_operation_simulate: 
            self._write_register(2050, value)

    
    #set the event 7 register state
    def _set_event_six_state(self, state):
        value=int(bool(state))
        if not self._driver_operation_simulate: 
            self._write_register(2060, value)
            
    def _get_temperature_setpoint(self):
        resp=int(self._read_register(300))
        #print(resp)
        #print(self._temperature_decimal_config)
        if self._temperature_decimal_config==1:
            temperature=float(resp)/10
        else:
            temperature=float(resp)
        return temperature
        
    def _get_humidity_setpoint(self):
        resp=int(self._read_register(319))
        if self._humidity_decimal_config==1:
            humidity=float(resp)/10
        else:
            humidity=float(resp)
        return humidity
                

        
    def _set_temperature_setpoint(self, value):
        if self._temperature_decimal_config==1:
            temperature=int(float(value)*10)
        else:
            temperature=int(value)        
          
        if not self._driver_operation_simulate: 
            self._write_register(300, temperature)

            
            
            
    def _set_humidity_setpoint(self, value):
        if self._humidity_decimal_config==1:
            humidity=int(float(value)*10)
        else:
            humidity=int(value)        
          
        if not self._driver_operation_simulate: 
            self._write_register(319, humidity)