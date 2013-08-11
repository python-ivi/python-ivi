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
-------------------

.. autoclass:: Base
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.Base()
   i.help(m, complete=True, indent=3)

:class:`StdFunc` class
----------------------

.. autoclass:: StdFunc
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.StdFunc()
   i.help(m, complete=True, indent=3)

:class:`ArbWfm` class
---------------------

.. autoclass:: ArbWfm
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ArbWfm()
   i.help(m, complete=True, indent=3)

:class:`ArbChannelWfm` class
----------------------------

.. autoclass:: ArbChannelWfm
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ArbChannelWfm()
   i.help(m, complete=True, indent=3)

:class:`ArbWfmBinary` class
---------------------------

.. autoclass:: ArbWfmBinary
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ArbWfmBinary()
   i.help(m, complete=True, indent=3)

:class:`DataMarker` class
--------------------------

.. autoclass:: DataMarker
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.DataMarker()
   i.help(m, complete=True, indent=3)

:class:`SparseMarker` class
----------------------------

.. autoclass:: SparseMarker
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.SparseMarker()
   i.help(m, complete=True, indent=3)

:class:`ArbDataMask` class
--------------------------

.. autoclass:: ArbDataMask
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ArbDataMask()
   i.help(m, complete=True, indent=3)

:class:`ArbFrequency` class
---------------------------

.. autoclass:: ArbFrequency
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ArbFrequency()
   i.help(m, complete=True, indent=3)

:class:`ArbSeq` class
---------------------

.. autoclass:: ArbSeq
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ArbSeq()
   i.help(m, complete=True, indent=3)

:class:`ArbSeqDepth` class
--------------------------

.. autoclass:: ArbSeqDepth
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ArbSeqDepth()
   i.help(m, complete=True, indent=3)

:class:`Trigger` class
----------------------

.. autoclass:: Trigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.Trigger()
   i.help(m, complete=True, indent=3)

:class:`InternalTrigger` class
------------------------------

.. autoclass:: InternalTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.InternalTrigger()
   i.help(m, complete=True, indent=3)

:class:`SoftwareTrigger` class
------------------------------

.. autoclass:: SoftwareTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.SoftwareTrigger()
   i.help(m, complete=True, indent=3)

:class:`Burst` class
--------------------

.. autoclass:: Burst
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.Burst()
   i.help(m, complete=True, indent=3)

:class:`ModulateAM` class
-------------------------

.. autoclass:: ModulateAM
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ModulateAM()
   i.help(m, complete=True, indent=3)

:class:`ModulateFM` class
-------------------------

.. autoclass:: ModulateFM
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ModulateFM()
   i.help(m, complete=True, indent=3)

:class:`SampleClock` class
--------------------------

.. autoclass:: SampleClock
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.SampleClock()
   i.help(m, complete=True, indent=3)

:class:`TerminalConfiguration` class
------------------------------------

.. autoclass:: TerminalConfiguration
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.TerminalConfiguration()
   i.help(m, complete=True, indent=3)

:class:`StartTrigger` class
---------------------------

.. autoclass:: StartTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.StartTrigger()
   i.help(m, complete=True, indent=3)

:class:`StopTrigger` class
--------------------------

.. autoclass:: StopTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.StopTrigger()
   i.help(m, complete=True, indent=3)

:class:`HoldTrigger` class
--------------------------

.. autoclass:: HoldTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.HoldTrigger()
   i.help(m, complete=True, indent=3)

:class:`ResumeTrigger` class
----------------------------

.. autoclass:: ResumeTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.ResumeTrigger()
   i.help(m, complete=True, indent=3)

:class:`AdvanceTrigger` class
-----------------------------

.. autoclass:: AdvanceTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   i = ivi.Driver()
   m = ivi.fgen.AdvanceTrigger()
   i.help(m, complete=True, indent=3)
