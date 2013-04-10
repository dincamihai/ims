#!/usr/bin/env python

import unittest
from listener import listener

class IMSTestCase(unittest.TestCase):

    def test_counter_reset(self):
        counter = {1: 1, 2: 0}
        listener.reseter(1)
        import pytest; pytest.set_trace()

if __name__=="__main__":
    unittest.main()
