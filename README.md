# Python IVI Readme

For more information and updates:
http://alexforencich.com/wiki/en/python-ivi/start

GitHub repository:
https://github.com/alexforencich/python-ivi

## Introduction

Python IVI is a Python-based interpretation of the Interchangeable Virtual
Instrument standard from the [IVI foundation](http://www.ivifoundation.org/).

## Included drivers

  * Oscilloscopes (scope):
    * Agilent InfiniiVision 7000A/B series
    * Agilent Infiniium 90000A/90000X series
  * Function Generators (fgen):
    * Tektronix AWG2000 series
  * DC Power Supplies (dcpwr):
    * Tektronix PS2520G/PS2521G
    * Agilent E3600A series
  * RF Power Meters (pwrmeter):
    * Agilent 436A
  * RF Signal Generators (rfsiggen):
    * Agilent 8642 A/B

## Instrument communication

Python IVI can use Python VXI-11, Python USBTMC, pySerial and linux-gpib to
connect to instruments.  The implementation of the initialize method takes a
VISA resource string and attempts to connect to an instrument.  If the resource
string starts with TCPIP, then Python IVI will attempt to use Python VXI-11.
If it starts with USB, it attempts to use Python USBTMC.  If it starts with
GPIB, it will attempt to use linux-gpib's python interface.  If it starts with
ASRL, it attemps to use pySerial.  Integration with PyVISA is planned, but not
currently supported.  

## A note on standards compliance

As the IVI standard only specifies the API for C, COM, and .NET, a Python
implementation is inherently not compliant and hence this is not an
implementation of the standard, but an interpretation that tries to remain
as faithful as possibe while presenting a uniform, easy-to-use, sensible,
python-style interface.

The Python IVI library is a Pythonized version of the .NET and COM IVI API
specifications, with the CamelCase for everything but the class names replaced
with lowercase_with_underscores.  The library most closely follows the .NET
standard, with the calls that would require the .NET helper classes follwing
the corresponding COM specifications.  There are some major deviations from
the specification in order to be consistent with the spirit of the other IVI
specifications.  The fgen class is the most obvious example of this, using
properties instead of the getters and setters as required by the IVI
specification.  

## Installation

Extract and run

    # python setup.py install

## Usage examples

This sample Python code will use Python IVI to connect to an Agilent MSO7104A
over LXI (VXI-11), configure the timebase, trigger, and channel 1, capture a
waveform, and read it out of the instrument.  

    # import Python IVI
    import ivi
    # connect to MSO7104A via LXI
    mso = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR")
    # connect to MSO7104A via USBTMC
    #mso = ivi.agilent.agilentMSO7104A("USB0::2391::5973::MY********::INSTR")
    # configure timebase
    mso.acquisition.time_per_record = 1e-3
    # configure triggering
    mso.trigger.type = 'edge'
    mso.trigger.source = 'channel1'
    mso.trigger.coupling = 'dc'
    mso.trigger.edge.slope = 'positive'
    mso.trigger.level = 0
    # configure channel
    mso.channels['channel1'].enabled = True
    mso.channels['channel1'].offset = 0
    mso.channels['channel1'].range = 4
    mso.channels['channel1'].coupling = 'dc'
    # initiate measurement
    mso.measurement.initiate()
    # read out channel 1 waveform data
    waveform = mso.channels[0].measurement.fetch_waveform()
    # measure peak-to-peak voltage
    vpp = mso.channels[0].measurement.fetch_waveform_measurement("voltage_peak_to_peak")
    # measure phase
    phase = mso.channels['channel1'].measurement.fetch_waveform_measurement("phase", "channel2")

This sample Python code will use Python IVI to connect to a Tektronix AWG2021,
generate a sinewave with numpy, and transfer it to channel 1.  

    # import Python IVI
    import ivi
    # import numpy
    from numpy import *
    # connect to AWG2021 via GPIB
    #awg = ivi.tektronix.tektronixAWG2021("GPIB0::25::INSTR")
    # connect to AWG2021 via E2050A GPIB to VXI11 bridge
    awg = ivi.tektronix.tektronixAWG2021("TCPIP0::192.168.1.105::gpib,25::INSTR")
    # connect to AWG2021 via serial
    #awg = ivi.tektronix.tektronixAWG2021("ASRL::/dev/ttyUSB0,9600::INSTR")
    # create a waveform
    n = 128
    f = 1
    a = 1
    wfm = a*sin(2*pi/n*f*arange(0,n))
    # transfer to AWG2021
    awg.outputs[0].arbitrary.create_waveform(wfm)
    # 2 volts peak to peak
    awg.outputs[0].arbitrary.gain = 2.0
    # zero offset
    awg.outputs[0].arbitrary.gain = 0.0
    # sample rate 128 MHz
    arb.arbitrary.sample_rate = 128e6
    # enable ouput
    awg.outputs[0].enabled = True

This sample Python code will use Python IVI to connect to an Agilent E3649A
and configure an output.

    # import Python IVI
    import ivi
    # connect to E3649A via GPIB
    #psu = ivi.agilent.agilentE3649A("GPIB0::5::INSTR")
    # connect to E3649A via E2050A GPIB to VXI11 bridge
    psu = ivi.agilent.agilentE3649A("TCPIP0::192.168.1.105::gpib,5::INSTR")
    # connect to E3649A via serial
    #psu = ivi.agilent.agilentE3649A("ASRL::/dev/ttyUSB0,9600::INSTR")
    # configure output
    psu.outputs[0].configure_range('voltage', 12)
    psu.outputs[0].voltage_level = 12.0
    psu.outputs[0].current_limit = 1.0
    psu.outputs[0].ovp_limit = 14.0
    psu.outputs[0].ovp_enabled = True
    psu.outptus[0].enabled = True
