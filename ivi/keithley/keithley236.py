"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2015 Hermann Kraus

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
from .. import dcpwr

class keithley236(dcpwr.Base, dcpwr.Measurement, ivi.Driver):
    """Keitley 236 Source Measure Unit driver.

    The following functions are unsupported at the moment:
    - Reading error status
    - Triggers
    - Sweeps
    - Remote sense
    - Filter
    - Intergration time setting"""

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '236')
        super(keithley236, self).__init__(*args, **kwargs)

        self._add_property('outputs[].mode',
                self._get_output_mode,
                self._set_output_mode,
                None,
                ivi.Doc("""
                Specifies the output mode of the instrument. Valid values are: 'voltage', 'current'

                In 'voltage' mode the voltage is specified and there is a current compliance value. Only the current can be measured.
                In 'current' mode the current is specified and there is a voltage compliance value. Only the voltage can be measured.
                """))

        self._output_count = 1

        self._output_spec = [
            {
                'range': {
                    'P110V': (110.0, 0.1),
                },
                'ovp_max': 0,
                'voltage_max': 110.0,
                'current_max': 0.1
            }
        ]

        self._identity_description = "Keitley 236 Source Measure Unit driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = "Keithley"
        self._identity_instrument_manufacturer = "Keithley"
        self._identity_instrument_model = "236"
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PSU']

        self._init_outputs()

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."

        super(keithley236, self)._initialize(resource, id_query, reset, **keywargs)

        # interface clear
        if not self._driver_operation_simulate:
            try:
                return self._interface.clear()
            except (AttributeError, NotImplementedError):
                self._write("X")

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

        self._configure_output_format()

    def _utility_disable(self):
        pass

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass

    def _init_outputs(self):
        try:
            super(keithley236, self)._init_outputs()
        except AttributeError:
            pass

        self._output_current_limit = list()
        self._output_current_limit_behavior = list()
        self._output_enabled = list()
        self._output_ovp_enabled = list()
        self._output_ovp_limit = list()
        self._output_voltage_level = list()
        self._output_trigger_source = list()
        self._output_trigger_delay = list()
        self._output_mode = list()
        for i in range(self._output_count):
            self._output_current_limit.append(0)
            self._output_current_limit_behavior.append('regulate')
            self._output_enabled.append(False)
            self._output_ovp_enabled.append(True)
            self._output_ovp_limit.append(0)
            self._output_voltage_level.append(0)
            self._output_trigger_source.append('bus')
            self._output_trigger_delay.append(0)
            self._output_mode.append('voltage')

    def _configure_output_format(self):
        """ Force correct output format """
        #TODO: Binary mode is ~3 times faster
        self._write('G4,2,0X')


    def _get_compliance(self):
        """ Read compliance value form device. Meaning depends on mode of operation.
            In voltage mode a current is returned, in current mode a voltage is returned.
            Format:
                VCP010.000E-03 (voltage mode)
                ICP010.000E-03 (current mode)
            Note: This is an internal helper function which is not intended to be called
            with _driver_operation_simulate == True.
        """
        raw = self._ask('U5X')
        return float(raw[3:])

    def _get_source_value(self):
        """Read back the source value.
        It is required to change the output format during this operation. Output format is
        changed afterwards to return measure value again.
        Note: This is an internal helper function which is not intended to be called
            with _driver_operation_simulate == True."""
        try:
            raw = self._ask('G1,2,0X')
        finally:
            self._configure_output_format()
        return float(raw)


    def _get_machine_state(self):
        """Read back configuration parameters.
        Note: This is an internal helper function which is not intended to be called
            with _driver_operation_simulate == True."""
        raw = self._ask('U3X')
        #TODO: Trigger mode
        return {'operate': "N1" in raw,
                'triggering': "R1" in raw
               }

    def _get_output_mode(self, index = 0):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            raw = self._ask("U4X")
            if "F0" in raw:
                value = 'voltage'
            else:
                value = 'current'
            self._output_mode[index] = value
        self._set_cache_valid(index=index)
        return self._output_mode[index]

    def _set_output_mode(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            #Safe mode switching:
            # Disable output, remember voltage and current settings,
            # switch mode, set voltage and current again, enable output if it was enabled
            enabled = self._get_output_enabled(index)
            voltage = self._get_output_voltage_level(index)
            current = self._get_output_current_limit(index)
            if value == 'voltage':
                self._write("N0XF0,0B%e,0,0L%e,0XN%dX" % (voltage, current, enabled))
            elif value == 'current':
                self._write("N0XF1,0B%e,0,0L%e,0XN%dX" % (current, voltage, enabled))
            else:
                raise ivi.InvalidOptionValueException()
        self._output_mode[index] = value
        self._set_cache_valid(index=index)

    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            #There are two different ways to read the current limit:
            # Voltage mode: Read compliance value
            # Current mode: Read output value
            if self._get_output_mode(index) == 'voltage':
                self._output_current_limit[index] = self._get_compliance()
            else:
                self._output_current_limit[index] = self._get_source_value()
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]

    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._get_output_mode(index) == 'voltage':
                self._write("L%e,0X" % value)
            else:
                self._write("B%e,0,0X" % value)
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)


    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._get_output_mode(index) == 'voltage':
                self._output_voltage_level[index] = self._get_source_value()
            else:
                self._output_voltage_level[index] = self._get_compliance()
            self._set_cache_valid(index=index)
        return self._output_voltage_level[index]

    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if abs(value) > self._output_spec[index]['voltage_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._get_output_mode(index) == 'voltage':
                self._write("B%e,0,0X" % value)
            else:
                self._write("L%e,0X" % value)
        self._output_voltage_level[index] = value
        self._set_cache_valid(index=index)


    def _set_output_current_limit_behavior(self, index, value):
        if value != 'regulate':
            raise ivi.ValueNotSupportedException()

    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_enabled[index] = self._get_machine_state()['operate']
            self._set_cache_valid(index=index)
        return self._output_enabled[index]

    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write("N%dX" % value)
        self._output_enabled[index] = value
        self._set_cache_valid(index=index)

    def _output_query_current_limit_max(self, index, voltage_level):
        index = ivi.get_index(self._output_name, index)
        if abs(voltage_level) > self._output_spec[index]['voltage_max']:
            raise ivi.OutOfRangeException()
        return self._output_spec[index]['current_max']

    def _output_query_voltage_level_max(self, index, current_limit):
        index = ivi.get_index(self._output_name, index)
        if abs(current_limit) > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        return self._output_spec[index]['voltage_max']

    def _output_measure(self, index, type):
        index = ivi.get_index(self._output_name, index)
        if type not in dcpwr.MeasurementType:
            raise ivi.ValueNotSupportedException()
        if type == 'voltage':
            if self._get_output_mode(index) == 'voltage':
                raise ivi.OperationNotSupportedException("Can not read voltage in voltage output mode")
            elif not self._driver_operation_simulate:
                return float(self._read())
        elif type == 'current':
            if self._get_output_mode(index) == 'voltage':
                return float(self._read())
            elif not self._driver_operation_simulate:
                raise ivi.OperationNotSupportedException("Can not read current in current output mode")
        return 0

    def _output_query_output_state(self, index, state):
        index = ivi.get_index(self._output_name, index)
        if state not in dcpwr.OutputState:
            raise ivi.ValueNotSupportedException()
        status = 0
        if not self._driver_operation_simulate:
            status = self._read_stb()
        compliance = bool(status & 128)
        if state == 'constant_voltage':
            if self._get_output_mode(index) == 'voltage':
                return not compliance
            else:
                return compliance
        elif state == 'constant_current':
            if self._get_output_mode(index) == 'current':
                return not compliance
            else:
                return compliance
        return False

    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            raw = self._ask("U0X")
            self._identity_instrument_model = raw[:3]
            self._identity_instrument_firmware_revision = raw[3:6]
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')

    def _get_identity_instrument_model(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_model

    def _get_identity_instrument_serial_number(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_serial_number

    def _get_identity_instrument_firmware_revision(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_firmware_revision

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("J0X")
            self._clear()
            self.driver_operation.invalidate_all_attributes()
