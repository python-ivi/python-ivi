"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2017 Jonas Långbacka

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
from .. import scope
from .. import scpi
from .. import extra

AcquisitionTypeMapping = {
        'normal': ['samp', 'off'],
        'peak_detect': ['pdet', 'off'],
        'high_resolution': ['hres', 'off'],
        'average': ['samp','aver'],
        'envelope': ['samp', 'env'],
        'envelope_peak_detect': ['pdet', 'env']}
BandwidthMapping = {
        6e9:   'full',
        800e6: 'b800',
        200e6: 'b200',
        20e6:  'b20'}
VerticalCoupling = set(['ac', 'dc'])
TriggerTypeMapping = {
        'edge': 'edge',
        'width': 'glit',
        'glitch': 'glit',
        'tv': 'tv',
        #'immediate': '',
        'ac_line': 'edge',
        'pattern': 'patt',
        'can': 'can',
        'duration': 'dur',
        'i2s': 'i2s',
        'iic': 'iic',
        'eburst': 'ebur',
        'lin': 'lin',
        'm1553': 'm1553',
        'sequence': 'seq',
        'spi': 'spi',
        'uart': 'uart',
        'usb': 'usb',
        'flexray': 'flex'}
TriggerCouplingMapping = {
        'ac': ('ac', 0, 0),
        'dc': ('dc', 0, 0),
        'hf_reject': ('dc', 0, 1),
        'lf_reject': ('lfr', 0, 0),
        'noise_reject': ('dc', 1, 0),
        'hf_reject_ac': ('ac', 0, 1),
        'noise_reject_ac': ('ac', 1, 0),
        'hf_noise_reject': ('dc', 1, 1),
        'hf_noise_reject_ac': ('ac', 1, 1),
        'lf_noise_reject': ('lfr', 1, 0)}
TVTriggerEventMapping = {'field1': 'fie1',
        'field2': 'fie2',
        'any_field': 'afi',
        'any_line': 'alin',
        'line_number': 'lfi1',
        'vertical': 'vert',
        'line_field1': 'lfi1',
        'line_field2': 'lfi2',
        'line': 'line',
        'line_alternate': 'lalt',
        'lvertical': 'lver'}
TVTriggerFormatMapping = {'generic': 'gen',
        'ntsc': 'ntsc',
        'pal': 'pal',
        'palm': 'palm',
        'secam': 'sec',
        'p480l60hz': 'p480',
        'p480': 'p480',
        'p720l60hz': 'p720',
        'p720': 'p720',
        'p1080l24hz': 'p1080',
        'p1080': 'p1080',
        'p1080l25hz': 'p1080l25hz',
        'p1080l50hz': 'p1080l50hz',
        'p1080l60hz': 'p1080l60hz',
        'i1080l50hz': 'i1080l50hz',
        'i1080': 'i1080l50hz',
        'i1080l60hz': 'i1080l60hz'}
PolarityMapping = {'positive': 'pos',
        'negative': 'neg'}
GlitchConditionMapping = {'less_than': 'less',
        'greater_than': 'gre'}
WidthConditionMapping = {'within': 'rang'}
SampleModeMapping = {'real_time': 'rtim',
        'equivalent_time': 'etim',
        'segmented': 'segm'}
SlopeMapping = {
        'positive': 'pos',
        'negative': 'neg',
        'either': 'eith',
        'alternating': 'alt'}
MeasurementFunctionMapping = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'voltage_rms': 'vrms display',
        'voltage_peak_to_peak': 'vpp',
        'voltage_max': 'vmax',
        'voltage_min': 'vmin',
        'voltage_high': 'vtop',
        'voltage_low': 'vbase',
        'voltage_average': 'vaverage display',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle',
        'amplitude': 'vamplitude',
        'voltage_cycle_rms': 'vrms cycle',
        'voltage_cycle_average': 'vaverage cycle',
        'overshoot': 'overshoot',
        'preshoot': 'preshoot',
        'ratio': 'vratio',
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
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'bmp8': 'bmp8bit',
        'png': 'png',
        'png24': 'png'}
TimebaseModeMapping = {
        'main': 'main',
        'window': 'wind',
        'xy': 'xy',
        'roll': 'roll'}
TimebaseReferenceMapping = {
        'left': 8.33,
        'center': 50.0,
        'right': 91.67}
TriggerModifierMapping = {'none': 'normal', 'auto': 'auto'}

class rohdeschwarzBaseScope(scope.Base,
                            ivi.Driver):
#                       scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset,
#                       scpi.common.SelfTest, scpi.common.Memory,
#                       scope.Base, scope.TVTrigger,
#                       scope.GlitchTrigger, scope.WidthTrigger, scope.AcLineTrigger,
#                       scope.WaveformMeasurement, scope.MinMaxWaveform,
#                       scope.ContinuousAcquisition, scope.AverageAcquisition,
#                       scope.SampleMode, scope.TriggerModifier, scope.AutoSetup,
#                       extra.common.SystemSetup, extra.common.Screenshot,
#                       ivi.Driver):
    "Rohde&Schwarz generic IVI oscilloscope driver"
    
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
        
        super(rohdeschwarzBaseScope, self).__init__(*args, **kwargs)
        
        self._self_test_delay = 40
        self._memory_size = 10
        
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9

        self._horizontal_divisions = 12
        self._vertical_divisions = 10

        self._acquisition_segmented_count = 2
        self._acquisition_segmented_index = 1
        self._acquisition_number_of_points_minimum = 10e3
        self._acquisition_record_length = 20e3
        self._acquisition_record_length_automatic = True

        self._timebase_mode = 'main'
        self._timebase_scale = 100e-6
        self._timebase_position = 0.0
        self._timebase_reference = 'center'
        self._timebase_range = 1.2e-3
        self._timebase_window_position = 0.0
        self._timebase_window_range = 600e-6
        self._timebase_window_scale = 50e-6
        self._display_screenshot_image_format_mapping = ScreenshotImageFormatMapping
        self._display_vectors = True
        self._display_labels = True

        self._identity_description = "Rohde&Schwarz generic IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Rohde&Schwarz"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = ['RTB2002', 'RTB2004',
                                                      'RTO2002', 'RTO2004', 'RTO2012', 'RTO2014', 'RTO2022', 'RTO2024', 'RTO2032', 'RTO2034',
                                                      'RTO2044', 'RTO2064']

        self._add_property('timebase.scale',
                        self._get_timebase_scale,
                        self._set_timebase_scale,
                        None,
                        ivi.Doc("""
                        Sets the horizontal scale or units per division for all channels and math waveforms.
                        """))

        self._add_property('timebase.position',
                        self._get_timebase_position,
                        self._set_timebase_position,
                        None,
                        ivi.Doc("""
                        Defines the trigger position, the time distance from the trigger point to the reference point (trigger offset). The trigger
                        point is the zero point of the diagram. Changing the horizontal position, you can move the trigger, even outside the screen.
                        """))

        self._add_property('timebase.reference',
                        self._get_timebase_reference,
                        self._set_timebase_reference,
                        None,
                        ivi.Doc("""
                        Defines the time reference point in the diagram. The reference point is the rescaling center of the time scale on the screen.
                        If you modify the time scale, the reference point remains fixed on the screen, and the scale is stretched or compressed to
                        both sides of the reference point. The reference point defines which part of the waveform is shown. By default, the reference
                        point is displayed in the center of the window, and you can move it to the left or right.
                        
                        Values:
                        * 'left'
                        * 'center'
                        * 'right'
                        """))

        self._add_property('timebase.acquisition_time',
                        self._get_timebase_acquisition_time,
                        self._set_timebase_acquisition_time,
                        None,
                        ivi.Doc("""
                        Defines the time of one acquisition, that is the time across the 12 divisions of the diagram:
                        timebase.acquisition_time = timebase.horizontal_divisions * timebase.scale
                        """))

        self._add_property('timebase.range',
                        self._get_timebase_range,
                        self._set_timebase_range,
                        None,
                        ivi.Doc("""
                        Sets the full-scale horizontal time in seconds for the main window. The
                        range is 12 times the current time-per-division setting.
                        """))

        self._add_property('timebase.real_acquisition_time',
                        self._get_timebase_real_acquisition_time,
                        None,
                        ivi.Doc("""
                        Queries the real acquisition time used in the hardware. If FFT analysis is performed, the value can differ from the adjusted
                        acquisition time (timebase.acquisition_time).
                        """))

        self._add_property('timebase.divisions',
                        self._get_timebase_divisions,
                        None,
                        ivi.Doc("""
                        Queries the number of horizontal divisions on the screen.
                        """))

        self._add_property('acquisition.record_length_automatic',
                        self._get_acquisition_record_length_automatic,
                        self._set_acquisition_record_length_automatic,
                        None,
                        ivi.Doc("""
                        Enables or disables the automatic record length. The instrument sets a value that fits to the selected timebase.
                        """))


        self._init_channels()

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        self._channel_count = self._analog_channel_count + self._digital_channel_count

        super(rohdeschwarzBaseScope, self)._initialize(resource, id_query, reset, **keywargs)

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
            super(rohdeschwarzBaseScope, self)._init_channels()
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
            self._channel_name.append("channel%d" % (i+1))
            self._channel_label.append("%d" % (i+1))
            self._analog_channel_name.append("C%d" % (i+1))
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
                self._channel_name.append("digital%d" % i)
                self._channel_label.append("D%d" % i)
                self._digital_channel_name.append("digital%d" % i)
            
            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_impedance[i] = 100000
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'dc'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)


    def _get_timebase_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask("timebase:scale?"))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_range')
        return self._timebase_scale

    def _set_timebase_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("timebase:scale %e" % value)
        self._timebase_scale = value
        self._timebase_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_range')
        self._set_cache_valid(False, 'timebase_window_scale')
        self._set_cache_valid(False, 'timebase_window_range')

    def _get_timebase_position(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_position = float(self._ask("timebase:position?"))
            self._set_cache_valid()
        return self._timebase_position

    def _set_timebase_position(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("timebase:position %e" % value)
        self._timebase_position = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'timebase_window_position')

    def _get_timebase_reference(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = float(self._ask("timebase:reference?"))
            print(value)
            self._timebase_reference = [k for k,v in TimebaseReferenceMapping.items() if v==value][0] # What to do for arbitrary reference values?
            self._set_cache_valid()
        return self._timebase_reference
    
    def _set_timebase_reference(self, value):
        if value not in TimebaseReferenceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("timebase:reference %s" % TimebaseReferenceMapping[value])
        self._timebase_reference = value
        self._set_cache_valid()

    def _get_timebase_acquisition_time(self):
        return self._get_timebase_range()

    def _set_timebase_acquisition_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("timebase:acqtime %e" % value)
        self._timebase_acquisition_time = value
        self._timebase_range = value / self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_range')
        self._set_cache_valid(False, 'timebase_window_scale')
        self._set_cache_valid(False, 'timebase_window_range')

    def _get_timebase_range(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_range = float(self._ask("timebase:range?"))
            self._timebase_scale = self._timebase_range / self._horizontal_divisions
            self._set_cache_valid()
            self._set_cache_valid(True, 'timebase_scale')
        return self._timebase_range

    def _set_timebase_range(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("timebase:range %e" % value)
        self._timebase_range = value
        self._timebase_scale = value / self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(True, 'timebase_scale')
        self._set_cache_valid(False, 'timebase_window_scale')
        self._set_cache_valid(False, 'timebase_window_range')

    def _get_timebase_real_acquisition_time(self):
        if not self._driver_operation_simulate:
            return float(self._ask("timebase:ratime?"))
        return

    def _get_timebase_divisions(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._horizontal_divisions = int(float(self._ask("timebase:divisions?")))
        return self._horizontal_divisions

    def _get_acquisition_start_time(self):
        return self._get_timebase_position() - self._get_acquisition_time_per_record() / 2

    def _set_acquisition_start_time(self, value):
        self._set_timebase_position(float(value) + self._get_acquisition_time_per_record() / 2)

    def _get_acquisition_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = [self._ask("channel:type?").lower()]
            value.append(self._ask("channel:arithmetics?").lower())
            self._acquisition_type = [k for k,v in AcquisitionTypeMapping.items() if v==value]
            self._set_cache_valid()
        return self._acquisition_type

    def _set_acquisition_type(self, value):
        if value not in AcquisitionTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("channel:type %s" % AcquisitionTypeMapping[value][0])
            self._write("channel:arithmetics %s" % AcquisitionTypeMapping[value][1])
        self._acquisition_type = value
        self._set_cache_valid()

    def _get_acquisition_number_of_points_minimum(self):
        return self._get_acquisition_record_length()

    def _set_acquisition_number_of_points_minimum(self, value):
        if value < 20e3:
            value = 20e3 # Minimum number of points is 20 kSa
        if not self._driver_operation_simulate:
            self._acquisition_record_length = int(value)
            self._acquisition_number_of_points_minimum = self._acquisition_record_length
            self._acquisition_record_length_automatic = False
            self._set_cache_valid()
            self._write("acquire:points %d" % self._acquisition_record_length)            

    def _get_acquisition_record_length_automatic(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_record_length_automatic = (False, True)[int(self._ask("acquire:points:automatic?"))]
            self._set_cache_valid()
        return self._acquisition_record_length_automatic

    def _set_acquisition_record_length_automatic(self, value):
        if not self._driver_operation_simulate:
            self._write("acquire:points:automatic %d" % (0, 1)[value])
            self._get_acquisition_record_length() # Need to update record length after turning off automatic record length
        self._acquisition_record_length_automatic = value

    def _get_acquisition_record_length(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_record_length = int(self._ask("acquire:points?"))
            self._set_cache_valid()
        return self._acquisition_record_length

    def _get_acquisition_sample_rate(self):
        return float(self._ask("acquire:srate?"))
        #return self._get_acquisition_record_length() / self._get_timebase_real_acquisition_time() # Observe that the real acquisition time is longer than acquisition time 

    def _get_acquisition_time_per_record(self):
        return self._get_timebase_range()

    def _set_acquisition_time_per_record(self, value):
        value = float(value)
        self._set_timebase_range(value)


    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask("%s:label?" % self._channel_name[index]).strip('"')
            self._set_cache_valid(index=index)
        return self._channel_label[index]
    
    def _set_channel_label(self, index, value):
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("%s:label '%s'" % (self._channel_name[index], value))
        self._channel_label[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_enabled[index] = bool(int(self._ask("%s:state?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_enabled[index]
    
    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write("%s:state %d" % (self._channel_name[index], int(value)))
        self._channel_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_input_frequency_max(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            bandwidth_limit = self._ask("%s:bandwidth?" % self._channel_name[index]).lower()
            if bandwidth_limit == 'full':
                self._channel_bw_limit[index] = self._bandwidth
            elif bandwidth_limit[0] == 'b':
                self._channel_bw_limit[index] = int(bandwidth_limit[1:])
            self._set_cache_valid(index=index)
        return self._channel_bw_limit[index]
    
    def _set_channel_input_frequency_max(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            if value in BandwidthMapping.keys():
                self._write("%s:bwlimit %s" % (self._channel_name[index], bandwidth[str(1e-6*value)]))
            else:
                raise ivi.ValueNotSupportedException("Supported bandwidth limits are %d" % BandwidthMapping.keys()
        self._channel_bw_limit[index] = value
        self._set_cache_valid(index=index)