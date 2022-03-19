"""
Contains the handler logic for the api 

"""

# imports
from miniMoi.logic.functions import customer


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
            pass

        elif ressource == "products/add":
            pass

        elif ressource == "products/delete":
            pass

        elif ressource == "products/update":
            pass

        #endregion

        #region 'category'
        elif ressource == "category/get":
            pass

        elif ressource == "category/add":
            pass

        elif ressource == "category/delete":
            pass

        elif ressource == "category/update":
            pass

        #endregion
        
        #region 'abo'
        elif ressource == "abo/get":
            pass

        elif ressource == "abo/add":
            pass

        elif ressource == "abo/delete":
            pass

        elif ressource == "abo/update":
            pass

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