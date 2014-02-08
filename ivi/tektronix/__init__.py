"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

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

# Function Generators
from .tektronixAWG2005 import tektronixAWG2005
from .tektronixAWG2020 import tektronixAWG2020
from .tektronixAWG2021 import tektronixAWG2021
from .tektronixAWG2040 import tektronixAWG2040
from .tektronixAWG2041 import tektronixAWG2041

# Power Supplies
from .tektronixPS2520G import tektronixPS2520G
from .tektronixPS2521G import tektronixPS2521G

# Optical attenuators
from .tektronixOA5002 import tektronixOA5002
from .tektronixOA5012 import tektronixOA5012
from .tektronixOA5022 import tektronixOA5022
from .tektronixOA5032 import tektronixOA5032

# Current probe amplifiers
from .tektronixAM5030 import tektronixAM5030
