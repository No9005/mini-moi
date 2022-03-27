"""
Contains the handler logic for the api 

"""

# imports
import json
import base64
from flask import send_file, make_response

from miniMoi import app
from miniMoi.language import language_files
from miniMoi.logic.helpers import tools
from miniMoi.logic.functions import customer, products, categories, abo, delivery, system, bulk, reporting

#region 'handler'
def api(request:dict) -> dict:
    """Processes the POST request
    
    Takes the request dict and
    processes the request.

    params:
    -------
    request : dict
        The post request dict.
            Format: {
                'ressource':str,
                'data':{}
            }

    returns:
    --------
    dict
        success, error & data

    """

    # grab the ressource
    ressource = request['ressource']

    # differenciate by the requested ressource
    try:

        #region 'delivery'
        if ressource == "delivery/create":
            """Creates next days delivery overview

            This function creates the overview for the
            next days delivery.

            params:
            -------
            None

            returns:
            --------
            dict
                success, error & data {
                            'data':{
                                'category_name':[],
                                'quantity':[],
                                'cost':[]
                            },
                            'order':[],
                            'mapping':[]
                            },
                        'overview_product':{
                            'category_name':{
                                'data':{
                                    'product_name':[],
                                    'subcat_1:[],
                                    'subcat_2:[],
                                    'subcat_X:[],
                                    ...},
                                'order':[],
                                'mapping':[]
                            },
                            'category_name2':{
                            { ...}
                            },
                            ...
                            
                            },
                        'total_earnigns':int,
                        'total_spendings':int,
                        'town_based':{
                            'townName':{
                                'data':{
                                    'customer_approach':list[int], 
                                    'customer_street':list[str], 
                                    'customer_nr':list[int],
                                    'customer_town':list[str],
                                    'customer_name':list[str],
                                    'customer_surname':list[str],
                                    'customer_id':list[int],
                                    'customer_phone':list[str],
                                    'customer_mobile':list[str],
                                    'quantity':list[int], 
                                    'product_name':list[str],
                                    'product_id':list[int],
                                    'category_name':list[str],
                                    'subcategory_name':list[str],
                                    'product_selling_price':list[float],
                                    'cost':list[float],
                                    'total_cost':list[float],
                                    'notes':list[str]
                                    'id':list[int] # -> the abo_id}
                                    },
                                'order':[],
                                'mapping':[]
                            'townName':{
                                ...
                                },
                            ...
                        }
                    }
                } 
            
            """

            response = delivery.create(
                language = app.config['DEFAULT_LANGUAGE'],
                tz = app.config['TZ_INFO']
            )

            return response

        elif ressource == "delivery/book":
            """Books the manipulated data

            Function takes the orders data,
            adds it to the Orders table and
            saves a excel file to disk.

            params:
            -------
            data : dict
                The town based data for each abo.
                    Format: {
                            'customer_approach':list[int], 
                            'customer_street':list[str], 
                            'customer_nr':list[int],
                            'customer_town':list[str],
                            'customer_name':list[str],
                            'customer_surname':list[str],
                            'customer_id':list[int],
                            'customer_phone':list[str],
                            'customer_mobile':list[str],
                            'quantity':list[int], 
                            'product_name':list[str], 
                            'product_id':list[int],
                            'category_name':list[str],
                            'subcategory_name':list[str],
                            'product_selling_price':list[float],
                            'cost':list[float],
                            'total_cost':list[float],
                            'notes':list[str]
                            'id':list[int] # -> the abo_id
                            }
                    }
        
            returns:
            -------
            dict
                success, error & data {
                    'msg':str
                }
            
            """

            # got jsonified data. turn into json
            data = json.loads(request['data']['data'])

            response = delivery.book(
                data = data,
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "delivery/saveData":
            """Creates the cover & overview and saves it.

            params:
            -------
            data : dict
                The town based data for each abo.
                    Format: {
                            'customer_approach':list[int], 
                            'customer_street':list[str], 
                            'customer_nr':list[int],
                            'customer_town':list[str],
                            'customer_name':list[str],
                            'customer_surname':list[str],
                            'customer_id':list[int],
                            'customer_phone':list[str],
                            'customer_mobile':list[str],
                            'quantity':list[int], 
                            'product_name':list[str], 
                            'product_id':list[int],
                            'category_name':list[str],
                            'subcategory_name':list[str],
                            'product_selling_price':list[float],
                            'cost':list[float],
                            'total_cost':list[float],
                            'notes':list[str]
                            'id':list[int] # -> the abo_id
                            }
                    }
            save_cover : bool, optional
                If true, the excel cover is printed.
                (default is True)
            save_overview : bool, optional
                If true, the excel overview is printed.
                (default is True)
        
            returns:
            -------
            dict
                success, error & data {
                    'msg':str
                }

            """

            # got jsonified data. turn into json
            data = json.loads(request['data']['data'])

            response = delivery.save_data(
                data = data,
                save_cover = True,
                save_overview = True,
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "delivery/orderDetails":
            """Create order details overview

            Creates the excel overview and returns it.

            params:
            -------
            data : dict
                The town based data for each abo.
                    Format: {
                            'customer_approach':list[int], 
                            'customer_street':list[str], 
                            'customer_nr':list[int],
                            'customer_town':list[str],
                            'customer_name':list[str],
                            'customer_surname':list[str],
                            'customer_id':list[int],
                            'customer_phone':list[str],
                            'customer_mobile':list[str],
                            'quantity':list[int], 
                            'product_name':list[str], 
                            'product_id':list[int],
                            'category_name':list[str],
                            'subcategory_name':list[str],
                            'product_selling_price':list[float],
                            'cost':list[float],
                            'total_cost':list[float],
                            'notes':list[str]
                            'id':list[int] # -> the abo_id
                            }
                    }
        
            returns:
            -------
            send_file | dict
                Format:
                    File: send_file()
                    Dict: {
                        success, 
                        error,
                        data:{
                            'file':io.BytesIO,
                            'date':str
                        }

            """

            response = delivery.print_order_details(
                data = request['data'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            if not response['success']: return response
            else: 
                
                return send_file(
                    response['data']['file'], 
                    attachment_filename="miniMoi_order_details_" + response['data']['date'] + ".xlsx",
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    as_attachment=True
                )

        #endregion

        #region 'customers'
        elif ressource == "customers/get":
            """Returns the requested customers

            params:
            -------
            filter_type : str | None
                Indicates the type of filter to apply.
                    Options: { None, 'customer', 
                            'town' }
                            None: Fetches data by id
                                interval.
                            'customer': Searches for
                                        a singel customer.
                            'town': Searches for all
                                    customers in one town.
            what : str | None:
                Indicates the query phrase.
                    Example: if None, the string indicates
                            the interval of ids.
            amount : int | None, optional
                The number of entries to query.
                (default is None).
    
            returns:
            --------
            dict
                success, error, data {
                    'data':[
                        {
                            'id':list[int],
                            'date':list[datetime],
                            'name':list[str],
                            'surname':list[str],
                            'street':list[str],
                            'nr':list[int],
                            'postal':list[str],
                            'town':list[str],
                            'phone':list[str],
                            'mobile':list[str],
                            'birthdate':list[str]("%Y.%m.%d),
                            'approach':list[int],
                            'notes':list[str],
                        },
                        ...
                    ],
                    'order':[],
                    'mapping':[]
                }

            """

            response = customer.get(
                filter_type = request['data']['filter_type'],
                what = request['data']['what'],
                amount = request['data']['amount'],
                language = app.config['DEFAULT_LANGUAGE'],
                tz = app.config['TZ_INFO']
            )

            return response

        elif ressource == "customers/delete":
            """Deletes a customer

            params:
            -------
            id : int
                the customer unique id.

            returns:
            -------
            dict
                success, error & data {
                    'msg':str
                }
            
            """

            response = customer.delete(
                customer_id = int(request['data']['id']),
                language = app.config['DEFAULT_LANGUAGE'],
            )

            return response
        
        elif ressource == "customers/add":
            """Adds customers to the db

            The add function either adds only one
            customer or a complete list of customers.

            params:
            -------
            to_add : list
                A list containing every single new
                customer.
                    Format: [
                        {
                            'name':str,
                            'surname':str,
                            'street':str,
                            'nr':int,
                            'postal':str,
                            'town':str,
                            'phone':str,
                            'mobile':str,
                            'birthdate':str("%Y-%m-%d),
                            'approach':int,
                            'notes':str
                        },
                        ...
                    ]

            returns:
            --------
            dict
                success, error & data {
                    'msg':str
                }
            
            """

            response = customer.add(
                customers = request['data']['to_add'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "customers/update":
            """Updates a single customer

            params:
            -------
            id : int
                The customer unique id.
            data : dict
                A dict containing the data
                to update.
                    Format: {
                        'name':str,
                        'surname':str,
                        'street':str,
                        'nr':int,
                        'postal':str,
                        'town':str,
                        'phone':str,
                        'mobile':str,
                        'birthdate':str("%Y.%m.%d)
                        'notes':str
                    }
    
            returns:
            -------
            dict
                success, error & data {
                    'msg':str
                }

            """

            response = customer.update(
                customer_id = int(request['data']['id']),
                data = request['data'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        #endregion
        
        #region 'products'
        elif ressource == "products/get":
            """Returns the requested products

            params:
            -------
            filter_type : str | None
                Indicates the type of filter to apply.
                    Options: { None, 'product', 
                            'category' }
                            None: Fetches data by id
                                interval.
                            'product': Searches for
                                        a singel product.
                            'category': Searches for all
                                        products in one
                                        category.
            what : str | None:
                Indicates the query phrase.
                    Example: if None, the string indicates
                            the interval of ids.
            amount : int | None, optional
                The number of entries to query.
                (default is None).

            returns:
            --------
            dict
                success, error, data {
                    'result':[
                        {
                            'id':int,
                            'name':str,
                            'category':int,
                            'purchase_price':float,
                            'selling_price':float,
                            'store':str,
                            'phone':str
                        },
                        ...
                    ]
                }

            """

            response = products.get(
                filter_type = request['data']['filter_type'],
                what = request['data']['what'],
                amount = request['data']['amount'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "products/add":
            """Adds products to the db

            The add function either adds only one
            or multiple products.

            params:
            -------
            to_add : list
                A list containing every single new
                product.
                    Format: [
                        {
                            'name':str,
                            'category':int,
                            'purchase_price':float,
                            'selling_price':float,
                            'store':str,
                            'phone':str
                        },
                        ...
                    ]
 

            returns:
            --------
            dict
                success, error & data {}

            """

            response = products.add(
                products = request['data']['to_add'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "products/delete":
            """Deletes a product

            params:
            -------
            id : int
                the customer unique id.

            returns:
            -------
            dict
                success, error & data

            """

            response = products.delete(
                product_id = int(request['data']['id']),
                language = app.config['DEFAULT_LANGUAGE'],
            )

            return response

        elif ressource == "products/update":
            """Updates a single product

            params:
            -------
            id : int
                The customer unique id.
            data : dict
                A dict containing the data
                to update.
                    Format: {
                        'name':str,
                        'category':int,
                        'purchase_price':float,
                        'selling_price':float,
                        'store':str,
                        'phone':str
                    }

            returns:
            -------
            dict
                success, error & data
    
            """

            response = products.update(
                product_id = int(request['data']['id']),
                data = request['data'],
                language = app.config['DEFAULT_LANGUAGE'],
            )

            return response

        #endregion

        #region 'category'
        elif ressource == "category/get":
            """Gets all product categories

            Fetches all product categories
            and return them.

            params:
            -------
            amount : int | None, optional
                The number of entries to query.
                (default is None).

            returns:
            -------
            dict
                success, error & data {
                    'result':[
                        {
                            'id':int,
                            'name':str
                        },
                        ...
                    ]
                }

            """

            response = categories.get(
                amount = request['data']['amount'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "category/add":
            """Adds categories to the db

            The add function either adds only one
            or multiple categories.

            params:
            -------
            to_add : list
                A list containing every single new
                category.
                    Format: [
                        {"name":'name'},
                        {"name":'name'},
                        ...
                    ]

            returns:
            --------
            dict
                success, error & data {}

            """

            response = categories.add(
                categories = request['data']['to_add'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "category/delete":
            """Deletes a category

            params:
            -------
            id : int
                the category unique id.

            returns:
            -------
            dict
                success, error & data

            """

            response = categories.delete(
                category_id = int(request['data']['id']),
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "category/update":
            """Updates a single category

            params:
            -------
            id : int
                The customer unique id.
            name : str
                The new category name

            returns:
            -------
            dict
                success, error & data

            """

            response = categories.update(
                category_id = int(request['data']['id']),
                name = request['data']['name'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        #endregion

        #region 'subcategory'
        elif ressource == "subcategory/get":
            """Gets all product subcategory

            Fetches all product subcategory
            and return them.

            params:
            -------
            amount : int | None, optional
                The number of entries to query.
                (default is None).

            returns:
            -------
            dict
                success, error & data {
                    'result':[
                        {
                            'id':int,
                            'name':str
                        },
                        ...
                    ]
                }

            """

            response = categories.get(
                category_type = "subcategory",
                amount = request['data']['amount'],
                language = app.config['DEFAULT_LANGUAGE'],
            )

            return response

        elif ressource == "subcategory/add":
            """Adds subcategory to the db

            The add function either adds only one
            or multiple subcategory.

            params:
            -------
            to_add : list
                A list containing every single new
                category.
                    Format: [
                        {"name":'name'},
                        {"name":'name'},
                        ...
                    ]

            returns:
            --------
            dict
                success, error & data {}

            """

            response = categories.add(
                categories = request['data']['to_add'],
                category_type = "subcategory",
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "subcategory/delete":
            """Deletes a subcategory

            params:
            -------
            id : int
                the category unique id.

            returns:
            -------
            dict
                success, error & data

            """

            response = categories.delete(
                category_id = int(request['data']['id']),
                category_type = "subcategory",
                language = app.config['DEFAULT_LANGUAGE'],
            )

            return response

        elif ressource == "subcategory/update":
            """Updates a single subcategory

            params:
            -------
            id : int
                The customer unique id.
            name : str
                The new category name

            returns:
            -------
            dict
                success, error & data

            """

            response = categories.update(
                category_id = int(request['data']['id']),
                category_type = "subcategory",
                name = request['data']['name'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        #endregion
        
        #region 'abo'
        elif ressource == "abo/get":
            """Returns the requested abos

            params:
            -------
            filter_type : str | None
                Indicates the type of filter to apply.
                    Options: { None, 'abo', 
                            'customer' }
                            None: Fetches data by id
                                interval.
                            'abo': searches for a single
                                abo.
                            'customer': Searches for all
                                        abos for one cust-
                                        omer.
            what : str | None:
                Indicates the query phrase.
                    Example: if None, the string indicates
                            the interval of ids.
            amount : int | None, optional
                The number of entries to query.
                (default is None).

            returns:
            --------
            dict
                success, error, data {
                    'result':[
                        {
                            'id':int
                            'customer_id':int,
                            'update_date':str,
                            'cycle_type':str,
                            'interval':int,
                            'next_delivery':str,
                            'product_id':int
                            'product_name':str
                        },
                        ...
                    ]
                }

            """

            response = abo.get(
                filter_type = request['data']['filter_type'],
                what = request['data']['what'],
                amount = request['data']['amount'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "abo/add":
            """Adds abos to a customer

            This function adds one or
            multiple abos to a specific
            customer.

            params:
            -------
            to_add : list
                A list containing every single new
                abo for the customer.
                    Format: [
                        {
                            'customer_id':int,
                            'cycle_type':str,
                            'interval':int,
                            'product':int,
                        },
                        ...
                    ]
            
            returns:
            --------
            dict
                success, error, data

            """

            response = abo.add(
                abos = request['data']['to_add'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        elif ressource == "abo/delete":
            """Deletes one specific abo

            params:
            -------
            abo_id : int
                the abo unique id.

            returns:
            -------
            dict
                success, error & data

            """

            response = abo.delete(
                abo_id = int(request['data']['id']),
                language = app.config['DEFAULT_LANGUAGE'],
            )

            return response

        elif ressource == "abo/update":
            """Updates a single abo for a customer

            params:
            -------
            customer_id : int
                The customer unique id.
            data : dict
                A dict containing the data
                to update.
                    Format: {
                        'cycle_type':str,
                        'interval':int,
                        'product':int,
                        'custom_next_delivery':str | None
                    }

            returns:
            -------
            dict
                success, error & data

            """

            response = abo.update(
                abo_id = int(request['data']['id']),
                data = request['data'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            return response

        #endregion

        #region 'orders'
        elif ressource == "orders/get":
            pass

        #endregion

        #region 'system'
        elif ressource == "system/dbBackup":
            """Copies the mini-moi db to the documents folder """

            response = system.make_db_copy()

            return response

        elif ressource == "system/dbRollback":
            """Rollback the db with old backup
            
            params:
            ------
            filename : str
                The name of the file to import

            returns:
            --------
            dict    
                success, error & data {msg}

            """

            response = system.rollback_db_save(
                filename = request['data']['filename']
            )

            return response 
            
        #endregion

        #region 'bulk'
        elif ressource == "bulk/createBlueprint":
            """Creates a blueprint for given table
    
            This function creates a blueprint for the
            given sql table.
            The blueprint is a empty excel with the correct
            columns in the specified app.config language.
            
            params:
            -------
            blueprint : str
                The name of the blueprint to create.
                    Options: { 'customers', 'category'
                            'subcategory', 'products',
                            'abo' }

            returns:
            --------
            dict
                success, error & datat {msg:str}
            
            """

            response = bulk.create_blueprint(
                blueprint = request['data']['blueprint'],
                file_type=app.config['FILE_TYPE']
            )

            return response

        elif ressource == "bulk/update":
            """Reads all blueprints and updates the tables
    
            This function reads all tables in the
            directory '~/mini-moi/blueprints'
            and updates the tables
            
            params:
            -------
            None

            returns:
            -------
            dict
                success, error & data {
                    'msg':str
                }

            """

            response = bulk.update(file_type=app.config['FILE_TYPE'])

            return response

        #endregion

        #region 'report'
        elif ressource == "reporting/get":
            """Creates the report """

            response = reporting.get_report()

            return response
        
        #endregion

        else: 
            
            # grab the language files
            try: errors = language_files[request['language']]['error_codes']
            except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

            return {'success':False, 'error':errors['404'].format(ressource=ressource), 'data':{}}


    except Exception as e: 
        
        # get code & msg
        code, msg = tools._convert_exception(e)

        # grab the language files
        try: errors = language_files[request['language']]['error_codes']
        except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']
        
        return {'success':False, 'error':errors['500'].format(
            c=str(code),
            m = str(msg)
        ), 'data':{}}

    return

#endregion