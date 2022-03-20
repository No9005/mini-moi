"""
Contains all tests.

To run the tests, activate your .venv (if you have one) and use:
    $ python3 -m unittest tests.<test to do>
    
"""

# imports
from sqlalchemy import create_engine

# create in memory db for tests
testEngine = create_engine(
                "sqlite://",
                echo=False,
                future=False
            )
