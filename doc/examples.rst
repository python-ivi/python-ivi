===================
Python IVI Examples
===================

Connecting to an Instrument
===========================

Connect to an Agilent MSO7104A oscilloscope over LXI (VXI11) on IP address 192.168.1.104::

    >>> import ivi
    >>> mso = ivi.agilent.agilentMSO7104A("TCPIP::192.168.1.104::INSTR")
    >>> mso.identity.instrument_model
    'MSO7104A'

Connect to an Agilent E3649A via an HP 2050A GPIB LAN bridge::

    >>> import ivi
    >>> psu = ivi.agilent.agilentE3649A("TCPIP::192.168.1.105::gpib,5::INSTR")
    >>> psu.identity.instrument_model
    'E3649A'

Configuring instruments
=======================

Connect to an Agilent MSO7104A oscilloscope over LXI (VXI11) and configure a channel::

    >>> import ivi
    >>> mso = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR")
    >>> #mso = ivi.agilent.agilentMSO7104A("USB0::2391::5973::MY********::INSTR")
    >>> mso.acquisition.time_per_record = 1e-3
    >>> mso.trigger.type = 'edge'
    >>> mso.trigger.source = 'channel1'
    >>> mso.trigger.coupling = 'dc'
    >>> mso.trigger.edge.slope = 'positive'
    >>> mso.trigger.level = 0
    >>> mso.channels['channel1'].enabled = True
    >>> mso.channels['channel1'].offset = 0
    >>> mso.channels['channel1'].range = 4
    >>> mso.channels['channel1'].coupling = 'dc'
    >>> mso.measurement.initiate()
    >>> waveform = mso.channels[0].measurement.fetch_waveform()
    >>> vpp = mso.channels[0].measurement.fetch_waveform_measurement("voltage_peak_to_peak")
    >>> phase = mso.channels['channel1'].measurement.fetch_waveform_measurement("phase", "channel2")

Connect to a Tektronix AWG2021, generate a sinewave with numpy, and transfer it to channel 1::

    >>> import ivi
    >>> from numpy import *
    >>> #awg = ivi.tektronix.tektronixAWG2021("GPIB0::25::INSTR")
    >>> awg = ivi.tektronix.tektronixAWG2021("TCPIP0::192.168.1.105::gpib,25::INSTR")
    >>> #awg = ivi.tektronix.tektronixAWG2021("ASRL::/dev/ttyUSB0,9600::INSTR")
    >>> n = 128
    >>> f = 1
    >>> a = 1
    >>> wfm = a*sin(2*pi/n*f*arange(0,n))
    >>> awg.outputs[0].arbitrary.create_waveform(wfm)
    >>> awg.outputs[0].arbitrary.gain = 2.0
    >>> awg.outputs[0].arbitrary.gain = 0.0
    >>> arb.arbitrary.sample_rate = 128e6
    >>> awg.outputs[0].enabled = True

Connect to an Agilent E3649A and configure an output::

    >>> import ivi
    >>> #psu = ivi.agilent.agilentE3649A("GPIB0::5::INSTR")
    >>> psu = ivi.agilent.agilentE3649A("TCPIP0::192.168.1.105::gpib,5::INSTR")
    >>> #psu = ivi.agilent.agilentE3649A("ASRL::/dev/ttyUSB0,9600::INSTR")
    >>> psu.outputs[0].configure_range('voltage', 12)
    >>> psu.outputs[0].voltage_level = 12.0
    >>> psu.outputs[0].current_limit = 1.0
    >>> psu.outputs[0].ovp_limit = 14.0
    >>> psu.outputs[0].ovp_enabled = True
    >>> psu.outptus[0].enabled = True

