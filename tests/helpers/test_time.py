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
        - parse_date_string()
        - to_string()
        - local_to_utc()

    methods:
    --------
    setUp
        Setup before testing
    tearDown
        Cleaning after testing
    test_date_by_weekday
        Calculate date based on weekday
    test_date_by_interval
        Calculate date based on interval
    test_clalculate_next_delivery
        Calculate next delivery

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

        # create a today (-> Wendsday, aka 2)
        date = datetime.datetime.strptime("16.03.2022", "%d.%m.%Y")


        #region 'cycle_type = None'
        result = time.calculate_next_delivery(
            date = date,
            cycle_type = None,
            interval = 2,
            language = "EN"
        )

        # assert
        self.assertEqual(result, None)

        #endregion

        #region 'cycle_type = day, interval = None'
        with self.assertRaises(AssertionError) as e:
            result = time.calculate_next_delivery(
                date = date,
                cycle_type = "day",
                interval = None,
                language = "EN"
            )
        
        # assert
        self.assertEqual(str(e.exception), "The 'interval' is not allowed to be None if the 'cycle_type' indicates a 'day' or 'interval'.")

        #endregion

        #region 'cycle_type = day, interval > 6'
        with self.assertRaises(AssertionError) as e:
            result = time.calculate_next_delivery(
                date = date,
                cycle_type = "day",
                interval = 7,
                language = "EN"
            )
        
        # assert
        self.assertEqual(str(e.exception), "'interval for day' needs to be one of the following '{ Monday, Tuesday, Wendsday, Thursday, Friday, Saturday, Sunday }'.")

        #endregion

        #region 'cycle_type = day, interval < 0'
        with self.assertRaises(AssertionError) as e:
            result = time.calculate_next_delivery(
                date = date,
                cycle_type = "day",
                interval = -1,
                language = "EN"
            )
        
        # assert
        self.assertEqual(str(e.exception), "'interval for day' needs to be one of the following '{ Monday, Tuesday, Wendsday, Thursday, Friday, Saturday, Sunday }'.")

        #endregion

        #region 'cycle_type = day, success'
        result = time.calculate_next_delivery(
                date = date,
                cycle_type = "day",
                interval = 3,
                language = "EN"
            )
        
        # assert
        self.assertEqual(result.strftime("%d.%m.%Y"), "24.03.2022")

        #endregion

        #region 'cycle_type = interval, interval = None'
        with self.assertRaises(AssertionError) as e:
            result = time.calculate_next_delivery(
                date = date,
                cycle_type = "interval",
                interval = None,
                language = "EN"
            )
        
        # assert
        self.assertEqual(str(e.exception), "The 'interval' is not allowed to be None if the 'cycle_type' indicates a 'day' or 'interval'.")

        #endregion

        #region 'cycle_type = interval, success'
        result = time.calculate_next_delivery(
                date = date,
                cycle_type = "interval",
                interval = 4,
                language = "EN"
            )
        
        # assert
        self.assertEqual(result.strftime("%d.%m.%Y"), "20.03.2022")

        #endregion

        #region 'cycle_type = unknown'
        with self.assertRaises(AssertionError) as e:
            result = time.calculate_next_delivery(
                date = date,
                cycle_type = "notKnown",
                interval = None,
                language = "EN"
            )
        
        # assert
        self.assertEqual(str(e.exception).split("{")[0], "'cycle_type' needs to be one of the following '")


        #endregion

    def test_utc_to_local(self):
        """Tests utc to local """

        # test without timedelta
        today = datetime.datetime.strptime("2022.03.22 13:00", "%Y.%m.%d %H:%M")
        result = time.utc_to_local(today, "Europe/Berlin")

        self.assertEqual(result.strftime("%Y.%m.%d %H:%M"), "2022.03.22 14:00")

        # test with timedelta
        today = datetime.datetime.strptime("2022.03.22 13:00", "%Y.%m.%d %H:%M") + datetime.timedelta(days=1)
        result = time.utc_to_local(today, "Europe/Berlin")

        self.assertEqual(result.strftime("%Y.%m.%d %H:%M"), "2022.03.23 14:00")

    #endregion

