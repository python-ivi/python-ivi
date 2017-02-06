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

import unittest

import ivi

class TestIndex(unittest.TestCase):

    def setUp(self):
        self.index_list = ['item1', 'item2', 'item3']
        self.index_dict = ivi.get_index_dict(self.index_list)

    def test_get_index_with_list(self):
        for i in range(len(self.index_list)):
            self.assertEqual(ivi.get_index(self.index_list, i), i)
            self.assertEqual(ivi.get_index(self.index_list, self.index_list[i]), i)
        self.assertRaises(ivi.SelectorRangeException, ivi.get_index, self.index_list, -1);
        self.assertRaises(ivi.SelectorRangeException, ivi.get_index, self.index_list, 100);
        self.assertRaises(ivi.SelectorNameException, ivi.get_index, self.index_list, 'bad_item');

    def test_get_index_dict(self):
        for i in range(len(self.index_list)):
            self.assertTrue(i in self.index_dict)
            self.assertTrue(self.index_list[i] in self.index_dict)
            self.assertEqual(self.index_dict[i], i)
            self.assertEqual(self.index_dict[self.index_list[i]], i)

    def test_get_index_with_dict(self):
        for i in range(len(self.index_list)):
            self.assertEqual(ivi.get_index(self.index_dict, i), i)
            self.assertEqual(ivi.get_index(self.index_dict, self.index_list[i]), i)
        self.assertRaises(ivi.SelectorRangeException, ivi.get_index, self.index_dict, -1);
        self.assertRaises(ivi.SelectorRangeException, ivi.get_index, self.index_dict, 100);
        self.assertRaises(ivi.SelectorNameException, ivi.get_index, self.index_dict, 'bad_item');

if __name__ == '__main__':
    unittest.main()
