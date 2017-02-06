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

import array
import io
import struct
import sys
import time

import numpy as np

from . import hprtl

from .. import ivi
from .. import specan
from .. import extra

AmplitudeUnitsMapping = {'dBm' : 'dbm',
                         'dBmV' : 'dbmv',
                         'dBuV' : 'dbuv',
                         'volt' : 'v',
                         'watt' : 'w'}
DetectorTypeMapping = {'maximum_peak' : 'pos',
                       'minimum_peak' : 'neg',
                       'sample' : 'smp'}
#TraceType = set(['clear_write', 'maximum_hold', 'minimum_hold', 'video_average', 'view', 'store'])
VerticalScale = set(['linear', 'logarithmic'])
#AcquisitionStatus = set(['complete', 'in_progress', 'unknown'])
ALCSourceMapping = {'internal': 'int',
                    'external': 'ext'}
PowerMode = set(['fixed', 'sweep'])

class agilentBase8590(ivi.Driver, specan.Base,
                extra.common.SerialNumber, extra.common.Memory, extra.common.Title, extra.common.SystemSetup, extra.common.Screenshot):
    "Agilent 8590 series IVI spectrum analyzer driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(agilentBase8590, self).__init__(*args, **kwargs)
        
        self._trace_count = 3

        self._memory_size = 9
        
        self._input_impedance = 50
        self._frequency_low = 9e3
        self._frequency_high = 1.8e9

        self._rf_level = 0.0
        self._rf_attenuation = 0.0
        self._rf_attenuation_auto = True
        self._rf_output_enabled = False
        self._rf_power_mode = 'fixed'
        self._rf_power_offset = 0.0
        self._rf_power_span = 0.0
        self._rf_tracking_adjust = 0
        self._alc_source = 'internal'

        self._identity_description = "Agilent 8590 series IVI spectrum analyzer driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['8590A', '8590B', '8591A', '8592A', '8592B',
                        '8593A', '8594A', '8595A''8590E', '8590L', '8591C', '8591E', '8591EM',
                        '8592L', '8593E', '8593EM', '8594E', '8594EM', '8594L', '8594Q', '8595E',
                        '8595EM', '8596E', '8596EM']
        
        self._add_method('display.clear',
                        self._display_clear,
                        ivi.Doc("""
                        Clears the display and resets all associated measurements. If the
                        oscilloscope is stopped, all currently displayed data is erased. If the
                        oscilloscope is running, all the data in active channels and functions is
                        erased; however, new data is displayed on the next acquisition.
                        """))
        self._add_method('system.display_string',
                        self._system_display_string,
                        ivi.Doc("""
                        Writes a string to the advisory line on the instrument display.  Send None
                        or an empty string to clear the advisory line.  
                        """))

        self._add_property('frequency.center',
                        self._get_frequency_center,
                        self._set_frequency_center)
        self._add_property('frequency.span',
                        self._get_frequency_span,
                        self._set_frequency_span)

        self._add_property('rf.level',
                        self._get_rf_level,
                        self._set_rf_level)
        self._add_property('rf.attenuation',
                        self._get_rf_attenuation,
                        self._set_rf_attenuation)
        self._add_property('rf.attenuation_auto',
                        self._get_rf_attenuation_auto,
                        self._set_rf_attenuation_auto)
        self._add_property('rf.output_enabled',
                        self._get_rf_output_enabled,
                        self._set_rf_output_enabled)
        self._add_property('rf.power_mode',
                        self._get_rf_power_mode,
                        self._set_rf_power_mode)
        self._add_property('rf.power_offset',
                        self._get_rf_power_offset,
                        self._set_rf_power_offset)
        self._add_property('rf.power_span',
                        self._get_rf_power_span,
                        self._set_rf_power_span)
        self._add_property('rf.tracking_adjust',
                        self._get_rf_tracking_adjust,
                        self._set_rf_tracking_adjust)
        self._add_method('rf.tracking_peak',
                        self._rf_tracking_peak)
        self._add_property('alc.source',
                        self._get_alc_source,
                        self._set_alc_source)

        self._init_traces()
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilentBase8590, self)._initialize(resource, id_query, reset, **keywargs)
        
        # interface clear
        if not self._driver_operation_simulate:
            # don't clear; actually resets device
            #self._clear()
            pass
        
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
            self._identity_instrument_serial_number = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            self._identity_instrument_manufacturer = "Agilent Technologies"
            self._identity_instrument_model = self._ask("ID?")
            self._identity_instrument_serial_number = self._ask("SER?")
            self._identity_instrument_firmware_revision = self._ask("REV?")
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_serial_number')
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
    
    def _get_identity_instrument_serial_number(self):
        if self._get_cache_valid():
            return self._identity_instrument_serial_number
        self._load_id_string()
        return self._identity_instrument_serial_number
    
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
            # TODO is there a command for this?
            #error_code, error_message = self._ask(":system:error?").split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (error_code, error_message)
    
    def _utility_lock_object(self):
        pass
    
    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("IP")
            self.driver_operation.invalidate_all_attributes()
    
    def _utility_reset_with_defaults(self):
        self._utility_reset()
    
    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            self._write("CNF?")
            # wait for test to complete
            time.sleep(40)
            # TODO any way to check status?
            code = int(self._read())
            if code != 0:
                message = "Self test failed"
        return (code, message)
    
    def _utility_unlock_object(self):
        pass



    def _init_traces(self):
        try:
            super(agilentBase8590, self)._init_traces()
        except AttributeError:
            pass

        self._trace_name = list()
        self._trace_type = list()
        for i in range(self._trace_count):
            self._trace_name.append("tr%c" % (i+ord('a')))
            self._trace_type.append('')

        self.traces._set_list(self._trace_name)

    def _system_fetch_setup(self):
        if self._driver_operation_simulate:
            return b''
        
        self._write("OL?")
        
        return self._read_raw()
    
    def _system_load_setup(self, data):
        if self._driver_operation_simulate:
            return
        
        self._write_raw(data)
    
    def _system_display_string(self, string=None):
        if string is None:
            string = ""
        
        if not self._driver_operation_simulate:
            self._write("PU")
            self._write("PA 8,137")
            self._write("HD")
            self._write("TEXT \\%s\\" % string)
    
    def _display_clear(self):
        if not self._driver_operation_simulate:
            self._write("HD")
            self._write("CLRDSP")
    
    def _get_display_title(self):
        # cannot read
        return self._display_title

    def _set_display_title(self, value):
        value = str(value)
        if not self._driver_operation_simulate:
            self._write("TITLE \\%s\\" % value)
        self._display_title = value
        self._set_cache_valid()

    def _display_fetch_screenshot(self, format='bmp', invert=False):
        if self._driver_operation_simulate:
            return b''
        
        #if format not in ScreenshotImageFormatMapping:
        #    raise ivi.ValueNotSupportedException()
        
        #format = ScreenshotImageFormatMapping[format]
        
        self._write("PRNPRT 0")
        self._write("PRINT 1")
        
        rtl = io.BytesIO(self._read_raw())

        img = hprtl.parse_hprtl(rtl)

        # rescale to get white background
        # presuming background of (90, 88, 85)
        np.multiply(img[:,:,0], 255/90, out=img[:,:,0], casting='unsafe')
        np.multiply(img[:,:,1], 255/88, out=img[:,:,1], casting='unsafe')
        np.multiply(img[:,:,2], 255/85, out=img[:,:,2], casting='unsafe')

        bmp = hprtl.generate_bmp(img)

        return bmp
    
    def _memory_save(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("SAVES %d" % index+1)
    
    def _memory_recall(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("RCLS %d" % index+1)
            self.driver_operation.invalidate_all_attributes()

    def _get_rf_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level = float(self._ask("srcpwr?"))
            self._set_cache_valid()
        return self._rf_level

    def _set_rf_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("srcpwr %e" % value)
        self._rf_level = value
        self._set_cache_valid()

    def _get_rf_attenuation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_attenuation = float(self._ask("srcat?"))
            self._set_cache_valid()
        return self._rf_attenuation

    def _set_rf_attenuation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("srcat %e" % value)
        self._rf_attenuation = value
        self._rf_attenuation_auto = False
        self._set_cache_valid()

    def _get_rf_attenuation_auto(self):
        # TODO is it possible to read this?
        return self._rf_attenuation_auto

    def _set_rf_attenuation_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("srcat %s" % ('auto' if value else 'man'))
        self._rf_attenuation_auto = value
        self._set_cache_valid()

    def _get_rf_output_enabled(self):
        # TODO is it possible to read this?
        return self._rf_output_enabled

    def _set_rf_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("srcpwr %s" % ('on' if value else 'off'))
        self._rf_output_enabled = value
        self._set_cache_valid()

    def _get_rf_power_mode(self):
        # TODO is it possible to read this?
        return self._rf_power_mode

    def _set_rf_power_mode(self, value):
        if value not in PowerMode:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("srcpswp %s" % ('on' if value == 'sweep' else 'off'))
        self._rf_power_mode = value
        self._set_cache_valid(False, 'rf_power_span')
        self._set_cache_valid()

    def _get_rf_power_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_power_offset = float(self._ask("srcpofs?"))
            self._set_cache_valid()
        return self._rf_power_offset

    def _set_rf_power_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("srcpofs %e" % value)
        self._rf_power_offset = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'rf_level')

    def _get_rf_power_span(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_power_span = float(self._ask("srcpswp?"))
            self._set_cache_valid()
        return self._rf_power_span

    def _set_rf_power_span(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("srcpswp %e" % value)
        self._rf_power_span = value
        self._set_cache_valid(False, 'rf_power_mode')
        self._set_cache_valid()

    def _get_rf_tracking_adjust(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_tracking_adjust = int(self._ask("srctk?"))
            self._set_cache_valid()
        return self._rf_tracking_adjust

    def _set_rf_tracking_adjust(self, value):
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("srctk %d" % value)
        self._rf_tracking_adjust = value
        self._set_cache_valid()

    def _rf_tracking_peak(self):
        if not self._driver_operation_simulate:
            self._write("srctkpk")

    def _rf_configure(self, frequency, level):
        self._set_rf_frequency(frequency)
        self._set_rf_level(level)

    def _get_alc_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("srcalc?").lower()
            self._alc_source = [k for k,v in ALCSourceMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._alc_source

    def _set_alc_source(self, value):
        if value not in ALCSourceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("srcalc %s" % ALCSourceMapping[value])
            self._set_cache_valid()
        self._alc_source = value

    def _get_level_amplitude_units(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("aunits?").lower()
            self._level_amplitude_units = [k for k,v in AmplitudeUnitsMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._level_amplitude_units
    
    def _set_level_amplitude_units(self, value):
        if value not in AmplitudeUnitsMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("aunits %s" % AmplitudeUnitsMapping[value])
        self._level_amplitude_units = value
        self._set_cache_valid()
    
    def _get_level_attenuation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._level_attenuation = float(self._ask("at?"))
            self._set_cache_valid()
        return self._level_attenuation
    
    def _set_level_attenuation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("at %e db" % value)
        self._level_attenuation = value
        self._set_cache_valid()
    
    def _get_level_attenuation_auto(self):
        # TODO is it possible to read this?
        return self._level_attenuation_auto
    
    def _set_level_attenuation_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("at %s" % ('auto' if value else 'man'))
        self._level_attenuation_auto = value
        self._set_cache_valid()
    
    def _get_acquisition_detector_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("det?").lower()
            self._acquisition_detector_type = [k for k,v in DetectorTypeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._acquisition_detector_type
    
    def _set_acquisition_detector_type(self, value):
        if value not in DetectorTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":det %s" % DetectorTypeMapping[value])
        self._acquisition_detector_type = value
        self._set_cache_valid()
    
    def _get_acquisition_detector_type_auto(self):
        return self._acquisition_detector_type_auto
    
    def _set_acquisition_detector_type_auto(self, value):
        value = bool(value)
        self._acquisition_detector_type_auto = value
    
    def _get_frequency_start(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_start = float(self._ask("fa?"))
            self._set_cache_valid()
        return self._frequency_start
    
    def _set_frequency_start(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("fa %f hz" % value)
        self._frequency_start = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'frequency_center')
        self._set_cache_valid(False, 'frequency_span')
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')
        self._set_cache_valid(False, 'sweep_coupling_sweep_time')
        self._set_cache_valid(False, 'sweep_coupling_video_bandwidth')
    
    def _get_frequency_stop(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_stop = float(self._ask("fb?"))
            self._set_cache_valid()
        return self._frequency_stop
    
    def _set_frequency_stop(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("fb %f hz" % value)
        self._frequency_stop = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'frequency_center')
        self._set_cache_valid(False, 'frequency_span')
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')
        self._set_cache_valid(False, 'sweep_coupling_sweep_time')
        self._set_cache_valid(False, 'sweep_coupling_video_bandwidth')

    def _get_frequency_center(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_center = float(self._ask("cf?"))
            self._set_cache_valid()
        return self._frequency_center

    def _set_frequency_center(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("cf %f hz" % value)
        self._frequency_center = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'frequency_start')
        self._set_cache_valid(False, 'frequency_stop')
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')
        self._set_cache_valid(False, 'sweep_coupling_sweep_time')
        self._set_cache_valid(False, 'sweep_coupling_video_bandwidth')

    def _get_frequency_span(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_span = float(self._ask("sp?"))
            self._set_cache_valid()
        return self._frequency_span

    def _set_frequency_span(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("sp %f hz" % value)
        self._frequency_span = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'frequency_start')
        self._set_cache_valid(False, 'frequency_stop')
        self._set_cache_valid(False, 'sweep_coupling_resolution_bandwidth')
        self._set_cache_valid(False, 'sweep_coupling_sweep_time')
        self._set_cache_valid(False, 'sweep_coupling_video_bandwidth')
    
    def _get_frequency_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._frequency_stop = float(self._ask("foffset?"))
            self._set_cache_valid()
        return self._frequency_offset
    
    def _set_frequency_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("foffset %e hz" % value)
        self._frequency_offset = value
        self._set_cache_valid()
    
    def _get_level_input_impedance(self):
        return self._level_input_impedance
    
    def _set_level_input_impedance(self, value):
        value = float(value)
        self._level_input_impedance = value
    
    def _get_acquisition_number_of_sweeps(self):
        return self._acquisition_number_of_sweeps
    
    def _set_acquisition_number_of_sweeps(self, value):
        value = int(value)
        self._acquisition_number_of_sweeps = value
    
    def _get_level_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._level_reference = float(self._ask("rl?"))
            self._set_cache_valid()
        return self._level_reference
    
    def _set_level_reference(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("rl %e db" % value)
        self._level_reference = value
        self._set_cache_valid()
    
    def _get_level_reference_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._level_reference = float(self._ask("roffset?"))
            self._set_cache_valid()
        return self._level_reference_offset
    
    def _set_level_reference_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("roffset %e db" % value)
        self._level_reference_offset = value
        self._set_cache_valid()
    
    def _get_sweep_coupling_resolution_bandwidth(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_resolution_bandwidth = float(self._ask("rb?"))
            self._set_cache_valid()
        return self._sweep_coupling_resolution_bandwidth
    
    def _set_sweep_coupling_resolution_bandwidth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("rb %e hz" % value)
        self._sweep_coupling_resolution_bandwidth = value
        self._sweep_coupling_resolution_bandwidth_auto = False
        self._set_cache_valid()
        self._set_cache_valid(True, 'sweep_coupling_resolution_bandwidth_auto')
    
    def _get_sweep_coupling_resolution_bandwidth_auto(self):
        # TODO is it possible to read this?
        return self._sweep_coupling_resolution_bandwidth_auto
    
    def _set_sweep_coupling_resolution_bandwidth_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("rb auto")
            else:
                self._set_sweep_coupling_resolution_bandwidth(self._get_sweep_coupling_resolution_bandwidth())
        self._sweep_coupling_resolution_bandwidth_auto = value
        self._set_cache_valid()
    
    def _get_acquisition_sweep_mode_continuous(self):
        return self._acquisition_sweep_mode_continuous
    
    def _set_acquisition_sweep_mode_continuous(self, value):
        value = bool(value)
        self._acquisition_sweep_mode_continuous = value
    
    def _get_sweep_coupling_sweep_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_sweep_time = float(self._ask("st?"))
            self._set_cache_valid()
        return self._sweep_coupling_sweep_time
    
    def _set_sweep_coupling_sweep_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("st %e s" % value)
        self._sweep_coupling_sweep_time = value
        self._sweep_coupling_sweep_time_auto = False
        self._set_cache_valid()
        self._set_cache_valid(True, 'sweep_coupling_sweep_time_auto')
    
    def _get_sweep_coupling_sweep_time_auto(self):
        # TODO is it possible to read this?
        return self._sweep_coupling_sweep_time_auto
    
    def _set_sweep_coupling_sweep_time_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("st auto")
            else:
                self._set_sweep_coupling_sweep_time(self._get_sweep_coupling_sweep_time())
        self._sweep_coupling_sweep_time_auto = value
        self._set_cache_valid()
    
    def _get_trace_type(self, index):
        index = ivi.get_index(self._trace_name, index)
        return self._trace_type[index]
    
    def _set_trace_type(self, index, value):
        index = ivi.get_index(self._trace_name, index)
        if value not in TraceType:
            raise ivi.ValueNotSupportedException()
        self._trace_type[index] = value
    
    def _get_acquisition_vertical_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_vertical_scale = 'logarithmic' if (self._ask("lg?") != '0') else 'linear'
            self._set_cache_valid()
        return self._acquisition_vertical_scale

    def _set_acquisition_vertical_scale(self, value):
        if value not in VerticalScale:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if value == 'logarithmic':
                self._write('lg')
            elif value == 'linear':
                self._write('ln')
        self._acquisition_vertical_scale = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'level_reference')
    
    def _get_sweep_coupling_video_bandwidth(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._sweep_coupling_resolution_bandwidth = float(self._ask("vb?"))
            self._set_cache_valid()
        return self._sweep_coupling_video_bandwidth
    
    def _set_sweep_coupling_video_bandwidth(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("vb %e hz" % value)
        self._sweep_coupling_video_bandwidth = value
        self._sweep_coupling_video_bandwidth_auto = False
        self._set_cache_valid()
        self._set_cache_valid(True, 'sweep_coupling_video_bandwidth_auto')
    
    def _get_sweep_coupling_video_bandwidth_auto(self):
        # TODO is it possible to read this?
        return self._sweep_coupling_video_bandwidth_auto
    
    def _set_sweep_coupling_video_bandwidth_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write("vb auto")
            else:
                self._set_sweep_coupling_video_bandwidth(self._get_sweep_coupling_video_bandwidth())
        self._sweep_coupling_video_bandwidth_auto = value
        self._set_cache_valid()
    
    def _acquisition_abort(self):
        pass
    
    def _acquisition_status(self):
        return 'unknown'
    
    def _trace_fetch_y(self, index):
        index = ivi.get_index(self._trace_name, index)

        if self._driver_operation_simulate:
            return ivi.TraceY()

        cmd = ''

        if index == 0:
            cmd = 'tra?'
        elif index == 1:
            cmd = 'trb?'
        elif index == 2:
            cmd = 'trc?'
        else:
            return None

        log_scale = float(self._ask("lg?"))
        ref_level = float(self._ask("rl?"))

        self._write('tdf a; mds w;')
        self._write(cmd)

        buf = self._read_raw(4)
        if buf[0:2] != b'#A':
            return None

        cnt = struct.unpack(">H", buf[2:4])[0]
        buf = self._read_raw(cnt)

        trace = ivi.TraceY()

        if log_scale > 0:
            # log scale
            trace.y_increment = 0.01
            trace.y_origin = ref_level
            trace.y_reference = 8000
        else:
            # linear scale
            trace.y_increment = ref_level/8000
            trace.y_origin = 0
            trace.y_reference = 0

        trace.y_raw = array.array('h', buf)

        if sys.byteorder == 'little':
            trace.y_raw.byteswap()

        return trace

    def _acquisition_initiate(self):
        pass
    
    def _trace_read_y(self, index):
        return self._trace_fetch_y(index)
    
    
