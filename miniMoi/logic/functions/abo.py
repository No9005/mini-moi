"""
Collection of functions to handle
the abo add, delete & update.

"""

# imports
from datetime import tzinfo
import typing

import pandas as pd

from miniMoi import Session, app
from miniMoi.models.Models import Abo, Customers, Products, Subcategory
from miniMoi.language import language_files
from miniMoi.logic.helpers import tools
import miniMoi.logic.helpers.time_module as time

#region 'functions'
def get(
        filter_type:typing.Union[str, None], 
        what:typing.Union[str, None],
        amount:typing.Union[int, None] = None,
        language:str = app.config['DEFAULT_LANGUAGE'],
        tz:str = app.config['TZ_INFO']
    ) -> dict:
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

    # get language
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # get language mapping for columns
    mappedCols = translation['column_mapping']['abo']

    # check if the filter is one of the allowed keywords
    allowedFilter = [None, "abo", "customer"]
    try: assert(filter_type in allowedFilter)
    except AssertionError as e:
        return {
            'success':False,
            'error':errors['wrongFilter'].format(
                f=str(set(allowedFilter))
            ),
            'data':{}
        }

    # create session
    session = Session()

    #region 'query'
    # is filter & what both none? -> return first x elements
    if filter_type is None: 
        
        result = session.query(Abo)

    # filter by customer surname?
    elif filter_type == "abo" and what is not None: 
        
        result = session.query(Abo).filter_by(id = what)

    # filter by town
    elif filter_type == "customer":

        result = session.query(Abo).filter_by(customer_id = int(what))

    # else return error
    else: return {'success':False, 'error':errors['unknownFilter'], 'data':{}}

    #endregion

    # limit the amount?
    if amount is not None: result = result.limit(amount)

    #region 'create dropdown options'
    # products
    products = session.query(Products)
    if products.first() is None: return {
        'success':False, 
        'error':errors['noElementInDB'].format(
            element = translation['table_mapping']['product']
        ),
        'data':{}
        }
    dropdown_products = {el.id:el.name for el in products.all()}

    # subcategory
    subcategories = session.query(Subcategory)
    if subcategories.first() is None: return {
        'success':False, 
        'error':errors['noElementInDB'].format(
            element = translation['table_mapping']['subcategory']
        ),
        'data':{}
        }
    dropdown_subcateogry = {el.id:el.name for el in subcategories.all()}

    #endregion

    #region 'create empty result return'
    intendedOrder = [
            'id', 'customer_id', 'update_date', 'cycle_type',
            'interval', 'next_delivery', 'product', 'subcategory',
            'quantity'
        ]

    emptyResult = {
        'data':[],
        'order':intendedOrder,
        'mapping':[mappedCols[col] for col in intendedOrder],
        'dropdown':{
            'cycle_type':translation['cycle_type_mapping'],
            'weekday_interval':translation['weekday_mapping'],
            'product':dropdown_products,
            'subcategory':dropdown_subcateogry
        }
    }

    #endregion

    # is result none?
    if result.first() is None: return{'success':True, 'error':"", 'data':emptyResult}

    # turn result into list of dicts
    fetched = []
    for row in result.all():

        # parse cycle type and interval
        cycle_type = "None"
        interval = "None"
        if row.cycle_type is not None: cycle_type = row.cycle_type
        if row.interval is not None: interval = row.interval 

        fetched.append(
            {
              'id':row.id,
              'customer_id':row.customer_id,
              'update_date':time.to_string(time.utc_to_local(row.update_date), "%Y.%m.%d %H:%M"),
              'cycle_type':cycle_type,
              'interval':interval,
              'next_delivery':time.to_string(time.utc_to_local(row.next_delivery), "%Y.%m.%d"),
              'product':row.product,
              'subcategory':row.subcategory,
              'quantity':row.quantity  
            }
        )

    if len(fetched) == 0: return{'success':True, 'error':"", 'data':emptyResult}    

    # update empty result
    emptyResult.update({'data':fetched})

    # turn into dict & return
    return {
        'success':True,
        'error':"",
        'data':emptyResult
    }

def update(abo_id:int, data:dict, language:str = app.config['DEFAULT_LANGUAGE'], tz = app.config['TZ_INFO']) -> dict:
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
                'quantity':int,
                'subcategory':int,
                'next_delivery':str(%Y.%m.%d) | None
            }
    language : str, optional
        the language iso code. Needed for the
        error msg.
        (default is app.config['DEFAULT_LANGUAGE])
    tz : str, optional
        The timezone info.
        (default is app.config['TZ_INFO'])

    returns:
    -------
    dict
        success, error & data
    
    """

    # get language
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # check if the list is not empty
    if not bool(data): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # create a session
    session = Session()

    # try to find the abo
    abo = session.query(Abo).filter_by(id = abo_id).first()
    if abo is None:

        # close session & return error
        session.close()

        return {'success':False, 'error':errors['notFound'].format(element="abo"), 'data':{}}

    #region 'fetch additional info'
    # fetch all available products
    products = pd.read_sql_query(
        session.query(Products).statement,
        session.bind
    )

    # get unique ids
    availableProducts = products['id'].unique().tolist()

    # fetch all available subcategories
    subcategories = pd.read_sql_query(
        session.query(Subcategory).statement,
        session.bind
    )

    # get unique ids
    availableSubcategory = subcategories['id'].unique().tolist()

    #endregion

    #region 'parse input'
    # check ints
    int_values = {}
    for val in ['customer_id', 'product', 'subcategory', 'quantity']:

        try: int_values.update({val:int(data[val])})
        except ValueError as e: return {
            'success':False, 
            'error':errors['wrongType'].format(
                var = translation['column_mapping']['abo'][val],
                dtype="int"
            ), 
            'data':{}
        }

    # parse cycle type
    cycle_type = data['cycle_type']
    if cycle_type == "None": cycle_type = None

    # parse interval
    interval = data['interval']

    if cycle_type is None: interval = None
    else:
        try: interval = int(interval)
        except ValueError as e: return {
            'success':False, 
            'error':errors['wrongType'].format(
                var = translation['column_mapping']['abo']['interval'],
                dtype="int"
            ), 
            'data':{}
        }

    # parse next_delivery
    next_delivery = data['next_delivery']

    # get 'auto.' in different languages
    auto = translation['html_text']['/management']['management_auto_text']
    if next_delivery in ['', 'None', None, auto]: next_delivery = None

    if next_delivery is not None:

        try: 
            # parse delivery into correct format
            next_delivery = "-".join(next_delivery.split("."))

            # parse to datetime
            next_delivery = time.local_to_utc(
                time.parse_date_string(next_delivery),
                tz
                )

        except: return {'success':False, 'error':errors['wrongFormat'].format(
            var=translation['column_mapping']['abo']['next_delivery'],
            format="Year.Month.Day"
        )}

    else:

        # calculate next delivery based on today
        today = time.today()
        next_delivery = time.calculate_next_delivery(
            date = today,
            cycle_type = cycle_type,
            interval = interval,
            language = language
        )

    #endregion

    # selected product available?
    if not int_values['product'] in availableProducts: 
        
        # close session
        session.close()

        return {
            'success':False,
            'error':errors['wrongProduct'],
            'data':{}
        }

    # selected subcategory available?
    if not int_values['subcategory'] in availableSubcategory:

        # close session
        session.close()

        return {
            'success':False,
            'error':errors['wrongSubcategory'],
            'data':{}
        }

    # update
    try:
        abo.update_date = time.utcnow()
        abo.cycle_type = cycle_type
        abo.interval = interval
        abo.next_delivery = next_delivery
        abo.product = int_values['product']
        abo.quantity = int_values['quantity']
        abo.subcategory = int_values['subcategory']

        # commit
        session.commit()

    except Exception as e:
        code, msg = tools._convert_exception(e)

        # close session
        session.close()

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "update",
                element = "abo",
                e=str(code),
                m=str(msg)
            ),
            'data':{}
            }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.abo.update', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['update_to_db'].format(
                element=translation['table_mapping']['abo']
            )
        }
    }

def add(abos:list, language:str = app.config['DEFAULT_LANGUAGE'], tz = app.config['TZ_INFO']) -> dict:
    """Adds abos to a customer

    This function adds one or
    multiple abos to a specific
    customer.

    params:
    -------
    abos : list
        A list containing every single new
        abo for the customer.
            Format: [
                {
                    'customer_id':int
                    'cycle_type':str,
                    'interval':int,
                    'product':int,
                    'quantity':int,
                    'subcategory':int,
                    'next_delivery':str(%Y.%m.%d) | None
                },
                ...
            ]
    language : str, optional
        The language iso. Needed for the error
        msg.
        (default is app.config['DEFAULT_LANGUAGE])
    tz : str, optional
        The timezone info.
        (default is app.config['TZ_INFO'])

    returns:
    --------
    dict
        success, error, data

    """

    # get language
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # get translation for the auto. generation in the frontend
    auto = translation['html_text']['/management']['management_auto_text']

    # check if the list is not empty
    if not bool(abos): return {'success':False, 'error':errors['noEntry'].format(
        element = "abo"
    ), 'data':{}}

    # create session
    session = Session()

    #region 'fetch additional info'
    # fetch all available products
    products = pd.read_sql_query(
        session.query(Products).statement,
        session.bind
    )

    # get unique ids
    availableProducts = products['id'].unique().tolist()

    # fetch all available subcategories
    subcategories = pd.read_sql_query(
        session.query(Subcategory).statement,
        session.bind
    )

    # get unique ids
    availableSubcategory = subcategories['id'].unique().tolist()

    #endregion

    # create empty list to store new entries
    toAdd = []

    # create the new products
    for abo in abos:

        # parse the int values
        int_values = {}
        for val in ['customer_id', 'product', 'subcategory', 'quantity']:

            try: int_values.update({val:int(abo[val])})
            except ValueError as e: return {
                'success':False, 
                'error':errors['wrongType'].format(
                    var = translation['column_mapping']['abo'][val],
                    dtype="int"
                ), 
                'data':{}
            }            

        try:

            # check if customer is available
            customer = session.query(Customers).filter_by(id = int_values['customer_id']).first()
            if customer is None: return {
                'success':False, 
                'error':errors['notFoundWithId'].format(
                    element="customer",
                    id = int_values['customer_id']
                    ), 
                'data':{}
                }


            #region 'check if abo settings are valid'
            # selected product?
            if not int_values['product'] in availableProducts: 
                
                # close session
                session.close()

                return {
                    'success':False,
                    'error':errors['wrongProduct'],
                    'data':{}
                }

            # selected subcategory?
            if not int_values['subcategory'] in availableSubcategory:

                # close session
                session.close()

                return {
                    'success':False,
                    'error':errors['wrongSubcategory'],
                    'data':{}
                    }

            # get today
            today = time.today()

            # parse cycle type
            cycle_type = abo['cycle_type']
            if cycle_type == "None": cycle_type = None

            # get interval
            interval = abo['interval']

            # parse interval
            if cycle_type is None: interval = None
            else: 
                
                try: interval = int(interval)
                except ValueError as e: return {
                    'success':False, 
                    'error':errors['wrongType'].format(
                        var = translation['column_mapping']['abo']['interval'],
                        dtype="int"
                    ), 
                    'data':{}
                }     

            #region 'parse next delivery'
            next_delivery = abo['next_delivery']
            if next_delivery in ['', 'None', None, auto]: next_delivery = None

            if next_delivery is not None:
                try: 
                    # parse delivery into correct format
                    next_delivery = "-".join(next_delivery.split("."))

                    # parse to datetime
                    next_delivery = time.local_to_utc(
                        time.parse_date_string(next_delivery),
                        tz
                        )

                except: return {'success':False, 'error':errors['wrongFormat'].format(
                    var=translation['column_mapping']['abo']['next_delivery'],
                    format="Year.Month.Day"
                )}

            # endregion

            # calculate next delivery (if next_delivery is None)
            else:
                next_delivery = time.calculate_next_delivery(
                    date = today,
                    cycle_type = cycle_type,
                    interval = interval,
                    language = language
                )

            #endregion

            toAdd.append(Abo(
                customer_id = int_values['customer_id'],
                cycle_type = cycle_type,
                interval = interval,
                next_delivery = next_delivery,
                product = int_values['product'],
                quantity = int_values['quantity'],
                subcategory = int_values['subcategory']
            ))

        except Exception as e:

            # get msg & code
            code, msg = tools._convert_exception(e)

            # close the session
            session.close()

            return {
                'success':False, 
                'error':errors['unableOperation'].format(
                    operation = "add",
                    element = "abo",
                    c=str(""),
                    e=str(code),
                    m=str(msg)
                    ), 
                'data':{}
                    }

    # append to session
    session.add_all(toAdd)

    # commit
    try: session.commit()
    except Exception as e:

        code, msg = tools._convert_exception(e)

        # close the session
        session.close()

        return {
            'success':False,
            'error':errors['noCommit'].format(
                e=str(code),
                m=str(msg)
            )
        }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.abo.add', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['added_to_db'].format(
                element=translation['table_mapping']['abo']
            )
        }
    }

def delete(abo_id:int, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # create session
    session = Session()

    # get the user
    abo = session.query(Abo).filter_by(id = abo_id).first()
    if abo is None: return {
        'success':False, 
        'error':errors['notFound'].format(element="abo"), 
        'data':{}
        }
    
    try:
        # delete it
        session.delete(abo)

        # commit
        session.commit()
    
    except Exception as e:
        code, msg = tools._convert_exception(e)

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "delete",
                element = "abo",
                e=str(code),
                m=str(msg)
            ), 
            'data':{}
            }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.abo.delete', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['deleted_from_db'].format(
                element=translation['table_mapping']['abo']
            )
        }
    }

#endregion
