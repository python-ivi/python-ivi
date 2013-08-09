=========================
:mod:`ivi` --- IVI driver
=========================

.. module:: ivi
   :synopsis: IVI driver

This module provides the base functionality of an IVI instrument driver.

Functions and Exceptions
------------------------

.. exception:: IviException

   Exception raised on various occasions; argument is a string describing what
   is wrong.

:class:`DriverOperation` class
------------------------------

.. autoclass:: DriverOperation
   :members:
   :show-inheritance:

:class:`DriverIdentity` class
-----------------------------

.. autoclass:: DriverIdentity
   :members:
   :show-inheritance:

:class:`DriverUtility` class
----------------------------

.. autoclass:: DriverUtility
   :members:
   :show-inheritance:

:class:`Driver` class
-------------------------

.. autoclass:: Driver
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   m = ivi.Driver()
   m.help(complete=True, indent=3)

Helper Classes
--------------

:class:`PropertyCollection` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: PropertyCollection
   :members:
   :private-members:

:class:`IndexedPropertyCollection` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: IndexedPropertyCollection
   :members:
   :private-members:
