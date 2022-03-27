"""
Collection of functions to handle bulk imports

"""

# import
import posixpath
import pandas as pd

from miniMoi import app, Session
from miniMoi.language import language_files
from miniMoi.logic.functions.products import add as products_add
from miniMoi.logic.functions.categories import add as categories_add
from miniMoi.logic.functions.customer import add as customer_add
from miniMoi.logic.functions.abo import add as abo_add
import miniMoi.models.Models as models
from miniMoi.logic.helpers import tools

from pathlib import Path, PosixPath


#region 'private functions'
def _unlink(path:PosixPath) -> None:
    """Deletes the file at the given directory """

    path.unlink()

def _to_csv(df:pd.DataFrame, path:str) -> dict:
    """Turns df to csv 
    
    This function is only needed for
    unittets.

    NOTE:
    Saves the .csv always with sep=";"
    
    params:
    -------
    df : pd.DataFrame
        The Dataframe to save to csv
    path : str
        The path to save to.

    returns:
    --------
    dict
        success, error & data

    """

    df.to_csv(path, sep=";", index=False)

    return {
        'success':True,
        'error':"",
        'data':{}
    }

def _to_excel(df:pd.DataFrame, path:str) -> dict:
    """Turns df to excel 
    
    This function is only needed for
    unittets.
    
    params:
    -------
    df : pd.DataFrame
        The Dataframe to save to csv
    path : str
        The path to save to.

    returns:
    --------
    dict
        success, error & data

    """

    df.to_excel(path, index=False)

    return {
        'success':True,
        'error':"",
        'data':{}
    }

def _load(home:PosixPath , errors:dict, file_type:str = "csv") -> dict:
    """Loads all blueprints from disk

    params:
    -------
    home : PosixPath
        The posixpath to load from.
    errors : dict
        The language file error dict.

    returns:
    -------
    dict
        success, error & data {
            'loaded':dict
        }
    
    """

    # create variable with relevant blueprints
    relevantBlueprints = ["customers", "category", "subcategory", "products", "abo"]

    # get all *.csv files
    loaded = {}

    # collect files
    if file_type == "xlsx": collected = home.glob("*.xlsx")
    elif file_type == "csv": collected = home.glob("*.csv")
    else: return {'success':False, 'error':errors['wrongFileType'].format(format = app.config['FILE_TYPE']), 'data':{}}
        
    
    for path in collected:
        
        # check if one of the blueprint names is in the filename
        for name in relevantBlueprints:

            #print(name+"_blueprint")
            #print(str(path).split("/"))

            if name + "_blueprint." + file_type in str(path).split("/")[-1]: 
                
                # load the dataframe
                if file_type == "xlsx": loaded.update({name: {'file':pd.read_excel(str(path)), 'path':path}})
                else: loaded.update({name: {'file':pd.read_csv(str(path), sep=";"), 'path':path}})
                break

    # check if there is at least one file
    if not bool(loaded): return {
        'success':False,
        'error':errors['noBlueprintFound'],
        'data':{}
        }

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{
            'loaded':loaded
        }
    }

#endregion

#region 'public functions'
def create_blueprint(blueprint:str, file_type:str="csv") -> dict:
    """Creates a blueprint for given table
    
    This function creates a blueprint for the
    given sql table.
    The blueprint is a empty excel with the correct
    columns in the specified app.config language.
    
    params:
    -------
    blueprint : str
        The name of the blueprint to create.
            Options: { 'customers', 'category'
                       'subcategory', 'products',
                       'abo' }
    file_type : str, optional
        The file type to save to.
        (default is 'csv')
            Options: {'xlsx', 'csv'}

    returns:
    --------
    dict
        success, error & datat {msg:str}
    
    """

    # get language files
    try: translation = language_files[app.config['DEFAULT_LANGUAGE']]
    except: translation = language_files['EN']

    # get errors
    errors = translation['error_codes']

    # create the directory
    home = app.config['BLUEPRINT_PATH']
    home.mkdir(exist_ok=True)

    # create session
    session = Session()

    #region 'query the tables'
    if blueprint == "customers": 
        col_names = translation['column_mapping']['customers']
        statement = session.query(models.Customers).limit(1)
    
    elif blueprint == "category": 
        col_names = translation['column_mapping']['categories']
        statement = session.query(models.Category).limit(1)
    
    elif blueprint == "subcategory": 
        col_names = translation['column_mapping']['categories']
        statement = session.query(models.Subcategory).limit(1)
    
    elif blueprint == "products": 
        col_names = translation['column_mapping']['products']
        statement = session.query(models.Products).limit(1)
    
    elif blueprint == "abo": 
        col_names = translation['column_mapping']['abo']
        statement = session.query(models.Abo).limit(1)

    else: return {
        'success':False, 
        'error':errors['blueprintUnknown'].format(blueprint=blueprint), 
        'data':{}
        }

    df = pd.read_sql_query(statement.statement, session.bind)

    #endregion

    # get col names
    cols = df.columns

    # translate the colum names
    translated_cols = [col_names[col] for col in cols]

    # create empty frame out of the columns
    df = pd.DataFrame(columns=translated_cols)

    # save to disk
    if file_type == "csv":
        fullPath = str(home/ (blueprint + "_blueprint.csv"))
        saved = _to_csv(df, str(fullPath))
    elif file_type == "xlsx":
        fullPath = str(home/ (blueprint + "_blueprint.xlsx"))
        saved = _to_excel(df, str(fullPath))
    else: return {'success':False, 'error':errors['wrongFileType'].format(format=app.config['FILE_TYPE']), 'data':{}}
    
    if not saved['success']: return saved

    # all done?
    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['blueprint_created'].format(
                blueprint=blueprint,
                path = fullPath
            )
        }
    }

def update(file_type:str="csv") ->dict:
    """Reads all blueprints and updates the tables
    
    This function reads all tables in the
    directory '~/mini-moi/blueprints'
    and updates the tables
    
    params:
    -------
    file_type : str, optional
        The file type to save to.
        (default is 'csv')
            Options: {'xlsx', 'csv'}

    returns:
    -------
    dict
        success, error & data {
            'msg':str
        }

    """

    # get language files
    try: translation = language_files[app.config['DEFAULT_LANGUAGE'] ]
    except: translation = language_files["EN"]

    # get errors
    errors = translation['error_codes']

    # create the directory path
    home = app.config['BLUEPRINT_PATH']

    # load files & convert it to dfs
    loaded = _load(home, errors, file_type)
    if not loaded['success']: return loaded
    loaded = loaded['data']['loaded']

    # create session to get additional info
    session = Session()

    # fallback for the productsmapping
    productsMapping = {}

    # run update
    update_progress = {
        'success':[],
        'failure':[]
    }
    for file in loaded:

        # grab the file
        tmp = loaded[file]['file']

        # is the file empty?
        if tmp.empty:
            
            # add to failure
            update_progress['failure'].append(file + " " + translation['notification']['is_empty'])

            # jump to the next
            continue

        #region 'parse data'
        # run process depending on name
        if file == "customers": 
        
            # rename the columns to the official names
            official = {value:key for key, value in translation['column_mapping']['customers'].items()}
            tmp.rename(columns = official, inplace=True)

            result = customer_add(tmp.to_dict('records'))

        elif file == "category" or file == "subcategory": 

            # rename the columns to the official names
            official = {value:key for key, value in translation['column_mapping']['categories'].items()}
            tmp.rename(columns = official, inplace=True)

            result = categories_add(tmp.to_dict('records'))
        
        elif file == "products": 

            # rename the columns to the official names
            official = {value:key for key, value in translation['column_mapping']['products'].items()}
            tmp.rename(columns = official, inplace=True)

            # create session & query the Categories from the table
            # turn also into mapper
            productsMapping = pd.read_sql_query(session.query(models.Category).statement, session.bind)
            productsMapping = {row['name']:row['id'] for i, row in productsMapping.iterrows()}

            # turn tmp category into strings & replace it with the mapping
            try: tmp.loc[:, 'category'] = tmp.loc[:, 'category'].astype(str).replace(productsMapping).astype(int)
            except Exception as e:
                code, msg = tools._convert_exception(e)

                update_progress['failure'].append(
                    file + ": " + errors['wrongProduct'] + ": {msg}".format(msg=msg)
                )

                continue

            result = products_add(loaded[file]['file'].to_dict('records'))
        
        elif file == "abo": 

            # rename the columns to the official names
            official = {value:key for key, value in translation['column_mapping']['abo'].items()}
            tmp.rename(columns = official, inplace=True)

            #region 'clean tmp'
            # query for products and subcategories
            if not bool(productsMapping):
                productsMapping = pd.read_sql_query(session.query(models.Products).statement, session.bind)
                productsMapping = {row['name']:row['id'] for i, row in productsMapping.iterrows()}

            subcatMapping = pd.read_sql_query(session.query(models.Subcategory).statement, session.bind)
            subcatMapping = {row['name']:row['id'] for i, row in subcatMapping.iterrows()}

            # parse weekday-mapping & cycle type mapping
            weekdayMapping = {value:key for key, value in translation['weekday_mapping'].items()}
            cycleMapping = {value:key for key, value in translation['cycle_type_mapping'].items()}

            # replace the names with the ids
            tmp.loc[:, 'product'] = tmp.loc[:, 'product'].astype(str).replace(productsMapping).astype(int)
            tmp.loc[:, 'subcategory'] = tmp.loc[:, 'subcategory'].astype(str).replace(subcatMapping).astype(int)
            tmp.loc[:, 'cycle_type'] = tmp.loc[:, 'cycle_type'].fillna("None").astype(str).replace(cycleMapping)

            # replace integers at positions of 'cycle_type == day' with the int
            tmp.loc[tmp['cycle_type'] == "day", 'interval'] = tmp.loc[tmp['cycle_type'] == "day", 'interval'].astype(str).replace(weekdayMapping)
            #tmp.loc[~tmp['cycle_type'].isna(), 'cycle_type'] = tmp.loc[~tmp['cycle_type'].isna(), 'cycle_type'].astype(int) 

            # fill missing values in 'next_delivery' to "None"
            tmp.loc[:, 'next_delivery'] = tmp.loc[:, 'next_delivery'].fillna("None")
            
            #endregion
            
            result = abo_add(loaded[file]['file'].to_dict('records'))

        #endregion

        # was the process successfull?
        if result['success']:

            # push to success
            update_progress['success'].append(file)

            # unlink
            _unlink(loaded[file]['path'])

        else: update_progress['failure'].append(file + ":" + result['error'])

        


    # send overview
    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['bulkFinished'].format(
                success= "{" + ", ".join(update_progress['success']) + "}",
                failures= "{" + ", ".join(update_progress['failure']) + "}",
            )
        }
    }



#endregion

