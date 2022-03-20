"""
Tests the functions in the module
    miniMoi.logic.helpers.time_module.py
    
"""

# imports
import unittest
from unittest.mock import patch

import datetime

import miniMoi.logic.helpers.time_module as time

# create test class
class TestTime(unittest.TestCase):
    """Tests the functions from the time_module
    
    CAUTION:
    Not all functions are tested.
    Some functions are basically just a 3rd party package
    call. These are
        - today()
        - utcnow()

    methods:
    --------
    setUp
    tearDown

    """

    #region 'init'
    def setUp(self):
        """Setup prior test """

        return

    def tearDown(self):
        """Cleaning after tests """

        return

    #endregion

    #region 'test'
    def test_date_by_weekday(self):
        """Tests the date_by_weekday function"""

        # create a today (-> Wendsday, aka 2)
        date = datetime.datetime.strptime("16.03.2022", "%d.%m.%Y")

        #region 'Weekday after today'
        result = time.date_by_weekday(
            today = date, 
            target_weekday = 5, 
            n_weeks = 1
        )

        # assert
        self.assertEqual(result.strftime("%d.%m.%Y"), "26.03.2022")

        #endregion

        #region 'Weekday prior today'
        result = time.date_by_weekday(
            today = date, 
            target_weekday = 1, 
            n_weeks = -1
        )

        # assert
        self.assertEqual(result.strftime("%d.%m.%Y"), "08.03.2022")

        #endregion

        #region 'Weekday is today'
        result = time.date_by_weekday(
            today = date, 
            target_weekday = 2, 
            n_weeks = 3
        )

        # assert
        self.assertEqual(result.strftime("%d.%m.%Y"), "06.04.2022")

        #endregion

    def test_date_by_interval(self):
        """Tests the date by interval function """

        # create a today (-> Wendsday, aka 2)
        date = datetime.datetime.strptime("16.03.2022", "%d.%m.%Y")

        #region 'positive interval'
        result = time.date_by_interval(
            today = date,
            interval = 3
        )

        # assert
        self.assertEqual(result.strftime("%d.%m.%Y"), "19.03.2022")

        #endregion

        #region 'negative interval'
        result = time.date_by_interval(
            today = date,
            interval = -15
        )

        # assert
        self.assertEqual(result.strftime("%d.%m.%Y"), "01.03.2022")
        
        #endregion

    def test_clalculate_next_delivery(self):
        """Tests the next delivery calculation """

        pass
    #endregion

