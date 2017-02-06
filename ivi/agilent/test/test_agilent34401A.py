"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import io
import unittest

from .. import agilent34401A

class Virtual34401A(object):
    def __init__(self):
        self.read_buffer = io.BytesIO()
        self.tx_log = list()
        self.rx_log = list()
        self.cmd_log = list()

        self.cmds = {
            '*cls' : None,
            '*idn?' : str,
            '*rst' : None,
            '*trg' : None,
            '*tst?' : int,
            'system:error?' : str,
            'abort' : None,
            'fetch?' : float,
            'initiate' : None,
            'read?' : float,
            'sense:function' : 'qstr',
            'sense:function?' : 'qstr',
            'volt:dc:range' : float,
            'volt:dc:range?' : float,
            'volt:ac:range' : float,
            'volt:ac:range?' : float,
            'curr:dc:range' : float,
            'curr:dc:range?' : float,
            'curr:ac:range' : float,
            'curr:ac:range?' : float,
            'res:range' : float,
            'res:range?' : float,
            'fres:range' : float,
            'fres:range?' : float,
            'freq:range:lower' : float,
            'freq:range:lower?' : float,
            'per:range:lower' : float,
            'per:range:lower?' : float,
            'cap:range' : float,
            'cap:range?' : float,
            'volt:dc:range:auto' : int,
            'volt:dc:range:auto?' : int,
            'volt:ac:range:auto' : int,
            'volt:ac:range:auto?' : int,
            'curr:dc:range:auto' : int,
            'curr:dc:range:auto?' : int,
            'curr:ac:range:auto' : int,
            'curr:ac:range:auto?' : int,
            'res:range:auto' : int,
            'res:range:auto?' : int,
            'fres:range:auto' : int,
            'fres:range:auto?' : int,
            'freq:range:auto' : int,
            'freq:range:auto?' : int,
            'per:range:auto' : int,
            'per:range:auto?' : int,
            'cap:range:auto' : int,
            'cap:range:auto?' : int,
            'volt:dc:resolution' : float,
            'volt:dc:resolution?' : float,
            'volt:ac:resolution' : float,
            'volt:ac:resolution?' : float,
            'curr:dc:resolution' : float,
            'curr:dc:resolution?' : float,
            'curr:ac:resolution' : float,
            'curr:ac:resolution?' : float,
            'res:resolution' : float,
            'res:resolution?' : float,
            'fres:resolution' : float,
            'fres:resolution?' : float,
            'trigger:delay' : float,
            'trigger:delay?' : float,
            'trigger:delay:auto' : int,
            'trigger:delay:auto?' : int,
            'trigger:source' : str,
            'trigger:source?' : str,
            'sample:count' : int,
            'sample:count?' : int,
            'trigger:count' : int,
            'trigger:count?' : int,
        }
        self.vals = {
            '*idn' : 'HEWLETT-PACKARD,34401A,0,1.7-5.0-1.0',
            '*tst' : 0,
            'system:error' : '+0,"No error"',
            'fetch?' : 1.0,
            'read?' : 1.0,
            'sense:function' : 'dc_volts',
            'volt:dc:range' : 1.0,
            'volt:ac:range' : 1.0,
            'curr:dc:range' : 1.0,
            'curr:ac:range' : 1.0,
            'res:range' : 1.0,
            'fres:range' : 1.0,
            'freq:range:lower' : 1.0,
            'per:range:lower' : 1.0,
            'cap:range' : 1.0,
            'volt:dc:range:auto' : 1,
            'volt:ac:range:auto' : 1,
            'curr:dc:range:auto' : 1,
            'curr:ac:range:auto' : 1,
            'res:range:auto' : 1,
            'fres:range:auto' : 1,
            'freq:range:auto' : 1,
            'per:range:auto' : 1,
            'cap:range:auto' : 1,
            'volt:dc:resolution' : 0.001,
            'volt:ac:resolution' : 0.001,
            'curr:dc:resolution' : 0.001,
            'curr:ac:resolution' : 0.001,
            'res:resolution' : 0.001,
            'fres:resolution' : 0.001,
            'trigger:delay' : 0.01,
            'trigger:delay:auto' : 1,
            'trigger:source' : 'imm',
            'sample:count' : 1,
            'trigger:count' : 1,
        }

        for n in range(4):
            ch = 'output%d' % (n+1)
            self.cmds[ch+':voltage'] = float
            self.cmds[ch+':voltage?'] = float
            self.vals[ch+':voltage'] = 0.0

    def write_raw(self, data):
        self.rx_log.append(data)
        cmd = data.split(b' ')[0].decode()

        print("Got command %s" % cmd)

        cmd = cmd.lower().lstrip(':')

        self.cmd_log.append(cmd)

        t = self.cmds[cmd]

        if '?' in cmd:
            cmd = cmd.strip('?')

            if t is int:
                d = '{0:+d}'.format(self.vals[cmd]).encode()
                self.tx_log.append(d)
                self.read_buffer = io.BytesIO(d)
            elif t is float:
                d = '{0:+E}'.format(self.vals[cmd]).encode()
                self.tx_log.append(d)
                self.read_buffer = io.BytesIO(d)
            elif t is str:
                d = self.vals[cmd].encode()
                self.tx_log.append(d)
                self.read_buffer = io.BytesIO(d)
            elif t == 'qstr':
                d = '"{0}"'.format(self.vals[cmd]).encode()
                self.tx_log.append(d)
                self.read_buffer = io.BytesIO(d)
        else:
            if t is int:
                self.vals[cmd] = int(data.split(b' ')[1].decode())
            elif t is float:
                self.vals[cmd] = float(data.split(b' ')[1].decode())
            elif t is str:
                self.vals[cmd] = data.split(b' ')[1].decode()
            elif t == 'qstr':
                self.vals[cmd] = data.split(b' ')[1].decode().strip("'\"")

    def read_raw(self, num=-1):
        return self.read_buffer.read(num)


class TestAgilent34401A(unittest.TestCase):

    def setUp(self):
        self.vdmm = Virtual34401A()
        self.dmm = agilent34401A(self.vdmm)

    def test_idn_command(self):
        self.assertEqual(self.dmm.identity.instrument_manufacturer, 'HEWLETT-PACKARD')
        self.assertEqual(self.dmm.identity.instrument_model, '34401A')
        self.assertEqual(self.dmm.identity.instrument_serial_number, '0')
        self.assertEqual(self.dmm.identity.instrument_firmware_revision, '1.7-5.0-1.0')

    def test_reset(self):
        self.dmm.utility.reset()
        self.assertEqual('*rst' in self.vdmm.cmd_log, True)

    def test_self_test(self):
        self.dmm._self_test_delay = 0
        self.assertEqual(self.dmm.utility.self_test(), (0, 'Self test passed'))
        self.assertEqual('*tst?' in self.vdmm.cmd_log, True)

    def test_error_query(self):
        self.assertEqual(self.dmm.utility.error_query(), (0, 'No error'))
        self.vdmm.vals['system:error'] = '-113,"Undefined header"'
        self.assertEqual(self.dmm.utility.error_query(), (-113, 'Undefined header'))

    def test_measurement_function(self):
        mapping = {
            'dc_volts': 'volt',
            'ac_volts': 'volt:ac',
            'dc_current': 'curr',
            'ac_current': 'curr:ac',
            'two_wire_resistance': 'res',
            'four_wire_resistance': 'fres',
            'frequency': 'freq',
            'period': 'per',
            'capacitance': 'cap',
            'continuity': 'cont',
            'diode': 'diod'}

        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            for func in mapping:
                self.dmm.measurement_function = func
                self.assertEqual(self.vdmm.vals['sense:function'], mapping[func])
                self.assertEqual(self.dmm.measurement_function, func)
                self.dmm.measurement_function = 'dc_volts'
                self.assertEqual(self.vdmm.vals['sense:function'], mapping['dc_volts'])
                self.assertEqual(self.dmm.measurement_function, 'dc_volts')
                self.vdmm.vals['sense:function'] = mapping[func]
                self.assertEqual(self.vdmm.vals['sense:function'], mapping[func])
                if cache:
                    self.assertEqual(self.dmm.measurement_function, 'dc_volts')
                else:
                    self.assertEqual(self.dmm.measurement_function, func)

    def test_range(self):
        mapping = {
            'dc_volts': 'volt:dc:range',
            'ac_volts': 'volt:ac:range',
            'dc_current': 'curr:dc:range',
            'ac_current': 'curr:ac:range',
            'two_wire_resistance': 'res:range',
            'four_wire_resistance': 'fres:range',
            'capacitance': 'cap:range'}

        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            for func in mapping:
                self.dmm.measurement_function = func
                self.dmm.range = 1.0
                self.assertEqual(self.vdmm.vals[mapping[func]], 1.0)
                self.assertEqual(self.dmm.range, 1.0)
                self.dmm.range = 2.0
                self.assertEqual(self.vdmm.vals[mapping[func]], 10.0)
                self.assertEqual(self.dmm.range, 10.0)
                self.vdmm.vals[mapping[func]] = 1.0
                self.assertEqual(self.vdmm.vals[mapping[func]], 1.0)
                if cache:
                    self.assertEqual(self.dmm.range, 10.0)
                else:
                    self.assertEqual(self.dmm.range, 1.0)

    def test_range_auto(self):
        mapping = {
            'dc_volts': 'volt:dc:range:auto',
            'ac_volts': 'volt:ac:range:auto',
            'dc_current': 'curr:dc:range:auto',
            'ac_current': 'curr:ac:range:auto',
            'two_wire_resistance': 'res:range:auto',
            'four_wire_resistance': 'fres:range:auto',
            'capacitance': 'cap:range:auto'}

        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            for func in mapping:
                self.dmm.measurement_function = func
                self.dmm.auto_range = 'on'
                self.assertEqual(self.vdmm.vals[mapping[func]], 1)
                self.assertEqual(self.dmm.auto_range, 'on')
                self.dmm.auto_range = 'off'
                self.assertEqual(self.vdmm.vals[mapping[func]], 0)
                self.assertEqual(self.dmm.auto_range, 'off')
                self.vdmm.vals[mapping[func]] = 1
                self.assertEqual(self.vdmm.vals[mapping[func]], 1)
                if cache:
                    self.assertEqual(self.dmm.auto_range, 'off')
                else:
                    self.assertEqual(self.dmm.auto_range, 'on')

    def test_resolution(self):
        mapping = {
            'dc_volts': 'volt:dc:resolution',
            'ac_volts': 'volt:ac:resolution',
            'dc_current': 'curr:dc:resolution',
            'ac_current': 'curr:ac:resolution',
            'two_wire_resistance': 'res:resolution',
            'four_wire_resistance': 'fres:resolution'}

        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            for func in mapping:
                self.dmm.measurement_function = func
                self.dmm.resolution = 0.0001
                self.assertEqual(self.vdmm.vals[mapping[func]], 0.0001)
                self.assertEqual(self.dmm.resolution, 0.0001)
                self.dmm.resolution = 0.0002
                self.assertEqual(self.vdmm.vals[mapping[func]], 0.001)
                self.assertEqual(self.dmm.resolution, 0.001)
                self.vdmm.vals[mapping[func]] = 0.01
                self.assertEqual(self.vdmm.vals[mapping[func]], 0.01)
                if cache:
                    self.assertEqual(self.dmm.resolution, 0.001)
                else:
                    self.assertEqual(self.dmm.resolution, 0.01)

    def test_trigger_delay(self):
        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            self.dmm.trigger.delay = 0.01
            self.assertEqual(self.vdmm.vals['trigger:delay'], 0.01)
            self.assertEqual(self.dmm.trigger.delay, 0.01)
            self.dmm.trigger.delay = 0.1
            self.assertEqual(self.vdmm.vals['trigger:delay'], 0.1)
            self.assertEqual(self.dmm.trigger.delay, 0.1)
            self.vdmm.vals['trigger:delay'] = 1.0
            self.assertEqual(self.vdmm.vals['trigger:delay'], 1.0)
            if cache:
                self.assertEqual(self.dmm.trigger.delay, 0.1)
            else:
                self.assertEqual(self.dmm.trigger.delay, 1.0)

    def test_trigger_delay_auto(self):
        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            self.dmm.trigger.delay_auto = True
            self.assertEqual(self.vdmm.vals['trigger:delay:auto'], 1)
            self.assertEqual(self.dmm.trigger.delay_auto, True)
            self.dmm.trigger.delay_auto = False
            self.assertEqual(self.vdmm.vals['trigger:delay:auto'], 0)
            self.assertEqual(self.dmm.trigger.delay_auto, False)
            self.vdmm.vals['trigger:delay:auto'] = 1
            self.assertEqual(self.vdmm.vals['trigger:delay:auto'], 1)
            if cache:
                self.assertEqual(self.dmm.trigger.delay_auto, False)
            else:
                self.assertEqual(self.dmm.trigger.delay_auto, True)

    def test_trigger_source(self):
        mapping = {
            'bus': 'bus',
            'external': 'ext',
            'immediate': 'imm'}
        for cache in (True, False):
            for src in mapping:
                self.dmm.driver_operation.cache = cache
                self.dmm.trigger.source = src
                self.assertEqual(self.vdmm.vals['trigger:source'], mapping[src])
                self.assertEqual(self.dmm.trigger.source, src)
                self.dmm.trigger.source = 'immediate'
                self.assertEqual(self.vdmm.vals['trigger:source'], 'imm')
                self.assertEqual(self.dmm.trigger.source, 'immediate')
                self.vdmm.vals['trigger:source'] = mapping[src]
                self.assertEqual(self.vdmm.vals['trigger:source'], mapping[src])
                if cache:
                    self.assertEqual(self.dmm.trigger.source, 'immediate')
                else:
                    self.assertEqual(self.dmm.trigger.source, src)

    def test_measurement_abort(self):
        self.dmm.measurement.abort()
        self.assertEqual('abort' in self.vdmm.cmd_log, True)

    def test_measurement_fetch(self):
        self.vdmm.vals['fetch'] = 1.2345
        self.assertEqual(self.dmm.measurement.fetch(1.0), 1.2345)

    def test_measurement_initiate(self):
        self.dmm.measurement.initiate()
        self.assertEqual('initiate' in self.vdmm.cmd_log, True)

    def test_measurement_read(self):
        self.vdmm.vals['read'] = 1.2345
        self.assertEqual(self.dmm.measurement.read(1.0), 1.2345)

    def test_trigger_multi_point_sample_count(self):
        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            self.dmm.trigger.multi_point.sample_count = 10
            self.assertEqual(self.vdmm.vals['sample:count'], 10)
            self.assertEqual(self.dmm.trigger.multi_point.sample_count, 10)
            self.dmm.trigger.multi_point.sample_count = 20
            self.assertEqual(self.vdmm.vals['sample:count'], 20)
            self.assertEqual(self.dmm.trigger.multi_point.sample_count, 20)
            self.vdmm.vals['sample:count'] = 30
            self.assertEqual(self.vdmm.vals['sample:count'], 30)
            if cache:
                self.assertEqual(self.dmm.trigger.multi_point.sample_count, 20)
            else:
                self.assertEqual(self.dmm.trigger.multi_point.sample_count, 30)

    def test_trigger_multi_point_count(self):
        for cache in (True, False):
            self.dmm.driver_operation.cache = cache
            self.dmm.trigger.multi_point.count = 10
            self.assertEqual(self.vdmm.vals['trigger:count'], 10)
            self.assertEqual(self.dmm.trigger.multi_point.count, 10)
            self.dmm.trigger.multi_point.count = 20
            self.assertEqual(self.vdmm.vals['trigger:count'], 20)
            self.assertEqual(self.dmm.trigger.multi_point.count, 20)
            self.vdmm.vals['trigger:count'] = 30
            self.assertEqual(self.vdmm.vals['trigger:count'], 30)
            if cache:
                self.assertEqual(self.dmm.trigger.multi_point.count, 20)
            else:
                self.assertEqual(self.dmm.trigger.multi_point.count, 30)

    def test_send_sofware_trigger(self):
        self.dmm.send_software_trigger()
        self.assertEqual('*trg' in self.vdmm.cmd_log, True)

