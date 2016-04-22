"""

Python Interchangeable Virtual Instrument Library - Rigol Oscilloscope Driver

Copyright (c) 2016 Ian Rees

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
from .. import scope
from .. import scpi

class rigolBaseScope( scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset,
                      scpi.common.SelfTest, scpi.common.Memory,
                      scope.Base, 
                      ivi.Driver ):
    "Rigol generic IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_scale = list()
        self._channel_invert = list()
        self._channel_bw_limit = list()
        
        super(rigolBaseScope, self).__init__(*args, **kwargs)
        
        self._self_test_delay = 40
        self._memory_size = 10
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        
        self._timebase_scale = 1e-6
        self._horizontal_divisions = 12
        self._vertical_divisions = 8

        self._trigger_sweep = "AUTO"
        
        self._identity_description = "Rigol generic IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "RIGOL Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = [ "DS1054Z" ]
       
########                 Nonstandard IVI properties                ######## 
# note that member variables are initialised in __init__ above, or 
# _init_channels() below.
        self._add_property( "channels[].bw_limit",
                            self._get_channel_bw_limit,
                            self._set_channel_bw_limit,
                            None,
                            ivi.Doc("20Mhz low-pass filter.  True=enabled.") )
        self._add_property("channels[].invert",
                           self._get_channel_invert,
                           self._set_channel_invert,
                           None,
                           ivi.Doc("""
                           Selects whether or not to invert the channel.
                           """))
        self._add_property("channels[].scale",
                           self._get_channel_scale,
                           self._set_channel_scale,
                           None,
                           ivi.Doc("""
                           Specifies the vertical scale, or units per division,
                           of the channel.  Units are volts.
                           """))
        self._add_property("channels[].tcal",
                           self._get_channel_tcal,
                           self._set_channel_tcal,
                           None,
                           ivi.Doc("""
                           Delay time calibration of the channel.  Only relevant
                           if timebase is less than 10us.
                           """))
        self._add_property("channels[].units",
                           self._get_channel_units,
                           self._set_channel_units,
                           None,
                           ivi.Doc("""
                           Display units for the channel.  Allowed values are:
                           VOLTage, WATT, AMPere, UNKNown
                           """))
        self._add_property("channels[].vernier",
                           self._get_channel_vernier,
                           self._set_channel_vernier,
                           None,
                           ivi.Doc("""
                           Allows for Vernier (fine) adjustment of the vertical
                           scale of each channel.  True = Vernier adjustment ON
                           """))
        self._add_property("timebase.scale",
                           self._get_timebase_scale,
                           self._set_timebase_scale,
                           None,
                           ivi.Doc("""
                           Sets the horizontal scale in seconds per division of 
                           the main window.
                           """))
        self._add_property("trigger.sweep",
                           self._get_trigger_sweep,
                           self._set_trigger_sweep,
                           None,
                           ivi.Doc("Trigger sweep mode; one of AUTO NORMal SINGLe"))

    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        
        super(rigolBaseScope, self)._initialize(resource, id_query, reset, **keywargs)
        
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

    
    def _utility_disable(self):
        pass
    
    def _utility_lock_object(self):
        pass
    
    def _utility_unlock_object(self):
        pass
    
    def _init_channels(self):
        try:
            super(rigolBaseScope, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list() # This seems important TODO: Figure out construction...

        self._channel_bw_limit = list()
        self._channel_invert = list()
        self._channel_scale = list()
        self._channel_tcal = list()
        self._channel_units = list()
        self._channel_vernier = list()
        
        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._analog_channel_name.append("channel%d" % (i+1))

            self._channel_bw_limit.append(False)
            self._channel_invert.append(False)
            self._channel_scale.append(1.0)
            self._channel_tcal.append(0.0)
            self._channel_units.append("VOLT")
            self._channel_vernier.append(False)
        
        # digital channels
        self._digital_channel_name = list()
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("d%d" % i)
            
            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_impedance[i] = 100000
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'dc'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)

