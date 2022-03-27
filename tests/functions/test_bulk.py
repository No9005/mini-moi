"""
Tests the functions in bulk.py

"""

# imports
import unittest
from unittest.mock import patch

import pandas as pd

from miniMoi import app, base
from miniMoi.logic.functions import bulk
import miniMoi.models.Models as models

from tests import testEngine

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from pathlib import Path

# create session macker to mock it
testSessionFactory = sessionmaker(bind=testEngine)
testSession = scoped_session(testSessionFactory)

# test class
@patch('miniMoi.logic.functions.bulk.Session', testSession)
class TestBulk(unittest.TestCase):
    """Tests the bulk functions

    CAUTION:
    Some 'private' functions are not tested because
    there are just mocks:
        - _unlink
        - _to_csv
        - _to_load

    methods:
    --------
    setUp
        Tests setup
    tearDown
        Clean after test
    test_create_blueprint
        Tests the blueprint creation
    test_update
        tests the bulk updater

    """

    def setUp(self) -> None:
        """Setup """

        # copy engine to self.
        self.testEngine = testEngine

        # create db (empty)
        base.metadata.create_all(self.testEngine)

    def tearDown(self) -> None:
        """Cleanup after tests """

        base.metadata.drop_all(self.testEngine)
        self.testEngine = None

    #region 'tests'
    @patch('miniMoi.logic.functions.bulk.Path.mkdir', return_value = "mock_mkdir")
    @patch('miniMoi.logic.functions.bulk._to_csv', return_value = {'success':True})
    def test_create_blueprint(self, mock_csv, mock_mkdir):
        """Tests the blueprint creator """

        # create app context
        with app.app_context():
            app.config['DEFAULT_LANGUAGE'] = "EN"
            app.config['BLUEPRINT_PATH'] = Path().cwd() / "unittestFOLDER"

            #region 'tests' -------------
            #region 'blueprint == customers'
            result = bulk.create_blueprint("customers")

            # assert
            self.assertTrue(result['success'])
            self.assertEqual(mock_csv.call_args_list[0][0][0].columns.tolist(), [
                'id', 'Date', 'Name', 'Surname', 'Street', 'Nr', 'Postal', 'City',
                'Phone',  'Mobile', 'Birthdate', 'Approach', 'Notes'
            ])

            self.assertEqual(mock_csv.call_args_list[0][0][1], str(app.config['BLUEPRINT_PATH']/"customers_blueprint.csv"))

            #endregion

            #region 'blueprint == category'
            result = bulk.create_blueprint("category")

            # assert
            self.assertTrue(result['success'])
            self.assertEqual(mock_csv.call_args_list[-1][0][0].columns.tolist(), [
                'id', 'Name'
            ])

            self.assertEqual(mock_csv.call_args_list[-1][0][1], str(app.config['BLUEPRINT_PATH']/"category_blueprint.csv"))

            #endregion

            #region 'blueprint == subcategory'
            result = bulk.create_blueprint("subcategory")

            # assert
            self.assertTrue(result['success'])
            self.assertEqual(mock_csv.call_args_list[-1][0][0].columns.tolist(), [
                'id', 'Name'
            ])

            self.assertEqual(mock_csv.call_args_list[-1][0][1], str(app.config['BLUEPRINT_PATH']/"subcategory_blueprint.csv"))

            #endregion

            #region 'blueprint == products'
            result = bulk.create_blueprint("products")

            # assert
            self.assertTrue(result['success'])
            self.assertEqual(mock_csv.call_args_list[-1][0][0].columns.tolist(), [
                'id', 'Name', 'Category', 'Purchase price', 'Selling price', 'Margin', 'Store',
                'Phone'
            ])

            self.assertEqual(mock_csv.call_args_list[-1][0][1], str(app.config['BLUEPRINT_PATH']/"products_blueprint.csv"))

            #endregion

            #region 'blueprint == abo'
            result = bulk.create_blueprint("abo")

            self.assertTrue(result['success'])
            self.assertEqual(mock_csv.call_args_list[-1][0][0].columns.tolist(), [
                'id', 'Customer id', 'Update date', 'Cycle type', 'Interval', 'Next delivery', 'Product',
                'Subcategory', 'Qnt.'
            ])

            self.assertEqual(mock_csv.call_args_list[-1][0][1], str(app.config['BLUEPRINT_PATH']/"abo_blueprint.csv"))

            #endregion

            #endregion

    @patch('miniMoi.logic.functions.bulk.products_add', return_value = {'success':True})
    @patch('miniMoi.logic.functions.bulk.categories_add', return_value = {'success':True})
    @patch('miniMoi.logic.functions.bulk.customer_add', return_value = {'success':True})
    @patch('miniMoi.logic.functions.bulk.abo_add', return_value = {'success':True})
    @patch('miniMoi.logic.functions.bulk._unlink', return_value = "mock_unlink")
    @patch('miniMoi.logic.functions.bulk._load')
    def test_update(self, mock_load, mock_unlink, mock_abo, mock_customer, mock_categories, mock_products):
        """Tests the db updater """

        #region 'create the possible dfs'
        """
        CAUTION:
        We will also add some official names too. see what happens
        
        """
        dfs = {
            'customers':pd.DataFrame({
                'id':[16,None],
                'Date':[None, None],
                'Name':["Michael", "Daniel"],
                'surname':["Meier", "Meier2"],
                'Street':["Str1", "str2"],
                'nr':[5, 6],
                'postal':["1234", "5678"],
                'City':["Spatzenheim", "Krügge"],
                'phone':[None, "+495555"],
                'mobile':["",""],
                'birthdate':["1900.08.16", "1400.02.02"],
                'approach':[5,10],
                'notes':["A", None]
            }),
            'category':pd.DataFrame({
                'id':[16,17,18],
                'name':["Brot","Milch", "Schnitzel"]
            }),
            'subcategory':pd.DataFrame({
                'id':[100,1,2],
                'name':["Geschnitten", "Hart", "Weich"]
            }),
            'products':pd.DataFrame({
                'id':[100,500],
                'name':["Baguette", "Buchtel"],
                'category':["Brot", "Milch"],
                'purchase_price':["1.50", 1.55],
                'Selling price':[12, 1.49],
                'margin':[13,13],
                'store':["Myne", None],
                'phone':[None, "+49"],
            }),
            'abo':pd.DataFrame({
                'id':[3,4,5],
                'Customer id':[1,2,1],
                'Update date':[None, None, ""],
                'Cycle type':["Weekday", None, "Interval"],
                'interval':["Wendsday", None, "80"],
                'next_delivery':[None, "2022.12.12", "None"],
                'Product':["Buchtel", "Baguette", "Baguette"],
                'subcategory':["Weich", "Hart", "Hart"],
                'quantity':[1,2,3]
            })
        }

        #endregion

        #region 'add categories, subcats & products to db'
        with Session(self.testEngine) as session:

            session.add_all([
                models.Category(name="Brot"),
                models.Category(name="Milch"),
                models.Category(name="Schnitzel"),
                models.Subcategory(name="Geschnitten"),
                models.Subcategory(name="Hart"),
                models.Subcategory(name="Weich"),
                models.Products(
                    name="Baguette",
                    category=1,
                    purchase_price=1.50,
                    selling_price=12.,
                    margin=0.0,
                    store="Myne",
                    phone=""
                ),
                models.Products(
                    name="Buchtel",
                    category=2,
                    purchase_price=1.55,
                    selling_price=1.49,
                    margin=0.0,
                    store="",
                    phone=""
                )
            ])

            session.commit()


        #endregion

        #region 'run tests' -----------------------------
        with app.app_context():
            app.config['DEFAULT_LANGUAGE'] = "EN"
            app.config['BLUEPRINT_PATH'] = Path().cwd() / "unittestFOLDER"

            #region 'df is empty'
            # mock update
            mock_load.return_value = {
                'success':True, 
                'data':{
                    'loaded':{
                        'products':{
                            'file':pd.DataFrame(columns=['id', 'name']),
                            'path':"somepath"
                        },
                    }
                }
            }

            # run
            result = bulk.update()

            # assert
            self.assertTrue(result['success'])
            self.assertEqual(result['data']['msg'], 'Successfull: {}, Failures: {products is empty}')

            #endregion

            #region 'update only customers'
            mock_load.return_value = {
                'success':True, 
                'data':{
                    'loaded':{
                        'customers':{
                            'file':dfs['customers'],
                            'path':"somepath"
                        },
                    }
                }
            }

            # run
            result = bulk.update()

            # assert
            self.assertTrue(result['success'])

            # get results as dict
            tmp = pd.DataFrame(mock_customer.call_args_list[-1][0][0]).fillna(-99).to_dict('list')

            # comparison frame
            tmpComp = {
                'id':[16, -99],
                'date':[-99, -99],
                'name':["Michael", "Daniel"],
                'surname':["Meier", "Meier2"],
                'street':["Str1", "str2"],
                'nr':[5, 6],
                'postal':["1234", "5678"],
                'town':["Spatzenheim", "Krügge"],
                'phone':[-99, "+495555"],
                'mobile':["",""],
                'birthdate':["1900.08.16", "1400.02.02"],
                'approach':[5,10],
                'notes':["A", -99]
            }


            for key, val in tmp.items():
                self.assertEqual(val, tmpComp[key])

            #endregion

            #region 'update only category'
            mock_load.return_value = {
                'success':True, 
                'data':{
                    'loaded':{
                        'category':{
                            'file':dfs['category'],
                            'path':"somepath"
                        },
                    }
                }
            }

            # run
            result = bulk.update()

            # assert
            self.assertTrue(result['success'])

            # get results as dict
            tmp = pd.DataFrame(mock_categories.call_args_list[-1][0][0]).fillna(-99).to_dict('list')

            # comparison frame
            tmpComp = {
                'id':[16,17,18],
                'name':["Brot","Milch", "Schnitzel"]
            }

            for key, val in tmp.items():
                self.assertEqual(val, tmpComp[key])

            #endregion

            #region 'update only subcategory'
            mock_load.return_value = {
                'success':True, 
                'data':{
                    'loaded':{
                        'subcategory':{
                            'file':dfs['subcategory'],
                            'path':"somepath"
                        },
                    }
                }
            }

            # run
            result = bulk.update()

            # assert
            self.assertTrue(result['success'])

            # get results as dict
            tmp = pd.DataFrame(mock_categories.call_args_list[-1][0][0]).fillna(-99).to_dict('list')

            # comparison frame
            tmpComp = {
                'id':[100,1,2],
                'name':["Geschnitten", "Hart", "Weich"]
            }

            for key, val in tmp.items():
                self.assertEqual(val, tmpComp[key])

            #endregion

            #region 'update only products'
            mock_load.return_value = {
                'success':True, 
                'data':{
                    'loaded':{
                        'products':{
                            'file':dfs['products'],
                            'path':"somepath"
                        },
                    }
                }
            }

            # run
            result = bulk.update()

            # assert
            self.assertTrue(result['success'])

            # get results as dict
            tmp = pd.DataFrame(mock_products.call_args_list[-1][0][0]).fillna(-99).to_dict('list')

            # comparison frame
            tmpComp = {
                'id':[100,500],
                'name':["Baguette", "Buchtel"],
                'category':[1, 2],
                'purchase_price':["1.50", 1.55],
                'selling_price':[12, 1.49],
                'margin':[13,13],
                'store':["Myne", -99],
                'phone':[-99, "+49"],
            }

            for key, val in tmp.items():
                self.assertEqual(val, tmpComp[key])

            #endregion

            #region 'update only abo'
            mock_load.return_value = {
                'success':True, 
                'data':{
                    'loaded':{
                        'abo':{
                            'file':dfs['abo'],
                            'path':"somepath"
                        },
                    }
                }
            }

            # run
            result = bulk.update()

            # assert
            self.assertTrue(result['success'])

            # get results as dict
            tmp = pd.DataFrame(mock_abo.call_args_list[-1][0][0]).fillna(-99).to_dict('list')

            # comparison frame
            tmpComp = {
                'id':[3,4,5],
                'customer_id':[1,2,1],
                'update_date':[-99, -99, ""],
                'cycle_type':["day", 'None', "interval"],
                'interval':[2, -99, "80"],
                'next_delivery':["None", "2022.12.12", "None"],
                'product':[2, 1, 1],
                'subcategory':[3, 2, 2],
                'quantity':[1,2,3]
            }

            for key, val in tmp.items():
                self.assertEqual(val, tmpComp[key])

            #endregion

            #region 'update abo with unknown product'
            # create frame with uknown product
            withUnknown = pd.DataFrame({
                'id':[3,4,5],
                'Customer id':[1,2,1],
                'Update date':[None, None, ""],
                'Cycle type':["Weekday", None, "Interval"],
                'interval':["Wendsday", None, "80"],
                'next_delivery':[None, "2022.12.12", "None"],
                'Product':["Buchtel", "Baguette", "Schnecke"],
                'subcategory':["Weich", "Hart", "Hart"],
                'quantity':[1,2,3]
            })

            mock_load.return_value = {
                'success':True, 
                'data':{
                    'loaded':{
                        'abo':{
                            'file':withUnknown,
                            'path':"somepath"
                        },
                    }
                }
            }

            # run -> should fail, cause 'Schnecke' is not int-convertable
            with self.assertRaises(ValueError) as e:
                result = bulk.update()

            #endregion


        #endregion

    #endregion