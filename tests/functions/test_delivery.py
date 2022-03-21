"""
Tests the delivery based functions

"""

# imports
import unittest
from unittest.mock import patch

import datetime

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from miniMoi import base
from miniMoi.models.Models import Abo, Customers, Products, Category, Subcategory, Orders

from miniMoi.logic.functions import delivery

from tests import testEngine

# create session macker to mock it
testSessionFactory = sessionmaker(bind=testEngine)
testSession = scoped_session(testSessionFactory)

# class
@patch('miniMoi.logic.functions.delivery.Session', testSession)
class TestDelivery(unittest.TestCase):
    """Tests the delivery functions 

    CAUTION:
    The functions
        - _prepare_granular()
        - _category_overview()
        - _product_overview()
    are tested with integration tests.
    
    methods:
    --------
    setUp
        Tests setup
    tearDown
        Clean after test


    """

    def setUp(self):
        """Prepare test """

        # copy engine to self.
        self.testEngine = testEngine

        # create db
        base.metadata.create_all(self.testEngine)

        # add data
        with Session(self.testEngine) as session:

            toAdd = []

            #region 'category'
            # 1
            toAdd.append(Category(
                name = "Brot"
            ))

            # 2
            toAdd.append(Category(
                name = "Semmel"
            ))

            # 3
            toAdd.append(Category(
                name = "Mischware"
            ))

            #endregion

            #region 'subcategory'
            # 1
            toAdd.append(Subcategory(
                name = "Ganz"
            ))

            # 2
            toAdd.append(Subcategory(
                name = "Geschnitten"
            ))

            #endregion

            #region 'products'
            # 1
            toAdd.append(Products(
                name = "Sonnenkernbrot",
                category = 1,
                purchase_price = 2.00,
                selling_price = 3.50,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            ))

            # 2
            toAdd.append(Products(
                name = "Fitnessbrot",
                category = 1,
                purchase_price = 2.50,
                selling_price = 5.00,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            ))

            # 3
            toAdd.append(Products(
                name = "Baguette",
                category = 3,
                purchase_price = 1.00,
                selling_price = 2.50,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            ))

            # 4
            toAdd.append(Products(
                name = "Kaisersemmel",
                category = 2,
                purchase_price = .20,
                selling_price = .50,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            ))

            # 5
            toAdd.append(Products(
                name = "Doppelweck",
                category = 2,
                purchase_price = .15,
                selling_price = .50,
                margin = .01,
                store = "MeinLaden",
                phone = "+50 phone"
            ))

            #endregion

            #region 'customers'
            # 1
            toAdd.append(Customers(
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
                notes = "idx 1"
            ))

            # 2
            toAdd.append(Customers(
                name = "Hans",
                surname = "Peter",
                street = "Quickhausen",
                nr = 5,
                postal = "0000",
                town = "Entenhausen",
                phone = "+83 phone",
                mobile = "+83 mobile",
                birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                approach = 1,
                notes = "First boy"
            ))

            #3
            toAdd.append(Customers(
                name = "Zorg",
                surname = "King",
                street = "Castlestreet",
                nr = 5,
                postal = "0001",
                town = "Dreamland",
                phone = "+83 phone",
                mobile = "+83 mobile",
                birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                approach = 1,
                notes = "First boy, again"
            ))

            #4
            toAdd.append(Customers(
                name = "Dagobert",
                surname = "Duck",
                street = "Gansstr.",
                nr = 5,
                postal = "0000",
                town = "Entenhausen",
                phone = "+83 phone",
                mobile = "+83 mobile",
                birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
                approach = 2,
                notes = "Not relevant"
            ))
            
            #endregion

            #region 'abos'
            #region customer 1
            toAdd.append(Abo(
                customer_id = 1,
                cycle_type = "day",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
                product = 2,
                subcategory = 2,
                quantity = 10
            ))

            toAdd.append(Abo(
                customer_id = 1,
                cycle_type = "interval",
                interval = 2,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
                product = 1,
                subcategory = 1,
                quantity = 2
            ))

            toAdd.append(Abo(
                customer_id = 1,
                cycle_type = "interval",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
                product = 4,
                subcategory = 1,
                quantity = 5
            ))

            # not relevant for tomorrow!
            toAdd.append(Abo(
                customer_id = 1,
                cycle_type = "interval",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date(),
                product = 3,
                subcategory = 1,
                quantity = 5
            ))

            #endregion

            #region customer 2
            toAdd.append(Abo(
                customer_id = 2,
                cycle_type = "day",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
                product = 5,
                subcategory = 2,
                quantity = 10
            ))

            toAdd.append(Abo(
                customer_id = 2,
                cycle_type = "interval",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
                product = 1,
                subcategory = 1,
                quantity = 5
            ))

            # not relevant for tomorrow!
            toAdd.append(Abo(
                customer_id = 2,
                cycle_type = "interval",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=2),
                product = 5,
                subcategory = 1,
                quantity = 5
            ))

            #endregion
            
            #region customer 3
            toAdd.append(Abo(
                customer_id = 3,
                cycle_type = "day",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
                product = 5,
                subcategory = 2,
                quantity = 10
            ))

            #endregion

            #region customer 4
            # not relevant for today!
            toAdd.append(Abo(
                customer_id = 4,
                cycle_type = "interval",
                interval = 5,
                next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=-1),
                product = 5,
                subcategory = 1,
                quantity = 5
            ))

            #endregion

            # add & commit
            session.add_all(toAdd)
            session.commit()
            
            #endregion

        return
    
    def tearDown(self):
        """Cleanup after test """

        base.metadata.drop_all(self.testEngine)
        self.testEngine = None

    #region 'tests'
    def test_create(self):
        """Tests the delivery overview creation """

        # run
        result = delivery.create(language = "EN", tz = "Europe/Berlin")

        # check town names
        self.assertTrue(
            all(
                [key in ['Dreamland', 'Entenhausen'] for key in result['data']['town_based'].keys()]
                )
        )

        # check town 'Dreamland'
        self.assertEqual(result['data']['town_based']['Dreamland'], {
            'customer_approach':[1], 
            'customer_street':["Castlestreet"], 
            'customer_nr':[5],
            'customer_town':["Dreamland"],
            'customer_name':["Zorg"],
            'customer_surname':["King"],
            'customer_id':[3],
            'customer_phone':["+83 phone"],
            'customer_mobile':["+83 mobile"],
            'quantity':[10], 
            'product_name':["Doppelweck"],
            'product_id':[5],
            'product_selling_price':[.5],
            'subcategory_name':["Geschnitten"],
            'category_name':["Semmel"],
            'cost':[5.00],
            'total_cost':[5.00],
            'customer_notes':["First boy, again"],
            'id':[8]
        })

        # check town 'Entenhausen'
        self.assertEqual(result['data']['town_based']['Entenhausen'], {
            'customer_approach':[1,1,3,3,3], 
            'customer_street':["Quickhausen", "Quickhausen", "Elmstreet", "Elmstreet", "Elmstreet"], 
            'customer_nr':[5,5,5,5,5],
            'customer_town':["Entenhausen", "Entenhausen", "Entenhausen", "Entenhausen", "Entenhausen"],
            'customer_name':["Hans", "Hans", "Fritz", "Fritz", "Fritz"],
            'customer_surname':["Peter", "Peter", "Meier", "Meier", "Meier"],
            'customer_id':[2,2,1,1,1],
            'customer_phone':["+83 phone", "+83 phone", "+83 phone", "+83 phone", "+83 phone"],
            'customer_mobile':["+83 mobile", "+83 mobile", "+83 mobile", "+83 mobile", "+83 mobile"],
            'quantity':[10,5,10,5,2], 
            'product_name':["Doppelweck", "Sonnenkernbrot", "Fitnessbrot", "Kaisersemmel", "Sonnenkernbrot"], 
            'product_id':[5, 1, 2, 4, 1],
            'product_selling_price':[0.5, 3.5, 5.0, 0.5, 3.5],
            'subcategory_name':["Geschnitten", "Ganz", "Geschnitten", "Ganz", "Ganz"],
            'category_name':["Semmel", "Brot", "Brot", "Semmel", "Brot"],
            'cost':[5.00, 17.50, 50.0, 2.50,7.0],
            'total_cost':[22.50, 22.50, 59.50, 59.50, 59.50],
            'customer_notes':["First boy", "First boy", "idx 1", "idx 1", "idx 1"],
            'id':[5, 6, 1, 3, 2]
        })

        # check 'overview_category'
        self.assertEqual(result['data']['overview_category'], {
            'category_name':["Brot", "Semmel"],
            'quantity':[17,25],
            'cost':[74.50, 12.50]
        })

        # check 'overview_product'
        self.assertEqual(result['data']['overview_product'], {
            'Brot':{
                'product_name':["Fitnessbrot", "Sonnenkernbrot"],
                'total':[10,7],
                'Geschnitten':[10,0],
                'Ganz':[0,7]
            },
            'Semmel':{
                'product_name':["Doppelweck", "Kaisersemmel"],
                'total':[20,5],
                'Geschnitten':[20,0],
                'Ganz':[0,5]
            }
        })

    def test_book(self):
        """Tests the order booking """

        # get old abo ids
        with Session(self.testEngine) as session:

            oldDates = {
                5:session.query(Abo).filter_by(id = 5).first().next_delivery,
                1:session.query(Abo).filter_by(id = 1).first().next_delivery,
                3:session.query(Abo).filter_by(id = 3).first().next_delivery,
                4:session.query(Abo).filter_by(id = 4).first().next_delivery,
                7:session.query(Abo).filter_by(id = 7).first().next_delivery,
            }

        # test data
        test = {
            'customer_approach':[1,1,3,3,3], 
            'customer_street':["Quickhausen", "Quickhausen", "Elmstreet", "Elmstreet", "Elmstreet"], 
            'customer_nr':[5,5,5,5,5],
            'customer_town':["Entenhausen", "Entenhausen", "Entenhausen", "Entenhausen", "Entenhausen"],
            'customer_name':["Hans", "Hans", "Fritz", "Fritz", "Fritz"],
            'customer_surname':["Peter", "Peter", "Meier", "Meier", "Meier"],
            'customer_id':[2,2,1,1,1],
            'customer_phone':["+83 phone", "+83 phone", "+83 phone", "+83 phone", "+83 phone"],
            'customer_mobile':["+83 mobile", "+83 mobile", "+83 mobile", "+83 mobile", "+83 mobile"],
            'quantity':[10,5,10,5,2], 
            'product_name':["Doppelweck", "Sonnenkernbrot", "Fitnessbrot", "Kaisersemmel", "Sonnenkernbrot"], 
            'product_id':[5, 1, 2, 4, 1],
            'product_selling_price':[0.5, 3.5, 5.0, 0.5, 3.5],
            'subcategory_name':["Geschnitten", "Ganz", "Geschnitten", "Ganz", "Ganz"],
            'category_name':["Semmel", "Brot", "Brot", "Semmel", "Brot"],
            'cost':[5.00, 17.50, 50.0, 2.50,7.0],
            'total_cost':[22.50, 22.50, 59.50, 59.50, 59.50],
            'customer_notes':["First boy", "First boy", "idx 1", "idx 1", "idx 1"],
            'id':[5, 6, 1, 3, 2]
        }

        # run
        result = delivery.book(test, "EN")

        # assert
        self.assertTrue(result['success'])

        # check db
        with Session(self.testEngine) as session:

            # get Orders
            orders = session.query(Orders)

            # assert
            """
            CAUTION:
            The orders are not added according the order of
            the passed data.
            It is added by the order of the fetched abo.id s.
            
            """

            self.assertEqual(orders.count(), 5)
            self.assertEqual(orders.first().customer_id, 1)
            self.assertEqual(orders.first().name, "Fitnessbrot")
            self.assertEqual(orders.first().total, 50.0)

            # check if abos where updated
            for i in [5,1,3]:
                self.assertNotEqual(session.query(Abo).filter_by(id = i).first().next_delivery, oldDates[i])

            # check if equal
            for i in [4,7]:
                self.assertEqual(session.query(Abo).filter_by(id = i).first().next_delivery, oldDates[i])


            

    #endregion