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

#region 'app construction' ---------------------
# grab cwd
cwd = Path().cwd() / "miniMoi"

# create db directory
(cwd/"db").mkdir(exist_ok=True)

# init python app
app = Flask(
    __name__,
    template_folder = str(cwd/"templates"),
    static_url_path = str(cwd/"static"),
    static_folder = "static"
    )

# grab the settings json
with open(cwd/"settings/settings.json", "r") as file:
    settings = json.loads(file.read())

#region 'app config'
app.config['VERSION'] = version.__version__
app.config['DEFAULT_LANGUAGE'] = settings['default_language']
app.config['ACTION_LOGGING'] = settings['action_logging'] == "True"
app.config['CWD'] = cwd
app.config['HOME'] = Path().home()
app.config['BLUEPRINT_PATH'] = Path().home() /"mini-moi/blueprints"

app.config['TZ_INFO'] = get_localzone_name()
print("TIMEZONE: ", get_localzone_name())

# add available languages
from miniMoi.language import language_files
app.config['AVAILABLE_LANGUAGES'] = [lang for lang in language_files.keys()]

#endregion

#region 'db init'
# get os
osName = sys.platform

print("OS: ", osName)

if osName == "win32": dbPath = "sqlite:///" + str(cwd/"db/app.db")
elif osName == "darwin": dbPath = "sqlite:////" + str(cwd/"db/app.db")
elif osName == "linux": dbPath = "sqlite:///" + str(cwd/"db/app.db")
else: raise Exception("Operating system not detectable: " + str(osName))

print("DB PATH: ", dbPath)

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
from .logic.db.init_database import run_creation
run_creation(engine, base)

#endregion

# import routes
from miniMoi import routes

#endregion

#test import! TBD:DELETE
from miniMoi.logic.db.generate_testdata import generate as generate_test
