"""
Tests the function for the customer processing

"""

# imports
import unittest
from unittest.mock import patch

import datetime

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from miniMoi import base
from miniMoi.models.Models import Abo, Customers, Products, Subcategory

from miniMoi.logic.functions import customer

from tests import testEngine

# create session macker to mock it
testSessionFactory = sessionmaker(bind=testEngine)
testSession = scoped_session(testSessionFactory)

# class
@patch('miniMoi.logic.functions.customer.Session', testSession)
class TestCustomer(unittest.TestCase):
    """Tests the customer functions 
    
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
                date = datetime.datetime.strptime("2022.03.15 12:00:00", "%Y.%m.%d %H:%M:%S"),
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
                quantity = 5,
                subcategory = 1
            )

            # create subcategories
            newSub = Subcategory(
                name="Sub1"
            )

            newSub2 = Subcategory(
                name="Sub2"
            )

            # add to db
            session.add_all([newUser, newProduct, newProduct2, newAbo, newSub, newSub2])

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
        result = customer.get(
            filter_type = None,
            what = None,
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result, {
            'success': True,
            'error': '',
            'data': {
                'data': [
                    {
                        'id': 1, 
                        'date':'2022.03.15 13:00',
                        'name':"Fritz",
                        'surname':"Meier",
                        'street':"Elmstreet",
                        'nr':5,
                        'postal':"0000",
                        'town':"Entenhausen",
                        'phone':"+83 phone",
                        'mobile':"+83 mobile",
                        'birthdate':"2022.03.16",
                        'approach':3,
                        'notes':""
                    }
                    ],
                'order': [
                    'id', 'date', 'name', 'surname', 'street', 'nr', 
                    'postal', 'town', 'phone', 'mobile', 'birthdate', 
                    'approach', 'notes'
                    ],
                'mapping': [
                    'id', 'Date', 'Name', 'Surname', 'Street', 'Nr', 
                    'Postal', 'City', 'Phone', 'Mobile', 'Birthdate', 
                    'Approach', 'Notes'
                ]
                }
        })

        #endregion

        #region 'filter_type = customer, success but emtpy'
        result = customer.get(
            filter_type = "customer",
            what = 5,
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result['data'], {
            'data':[],
            'order':[
                'id', 'date', 'name', 'surname', 'street', 'nr', 'postal',
                'town', 'phone', 'mobile', 'birthdate', 'approach', 'notes'
                ],
            'mapping':[
                'id', 'Date', 'Name', 'Surname', 'Street',
                'Nr', 'Postal', 'City',
                'Phone', 'Mobile', 'Birthdate', 'Approach',
                'Notes'
            ]
        })

        #endregion

        #region 'filter_type = customer, success'
        #run 
        result = customer.get(
            filter_type = "customer",
            what = "Meier",
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'data': [
                    {
                        'id': 1, 
                        'date':'2022.03.15 13:00',
                        'name':"Fritz",
                        'surname':"Meier",
                        'street':"Elmstreet",
                        'nr':5,
                        'postal':"0000",
                        'town':"Entenhausen",
                        'phone':"+83 phone",
                        'mobile':"+83 mobile",
                        'birthdate':"2022.03.16",
                        'approach':3,
                        'notes':""
                        }
                    ],
            'order': [
                    'id', 'date', 'name', 'surname', 'street', 'nr', 
                    'postal', 'town', 'phone', 'mobile', 'birthdate', 
                    'approach', 'notes'
                    ],
            'mapping': [
                'id', 'Date', 'Name', 'Surname', 'Street', 'Nr', 
                'Postal', 'City', 'Phone', 'Mobile', 'Birthdate', 
                'Approach', 'Notes'
            ]
            }})

        #endregion

        #region 'filter_type = customer, success'
        result = customer.get(
            filter_type = "town",
            what = "Entenhausen",
            language = "EN",
            tz = "Europe/Berlin"
        )

        self.assertEqual(result, {'success':True, 'error':"", 'data':{
            'data': [
                    {
                        'id': 1, 
                        'date':'2022.03.15 13:00',
                        'name':"Fritz",
                        'surname':"Meier",
                        'street':"Elmstreet",
                        'nr':5,
                        'postal':"0000",
                        'town':"Entenhausen",
                        'phone':"+83 phone",
                        'mobile':"+83 mobile",
                        'birthdate':"2022.03.16",
                        'approach':3,
                        'notes':""
                        }
                    ],
            'order': [
                    'id', 'date', 'name', 'surname', 'street', 'nr', 
                    'postal', 'town', 'phone', 'mobile', 'birthdate', 
                    'approach', 'notes'
                    ],
            'mapping': [
                'id', 'Date', 'Name', 'Surname', 'Street', 'Nr', 
                'Postal', 'City', 'Phone', 'Mobile', 'Birthdate', 
                'Approach', 'Notes'
            ]
            }})

        #endregion

        #region 'limit = 0'
        result = customer.get(
            filter_type = "customer",
            what = 1,
            amount = 0,
            language = "EN",
            tz = "Europe/Berlin"
        )
        
        self.assertEqual(result['data'], {
            'data':[],
            'order':[
                'id', 'date', 'name', 'surname', 'street', 'nr', 'postal',
                'town', 'phone', 'mobile', 'birthdate', 'approach', 'notes'
                ],
            'mapping':[
                'id', 'Date', 'Name', 'Surname', 'Street',
                'Nr', 'Postal', 'City',
                'Phone', 'Mobile', 'Birthdate', 'Approach',
                'Notes'
            ]
        })

        #endregion

    def test_update(self):
        """Tests the updater """

        #region 'id not found'
        result = customer.update(
            customer_id = 5,
            data = {
                'name':"Peter",
                'surname':"Fischkopf",
                'street':"Weiher",
                'nr':3,
                'postal':"0101",
                'town':"Birdy",
                'phone':"",
                'mobile':"",
                'birthdate':"1832-12-10",
                'notes':"Some notes"
            },
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "The customer was not found.")

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Customers).filter_by(id = 1).first()
            self.assertEqual(result.name, "Fritz")

        #endregion

        #region 'no changes passed'
        result = customer.update(
            customer_id = 1,
            data = {
            },
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "You did not enter/change anything.")

        #endregion

        #region 'success'
        result = customer.update(
            customer_id = 1,
            data = {
                'name':"Peter",
                'surname':"Fischkopf",
                'street':"Weiher",
                'nr':3,
                'postal':"0101",
                'town':"Birdy",
                'phone':"",
                'mobile':"",
                'birthdate':"1832-12-10",
                'approach':"15",
                'notes':"Some notes"
            },
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # check db
        with Session(testEngine) as session:
            # query abo
            result = session.query(Customers).filter_by(id = 1).first()
            self.assertEqual(result.name, "Peter")
            self.assertEqual(result.nr, 3)

        #endregion

        #region 'birthdate wrong format'
        result = customer.update(
            customer_id = 1,
            data = {
                'name':"Hans",
                'surname':"Fischkopf",
                'street':"Weiher",
                'nr':3,
                'postal':"0101",
                'town':"Birdy",
                'phone':"",
                'mobile':"",
                'birthdate':"1832-12:10",
                'approach':"10",
                'notes':"Some notes"
            },
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "'Birthdate' needs to be in the format 'Year.Month.Day'.")

        # check db
        with Session(testEngine) as session:

            result = session.query(Customers).filter_by(id = 1).first()
            self.assertEqual(result.name, "Peter")

        #endregion
    
    def test_add(self):
        """Adds a element to the db """

        #region 'nothing to add'
        result = customer.add(
            customers = [],
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "You did not enter/change anything.")

        #endregion

        #region 'success'
        """
        We add multiple customers at once!
        
        """

        result = customer.add(
            customers = [
                {
                    'name':"Heinzel",
                    'surname':"Männchen",
                    'street':"Weiher",
                    'nr':3,
                    'postal':"2020",
                    'town':"Schnapp",
                    'phone':"",
                    'mobile':"",
                    'birthdate':"1755-12-10",
                    'approach':"3",
                    'notes':"Gut'n Tach"
                },
                {
                    'name':"Zorg",
                    'surname':"King",
                    'street':"Castle",
                    'nr':1,
                    'postal':"9999",
                    'town':"Dreamland",
                    'phone':"",
                    'mobile':"",
                    'birthdate':"2022-12-10",
                    'approach':4,
                    'notes':""
                }
            ],
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # check with db
        with Session(testEngine) as session:

            # query
            result = session.query(Customers)

            # 3 entries?
            self.assertEqual(result.count(), 3)

            # check entry 2 & 3
            self.assertEqual(result.filter_by(id = 2).first().name, "Heinzel")
            self.assertEqual(result.filter_by(id = 3).first().name, "Zorg")

        
        #endregion

        #region 'birthdate wrong format'
        result = customer.add(
            customers = [
                {
                    'name':"Bilbo",
                    'surname':"Männchen",
                    'street':"Weiher",
                    'nr':3,
                    'postal':"2020",
                    'town':"Schnapp",
                    'phone':"",
                    'mobile':"",
                    'birthdate':"1755-12:10",
                    'approach':3,
                    'notes':""
                },
            ],
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "'Birthdate' needs to be in the format 'Year.Month.Day'.")

        #endregion

        #region 'birthdate empty'
        """--> should work"""
        result = customer.add(
            customers = [
                {
                    'name':"Bilbo",
                    'surname':"Männchen",
                    'street':"Weiher",
                    'nr':3,
                    'postal':"2020",
                    'town':"Schnapp",
                    'phone':"",
                    'mobile':"",
                    'birthdate':"",
                    'approach':3,
                    'notes':""
                },
            ],
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])
        
        #endregion

    def test_delete(self):
        """Tests the consumer deletion """

        # add abo
        with Session(testEngine) as session:

            session.add(Customers(
                name="Heinzel",
                surname="Männchen",
                street="Weiher",
                nr=3,
                postal="2020",
                town="Schnapp",
                phone="",
                mobile="",
                birthdate=datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                notes="Gut'n Tach"
            ))        
    
            session.commit()

            # check
            self.assertEqual(session.query(Customers).count(), 2)

        #region 'customer not found'
        result = customer.delete(
            customer_id = 5,
            language = "EN"
        )

        # assert
        self.assertEqual(result['error'], "The customer was not found.")

        #endregion

        #region 'success'
        result = customer.delete(
            customer_id = 1,
            language = "EN"
        )

        # assert
        self.assertTrue(result['success'])

        # db check
        with Session(testEngine) as session:

            result = session.query(Customers)

            self.assertEqual(result.count(), 1)
            self.assertEqual(result.first().id, 2)

        #endregion

    #endregion
