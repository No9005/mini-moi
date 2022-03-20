"""
Contains collection of tools

"""

# imports
import typing
import datetime
import json
import sys

import numpy as np

from miniMoi.models.Models import Log

#region 'functions'
def _convert_exception(e) -> tuple:
    """Converts the passed exception """

    return (str(type(e).__name__), str(e))

def _to_dict(orm_object, to_fetch:list) -> dict:
    """Transforms the orm_object into a dict """

    if orm_object is None: return {}

    payload = {col:orm_object.__dict__[col] for col in to_fetch}
    
    return payload

def _update_logs(session, ressource:str, action:str) -> None:
    """Adds the user action to the logs 
    
    NOTE:
    prints warnings if the commit was no success

    params:
    -------
    session : sqlAlchemy session object
        The sql session object to add elements to.
    ressource : str
        The function name/endpoint which was called.
    action : str
        Stringified parameters.

    returns:
    -------
    None

    """

    # create a new log
    newLog = Log(
        ressource = str(ressource),
        action = str(action)
    )

    # add to session
    session.add(newLog)

    #try to commit
    try: session.commit()
    except:

        session.rollback()
        
        print("NOT ABLE TO LOG: ", str(ressource), str(action))
        sys.stdout.flush()

    return

#endregion

#region 'classes'
class jEncoder(json.JSONEncoder):
    """Custom Encoder for json.dumps()
    
    'json' is not able to process special
    data types out of the box.
    These include (but not only)
        [1] np.ndarrays
        [2] pd.DataFrames
        [3] DateTimes
    This class extends the 'json' encoding
    to handle more special types.

    attributes:
    ----------
    None

    methods:
    --------
    default
        Modifies & updates the converter
        function.

    """

    def default(self, obj:typing.Any) -> typing.Any:
        """Converts dtypes to default python objects """

        if isinstance(obj, np.integer): return int(obj)
        elif isinstance(obj, np.floating): return float(obj)
        elif isinstance(obj, np.ndarray): return obj.tolist()
        elif isinstance(obj, datetime.datetime): return obj.strftime("%Y.%m.%d")
        elif isinstance(obj, datetime.date): return obj.strftime("%Y.%m.%d")

        return super(jEncoder, self).default(obj)


#endregion
