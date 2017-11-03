#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 17:37:04 2017

@author: jonas
"""

from ivi.keithley import keithley2280S
import time
from matplotlib import pyplot

PSU = keithley2280S('TCPIP::172.20.0.49::INSTR', prefer_pyvisa=True, query_instr_status=True)
PSU.outputs[0].voltage_level=2.0
PSU.outputs[0].enabled = True
PSU.outputs[0].configure_measurement(
        type='current', 
        sample_count=100,
        measurement_range=0.1, 
        NPLC=0.02, 
        adc_autozero=False,
        auto_clear_buffer=True)

PSU.outputs[0].trigger_current_state = True
PSU.outputs[0].trigger_current_level = 1e-3
PSU.outputs[0].trace_points = 1000
PSU.outputs[0].trigger_sample_count = 20
PSU.outputs[0].trigger_count = 5

PSU.outputs[0].enabled = True
PSU.trigger.initiate()

V, t = PSU.outputs[0].fetch_measurement(measurement_type=('current', 'relative_time_seconds'))
pyplot.plot(V)