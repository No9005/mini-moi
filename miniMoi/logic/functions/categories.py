"""
Contains the functions to add/delete & update
for the category and subcategory table.

The mapper for the category and subcategory
are basically the same, so we can add a
more general approach for both of them.

"""

# imports
import typing

from miniMoi import Session, app
from miniMoi.models.Models import Category, Subcategory
from miniMoi.language import language_files
from miniMoi.logic.helpers import tools

# mapper
mapper = {
    'category':Category,
    'subcategory':Subcategory
}

#region 'functions'
def get(
        category_type:str = "category", 
        amount:typing.Union[int, None] = None, 
        language:str = app.config['DEFAULT_LANGUAGE']
    ) -> dict:
    """Gets all product categories/subcategories

    Fetches all product categories/subcategories
    and return them.

    params:
    -------
    category_type : str, optional
        Indicates the table to query.
        (default is 'category')
            Options: {'category', 'subcategory'}
                'category': Queries the Category
                            table.
                'subcategory': Queries the Sub-
                               category table.
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
            ],
            'category_type':str
        }

    """

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # create session
    session = Session()

    # query all
    result = session.query(mapper[category_type])

    # limit?
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
            'result':fetched,
            'category_type':category_type
        }
    }

def update(
        category_id:int,
        name:str,
        category_type:str = "category", 
        language:str = app.config['DEFAULT_LANGUAGE']
    ) -> dict:
    """Updates a single (sub-) category

    params:
    -------
    category_id : int
        The customer unique id.
    name : str
        The new category name
    category_type : str, optional
        Indicates the table to query.
        (default is 'category')
            Options: {'category', 'subcategory'}
                'category': Queries the Category
                            table.
                'subcategory': Queries the Sub-
                               category table.
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
    category = session.query(mapper[category_type]).filter_by(id = category_id).first()
    if category is None:

        # close session & return error
        session.close()

        return {'success':False, 'error':errors['notFound'].format(element=category_type), 'data':{}}

    # try to update
    try: 
        category.name = name

        session.commit()
          
    except Exception as e:

        code, msg = tools._convert_exception(e)

        # close session
        session.close()

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "update",
                element = category_type,
                e=str(code),
                m=str(msg)
            ),
            'data':{}
            }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.categories.update', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

def add(categories:list, category_type:str = "category", language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
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
    category_type : str, optional
        Indicates the table to query.
        (default is 'category')
            Options: {'category', 'subcategory'}
                'category': Queries the Category
                            table.
                'subcategory': Queries the Sub-
                               category table.
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

            toAdd.append(mapper[category_type](
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
                    element = category_type,
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

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.categories.add', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

def delete(category_id:int, category_type:str = "category", language:str = app.config['DEFAULT_LANGUAGE']) -> dict:
    """Deletes a category

    params:
    -------
    category_id : int
        the category unique id.
    category_type : str, optional
        Indicates the table to query.
        (default is 'category')
            Options: {'category', 'subcategory'}
                'category': Queries the Category
                            table.
                'subcategory': Queries the Sub-
                               category table.
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
    category = session.query(mapper[category_type]).filter_by(id = category_id).first()
    if category is None: return {
        'success':False, 
        'error':errors['notFound'].format(element=category_type), 
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
                element = category_type,
                e=str(code),
                m=str(msg)
            ), 
            'data':{}
            }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.categories.delete', str(locals()))

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{}
    }

#endregion