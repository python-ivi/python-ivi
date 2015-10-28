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


class ApertureTime(ivi.IviContainer):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in seconds

    This is a base class to keep common code in one place. You should use subclasses like DCApertureTime"""

    def __init__(self, *args, **kwargs):
        super(ApertureTime, self).__init__(*args, **kwargs)

    def _set_aperture_time(self, mode, value):
        raise NotImplementedError()

    def _get_aperture_time(self, mode):
        raise NotImplementedError()

    def _set_aperture_time(self, mode, value):
        raise NotImplementedError()

    def _get_aperture_time(self, mode):
        raise NotImplementedError()


class ApertureNPLC(ivi.IviContainer):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in power line cycles

    This is a base class to keep common code in one place. You should use subclasses like DCApertureNPLC"""

    def __init__(self, *args, **kwargs):
        super(ApertureNPLC, self).__init__(*args, **kwargs)

    def _set_aperture_nplc(self, mode, value):
        if not self._driver_operation_simulate:
            raise NotImplementedError()

    def _get_aperture_nplc(self, mode):
        if not self._driver_operation_simulate:
            raise NotImplementedError()
        else:
            return 1.


class VoltageApertureTime(ApertureTime):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in Voltage mode"""

    def __init__(self, *args, **kwargs):
        super(VoltageApertureTime, self).__init__(*args, **kwargs)
        self._add_property('voltage.aperture.time',
            self._get_voltage_aperture_time,
            self._set_voltage_aperture_time)

        self._add_property('voltage.aperture.time_enabled',
            self._get_voltage_aperture_time_enabled,
            self._set_voltage_aperture_time_enabled)



    def _set_voltage_aperture_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time('voltage', value)
        self._voltage_aperture_time = value
        self._set_cache_valid()

    def _get_voltage_aperture_time(self):
        if not self._get_cache_valid():
            self._voltage_aperture_time = self._get_aperture_time('voltage')
            self._set_cache_valid()
        return self._voltage_aperture_time

    def _set_voltage_aperture_time_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time_enabled('voltage', value)
        self._voltage_aperture_time_enabled = value
        self._set_cache_valid()

    def _get_voltage_aperture_time_enabled(self):
        if not self._get_cache_valid():
            self._voltage_aperture_time_enabled = self._get_aperture_time_enabled('voltage')
            self._set_cache_valid()
        return self._voltage_aperture_time_enabled



class VoltageApertureNPLC(ApertureNPLC):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in Voltage mode"""

    def __init__(self, *args, **kwargs):
        super(VoltageApertureNPLC, self).__init__(*args, **kwargs)

        self._add_property('voltage.aperture.nplc',
            self._get_voltage_aperture_nplc,
            self._set_voltage_aperture_nplc)

    def _set_voltage_aperture_nplc(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_nplc('voltage', value)
        self._voltage_aperture_nplc = value
        self._set_cache_valid()

    def _get_voltage_aperture_nplc(self):
        if not self._get_cache_valid():
            self._voltage_aperture_nplc = self._get_aperture_nplc('voltage')
            self._set_cache_valid()
        return self._voltage_aperture_nplc



class ResistanceApertureTime(ApertureTime):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in resistance mode"""

    def __init__(self, *args, **kwargs):
        super(ResistanceApertureTime, self).__init__(*args, **kwargs)
        self._add_property('resistance.aperture.time',
            self._get_resistance_aperture_time,
            self._set_resistance_aperture_time)

        self._add_property('resistance.aperture.time_enabled',
            self._get_resistance_aperture_time_enabled,
            self._set_resistance_aperture_time_enabled)



    def _set_resistance_aperture_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time('resistance', value)
        self._resistance_aperture_time = value
        self._set_cache_valid()

    def _get_resistance_aperture_time(self):
        if not self._get_cache_valid():
            self._resistance_aperture_time = self._get_aperture_time('resistance')
            self._set_cache_valid()
        return self._resistance_aperture_time

    def _set_resistance_aperture_time_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time_enabled('resistance', value)
        self._resistance_aperture_time_enabled = value
        self._set_cache_valid()

    def _get_resistance_aperture_time_enabled(self):
        if not self._get_cache_valid():
            self._resistance_aperture_time_enabled = self._get_aperture_time_enabled('resistance')
            self._set_cache_valid()
        return self._resistance_aperture_time_enabled



class ResistanceApertureNPLC(ApertureNPLC):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in resistance mode"""

    def __init__(self, *args, **kwargs):
        super(ResistanceApertureNPLC, self).__init__(*args, **kwargs)

        self._add_property('resistance.aperture.nplc',
            self._get_resistance_aperture_nplc,
            self._set_resistance_aperture_nplc)

    def _set_resistance_aperture_nplc(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_nplc('resistance', value)
        self._resistance_aperture_nplc = value
        self._set_cache_valid()

    def _get_resistance_aperture_nplc(self):
        if not self._get_cache_valid():
            self._resistance_aperture_nplc = self._get_aperture_nplc('resistance')
            self._set_cache_valid()
        return self._resistance_aperture_nplc

class CurrentApertureTime(ApertureTime):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in Current mode"""

    def __init__(self, *args, **kwargs):
        super(CurrentApertureTime, self).__init__(*args, **kwargs)
        self._add_property('current.aperture.time',
            self._get_current_aperture_time,
            self._set_current_aperture_time)

        self._add_property('current.aperture.time_enabled',
            self._get_current_aperture_time_enabled,
            self._set_current_aperture_time_enabled)

    def _set_current_aperture_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time('current', value)
        self._current_aperture_time = value
        self._set_cache_valid()

    def _get_current_aperture_time(self):
        if not self._get_cache_valid():
            self._current_aperture_time = self._get_aperture_time('current')
            self._set_cache_valid()
        return self._current_aperture_time

    def _set_current_aperture_time_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time_enabled('current', value)
        self._current_aperture_time_enabled = value
        self._set_cache_valid()

    def _get_current_aperture_time_enabled(self):
        if not self._get_cache_valid():
            self._current_aperture_time_enabled = self._get_aperture_time_enabled('current')
            self._set_cache_valid()
        return self._current_aperture_time_enabled



class CurrentApertureNPLC(ApertureNPLC):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in Current mode"""

    def __init__(self, *args, **kwargs):
        super(CurrentApertureNPLC, self).__init__(*args, **kwargs)

        self._add_property('current.aperture.nplc',
            self._get_current_aperture_nplc,
            self._set_current_aperture_nplc)

    def _set_current_aperture_nplc(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_nplc('current', value)
        self._current_aperture_nplc = value
        self._set_cache_valid()

    def _get_current_aperture_nplc(self):
        if not self._get_cache_valid():
            self._current_aperture_nplc = self._get_aperture_nplc('current')
            self._set_cache_valid()
        return self._current_aperture_nplc



class TemperatureApertureTime(ApertureTime):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in Temperature mode"""

    def __init__(self, *args, **kwargs):
        super(TemperatureApertureTime, self).__init__(*args, **kwargs)
        self._add_property('temperature.aperture.time',
            self._get_temperature_aperture_time,
            self._set_temperature_aperture_time)

        self._add_property('temperature.aperture.time_enabled',
            self._get_temperature_aperture_time_enabled,
            self._set_temperature_aperture_time_enabled)

    def _set_temperature_aperture_time(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time('temperature', value)
        self._temperature_aperture_time = value
        self._set_cache_valid()

    def _get_temperature_aperture_time(self):
        if not self._get_cache_valid():
            self._temperature_aperture_time = self._get_aperture_time('temperature')
            self._set_cache_valid()
        return self._temperature_aperture_time

    def _set_temperature_aperture_time_enabled(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._set_aperture_time_enabled('temperature', value)
        self._temperature_aperture_time_enabled = value
        self._set_cache_valid()

    def _get_temperature_aperture_time_enabled(self):
        if not self._get_cache_valid():
            self._temperature_aperture_time_enabled = self._get_aperture_time_enabled('temperature')
            self._set_cache_valid()
        return self._temperature_aperture_time_enabled



class TemperatureApertureNPLC(ApertureNPLC):
    """Extension IVI methods for instruments that support selecting the measurement aperture (integration time) in Temperature mode"""

    def __init__(self, *args, **kwargs):
        super(TemperatureApertureNPLC, self).__init__(*args, **kwargs)

        self._add_property('temperature.aperture.nplc',
            self._get_temperature_aperture_nplc,
            self._set_temperature_aperture_nplc)

    def _set_temperature_aperture_nplc(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._set_aperture_nplc('temperature', value)
        self._temperature_aperture_nplc = value
        self._set_cache_valid()

    def _get_temperature_aperture_nplc(self):
        if not self._get_cache_valid():
            self._temperature_aperture_nplc = self._get_aperture_nplc('temperature')
            self._set_cache_valid()
        return self._temperature_aperture_nplc