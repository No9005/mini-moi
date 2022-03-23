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
from miniMoi.logic.functions import customer, products, categories, abo, delivery

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
                    'overview_category':{
                        'category_name':[],
                        'quantity':[],
                        'cost':[]
                        },
                    'overview_product':{
                        'category_name':{
                            'product_name':[],
                            'subcat_1:[],
                            'subcat_2:[],
                            'subcat_X:[],
                            ...
                        },
                        'category_name2':{
                            ...
                        },
                        ...
                        
                        },
                    'total_earnings':int,
                    'town_based':{
                        'townName':{
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
                            },
                        'townName':{
                            ...
                            },
                        ...
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

            This function takes the data and adds 
            the provided info to the 'Orders' table.
            It also calculates the next delivery
            date.
            In the end it returns the printed excel.

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
            
            """

            response = delivery.book(
                data = request['data'],
                language = app.config['DEFAULT_LANGUAGE']
            )

            if not response['success']: return response
            else: 
                
                # reference: https://stackoverflow.com/questions/27337013/how-to-send-zip-files-in-the-python-flask-framework
                return send_file(
                    response['data']['zip'], 
                    attachment_filename="miniMoi_overview_" + response['data']['date'] + ".zip",
                    as_attachment=True
                )

        elif ressource == "delivery/cover":
            """Create the cover excel sheet

            Creates the excel cover and returns it.

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

            # got jsonified data. turn into json
            data = json.loads(request['data']['data'])

            response = delivery.print_cover(
                data = data,
                language = app.config['DEFAULT_LANGUAGE']
            )

            if not response['success']: return response
            else: 

                newResponse = {
                    'success':True,
                    'data':{
                        'content':base64.b64encode(response['data']['file'].getvalue()).decode(),
                        'name':"miniMoi_cover_" + response['data']['date'] + ".xlsx"
                    }
                    
                }

                #https://stackoverflow.com/questions/63921787/display-image-from-flask-send-file-ajax-response-into-the-image-tag
                #newResponse = make_response(
                #    base64.b64encode(response['data']['file']))
                #newResponse.headers['Content-Type'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                #newResponse.headers.set(
                #    'Content-Disposition', 
                #    'attachment', 
                #    filename="miniMoi_cover_" + response['data']['date'] + ".xlsx"
                #    )

                return newResponse
                
                """return send_file(
                    response['data']['file'], 
                    attachment_filename="miniMoi_cover_" + response['data']['date'] + ".xlsx",
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    as_attachment=True
                )"""

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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            --------
            dict
                success, error, data {
                    'result':[
                        'name':str,
                        'surname':str,
                        'street':str,
                        'nr':int,
                        'postal':str,
                        'town':str,
                        'phone':str,
                        'mobile':str,
                        'birthdate':str("%Y.%m.%d)
                        'notes':str,
                        ...
                    ]
                }

            """

            response = customer.get(
                filter_type = request['filter_type'],
                what = request['what'],
                amount = request['amount'],
                language = request['language'],
                tz = app.config['TZ_INFO']
            )

            return response

        elif ressource == "customers/delete":
            """Deletes a customer

            params:
            -------
            customer_id : int
                the customer unique id.
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])
            
            returns:
            -------
            dict
                success, error & data
            
            """

            response = customer.delete(
                customer_id = request['customer_id'],
                language = request['language'],
            )

            return response
        
        elif ressource == "customers/add":
            """Adds customers to the db

            The add function either adds only one
            customer or a complete list of customers.

            params:
            -------
            customers : list
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
                            'birthdate':str("%Y.%m.%d)
                            'notes':str
                        },
                        ...
                    ]
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])


            returns:
            --------
            dict
                success, error & data {}
            """

            response = customer.add(
                customers = request['customers'],
                language = request['language']
            )

            return response

        elif ressource == "customer/update":
            """Updates a single customer

            params:
            -------
            customer_id : int
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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            -------
            dict
                success, error & data

            """

            response = customer.update(
                customer_id = request['customer_id'],
                data = request['data'],
                language = request['language']
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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

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
                filter_type = request['filter_type'],
                what = request['what'],
                amount = request['amount'],
                language = request['language'],
            )

        elif ressource == "products/add":
            """Adds products to the db

            The add function either adds only one
            or multiple products.

            params:
            -------
            products : list
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
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])


            returns:
            --------
            dict
                success, error & data {}

            """

            response = products.add(
                products = request['products'],
                language = request['language']
            )

            return response

        elif ressource == "products/delete":
            """Deletes a product

            params:
            -------
            product_id : int
                the customer unique id.
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])
            
            returns:
            -------
            dict
                success, error & data

            """

            response = products.delete(
                product_id = request['product_id'],
                language = request['language'],
            )

            return response

        elif ressource == "products/update":
            """Updates a single product

            params:
            -------
            product_id : int
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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            -------
            dict
                success, error & data
    
            """

            response = customer.update(
                product_id = request['product_id'],
                data = request['data'],
                language = request['language']
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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

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
                amount = request['amount'],
                language = request['language'],
            )

            return response

        elif ressource == "category/add":
            """Adds categories to the db

            The add function either adds only one
            or multiple categories.

            params:
            -------
            categories : list
                A list containing every single new
                category.
                    Format: [
                        'name',
                        'name',
                        ...
                    ]
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            --------
            dict
                success, error & data {}

            """

            response = categories.add(
                categories = request['categories'],
                language = request['language']
            )

            return response

        elif ressource == "category/delete":
            """Deletes a category

            params:
            -------
            category_id : int
                the category unique id.
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])
            
            returns:
            -------
            dict
                success, error & data

            """

            response = categories.delete(
                category_id = request['category_id'],
                language = request['language'],
            )

            return response

        elif ressource == "category/update":
            """Updates a single category

            params:
            -------
            category_id : int
                The customer unique id.
            name : str
                The new category name
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            -------
            dict
                success, error & data

            """

            response = categories.update(
                category_id = request['category_id'],
                name = request['name'],
                language = request['language']
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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

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
                amount = request['amount'],
                language = request['language'],
            )

            return response

        elif ressource == "subcategory/add":
            """Adds subcategory to the db

            The add function either adds only one
            or multiple subcategory.

            params:
            -------
            categories : list
                A list containing every single new
                category.
                    Format: [
                        'name',
                        'name',
                        ...
                    ]
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            --------
            dict
                success, error & data {}

            """

            response = categories.add(
                categories = request['categories'],
                category_type = "subcategory",
                language = request['language']
            )

            return response

        elif ressource == "subcategory/delete":
            """Deletes a subcategory

            params:
            -------
            category_id : int
                the category unique id.
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])
            
            returns:
            -------
            dict
                success, error & data

            """

            response = categories.delete(
                category_id = request['category_id'],
                category_type = "subcategory",
                language = request['language'],
            )

            return response

        elif ressource == "subcategory/update":
            """Updates a single subcategory

            params:
            -------
            category_id : int
                The customer unique id.
            name : str
                The new category name
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            -------
            dict
                success, error & data

            """

            response = categories.update(
                category_id = request['category_id'],
                category_type = "subcategory",
                name = request['name'],
                language = request['language']
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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE'])

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
                filter_type = request['filer_type'],
                what = request['what'],
                amount = request['amount'],
                language = request['language'],
                tz = app.config['TZ_INFO']
            )

            return response

        elif ressource == "abo/add":
            """Adds abos to a customer

            This function adds one or
            multiple abos to a specific
            customer.

            params:
            -------
            customer_id : int
                The id of the customer to add
                the abo to.
            abos : list
                A list containing every single new
                abo for the customer.
                    Format: [
                        {
                            'cycle_type':str,
                            'interval':int,
                            'product':int,
                        },
                        ...
                    ]
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            --------
            dict
                success, error, data

            """

            response = abo.add(
                customer_id = request['customer_id'],
                abos = request['abos'],
                language = request['language'],
                tz = app.config['TZ_INFO']
            )

            return response

        elif ressource == "abo/delete":
            """Deletes one specific abo

            params:
            -------
            abo_id : int
                the abo unique id.
            language : str, optional
                The language iso. Needed for the error
                msg.
                (default is app.config['DEFAULT_LANGUAGE])
            
            returns:
            -------
            dict
                success, error & data

            """

            response = abo.delete(
                abo_id = request['abo_id'],
                language = request['language'],
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
            language : str, optional
                the language iso code. Needed for the
                error msg.
                (default is app.config['DEFAULT_LANGUAGE])

            returns:
            -------
            dict
                success, error & data

            """

            response = abo.update(
                abo_id = request['abo_id'],
                data = request['data'],
                language = request['language'],
                tz = app.config['TZ_INFO']
            )

            return response

        #endregion

        #region 'orders'
        elif ressource == "orders/get":
            pass

        #endregion

        else: return {'success':False, 'error':errors['404'].format(ressource=ressource), 'data':{}}


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