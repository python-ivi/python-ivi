=======================================
:mod:`ivi.scope` --- Oscilloscope class
=======================================

.. module:: ivi.scope
   :synopsis: Oscilloscope base class

This module provides the base functionality for Oscilloscopes.

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
   obj = ivi.scope.Base()
   ivi.help(obj, complete=True, indent=3)

:class:`Interpolation` class
----------------------------

.. autoclass:: Interpolation
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.Interpolation()
   ivi.help(obj, complete=True, indent=3)

:class:`TVTrigger` class
------------------------

.. autoclass:: TVTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.TVTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`RuntTrigger` class
--------------------------

.. autoclass:: RuntTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.RuntTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`GlitchTrigger` class
----------------------------

.. autoclass:: GlitchTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.GlitchTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`WidthTrigger` class
---------------------------

.. autoclass:: WidthTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.WidthTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`AcLineTrigger` class
----------------------------

.. autoclass:: AcLineTrigger
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.AcLineTrigger()
   ivi.help(obj, complete=True, indent=3)

:class:`WaveformMeasurement` class
----------------------------------

.. autoclass:: WaveformMeasurement
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.WaveformMeasurement()
   ivi.help(obj, complete=True, indent=3)

:class:`MinMaxWaveform` class
-----------------------------

.. autoclass:: MinMaxWaveform
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.MinMaxWaveform()
   ivi.help(obj, complete=True, indent=3)

:class:`ProbeAutoSense` class
-----------------------------

.. autoclass:: ProbeAutoSense
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.ProbeAutoSense()
   ivi.help(obj, complete=True, indent=3)

:class:`ContinuousAcquisition` class
------------------------------------

.. autoclass:: ContinuousAcquisition
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.ContinuousAcquisition()
   ivi.help(obj, complete=True, indent=3)

:class:`AverageAcquisition` class
---------------------------------

.. autoclass:: AverageAcquisition
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.AverageAcquisition()
   ivi.help(obj, complete=True, indent=3)

:class:`SampleMode` class
-------------------------

.. autoclass:: SampleMode
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.SampleMode()
   ivi.help(obj, complete=True, indent=3)

:class:`TriggerModifier` class
------------------------------

.. autoclass:: TriggerModifier
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.TriggerModifier()
   ivi.help(obj, complete=True, indent=3)

:class:`AutoSetup` class
------------------------

.. autoclass:: AutoSetup
   :members:
   :show-inheritance:
   
.. exec::
   import ivi
   obj = ivi.scope.AutoSetup()
   ivi.help(obj, complete=True, indent=3)

