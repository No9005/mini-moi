"""
Initiate the database (if not already active)

"""

# imports

from miniMoi import engine, base
from sqlalchemy_utils import database_exists, create_database


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
