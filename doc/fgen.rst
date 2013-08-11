============================================
:mod:`ivi.fgen` --- Function Generator class
============================================

.. module:: ivi.fgen
   :synopsis: DC power supply base class

This module provides the base functionality for Function Generators.

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
   m = ivi.fgen.Base()
   i.help(m, complete=True, indent=3)
