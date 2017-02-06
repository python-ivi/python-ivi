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

from .. import colbyPDL10A

class VirtualPDL10A(object):
    def __init__(self):
        self.read_buffer = io.BytesIO()
        self.tx_log = list()
        self.rx_log = list()
        self.cmd_log = list()

        self.cmds = {
            '*cls' : None,
            '*idn?' : str,
            '*rst': None,
            '*tst?': int,
            'del?': float,
            'del': float,
            'err?': str,
            'mode?': str,
            'mode' : str,
        }
        self.vals = {
            '*idn': 'Colby Instruments Inc,PDL 10A5 ,123            ,V2.1',
            '*tst': 0,
            'del': 0.0,
            'err': '0',
            'mode': '',
        }

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
                d = '{0:d}'.format(self.vals[cmd]).encode()
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
        else:
            if t is int:
                self.vals[cmd] = int(data.split(b' ')[1].decode())
            elif t is float:
                self.vals[cmd] = float(data.split(b' ')[1].decode())
            elif t is str:
                self.vals[cmd] = data.split(b' ')[1].decode()

    def read_raw(self, num=-1):
        return self.read_buffer.read(num)


class TestColbyPDL10A(unittest.TestCase):

    def setUp(self):
        self.vpdl = VirtualPDL10A()
        self.pdl = colbyPDL10A(self.vpdl)

    def test_idn_command(self):
        self.assertEqual(self.pdl.identity.instrument_manufacturer, 'Colby Instruments Inc')
        self.assertEqual(self.pdl.identity.instrument_model, 'PDL 10A5')
        self.assertEqual(self.pdl.identity.instrument_serial_number, '123')
        self.assertEqual(self.pdl.identity.instrument_firmware_revision, 'V2.1')

    def test_reset(self):
        self.pdl.utility.reset()
        self.assertEqual('*rst' in self.vpdl.cmd_log, True)

    def test_self_test(self):
        self.pdl._self_test_delay = 0
        self.assertEqual(self.pdl.utility.self_test(), (0, 'Self test passed'))
        self.assertEqual('*tst?' in self.vpdl.cmd_log, True)

    def test_error_query(self):
        self.assertEqual(self.pdl.utility.error_query(), (0, '0'))
        self.vpdl.vals['err'] = '1;DE?;Parsed command unknown;Command Error;'
        self.assertEqual(self.pdl.utility.error_query(), (1, '1;DE?;Parsed command unknown;Command Error;'))

    def test_set_mode(self):
        for cache in (True, False):
            self.pdl.driver_operation.cache = cache
            self.pdl.mode = '625ps'
            self.assertEqual(self.vpdl.vals['mode'], '625ps')
            self.assertEqual(self.pdl.mode, '625ps')
            self.pdl.mode = '312.5ps'
            self.assertEqual(self.vpdl.vals['mode'], '312.5ps')
            self.assertEqual(self.pdl.mode, '312.5ps')
            self.vpdl.vals['mode'] = '625ps'
            self.assertEqual(self.vpdl.vals['mode'], '625ps')
            if cache:
                self.assertEqual(self.pdl.mode, '312.5ps')
            else:
                self.assertEqual(self.pdl.mode, '625ps')

    def test_set_delay(self):
        for cache in (True, False):
            self.pdl.driver_operation.cache = cache
            self.pdl.mode = '625ps'
            self.pdl.delay = 100.0e-12
            self.assertEqual(self.vpdl.vals['del'], 100.0e-12)
            self.assertEqual(self.pdl.delay, 100.0e-12)
            self.pdl.delay = 200.0e-12
            self.assertEqual(self.vpdl.vals['del'], 200.0e-12)
            self.assertEqual(self.pdl.delay, 200.0e-12)
            self.vpdl.vals['del'] = 100.0e-12
            self.assertEqual(self.vpdl.vals['del'], 100.0e-12)
            if cache:
                self.assertEqual(self.pdl.delay, 200.0e-12)
            else:
                self.assertEqual(self.pdl.delay, 100.0e-12)

