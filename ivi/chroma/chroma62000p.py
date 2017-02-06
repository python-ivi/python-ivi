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

from .chromaBaseDCPwr import *

OCPLevels = set(["low", "high"])

class chroma62000p(chromaBaseDCPwr):
    "Chroma ATE 62000P series IVI DC power supply driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        super(chroma62000p, self).__init__(*args, **kwargs)

        self._output_count = 1

        self._output_spec = [
            {
                'range': {
                    'P600V': (600.0, 120.0)
                },
                'ovp_max': 660.0,
                'ocp_max': 132.0,
                'voltage_max': 600.0,
                'current_max': 120.0
            }
        ]

        self._memory_size = 10

        self._identity_description = "Chroma 62000P series IVI DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Chroma ATE"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['62006P-100-25', '62012P-80-60', '62012P-100-50', '62012P-600-8',
                                                      '62006P-30-80', '62006P-300-8', '62012P-40-120', '62024P-40-120',
                                                      '62024P-80-60', '62024P-100-50', '62024P-600-8', '62050P-100-100']

        self._add_property('outputs.slew_rate',
                         self._get_output_slew_rate,
                         self._set_output_slew_rate)
        self._init_outputs()


    # Tested on Chroma 62012P-80-60; working
    def _get_output_current_limit(self, index):
        """
        This function fetches the output current limit setting of the instrument.
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_current_limit[index] = float(self._ask("SOUR:CURR?"))
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]

    # Tested on Chroma 62012P-80-60; working
    def _set_output_current_limit(self, index, value):
        """
        This function sets the output current limit of the instrument.
        """
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("SOUR:CURR %.2f" % float(value))
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)

    # Tested on Chroma 62012P-80-60; working
    def _get_output_enabled(self, index):
        """
        This function queries the output state of the instrument.
        * 0, False = OFF
        * 1, True = ON
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            result = self._ask("CONF:OUTP?")
            if result == "ON":
                self._output_enabled[index] = True
            elif result == "OFF":
                self._output_enabled[index] = False
            self._set_cache_valid(index=index)
        return self._output_enabled[index]

    # Tested on Chroma 62012P-80-60; working
    def _set_output_enabled(self, index, value):
        """
        This function sets the output state of the instrument.
        * 0, False = OFF
        * 1, True = ON
        """
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if value:
            wr_value = "ON"
        else:
            wr_value = "OFF"
        if not self._driver_operation_simulate:
            self._write("CONF:OUTP %s" % str(wr_value))
        self._output_enabled[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False, index=k)
        self._set_cache_valid(index=index)

    # Tested on Chroma 62012P-80-60; working
    def _get_output_voltage_level(self, index):
        """
        This function fetches the output voltage setting of the instrument.
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_voltage_level[index] = float(self._ask("SOUR:VOLT?"))
            self._set_cache_valid(index=index)
        return self._output_voltage_level[index]

    # Tested on Chroma 62012P-80-60; working
    def _set_output_voltage_level(self, index, value):
        """
        This function sets the output voltage of the instrument.
        """
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_voltage_max[index]:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("SOUR:VOLT %.2f" % float((value)))
        self._output_voltage_level[index] = value
        self._set_cache_valid(index=index)

    # Tested on Chroma 62012P-80-60; working
    def _get_output_ovp_limit(self, index):
        """
        This function fetches the OVP limit.
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_ovp_limit[index] = float(self._ask("SOUR:VOLT:PROT:HIGH?"))
            self._set_cache_valid(index=index)
        return self._output_ovp_limit[index]

    # Tested on Chroma 62012P-80-60; working
    def _set_output_ovp_limit(self, index, value):
        """
        This function sets the OVP limit.
        """
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['ovp_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("SOUR:VOLT:PROT:HIGH %.1f" % value)
        self._output_ovp_limit[index] = value
        self._set_cache_valid(index=index)

    ##TODO: figure out how to handle OCP high and low levels
    #def _get_output_ocp_limit(self, index):
    #    """
    #    This function fetches the OCP limit.
    #    """
    #    index = ivi.get_index(self._output_name, index)
    #    if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
    #        self._output_ocp_limit[index] = float(self._ask("SOUR:CURR:PROT:HIGH?"))
    #        self._set_cache_valid(index=index)
    #    return self._output_ocp_limit[index]
#
    ##TODO: figure out how to handle OCP high and low levels
    #def _set_output_ocp_limit(self, index, value):
    #    """
    #    This function sets the high level OCP limit.
    #    """
    #    index = ivi.get_index(self._output_name, index)
    #    value = float(value)
    #    if value < 0 or value > self._output_spec[index]['ocp_max']:
    #        raise ivi.OutOfRangeException()
    #    if not self._driver_operation_simulate:
    #        self._write("SOUR:CURR:PROT:HIGH %.1f" % value)
    #    self._output_ocp_limit[index] = value
    #    self._set_cache_valid(index=index)

    # Tested on Chroma 62012P-80-60; working
    def _output_measure(self, index, meas_type):
        """
        This function measures the voltage or current of the output.
        """
        index = ivi.get_index(self._output_name, index)
        if meas_type not in ['voltage', 'current']:
            raise ivi.ValueNotSupportedException()
        if meas_type == 'voltage':
            if not self._driver_operation_simulate:
                return float(self._ask("FETC:VOLT?"))
        elif meas_type == 'current':
            if not self._driver_operation_simulate:
                return float(self._ask("FETC:CURR?"))
        return 0

    # Tested on Chroma 62012P-80-60; working
    def _get_output_slew_rate(self, index):
        """
        This function queries the output voltage slew rate.
        Values returned are in V/ms
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._output_slew_rate[index] = float(self._ask("SOUR:VOLT:SLEW?"))
            self._set_cache_valid(index=index)
        return self._output_slew_rate[index]

    # Tested on Chroma 62012P-80-60; working
    def _set_output_slew_rate(self, index, value):
        """
        This function sets the output voltage slew rate. Ranges for the 62000P series are:
        * 62006P-30-80: 0.001V/ms - 5V/ms
        * 62006P-100-25: 0.001V/ms - 10V/ms
        * 62006P-300-8: 0.001V/ms - 10V/ms
        * 62012P-40-120: 0.001V/ms - 5V/ms
        * 62012P-80-60: 0.001V/ms - 10V/ms
        * 62012P-100-50: 0.001V/ms - 10V/ms
        """
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            self._write("SOUR:VOLT:SLEW %.3f" % float(value))
        self._output_slew_rate[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False, index=k)
        self._set_cache_valid(index=index)
