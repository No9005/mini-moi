"""
Tests the function for the products processing

"""

# imports
import unittest
from unittest.mock import patch

import datetime

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from miniMoi import base
from miniMoi.models.Models import Abo, Customers, Products, Category, Subcategory

from miniMoi.logic.functions import products

from tests import testEngine

# create session macker to mock it
testSessionFactory = sessionmaker(bind=testEngine)
testSession = scoped_session(testSessionFactory)

# class
@patch('miniMoi.logic.functions.products.Session', testSession)
class TestProducts(unittest.TestCase):
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
                product = 2,
                subcategory = 1,
                quantity = 5
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

        #region 'filter_type = None'
        result = products.get(
            filter_type = None,
            what = None,
            language = "EN"
        )

        self.assertEqual(result, {
            'success': True,
            'error': '',
            'data': {
                'data': [
                    {
                        'id':1,
                        'name':"Brot",
                        'category':1,
                        'purchase_price':3.50,
                        'selling_price':10.00,
                        'margin':.01,
                        'store':"MeinLaden",
                        'phone':"+50 phone"
                    },
                    {
                        'id':2,
                        'name':"Baguette",
                        'category':2,
                        'purchase_price':1.50,
                        'selling_price':2.00,
                        'margin':.01,
                        'store':"MeinLaden",
                        'phone':"+50 phone"
                    }
                    ],
                'order': [
                    'id', 'name', 'category', 'purchase_price', 'selling_price', 
                    'margin', 'store', 'phone'],
                'mapping': [
                    'id', 'Name', 'Category', 'Purchase price', 'Selling price', 
                    'Margin', 'Store', 'Phone'
                    ],
                'dropdown': {'category': {1: 'Brot', 2: 'Weißwaren'}},
                'table_name':"Products"
                }
        })

        #endregion

        #region 'filter_type = product, success but emtpy'
        result = products.get(
            filter_type = "product",
            what = "NotThere",
            language = "EN"
        )

        self.assertEqual(result['data'], {
            'data':[],
            'order': [
                    'id', 'name', 'category', 'purchase_price', 'selling_price', 
                    'margin', 'store', 'phone'
                    ],
            'mapping': [
                'id', 'Name', 'Category', 'Purchase price', 'Selling price', 
                'Margin', 'Store', 'Phone'
                ],
            'dropdown': {'category': {1: 'Brot', 2: 'Weißwaren'}},
            'table_name':"Products"
        })

        #endregion

        #region 'filter_type = product, success'
        #run 
        result = products.get(
            filter_type = "product",
            what = "Baguette",
            language = "EN"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'data': [
                    {
                        'id':2,
                        'name':"Baguette",
                        'category':2,
                        'purchase_price':1.50,
                        'selling_price':2.00,
                        'margin':.01,
                        'store':"MeinLaden",
                        'phone':"+50 phone"
                        }
                    ],
            'order': [
                'id', 'name', 'category', 'purchase_price', 'selling_price', 
                'margin', 'store', 'phone'],
            'mapping': [
                'id', 'Name', 'Category', 'Purchase price', 'Selling price', 
                'Margin', 'Store', 'Phone'
                ],
            'dropdown': {'category': {1: 'Brot', 2: 'Weißwaren'}},
            'table_name':"Products"
            }})

        #endregion

        #region 'filter_type = category, success'
        # add new product
        with Session(testEngine) as session:

            session.add(Products(
                name = "Brot2",
                category = 1,
                purchase_price = 100.50,
                selling_price = 10.00,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            ))

            session.commit()
        
        # run
        result = products.get(
            filter_type = "category",
            what = 1,
            language = "EN"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'data': [
                    {
                        'id':1,
                        'name':"Brot",
                        'category':1,
                        'purchase_price':3.50,
                        'selling_price':10.00,
                        'margin':.01,
                        'store':"MeinLaden",
                        'phone':"+50 phone"
                    },
                    {
                        'id':3,
                        'name':"Brot2",
                        'category':1,
                        'purchase_price':100.50,
                        'selling_price':10.00,
                        'margin':.01,
                        'store':"MeinLaden",
                        'phone':"+50 phone"
                        }
                    ],
            'order': [
                'id', 'name', 'category', 'purchase_price', 'selling_price', 
                'margin', 'store', 'phone'],
            'mapping': [
                'id', 'Name', 'Category', 'Purchase price', 'Selling price', 
                'Margin', 'Store', 'Phone'
                ],
            'dropdown': {'category': {1: 'Brot', 2: 'Weißwaren'}},
            'table_name':"Products"
            }})

        #endregion

        #region 'limit = 0'
        result = products.get(
            filter_type = "category",
            what = 1,
            amount = 0,
            language = "EN",
        )
        

        self.assertEqual(result['data'], {
            'data':[],
            'order': [
                    'id', 'name', 'category', 'purchase_price', 'selling_price', 
                    'margin', 'store', 'phone'
                    ],
            'mapping': [
                'id', 'Name', 'Category', 'Purchase price', 'Selling price', 
                'Margin', 'Store', 'Phone'
                ],
            'dropdown': {'category': {1: 'Brot', 2: 'Weißwaren'}},
            'table_name':"Products"
        })

        #endregion

    def test_update(self):
        """Tests the updater """

        #region 'id not found'
        result = products.update(
            product_id = 5,
            data = {
                'name':"Apfel",
                'category':2,
                'purchase_price':20.0,
                'selling_price':25.0,
                'store':"AndererLaden",
                'phone':"+phone"
            },
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "The Product was not found.")

        #endregion

        #region 'no changes passed'
        result = products.update(
            product_id = 1,
            data = {
            },
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "You did not enter/change anything.")

        # check db
        with Session(testEngine) as session:

            result = session.query(Products).filter_by(id = 1).first()
            self.assertEqual(result.name, "Brot")

        #endregion

        #region 'success'
        result = products.update(
            product_id = 1,
            data = {
                'name':"Apfel",
                'category':2,
                'purchase_price':"20.0",
                'selling_price':"25,0",
                'store':"AndererLaden",
                'phone':"+phone"
            },
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # check db
        with Session(testEngine) as session:
            # query 
            result = session.query(Products).filter_by(id = 1).first()
            self.assertEqual(result.name, "Apfel")
            self.assertEqual(result.category, 2)
            self.assertEqual(result.margin, .2)


        #endregion

        #region 'category not found'
        result = products.update(
            product_id = 1,
            data = {
                'name':"Raupe",
                'category':10,
                'purchase_price':20.0,
                'selling_price':25.0,
                'store':"AndererLaden",
                'phone':"+phone"
            },
            language ="EN"
        )

        # assert
        self.assertEqual(result['error'], "Selected category for product not available. (prior 'Apfel', now 'Raupe', category '10').")

        # check db, no changes?
        with Session(testEngine) as session:
            # query 
            result = session.query(Products).filter_by(id = 1).first()
            self.assertEqual(result.name, "Apfel")
            self.assertEqual(result.category, 2)

        #endregion
    
    def test_add(self):
        """Adds a element to the db """

        #region 'empty'
        result = products.add(
            products = [],
            language="EN"
        )

        # assert
        self.assertEqual(result['error'], "You did not enter/change anything.")

        #endregion

        #region 'success'
        """
        We add multiple abos at once!
        
        """

        result = products.add(
            products = [{
                    'name':"Apfel",
                    'category':2,
                    'purchase_price':20.0,
                    'selling_price':"25.0",
                    'store':"AndererLaden",
                    'phone':"+phone"
                },
                {
                    'name':"Wurm",
                    'category':1,
                    'purchase_price':"1,50",
                    'selling_price':25.0,
                    'store':"AndererLaden",
                    'phone':"+phone"
                }
            ],
            language="EN"
        )

        # assert
        self.assertTrue(result['success'])

        # check with db
        with Session(testEngine) as session:

            # query
            result = session.query(Products)

            # 4 entries?
            self.assertEqual(result.count(), 4)

            # check entries
            self.assertEqual(result.filter_by(id = 3).first().name, "Apfel")
            self.assertEqual(result.filter_by(id = 4).first().margin, .94)
            self.assertEqual(result.filter_by(id=4).first().purchase_price, 1.50)
            self.assertEqual(result.filter_by(id=3).first().selling_price, 25.0)


        
        #endregion

    def test_delete(self):
        """Tests the products deletion """

        #region 'product not found'
        result = products.delete(
            product_id = 5,
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "The Product was not found.")

        #endregion

        #region 'success'
        result = products.delete(
            product_id = 1,
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # db check
        with Session(testEngine) as session:

            result = session.query(Products)

            self.assertEqual(result.count(), 1)
            self.assertEqual(result.first().id, 2)

        #endregion

    #endregion
