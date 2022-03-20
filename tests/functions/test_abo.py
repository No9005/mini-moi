"""
Tests the function for the abo processing

"""

# imports
import unittest
from unittest.mock import patch

import datetime

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from miniMoi import base
from miniMoi.models.Models import Abo, Customers, Products

from miniMoi.logic.functions import abo

from tests import testEngine

# create session macker to mock it
testSessionFactory = sessionmaker(bind=testEngine)
testSession = scoped_session(testSessionFactory)

# class
@patch('miniMoi.logic.functions.abo.Session', testSession)
class TestAbo(unittest.TestCase):
    """Tests the abo functions 
    
    methods:
    --------
    setUp
        Tests setup
    tearDown
        Clean after test
    test_get
        Tests the getter
    test_update
        Tests the updater
    test_add
        Tests the add
    test_delete
        Tests the delete process

    """

    def setUp(self):
        """Prepares the test """

        # copy engine to self.
        self.testEngine = testEngine

        # create db
        base.metadata.create_all(self.testEngine)

        # add a test user
        with Session(self.testEngine) as session:

            # create user
            newUser = Customers(
                name = "Fritz",
                surname = "Meier",
                street = "Elmstreet",
                nr = 5,
                postal = "0000",
                town = "Entenhausen",
                phone = "+83 phone",
                mobile = "+83 mobile",
                birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                approach = 3,
                notes = ""
            )

            # create product
            newProduct = Products(
                name = "Brot",
                category = 1,
                purchase_price = 3.50,
                selling_price = 10.00,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            )

            newProduct2 = Products(
                name = "Baguette",
                category = 2,
                purchase_price = 1.50,
                selling_price = 2.00,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            )

            # create one abo
            newAbo = Abo(
                customer_id = 1,
                update_date = datetime.datetime.strptime("2022.03.15 12:00:00", "%Y.%m.%d %H:%M:%S"),
                cycle_type = "day",
                interval = 5,
                next_delivery = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                product = 2
            )

            # add to db
            session.add_all([newUser, newProduct, newProduct2, newAbo])

            # commit
            session.commit()

    def tearDown(self):
        """Cleans the mess after a test"""

        base.metadata.drop_all(self.testEngine)
        self.testEngine = None
        self.account = None

    #region 'tests'
    def test_get(self):
        """Tests the data getter """

        #region 'filter_type = None'
        result = abo.get(
            filter_type = None,
            what = None,
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result, {
            'success': True,
            'error': '',
            'data': {
                'result': [
                    {
                        'id': 1, 
                        'customer_id': 1, 
                        'update_date': '2022.03.15 13:00', 
                        'cycle_type': 'day', 
                        'interval': 5, 
                        'next_delivery': '2022.03.16', 
                        'product_id': 2, 
                        'product_name': 'Baguette'
                        }
                    ]
                }
        })

        #endregion

        #region 'filter_type = abo, success but emtpy'
        result = abo.get(
            filter_type = "abo",
            what = 5,
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{'result':[]}})

        #endregion

        #region 'filter_type = abo, success'
        # add abo
        with Session(testEngine) as session:
            newAbo = Abo(
                customer_id = 1,
                update_date = datetime.datetime.strptime("2022.03.15 12:00:00", "%Y.%m.%d %H:%M:%S"),
                cycle_type = "interval",
                interval = 6,
                next_delivery = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                product = 1
            )
            
            session.add(newAbo)

            session.commit()

        #run 
        result = abo.get(
            filter_type = "abo",
            what = 2,
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'result': [
                    {
                        'id': 2, 
                        'customer_id': 1, 
                        'update_date': '2022.03.15 13:00', 
                        'cycle_type': 'interval', 
                        'interval': 6, 
                        'next_delivery': '2022.03.16', 
                        'product_id': 1, 
                        'product_name': 'Brot'
                        }
                    ]
            }})

        #endregion

        #region 'filter_type = customer, success'
        result = abo.get(
            filter_type = "customer",
            what = 1,
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'result': [
                    {
                        'id': 1, 
                        'customer_id': 1, 
                        'update_date': '2022.03.15 13:00', 
                        'cycle_type': 'day', 
                        'interval': 5, 
                        'next_delivery': '2022.03.16', 
                        'product_id': 2, 
                        'product_name': 'Baguette'
                    },
                    {
                        'id': 2, 
                        'customer_id': 1, 
                        'update_date': '2022.03.15 13:00', 
                        'cycle_type': 'interval', 
                        'interval': 6, 
                        'next_delivery': '2022.03.16', 
                        'product_id': 1, 
                        'product_name': 'Brot'
                        }
                    ]
            }})

        #endregion

        #region 'limit = 0'
        result = abo.get(
            filter_type = "customer",
            what = 1,
            amount = 0,
            language = "EN",
            tz = "Europe/Berlin"
        )
        
        self.assertEqual(result, {'success':True, 'error':"", 'data':{'result':[]}})

        #endregion

    def test_update(self):
        """Tests the updater """

        #region 'id not found'
        result = abo.update(
            abo_id = 5,
            data = {
                'cycle_type':"interval",
                'interval':3,
                'product':1,
                'custom_next_delivery':None
            }
        )

        # assert
        self.assertEqual(result['error'], "The abo was not found.")

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Abo).filter_by(id = 1).first()
            self.assertEqual(result.cycle_type, "day")

        #endregion

        #region 'no changes passed'
        result = abo.update(
            abo_id = 1,
            data = {
            }
        )

        # assert
        self.assertEqual(result['error'], "You did not enter/change anything.")

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Abo).filter_by(id = 1).first()
            self.assertEqual(result.cycle_type, "day")

        #endregion

        #region 'no_custom_delivery, success'
        result = abo.update(
            abo_id = 1,
            data = {
                'cycle_type':"interval",
                'interval':3,
                'product':1,
                'next_delivery':None
            }
        )

        # assert
        self.assertTrue(result['success'])

        # create datetime to check against
        current = (datetime.datetime.utcnow() + datetime.timedelta(days=3)).strftime("%Y.%m.%d")

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Abo).filter_by(id = 1).first()
            self.assertEqual(result.cycle_type, "interval")
            self.assertEqual(result.next_delivery.strftime("%Y.%m.%d"), current)

        #endregion

        #region 'custom delivery, success'
        result = abo.update(
            abo_id = 1,
            data = {
                'cycle_type':"day",
                'interval':2,
                'product':1,
                'next_delivery':"2021-12-01"
            }
        )

        # assert
        self.assertTrue(result['success'])

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Abo).filter_by(id = 1).first()
            self.assertEqual(result.cycle_type, "day")
            self.assertEqual(result.next_delivery.strftime("%Y.%m.%d"), "2021.12.01")

        #endregion

        #region 'product id not found'
        result = abo.update(
            abo_id = 1,
            data = {
                'cycle_type':"interval",
                'interval':3,
                'product':15,
                'custom_next_delivery':None
            }
        )

        # assert
        self.assertEqual(result['error'], "Selected product not available.")

        #endregion
    
    def test_add(self):
        """Adds a element to the db """

        #region 'customer not found'
        result = abo.add(
            customer_id = 6,
            abos = [{
                'cycle_type':"day",
                'interval':6,
                'product':6
            }]
        )

        # assert
        self.assertEqual(result['error'], "The customer was not found.")

        #endregion

        #region 'product not available'
        result = abo.add(
            customer_id = 1,
            abos = [{
                'cycle_type':"day",
                'interval':6,
                'product':6
            }]
        )

        # assert
        self.assertEqual(result['error'], "Selected product not available.")

        #endregion

        #region 'success'
        """
        We add multiple abos at once!
        
        """

        result = abo.add(
            customer_id = 1,
            abos = [{
                'cycle_type':"day",
                'interval':6,
                'product':1
                },
                {'cycle_type':"interval",
                'interval':8,
                'product':2}
            ]
        )

        # assert
        self.assertTrue(result['success'])

        # check with db
        with Session(testEngine) as session:

            # query
            result = session.query(Abo)

            # 3 entries?
            self.assertEqual(result.count(), 3)

            # check entry 2 & 3
            self.assertEqual(result.filter_by(id = 2).first().cycle_type, "day")
            self.assertEqual(result.filter_by(id = 3).first().cycle_type, "interval")

        
        #endregion

    def test_delete(self):
        """Tests the abo deletion """

        # add abo
        with Session(testEngine) as session:

            session.add(Abo(
                customer_id = 1,
                update_date = datetime.datetime.strptime("2022.03.15 12:00:00", "%Y.%m.%d %H:%M:%S"),
                cycle_type = "interval",
                interval = 100,
                next_delivery = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                product = 1
            ))        
    
            session.commit()

            # check
            self.assertEqual(session.query(Abo).count(), 2)

        #region 'abo not found'
        result = abo.delete(
            abo_id = 5,
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "The abo was not found.")

        #endregion

        #region 'success'
        result = abo.delete(
            abo_id = 1,
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # db check
        with Session(testEngine) as session:

            result = session.query(Abo)

            self.assertEqual(result.count(), 1)
            self.assertEqual(result.first().id, 2)

        #endregion

    #endregion
