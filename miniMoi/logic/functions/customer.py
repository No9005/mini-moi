"""
Collection of functions to handle processes
related to the customer.

"""

# imports
import datetime
import typing
import copy

from miniMoi import Session, app
from miniMoi.models.Models import Customers
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
    tz : str, optional
        The timezone info.
        (default is app.config['TZ_INFO'])

    returns:
    --------
    dict
        success, error, data {
            'result':[
                {
                    'id':int,
                    'date':datetime,
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
                },
                ...
            ]
        }

    """

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the filter is one of the allowed keywords
    allowedFilter = [None, "customer", "town"]
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
    if filter_type is None and what is None: 
        
        result = session.query(Customers)
    
    # filter is None -> what should be the start of the users
    elif filter_type is None:

        result = session.query(Customers).filter(Customers.id >= int(what))

    # filter by customer surname?
    elif filter_type == "customer" and what is not None: 
        
        result = session.query(Customers).filter_by(surname = what)

    # filter by town
    elif filter_type == "town":

        result = session.query(Customers).filter_by(town = what)

    # else return error
    else: return {'success':False, 'error':errors['unknownFilter'], 'data':{}}

    #endregion

    # limit the amount?
    if amount is not None: result = result.limit(amount)

    # result is None?
    if result is None: return{'success':True, 'error':"", 'data':{'result':[]}}

    # turn into list
    fetched = []
    for row in result.all():

        tmp = {}

        for col in row.__table__.columns:

            # convert timestamp
            if col.name == "date": tmp[col.name] = time.to_string(
                time.utc_to_local(getattr(row, col.name), tz),
                "%Y.%m.%d %H:%M"
                )
            
            elif col.name == "birthdate": tmp[col.name] = time.to_string(
                time.utc_to_local(getattr(row, col.name), tz),
                "%Y.%m.%d"
                )
            
            else: tmp[col.name] = getattr(row, col.name)

        fetched.append(copy.deepcopy(tmp))

    # turn into dict & return
    return {
        'success':True,
        'error':"",
        'data':{
            'result':fetched
        }
    }

def update(customer_id:int, data:dict, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the list is not empty
    if not bool(data): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # create a session
    session = Session()

    # try to find the customer
    customer = session.query(Customers).filter_by(id = customer_id).first()
    if customer is None:

        # close session & return error
        session.close()

        return {'success':False, 'error':errors['notFound'].format(element="customer"), 'data':{}}

    try:

        # check if the format of the birthdate is correct
        birthdate = datetime.datetime.strptime(data['birthdate'], "%Y.%m.%d")

        # try to update him
        customer.name = data['name']
        customer.surname = data['surname']
        customer.street = data['street']
        customer.nr = data['nr']
        customer.postal = data['postal']
        customer.town = data['town']
        customer.phone = data['phone']
        customer.mobile = data['mobile']
        customer.birthdate = birthdate
    
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
                    element = "customer",
                    c = "",
                    e=str(code),
                    m=str(msg)
                ),
                'data':{}
                }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.customer.update', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

def add(customers:list, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the list is not empty
    if not bool(customers): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # create a session
    session = Session()

    # empty list to add the class objects
    toAdd = []

    # create a new customer object for each in the list
    for customer in customers:

        try:

            # check if the datetime is convertable
            birthdate = datetime.datetime.strptime(customer['birthdate'], "%Y.%m.%d")

            # try to create the new object
            toAdd.append(Customers(
                name = customer['name'],
                surname = customer['surname'],
                street = customer['street'],
                nr = customer['nr'],
                postal = customer['postal'],
                town = customer['town'],
                phone = customer['phone'],
                mobile = customer['mobile'],
                birthdate = birthdate,
                notes = customer['notes']
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
                    element = "customer",
                    c=str(customer['name']),
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
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.customer.add', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

def delete(customer_id:int, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # create session
    session = Session()

    # get the user
    customer = session.query(Customers).filter_by(id = customer_id).first()
    if customer is None: return {
        'success':False, 
        'error':errors['notFound'].format(element="customer"), 
        'data':{}
        }

    try:
        # delete it
        session.delete(customer)

        # commit
        session.commit()
    
    except Exception as e:
        code, msg = tools._convert_exception(e)

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "delete",
                element = "customer",
                e=str(code),
                m=str(msg)
            ), 
            'data':{}
            }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.customer.delete', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

#endregion