"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2017 Alex Forencich

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

from .. import ivi
from .. import scpi

Source = set(['internal', 'external'])
ALCSourceMapping = {'internal': 'int',
                    'external': 'diode'}
PowerMode = set(['fixed', 'sweep'])
FrequencyModeMapping = {'cw': 'cw',
                        'sweep': 'sweep'}
TrackingHost = set(['hp8560', 'hp8561', 'hp8562', 'hp8562old', 'hp8563', 'hp8563e', 'hp8566',
                    'hp8593', 'hp8594', 'hp8595', 'hp8596', 'hp8340_5', 'hp8340_1', 'hp8341_5',
                    'hp8341_1', 'hp70909', 'hp70910', 'hp83590_5', 'hp83590_1', 'hp83592_5',
                    'hp83592_1', 'hp83594_5', 'hp83594_1', 'hp83595_5', 'hp83595_1'])
SweeptuneSetting = set(['default', 'custom'])

class agilent85644A(ivi.Driver, scpi.common.Memory):
    "Agilent 85644A IVI tracking source driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '85644A')

        super(agilent85644A, self).__init__(*args, **kwargs)

        self._memory_size = 10

        self._rf_frequency = 3e9
        self._rf_frequency_offset = 0.0
        self._rf_frequency_mode = 'cw'
        self._rf_level = 0.0
        self._rf_attenuation = 0.0
        self._rf_attenuation_auto = True
        self._rf_output_enabled = False
        self._rf_power_mode = 'fixed'
        self._rf_power_slope = 0.0
        self._rf_power_center = 0.0
        self._rf_power_span = 0.0
        self._rf_tracking_adjust = 0
        self._rf_tracking_host = 'hp8560'
        self._rf_tracking_sweeptune = 'default'
        self._alc_enabled = True
        self._alc_source = 'internal'

        self._reference_oscillator_source = 'internal'

        self._identity_description = "Agilent 85644/5A IVI tracking source driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 2
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = list(['85644A', '85645A'])

        self._frequency_low = 300e3
        self._frequency_high = 6.5e9

        self._add_property('rf.frequency',
                        self._get_rf_frequency,
                        self._set_rf_frequency)
        self._add_property('rf.frequency_offset',
                        self._get_rf_frequency_offset,
                        self._set_rf_frequency_offset)
        self._add_property('rf.frequency_mode',
                        self._get_rf_frequency_mode,
                        self._set_rf_frequency_mode)
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
        self._add_property('rf.power_slope',
                        self._get_rf_power_slope,
                        self._set_rf_power_slope)
        self._add_property('rf.power_center',
                        self._get_rf_power_center,
                        self._set_rf_power_center)
        self._add_property('rf.power_span',
                        self._get_rf_power_span,
                        self._set_rf_power_span)
        self._add_property('rf.tracking_adjust',
                        self._get_rf_tracking_adjust,
                        self._set_rf_tracking_adjust)
        self._add_property('rf.tracking_host',
                        self._get_rf_tracking_host,
                        self._set_rf_tracking_host)
        self._add_property('rf.tracking_sweeptune',
                        self._get_rf_tracking_sweeptune,
                        self._set_rf_tracking_sweeptune)
        self._add_method('rf.configure',
                        self._rf_configure)
        self._add_method('rf.is_unleveled',
                        self._rf_is_unleveled)
        self._add_property('alc.enabled',
                        self._get_alc_enabled,
                        self._set_alc_enabled)
        self._add_property('alc.source',
                        self._get_alc_source,
                        self._set_alc_source)
        self._add_property('reference_oscillator.source',
                        self._get_reference_oscillator_source)


    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilent85644A, self)._initialize(resource, id_query, reset, **keywargs)

        # interface clear
        #if not self._driver_operation_simulate:
        #    self._clear()

        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)

        # reset
        if reset:
            self.utility_reset()


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
            self._write("*TST?")
            # wait for test to complete
            time.sleep(30)
            code = int(self._read())
            if code != 0:
                message = "Self test failed"
        return (code, message)

    def _utility_unlock_object(self):
        pass


    def _get_rf_frequency(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency = float(self._ask("source:frequency?"))
            self._set_cache_valid()
        return self._rf_frequency

    def _set_rf_frequency(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:frequency %e" % value)
        self._rf_frequency = value
        self._set_cache_valid()

    def _get_rf_frequency_offset(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_frequency_offset = float(self._ask("source:frequency:offset?"))
            self._set_cache_valid()
        return self._rf_frequency_offset

    def _set_rf_frequency_offset(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:frequency:offset %e" % value)
        self._rf_frequency_offset = value
        self._set_cache_valid()

    def _get_rf_frequency_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("source:frequency:mode?").lower()
            self._rf_frequency_mode = [k for k,v in FrequencyModeMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._rf_frequency_mode

    def _set_rf_frequency_mode(self, value):
        if value not in FrequencyModeMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("source:frequency:mode %s" % FrequencyModeMapping[value])
        self._rf_frequency_mode = value
        self._set_cache_valid()

    def _get_rf_level(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_level = float(self._ask("source:power:level?"))
            self._set_cache_valid()
        return self._rf_level

    def _set_rf_level(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:power:level %e" % value)
        self._rf_level = value
        self._set_cache_valid(False, 'rf_power_center')
        self._set_cache_valid()

    def _get_rf_attenuation(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_attenuation = float(self._ask("source:power:attenuation?"))
            self._set_cache_valid()
        return self._rf_attenuation

    def _set_rf_attenuation(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:power:attenuation %e" % value)
        self._rf_attenuation = value
        self._rf_attenuation_auto = False
        self._set_cache_valid()

    def _get_rf_attenuation_auto(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_attenuation_auto = bool(int(self._ask("source:power:attenuation:auto?")))
            self._set_cache_valid()
        return self._rf_attenuation_auto

    def _set_rf_attenuation_auto(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("source:power:attenuation:auto %d" % int(value))
        self._rf_attenuation_auto = value
        self._set_cache_valid()

    def _get_rf_output_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_output_enabled = bool(int(self._ask("output:state?")))
        return self._rf_output_enabled

    def _set_rf_output_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("output:state %d" % int(value))
        self._rf_output_enabled = value
        self._set_cache_valid()

    def _get_rf_power_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_power_mode = self._ask("source:power:mode?").lower()
            self._set_cache_valid()
        return self._rf_power_mode

    def _set_rf_power_mode(self, value):
        if value not in PowerMode:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("source:power:mode %s" % value)
        self._rf_power_mode = value
        self._set_cache_valid(False, 'rf_power_span')
        self._set_cache_valid()

    def _get_rf_power_slope(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_power_slope = float(self._ask("source:power:slope?"))
            self._set_cache_valid()
        return self._rf_power_slope

    def _set_rf_power_slope(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:power:slope %e" % value)
        self._rf_power_slope = value
        self._set_cache_valid()

    def _get_rf_power_center(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_power_center = float(self._ask("source:power:center?"))
            self._set_cache_valid()
        return self._rf_power_center

    def _set_rf_power_center(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:power:center %e" % value)
        self._rf_power_center = value
        self._set_cache_valid(False, 'rf_level')
        self._set_cache_valid()

    def _get_rf_power_span(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_power_span = float(self._ask("source:power:span?"))
            self._set_cache_valid()
        return self._rf_power_span

    def _set_rf_power_span(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write("source:power:span %e" % value)
        self._rf_power_span = value
        self._set_cache_valid(False, 'rf_power_mode')
        self._set_cache_valid()

    def _get_rf_tracking_adjust(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_tracking_adjust = int(self._ask("calibration:track:adj?"))
            self._set_cache_valid()
        return self._rf_tracking_adjust

    def _set_rf_tracking_adjust(self, value):
        value = int(value)
        if not self._driver_operation_simulate:
            self._write("calibration:track:adj %d" % value)
        self._rf_tracking_adjust = value
        self._set_cache_valid()

    def _get_rf_tracking_host(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._rf_tracking_host = self._ask("source:sweep:rselect?").lower()
            self._set_cache_valid()
        return self._rf_tracking_host

    def _set_rf_tracking_host(self, value):
        if value not in TrackingHost:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("source:sweep:rselect %s" % value)
        self._rf_tracking_host = value
        self._set_cache_valid()

    def _get_rf_tracking_sweeptune(self):
        # read not implemented
        #if not self._driver_operation_simulate and not self._get_cache_valid():
        #    self._rf_tracking_sweeptune = self._ask("calibration:sweeptune:setting?").lower()
        #    self._set_cache_valid()
        return self._rf_tracking_sweeptune

    def _set_rf_tracking_sweeptune(self, value):
        if value not in SweeptuneSetting:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            # appears that the options are swapped (firmware bug)
            self._write("calibration:sweeptune:setting %s" % ('default' if value == 'custom' else 'custom'))
            #self._write("calibration:sweeptune:setting %s" % value)
        self._rf_tracking_sweeptune = value
        self._set_cache_valid()

    def _rf_configure(self, frequency, level):
        self._set_rf_frequency(frequency)
        self._set_rf_level(level)

    def _rf_is_unleveled(self):
        if not self._driver_operation_simulate:
            return bool(int(self._ask("diagnostic:unleveled?")))
        return False

    def _get_alc_enabled(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._alc_enabled = bool(int(self._ask("source:power:alc:state?")))
            self._set_cache_valid()
        return self._alc_enabled

    def _set_alc_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("source:power:alc:state %d" % int(value))
            self._set_cache_valid()
        self._alc_enabled = value

    def _get_alc_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("source:power:alc:source?").lower()
            self._alc_source = [k for k,v in ALCSourceMapping.items() if v==value][0]
            self._set_cache_valid()
        return self._alc_source

    def _set_alc_source(self, value):
        if value not in ALCSourceMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write("source:power:alc:source %s" % ALCSourceMapping[value])
            self._set_cache_valid()
        self._alc_source = value

    def _get_reference_oscillator_source(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._reference_oscillator_source = 'external' if int(self._ask("source:roscillator:source?")) else 'internal'
        return self._reference_oscillator_source


