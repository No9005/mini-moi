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

    # get language files
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # get language mapping for columns
    mappedCols = translation['column_mapping']['customers']

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

    #region 'create empty result return'
    intendedOrder = [
            'id', 'date', 'name', 'surname', 'street',
            'nr', 'postal', 'town',
            'phone', 'mobile', 'birthdate', 'approach',
            'notes'
        ]

    emptyResult = {
        'data':[],
        'order':intendedOrder,
        'mapping':[mappedCols[col] for col in intendedOrder],
        'table_name':translation['table_mapping']['customer']
    }

    #endregion

    # result is None?
    if result.first() is None: return{'success':True, 'error':"", 'data':emptyResult}

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

    if len(fetched) == 0: return{'success':True, 'error':"", 'data':emptyResult}

    # update empty result
    emptyResult.update({'data':fetched})

    # turn into dict & return
    return {
        'success':True,
        'error':"",
        'data':emptyResult
    }

def update(customer_id:int, data:dict, language:str = app.config['DEFAULT_LANGUAGE'], tz = app.config['TZ_INFO']) -> dict:
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
    tz : str, optional
        The timezone info
        (default is app.config['TZ_INFO'])

    returns:
    -------
    dict
        success, error & data {
            'msg':str
        }
    
    """

    # get language
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # check if the list is not empty
    if not bool(data): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # check id
    if customer_id == translation['html_text']['/management']['management_auto_text']: return {
        'success':False,
        'error':errors['pageRefresh'],
        'data':{}
    }

    # parse to int
    customerId = int(customer_id)

    # create a session
    session = Session()

    # try to find the customer
    customer = session.query(Customers).filter_by(id = customerId).first()
    if customer is None:

        # close session & return error
        session.close()

        return {
            'success':False, 
            'error':errors['notFound'].format(
                element=translation['table_mapping']['customer']
            ), 
            'data':{}
        }

    # parse birthdate
    birthdate = None
    if data['birthdate'] != "":

        birthdate = time.parse_UI_date(data['birthdate'], language, tz)
        if not birthdate['success']: return {
            'success':False,
            'error':birthdate['error'].format(
                var=translation['column_mapping']['customers']['birthdate'],
                format=translation['formats']['birthdate']
            ),
            'data':{}
        }

        birthdate = birthdate['data']['date']
    
    try:
        
        # parse to int
        for col in ['nr', 'approach']:
            try: int(data[col])
            except ValueError as e: return {'success':False, 'error':errors['wrongType'].format(
                var = translation['column_mapping']['customers'][col],
                dtype= translation['type_mapping']['int']
            ), 'data':{}}

        # try to update him
        customer.name = str(data['name'])
        customer.surname = str(data['surname'])
        customer.street = str(data['street'])
        customer.nr = int(data['nr'])
        customer.postal = str(data['postal'])
        customer.town = str(data['town'])
        customer.phone = str(data['phone'])
        customer.mobile = str(data['mobile'])
        customer.approach = int(data['approach'])
        customer.birthdate = birthdate
    
        # commit
        session.commit()

    except Exception as e:

        code, msg = tools._convert_exception(e)

        # check if sqlite3.IntegrityError -> sql msg
        if code == "IntegrityError": errorMsg = errors['notUnique'].format(
                table = translation['table_mapping']['customer'],
                nonUnique = msg.split("parameters")[-1].split("]")[0].lstrip()
            )

        # send normal msg
        else: errorMsg = errors['unableOperation'].format(
                operation = "update",
                element = translation['table_mapping']['customer'],
                e=str(code),
                m=str(msg)
            )

        # close the session
        session.close()

        return {
            'success':False,
            'error':errorMsg,
            'data':{}
        }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.customer.update', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['update_to_db'].format(
                element=translation['table_mapping']['customer']
            )
        }
    }

def add(customers:list, language:str = app.config['DEFAULT_LANGUAGE'], tz = app.config['TZ_INFO']) -> dict:
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
                    'birthdate':str("%Y-%m-%d),
                    'approach':int,
                    'notes':str
                },
                ...
            ]
    language : str, optional
        The language iso. Needed for the error
        msg.
        (default is app.config['DEFAULT_LANGUAGE])
    tz : str, optional
        The timezone info
        (default is app.config['TZ_INFO'])

    returns:
    --------
    dict
        success, error & data {
            'msg':str
        }

    """

    # get language
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # check if the list is not empty
    if not bool(customers): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # create a session
    session = Session()

    # empty list to add the class objects
    toAdd = []

    # create a new customer object for each in the list
    for customer in customers:

        # check if the stringified ints are int convertable
        for col in ['nr', 'approach']:
            try: int(customer[col])
            except ValueError as e: return {'success':False, 'error':errors['wrongType'].format(
                var = translation['column_mapping']['customers'][col],
                dtype=translation['type_mapping']['int']
            ), 'data':{}}

        # parse birthdate
        birthdate = None
        if customer['birthdate'] != "":
            
            birthdate = time.parse_UI_date(customer['birthdate'], language, tz)
            if not birthdate['success']: return {
                'success':False,
                'error':birthdate['error'].format(
                    var=translation['column_mapping']['customers']['birthdate'],
                    format=translation['formats']['birthdate']
                ),
                'data':{}
            }

            birthdate = birthdate['data']['date']

        try:

            # try to create the new object
            toAdd.append(Customers(
                name = str(customer['name']),
                surname = str(customer['surname']),
                street = str(customer['street']),
                nr = int(customer['nr']),
                postal = str(customer['postal']),
                town = str(customer['town']),
                phone = str(customer['phone']),
                mobile = str(customer['mobile']),
                birthdate = birthdate,
                approach = int(customer['approach']),
                notes = str(customer['notes'])
            ))

        except Exception as e:

            code, msg = tools._convert_exception(e)

            # check if sqlite3.IntegrityError -> sql msg
            if code == "IntegrityError": errorMsg = errors['notUnique'].format(
                    table = translation['table_mapping']['customer'],
                    nonUnique = msg.split("parameters")[-1].split("]")[0].lstrip()
                )

            # send normal msg
            else: errorMsg = errors['noCommit'].format(
                    e=str(code),
                    m=str(msg)
                )

            # close the session
            session.close()

            return {
                'success':False,
                'error':errorMsg,
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
        'data':{
            'msg':translation['notification']['added_to_db'].format(
                element=translation['table_mapping']['customers']
            )
        }
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

    # get language
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # check id
    if customer_id == translation['html_text']['/management']['management_auto_text']: return {
        'success':False,
        'error':errors['pageRefresh'],
        'data':{}
    }

    # parse to int
    customerId = int(customer_id)

    # create session
    session = Session()

    # get the user
    customer = session.query(Customers).filter_by(id = customerId).first()
    if customer is None: return {
        'success':False, 
        'error':errors['notFound'].format(
            element=translation['table_mapping']['customer']
            ), 
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
                operation = translation['operation_mapping']['delete'],
                element = translation['table_mapping']['customer'],
                c=translation['column_mapping']['customers']['id'] + " : " + str(customerId),
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
        'data':{
            'msg':translation['notification']['deleted_from_db'].format(
                element=translation['table_mapping']['customer']
            )
        }
    }

#endregion