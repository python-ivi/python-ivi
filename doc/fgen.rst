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
   obj = ivi.fgen.Base()
   ivi.help(obj, complete=True, indent=3)

:class:`StdFunc` class
----------------------

.. autoclass:: StdFunc
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.StdFunc()
   ivi.help(obj, complete=True, indent=3)

:class:`ArbWfm` class
---------------------

.. autoclass:: ArbWfm
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ArbWfm()
   ivi.help(obj, complete=True, indent=3)

:class:`ArbChannelWfm` class
----------------------------

.. autoclass:: ArbChannelWfm
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ArbChannelWfm()
   ivi.help(obj, complete=True, indent=3)

:class:`ArbWfmBinary` class
---------------------------

.. autoclass:: ArbWfmBinary
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ArbWfmBinary()
   ivi.help(obj, complete=True, indent=3)

:class:`DataMarker` class
--------------------------

.. autoclass:: DataMarker
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.DataMarker()
   ivi.help(obj, complete=True, indent=3)

:class:`SparseMarker` class
----------------------------

.. autoclass:: SparseMarker
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.SparseMarker()
   ivi.help(obj, complete=True, indent=3)

:class:`ArbDataMask` class
--------------------------

.. autoclass:: ArbDataMask
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ArbDataMask()
   ivi.help(obj, complete=True, indent=3)

:class:`ArbFrequency` class
---------------------------

.. autoclass:: ArbFrequency
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ArbFrequency()
   ivi.help(obj, complete=True, indent=3)

:class:`ArbSeq` class
---------------------

.. autoclass:: ArbSeq
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ArbSeq()
   ivi.help(obj, complete=True, indent=3)

:class:`ArbSeqDepth` class
--------------------------

.. autoclass:: ArbSeqDepth
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ArbSeqDepth()
   ivi.help(obj, complete=True, indent=3)

:class:`Trigger` class
----------------------

.. autoclass:: Trigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.Trigger()
   ivi.help(obj, complete=True, indent=3)

:class:`InternalTrigger` class
------------------------------

.. autoclass:: InternalTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.InternalTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`SoftwareTrigger` class
------------------------------

.. autoclass:: SoftwareTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.SoftwareTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`Burst` class
--------------------

.. autoclass:: Burst
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.Burst()
   ivi.help(obj, complete=True, indent=3)

:class:`ModulateAM` class
-------------------------

.. autoclass:: ModulateAM
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ModulateAM()
   ivi.help(obj, complete=True, indent=3)

:class:`ModulateFM` class
-------------------------

.. autoclass:: ModulateFM
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ModulateFM()
   ivi.help(obj, complete=True, indent=3)

:class:`SampleClock` class
--------------------------

.. autoclass:: SampleClock
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.SampleClock()
   ivi.help(obj, complete=True, indent=3)

:class:`TerminalConfiguration` class
------------------------------------

.. autoclass:: TerminalConfiguration
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.TerminalConfiguration()
   ivi.help(obj, complete=True, indent=3)

:class:`StartTrigger` class
---------------------------

.. autoclass:: StartTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.StartTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`StopTrigger` class
--------------------------

.. autoclass:: StopTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.StopTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`HoldTrigger` class
--------------------------

.. autoclass:: HoldTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.HoldTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`ResumeTrigger` class
----------------------------

.. autoclass:: ResumeTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.ResumeTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`AdvanceTrigger` class
-----------------------------

.. autoclass:: AdvanceTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.fgen.AdvanceTrigger()
   ivi.help(obj, complete=True, indent=3)
