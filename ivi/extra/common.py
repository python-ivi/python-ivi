"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014 Alex Forencich

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

class Memory(object):
    "Extension IVI methods for instruments that support storing configurations in internal memory"
    
    def __init__(self, *args, **kwargs):
        super(Memory, self).__init__(*args, **kwargs)
        
        self._memory_size = 10
        
        ivi.add_method(self, 'memory.save',
                        self._memory_save,
                        ivi.Doc("""
                        Stores the current state of the instrument into an internal storage
                        register.  Use memory.recall to restore the saved state.
                        """))
        ivi.add_method(self, 'memory.recall',
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


class SystemSetup(object):
    "Extension IVI methods for instruments that support fetching and reloading of the system setup"
    
    def __init__(self, *args, **kwargs):
        super(SystemSetup, self).__init__(*args, **kwargs)
        
        ivi.add_method(self, 'system.fetch_setup',
                        self._system_fetch_setup,
                        ivi.Doc("""
                        Returns the current instrument setup in the form of a binary block.  The
                        setup can be stored in memory or written to a file and then reloaded to the
                        instrument at a later time with system.load_setup.
                        """))
        ivi.add_method(self, 'system.load_setup',
                        self._system_load_setup,
                        ivi.Doc("""
                        Transfers a binary block of setup data to the instrument to reload a setup
                        previously saved with system.fetch_setup.
                        """))
    
    def _system_fetch_setup(self):
        return b''
    
    def _system_load_setup(self, data):
        pass


class Screenshot(object):
    "Extension IVI methods for instruments that support fetching screenshots"
    
    def __init__(self, *args, **kwargs):
        super(Screenshot, self).__init__(*args, **kwargs)
        
        ivi.add_method(self, 'display.fetch_screenshot',
                        self._display_fetch_screenshot,
                        ivi.Doc("""
                        Captures the oscilloscope screen and transfers it in the specified format.
                        The display graticule is optionally inverted.
                        """))
    
    def _display_fetch_screenshot(self, format='png', invert=False):
        return b''
    
    

