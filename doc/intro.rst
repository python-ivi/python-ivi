==========================
Introduction to Python IVI
==========================

Overview
========
Python IVI is a Python-based interpretation of the Interchangeable Virtual
Instrument standard from the `IVI foundation`_.  The implementation is
pure Python and highly portable.  

It is released under the MIT license, see LICENSE_ for more
details.

Copyright (C) 2012-2014 Alex Forencich <alex@alexforencich.com>

See also:

- `Python IVI home page`_
- `GitHub repository`_
- `IVI Foundation`_

.. _LICENSE: appendix.html#license
.. _`Python IVI home page`: http://alexforencich.com/wiki/en/python-ivi/start
.. _`GitHub repository`: https://github.com/alexforencich/python-ivi
.. _`IVI Foundation`: http://www.ivifoundation.org/


Features
========
- Supports Python 2 and Python 3
- Pure Python
- Highly portable
- Communicates with instruments with various add-on modules

Requirements
============
- Python 2 or Python 3
- One or more communication extensions

Installation
============

To install the module for all users on the system, administrator rights (root)
are required.

From source
~~~~~~~~~~~
Download the archive, extract, and run::

    python setup.py install

Packages
~~~~~~~~
There are also packaged versions for some Linux distributions:

Arch Linux
    Python IVI is available under the name "python-ivi-git" in the AUR.

Instrument Communication Extensions
===================================

Python IVI does not contain any IO drivers itself.  In order to communicate
with an instrument, you must install one or more of the following drivers:

Python VXI11
~~~~~~~~~~~~

Python VXI11 provides a pure python TCP/IP driver for LAN based instruments
that support the VXI11 protocol.  This includes most LXI instruments and also
devices like the Agilent E2050 GPIB to LAN converter.  

Home page:
http://www.alexforencich.com/wiki/en/python-vxi11/start

GitHub repository:
https://github.com/alexforencich/python-vxi11

Python USBTMC
~~~~~~~~~~~~~

Python USBTMC provides a pure python USBTMC driver for instruments that
support the USB Test and Measurement Class.  Python USBTMC uses PyUSB to
connect to the instrument in a platform-independent manner.

Home page:
http://alexforencich.com/wiki/en/python-usbtmc/start

GitHub repository:
https://github.com/alexforencich/python-usbtmc

Linux GPIB
~~~~~~~~~~

Python IVI provides an interface wrapper for the Linux GPIB driver.  If the
Linux GPIB driver and its included Python interface available, Python IVI can
use it to communicate with instruments via any GPIB interface supported by
Linux GPIB.  

Home page:
http://linux-gpib.sourceforge.net/

pySerial
~~~~~~~~

Python IVI provides an interface wrapper for the pySerial library.  If
pySerial is installed, Python IVI can use it to communicate with instruments
via the serial port.  

Home page:
http://pyserial.sourceforge.net/
