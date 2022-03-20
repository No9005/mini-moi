"""
Contains the functions to add/delete & update
categories

"""

# imports
import typing

from miniMoi import Session, app
from miniMoi.models.Models import Category
from miniMoi.language import language_files
from miniMoi.logic.helpers import tools


#region 'functions'
def get(amount:typing.Union[int, None] = None, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # create session
    session = Session()

    # query all
    result = session.query(Category)

    # limit?
    if amount is not None: result.limit(amount)

    # turn into dict & return
    return {
        'success':True,
        'error':"",
        'data':{
            'result':[u.__dict__ for u in result.all()]
        }
    }

def update(category_id:int, name:str, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the name is a string
    if not isinstance(name, str): return {'success':False, 'error':errors['wrongType'].format(
        var = "name",
        dtype= "str"
    ), 'data':{}}

    # create a session
    session = Session()

    # try to find the category
    category = session.query(Category).filter_by(id = category_id).first()
    if category is None:

        # close session & return error
        session.close()

        return {'success':False, 'error':errors['notFound'].format(element="category"), 'data':{}}

    # try to update
    try: category.name = name  
    except Exception as e:

        code, msg = tools._convert_exception(e)

        # close session
        session.close()

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "update",
                element = "category",
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

def add(categories:list, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # check if the list is not empty
    if not bool(categories): return {'success':False, 'error':errors['noEntry'].format(
        element = "category"
    ), 'data':{}}

    # create session
    session = Session()

    # create empty list to store new entries
    toAdd = []

    # create the new products
    for name in categories:

        try:

            toAdd.append(Category(
                name = name
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
                    element = "category",
                    c=str(name),
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

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

def delete(category_id:int, language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # create session
    session = Session()

    # get the user
    category = session.query(Category).filter_by(id = category_id).first()
    if category is None: return {
        'success':False, 
        'error':errors['notFound'].format(element="category"), 
        'data':{}
        }
    
    try:
        # delete it
        session.delete(category)

        # commit
        session.commit()
    
    except Exception as e:
        code, msg = tools._convert_exception(e)

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "delete",
                element = "category",
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
