"""
Contains the functions to add/delete & update
products

"""

# imports
import typing
from numpy import var

import pandas as pd

from miniMoi import Session, app
from miniMoi.models.Models import Products, Category
from miniMoi.language import language_files
from miniMoi.logic.helpers import tools

#region 'functions'
def get(
        filter_type:typing.Union[str, None], 
        what:typing.Union[str, None],
        amount:typing.Union[int, None] = None,
        language:str = app.config['DEFAULT_LANGUAGE']
    ) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the filter is one of the allowed keywords
    allowedFilter = [None, "product", "category"]
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
        
        result = session.query(Products)

    # filter by product name?
    elif filter_type == "product" and what is not None: 
        
        result = session.query(Products).filter_by(name = what)

    # filter by town
    elif filter_type == "category":

        try: result = session.query(Products).filter_by(category = int(what))
        except ValueError as e:

            code, msg = tools._convert_exception(e)

            # close session
            session.close()

            return {
                'success':False, 
                'error':errors['wrongType'].format(
                    var = "what",
                    dtype = "int"
                ),
                'data':{}
                }


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

        fetched.append({col.name:getattr(row, col.name) for col in row.__table__.columns})

    # turn into dict & return
    return {
        'success':True,
        'error':"",
        'data':{
            'result':fetched
        }
    }
    
def update(product_id:int, data:dict, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the list is not empty
    if not bool(data): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # create a session
    session = Session()

    # try to find the customer
    product = session.query(Products).filter_by(id = product_id).first()
    if product is None:

        # close session & return error
        session.close()

        return {'success':False, 'error':errors['notFound'].format(element="product"), 'data':{}}

    # fetch all possible categories
    categories = pd.read_sql_query(
        session.query(Category).statement,
        session.bind
    )

    # get unique ids
    availableCategories = categories['id'].unique().tolist()

    # check if product has valid category
    if data['category'] not in availableCategories:

        # close session
        session.close()

        return {
            'success':False,
            'error':errors['wrongCategory'].format(
                prior = str(product.name),
                p = str(data['name']),
                c = str(data['category'])
            ),
            'data':{}
        }

    # try to update
    try:
        product.name = data['name']
        product.category = data['category']
        product.purchase_price = data['purchase_price']
        product.selling_price = data['selling_price']
        product.store = data['store']
        product.phone = data['phone']
        product.margin = round(
            (data['selling_price'] - data['purchase_price']) / data['purchase_price'],
            3
            )

        session.commit()

    except Exception as e:

        code, msg = tools._convert_exception(e)

        # close session
        session.close()

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "update",
                element = "product",
                e=str(code),
                m=str(msg)
            ),
            'data':{}
            }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.products.update', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

def add(products:list, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the list is not empty
    if not bool(products): return {'success':False, 'error':errors['noEntry'].format(
        element = "product"
    ), 'data':{}}

    # turn into pd.DataFrame
    df = pd.DataFrame(products)

    # calculate margin
    df['margin'] = ((df['selling_price'] - df['purchase_price']) / df['purchase_price']).round(3)

    # create session
    session = Session()

    # fetch all possible category numbers (with_entities for only one column)
    categories = pd.read_sql_query(
        session.query(Category).statement,
        session.bind
    )

    # get unique ids
    availableCategories = categories['id'].unique().tolist()

    # create empty list to store new entries
    toAdd = []

    # create the new products
    for i, product in df.iterrows():

        try:

            # check if selected category is available
            if not product['category'] in availableCategories: 
                
                # close session
                session.close()

                return {
                    'success':False,
                    'error':errors['wrongCategory'].format(
                        p = str(product['name']),
                        c = str(product['category'])
                    ),
                    'data':{}
                }

            toAdd.append(Products(
                name = product['name'],
                category = product['category'],
                purchase_price = product['purchase_price'],
                selling_price = product['selling_price'],
                margin = product['margin'],
                store = product['store'],
                phone = product['phone'] 
            ))

        except Exception as e:

            # get msg & code
            code, msg = tools._convert_exception(e)

            # close the session
            session.close()

            print(product)

            return {
                'success':False, 
                'error':errors['unableOperation'].format(
                    operation = "add",
                    element = "product",
                    c=str(product['name']),
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
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.products.add', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

def delete(product_id:int, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # create session
    session = Session()

    # get the user
    product = session.query(Products).filter_by(id = product_id).first()
    if product is None: return {
        'success':False, 
        'error':errors['notFound'].format(element="product"), 
        'data':{}
        }
    
    try:
        # delete it
        session.delete(product)

        # commit
        session.commit()
    
    except Exception as e:
        code, msg = tools._convert_exception(e)

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "delete",
                element = "product",
                e=str(code),
                m=str(msg)
            ), 
            'data':{}
            }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.products.delete', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

#endregion
