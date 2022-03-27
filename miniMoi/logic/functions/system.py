"""
Contains a collection of system operations

"""

# import
import shutil
from pathlib import Path

from miniMoi import app
from miniMoi.language import language_files
import miniMoi.logic.helpers.time_module as time

#region 'public functions' -------------------------
def make_db_copy():
    """Copies the db to the mini-moi download folder """

    # get language files
    try: translation = language_files[app.config['DEFAULT_LANGUAGE']]
    except: translation = language_files['EN']

    # create home path
    home = Path().home()
    fullPath = home / "mini-moi/backups"

    # create a folder in the Downloads folder
    fullPath.mkdir(exist_ok=True)

    # create the today date in local time
    today = time.to_string(
        time.utc_to_local(time.today(), app.config['TZ_INFO']),
        str_format = "%Y-%m-%d"
        )

    # copy the mini-moi app to the database
    shutil.copyfile(str(app.config['CWD']/"db/app.db"), (fullPath/("app_backup_" + today + ".db")))

    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['db_backup_success'].format(
                directory = str(fullPath)
                )
        }
    }

def rollback_db_save(filename:str) -> dict:
    """Select file to exchange with current db
    
    This function uses the file name to search
    for the file in the mini-moi folders.
    
    params:
    -------
    filename : str
        The file name to search for in
        the 'mini-moi' folder.

    returns:
    -------
    dict
        success, error & data {}

    """

    # get language files
    try: translation = language_files[app.config['DEFAULT_LANGUAGE']]
    except: translation = language_files['EN']

    # create source path
    sourcePath = app.config['MINI_MOI_HOME'] / "backups" / filename

    # copy it to the cwd db
    shutil.copyfile(str(sourcePath), str(app.config['CWD']/"db/app.db"))

    return {
        'success':True,
        'error':"",
        'data':{
            'msg':translation['notification']['db_rollback_success'].format(file=str(sourcePath))
        }
    }

#endregion
