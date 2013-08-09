==========================================
:mod:`ivi.dcpwr` --- DC power supply class
==========================================

.. module:: ivi.dcpwr
   :synopsis: DC power supply base class

This module provides the base functionality for DC power supplies.

Functions and Exceptions
------------------------

.. exception:: IviException

   Exception raised on various occasions; argument is a string describing what
   is wrong.

:class:`Base` class
-------------------------

.. autoclass:: Base
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.dcpwr.Base()
   i.help(m, complete=True, indent=3)

:class:`Trigger` class
----------------------

.. autoclass:: Trigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.dcpwr.Trigger()
   i.help(m, complete=True, indent=3)

:class:`SoftwareTrigger` class
------------------------------

.. autoclass:: SoftwareTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.dcpwr.SoftwareTrigger()
   i.help(m, complete=True, indent=3)

:class:`Measurement` class
--------------------------

.. autoclass:: Measurement
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.dcpwr.Measurement()
   i.help(m, complete=True, indent=3)
