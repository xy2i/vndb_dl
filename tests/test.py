# -*- coding: utf-8 -*-

from .context import vndb_dl

import unittest

class TestSuite(unittest.TestCase):
    """ Tests for prosper behavior of vndb_dl. """

    def setUp(self):
        self.vn = vndb_dl.VN("4")

    def test_extraction(self):
        self.assertEqual(self.vn.metadata["Title"], "Clannad")
        self.assertEqual(self.vn.metadata["Developer"], "Key")
    
if __name__ == '__main__':
    unittest.main()