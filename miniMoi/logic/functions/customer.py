"""
Collection of functions to handle processes
related to the customer.

"""

# imports
import datetime
import typing

from miniMoi import Session, app
from miniMoi.models.Models import Customers
from miniMoi.language import language_files
from miniMoi.logic.helpers import tools

#region 'functions'
def get(
        filter_type:typing.Union[str, None], 
        what:typing.Union[str, None],
        amount:typing.Union[int, None] = None,
        language:str = app.config['DEFAULT_LANGUAGE']
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the filter is one of the allowed keywords
    allowedFilter = [None, "customer", "town"]
    try: assert(filter_type in allowedFilter)
    except AssertionError as e:
        return {
            'success':False,
            'error':errors['cust.get.0'].format(
                f=str(set(allowedFilter))
            ),
            'data':{}
        }

    # create session
    session = Session()

    # is filter & what both none? -> return first x elements
    if filter_type is None and what is None: 
        
        result = session.query(Customers)

        # special case: check if limit is valid, else reduce it!
        if amount is None: result.limit(25)
    
    # filter is None -> what should be the start of the users
    elif filter_type is None:

        result = session.query(Customers).filter(Customers.id >= int(what))

    # filter by customer surname?
    elif filter_type == "customer" and what is not None: 
        
        result = session.query(Customers).filter_by(surname = what).first()

    # filter by town
    elif filter_type == "town":

        result = session.query(Customers).filter_by(town = what)

    # else return error
    else: return {'success':False, 'error':errors['cust.get.1'], 'data':{}}

    # limit the amount?
    if amount is not None: result.limit(amount)

    # turn into dict & return
    return {
        'success':True,
        'error':"",
        'data':{
            'result':[u.__dict__ for u in result.all()]
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
    if not bool(data): return {'success':False, 'error':errors['cust.upt.0'], 'data':{}}

    # create a session
    session = Session()

    # try to find the customer
    customer = session.query(Customers).filter_by(id = customer_id).first()
    if customer is None:

        # close session & return error
        session.close()

        return {'success':False, 'error':errors['cust.notFound'], 'data':{}}

    try:

        # check if the format of the birthdate is correct
        datetime.datetime.strptime(data['birthdate'], "%Y.%m.%d")

        # try to update him
        customer.name = data['name']
        customer.surname = data['surname']
        customer.street = data['street']
        customer.nr = data['nr']
        customer.postal = data['postal']
        customer.town = data['town']
        customer.phone = data['phone']
        customer.mobile = data['mobile']
        customer.birthdate = data['birthdate']
    
        # commit
        session.commit()

    except Exception as e:

            code, msg = tools._convert_exception(e)

            # close session
            session.close()

            return {
                'success':False, 
                'error':errors['cust.upt.1'].format(
                    e=str(code),
                    m=str(msg)
                ),
                'data':{}
                }

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
    if not bool(customers): return {'success':False, 'error':errors['cust.add.0'], 'data':{}}

    # create a session
    session = Session()

     # empty list to add the class objects
    toAdd = []

    # create a new customer object for each in the list
    for customer in customers:

        try:

            # check if the datetime is convertable
            datetime.datetime.strptime(customer['birthdate'], "%Y.%m.%d")

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
                birthdate = customer['birthdate'],
                notes = customer['notes']
            ))

        except Exception as e:

            # get msg & code
            code, msg = tools._convert_exception(e)

            # close the session
            session.close()

            return {
                'success':False, 
                'error':errors['cust.add.1'].format(
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
            'error':errors['cust.add.2'].format(
                e=str(code),
                m=str(msg)
            )
        }

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
    if customer is None: return {'success':False, 'error':errors['cust.notFound'], 'data':{}}

    try:
        # delete it
        session.delete(customer)

        # commit
        session.commit()
    
    except Exception as e:
        code, msg = tools._convert_exception(e)

        return {
            'success':False, 
            'error':errors['cust.del.0'].format(
                e=str(code),
                m=str(msg)
            ), 
            'data':{}
            }

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

#endregion