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

#endregion
