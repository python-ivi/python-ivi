"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich
Copyright (c) 2015 Rikard Lindstrom

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

from .. import ivi
from .. import dmm
from .. import scpi

MeasurementFunctionMapping = {
        'dc_volts': 'volt:dc',
        'ac_volts': 'volt:ac',
        'dc_current': 'curr:dc',
        'ac_current': 'curr:ac',
        'two_wire_resistance': 'res',
        'four_wire_resistance': 'fres',
        'frequency': 'freq',
        'period': 'per',
        'continuity': 'cont',
        'diode': 'diod',
        'capacitance': 'cap',
        'temperature': 'temp'}

MeasurementRangeMapping = {
        'dc_volts': 'volt:dc:range',
        'ac_volts': 'volt:ac:range',
        'dc_current': 'curr:dc:range',
        'ac_current': 'curr:ac:range',
        'two_wire_resistance': 'res:range',
        'four_wire_resistance': 'fres:range',
        'frequency': 'freq:volt:range'}

MeasurementAutoRangeMapping = {
        'dc_volts': 'volt:dc:range:auto',
        'ac_volts': 'volt:ac:range:auto',
        'dc_current': 'curr:dc:range:auto',
        'ac_current': 'curr:ac:range:auto',
        'two_wire_resistance': 'res:range:auto',
        'four_wire_resistance': 'fres:range:auto',
        'frequency': 'freq:volt:range:auto'}

MeasurementResolutionMapping = {
        'dc_volts': 'volt:dc:resolution',
        'ac_volts': 'volt:ac:resolution',
        'dc_current': 'curr:dc:resolution',
        'ac_current': 'curr:ac:resolution',
        'two_wire_resistance': 'res:resolution',
        'four_wire_resistance': 'fres:resolution'}
        
ThermocoupleReferenceJunctionType = set(['internal', 'fixed'])
ThermocoupleType = set(['b', 'c', 'd', 'e', 'g', 'j', 'k', 'n', 'r', 's', 't', 'u', 'v'])
TemperatureTransducerType = {
		'thermocouple': 'tc', 
		'thermistor': 'thermistor',
		'four_wire_thermistor': 'fthermistor',
		'two_wire_rtd': 'rtd', 
		'four_wire_rtd': 'frtd'}

class rigolDM3068Agilent(
		scpi.dmm.Base,
		dmm.ACMeasurement,
		dmm.TemperatureMeasurement,
		dmm.Thermocouple,
		dmm.ResistanceTemperatureDevice,
		dmm.Thermistor
	):
    "Rigol DM3068 in Agilent mode IVI DMM driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'DM3068')
        
        super(rigolDM3068Agilent, self).__init__(*args, **kwargs)
        
        self._memory_size = 5
        
        self._ac_frequency_max = 300000 #can't be changed
        
        self._identity_description = "Rigol DM3068 in Agilent mode IVI DMM driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Rigol Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['DM3068']
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(rigolDM3068Agilent, self)._initialize(resource, id_query, reset, **keywargs)
        
        #Fix for "Vxi11Exception: 11: Device locked by another link [write]" error
        self._interface.lock_timeout = 0
        
        #Select agilent commands, should be compatible wit Agilent 34401
        self._write("CMDSet AGILENT");

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
            self.utility.reset()

    def _get_measurement_function(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":conf?").lower().strip('"').split(" ")[0]
            value = [k for k,v in MeasurementFunctionMapping.items() if v==value][0]
            self._measurement_function = value
            self._set_cache_valid()
        return self._measurement_function
    
    def _set_measurement_function(self, value):
        if value not in MeasurementFunctionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":meas:%s?" % MeasurementFunctionMapping[value])
        self._measurement_function = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'range')
        self._set_cache_valid(False, 'auto_range')
        self._set_cache_valid(False, 'resolution')
    
    def _get_range(self):
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementRangeMapping:
                cmd = MeasurementRangeMapping[func]
                value = float(self._ask("%s?" % (cmd)))
                self._range = value
                self._set_cache_valid()
        return self._range
    
    def _set_range(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementRangeMapping:
                cmd = MeasurementRangeMapping[func]
                self._write("%s %g" % (cmd, value))
        self._range = value
        self._set_cache_valid()
        
    def _set_resolution(self, value):
        value = float(value)
        minVal = (0.03 / 1000000) * self._get_range()
        maxVal = (6.0 / 1000000) * self._get_range()
        value = min(maxVal, value)
        value = max(minVal, value)
        
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementResolutionMapping:
                cmd = MeasurementResolutionMapping[func]
                self._write("%s %g" % (cmd, value))
        self._resolution = value
        self._set_cache_valid()
        
    def _get_ac_frequency_max(self):
        return self._ac_frequency_max
    
    def _set_ac_frequency_max(self, value):
        pass #can't be changed, do nothing
    
    def _get_ac_frequency_min(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = float(self._ask(":detector:bandwidth?"))
            self._ac_frequency_min = value
            self._set_cache_valid()
        return self._ac_frequency_min
    
    def _set_ac_frequency_min(self, value):
        if (value >= 200): value = 200
        elif (value < 20): value = 3
        else: value = 20
        
        if not self._driver_operation_simulate:
        	self._write(":detector:bandwidth %i" % value)
        
        value = float(value)
        self._ac_frequency_min = value
        self._set_cache_valid()
    
    def _get_temperature_transducer_type(self):
    	if not self._driver_operation_simulate and not self._get_cache_valid():
            self._temperature_transducer_type = self._ask(":temperature:transducer:type?")
            self._set_cache_valid()
        return self._temperature_transducer_type
    
    def _set_temperature_transducer_type(self, value):
        if value not in TemperatureTransducerType:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
        	self._write("temperature:transducer:type %s" % TemperatureTransducerType[value])
        self._temperature_transducer_type = value
        self._set_cache_valid()
