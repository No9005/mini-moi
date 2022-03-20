"""
Contains the handler logic for the api 

"""

# imports
from miniMoi.logic.functions import customer, products, category, abo

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
        if ressource == "delivery/overview/create":
            pass

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

            response = category.get(
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

            response = category.add(
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

            response = category.delete(
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

            response = category.update(
                category_id = request['category_id'],
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
            tz : str, optional
                Timezone info as string.
                (default is app.config['TZ_INFO])

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
                tz = request['tz']
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
                language = request['language']
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
                language = request['language']
            )

            return response

        #endregion

        #region 'orders'
        elif ressource == "orders/get":
            pass

        #endregion


    except Exception as e: 
        
        # get code & msg
        
        return {'success':False, 'error':"", 'data':{}}

    return

#endregion