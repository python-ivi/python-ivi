"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2016-2017 Alex Forencich

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
import sys
import time

from .. import ivi
from .. import scope
from .. import scpi
from .. import extra

AcquisitionTypeMapping = {
        'normal': 'sample',
        'peak_detect': 'peakdetect',
        'high_resolution': 'hires',
        'average': 'average',
        'envelope': 'envelope'}
VerticalCoupling = set(['ac', 'dc'])
TriggerTypeMapping = {
        'edge': 'edge',
        'runt': 'pulse',
        'width': 'pulse',
        'glitch': 'pulse',
        'tv': 'video',
        #'immediate': '',
        'ac_line': 'edge',
        'logic': 'logic',
        'bus': 'bus'}
TriggerCouplingMapping = {
        'ac': 'ac',
        'dc': 'dc',
        'hf_reject': 'hfrej',
        'lf_reject': 'lfrej',
        'noise_reject': 'noiserej'}
TVTriggerEventMapping = {'field1': 'odd',
        'field2': 'even',
        'any_field': 'allfields',
        'any_line': 'alllines',
        'line_number': 'numeric'}
TVTriggerFormatMapping = {'ntsc': 'ntsc',
        'pal': 'pal',
        'secam': 'secam',
        'bilevelcustom': 'bilevelcustom',
        'trilevelcustom': 'trilevelcustom',
        'hd480p60' : 'hd480p60',
        'hd576p50' : 'hd576p50',
        'hd720p30' : 'hd720p30',
        'hd720p50' : 'hd720p50',
        'hd720p60' : 'hd720p60',
        'hd875i60' : 'hd875i60',
        'hd1080p24' : 'hd1080p24',
        'hd1080sf24' : 'hd1080sf24',
        'hd1080i50' : 'hd1080i50',
        'hd1080i60' : 'hd1080i60',
        'hd1080p25' : 'hd1080p25',
        'hd1080p30' : 'hd1080p30',
        'hd1080p50' : 'hd1080p50',
        'hd1080p60' : 'hd1080p60'}
PolarityMapping = {'positive': 'positive',
        'negative': 'negative'}
PolarityMapping3 = {'positive': 'positive',
        'negative': 'negative',
        'either': 'either'}
GlitchConditionMapping = {'less_than': 'lessthan',
        'greater_than': 'morethan',
        'equal': 'equal',
        'unequal': 'unequal'}
WidthConditionMapping = {'within': 'within', 'outside': 'outside'}
SampleModeMapping = {'real_time': 'rtim',
        'equivalent_time': 'etim',
        'segmented': 'segm'}
SlopeMapping = {
        'positive': 'rise',
        'negative': 'fall',
        'either': 'either'}
MeasurementFunctionMapping = {
        'rise_time': 'rise',
        'fall_time': 'fall',
        'frequency': 'frequency',
        'period': 'period',
        'voltage_rms': 'rms',
        'voltage_peak_to_peak': 'pk2pk',
        'voltage_max': 'maximum',
        'voltage_min': 'minimum',
        'voltage_high': 'high',
        'voltage_low': 'low',
        'voltage_average': 'mean',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_negative': 'nduty',
        'duty_cycle_positive': 'pduty',
        'amplitude': 'amplitude',
        'voltage_cycle_rms': 'crms',
        'voltage_cycle_average': 'cmean',
        'overshoot': 'tovershoot',

        'area': 'area',
        'burst': 'burst',
        'cycle_area': 'carea',
        'overshoot_negative': 'novershoot',
        'overshoot_positive': 'povershoot',
        'edgecount_negative': 'nedgecount',
        'edgecount_positive': 'pedgecount',
        'pulsecount_negative': 'npulsecount',
        'pulsecount_positive': 'ppulsecount',

        'histogram_hits': 'hits',
        'histogram_peak_hits': 'peakhits',
        'histogram_median': 'median',
        'histogram_sigma1': 'sigma1',
        'histogram_sigma2': 'sigma2',
        'histogram_sigma3': 'sigma3',
        'histogram_stdev': 'stdev',
        'histogram_waveforms': 'waveforms',

        'phase': 'phase',
        'delay': 'delay'}
MeasurementFunctionMappingDigital = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle'}
ScreenshotImageFormatMapping = {
        'tif': 'tiff',
        'tiff': 'tiff',
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'png': 'png',
        'png24': 'png'}
TimebaseModeMapping = {
        'main': 'main',
        'window': 'window',
        'xy': 'xy'}
TriggerModifierMapping = {'none': 'normal', 'auto': 'auto'}

class tektronixBaseScope(scpi.common.IdnCommand, scpi.common.Reset, scpi.common.Memory,
                         scpi.common.SystemSetup,
                         scope.Base, scope.TVTrigger, scope.RuntTrigger,
                         scope.GlitchTrigger, scope.WidthTrigger, scope.AcLineTrigger,
                         scope.WaveformMeasurement, scope.MinMaxWaveform,
                         scope.ContinuousAcquisition, scope.AverageAcquisition,
                         scope.TriggerModifier, scope.AutoSetup,
                         extra.common.Screenshot,
                         ivi.Driver):
    "Tektronix generic IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_label = list()
        self._channel_probe_skew = list()
        self._channel_scale = list()
        self._channel_trigger_level = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_bw_limit = list()

        super(tektronixBaseScope, self).__init__(*args, **kwargs)

        self._memory_size = 10
        self._memory_offset = 1

        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9

        self._horizontal_divisions = 10
        self._vertical_divisions = 10

        self._acquisition_segmented_count = 2
        self._acquisition_segmented_index = 1
        self._timebase_mode = 'main'
        self._timebase_reference = 'center'
        self._timebase_position = 0.0
        self._timebase_range = 1e-3
        self._timebase_scale = 100e-6
        self._timebase_window_position = 0.0
        self._timebase_window_range = 5e-6
        self._timebase_window_scale = 500e-9
        self._display_screenshot_image_format_mapping = ScreenshotImageFormatMapping
        self._display_vectors = True
        self._display_labels = True

        self._identity_description = "Tektronix generic IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Tektronix"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['DPO4032', 'DPO4034', 'DPO4054', 
                'DPO4104', 'DPO4014B', 'DPO4034B', 'DPO4054B', 'DPO4102B', 'DPO4104B',
                'MSO4032', 'MSO4034', 'MSO4054', 'MSO4104', 'MSO4014B', 'MSO4034B',
                'MSO4054B', 'MSO4102B', 'MSO4104B', 'MDO4054', 'MDO4104', 'MDO4014B',
                'MDO4034B', 'MDO4054B', 'MDO4104B', 'MDO3012', 'MDO3014', 'MDO3022',
                'MDO3024', 'MDO3032', 'MDO3034', 'MDO3052', 'MDO3054', 'MDO3102',
                'MDO3104']

        self._add_property('channels[].invert',
                        self._get_channel_invert,
                        self._set_channel_invert,
                        None,
                        ivi.Doc("""
                        Selects whether or not to invert the channel.
                        """))
        self._add_property('channels[].label',
                        self._get_channel_label,
                        self._set_channel_label,
                        None,
                        ivi.Doc("""
                        Sets the channel label.  Setting a channel label also adds the label to
                        the nonvolatile label list.
                        """))
        self._add_property('channels[].probe_id',
                        self._get_channel_probe_id,
                        None,
                        None,
                        ivi.Doc("""
                        Returns the type of probe attached to the channel.
                        """))
        self._add_property('channels[].probe_skew',
                        self._get_channel_probe_skew,
                        self._set_channel_probe_skew,
                        None,
                        ivi.Doc("""
                        Specifies the channel-to-channel skew factor for the channel.  Each analog
                        channel can be adjusted + or - 100 ns for a total of 200 ns difference
                        between channels.  This can be used to compensate for differences in cable
                        delay.  Units are seconds.
                        """))
        self._add_property('channels[].scale',
                        self._get_channel_scale,
                        self._set_channel_scale,
                        None,
                        ivi.Doc("""
                        Specifies the vertical scale, or units per division, of the channel.  Units
                        are volts.
                        """))
        self._add_property('channels[].trigger_level',
                        self._get_channel_trigger_level,
                        self._set_channel_trigger_level,
                        None,
                        ivi.Doc("""
                        Specifies the trigger level of the channel.  Units are volts.
                        """))
        self._add_property('timebase.mode',
                        self._get_timebase_mode,
                        self._set_timebase_mode,
                        None,
                        ivi.Doc("""
                        Sets the current time base. There are four time base modes:

                        * 'main': normal timebase
                        * 'window': zoomed or delayed timebase
                        * 'xy': channels are plotted against each other, no timebase
                        * 'roll': data moves continuously from left to right
                        """))
        self._add_property('timebase.position',
                        self._get_timebase_position,
                        self._set_timebase_position,
                        None,
                        ivi.Doc("""
                        Sets the time interval between the trigger event and the display reference
                        point on the screen. The maximum position value depends on the time/division
                        settings.
                        """))
        self._add_property('timebase.range',
                        self._get_timebase_range,
                        self._set_timebase_range,
                        None,
                        ivi.Doc("""
                        Sets the full-scale horizontal time in seconds for the main window. The
                        range is 10 times the current time-per-division setting.
                        """))
        self._add_property('timebase.scale',
                        self._get_timebase_scale,
                        self._set_timebase_scale,
                        None,
                        ivi.Doc("""
                        Sets the horizontal scale or units per division for the main window.
                        """))
        self._add_property('timebase.window.position',
                        self._get_timebase_window_position,
                        self._set_timebase_window_position,
                        None,
                        ivi.Doc("""
                        Sets the horizontal position in the zoomed (delayed) view of the main
                        sweep. The main sweep range and the main sweep horizontal position
                        determine the range for this command. The value for this command must
                        keep the zoomed view window within the main sweep range.
                        """))
        self._add_property('timebase.window.range',
                        self._get_timebase_window_range,
                        self._set_timebase_window_range,
                        None,
                        ivi.Doc("""
                        Sets the fullscale horizontal time in seconds for the zoomed (delayed)
                        window. The range is 10 times the current zoomed view window seconds per
                        division setting. The main sweep range determines the range for this
                        command. The maximum value is one half of the timebase.range value.
                        """))
        self._add_property('timebase.window.scale',
                        self._get_timebase_window_scale,
                        self._set_timebase_window_scale,
                        None,
                        ivi.Doc("""
                        Sets the zoomed (delayed) window horizontal scale (seconds/division). The
                        main sweep scale determines the range for this command. The maximum value
                        is one half of the timebase.scale value.
                        """))
        self._add_property('display.vectors',
                        self._get_display_vectors,
                        self._set_display_vectors,
                        None,
                        ivi.Doc("""
                        When enabled, draws a line between consecutive waveform data points.
                        """))
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

        self._init_channels()

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        self._channel_count = self._analog_channel_count + self._digital_channel_count

        super(tektronixBaseScope, self)._initialize(resource, id_query, reset, **keywargs)

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
            super(tektronixBaseScope, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_label = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_scale = list()
        self._channel_trigger_level = list()
        self._channel_bw_limit = list()

        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append("ch%d" % (i+1))
            self._channel_label.append("")
            self._analog_channel_name.append("ch%d" % (i+1))
            self._channel_probe_skew.append(0)
            self._channel_scale.append(1.0)
            self._channel_trigger_level.append(0.0)
            self._channel_invert.append(False)
            self._channel_probe_id.append("NONE")
            self._channel_bw_limit.append(False)

        # digital channels
        self._digital_channel_name = list()
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("d%d" % i)
                self._channel_label.append("")
                self._digital_channel_name.append("d%d" % i)

            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_impedance[i] = 100000
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'dc'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1

        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)
        self._channel_name_dict = ivi.get_index_dict(self._channel_name)

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            esr = self._ask("*esr?")
            error_code, error_message = self._ask("evmsg?").split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (error_code, error_message)

    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            self._write("diag:select all")
            self._write("diag:loop:option once")
            self._write("diag:state execute")
            # wait for test to complete
            res = ''
            while 1:
                res = self._ask("diag:result:flag?").strip('"').lower()
                if res != 'in progress':
                    break
                time.sleep(5)
            code = 0 if res == 'pass' else 1
            if code != 0:
                message = "Self test failed"
        return (code, message)

    def _system_display_string(self, string = None):
        if string is None:
            string = ""

        if not self._driver_operation_simulate:
            self._write(":message:show \"%s\"" % string)
            self._write(":message:state 1")

    def _display_fetch_screenshot(self, format='png', invert=False):
        if self._driver_operation_simulate:
            return b''

        if format not in self._display_screenshot_image_format_mapping:
            raise ivi.ValueNotSupportedException()

        format = self._display_screenshot_image_format_mapping[format]

        self._write(":hardcopy:inksaver %d" % int(bool(invert)))
        self._write(":save:image:fileformat %s" % format)
        self._write(":hardcopy start")

        return self._read_raw()

    def _get_timebase_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            if int(self._ask(":zoom:state?")):
                self._timebase_mode = "window"
            elif self._ask(":display:xy?") == "TRIGGERED":
                self._timebase_mode = "xy"
            else:
                self._timebase_mode = "main"
            self._set_cache_valid()
        return self._timebase_mode

    def _set_timebase_mode(self, value):
        if value not in TimebaseModeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            if value == 'window':
                self._write(":display:xy off")
                self._write(":zoom:state 1")
            elif value == 'xy':
                self._write(":zoom:state 0")
                self._write(":display:xy triggered")
            else:
                self._write(":zoom:state 0")
                self._write(":display:xy off")
        self._timebase_mode = value
        self._set_cache_valid()

    def _get_timebase_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_position = float(self._ask(":horizontal:delay:time?"))
            self._set_cache_valid()
        return self._timebase_position

    def _set_timebase_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":horizontal:delay:mode 1")
            self._write(":horizontal:delay:time %e" % value)
        self._timebase_position = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'acquisition_start_time')
        self._set_cache_valid(False, 'timebase_window_position')

    def _get_timebase_range(self):
        return self._get_timebase_scale() * self._horizontal_divisions

    def _set_timebase_range(self, value):
        value = float(value)
        self._set_timebase_scale(value / self._horizontal_divisions)

    def _get_timebase_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask(":horizontal:scale?"))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
        return self._timebase_scale

    def _set_timebase_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":horizontal:scale %e" % value)
        self._timebase_scale = value
        self._timebase_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(False, 'timebase_window_range')

    def _get_timebase_window_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_position = (float(self._ask(":zoom:zoom1:position?"))-50) / 100 * self._get_timebase_range() + self._get_timebase_position()
            self._set_cache_valid()
        return self._timebase_window_position

    def _set_timebase_window_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":zoom:zoom1:position %e" % (((value - self._get_timebase_position()) / self._get_timebase_range() * 100) + 50))
        self._timebase_window_position = value
        self._set_cache_valid()

    def _get_timebase_window_range(self):
        return self._get_timebase_window_scale() * self._horizontal_divisions

    def _set_timebase_window_range(self, value):
        value = float(value)
        self._set_timebase_window_scale(value / self._horizontal_divisions)

    def _get_timebase_window_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_window_scale = float(self._ask(":zoom:zoom1:scale?"))
            self._timebase_window_range = self._timebase_window_scale * self._horizontal_divisions
            self._set_cache_valid()
        return self._timebase_window_scale

    def _set_timebase_window_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":zoom:zoom1:scale %e" % value)
        self._timebase_window_scale = value
        self._timebase_window_range = value * self._horizontal_divisions
        self._set_cache_valid()

    def _get_display_vectors(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_vectors = not bool(int(self._ask(":display:style:dotsonly?")))
            self._set_cache_valid()
        return self._display_vectors

    def _set_display_vectors(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":display:style:dotsonly %d" % int(not value))
        self._display_vectors = value
        self._set_cache_valid()

    def _display_clear(self):
        if not self._driver_operation_simulate:
            self._write(":message:state 0")
            self._write(":display:persistence clear")

    def _get_acquisition_start_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_start_time = float(self._ask(":horizontal:delay:time?")) - self._get_acquisition_time_per_record() / 2
            self._set_cache_valid()
        return self._acquisition_start_time

    def _set_acquisition_start_time(self, value):
        value = float(value)
        value = value + self._get_acquisition_time_per_record() / 2
        if not self._driver_operation_simulate:
            self._write(":horizontal:delay:time %e" % value)
        self._acquisition_start_time = value
        self._set_cache_valid()

    def _get_acquisition_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":acquire:mode?").lower()
            self._acquisition_type = [k for k,v in AcquisitionTypeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._acquisition_type

    def _set_acquisition_type(self, value):
        if value not in AcquisitionTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":acquire:mode %s" % AcquisitionTypeMapping[value])
        self._acquisition_type = value
        self._set_cache_valid()

    def _get_acquisition_number_of_points_minimum(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_number_of_points_minimum = int(self._ask(":horizontal:recordlength?"))
            self._set_cache_valid()
        return self._acquisition_number_of_points_minimum

    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        # coerce value?
        if not self._driver_operation_simulate:
            self._write(":horizontal:recordlength %d" % value)
        self._acquisition_number_of_points_minimum = value
        self._set_cache_valid()

    def _get_acquisition_record_length(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_record_length = int(self._ask(":horizontal:recordlength?"))
            self._set_cache_valid()
        return self._acquisition_record_length

    def _get_acquisition_time_per_record(self):
        return self._get_timebase_range()

    def _set_acquisition_time_per_record(self, value):
        self._set_timebase_range(value)

    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask(":%s:label?" % self._channel_name[index]).strip('"')
            self._set_cache_valid(index=index)
        return self._channel_label[index]

    def _set_channel_label(self, index, value):
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write(":%s:label \"%s\"" % (self._channel_name[index], value))
        self._channel_label[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_enabled[index] = bool(int(self._ask(":select:%s?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_enabled[index]

    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write(":select:%s %d" % (self._channel_name[index], int(value)))
        self._channel_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_input_impedance[index] = float(self._ask(":%s:termination?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_input_impedance[index]

    def _set_channel_input_impedance(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if value != 50 and value != 1000000:
            raise Exception('Invalid impedance selection')
        if not self._driver_operation_simulate:
            self._write(":%s:termination %f" % (self._channel_name[index], value))
        self._channel_input_impedance[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_input_frequency_max(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_input_frequency_max[index] = float(self._ask(":%s:bandwidth?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_input_frequency_max[index]

    def _set_channel_input_frequency_max(self, index, value):
        value = float(value)
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._write(":%s:bandwidth %e" % (self._channel_name[index], value))
        self._channel_input_frequency_max[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_attenuation[index] = 1/float(self._ask(":%s:probe:gain?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_attenuation[index]

    def _set_channel_probe_attenuation(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = 1/float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:probe:gain %e" % (self._channel_name[index], value))
        self._channel_probe_attenuation[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, 'channel_offset', index)
        self._set_cache_valid(False, 'channel_scale', index)

    def _get_channel_probe_skew(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_skew[index] = float(self._ask(":%s:deskew?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_skew[index]

    def _set_channel_probe_skew(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:deskew %e" % (self._channel_name[index], value))
        self._channel_probe_skew[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_invert(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_invert[index] = bool(int(self._ask(":%s:invert?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_invert[index]

    def _set_channel_invert(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:invert %e" % (self._channel_name[index], int(value)))
        self._channel_invert[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_probe_id(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_id[index] = self._ask(":%s:probe:id?" % self._channel_name[index])
            self._set_cache_valid(index=index)
        return self._channel_probe_id[index]

    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_coupling[index] = self._ask(":%s:coupling?" % self._channel_name[index]).lower()
            self._set_cache_valid(index=index)
        return self._channel_coupling[index]

    def _set_channel_coupling(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in VerticalCoupling:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":%s:coupling %s" % (self._channel_name[index], value))
        self._channel_coupling[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_offset[index] = -float(self._ask(":%s:position?" % self._channel_name[index])) * self._get_channel_scale(index)
            self._set_cache_valid(index=index)
        return self._channel_offset[index]

    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:position %e" % (self._channel_name[index], -value / self._get_channel_scale(index)))
        self._channel_offset[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_range(self, index):
        return self._get_channel_scale(index) * self._vertical_divisions

    def _set_channel_range(self, index, value):
        value = float(value)
        self._set_channel_scale(index, value / self._vertical_divisions)

    def _get_channel_scale(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_scale[index] = float(self._ask(":%s:scale?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_scale[index]

    def _set_channel_scale(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:scale %e" % (self._channel_name[index], value))
        self._channel_scale[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, "channel_offset", index)
    
    def _get_channel_trigger_level(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_trigger_level[index] = float(self._ask(":trigger:a:level:%s?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_trigger_level[index]

    def _set_channel_trigger_level(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:a:level:%s %e" % (self._channel_name[index], value))
        self._channel_trigger_level[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, "trigger_level")

    def _get_measurement_status(self):
        if not self._driver_operation_simulate:
            if int(self._ask(":acquire:numacq?")) > 0:
                return "complete"
            elif int(self._ask(":acquire:state?")) > 0:
                return "in_progress"
            else:
                return "unknown"
        return self._measurement_status

    def _get_trigger_coupling(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:edge:coupling?").lower()
            self._trigger_coupling = [k for k,v in TriggerCouplingMapping.items() if v==value][0]
        return self._trigger_coupling

    def _set_trigger_coupling(self, value):
        if value not in TriggerCouplingMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:edge:coupling %s" % TriggerCouplingMapping[value])
        self._trigger_coupling = value
        self._set_cache_valid()

    def _get_trigger_holdoff(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_holdoff = float(self._ask(":trigger:a:holdoff?"))
            self._set_cache_valid()
        return self._trigger_holdoff

    def _set_trigger_holdoff(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:a:holdoff %e" % value)
        self._trigger_holdoff = value
        self._set_cache_valid()

    def _get_trigger_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            ch = self._get_trigger_source()
            try:
                self._trigger_level = self._get_channel_trigger_level(ch)
                self._set_cache_valid()
            except:
                pass
        return self._trigger_level

    def _set_trigger_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            ch = self._get_trigger_source()
            self._set_channel_trigger_level(ch, value)
        self._trigger_level = value
        self._set_cache_valid()

    def _get_trigger_edge_slope(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:edge:slope?").lower()
            self._trigger_edge_slope = [k for k,v in SlopeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_edge_slope

    def _set_trigger_edge_slope(self, value):
        if value not in SlopeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:edge:slope %s" % SlopeMapping[value])
        self._trigger_edge_slope = value
        self._set_cache_valid()

    def _get_trigger_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            t = self._ask(":trigger:a:type?").lower()
            if t == 'edge':
                value = self._ask(":trigger:a:edge:source?").lower()
            elif t == 'logic':
                # TODO
                value = ''
            elif t == 'pulse':
                pc = self._ask(":trigger:a:pulse:class?").lower()
                if pc == 'runt':
                    value = self._ask(":trigger:a:runt:source?").lower()
                elif pc == 'width':
                    value = self._ask(":trigger:a:pulsewidth:source?").lower()
                elif pc == 'transition':
                    value = self._ask(":trigger:a:transition:source?").lower()
                elif pc == 'timeout':
                    value = self._ask(":trigger:a:timeout:source?").lower()
            elif t == 'bus':
                # TODO
                value = ''
            elif t == 'video':
                value = self._ask(":trigger:a:video:source?").lower()
            # TODO process value
            self._trigger_source = value
            self._set_cache_valid()
        return self._trigger_source

    def _set_trigger_source(self, value):
        if hasattr(value, 'name'):
            value = value.name
        value = str(value)
        if value not in self._channel_name:
            raise ivi.UnknownPhysicalNameException()
        if not self._driver_operation_simulate:
            t = self._ask(":trigger:a:type?").lower()
            if t == 'edge':
                self._write(":trigger:a:edge:source %s" % value)
            elif t == 'logic':
                # TODO
                pass
            elif t == 'pulse':
                pc = self._ask(":trigger:a:pulse:class?").lower()
                if pc == 'runt':
                    self._write(":trigger:a:runt:source %s" % value)
                elif pc == 'width':
                    self._write(":trigger:a:pulsewidth:source %s" % value)
                elif pc == 'transition':
                    self._write(":trigger:a:transition:source %s" % value)
                elif pc == 'timeout':
                    self._write(":trigger:a:timeout:source %s" % value)
            elif t == 'bus':
                # TODO
                pass
            elif t == 'video':
                self._write(":trigger:a:video:source %s" % value)
            #self._write(":trigger:source %s" % value)
        self._trigger_source = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'trigger_level')
        self._set_cache_valid(False, 'trigger_runt_threshold_high')
        self._set_cache_valid(False, 'trigger_runt_threshold_low')
        for i in range(self._analog_channel_count): self._set_cache_valid(False, 'channel_trigger_level', i)

    def _get_trigger_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:type?").lower()
            if value == 'edge':
                src = self._ask(":trigger:a:edge:source?").lower()
                if src == 'line':
                    value = 'ac_line'
            elif value == 'logic':
                # TODO
                value = 'logic'
            elif value == 'pulse':
                pc = self._ask(":trigger:a:pulse:class?").lower()
                if pc == 'width':
                    wh = self._ask(":trigger:a:pulsewidth:when?").lower()
                    if wh in GlitchConditionMapping.values():
                        value = 'glitch'
                    else:
                        value = 'width'
                else:
                    value = pc
            elif value == 'bus':
                # TODO
                value = 'bus'
            elif value == 'video':
                value = 'tv'
            #else:
            #    value = [k for k,v in TriggerTypeMapping.items() if v==value][0]
            self._trigger_type = value
            self._set_cache_valid()
        return self._trigger_type

    def _set_trigger_type(self, value):
        if value not in TriggerTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:type %s" % TriggerTypeMapping[value])
            if value == 'ac_line':
                self._write(":trigger:a:edge:source line")
            elif value in ['runt', 'width', 'glitch', 'transition', 'timeout']:
                self._write(":trigger:a:pulse:class %s" % value)
                print(value)
                if value == 'glitch':
                    t = self._ask(":trigger:a:pulsewidth:when?").lower()
                    if t not in GlitchConditionMapping.values():
                        self._write(":trigger:a:pulsewidth:when %s" % GlitchConditionMapping[self._trigger_glitch_condition])
                elif value == 'width':
                    t = self._ask(":trigger:a:pulsewidth:when?").lower()
                    if t not in WidthConditionMapping.values():
                        self._write(":trigger:a:pulsewidth:when %s" % WidthConditionMapping[self._trigger_width_condition])
        self._trigger_type = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'trigger_source')
        self._set_cache_valid(False, 'trigger_level')

    def _measurement_abort(self):
        pass

    def _get_trigger_tv_trigger_event(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:video:sync?").lower()
            # may need processing
            self._trigger_tv_trigger_event = [k for k,v in TVTriggerEventMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_tv_trigger_event

    def _set_trigger_tv_trigger_event(self, value):
        if value not in TVTriggerEventMapping:
            raise ivi.ValueNotSupportedException()
        # may need processing
        if not self._driver_operation_simulate:
            self._write(":trigger:a:video:sync %s" % TVTriggerEventMapping[value])
        self._trigger_tv_trigger_event = value
        self._set_cache_valid()

    def _get_trigger_tv_line_number(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = int(self._ask(":trigger:a:video:line?"))
            # may need processing
            self._trigger_tv_line_number = value
            self._set_cache_valid()
        return self._trigger_tv_line_number

    def _set_trigger_tv_line_number(self, value):
        value = int(value)
        # may need processing
        if not self._driver_operation_simulate:
            self._write(":trigger:a:video:line %e" % value)
        self._trigger_tv_line_number = value
        self._set_cache_valid()

    def _get_trigger_tv_polarity(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:video:polarity?").lower()
            self._trigger_tv_polarity = [k for k,v in PolarityMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_tv_polarity

    def _set_trigger_tv_polarity(self, value):
        if value not in PolarityMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:video:polarity %s" % PolarityMapping[value])
        self._trigger_tv_polarity = value
        self._set_cache_valid()

    def _get_trigger_tv_signal_format(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:video:standard?").lower()
            self._trigger_tv_signal_format = [k for k,v in TVTriggerFormatMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_tv_signal_format

    def _set_trigger_tv_signal_format(self, value):
        if value not in TVTriggerFormatMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:video:standard %s" % TVTriggerFormatMapping[value])
        self._trigger_tv_signal_format = value
        self._set_cache_valid()

    def _get_trigger_runt_threshold_high(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            ch = self._ask(":trigger:a:runt:source?")
            self._trigger_runt_threshold_high = float(self._ask(":trigger:a:upperthreshold:%s?" % ch))
            self._set_cache_valid()
        return self._trigger_runt_threshold_high

    def _set_trigger_runt_threshold_high(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            ch = self._get_trigger_source()
            self._write(":trigger:a:upperthreshold:%s %e" % (ch, value))
        self._trigger_runt_threshold_high = value
        self._set_cache_valid()

    def _get_trigger_runt_threshold_low(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            ch = self._ask(":trigger:a:runt:source?")
            self._trigger_runt_threshold_low = float(self._ask(":trigger:a:lowerthreshold:%s?" % ch))
            self._set_cache_valid()
        return self._trigger_runt_threshold_low

    def _set_trigger_runt_threshold_low(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            ch = self._get_trigger_source()
            self._write(":trigger:a:lowerthreshold:%s %e" % (ch, value))
        self._trigger_runt_threshold_low = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'trigger_level')
        for i in range(self._analog_channel_count): self._set_cache_valid(False, 'channel_trigger_level', i)

    def _get_trigger_runt_polarity(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:runt:polarity?").lower()
            self._trigger_runt_polarity = [k for k,v in PolarityMapping3.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_runt_polarity

    def _set_trigger_runt_polarity(self, value):
        if value not in PolarityMapping3:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:runt:polarity %s" % PolarityMapping3[value])
        self._trigger_runt_polarity = value
        self._set_cache_valid()

    # TODO: need runt condition and width

    def _get_trigger_glitch_condition(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:pulsewidth:when?").lower()
            if value in GlitchConditionMapping.values():
                self._trigger_glitch_condition = [k for k,v in GlitchConditionMapping.items() if v==value][0]
                self._set_cache_valid()
        return self._trigger_glitch_condition

    def _set_trigger_glitch_condition(self, value):
        if value not in GlitchConditionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:pulsewidth:when %s" % GlitchConditionMapping[value])
        self._trigger_glitch_condition = value
        self._set_cache_valid()

    def _get_trigger_glitch_polarity(self):
        return self._get_trigger_width_polarity()

    def _set_trigger_glitch_polarity(self, value):
        self._set_trigger_width_polarity(value)

    def _get_trigger_glitch_width(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_glitch_width = float(self._ask(":trigger:a:pulsewidth:width?"))
            self._set_cache_valid()
        return self._trigger_glitch_width

    def _set_trigger_glitch_width(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:a:pulsewidth:width %e" % value)
        self._trigger_glitch_width = value
        self._set_cache_valid()

    def _get_trigger_width_condition(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:pulsewidth:when?").lower()
            if value in WidthConditionMapping.values():
                self._trigger_width_condition = [k for k,v in WidthConditionMapping.items() if v==value][0]
                self._set_cache_valid()
        return self._trigger_width_condition

    def _set_trigger_width_condition(self, value):
        if value not in WidthConditionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:pulsewidth:when %s" % WidthConditionMapping[value])
        self._trigger_width_condition = value
        self._set_cache_valid()

    def _get_trigger_width_threshold_high(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_width_threshold_high = float(self._ask(":trigger:a:pulsewidth:highlimit?"))
            self._set_cache_valid()
        return self._trigger_width_threshold_high

    def _set_trigger_width_threshold_high(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:a:pulsewidth:highlimit %e" % value)
        self._trigger_width_threshold_high = value
        self._set_cache_valid()

    def _get_trigger_width_threshold_low(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_width_threshold_low = float(self._ask(":trigger:a:pulsewidth:lowlimit?"))
            self._set_cache_valid()
        return self._trigger_width_threshold_low

    def _set_trigger_width_threshold_low(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":trigger:a:pulsewidth:lowlimit %e" % value)
        self._trigger_width_threshold_low = value
        self._set_cache_valid()

    def _get_trigger_width_polarity(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:pulsewidth:polarity?").lower()
            self._trigger_width_polarity = [k for k,v in PolarityMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_width_polarity

    def _set_trigger_width_polarity(self, value):
        if value not in PolarityMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:pulsewidth:polarity %s" % PolarityMapping[value])
        self._trigger_width_polarity = value
        self._set_cache_valid()

    def _get_trigger_ac_line_slope(self):
        return self._get_trigger_edge_slope()

    def _set_trigger_ac_line_slope(self, value):
        self._set_trigger_edge_slope(value)

    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)

        if self._driver_operation_simulate:
            return ivi.TraceYT()

        self._write(":data:source %s" % self._channel_name[index])
        self._write(":data:encdg fastest")
        self._write(":data:width 2")
        self._write(":data:start 1")
        self._write(":data:stop 1e10")

        trace = ivi.TraceYT()

        # Read preamble
        # The order and number of values returned by "WFMOutpre?" seem not to
        # be consistent across different oscilloscopes (even not complying with
        # the programmer's manual), so we explicitly give the order we want.
        pre = self._ask(';'.join(
                (':WFMOutpre:PT_Fmt?',
                 ':WFMOutpre:NR_Pt?',
                 ':WFMOutpre:BYT_Nr?',
                 ':WFMOutpre:ENCdg?',
                 ':WFMOutpre:BN_Fmt?',
                 ':WFMOutpre:BYT_Or?',
                 ':WFMOutpre:XINcr?',
                 ':WFMOutpre:XZEro?',
                 ':WFMOutpre:PT_OFF?',
                 ':WFMOutpre:YMUlt?',
                 ':WFMOutpre:YOFf?',
                 ':WFMOutpre:YZEro?',
                 ))).split(';')

        acq_format = pre[0].strip().upper()         # PT_Fmt
        points = int(pre[1])                        # NR_Pt
        point_size = int(pre[2])                    # BYT_Nr
        point_enc = pre[3].strip().upper()          # ENCdg
        point_fmt = pre[4].strip().upper()          # BN_Fmt
        byte_order = pre[5].strip().upper()         # BYT_Or
        trace.x_increment = float(pre[6])           # XINcr
        trace.x_origin = float(pre[7])              # XZEro
        trace.x_reference = int(float(pre[8]))      # PT_OFF
        trace.y_increment = float(pre[9])           # YMUlt
        trace.y_reference = int(float(pre[10]))     # YOFf
        trace.y_origin = float(pre[11])             # YZEro

        if acq_format != 'Y':
            raise UnexpectedResponseException()

        if point_enc != 'BINARY':
            raise UnexpectedResponseException()

        # Read waveform data
        raw_data = self._ask_for_ieee_block(":curve?")
        self._read_raw() # flush buffer

        # Store in trace object
        if point_fmt == 'RP' and point_size == 1:
            trace.y_raw = array.array('B', raw_data[0:points*2])
        elif point_fmt == 'RP' and point_size == 2:
            trace.y_raw = array.array('H', raw_data[0:points*2])
        elif point_fmt == 'RI' and point_size == 1:
            trace.y_raw = array.array('b', raw_data[0:points*2])
        elif point_fmt == 'RI' and point_size == 2:
            trace.y_raw = array.array('h', raw_data[0:points*2])
        elif point_fmt == 'FP' and point_size == 4:
            trace.y_increment = 1
            trace.y_reference = 0
            trace.y_origin = 0
            trace.y_raw = array.array('f', raw_data[0:points*4])
        else:
            raise UnexpectedResponseException()

        if (byte_order == 'LSB') != (sys.byteorder == 'little'):
            trace.y_raw.byteswap()

        return trace

    def _measurement_read_waveform(self, index, maximum_time):
        return self._measurement_fetch_waveform(index)

    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write(":acquire:stopafter sequence")
            self._write(":acquire:state run")
            self._set_cache_valid(False, 'trigger_continuous')

    def _get_reference_level_high(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._reference_level_high = float(self._ask(":measurement:reflevel:percent:high?"))
            self._set_cache_valid()
        return self._reference_level_high

    def _set_reference_level_high(self, value):
        value = float(value)
        if value < 0: value = 0
        if value > 100: value = 100
        if not self._driver_operation_simulate:
            self._write(":measurement:reflevel:method percent")
            self._write(":measurement:reflevel:percent:high %e" % value)
        self._reference_level_high = value
        self._set_cache_valid()

    def _get_reference_level_low(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._reference_level_low = float(self._ask(":measurement:reflevel:percent:low?"))
            self._set_cache_valid()
        return self._reference_level_low

    def _set_reference_level_low(self, value):
        value = float(value)
        if value < 0: value = 0
        if value > 100: value = 100
        if not self._driver_operation_simulate:
            self._write(":measurement:reflevel:method percent")
            self._write(":measurement:reflevel:percent:low %e" % value)
        self._reference_level_low = value
        self._set_cache_valid()

    def _get_reference_level_middle(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._reference_level_middle = float(self._ask(":measurement:reflevel:percent:mid1?"))
            self._set_cache_valid()
        return self._reference_level_middle

    def _set_reference_level_middle(self, value):
        value = float(value)
        if value < 0: value = 0
        if value > 100: value = 100
        if not self._driver_operation_simulate:
            self._write(":measurement:reflevel:method percent")
            self._write(":measurement:reflevel:percent:mid1 %e" % value)
            self._write(":measurement:reflevel:percent:mid2 %e" % value)
        self._reference_level_middle = value
        self._set_cache_valid()

    def _measurement_fetch_waveform_measurement(self, index, measurement_function, ref_channel = None):
        index = ivi.get_index(self._channel_name, index)
        if index < self._analog_channel_count:
            if measurement_function not in MeasurementFunctionMapping:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMapping[measurement_function]
        else:
            if measurement_function not in MeasurementFunctionMappingDigital:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMappingDigital[measurement_function]
        if not self._driver_operation_simulate:
            self._write(":measurement:immed:type %s" % func)
            self._write(":measurement:immed:source1 %s" % self._channel_name[index])
            if measurement_function in ['ratio', 'phase', 'delay']:
                if hasattr(ref_channel, 'name'):
                    ref_channel = ref_channel.name
                ref_index = ivi.get_index(self._channel_name, ref_channel)
                self._write(":measurement:immed:source2 %s" % self._channel_name[ref_index])
            return float(self._ask(":measurement:immed:value?"))
        return 0

    def _measurement_read_waveform_measurement(self, index, measurement_function, maximum_time):
        return self._measurement_fetch_waveform_measurement(index, measurement_function)

    def _get_acquisition_number_of_envelopes(self):
        return self._acquisition_number_of_envelopes

    def _set_acquisition_number_of_envelopes(self, value):
        self._acquisition_number_of_envelopes = value

    def _measurement_fetch_waveform_min_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        data = list()
        return data

    def _measurement_read_waveform_min_max(self, index, maximum_time):
        return self._measurement_fetch_waveform_min_max(index)

    def _get_trigger_continuous(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_continuous = self._ask(":acquire:stopafter?").lower() == 'runstop'
            self._set_cache_valid()
        return self._trigger_continuous

    def _set_trigger_continuous(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            if value:
                self._write(":acquire:stopafter runstop")
                self._write(":acquire:state run")
            else:
                self._write(":acquire:stopafter sequence")
        self._trigger_continuous = value
        self._set_cache_valid()

    def _get_acquisition_number_of_averages(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_number_of_averages = int(self._ask(":acquire:numavg?"))
            self._set_cache_valid()
        return self._acquisition_number_of_averages

    def _set_acquisition_number_of_averages(self, value):
        if value not in [2, 4, 8, 16, 32, 64, 128, 256, 512]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":acquire:numavg %d" % value)
        self._acquisition_number_of_averages = value
        self._set_cache_valid()
    
    def _get_trigger_modifier(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":trigger:a:mode?").lower()
            self._trigger_modifier = [k for k,v in TriggerModifierMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_modifier

    def _set_trigger_modifier(self, value):
        if value not in TriggerModifierMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":trigger:a:mode %s" % TriggerModifierMapping[value])
        self._trigger_modifier = value
        self._set_cache_valid()

    def _measurement_auto_setup(self):
        if not self._driver_operation_simulate:
            self._write(":autoset execute")

