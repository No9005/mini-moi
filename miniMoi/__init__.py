"""
Flask app to assist during administration of
delivery apps.

"""

# imports
import os
import sys
import json
from pathlib import Path
from tzlocal import get_localzone_name

from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from . import version

import miniMoi.setup.setup_process as setup

#region 'app construction' ---------------------
# grab cwd & home
cwd = Path().cwd() / "miniMoi"
home = Path().home()

print("HOME:: ", home)

# first startup?
setupFlag = False
if not (home / "mini-moi/system/done.txt").is_file(): 

    # set flag
    setupFlag = True
    
    print("START:: running app setup")
    setup.run()

    print("FINISHED:: app setup done")

# init python app
app = Flask(__name__)

# grab the settings json
with open(home / "mini-moi/system/settings/settings.json", "r") as file:
    settings = json.loads(file.read())

#region 'app config'
#region 'paths'
app.config['HOME'] = home
app.config['MINI_MOI_HOME'] = home / "mini-moi"
app.config['BLUEPRINT_PATH'] = home /"mini-moi/blueprints"
app.config['SETTINGS_FILE_PATH'] = home / "mini-moi/system/settings/settings.json"
app.config['DB_FILE_PATH'] = home / "mini-moi/system/db/app.db"
app.config['CWD'] = cwd

#endregion

#region 'core & settings file'
app.config['VERSION'] = version.__version__
app.config['DEFAULT_LANGUAGE'] = settings['default_language']
app.config['FILE_TYPE'] = "csv" # -> "xlsx" or "csv"
app.config['ACTION_LOGGING'] = settings['action_logging'] == "True"
app.config['TZ_INFO'] = get_localzone_name()
print("TIMEZONE:: ", get_localzone_name())

#endregion


# add available languages
from miniMoi.language import language_files
app.config['AVAILABLE_LANGUAGES'] = [lang for lang in language_files.keys()]

#endregion

#region 'db init'
# get os
osName = sys.platform

print("OS:: ", osName)

if osName == "win32": dbPath = "sqlite:///" + str(app.config['DB_FILE_PATH'])
elif osName == "darwin": dbPath = "sqlite:////" + str(app.config['DB_FILE_PATH'])
elif osName == "linux": dbPath = "sqlite:///" + str(app.config['DB_FILE_PATH'])
else: raise Exception("Operating system not detectable: " + str(osName))

print("DB PATH:: ", dbPath)

# create engine
engine = create_engine(
    dbPath,
    echo = False,
    future = False
)

# create session maker
sessionFactory = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

# build session
Session = scoped_session(sessionFactory)

# create base
base = declarative_base()

# check if database is available
if setupFlag or app.config['DB_FILE_PATH'].is_file() == False:

    from .logic.db.init_database import run_creation, create_defaults
    
    print("START:: created db")
    
    run_creation(engine, base)

    print("FINISHED:: db created")

    if not create_defaults(Session): raise Exception("ERROR:: Not able to create db defaults!")
    else: print("FINISHED:: created db defaults")

    # write done file
    setup.set_done()

#endregion

# import routes
from miniMoi import routes

#endregion

