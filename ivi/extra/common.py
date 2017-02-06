"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014-2017 Alex Forencich

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

class SerialNumber(ivi.IviContainer):
    "Extension IVI methods for instruments that can report a serial number"

    def __init__(self, *args, **kwargs):
        super(SerialNumber, self).__init__(*args, **kwargs)

        self._identity_instrument_serial_number = "Cannot query from instrument"

        self._add_property('identity.instrument_serial_number',
                        self._get_identity_instrument_serial_number,
                        None,
                        None,
                        """
                        Returns the serial number of the physical instrument. The IVI specific
                        driver returns the value it queries from the instrument or a string
                        indicating that it cannot query the instrument identity.

                        In some cases, it is not possible for the specific driver to query the
                        serial number of the instrument. This can occur when the Simulate
                        attribute is set to True or if the instrument is not capable of returning
                        the serial number. For these cases, the specific driver returns defined
                        strings for this attribute. If the Simulate attribute is set to True,
                        the specific driver returns "Not available while simulating" as the value
                        of this attribute. If the instrument is not capable of returning the
                        serial number and the Simulate attribute is set to False, the specific
                        driver returns "Cannot query from instrument" as the value of this
                        attribute.

                        The string that this attribute returns does not have a predefined maximum
                        length.
                        """)

    def _get_identity_instrument_serial_number(self):
        return self._identity_instrument_serial_number


class Memory(ivi.IviContainer):
    "Extension IVI methods for instruments that support storing configurations in internal memory"

    def __init__(self, *args, **kwargs):
        super(Memory, self).__init__(*args, **kwargs)

        self._memory_size = 10

        self._add_method('memory.save',
                        self._memory_save,
                        ivi.Doc("""
                        Stores the current state of the instrument into an internal storage
                        register.  Use memory.recall to restore the saved state.
                        """))
        self._add_method('memory.recall',
                        self._memory_recall,
                        ivi.Doc("""
                        Recalls the state of the instrument from an internal storage register
                        that was previously saved with memory.save.
                        """))

    def _memory_save(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        pass

    def _memory_recall(self, index):
        index = int(index)
        if index < 0 or index >= self._memory_size:
            raise OutOfRangeException()
        pass


class Title(ivi.IviContainer):
    "Extension IVI methods for instruments that support setting a title"

    def __init__(self, *args, **kwargs):
        super(Title, self).__init__(*args, **kwargs)

        self._display_title = ""

        self._add_property('display.title',
                        self._get_display_title,
                        self._set_display_title,
                        None,
                        ivi.Doc("""
                        Sets the instrument display title.
                        """))

    def _get_display_title(self):
        return self._display_title

    def _set_display_title(self, value):
        value = str(value)
        self._display_title = value


class SystemSetup(ivi.IviContainer):
    "Extension IVI methods for instruments that support fetching and reloading of the system setup"
    
    def __init__(self, *args, **kwargs):
        super(SystemSetup, self).__init__(*args, **kwargs)
        
        self._add_method('system.fetch_setup',
                        self._system_fetch_setup,
                        ivi.Doc("""
                        Returns the current instrument setup in the form of a binary block.  The
                        setup can be stored in memory or written to a file and then reloaded to the
                        instrument at a later time with system.load_setup.
                        """))
        self._add_method('system.load_setup',
                        self._system_load_setup,
                        ivi.Doc("""
                        Transfers a binary block of setup data to the instrument to reload a setup
                        previously saved with system.fetch_setup.
                        """))
    
    def _system_fetch_setup(self):
        return b''
    
    def _system_load_setup(self, data):
        pass


class Screenshot(ivi.IviContainer):
    "Extension IVI methods for instruments that support fetching screenshots"
    
    def __init__(self, *args, **kwargs):
        super(Screenshot, self).__init__(*args, **kwargs)
        
        self._add_method('display.fetch_screenshot',
                        self._display_fetch_screenshot,
                        ivi.Doc("""
                        Captures the screen and transfers it in the specified format.
                        The display graticule is optionally inverted.
                        """))
    
    def _display_fetch_screenshot(self, format='png', invert=False):
        return b''
    
    

