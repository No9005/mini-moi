"""
Contains collection of tools

"""

# imports
import typing
import datetime

#region 'functions'
def _convert_exception(e) -> tuple:
    """Converts the passed exception """

    return (str(type(e).__name__), str(e))

def _to_dict(orm_object, to_fetch:list) -> dict:
    """Transforms the orm_object into a dict """

    if orm_object is None: return {}

    payload = {col:orm_object.__dict__[col] for col in to_fetch}
    
    return payload

#endregion
