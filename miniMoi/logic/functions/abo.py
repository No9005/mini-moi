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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

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

    # is result none?
    if result is None: return{'success':True, 'error':"", 'data':{'result':[]}}

    #region 'fetch all products'
    products = pd.read_sql_query(
        session.query(Products).statement,
        session.bind
    )
    #endregion

    # turn result into list of dicts
    resultList = []
    for r in result.all():

        resultList.append({
                'id':r.id,
                'customer_id':r.customer_id,
                'update_date':time.to_string(time.utc_to_local(r.update_date, tz), "%Y.%m.%d %H:%M"),
                'cycle_type':r.cycle_type,
                'interval':r.interval,
                'next_delivery':time.to_string(time.utc_to_local(r.next_delivery, tz), "%Y.%m.%d"),
                'product_id':r.product,
                'product_name':products.loc[products['id'] == r.product, "name"].values.tolist()[0]
            })

    # turn into dict & return
    return {
        'success':True,
        'error':"",
        'data':{
            'result':resultList
        }
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

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

    # fetch all available products
    products = pd.read_sql_query(
        session.query(Products).statement,
        session.bind
    )

    # get unique ids
    availableProducts = products['id'].unique().tolist()

    # selected product available?
    if not data['product'] in availableProducts: 
        
        # close session
        session.close()

        return {
            'success':False,
            'error':errors['wrongProduct'],
            'data':{}
        }

    # fetch all available subcategories
    subcategories = pd.read_sql_query(
        session.query(Subcategory).statement,
        session.bind
    )

    # get unique ids
    availableSubcategory = subcategories['id'].unique().tolist()
    if not data['subcategory'] in availableSubcategory:

        # close session
        session.close()

        return {
            'success':False,
            'error':errors['wrongSubcategory'],
            'data':{}
        }

    # grab interval & cycle_type
    interval = data['interval']
    cycle_type = data['cycle_type']

    try:
        # calculate next delivery
        if data['next_delivery'] is None:

            # calculate next delivery based on today
            today = time.today()
            next_delivery = time.calculate_next_delivery(
                date = today,
                cycle_type = cycle_type,
                interval = interval,
                language = language
            )
            
        # set the custom next delivery date
        else: next_delivery = time.local_to_utc(
            time.parse_date_string(data['next_delivery']),
            tz
            )
    
    except Exception as e:
        code, msg = tools._convert_exception(e)
        
        session.close()

        return {
            'success':False,
            'error':errors['unableOperation'].format(
                operation = "update",
                element = "abo",
                c = "",
                e=str(code),
                m=str(msg)
            ),
            'data':{}
        }

    # update
    try:
        abo.update_date = time.utcnow()
        abo.cycle_type = cycle_type
        abo.interval = interval
        abo.next_delivery = next_delivery
        abo.product = data['product']
        abo.quantity = int(data['quantity'])
        abo.subcategory = int(data['subcategory'])

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
        'data':{}
    }

def add(customer_id:int, abos:list, language:str = app.config['DEFAULT_LANGUAGE'], tz = app.config['TZ_INFO']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the list is not empty
    if not bool(abos): return {'success':False, 'error':errors['noEntry'].format(
        element = "abo"
    ), 'data':{}}

    # create session
    session = Session()

    # check if customer is available
    customer = session.query(Customers).filter_by(id = customer_id).first()
    if customer is None: return {
        'success':False, 
        'error':errors['notFound'].format(element="customer"), 
        'data':{}
        }

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

    # create empty list to store new entries
    toAdd = []

    # create the new products
    for abo in abos:

        try:

            #region 'check if abo settings are valid'
            # selected product?
            if not abo['product'] in availableProducts: 
                
                # close session
                session.close()

                return {
                    'success':False,
                    'error':errors['wrongProduct'],
                    'data':{}
                }

            # selected subcategory?
            if not abo['subcategory'] in availableSubcategory:

                # close session
                session.close()

                return {
                    'success':False,
                    'error':errors['wrongSubcategory'],
                    'data':{}
        }

            # get today
            today = time.today()

            # get interval
            interval = abo['interval']

            # get cycle_type
            cycle_type = abo['cycle_type']


            # calculate next delivery (if next_delivery is None)
            if abo['next_delivery'] is None:
                next_delivery = time.calculate_next_delivery(
                    date = today,
                    cycle_type = cycle_type,
                    interval = interval,
                    language = language
                )

            # else set the custom next delivery date
            else: next_delivery = time.local_to_utc(
                time.parse_date_string(abo['next_delivery']),
                tz
                )
            
            #endregion

            toAdd.append(Abo(
                customer_id = customer_id,
                cycle_type = cycle_type,
                interval = interval,
                next_delivery = next_delivery,
                product = abo['product'],
                quantity = int(abo['quantity']),
                subcategory = int(abo['subcategory'])
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
        'data':{}
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

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
        'data':{}
    }

#endregion
