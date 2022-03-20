"""
Tests the function for the category processing

"""

# imports
import unittest
from unittest.mock import patch

import datetime

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from miniMoi import base
from miniMoi.models.Models import Abo, Customers, Products, Category

from miniMoi.logic.functions import category

from tests import testEngine

# create session macker to mock it
testSessionFactory = sessionmaker(bind=testEngine)
testSession = scoped_session(testSessionFactory)

# class
@patch('miniMoi.logic.functions.category.Session', testSession)
class TestCategory(unittest.TestCase):
    """Tests the category functions 
    
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

            # create category
            newCategory = Category(
                name = "Brot"
            )

            newCategory2 = Category(
                name = "Weißwaren"
            )

            # add to db
            session.add_all([newUser, newProduct, newProduct2, newAbo, newCategory, newCategory2])

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

        #region 'success'
        result = category.get(
            language = "EN",
        )

        self.assertEqual(result, {
            'success': True,
            'error': '',
            'data': {
                'result': [
                    {
                        'id': 1, 
                        'name':"Brot",
                    },
                    {
                        'id': 2, 
                        'name':"Weißwaren",
                    },
                    ]
                }
        })

        #endregion

        #region 'amount = 0'
        result = category.get(
            amount = 0,
            language = "EN"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{'result':[]}})

        #endregion

        #region 'amount = 1'
        result = category.get(
            amount = 1,
            language = "EN"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'result': [
                     {
                        'id': 1, 
                        'name':"Brot",
                    },
                    ]
            }})

        #endregion

    def test_update(self):
        """Tests the updater """

        #region 'id not found'
        result = category.update(
            category_id = 5,
            name = ""
        )

        # assert
        self.assertEqual(result['error'], "The category was not found.")

        #endregion

        #region 'wrong type'
        result = category.update(
            category_id = 1,
            name = None
        )

        # assert
        self.assertEqual(result['error'], "'name' needs to be a(n) str.")

        # check db
        with Session(testEngine) as session:
            
            # query category
            result = session.query(Category)
            self.assertEqual(result.count(), 2)

        #endregion

        #region 'success'
        result = category.update(
            category_id = 2,
            name = "Wurst"
        )

        # assert
        self.assertTrue(result['success'])

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Category)

            self.assertEqual(result.filter_by(id = 1).first().name, "Brot")
            self.assertEqual(result.filter_by(id=2).first().name, "Wurst")

        #endregion

    def test_add(self):
        """Adds a element to the db """

        #region 'no changes'
        result = category.add(
            categories = [],
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "You did not enter/change anything.")

        #endregion

        #region 'success'
        """
        We add multiple categories at once!
        
        """

        result = category.add(
            categories = ["Semmelbrösel", "Noobkanone"]
        )

        # assert
        self.assertTrue(result['success'])

        # check with db
        with Session(testEngine) as session:

            # query
            result = session.query(Category)

            # 3 entries?
            self.assertEqual(result.count(), 4)

            # check entries
            self.assertEqual(result.filter_by(id = 3).first().name, "Semmelbrösel")
            self.assertEqual(result.filter_by(id = 4).first().name, "Noobkanone")
            self.assertEqual(result.filter_by(id = 1).first().name, "Brot")

        #endregion

    def test_delete(self):
        """Tests the category deletion """

        # add abo
        with Session(testEngine) as session:

            session.add(Category(name = "Noobkanone"))        
    
            session.commit()

            # check
            self.assertEqual(session.query(Category).count(), 3)

        #region 'abo not found'
        result = category.delete(
            category_id = 10,
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "The category was not found.")

        #endregion

        #region 'success'
        result = category.delete(
            category_id = 1,
            language = "EN"
        )

        result = category.delete(
            category_id = 3,
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # db check
        with Session(testEngine) as session:

            result = session.query(Category)

            self.assertEqual(result.count(), 1)
            self.assertEqual(result.first().id, 2)
            self.assertEqual(result.first().name, "Weißwaren")


        #endregion

    #endregion
