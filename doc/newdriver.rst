==============================
Writing New Python IVI Drivers
==============================

First, you're going to need to download the IVI specification for the type of instrument you have from the IVI foundation. This isn't completely necessary, but there is a lot of information in the spec about the specific functionality of various commands that isn't in the source code. I suppose this should probably be changed, but the spec is freely available so it isn't that big of an issue. You only need to download the spec for your type of device (IviFgen, IviScope, etc.).  You're also going to need to download the programming guide for your instrument, if you haven't already.

Now that you know what instrument class your instrument is, you should create a file for it in the proper subdirectory with the proper name. Note that supporting several instruments in the same line is pretty easy, just look at some of the other files for reference. I would highly recommend creating wrappers for all of the instruments in the series even if you don't have any on hand for testing. You also will need to add a line (or several lines) to ``__init__.py`` in the same directory so that the instrument files are loaded automatically with python-ivi and don't need to be loaded individually.

The structure of the individual driver files is quite simple. Take a look at the existing files for reference. Start by adding the header comment and license information. Then add the correct includes. At minimum, you will need to include ivi and the particular instrument class that you need from the parent directory (``from .. include ivi``). After that, you can specify any constants and/or mappings that the instrument requires. IVI specifies one set of standard configuration values for a lot of functions and this does not necessarily agree with the instrument's firmware, so it's likely you will need to redefine several of these lists as mappings to make writing the code easier. This can be done incrementally while the driver functionality is being implemented.

Next, you need to add the class definition. The name should match the file name, and it will derive from ivi.Driver and the supported subclasses of your instrument. Go over the IVI spec and the programming guide and see what subclasses are supported by seeing which functions are supported by the instrument. There isn't always going to be a 1:1 mapping - there will likely be functions that the instrument does not support but IVI has a wrapper for, and there will likely be functions that IVI does not have a wrapper for but the instrument does support that may be very useful. You should add a subclass if any portion of its functionality is supported by the instrument.

After that, you need to define the functions common to all IVI drivers. You can just copy everything from init to utility_unlock_object from an existing driver and then update everything for your instrument. Generally all this code will be very similar. Take a look at some of the existing drivers for reference. Very important: any ``super()`` calls must be updated so that the class name matches (requirement for Python 2). You should also remove all of the initialization in ``__init__`` that you don't need - the bare minimum is ``_instrument_id`` and all of the ``_identity`` values. For some instruments, you're going to need to specify channel counts as well as an ``_init_channels`` or ``_init_outputs`` method.  Note that if one of these methods is needed, it cannot be empty as it must at least have a call to super so that all of the proper init methods are called. At this point, you can test the connection to the equipment to make sure it is communicating and reading out the ID properly.

Testing you code is actually pretty straightforward; you don't need to re-install the library to test it; just make sure to instantiate it while you're running in the same directory as the ivi folder (not inside). I recommend ipython for testing. Unfortulatey, the auto reload doesn't work very well for python-ivi, so you'll need to restart ipython every time you change something. However, it supports history and autocompletion, so after you import IVI once, you can just type 'imp' and hit the up arrow until 'import ivi' shows up.

Test the interface and identity query by instantiating your driver and connecting to the instrument by running something like this in ipython::

   >>> import ivi
   >>> mso = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR")
   >>> mso.identity.instrument_model

If everything is working, the instrument's model number will be displayed. Once you get this working, you can move on to implementing the actual functionality.

Start by copying in all of the bare function definitions from the driver file. Copy all of the get and _set function definitions from the ivi driver file for the Base class and all of the subclasses that you are implementing. You also need any methods whose only implementation is 'pass'. The ones that call other methods can generally be left out as the default implementation should be fine. You may also want to copy some of the instance variable initializations from the ``__init__`` method as well if you need different defaults. These should be added to the init method you created earlier for your instrument.

Finally, you need to go write python code for all of the functions that the instrument supports. Take a look at some ``_get``/``_set`` pairs for some of the existing drivers to see the format. It's rather straightforward but quite tedious.  

Driver Template
---------------

This is a sample template driver that incorporates all of the major components.  It is drawn from the Agilent 7000 series driver.  Template::


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

    import struct

    from .. import ivi
    from .. import scope

    AcquisitionTypeMapping = {
            'normal': 'norm',
            'peak_detect': 'peak',
            'high_resolution': 'hres',
            'average': 'aver'}
    # more instrument-specific sets and mappings

    class agilent7000(ivi.Driver, scope.Base, scope.TVTrigger,
                    scope.GlitchTrigger, scope.WidthTrigger, scope.AcLineTrigger,
                    scope.WaveformMeasurement, scope.MinMaxWaveform,
                    scope.ContinuousAcquisition, scope.AverageAcquisition,
                    scope.SampleMode, scope.AutoSetup):
        "Agilent InfiniiVision 7000 series IVI oscilloscope driver"
        
        def __init__(self, *args, **kwargs):
            self._analog_channel_name = list()
            self._analog_channel_count = 4
            self._digital_channel_name = list()
            self._digital_channel_count = 16
            self._channel_label = list()
            # other per-channel instrument-specific variables that are
            # referenced in _init_channels
            
            super(agilent7000, self).__init__(*args, **kwargs)
            
            self._instrument_id = 'AGILENT TECHNOLOGIES'
            self._analog_channel_name = list()
            self._analog_channel_count = 4
            self._digital_channel_name = list()
            self._digital_channel_count = 16
            self._channel_count = 20
            self._bandwidth = 1e9
            # initialize other instrument-specific variables
            
            self._identity_description = "Agilent InfiniiVision 7000 series IVI oscilloscope driver"
            self._identity_identifier = ""
            self._identity_revision = ""
            self._identity_vendor = ""
            self._identity_instrument_manufacturer = "Agilent Technologies"
            self._identity_instrument_model = ""
            self._identity_instrument_firmware_revision = ""
            self._identity_specification_major_version = 4
            self._identity_specification_minor_version = 1
            self._identity_supported_instrument_models =['DSO7012A','DSO7014A','DSO7032A',
                    'DSO7034A','DSO7052A','DSO7054A','DSO7104A','MSO7012A','MSO7014A','MSO7032A',
                    'MSO7034A','MSO7052A','MSO7054A','MSO7104A','DSO7012B','DSO7014B','DSO7032B',
                    'DSO7034B','DSO7052B','DSO7054B','DSO7104B','MSO7012B','MSO7014B','MSO7032B',
                    'MSO7034B','MSO7052B','MSO7054B','MSO7104B']
            
            self.channels._add_property('label',
                            self._get_channel_label,
                            self._set_channel_label,
                            None,
                            """
                            Custom property documentation
                            """)
            # other instrument specific properties
            
            self._init_channels()
        
        def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
            "Opens an I/O session to the instrument."
            
            self._channel_count = self._analog_channel_count + self._digital_channel_count
            
            super(agilent7000, self).initialize(resource, id_query, reset, **keywargs)
            
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
        
        def _init_channels(self):
            super(agilent7000, self)._init_channels()
            
            self._channel_name = list()
            self._channel_label = list()
            # init per-channel instrument-specific variables
            
            for i in range(self._channel_count):
                self._channel_name.append("channel%d" % (i+1))
                self._channel_label.append("%d" % (i+1))
                # init per-channel instrument-specific variables
            
            self.channels._set_list(self._channel_name)
        
        def _get_acquisition_start_time(self):
            pos = 0
            if not self._driver_operation_simulate and not self._get_cache_valid():
                pos = float(self._ask(":timebase:position?"))
                self._set_cache_valid()
            self._acquisition_start_time = pos - self._get_acquisition_time_per_record() * 5 / 10
            return self._acquisition_start_time
        
        def _set_acquisition_start_time(self, value):
            value = float(value)
            value = value + self._get_acquisition_time_per_record() * 5 / 10
            if not self._driver_operation_simulate:
                self._write(":timebase:position %e" % value)
            self._acquisition_start_time = value
            self._set_cache_valid()
        
        # more definitions
    

