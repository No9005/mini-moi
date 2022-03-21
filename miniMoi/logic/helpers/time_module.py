"""
functions relevant to calculate times

"""

# import
import typing
import datetime
import pytz

from miniMoi.language import language_files

#region 'functions' -----------------
def today():
    """Gets today as utcnow() """

    return datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

def utcnow():
    """Returns utcnow """

    return datetime.datetime.utcnow()

def date_by_weekday(
        today:datetime.datetime, 
        target_weekday:int, 
        n_weeks:int
        ) -> datetime.datetime:
    """Calculates date based on weekday & week
    
    This function returns the future date
    based on the current date and the
    specified weekday in a certain amount
    of weeks.

    params:
    -------
    today : datetime.datetime
        Current date in utcnow().
    target_weekday : int
        The idx of the weekday.
            Example: if you want a Monday in
                     3 weeks from now you can
                     pass '0' for the target.
    n_weeks : int
        The amount of weeks in the future.
            Example: A date in 3 weeks needs
                     n_weeks = 3

    returns:
    --------
    datetime.datetime
        The new date.
    
    """

    # get weekday idx of today
    todayIdx = today.weekday()

    # get difference between the weekdays
    diff = target_weekday - todayIdx

    return today + datetime.timedelta(weeks=n_weeks, days=diff)

def date_by_interval(today:datetime.datetime, interval:int) -> datetime.datetime:
    """Calculates date based on time interval

    Takes today and returns the date after
    appling the interval.

    params:
    -------
    today : datetime.datetime
        Current date in utcnow()
    interval : int
        Days to add.
    
    returns:
    --------
    datetime.datetime
        The new date.

    """

    return today + datetime.timedelta(days=interval)

def calculate_next_delivery(date:datetime.datetime, cycle_type:str, interval:int, language:str="EN") -> typing.Union[datetime.datetime, None]:
    """Calculates the next delivery date
    
    Calculates the next delivery date for the db
    based on the passed date and the criteria 
    provided by 'cycle_type' and 'interval'.

    EXCEPTIONS:
        [1] AssertionError
            If parameters where not correct.
    
    params:
    -------
    date : datetime.datetime
        The start date for the calculations.
    cycle_type : str
        The type of cycle to apply.
            Options: { None, 'day', 'interval' }
                None: The process quits and returns
                      None
    interval : int
        A number indicating either the amount of
        days to let pass or the weekday as idx.
            Note: The weekdays are 0-6 starting
                  at Monday = 0
    language : str
        The language iso code. Indicates the language
        to use for errors.
        (default is "EN")

    returns:
    --------
    datetime.datetime | None
        The next delivery date

    """

    # get language files
    try: errors = language_files[language]['error_codes']
    except: errors = language_files['EN']['error_codes']

    # cycle time none?
    if cycle_type is None: return None
    
    # cycle time day?
    elif cycle_type == "day":
        
        # interval none?
        if interval is None: raise AssertionError(errors['cycleMismatch'])

        # interval outside of 0-6?
        elif interval < 0 or interval > 6: raise AssertionError(
            errors['notAllowed'].format(
                    var="interval for day",
                    available = "{ " + errors['weekdays'] + " }"
                )
        )
            
        # generate the date by weekday
        next_delivery = date_by_weekday(
            today = date,
            target_weekday = interval,
            n_weeks = 1
        )

    elif cycle_type == "interval":
        
        # interval none?
        if interval is None: raise AssertionError(errors['cycleMismatch'])

        # generate the next delivery date
        next_delivery = date_by_interval(
            today = date,
            interval = interval
        )

    # non valid type
    else: raise AssertionError(
        errors['notAllowed'].format(
                var="cycle_type",
                available = str(set([None, 'day', 'interval']))
            )
        )

    # did all work?
    return next_delivery

def parse_date_string(string:str) -> datetime.datetime:
    """Parses a string into a datetime object
    
    params:
    -------
    string : str
        The string to parse.
        Format: "%Y-%m-%d"
        
    returns:
    --------
    datetime.datetime
        Datetime object

    """

    return datetime.datetime.strptime(string, "%Y-%m-%d")

def to_string(date:datetime.datetime, str_format:str = "%Y.%m.%d") -> str:
    """Converst datetime to string

    Applies the format and returns the string.

    params:
    -------
    date : datetime.datetime
        Datetime object
    str_format : str
        The string format to use.
        (default is "%Y.%m.%d)

    returns:
    -------
    str
    
    """

    return date.strftime(str_format)

def utc_to_local(date:datetime.datetime, tz:str = "Europe/Paris") -> datetime.datetime:
    """Convert utcnow to local time

    params:
    -------
    date : datetime.datetime
        Datetime object in utc.
    tz : str
        Timezone as string.
        (default is "Europe/Paris")

    returns:
    --------
    datetime.datetime
        In local time
    
    """

    # get timezone info
    tzInfo = pytz.timezone(tz)

    return pytz.utc.localize(date).astimezone(tzInfo)

def local_to_utc(date:datetime.datetime, tz:str = "Europe/Paris") -> datetime.datetime:
    """Converst a local time to utc 
    
    REFERENCE:
       [1] https://stackoverflow.com/questions/79797/how-to-convert-local-time-string-to-utc

    params:
    -------
    date : datetime.datetime
        The datetime object in local time.
    tz : str, optional
        The timezone from the current time
        object.
        (default is "Europe/Paris")
    
    returns:
    --------
    datetime.datetime
        Time converted into utc

    """

    # create local timezone
    local = pytz.timezone(tz)
    
    # localize
    localized = local.localize(date, is_dst=None)

    return localized.astimezone(pytz.utc)

#endregion
