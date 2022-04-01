"""
Tests the function for the category processing

"""

# imports
import unittest
from unittest.mock import patch

import datetime

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from miniMoi import base
from miniMoi.models.Models import Abo, Customers, Products, Category, Subcategory

from miniMoi.logic.functions import categories

from tests import testEngine

# create session macker to mock it
testSessionFactory = sessionmaker(bind=testEngine)
testSession = scoped_session(testSessionFactory)

# class
@patch('miniMoi.logic.functions.categories.Session', testSession)
class TestCategories(unittest.TestCase):
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
                product = 2,
                subcategory = 2,
                quantity = 10
            )

            # create category
            newCategory = Category(
                name = "Brot"
            )

            newCategory2 = Category(
                name = "Weißwaren"
            )

            # create subcategories
            newSub = Subcategory(
                name="Sub1"
            )

            newSub2 = Subcategory(
                name="Sub2"
            )

            # add to db
            session.add_all([newUser, newProduct, newProduct2, newAbo, newCategory, newCategory2, newSub, newSub2])

            # commit
            session.commit()

    def tearDown(self):
        """Cleans the mess after a test"""

        base.metadata.drop_all(self.testEngine)
        self.testEngine = None

    #region 'tests'
    def test_get(self):
        """Tests the data getter """

        #region 'success'
        result = categories.get(
            language = "EN",
        )

        self.assertEqual(result, {
            'success': True,
            'error': '',
            'data': {
                'data': [
                    {
                        'id': 1, 
                        'name':"Brot",
                    },
                    {
                        'id': 2, 
                        'name':"Weißwaren",
                    },
                    ],
                'category_type':"category",
                'order': ['id', 'name'], 
                'mapping': ['id', 'Name'],
                'table_name':"Category"
                }
        })

        #endregion

        #region 'amount = 0'
        result = categories.get(
            amount = 0,
            language = "EN"
        )

        self.assertEqual(result['data'], {
            'data':[],
            'order':["id", "name"],
            'mapping':["id", "Name"],
            'category_type':"category",
            'table_name':"Category"
        })

        #endregion

        #region 'amount = 1'
        result = categories.get(
            amount = 1,
            language = "EN"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'data': [
                     {
                        'id': 1, 
                        'name':"Brot",
                    },
                    ],
            'category_type':"category",
            'order': ['id', 'name'], 
            'mapping': ['id', 'Name'],
            'table_name':"Category"
            }
            })

        #endregion

        #region 'success, fetch 'subcategory''
        result = categories.get(
            category_type = "subcategory",
            language = "EN",
        )

        self.assertEqual(result, {
            'success': True,
            'error': '',
            'data': {
                'data': [
                    {
                        'id': 1, 
                        'name':"Sub1",
                    },
                    {
                        'id': 2, 
                        'name':"Sub2",
                    },
                    ],
                'category_type':"subcategory",
                'order': ['id', 'name'], 
                'mapping': ['id', 'Name'],
                'table_name':"Subcategory"
                }
        })

        #endregion

    def test_update(self):
        """Tests the updater """

        #region 'id not found, type = categories'
        result = categories.update(
            category_id = 5,
            name = "",
            language="EN"
        )

        # assert
        self.assertEqual(result['error'], "The Category was not found.")

        #endregion

        #region 'id not found, type = subcategories'
        result = categories.update(
            category_id = 5,
            category_type = "subcategory",
            name = "",
            language="EN"
        )

        # assert
        self.assertEqual(result['error'], "The Subcategory was not found.")

        #endregion

        #region 'wrong type'
        result = categories.update(
            category_id = 1,
            name = None,
            language="EN"
        )

        # assert
        self.assertEqual(result['error'], "'Name' needs to be a(n) text.")

        # check db
        with Session(testEngine) as session:
            
            # query category
            result = session.query(Category)
            self.assertEqual(result.count(), 2)

        #endregion

        #region 'success, type = category'
        result = categories.update(
            category_id = 2,
            name = "Wurst",
            language="EN"
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

        #region 'success, type = subcategory'
        result = categories.update(
            category_id = 1,
            category_type="subcategory",
            name = "DifferentName",
            language="EN"
        )

        # assert
        self.assertTrue(result['success'])

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Subcategory)

            self.assertEqual(result.filter_by(id = 1).first().name, "DifferentName")
            self.assertEqual(result.filter_by(id=2).first().name, "Sub2")

        #endregion

    def test_add(self):
        """Adds a element to the db """

        #region 'no changes'
        result = categories.add(
            categories = [],
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "You did not enter/change anything.")

        #endregion

        #region 'success, categories'
        """
        We add multiple categories at once!
        
        """

        result = categories.add(
            categories = [{"name":"Semmelbrösel"}, {"name":"Noobkanone"}],
            language = "EN"
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


            self.assertEqual(session.query(Subcategory).count(), 2)

        #endregion

        #region 'success, subcategories'
        """
        We add multiple subcategories at once!
        
        """

        result = categories.add(
            categories = [{"name":"Sub4"}, {"name":"Sub5"}],
            category_type="subcategory"
        )

        # assert
        self.assertTrue(result['success'])

        # check with db
        with Session(testEngine) as session:

            # query
            result = session.query(Subcategory)

            # 3 entries?
            self.assertEqual(result.count(), 4)

            # check entries
            self.assertEqual(result.filter_by(id = 3).first().name, "Sub4")
            self.assertEqual(result.filter_by(id = 4).first().name, "Sub5")
            self.assertEqual(result.filter_by(id = 1).first().name, "Sub1")


            self.assertEqual(session.query(Category).count(), 4)

        #endregion

    def test_delete(self):
        """Tests the category deletion """

        # add abo
        with Session(testEngine) as session:

            session.add(Category(name = "Noobkanone"))
            session.add(Category(id=0, name = "default")) 
    
            session.commit()

            # check
            self.assertEqual(session.query(Category).count(), 4)

        #region 'try to delete default --> fail'
        result = categories.delete(
            category_id = 0,
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "Default values can not be deleted.")

        #endregion

        #region 'abo not found'
        result = categories.delete(
            category_id = 10,
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "The Category was not found.")

        #endregion

        #region 'success, categories'
        result = categories.delete(
            category_id = 1,
            language = "EN"
        )

        result = categories.delete(
            category_id = 3,
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # db check
        with Session(testEngine) as session:

            result = session.query(Category)

            self.assertEqual(result.count(), 2)
            self.assertEqual(result.first().id, 0)
            self.assertEqual(result.first().name, "default")

            # id 2 should be still there
            self.assertEqual(result.get(2).id, 2)
            self.assertEqual(result.get(2).name, "Weißwaren")

            self.assertEqual(session.query(Subcategory).count(), 2)

        #endregion

        #region 'success, subcategories'
        result = categories.delete(
            category_id = 1,
            category_type  = "subcategory",
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # db check
        with Session(testEngine) as session:

            result = session.query(Subcategory)

            self.assertEqual(result.count(), 1)
            self.assertEqual(result.first().id, 2)

            self.assertEqual(session.query(Category).count(), 2)


        #endregion

    #endregion
