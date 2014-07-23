# -*- coding: utf-8 -*-
# Copyright (c) 2014 The python-ivi developers. All rights reserved.
# Project site: https://github.com/python-ivi/python-ivi
# Use of this source code is governed by a MIT-style license that
# can be found in the COPYING file for the project.
"""Unit tests for agilentMSOX3024A.py.
"""

import unittest

from ivi.agilent.agilentMSOX3024A import agilentMSOX3024A


class TestAgilentMSOX3024A(unittest.TestCase):

    def setUp(self):  # NOQA
        self.scope = agilentMSOX3024A()

    def test_identity_description(self):
        self.assertEqual(
            self.scope._identity_description,
            'Agilent InfiniiVision 3000A X-series IVI oscilloscope driver')

    def test_identity_support_instrument_model(self):
        self.assertIn('MSOX3024A',
                      self.scope._identity_supported_instrument_models)

    def test_analog_channel_count(self):
        self.assertEqual(self.scope._analog_channel_count, 4)

    def test_analog_channel_name(self):
        analog_channel_names = ['channel{}'.format(x) for x in range(1, 5)]
        self.assertEqual(
            self.scope._analog_channel_name,
            analog_channel_names)

    def test_digital_channel_count(self):
        self.assertEqual(self.scope._digital_channel_count, 16)

    def test_digital_channel_name(self):
        digital_channel_names = ['digital{}'.format(x) for x in range(16)]
        self.assertEqual(
            self.scope._digital_channel_name,
            digital_channel_names)

    def test_channel_count(self):
        self.assertEqual(self.scope._channel_count, 20)

    def test_bandwidth(self):
        self.assertEqual(self.scope._bandwidth, 200e6)

    def test_wavegen_output_count(self):
        self.assertEqual(self.scope._output_count, 1)

    def test_output_standard_waveform_mapping(self):
        waveforms = ('sine', 'square', 'ramp_up', 'pulse', 'noise',
                     'dc', 'sinc', 'exprise', 'expfall', 'cardiac', 'gaussian')
        for waveform in waveforms:
            self.assertIn(
                waveform, self.scope._output_standard_waveform_mapping)

    def test_horizontal_divisions(self):
        self.assertEqual(10, self.scope._horizontal_divisions)

    def test_vertical_divisions(self):
        self.assertEqual(8, self.scope._vertical_divisions)

    def test_display_screenshot_image_format_mapping(self):
        image_formats = ('bmp', 'bmp24', 'bmp8', 'png', 'png24')
        for image_format in image_formats:
            self.assertIn(image_format,
                          self.scope._display_screenshot_image_format_mapping)

    def test_output_name(self):
        self.assertEqual(self.scope._output_name, ['wgen'])

    def test_output_operation_mode(self):
        self.assertEqual(self.scope._output_operation_mode, ['continuous'])

    def test_output_enabled(self):
        self.assertEqual(self.scope._output_enabled, [False])

    def test_output_impedance(self):
        self.assertEqual(self.scope._output_impedance, [50])

    def test_output_mode(self):
        self.assertEqual(self.scope._output_mode, ['function'])

    def test_output_reference_clock_source(self):
        self.assertEqual(self.scope._output_reference_clock_source, [''])

    def test_get_output_operation_mode(self):
        self.assertEqual(self.scope._get_output_operation_mode(0),
                         'continuous')

    def test_set_output_operation_mode_valid(self):
        # Make sure an exception isn't raised for a valid operation mode
        self.scope._set_output_operation_mode(0, 'burst')

    def test_set_output_operation_mode_to_invalid_mode(self):
        self.assertRaises(
            TypeError,
            self.scope._set_output_operation_mode,
            (0, 'trash_mode'))

    def test_get_output_enabled_while_simulating_driver_operation(self):
        # TODO(mdr) Need to test _get_output_enabled() using mocks/spies when
        # self.scope._driver_operation_simulate = False
        self.scope._driver_operation_simulate = True
        self.assertEqual(self.scope._get_output_enabled(0), False)

    def test_set_output_enabled_while_simulating_driver_operation(self):
        # TODO(mdr) Need to test _set_output_enabled() using mocks/spies when
        # self.scope._driver_operation_simulate = False
        self.scope._driver_operation_simulate = True
        # Make sure an exception isn't raised
        self.scope._set_output_enabled(0, True)

    def test_get_output_impedance_while_simulating_driver_operation(self):
        # TODO(mdr) Need to test _get_output_impedance() using mocks/spies when
        # self.scope._driver_operation_simulate = False
        self.scope._driver_operation_simulate = True
        self.assertEqual(self.scope._get_output_impedance(0), 50)

    def test_set_output_impedance_while_simulating_driver_operation(self):
        # TODO(mdr) Need to test _set_output_impedance() using mocks/spies when
        # self.scope._driver_operation_simulate = False
        self.scope._driver_operation_simulate = True
        # Make sure an exception isn't raised
        self.scope._set_output_impedance(0, 1000000)

    def test_output_impedance_must_be_set_to_valid_impedance(self):
        self.scope._driver_operation_simulate = True
        invalid_impedances = (25, 75, 100, 1000001)
        for invalid_impedance in invalid_impedances:
            self.assertRaises(
                Exception,
                self.scope._set_output_impedance,
                0,
                invalid_impedance)
