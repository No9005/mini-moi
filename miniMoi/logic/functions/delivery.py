"""
Collection of function which handle the delivery

"""

# import
import typing
import datetime
import zipfile
import io

import pandas as pd
import xlsxwriter as xlsx

from miniMoi import Session, app
from miniMoi.models.Models import Abo, Customers, Products, Category, Subcategory, Orders
from miniMoi.logic.helpers import tools
from miniMoi.language import language_files
import miniMoi.logic.helpers.time_module as time
import miniMoi.logic.helpers.excel as xlsx


#region 'helpers (private) functions' ----------------------------
def _create_mapping(data:dict, translation:dict) -> tuple:
    """Creates column ordering & mapper

    Needed for correct displaying of elements
    in forntend.

    params:
    ------
    data : dict
        The data as dict to check.
    translation : dict
        The excel translation dict.

    returns:
    --------
    tuple
        (ordering, mapper)
    
    """

    # get cols ordering
    cols = [col for col in data.keys()]

    # create empty mapper
    mapper = []

    # cycle through cols and try to get a translation
    for element in cols:
        if element in translation: mapper.append(translation[element])
        else: mapper.append(element)

    return (cols, mapper)

def _product_overview(granular:pd.DataFrame, to_dict:bool=False) -> typing.Union[pd.DataFrame, dict]:
    """Produces the product overview

    params:
    ------
    granular : pd.DataFrame
        The result from the 
        'granular()' function.
    to_dict : bool, optional
        If true, the df gets converted
        to a dict.
    
    returns:
    --------
    pd.DataFrame | dict

    """

    # create product overview
    overview_product = granular.groupby('category_name').apply(lambda x: pd.crosstab(
        index = x['product_name'],
        columns = x['subcategory_name'],
        values = x['quantity'],
        aggfunc="sum"
    ))

    # add total to overview
    overview_product['total'] = overview_product.sum(axis=1)
    
    # prepare for convert
    overview_product = overview_product.fillna(0).astype(int).reset_index()
    
    # all but 'category_name' column
    opCols = [col for col in overview_product.columns if col != "category_name"]

    if to_dict: return {
        t:overview_product.loc[overview_product['category_name'] == t, opCols].sort_values('product_name').to_dict("list") for t in overview_product['category_name'].unique().tolist()
    }

    return overview_product

def _category_overview(granular:pd.DataFrame, to_dict:bool=False) -> typing.Union[pd.DataFrame, dict]:
    """Produces the category overview

    params:
    ------
    granular : pd.DataFrame
        The result from the 
        'granular()' function.
    to_dict : bool, optional
        If true, the df gets converted
        to a dict.
    
    returns:
    --------
    pd.DataFrame | dict

    """

    # create category overview
    overview_category = granular.groupby('category_name').apply(
        lambda x: x[['quantity', 'cost']].sum()
        ).reset_index().fillna(0).sort_values('category_name')

    if to_dict: return overview_category.to_dict("list")
    
    return overview_category

def _prepare_granular(df:pd.DataFrame, reset_index:bool = True) -> pd.DataFrame:
    """Produces the granular grouping 
    
    params:
    ------
    df : pd.DataFrame
        The dataframe to group.
            Columns: { 'product_name',
                       'category_name',
                       'subcategory_name',
                       'quantity',
                       'cost'
                    }
    reset_index : bool, optional
        If true, the index gets reset.
        (default is True)
            
    returns:
    --------
    pd.DataFrame
        The grouped dataframe
    
    """

    granular =  df.groupby(
        ['product_name', 'category_name', 'subcategory_name']
        ).apply(lambda x: x[['quantity','cost']].sum())

    if reset_index: return granular.reset_index()

    return granular

#endregion


#region '(public) functions' -------------------------------------
def create(language = app.config['DEFAULT_LANGUAGE'], tz = app.config['TZ_INFO']) -> dict:
    """Creates next days delivery overview

    This function creates the overview for the
    next days delivery.

    params:
    -------
    language : str, optional
        language ISO code for the errors.
        (default is app.config['DEFAULT_LANGUAGE])
    tz : str, optional
        Timzone information.
        (default is app.config['TZ_INFO'])

    returns:
    --------
    dict
        success, error & data {
            'overview_category':{
                'category_name':[],
                'quantity':[],
                'cost':[]
                },
            'overview_product':{
                'category_name':{
                    'product_name':[],
                    'subcat_1:[],
                    'subcat_2:[],
                    'subcat_X:[],
                    ...
                },
                'category_name2':{
                    ...
                },
                ...
                
                },
            'total_earnigns':int,
            'total_spendings':int,
            'town_based':{
                'townName':{
                    'customer_approach':list[int], 
                    'customer_street':list[str], 
                    'customer_nr':list[int],
                    'customer_town':list[str],
                    'customer_name':list[str],
                    'customer_surname':list[str],
                    'customer_id':list[int],
                    'customer_phone':list[str],
                    'customer_mobile':list[str],
                    'quantity':list[int], 
                    'product_name':list[str],
                    'product_id':list[int],
                    'category_name':list[str],
                    'subcategory_name':list[str],
                    'product_selling_price':list[float],
                    'cost':list[float],
                    'total_cost':list[float],
                    'notes':list[str]
                    'id':list[int] # -> the abo_id
                    },
                'townName':{
                    ...
                    },
                ...
            }

        }
    
    """

    # get language files
    try: translation = language_files[language]
    except: translation = language_files[app.config['DEFAULT_LANGUAGE']]

    # get language errorcodes
    errors = translation['error_codes']

    # create session
    session = Session()

    #region 'query abos & prepare df' --------------------------
    # query all abos which are within the range
    # of utcnow +- 1 day
    today = time.today()
    tomorrow = today + datetime.timedelta(days=1)
    yesterday = today + datetime.timedelta(days=-1)

    # query abos
    abosQuery = session.query(Abo).filter(Abo.next_delivery <= tomorrow).filter(Abo.next_delivery >= yesterday)
    abos = pd.read_sql_query(
        abosQuery.statement,
        session.bind
    )

    #region 'prepare df'
    # check if df is empty
    if abos.empty: return {'success':False, 'error':errors['noDelivery'], 'data':{}}

    # copy utc
    abos.loc[:, 'next_delivery_utc'] = abos.loc[:, 'next_delivery']

    # convert utcnow to local time
    abos.loc[:, 'next_delivery'] = abos.loc[:, 'next_delivery'].map(lambda x: time.to_string(time.utc_to_local(x, tz)))

    # convert today & tomorrow to local time
    todayLocal = time.utc_to_local(today, tz)
    tomorrowLocal = time.utc_to_local(tomorrow, tz)

    # filter abos to be only for tomorrow
    abos = abos[abos['next_delivery'] == time.to_string(tomorrowLocal)]

    #endregion

    #endregion

    #region 'query additional info' ----------------------------
    # query customers
    customersQuery = session.query(Customers).filter(Customers.id.in_(
        abos['customer_id'].unique().tolist()
    ))
    customers = pd.read_sql_query(customersQuery.statement, session.bind)
    customers.columns = ["customer_" + col for col in customers.columns]

    # query products
    productsQuery = session.query(Products).filter(Products.id.in_(
        abos['product'].unique().tolist()
    ))
    products = pd.read_sql_query(productsQuery.statement, session.bind)
    products.columns = ["product_" + col for col in products.columns]

    # query categories
    categoriesQuery = session.query(Category).filter(Category.id.in_(
        products['product_category'].unique().tolist()
    ))
    categories = pd.read_sql_query(categoriesQuery.statement, session.bind)
    categories.columns = ["category_" + col for col in categories.columns]

    # query subcategories
    subcategoryQuery = session.query(Subcategory).filter(Subcategory.id.in_(
        abos['subcategory'].unique().tolist()
    ))
    subcategories = pd.read_sql_query(subcategoryQuery.statement, session.bind)
    subcategories.columns = ["subcategory_" +  col for col in subcategories.columns]

    #endregion

    #region 'merge together' -----------------------------------
    # abos + costumers
    df = pd.merge(abos, customers, how="left", left_on="customer_id", right_on="customer_id")

    # df + products
    df = pd.merge(df, products, how="left", left_on="product", right_on="product_id")

    # df + categories
    df = pd.merge(df, categories, how="left", left_on="product_category", right_on="category_id")

    # df + subcategories
    df = pd.merge(df, subcategories, how="left", left_on="subcategory", right_on="subcategory_id")
    
    #endregion

    #region 'create overview' ----------------------------------
    # calculate cost & total for each participant
    df['cost'] = df.loc[:, 'product_selling_price'] * df.loc[:, 'quantity']
    df['spendings'] = df.loc[:, 'product_purchase_price'] * df.loc[:, 'quantity']

    # group on granularest level
    granular = _prepare_granular(df)

    # create category overview
    overview_category = _category_overview(granular, to_dict=True)

    # create product overview
    overview_product = _product_overview(granular, to_dict = True)

    # get total earned price
    totalEarnings = df['cost'].sum()
    totalSpendings = df['spendings'].sum()

    # sort for town based userlist
    cost_per_customer = df.groupby('customer_id').apply(lambda x: x['cost'].sum()).reset_index()
    cost_per_customer.rename(columns={0:'total_cost'}, inplace=True)

    # merge together
    df = pd.merge(df, cost_per_customer, how="left", left_on="customer_id", right_on="customer_id")

    # select only relevant information
    relevantCols = [
        'customer_approach', 
        'customer_street', 
        'customer_nr',
        'customer_town',
        'customer_name',
        'customer_surname',
        'customer_id',
        'customer_phone',
        'customer_mobile',
        'quantity', 
        'product_name',
        'product_id',
        'product_selling_price',
        'subcategory_name',
        'category_name',
        'cost',
        'total_cost',
        'customer_notes',
        'id'
        ]
    df = df.loc[:, relevantCols].sort_values(['customer_town', 'customer_approach', 'product_name'])

    # turn into townbased dict
    townbased = {
            t:df[df['customer_town'] == t].to_dict("list") for t in df['customer_town'].unique().tolist()
        } 

    #endregion

    # get xlsx table name mapping
    xlsxNames = translation['xlsx']

    # create orders & mapping
    townbasedOrder, townbasedMapping = _create_mapping(townbased, xlsxNames)
    categoryOrder, categoryMapping = _create_mapping(overview_category, xlsxNames)

    productOverview = {}
    for p in overview_product.keys():

        # get mapping
        tmpOrder, tmpMapping = _create_mapping(overview_product[p], xlsxNames)

        productOverview.update({
            p:{
                'data':overview_product[p],
                'order':[c for c in tmpOrder],
                'mapping':[c for c in tmpMapping]
            }
        })

    # did all work?
    return {
        'success':True,
        'error':"",
        'data':{
            'overview_category':{
                'data':overview_category,
                'order':categoryOrder,
                'mapping':categoryMapping
                },
            'overview_product':productOverview,
            'total_earnings':totalEarnings,
            'total_spendings':totalSpendings,
            'town_based':{
                'data':townbased,
                'mapping':townbasedMapping,
                'order':townbasedOrder
                }
        }
    }

def book(data:dict, language = app.config['DEFAULT_LANGUAGE']) -> dict:
    """Books the manipulated data

    This function takes the data and adds 
    the provided info to the 'Orders' table.
    It also calculates the next delivery
    date.
    In the end it returns the printed excel.

    params:
    -------
    data : dict
        The town based data for each abo.
            Format: {
                    'customer_approach':list[int], 
                    'customer_street':list[str], 
                    'customer_nr':list[int],
                    'customer_town':list[str],
                    'customer_name':list[str],
                    'customer_surname':list[str],
                    'customer_id':list[int],
                    'customer_phone':list[str],
                    'customer_mobile':list[str],
                    'quantity':list[int], 
                    'product_name':list[str], 
                    'product_id':list[int],
                    'category_name':list[str],
                    'subcategory_name':list[str],
                    'product_selling_price':list[float],
                    'cost':list[float],
                    'total_cost':list[float],
                    'notes':list[str]
                    'id':list[int] # -> the abo_id
                    }
            }
    language : str, optional
        language ISO code for the errors.
        (default is app.config['DEFAULT_LANGUAGE])
 
    returns:
    -------
    dict
        success, error & data:{
            'zip':io.BytesIO,
            'date':str
        }

    """

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # data empty?
    if not bool(data): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # all relevant columns in the data?
    relCols = [
        'customer_approach',
        'customer_street', 
        'customer_nr',
        'customer_town',
        'customer_name',
        'customer_surname',
        'customer_id',
        'customer_phone',
        'customer_mobile',
        'quantity', 
        'product_name', 
        'product_id',
        'product_selling_price',
        'subcategory_name',
        'category_name',
        'cost',
        'total_cost',
        'customer_notes',
        'id'
        ]
    for col in relCols:

        if col not in data.keys(): return {
            'success':False, 
            'error':errors['missingData'].format(column=str(col)), 
            'data':{}
            }

    # turn into pd.dataFrame
    df = pd.DataFrame(data)

    # sort
    df = df.sort_values(['customer_town', 'customer_approach', 'product_name'])

    # create session
    session = Session()

    # fetch all abos to update
    abos = session.query(Abo).filter(Abo.id.in_(
        df['id'].unique().tolist()
    )).all()
    
    # add order & update next_delivery
    toAdd = []
    
    try:
        for abo in abos:

            # grab df row
            tmp = df[df['id'] == abo.id]

            # add order
            toAdd.append(Orders(
                customer_id = tmp['customer_id'].tolist()[0],
                product = tmp['product_id'].tolist()[0],
                name = tmp['product_name'].tolist()[0],
                quantity = tmp['quantity'].tolist()[0],
                price = tmp['product_selling_price'].tolist()[0],
                total = tmp['cost'].tolist()[0]
            ))

            # update abo next_delivery
            abo.next_delivery = time.calculate_next_delivery(
                date = abo.next_delivery,
                cycle_type = abo.cycle_type,
                interval = abo.interval,
                language = language
            )

    except Exception as e:

        code, msg = tools._convert_exception(e)

        # close session
        session.close()

        return {
            'success':False, 
            'error':errors['unableOperation'].format(
                operation = "book",
                element = "abo",
                c = "",
                e=str(code),
                m=str(msg)
            ),
            'data':{}
            }

    # add to add to the session
    session.add_all(toAdd)

    # create product overviews
    # group on granularest level
    granular = _prepare_granular(df)

    # create category overview
    overview_category = _category_overview(granular, to_dict=True)

    # create product overview
    overview_product = _product_overview(granular, to_dict = True)

    # build townbased
    townbased = {
            t:df[df['customer_town'] == t].to_dict("list") for t in df['customer_town'].unique().tolist()
        } 

    # create excel
    cover = xlsx.print_cover(
        category_overview = overview_category,
        product_overview = overview_product,
        path = None,
        tomorrow = True,
        language = language
    )

    orderDetails = xlsx.print_order_list(
        townbased,
        path = None,
        tomorrow = True,
        language = language
    )

    # zip the files
    archive = io.BytesIO()

    # get today
    useDate = time.to_string(
                time.utc_to_local(
                    time.utcnow() + datetime.timedelta(days=1),
                    tz = app.config['TZ_INFO']
                    ), 
                "%Y-%m-%d"
                )

    with zipfile.ZipFile(archive, "w") as zip_archive:

        # add the files
        with zip_archive.open("/cover_" + useDate + ".xlsx", "w") as file1:
            file1.write(cover.read())
        
        with zip_archive.open("/order_details_" + useDate + ".xlsx", "w") as file2:
            file2.write(orderDetails.read())

    archive.seek(0)


    if False: 
        """
        CAUTION:
        Write the archive to disk by using the writing mode
        'wb' for -> 'write binary'.

        """

        # write the buffer to the disk
        with open(str(app.config['CWD'].parent/"vorlagen/archive.zip"), "wb") as f:
            f.write(archive.getbuffer())

    # commit
    try: session.commit()
    except Exception as e:

        code, msg = tools._convert_exception(e)

        # close the session
        session.close()

        return {
            'success':False,
            'error':errors['noCommit'].format(
                e=str(code),
                m=str(msg)
            )
        }

    # add logs
    if app.config['ACTION_LOGGING']: tools._update_logs(session, 'miniMoi.logic.functions.delivery.book', "See oders around: {time}".format(time=time.to_string(time.utcnow(), "%Y-%m-%d %H:%M:%S")))

    return {
        'success':True,
        'error':"",
        'data':{
            'zip':archive,
            'date':useDate
        }
    }

def print_order_details(
        data:dict,
        language = app.config['DEFAULT_LANGUAGE']
    ) -> dict:
    """Create order details overview

    Creates the excel overview and returns it.

    params:
    -------
    data : dict
        The town based data for each abo.
            Format: {
                    'customer_approach':list[int], 
                    'customer_street':list[str], 
                    'customer_nr':list[int],
                    'customer_town':list[str],
                    'customer_name':list[str],
                    'customer_surname':list[str],
                    'customer_id':list[int],
                    'customer_phone':list[str],
                    'customer_mobile':list[str],
                    'quantity':list[int], 
                    'product_name':list[str], 
                    'product_id':list[int],
                    'category_name':list[str],
                    'subcategory_name':list[str],
                    'product_selling_price':list[float],
                    'cost':list[float],
                    'total_cost':list[float],
                    'notes':list[str]
                    'id':list[int] # -> the abo_id
                    }
            }
    language : str, optional
        language ISO code for the errors.
        (default is app.config['DEFAULT_LANGUAGE])
 
    returns:
    -------
    dict
        success, error & data:{
            'file':io.BytesIO,
            'date':str
            }

    """

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # data empty?
    if not bool(data): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # all relevant columns in the data?
    relCols = [
        'customer_approach',
        'customer_street', 
        'customer_nr',
        'customer_town',
        'customer_name',
        'customer_surname',
        'customer_id',
        'customer_phone',
        'customer_mobile',
        'quantity', 
        'product_name', 
        'product_id',
        'product_selling_price',
        'subcategory_name',
        'category_name',
        'cost',
        'total_cost',
        'customer_notes',
        'id'
        ]
    for col in relCols:

        if col not in data.keys(): return {
            'success':False, 
            'error':errors['missingData'].format(column=str(col)), 
            'data':{}
            }

    # turn into pd.dataFrame
    df = pd.DataFrame(data)

    # sort
    df = df.sort_values(['customer_town', 'customer_approach', 'product_name'])

    # build townbased
    townbased = {
            t:df[df['customer_town'] == t].to_dict("list") for t in df['customer_town'].unique().tolist()
        } 

    orderDetails = xlsx.print_order_list(
        townbased,
        path = None,
        tomorrow = True,
        language = language
    )

    return {
        'success':True,
        'error':"",
        'data':{
            'file':orderDetails,
            'date':time.to_string(
                time.utc_to_local(
                    time.utcnow() + datetime.timedelta(days=1),
                    tz = app.config['TZ_INFO']
                    ), 
                "%Y-%m-%d"
                )
            }
    }

def print_cover(
        data:dict,
        language = app.config['DEFAULT_LANGUAGE']
    ) -> dict:
    """Create the cover excel sheet

    Creates the excel cover and returns it.

    params:
    -------
    data : dict
        The town based data for each abo.
            Format: {
                    'customer_approach':list[int], 
                    'customer_street':list[str], 
                    'customer_nr':list[int],
                    'customer_town':list[str],
                    'customer_name':list[str],
                    'customer_surname':list[str],
                    'customer_id':list[int],
                    'customer_phone':list[str],
                    'customer_mobile':list[str],
                    'quantity':list[int], 
                    'product_name':list[str], 
                    'product_id':list[int],
                    'category_name':list[str],
                    'subcategory_name':list[str],
                    'product_selling_price':list[float],
                    'cost':list[float],
                    'total_cost':list[float],
                    'notes':list[str]
                    'id':list[int] # -> the abo_id
                    }
            }
    language : str, optional
        language ISO code for the errors.
        (default is app.config['DEFAULT_LANGUAGE])
 
    returns:
    -------
    dict
        success, error & data:{
            'file':io.BytesIO,
            'date':str
            }

    """

    # get language errorcodes
    try: errors = language_files[language]['error_codes']
    except: errors = language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']

    # data empty?
    if not bool(data): return {'success':False, 'error':errors['noEntry'], 'data':{}}

    # all relevant columns in the data?
    relCols = [
        'customer_approach',
        'customer_street', 
        'customer_nr',
        'customer_town',
        'customer_name',
        'customer_surname',
        'customer_id',
        'customer_phone',
        'customer_mobile',
        'quantity', 
        'product_name', 
        'product_id',
        'product_selling_price',
        'subcategory_name',
        'category_name',
        'cost',
        'total_cost',
        'customer_notes',
        'id'
        ]
    for col in relCols:

        if col not in data.keys(): return {
            'success':False, 
            'error':errors['missingData'].format(column=str(col)), 
            'data':{}
            }

    # turn into pd.dataFrame
    df = pd.DataFrame(data)

    # create product overviews
    # group on granularest level
    granular = _prepare_granular(df)

    # create category overview
    overview_category = _category_overview(granular, to_dict=True)

    # create product overview
    overview_product = _product_overview(granular, to_dict = True)

    # create excel
    cover = xlsx.print_cover(
        category_overview = overview_category,
        product_overview = overview_product,
        path = None,
        tomorrow = True,
        language = language
    )

    return {
        'success':True,
        'error':"",
        'data':{
            'file':cover,
            'date':time.to_string(
                time.utc_to_local(
                    time.utcnow() + datetime.timedelta(days=1),
                    tz = app.config['TZ_INFO']
                    ), 
                "%Y-%m-%d"
                )
            }
    }

#endregion

