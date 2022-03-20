"""
Tests the tools.py from auth.

"""

# imports
import sys
import unittest
from unittest.mock import patch

import miniMoi.logic.helpers.tools as tools

# class
class TestTools(unittest.TestCase):
    """Tests the tools.py functions

    CAUTION:
    one function and one class are not tested
        - _to_dict()
        - jEncoder

    methods:
    --------
    setUp
        Setsup the testcase
    tearDown
        Cleaning after tests
    test_convert_exception
        Tests the exception conversion

    """

    def setUp(self):
        """Setup for each test"""

        return super().setUp()

    def tearDown(self):
        """Cleans certain attributes after tests"""

        return super().tearDown()
    
    #region 'tests'
    def test_convert_exception(self):
        """Tests the exception converts """

        try:
            raise KeyError("I am a key")
        except Exception as e:
            code, msg = tools._convert_exception(e)

        self.assertEqual(code, "KeyError")
        self.assertEqual(msg, "'I am a key'")


    #endregion