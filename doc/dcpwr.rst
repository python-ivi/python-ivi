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
   obj = ivi.dcpwr.Base()
   ivi.help(obj, complete=True, indent=3)

:class:`Trigger` class
----------------------

.. autoclass:: Trigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.dcpwr.Trigger()
   ivi.help(obj, complete=True, indent=3)

:class:`SoftwareTrigger` class
------------------------------

.. autoclass:: SoftwareTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.dcpwr.SoftwareTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`Measurement` class
--------------------------

.. autoclass:: Measurement
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.dcpwr.Measurement()
   ivi.help(obj, complete=True, indent=3)
