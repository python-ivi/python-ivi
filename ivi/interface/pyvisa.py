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

import io
import sys

try:
    import visa
except ImportError:
    # PyVISA not installed, pass it up
    raise ImportError
except:
    # any other error
    e = sys.exc_info()[1]
    sys.stderr.write("python-ivi: PyVISA is installed, but could not be loaded (%s: %s)\n" %
        (e.__class__.__name__, e.args[0]))
    raise ImportError

class PyVisaInstrument:
    "PyVisa wrapper instrument interface client"
    def __init__(self, resource, *args, **kwargs):
        if type(resource) is str:
            self.instrument = visa.instrument(resource, *args, **kwargs)
        else:
            self.instrument = resource
        
        self.buffer = io.BytesIO()

    def write_raw(self, data):
        "Write binary data to instrument"
        
        self.instrument.write(data)

    def read_raw(self, num=-1):
        "Read binary data from instrument"
        
        # PyVISA only supports reading entire buffer
        #return self.instrument.read_raw()
        
        data = self.buffer.read(num)
        
        if len(data) == 0:
            self.buffer = io.BytesIO(self.instrument.read_raw())
            data = self.buffer.read(num)
        
        return data
    
    def ask_raw(self, data, num=-1):
        "Write then read binary data"
        self.write_raw(data)
        return self.read_raw(num)
    
    def write(self, message, encoding = 'utf-8'):
        "Write string to instrument"
        if type(message) is tuple or type(message) is list:
            # recursive call for a list of commands
            for message_i in message:
                self.write(message_i, encoding)
            return
        
        self.write_raw(str(message).encode(encoding))

    def read(self, num=-1, encoding = 'utf-8'):
        "Read string from instrument"
        return self.read_raw(num).decode(encoding).rstrip('\r\n')

    def ask(self, message, num=-1, encoding = 'utf-8'):
        "Write then read string"
        if type(message) is tuple or type(message) is list:
            # recursive call for a list of commands
            val = list()
            for message_i in message:
                val.append(self.ask(message_i, num, encoding))
            return val
        
        self.write(message, encoding)
        return self.read(num, encoding)
    
    def read_stb(self):
        "Read status byte"
        raise NotImplementedError()
    
    def trigger(self):
        "Send trigger command"
        
        self.instrument.trigger()
    
    def clear(self):
        "Send clear command"
        raise NotImplementedError()
    
    def remote(self):
        "Send remote command"
        raise NotImplementedError()
    
    def local(self):
        "Send local command"
        raise NotImplementedError()
    
    def lock(self):
        "Send lock command"
        raise NotImplementedError()
    
    def unlock(self):
        "Send unlock command"
        raise NotImplementedError()

