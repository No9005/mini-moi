"""
Initiate the database (if not already active)

"""

# imports
from sqlalchemy_utils import database_exists, create_database

# import models, else create all will fail!
from miniMoi.models.Models import Customers, Orders, Abo, Category, Subcategory, Products, Log


def run_creation(engine, base) -> None:
    """Creates the database
    
    If not already existing, the database is
    created.
    Afterwards all missing tables are created.

    params:
    -------
    engine : sql alchemy engine
        The sql alchemy engine
    base : sqlalchemy base
        The sql alchemy base

    returns:
    --------
    None

    """

    # check if the database exists already
    if not database_exists(engine.url): create_database(engine.url)

    # try to create the tables
    # already created tables are not recreated again
    with engine.connect() as conn:
        base.metadata.create_all(engine)


def create_defaults(Session) -> bool:
    """Creates default db entries

    Some delete operations need onDelete values.
    This function creates a default value.
    Relevant for
        - abo.subcategory

    params:
    -------
    Session : sqlalchemy session maker
        The session maker to create a session

    returns:
    --------
    bool
        True if successfull, else false

    """

    # create session
    session = Session()

    try:

        # create empty adding list
        toAdd = []

        # create the default for subcategory
        toAdd.append(Subcategory(
            id = 0,
            name = "None"
        ))

        # add and commit
        session.add_all(toAdd)
        session.commit()

    except Exception as e:

        # terminate the db session!
        session.remove()

        return False

    return True