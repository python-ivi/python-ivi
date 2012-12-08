# Python IVI Readme

For more information and updates:
http://alexforencich.com/wiki/en/python-ivi/start

GitHub repository:
https://github.com/alexforencich/python-ivi

Python IVI is a Python-based interpretation of the Interchangeable Virtual
Instrument standard from the [IVI foundation](http://www.ivifoundation.org/).

## Included drivers

  * DC Power Supplies (dcpwr):
    * Tektronix PS2520G/PS2521G
    * Agilent E3600A series
  * Function Generators (fgen):
    * Tektronix AWG2000 series
  * RF Signal Generators (rfsiggen):
    * Agilent 8642 A/B
  * Oscilloscopes (scope):
    * Agilent InfiniiVision 7000A series

## Instrument communication

Python IVI can use Python VXI11, pySerial and linux-gpib to connect to
instruments.  The implementation of the initialize method takes a VISA
resource string and attempts to connect to an instrument.  If the resource
string starts with TCPIP, then Python IVI will attempt to use Python VXI11.
If it starts with GPIB, it will attempt to use linux-gpib's python interface.
If it starts with ASRL, it attemps to use pySerial.  Integration with PyVISA
is planned, but not currently supported.  

## A note on standards compliance

As the IVI standard only specifies the API for C, COM, and .NET, a Python
implementation is inherently not compliant and hence this is not an
implementation of the standard, but an interpretation that tries to remain
as faithful as possibe while presenting a uniform, easy-to-use, sensible,
python-style interface.

The PyIVI library is a Pythonized version of the .NET and COM IVI API
specifications, with the CamelCase for everything but the class names replaced
with lowercase_with_underscores.  The library most closely follows the .NET
standard, with the calls that would require the .NET helper classes follwing
the corresponding COM specifications.  There are some major deviations from
the specification in order to be consistent with the spirit of the other IVI
specifications.  The fgen class is the most obvious example of this, using
properties instead of the getters and setters as required by the IVI
specification.  

## Usage example

This sample Python code will use Python IVI to connect to an Agilent MSO7104A
over LXI (VXI11), configure the timebase, trigger, and channel 1, capture a
waveform, and read it out of the instrument.  

    # import Python IVI
    import ivi
    # connect to MSO7104A via LXI
    mso = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR")
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
    
