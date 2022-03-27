"""
Contains functions in regards to the reporting

"""

# import
import datetime

import pandas as pd

from miniMoi import app, Session
import miniMoi.models.Models as models
from miniMoi.language import language_files
import miniMoi.logic.helpers.time_module as time

#region 'private functions' ---------------

#endregion


#region 'public functions' ----------------
def get_report():
    """Fetches the Orders & builds reports

    The information from the table 'Orders'
    gets fetched (time interval : this year).
    Additionally the info for product and 
    category are queried.
    With those three informations, we create
    the reporting values.
    
    params:
    -------
    None
    
    returns:
    --------
    dict
        success, error & data{
            }
    
    """

    # get language
    try: translation = language_files[app.config['DEFAULT_LANGUAGE']]
    except: translation = language_files["EN"]

    # get language errorcodes
    errors = translation['error_codes']

    #region 'get dates'
    # what was the date of the first of this year?
    """
    CAUTION:
    The orders are always saved at the previous day. So the first day of the
    current year is the 31.12. of last year
    
    """

    today = time.today()
    currentYear = time.today().year
    startOfYear = time.parse_date_string(str(currentYear-1) + "-12-31")
    endOfYear = time.parse_date_string(str(currentYear) + "-12-30")

    #endregion

    # create session
    session = Session()

    # get data for the current year
    year = session.query(models.Orders).filter(models.Orders.date >= startOfYear).filter(models.Orders.date <= endOfYear)
    year = pd.read_sql_query(year.statement, session.bind)

    #region 'prepare date'
    # add one day to date (cause it gets booked in the previous day)
    year.loc[:, 'date'] = year.loc[:, 'date'] + datetime.timedelta(days=1)

    # get month, day & weekday
    year['month'] = year['date'].map(lambda x: x.month)
    year['day'] = year['date'].map(lambda x: x.day)
    year['weekday'] = year['date'].map(lambda x: x.weekday())

    # replace weekday int with the name
    year['weekday_name'] = year['weekday'].replace(translation['weekday_mapping'])

    # replace the month with its name
    year['month_name'] = year['month'].replace(translation['month_mapping'])

    #endregion

    #region 'calculations'
    calculations = {
        'current_week':{
            'start':time.date_by_weekday(today, 6, -1),
            'end':today.replace(hour=23, minute=59, second=59),
            'time_grouper':"weekday_name",
            'data':{}
        },
        'last_week':{
            'start':time.date_by_weekday(today, 6, -2),
            'end':time.date_by_weekday(today, 6, -1).replace(hour=23, minute=59, second=59),
            'time_grouper':"weekday_name",
            'data':{}
        },
        'month':{
            'start':today.replace(day=1),
            'end':today.replace(hour=23, minute=59, second=59),
            'time_grouper':"day",
            'data':{}
        },
        'year':{
            'start':today.replace(day=1, month=1),
            'end':today.replace(hour=23, minute=59, second=59),
            'time_grouper':"month_name",
            'data':{}
        }
    }

    for name in calculations:

        # get the time grouper
        timeGrouper = calculations[name]['time_grouper']

        # build filter for the timeinterval
        condition1 = year['date'] >= calculations[name]['start']
        condition2 = year['date'] <= calculations[name]['end']

        # filter the dataframe
        tmp = year[condition1 & condition2]

        # product selling overview
        calc = tmp.groupby('product_name')['quantity'].sum()
        calculations[name]['data'].update({
            'selling_overview': {
                'index':calc.index.tolist(),
                'values':calc.tolist()
            }
        })

        # get revenue source
        calc = tmp.groupby('category')['total'].sum()
        calculations[name]['data'].update({
            'revenue_sources': {
                'index':calc.index.tolist(),
                'values':calc.tolist()
            }
        })

        # get earnings
        calc = tmp.groupby(timeGrouper)['total'].sum()
        calculations[name]['data'].update({
            'earnings': {
                'index':calc.index.tolist(),
                'values':calc.tolist()
            }
        })

    #endregion

    
    # did all work?
    return {
        'success':True,
        'error':"",
        'data':calculations
    }




#endregion