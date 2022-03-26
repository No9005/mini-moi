"""
Collection of functions to handle bulk imports

"""

# import
import pandas as pd

from miniMoi import app, Session
from miniMoi.language import language_files
from miniMoi.logic.functions.products import add as products_add
from miniMoi.logic.functions.categories import add as categories_add
from miniMoi.logic.functions.customer import add as customer_add
from miniMoi.logic.functions.abo import add as abo_add
import miniMoi.models.Models as models

#region 'public functions'
def create_blueprint(blueprint:str) -> dict:
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
        statement = session.query(models.Customers)
    
    elif blueprint == "category": 
        col_names = translation['column_mapping']['categories']
        statement = session.query(models.Category)
    
    elif blueprint == "subcategory": 
        col_names = translation['column_mapping']['categories']
        statement = session.query(models.Subcategory)
    
    elif blueprint == "products": 
        col_names = translation['column_mapping']['products']
        statement = session.query(models.Products)
    
    elif blueprint == "abo": 
        col_names = translation['column_mapping']['abo']
        statement = session.query(models.Abo)

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
    fullPath = str(home/ (blueprint + "_blueprint.csv"))
    df.to_csv(fullPath, sep=";", index=False)


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

def update() ->dict:
    """Reads all blueprints and updates the tables
    
    This function reads all tables in the
    directory '~/mini-moi/blueprints'
    and updates the tables
    
    params:
    -------
    None

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

    # create variable with relevant blueprints
    relevantBlueprints = ["customers", "category", "subcategory", "products", "abo"]

    # get all *.csv files
    loaded = {}

    for path in home.glob("*.csv"):

        print(path)
        

        # check if one of the blueprint names is in the filename
        for name in relevantBlueprints:

            print(name+"_blueprint")
            print(str(path).split("/"))

            if name+"_blueprint.csv" in str(path).split("/"): 
                
                # load the dataframe
                loaded.update({name: {'file':pd.read_csv(str(path), sep=";"), 'path':path}})
                break

    # check if there is at least one file
    if not bool(loaded): return {
        'success':False,
        'error':errors['noBlueprintFound'],
        'data':{}
        }

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

            print(tmp)

            result = customer_add(tmp.to_dict('records'))

            print(result)

        elif file == "category" or file == "subcategory": 

            # rename the columns to the official names
            official = {value:key for key, value in translation['column_mapping']['categories'].items()}
            tmp.rename(columns = official, inplace=True)

            result = categories_add(tmp.to_dict('records'))
        
        elif file == "products": 

            # rename the columns to the official names
            official = {value:key for key, value in translation['column_mapping']['products'].items()}
            tmp.rename(columns = official, inplace=True)
            
            result = products_add(loaded[file]['file'].to_dict('records'))
        
        elif file == "abo": 

            # rename the columns to the official names
            official = {value:key for key, value in translation['column_mapping']['abo'].items()}
            tmp.rename(columns = official, inplace=True)
            
            result = abo_add(loaded[file]['file'].to_dict('records'))

        #endregion

        # was the process successfull?
        if result['success']:

            # push to success
            update_progress['success'].append(file)

            # unlink
            loaded[file]['path'].unlink()

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

