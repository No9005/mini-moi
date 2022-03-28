"""
Handles the demo db generation process

"""

# import
from miniMoi import app, engine, base, Session
from miniMoi.logic.db import generate_testdata, init_database
from miniMoi.logic.functions import system

#region 'functions'
def run():
    """Runs the demo creation process """

    # delete current db
    system.delete_db()

    # create new db
    init_database.run_creation(engine, base)

    # create defaults
    init_database.create_defaults(Session)

    # run the dummy data builder
    generate_testdata.generate()


    return {
        'success':True,
        'error':"",
        'data':{}
    }
    

#endregion
