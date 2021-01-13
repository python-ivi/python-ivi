"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2017-2018 Acconeer AB

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

AcquisitionInterpolationMapping = {
        'linear': 'lin',
        'sinex': 'sinx',
        'sample_and_hold': 'smhd'}
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
DelaySlopeMapping = {
        'positive': 'pos',
        'negative': 'neg'}
VerticalCouplingMapping = {
        'dc':  'dcl',
        'ac':  'acl',
        'gnd': 'gnd'}
TriggerModifierMapping = {
        'none': 'norm', # according to IVI standardization, oscilloscope normal triggde mode is called 'none'
        'normal': 'norm',
        'auto': 'auto'}
TriggerCouplingMapping = {
        'ac': ('ac', 0, 0),
        'dc': ('dc', 0, 0),
        'lf_reject': ('lfr', 0, 0),
        'hf_reject_dc': ('dc', 1, 0),
        'hf_reject_ac': ('ac', 1, 0),
        'noise_reject_dc': ('dc', 0, 1),
        'noise_reject_ac': ('ac', 0, 1)}
TriggerTypeMapping = {
        'edge': 'edge',
        'width': 'width',
        'tv': 'tv',
        # commented fields are to be supported in future
        # 'immediate': '',
        'line': 'line',
        # 'pattern': 'patt', # called logic trigger
        # 'bus': 'bus'
        }
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
        'either': 'eith'}
SearchConditionMapping = {
        'edge': 'edge',
        'width': 'widt',
        'peak': 'peak',
        'runt': 'runt',
        'rtime': 'rtim',
        'datatoclock': 'dat',
        'pattern': 'patt',
        'protocol': 'prot'}
MeasurementFunctionMapping = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'standard_deviation': 'stddev',
        'voltage_rms': 'vrms display',
        'voltage_peak_to_peak': 'peak',
        'voltage_max': 'vmax',
        'voltage_min': 'vmin',
        'voltage_high': 'vtop',
        'voltage_low': 'vbase',
        'voltage_average': 'vaverage display',
        'voltage_mean': 'mean',
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
        'duty_cycle_positive': 'dutycycle',
        'phase': 'phase',
        'delay': 'delay'}
MeasurementResultTypeMapping = {
        'mean': 'avg',
        'avg': 'avg',
        'std': 'stddev',
        'count': 'wfmcount',
        'min': 'npeak',
        'max': 'ppeak'}
MeasurementStatusMapping = {
        'complete': 'comp',
        'in_progress': 'stop',
        'running': 'run',
        'break': 'bre'}
ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'png': 'png'}
TimebaseModeMapping = {
        'main': 'main',
        'window': 'wind',
        'xy': 'xy',
        'roll': 'roll'}
TimebaseReferenceMapping = {
        'left': 8.33,
        'center': 50.0,
        'right': 91.67}

class rohdeschwarzBaseScope(scpi.common.IdnCommand, scpi.common.ErrorQuery, scpi.common.Reset,
                            scope.Base, scope.ContinuousAcquisition, scope.TriggerModifier, scope.Interpolation,
                            scope.WaveformMeasurement,
                            extra.common.Screenshot,
                            ivi.Driver):
    "Rohde&Schwarz generic IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._channel_label = list()

        self._vertical_divisions = 10

        super(rohdeschwarzBaseScope, self).__init__(*args, **kwargs)

        self._memory_size = 10
        self._bandwidth = 1e9
        self._trigger_holdoff_min = 51.2e-9
        self._channel_offset_max = 1.2
        self._horizontal_divisions = 12

        self._acquisition_segmented_count = 2
        self._acquisition_segmented_index = 1
        self._acquisition_number_of_points_minimum = 10e3
        self._acquisition_record_length = 20e3
        self._acquisition_record_length_automatic = True
        self._acquisition_type = 'normal'
        self._acquisition_interpolation = 'sinex'

        self._timebase_mode = 'main'
        self._timebase_scale = 100e-6
        self._timebase_position = 0.0
        self._timebase_reference = 'center'
        self._timebase_range = 1.2e-3
        self._timebase_window_position = 0.0
        self._timebase_window_range = 600e-6
        self._timebase_window_scale = 50e-6

        self._trigger_mode = 'auto'
        self._trigger_type = 'edge'
        self._trigger_continuous = True

        self._search_state = 'off'
        self._search_condition = 'edge'
        self._search_trigger_edge_slope = 'positive'
        self._search_trigger_edge_level = '0.5'

        self._display_screenshot_image_format_mapping = ScreenshotImageFormatMapping
        self._display_vectors = True

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

        self._add_property('channels[].show_label',
                        self._get_channel_show_label,
                        self._set_channel_show_label,
                        None,
                        ivi.Doc("""
                        Turns the analog and digital channel labels on and off.
                        """))

        self._add_property('search.state',
                        self._get_search_state,
                        self._set_search_state,
                        None,
                        ivi.Doc("""
                        Specifies the state of the search functionality. It is either on or off.
                        """))

        self._add_property('search.source',
                        self._get_search_source,
                        self._set_search_source,
                        None,
                        ivi.Doc("""
                        Specifies the source the oscilloscope monitors for the search function. The
                        value can be a channel name alias, a driver-specific channel string, or
                        one of the values below.
                        """))

        self._add_property('search.trigger.edge.level',
                        self._get_search_trigger_edge_level,
                        self._set_search_trigger_edge_level,
                        None,
                        ivi.Doc("""
                        Specifies the voltage threshold for the search function. The units are
                        volts.
                        """))

        self._add_property('search.trigger.edge.slope',
                        self._get_search_trigger_edge_slope,
                        self._set_search_trigger_edge_slope,
                        None,
                        ivi.Doc("""
                        Specifies whether a rising or a falling edge triggers the oscilloscope.

                        This attribute affects instrument operation only when the Trigger Type
                        attribute is set to Edge Trigger.

                        Values:
                         * 'positive'
                         * 'negative'
                         * 'either'
                        """))

        self._add_property('search.condition',
                        self._get_search_condition,
                        self._set_search_condition,
                        None,
                        ivi.Doc("""
                        Specifies the event that triggers the oscilloscope.

                        Values:

                        * 'edge'
                        * 'width'
                        * 'peak'
                        * 'runt'
                        * 'rtime'
                        * 'datatoclock'
                        * 'pattern'
                        * 'protocol'
                        """))

        self._add_method('search.get_result',
                        self._search_get_result,
                        ivi.Doc("""
                        Get result of search function.
                        """))

        self._add_method('measurement.statistics.reset',
                        self._reset_measurement_statistics,
                        ivi.Doc("""
                        Reset measurement staistics .
                        """))

        self._add_property('measurement.enable',
                        self._get_measurement_enable,
                        self._set_measurement_enable,
                        None,
                        ivi.Doc("""
                        Enable or disable measurement.
                        Values:
                         * 'on'
                         * 'off'
                        """))

        self._add_property('measurement.function',
                        self._get_measurement_function,
                        self._set_measurement_function,
                        None,
                        ivi.Doc("""
                        Specifies the measurement function used.

                        Values: specified in MeasurementFunctionMapping
                        """))

        self._add_method('measurement.source',
                        self._set_measurement_source,
                        ivi.Doc("""
                        Specifies measurement source, both source 1 and source 2(optional, based on measurement function).
                        """))

        self._add_property('measurement.statistics.enable',
                        self._get_measurement_statistics_enable,
                        self._set_measurement_statistics_enable,
                        None,
                        ivi.Doc("""
                        Enable or disable statistics for measurement.
                        Values:
                         * 'on'
                         * 'off'
                        """))

        self._add_method('measurement.set_delay_slope',
                        self._measurement_set_delay_slope,
                        ivi.Doc("""
                        Specifies whether a rising or a falling edge is used for delay measurements.
                        Values:
                         * 'positive'
                         * 'negative'
                        """))

        self._add_property('acquisition.number_of_waveforms',
                        self._get_acquisition_number_of_waveforms,
                        self._set_acquisition_number_of_waveforms,
                        None,
                        ivi.Doc("""
                        The number of waveforms that are acquired with a [Single] acquisition.
                        """))

        self._init_channels() # Remove from base class?

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

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

    def _utility_self_test(self):
        pass

    def _utility_reset(self):
        # Reset and wait for completion
        self._ask("*RST; *OPC?")
        self._clear()

    def _init_channels(self):
        try:
            super(rohdeschwarzBaseScope, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_label = list()
        self._channel_show_label = list()

        # analog channels
        self._analog_channel_name = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_coupling = list()
        self._channel_input_impedance = list()
        self._channel_input_frequency_max = list()
        self._channel_probe_attenuation = list()
        self._channel_scale = list()
        self._channel_range = list()
        self._channel_offset = list()
        self._channel_trigger_level = list()
        self._channel_bw_limit = list()

        for i in range(self._analog_channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_label.append("C%d" % (i+1))
            self._channel_show_label.append(False)
            self._analog_channel_name.append("C%d" % (i+1))

            self._channel_probe_skew.append(0)
            self._channel_invert.append(False)
            self._channel_coupling.append('dc')
            self._channel_input_impedance.append(1e9)
            self._channel_input_frequency_max.append(1e9)
            self._channel_probe_attenuation.append(1)
            self._channel_scale.append(50e-3)
            self._channel_range.append(self._vertical_divisions * self._channel_scale[i])
            self._channel_offset.append(0)
            self._channel_trigger_level.append(0.0)
            self._channel_bw_limit.append(False)

        # digital channels
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("digital%d" % i)
                self._channel_label.append("D%d" % i)
                self._channel_show_label.append(False)
                self._digital_channel_name.append("digital%d" % i)
                self._channel_trigger_level.append(0.0)

        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)

    # scope.Base
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
            self._acquisition_type = [k for k,v in AcquisitionTypeMapping.items() if v==value][0]
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
        if value < 10e3:
            value = 10e3 # Minimum number of points is 10 kSa
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

    # scope.Interpolation
    def _get_acquisition_interpolation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("acquire:interpolate?").lower()
            self._acquisition_interpolation = [k for k,v in AcquisitionInterpolationMapping.items() if v==value][0]
        return self._acquisition_interpolation

    def _set_acquisition_interpolation(self, value):
        if value not in AcquisitionInterpolationMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("acquire:interpolate %s" % AcquisitionInterpolationMapping[value])
        self._acquisition_interpolation = value

    # scope.Base, continued
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
            # If self._channel_show_label == True, then also display label on the screen
            if self._channel_show_label[index] == True:
                self._write("%s:label:state on" % self._channel_name[index])
        self._channel_label[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_show_label(self, index):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._channel_show_label[index] = bool(int(self._ask("%s:label:state?" % self._channel_name[index])))
            self._set_cache_valid()
        return self._channel_show_label[index]

    def _set_channel_show_label(self, index, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("%s:label:state %s" % (self._channel_name[index], ('off', 'on')[int(value)]))
        self._channel_show_label[index] = value
        self._set_cache_valid()

    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if index < self._analog_channel_count:
                self._channel_enabled[index] = bool(int(self._ask("%s:state?" % self._channel_name[index])))
                self._set_cache_valid(index=index)
            else:
                self._channel_enabled[index] = bool(int(self._ask("%s:display?" % self._channel_name[index])))
                self._set_cache_valid(index=index)
        return self._channel_enabled[index]

    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            if index < self._analog_channel_count:
                self._write("%s:state %d" % (self._channel_name[index], int(value)))
            else:
                state = ['off', 'on']
                self._write("%s:display %s" % (self._channel_name[index], state[int(value)]))
        self._channel_enabled[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_input_impedance(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        return self._channel_input_impedance[index]

    def _set_channel_input_impedance(self, index, value):
        raise ivi.ValueNotSupportedException('Input impedance of all BNC inputs is fixed to 1 MOhm')

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
                self._write("%s:bandwidth %s" % (self._analog_channel_name[index], str(1e-6*value)))
            else:
                raise ivi.ValueNotSupportedException("Supported bandwidth limits are %d" % BandwidthMapping.keys())
        self._channel_bw_limit[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_attenuation[index] = float(self._ask("probe%s:setup:attenuation:manual?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_attenuation[index]

    def _set_channel_probe_attenuation(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if 0.001 > value > 10000:
            raise ivi.OutOfRangeException
        if not self._driver_operation_simulate:
            print("probe%s:setup:attenuation:manual %f" % (self._channel_name[index], value))
            self._write("probe%s:setup:attenuation:manual %e" % (self._analog_channel_name[index], value))
        self._channel_probe_attenuation[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, 'channel_offset', index)
        self._set_cache_valid(False, 'channel_scale', index)
        self._set_cache_valid(False, 'channel_range', index)
        self._set_cache_valid(False, 'channel_trigger_level', index)
        self._set_cache_valid(False, 'trigger_level')

    def _get_channel_probe_skew(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_skew[index] = float(self._ask("%s:skew?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_skew[index]

    def _set_channel_probe_skew(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("%s:skew %e" % (self._channel_name[index], value))
        self._channel_probe_skew[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_invert(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            value = self._ask("%s:polarity?" % self._channel_name[index]).lower()
            if value == 'norm':
                self._channel_invert[index] = False
            elif value == 'inv':
                self._channel_invert[index] = True
            self._set_cache_valid(index=index)
        return self._channel_invert[index]

    def _set_channel_invert(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate:
            self._write("%s:polarity %s" % (self._channel_name[index], ('norm', 'inv')[value]))
        self._channel_invert[index] = value

    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            value = self._ask("%s:coupling?" % self._channel_name[index]).lower()
            self._channel_coupling[index] = [k for k,v in VerticalCouplingMapping.items() if v==value][0]
            self._set_cache_valid(index=index)
        return self._channel_coupling[index]

    def _set_channel_coupling(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in VerticalCouplingMapping.keys():
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("%s:coupling %s" % (self._channel_name[index], VerticalCouplingMapping[value]))
        self._channel_coupling[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_offset(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_offset[index] = float(self._ask("%s:offset?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_offset[index]

    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if abs(value) > self._channel_offset_max:
            raise ivi.OutOfRangeException
        if not self._driver_operation_simulate:
            self._write("%s:offset %e" % (self._channel_name[index], value))
        self._channel_offset[index] = value
        self._set_cache_valid(index=index)

    def _get_channel_range(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_range[index] = float(self._ask("%s:range?" % self._channel_name[index]))
            self._channel_scale[index] = self._channel_range[index] / self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_scale", index)
        return self._channel_range[index]

    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        # Instrument can handle 5 V/division with 1:1 probe compensation
        if 1e-3 * self._channel_scale[index] * self._channel_probe_attenuation[index] > value > 5 * self._channel_scale[index] * self._channel_probe_attenuation[index]:
            raise ivi.OutOfRangeException
        if not self._driver_operation_simulate:
            self._write("%s:range %e" % (self._channel_name[index], value))
        self._channel_range[index] = value
        self._channel_scale[index] = value / self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_scale", index)
        self._set_cache_valid(False, "channel_offset", index)

    def _get_channel_scale(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_scale[index] = float(self._ask("%s:scale?" % self._channel_name[index]))
            self._channel_range[index] = self._channel_scale[index] * self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_range", index)
        return self._channel_scale[index]

    def _set_channel_scale(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        # Instrument can handle 5 V/division with 1:1 probe compensation
        if 1e-3 * self._channel_probe_attenuation[index] > value > 5 * self._channel_probe_attenuation[index]:
            raise ivi.OutOfRangeException
        if not self._driver_operation_simulate:
            self._write("%s:scale %e" % (self._channel_name[index], value))
        self._channel_scale[index] = value
        self._channel_range[index] = value * self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_range", index)
        self._set_cache_valid(False, "channel_offset", index)


    # Trigger functions
    def _get_trigger_coupling(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            coupling = self._ask("trigger:a:edge:coupling?").lower()
            hf_reject = int(self._ask("trigger:a:edge:filter:hfreject?"))
            noise_reject = int(self._ask("trigger:a:edge:filter:nreject?"))
            for k in TriggerCouplingMapping:
                if (coupling, hf_reject, noise_reject) == TriggerCouplingMapping[k]:
                    self._trigger_coupling = k
                    break
        return self._trigger_coupling

    def _set_trigger_coupling(self, value):
        if value not in TriggerCouplingMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("trigger:a:edge:coupling %s" % TriggerCouplingMapping[value][0])
            self._write("trigger:a:edge:filter:hfreject %d" % TriggerCouplingMapping[value][1])
            self._write("trigger:a:edge:filter:nreject %d" % TriggerCouplingMapping[value][2])
        self._trigger_coupling = value
        self._set_cache_valid()

    def _get_trigger_holdoff(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            # First check if trigger holdoff is enabled. One can set a value but it won't apply before enabled.
            if self._ask("trigger:a:holdoff:mode?").lower() == 'off':
                self._trigger_holdoff = 0.0
            elif self._ask("trigger:a:holdoff:mode?").lower() == 'time':
                self._trigger_holdoff = float(self._ask("trigger:a:holdoff:time?"))
            self._set_cache_valid()
        return self._trigger_holdoff

    def _set_trigger_holdoff(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            if float(value) == 0.0:
                self._write("trigger:a:holdoff:mode off")
            elif value < self._trigger_holdoff_min:
                raise ivi.OutOfRangeException("Minimum trigger hold off time is %e" % self._trigger_holdoff_min)
            else:
                self._write("trigger:a:holdoff:time %e" % value)
                self._write("trigger:a:holdoff:mode time")
        self._trigger_holdoff = value
        self._set_cache_valid()

    def _get_channel_trigger_level(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_trigger_level[index] = float(self._ask("trigger:a:level%d?" % (index+1)))
            self._set_cache_valid(index=index)
        return self._channel_trigger_level[index]

    def _set_channel_trigger_level(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            if index < self._analog_channel_count:
                if value > self._channel_range[index]:
                    raise ivi.OutOfRangeException("Trigger level cannot be outside vertical range")
                self._write("trigger:a:level%d %e" % (index+1, value))
            else:
                self._write("%s:THRESHOLD %e" % (self._channel_name[index], value))
        self._channel_trigger_level[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, "trigger_level")

    def _get_trigger_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            ch = self._get_trigger_source()
            self._trigger_level = self._get_channel_trigger_level(ch)
            self._set_cache_valid()
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
            value = self._ask("trigger:a:edge:slope?").lower()
            self._trigger_edge_slope = [k for k,v in SlopeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_edge_slope

    def _set_trigger_edge_slope(self, value):
        if value not in SlopeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("trigger:a:edge:slope %s" % SlopeMapping[value])
        self._trigger_edge_slope = value
        self._set_cache_valid()

    def _get_trigger_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("trigger:a:source?").lower()
            if value[0:2] == 'ch':
                self._trigger_source = 'channel' + value[-1]
            elif value[0] == 'd':
                self._trigger_source == 'digital' + value[-1]
            else:
                self._trigger_source = value
            self._set_cache_valid()
        return self._trigger_source

    def _set_trigger_source(self, value):
        if hasattr(value, 'name'):
            value = value.name.lower()
        value = str(value)
        if value not in self._channel_name + ['line']:
            raise ivi.UnknownPhysicalNameException()
        if not self._driver_operation_simulate:
            if value[0:2] == 'ch':
                scpi_string = 'ch' + value[-1]
            elif value[0] == 'd':
                scpi_string = 'd' + value[-1]
            else:
                scpi_string = value
            self._write("trigger:a:source %s" % scpi_string)
        self._trigger_source = value
        self._set_cache_valid()

    def _get_trigger_continuous(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._trigger_continuous = self._ask("acquire:state?").lower() == 'run'
            self._set_cache_valid()
        return self._trigger_continuous

    def _set_trigger_continuous(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            scpi_string = 'stop'
            if value:
                scpi_string = 'run'
            self._write("acquire:state %s" % scpi_string)
        self._trigger_continuous = value
        self._set_cache_valid()

    def _get_trigger_modifier(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("trigger:a:mode?").lower()
            self._trigger_modifier = [k for k,v in TriggerModifierMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_modifier

    def _set_trigger_modifier(self, value):
        if value not in TriggerModifierMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("trigger:a:mode %s" % TriggerModifierMapping[value])
        self._trigger_modifier = value
        self._set_cache_valid()

    def _get_trigger_type(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("trigger:a:type?").lower()
            self._trigger_type = [k for k,v in TriggerTypeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._trigger_type

    def _set_trigger_type(self, value):
        if value not in TriggerTypeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("trigger:a:type %s" % TriggerTypeMapping[value])
        self._trigger_type = value
        self._set_cache_valid()

    def _measurement_abort(self):
        if not self._driver_operation_simulate:
            self._write("stop")
        self._set_cache_valid(False, 'trigger_continuous')

    def _measurement_initiate(self):
        if not self._driver_operation_simulate:
            self._write("trigger:a:mode normal")
            self._write("runsingle")
        self._set_cache_valid(False, 'trigger_continuous')

    def _get_measurement_status(self):
        if not self._driver_operation_simulate:
            value = self._ask("acquire:state?").lower()
            self._measurement_status = [k for k,v in MeasurementStatusMapping.items() if v==value][0]
            if value == 'stop' or value == 'comp':
                self._set_cache_valid(False, 'trigger_continuous')
        return self._measurement_status

    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)

        if self._driver_operation_simulate:
            return list()

        data_header = self._ask("%s:data:header?" % self._channel_name[index]).split(',') # x0, xN, record length, values/sample interval
        x0 = float(data_header[0])
        xN = float(data_header[1])
        N = int(data_header[2])
        dx = (xN - x0) / N
        x = [(x0 + i * dx) for i in range(0, N)]
        y = self._ask("%s:data?" % self._channel_name[index]).split(',')
        y = [float(yi) for yi in y]
        return list(zip(x, y))

    def _measurement_fetch_waveform_measurement(self, index, measurement_function, result_type=None, ref_channel=None):
        index = ivi.get_index(self._channel_name, index)
        meas_source1 = None
        meas_source2 = None
        ref_channel_state = None
        channel_state = self._get_channel_enabled(index)
        if index < self._analog_channel_count:
            if measurement_function not in MeasurementFunctionMapping:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMapping[measurement_function]
            meas_source1 = "CH%d" %(index+1)
        else:
            if measurement_function not in MeasurementFunctionMappingDigital:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMappingDigital[measurement_function]
            meas_source1 = "D%d" %(index - self._analog_channel_count)
        if not self._driver_operation_simulate:
            self._set_channel_enabled(index, True)
            self._write("measurement1:enable on")
            self._write("measurement1:main %s" % func)
            self._write("measurement1:source %s" %meas_source1)
            if measurement_function in ['ratio', 'phase', 'delay']:
                if hasattr(ref_channel, 'name'):
                    ref_channel = ref_channel.name
                ref_index = ivi.get_index(self._channel_name, ref_channel)
                ref_channel_state = self._get_channel_enabled(ref_index)
                self._set_channel_enabled(ref_index, True)
                if ref_index < self._analog_channel_count:
                    meas_source2 = "CH%d" %(ref_index+1)
                else:
                    meas_source2 = "D%d" %(ref_index - self._analog_channel_count)
                self._write("measurement1:source %s, %s"  %(meas_source1, meas_source2))
            if result_type is None:
                result = float(self._ask("measurement1:result?"))
            else:
                if result_type.lower() not in MeasurementResultTypeMapping:
                    raise ivi.ValueNotSupportedException()
                result = float(self._ask("measurement1:result:%s?" % MeasurementResultTypeMapping[result_type.lower()]))
            if ref_channel_state is not None:
                self._set_channel_enabled(ref_index, ref_channel_state)
            self._set_channel_enabled(index, channel_state)
            return result
        return 0

    def _measurement_read_waveform(self, index, maximum_time=None):
        # Add functionaly according to Python-IVI scope specification
        return self._measurement_fetch_waveform(index)

    def _measurement_read_waveform_measurement(self, index, measurement_function, maximum_time):
        return self._measurement_fetch_waveform_measurement(index, measurement_function)

    def _get_acquisition_number_of_waveforms(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_number_of_waveforms = int(self._ask("acquire:nsingle:count?"))
            self._set_cache_valid()
        return self._acquisition_number_of_waveforms

    def _set_acquisition_number_of_waveforms(self, value):
        if value < 1:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("acquire:nsingle:count %d" % value)
        self._acquisition_number_of_waveforms = value
        self._set_cache_valid()

    # extra.common
    def _display_fetch_screenshot(self, format='png', invert=False):
        if self._driver_operation_simulate:
            return b''

        if format not in self._display_screenshot_image_format_mapping:
            raise ivi.ValueNotSupportedException()

        self._write("hcopy:format %s" % format)
        self._write("hcopy:color:scheme %s" % ('color' if not invert else 'inverted'))

        screenshot = self._ask_for_ieee_block("hcopy:data?")
        self._read_raw() # flush buffer

        return screenshot

    # scope.WaveformMeasurement
    def _get_reference_level_high(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._reference_level_high = float(self._ask("reflevel:relative:upper?"))
            self._set_cache_valid()
        return self._reference_level_high

    def _set_reference_level_high(self, value):
        value = float(value)
        if value < 0: value = 0
        if value > 100: value = 100
        if not self._driver_operation_simulate:
            self._write("reflevel:relative:mode user")
            self._write("reflevel:relative:upper %e" % value)
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
            self._write("reflevel:relative:mode user")
            self._write("reflevel:relative:lower %e" % value)
        self._reference_level_low = value
        self._set_cache_valid()

    def _get_reference_level_middle(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._reference_level_middle = float(self._ask("reflevel:relative:middle?"))
            self._set_cache_valid()
        return self._reference_level_middle

    def _set_reference_level_middle(self, value):
        value = float(value)
        if value < 0: value = 0
        if value > 100: value = 100
        if not self._driver_operation_simulate:
            self._write("reflevel:relative:mode user")
            self._write("reflevel:relative:middle %e" % value)
        self._reference_level_middle = value
        self._set_cache_valid()

    def _get_search_state(self):
        if not self._driver_operation_simulate:
            self._search_state = self._ask("search:state?")

        self._set_cache_valid()
        return self._search_state

    def _set_search_state(self, value):
        value = str(value)
        if not self._driver_operation_simulate:
            self._write("search:state %s" % value)

        self._search_state = value
        self._set_cache_valid()

    def _get_search_source(self):
        if not self._driver_operation_simulate:
            value = self._ask("search:source?").lower()
            if value[0:2] == 'ch':
                self.search_source = 'channel' + value[-1]
            elif value[0] == 'd':
                self.search_source == 'digital'
                if value[-2].isdigit():
                    self.search_source = self.search_source + value[-2:]
                else:
                    self.search_source = self.search_source + value[-1]
            else:
                self.search_source = value
        self._set_cache_valid()
        return self.search_source

    def _set_search_source(self, value):
        if hasattr(value, 'name'):
            value = value.name.lower()
        value = str(value)
        if value not in self._channel_name + ['line']:
            raise ivi.UnknownPhysicalNameException()
        if not self._driver_operation_simulate:
            if value[0:2] == 'ch':
                scpi_string = 'ch' + value[-1]
            elif value[0] == 'd':
                scpi_string = 'd' + value[-1]
                if value[-2].isdigit():
                    scpi_string = scpi_string + value[-2:]
                else:
                    scpi_string = scpi_string + value[-1]
            else:
                scpi_string = value
            self._write("search:source %s" % scpi_string)

        self._search_source = value
        self._set_cache_valid()

    def _get_search_trigger_edge_level(self):
        if not self._driver_operation_simulate:
            self._search_trigger_edge_level = self._ask("search:trigger:edge:level?")

        return self._search_trigger_edge_level

    def _set_search_trigger_edge_level(self, value):
        value = float(value)

        if not self._driver_operation_simulate:
            self._write("search:trigger:edge:level %f" % value)

        self._search_trigger_edge_level = value
        self._set_cache_valid()

    def _get_search_trigger_edge_slope(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("search:trigger:edge:slope?").lower()
            self._search_trigger_edge_slope = [k for k,v in SlopeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._search_trigger_edge_slope

    def _set_search_trigger_edge_slope(self, value):
        if value not in SlopeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("search:trigger:edge:slope %s" % SlopeMapping[value])
        self._search_trigger_edge_slope = SlopeMapping[value]
        self._set_cache_valid()

    def _get_search_condition(self):
        if not self._driver_operation_simulate:
            value = self._ask("search:condition?").lower()
            self._search_condition = [k for k,v in SearchConditionMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._search_condition

    def _set_search_condition(self, value):
        if value not in SearchConditionMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("search:condition %s" % SearchConditionMapping[value])
        self._search_condition = SearchConditionMapping[value]
        self._set_cache_valid()

    def _search_get_result(self):
        result_str = ""
        if self._search_state == 'on':
            result_str = self._ask("search:result:all?")

        return result_str

    def _get_measurement_enable(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._measurement_enable = self._ask("measurement1:enable?").lower()
            self._set_cache_valid()
        return self._measurement_enable

    def _set_measurement_enable(self, value):
        if not isinstance(value, str) or value.lower() not in ['on', 'off']:
            raise ivi.ValueNotSupportedException()

        if not self._driver_operation_simulate:
            self._write("measurement1:enable %s" % value.lower())
        self._measurement_enable = value.lower()
        self._set_cache_valid()

    def _get_measurement_function(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._measurement_function = self._ask("measurement1:main?").lower()
            self._set_cache_valid()
        return self._measurement_function

    def _set_measurement_function(self, measurement_function):
        if measurement_function not in MeasurementFunctionMapping:
            raise ivi.ValueNotSupportedException()
        func = MeasurementFunctionMapping[measurement_function]
        if not self._driver_operation_simulate:
            self._write("measurement1:main %s" % func)
        self._measurement_function = func
        self._set_cache_valid()

    def _set_measurement_source(self, source1, source2=None):
        scpi_source1_string = self._get_channel_name_string(source1)
        if source2 is not None:
            scpi_source2_string = self._get_channel_name_string(source2)
            self._write("measurement1:source %s, %s" % (scpi_source1_string, scpi_source2_string))
        else:
            self._write("measurement1:source %s" % scpi_source1_string)
        self._set_cache_valid()

    def _get_channel_name_string(self, value):
        if hasattr(value, 'name'):
            value = value.name.lower()
        value = str(value)
        if value not in self._channel_name + ['line']:
            raise ivi.UnknownPhysicalNameException()
        if not self._driver_operation_simulate:
            if value[0:2] == 'ch':
                scpi_string = 'ch' + value[-1]
            elif value[0] == 'd':
                scpi_string = 'd' + value[-1]
            else:
                scpi_string = value
        return scpi_string

    def _reset_measurement_statistics(self):
        if not self._driver_operation_simulate:
            self._write("measurement1:statistics:reset")

    def _get_measurement_statistics_enable(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._measurement_statistic_enable = self._ask("measurement1:statistics:enable?").lower()
            self._set_cache_valid()
        return self._measurement_statistic_enable

    def _set_measurement_statistics_enable(self, value):
        if not isinstance(value, str) or value.lower() not in ['on', 'off']:
            raise ivi.ValueNotSupportedException()

        if not self._driver_operation_simulate:
            self._write("measurement1:statistics:enable %s" % value)
        self._measurement_statistic_enable = value.lower()
        self._set_cache_valid()

    def _measurement_set_delay_slope(self, signal_slope, reference_slope):
        if signal_slope not in DelaySlopeMapping or reference_slope not in DelaySlopeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("measurement1:delay:slope %s,%s" % (DelaySlopeMapping[signal_slope], DelaySlopeMapping[reference_slope]))
