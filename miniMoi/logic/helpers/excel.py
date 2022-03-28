"""
Helper functions to produce excel data

"""

# import
import typing
import io

import xlsxwriter as xlsx

from pathlib import Path

import miniMoi.logic.helpers.time_module as time
from miniMoi.language import language_files

# region 'private functions' ------------------------

#endregion

#region 'functions' ---------------------------------
def print_cover(
        category_overview:dict, 
        product_overview:dict,
        path:typing.Union[str, None] = None,
        tomorrow:bool=True,
        language:str = "EN"
    ) -> io.BytesIO:
    """Creates the excel cover
    
    This function parses the passed
    data into the excel format.

    params:
    -------
    category_overview : dict
        The dict containing the category
        overview.
            Format: {
                'category_name':list,
                'quantity':list,
                'cost':list
            }
    product_overview : dict
        The dict containing the product
        overview.
            Format: {
                'product_name':list,
                'total':list,
                'subcat1':list,
                'subcatX':list,
                ...
            }
    path : str | None
        If none, the file gets returned
        as bytes io.
        Else it gets saved to disk.
        (default is None)
    tomorrow : bool, optional
        If true, the date gets increased
        by 1.
        (default is True)
    language : bool, optional
        The language to use.
        (default is "EN")
    
    returns:
    --------
    io.BytesIO | None
        Returns the bytes io
    
    """

    # get language files
    try: xlsx_language = language_files[language]['xlsx']
    except: xlsx_language = language_files["EN"]['xlsx']

    # grab current date
    useDate = time.today()

    # increase it?
    if tomorrow: useDate = time.date_by_interval(useDate, interval = 1)

    # parse to string
    date_string = time.to_string(useDate)

    # create bytesIO; see here: https://gist.github.com/marceloleiva/839a73db81e83069694cf53399cded33
    if path is None: output = io.BytesIO()
    else: output = str(path)
    
    # create workbook & worksheet
    workbook = xlsx.Workbook(output, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet("overview")

    # create meta data
    workbook.set_properties({
        'author':"Daniel Kiermeier",
        'category':"CRM light, order overview",
        'keywords':"Mini Moi, order overview",
        'comments':(
            "This file was created by using Mini Moi - "
            "an CRM light app created by Daniel Kiermeier. "
            "You can checkout the project on "
            "https://github.com/No9005/mini-moi "
            )
    })

    # set header image
    worksheet.set_margins(top=1.3)
    worked = worksheet.set_header('&L&G', {'image-left': Path().cwd()/"miniMoi/static/img/miniMoi_logo.png"})

    print(worked)
    #region 'format cells'
    highlight = "b2b2b2"
    offwhite = "eeeeee"

    formats = {
        'title':workbook.add_format({
            'bold':1,
            'font_size':12,
            'font_name':"Grotesk",
            'align':"left",
            'valign':"vcenter",
            'text_wrap':True
            }),
        'notes':workbook.add_format({
            'bold':1,
            'font_name':"Grotesk",
            'align':"left",
            'valign':"vcenter",
            'text_wrap':True,
            'bg_color':offwhite
        }),
        'notes_bg':workbook.add_format({
            'bg_color':offwhite,
            'font_name':"Grotesk",
            'text_wrap':True,
            'align':"left",
            'valign':"vcenter",
        }),
        'subtitle':workbook.add_format({
            'bold':1,
            'font_size':10,
            'font_name':"Grotesk",
            'align':"left",
            'valign':"vcenter",
            'text_wrap':True,
            'bottom':2
        }),
        'table_head':workbook.add_format({
            'align':"left",
            'font_size':9,
            'font_name':"Grotesk",
            'valign':"vcenter",
            'text_wrap':True,
            'bg_color':highlight,
            'bottom':1
        }),
        'table':workbook.add_format({
            'align':"left",
            'font_size':8,
            'font_name':"Grotesk",
            'valign':"vcenter",
            'text_wrap':True,
            'bottom':4
        })
        }

    #endregion

    #region 'write'
    #region 'write info'
    # write title
    worksheet.merge_range(
        1,0, 
        2,5, 
        xlsx_language['title_overview'].format(
            date=date_string, 
            day=xlsx_language['days'][useDate.weekday()].upper()
            ),
        formats['title']
        )

    # write notes
    worksheet.merge_range(
        4,0,
        4,5,
        xlsx_language['notes'],
        formats['notes']
        )
    worksheet.merge_range(
        5,0,
        9,5,
        "",
        formats['notes_bg']
        )

    # add kilometers
    worksheet.merge_range(
        1,7,
        1,8,
        xlsx_language['km'],
        formats['subtitle']
        )
    worksheet.write(2,7, xlsx_language['start'], formats['table'])
    worksheet.write(2,8, "", formats['table'])
    worksheet.write(3,7, xlsx_language['end'], formats['table'])
    worksheet.write(3,8, "", formats['table'])

    # add time
    worksheet.merge_range(
        6,7,
        6,8,
        xlsx_language['time'],
        formats['subtitle']
        )
    worksheet.write(7,7, xlsx_language['start'], formats['table'])
    worksheet.write(7,8, "", formats['table'])
    worksheet.write(8,7, xlsx_language['end'], formats['table'])
    worksheet.write(8,8, "", formats['table'])

    #endregion

    #region 'write data'
    #region 'product overview'
    """
    CAUTION:
    The first product subtitle starts at line
    idx 11.
    We have therefore 41 rows left.
    
    """

    # set rows left
    rows_left = 41

    # set cursor
    cursor_row_start = 11
    cursor_row_end = None
    cursor_row = 11
    cursor_col = 0

    # write product overview
    for category in product_overview:

        # grab category
        tmp = product_overview[category]

        # grab number of rows
        n_rows = len(tmp['product_name'])

        # grab number of cols
        n_cols = len(tmp.keys())

        # write category name
        worksheet.merge_range(
            cursor_row, cursor_col,
            cursor_row, cursor_col + n_cols -1,
            str(category),
            formats['subtitle']
        )

        # add to cursor
        cursor_row += 1
        rows_left -=1
        cursor_row_start +=1
        
        # iterate through cols and rows
        for col in tmp:

            # write the column name
            try: worksheet.write(cursor_row, cursor_col, xlsx_language[col], formats['table_head'])
            except: worksheet.write(cursor_row, cursor_col, col, formats['table_head'])

            # add to cursor
            cursor_row +=1
            rows_left -=1

            # for each row within the column
            for row in tmp[col]:
                
                # write value
                worksheet.write(cursor_row, cursor_col, row, formats['table'])

                # add to cursor
                cursor_row +=1

            # reached end? add to col
            cursor_col += 1

            # save cursor_row_end
            cursor_row_end = cursor_row

            # reset to the start
            cursor_row = cursor_row_start

        # reached end of category?
        # set cursor_row start to cursor_row_end + 2
        cursor_row_start = cursor_row_end + 2

        # reset cursor
        cursor_row = cursor_row_start

        # reset col cursors
        cursor_col = 0

    #endregion

    #region 'category overview'
    # set cursor
    cursor_row_start = 11
    cursor_col = 7

    # write name
    worksheet.merge_range(
        cursor_row_start, cursor_col,
        cursor_row_start, cursor_col + 1,
        xlsx_language['total'],
        formats['subtitle']
    )

    # add to cursor
    cursor_row_start +=1

    # write heads
    worksheet.write(cursor_row_start, cursor_col, xlsx_language['quantity'], formats['table_head'])
    worksheet.write(cursor_row_start, cursor_col+1, xlsx_language['category_name'], formats['table_head'])

    # add to cursor
    cursor_row_start +=1

    # write data
    for i, row in enumerate(category_overview['quantity']): worksheet.write(cursor_row_start + i, cursor_col, row, formats['table'])
    for i, row in enumerate(category_overview['category_name']): worksheet.write(cursor_row_start + i, cursor_col+1, row, formats['table'])

    #endregion

    #endregion

    #endregion

    # close & save
    workbook.close()

    # get to the first byte
    if path is None: output.seek(0)

    return output

def print_order_list(
        data:dict, 
        path:typing.Union[str, None]=None, 
        tomorrow:bool = True, 
        language:str = "EN"
    ) -> typing.Union[io.BytesIO, str]:
    """Creates the excel cover
    
    This function parses the passed
    data into the excel format.

    params:
    -------
    data : dict
        Contains the orders list for the
        consumers.
            Format: {
                'town1':{
                    'customer_approach':list, 
                    'customer_street':list, 
                    'customer_nr':list,
                    'customer_town':list,
                    'customer_name':list,
                    'customer_surname':list,
                    'customer_id':list,
                    'customer_phone':list,
                    'customer_mobile':list,
                    'quantity':list, 
                    'product_name':list, 
                    'product_id':list,
                    'product_selling_price':list,
                    'subcategory_name':list,
                    'category_name':list,
                    'cost':list,
                    'total_cost':list,
                    'customer_notes':list,
                    'id':list
                },
                'townX':{...},
                ...
            }
    path : str | None
        If none, the file gets returned
        as bytes io.
        Else it gets saved to disk.
        (default is None)
    tomorrow : bool, optional
        If true, the date gets increased
        by 1.
        (default is True)
    language : bool, optional
        The language to use.
        (default is "EN")
    
    returns:
    --------
    io.BytesIO
        Returns the bytes io

    """

    # get language files
    try: xlsx_language = language_files[language]['xlsx']
    except: xlsx_language = language_files["EN"]['xlsx']

    # grab current date
    useDate = time.today()

    # increase it?
    if tomorrow: useDate = time.date_by_interval(useDate, interval = 1)

    # parse to string
    date_string = time.to_string(useDate)

    # create bytesIO; see here: https://gist.github.com/marceloleiva/839a73db81e83069694cf53399cded33
    if path is None: output = io.BytesIO()
    else: output = str(path)
    
    # create workbook & worksheet
    workbook = xlsx.Workbook(output, {'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet("order details")
    worksheet.set_landscape()

    # create meta data
    workbook.set_properties({
        'author':"Daniel Kiermeier",
        'category':"CRM light, order details",
        'keywords':"Mini Moi, order details",
        'comments':(
            "This file was created by using Mini Moi - "
            "an CRM light app created by Daniel Kiermeier. "
            "You can checkout the project on "
            "https://github.com/No9005/mini-moi "
            )
    })

    # set header image
    worksheet.set_margins(top=1.3)
    worksheet.set_header('&L&G', {'image-left': Path().cwd()/"miniMoi/static/img/miniMoi_logo.png"})

    #region 'format cells'
    #region 'set width'
    worksheet.set_column(0,0, 10) # street
    worksheet.set_column(1,1, 5) # nr
    worksheet.set_column(2,2, 10) # name
    worksheet.set_column(3,3, 10) # surname
    worksheet.set_column(4,4, 5) # quant
    worksheet.set_column(5,5, 10) # product
    worksheet.set_column(6,6, 10) # type
    worksheet.set_column(7,7, 5) # cost
    worksheet.set_column(8,8, 10) # phone
    worksheet.set_column(9,9, 10) # mobile
    worksheet.set_column(10,10, 20) # notes
    worksheet.set_column(11,11, 5) # check

    #endregion

    highlight = "b2b2b2"
    offwhite = "eeeeee"

    formats = {
        'title':workbook.add_format({
            'bold':1,
            'font_size':12,
            'font_name':"Grotesk",
            'align':"left",
            'valign':"vcenter",
            'text_wrap':True
            }),
        'notes':workbook.add_format({
            'bold':1,
            'font_name':"Grotesk",
            'align':"left",
            'valign':"vcenter",
            'text_wrap':True,
            'bg_color':offwhite
        }),
        'notes_bg':workbook.add_format({
            'bg_color':offwhite,
            'font_name':"Grotesk",
            'text_wrap':True,
            'align':"left",
            'valign':"vcenter",
        }),
        'subtitle':workbook.add_format({
            'bold':1,
            'font_size':10,
            'font_name':"Grotesk",
            'align':"left",
            'valign':"vcenter",
            'text_wrap':True,
            'bottom':2
        }),
        'table_head':workbook.add_format({
            'align':"left",
            'font_size':9,
            'font_name':"Grotesk",
            'valign':"vcenter",
            'text_wrap':True,
            'bg_color':highlight,
            'bottom':1
        }),
        'table':workbook.add_format({
            'align':"left",
            'font_size':8,
            'font_name':"Grotesk",
            'valign':"vcenter",
            'text_wrap':True,
            'bottom':4
        }),
        'table_no_border':workbook.add_format({
            'align':"left",
            'font_size':8,
            'font_name':"Grotesk",
            'valign':"vcenter",
            'text_wrap':True
        }),
        'table_separator':workbook.add_format({
            'align':"left",
            'font_size':8,
            'font_name':"Grotesk",
            'valign':"vcenter",
            'text_wrap':True,
            'bottom':1
        })
        }

    #endregion

    #region 'write'
    #region 'write info'
    # write title
    worksheet.merge_range(
        1,0, 
        2,5, 
        xlsx_language['title_details'].format(
            date=date_string, 
            day=xlsx_language['days'][useDate.weekday()].upper()
            ),
        formats['title']
        )

    #endregion

    #region 'write details'
    # needed cols
    neededCols = [
        'customer_street',
        'customer_nr',
        'customer_name',
        'customer_surname',
        'quantity',
        'product_name',
        'subcategory_name',
        'total_cost',
        'customer_phone',
        'customer_mobile',
        'customer_notes'
        ]

    # get number of cols -> +1 for checkbox
    n_cols = len(neededCols) + 1

    # set cursor
    cursor_row_start = 4
    cursor_row = 4
    cursor_col = 0

    # for each town
    for town in data:

        # get town
        tmp = data[town]

        # kill not needed columns
        tmp = {col:tmp[col] for col in neededCols}

        # write town name
        worksheet.merge_range(
            cursor_row, cursor_col,
            cursor_row, cursor_col + n_cols -1,
            town,
            formats['subtitle']
        )

        # add to cursor
        cursor_row_start +=1
        cursor_row = cursor_row_start

        # for each column in the data
        for c, col in enumerate(tmp.keys()):

            # write down the column
            worksheet.write(cursor_row, cursor_col, xlsx_language[col], formats['table_head'])

            # add cursor row
            cursor_row += 1

            # get length of rows
            n_rows = len(tmp[col])

            # only for the first col: check the separator idx
            if c == 0:
                separator_idx = []
                for i, row in enumerate(tmp[col]):
                    try: 
                        if row != tmp[col][i+1]: separator_idx.append(i)
                    except: separator_idx.append(i)

            # for each entry
            for i, row in enumerate(tmp[col]):
                
                # blank text
                insert_value = ""

                # determin if we should write the text or not
                if i == 0: insert_value = row
                else :

                    # was the last value a different one?
                    if row != tmp[col][i-1]: insert_value = row

                if i in separator_idx: use_format = formats['table_separator']
                else: use_format = formats['table']

                # write the value
                worksheet.write(cursor_row, cursor_col, insert_value, use_format)

                # add to cursor
                cursor_row += 1

            # end of row? -> reset
            cursor_row = cursor_row_start
            cursor_col += 1

        # end of all columns? -> add checkbox
        worksheet.write(cursor_row, cursor_col, xlsx_language['checkbox'], formats['table_head'])

        # add to cursor
        cursor_row += 1

        # for length of n_rows write nothing
        for i in range(n_rows): 
            
            if i in separator_idx: worksheet.write(cursor_row, cursor_col, "", formats['table_separator'])
            else: worksheet.write(cursor_row, cursor_col, "", formats['table'])

            # add to cursor row
            cursor_row += 1

        # set cursor_row_end to cursor_row and add 2
        cursor_row_start = cursor_row + 2
        cursor_row = cursor_row_start
        cursor_col = 0

        # loop again!

    #endregion

    # close & save
    workbook.close()

    # get to the first byte
    if path is None: output.seek(0)

    return output

    #endregion

#endregion


#region 'CAUTION: visual inspection'
"""
CAUTION:
Not for production, only for testing!

"""

def test_cover():
    """Prints a cover to the 'vorlagen' directory. """

    cwd = Path().cwd()
    print("CWD:", cwd)

    testProducts = {'Brot':{
                'product_name':["Fitnessbrot", "Sonnenkernbrot"],
                'total':[10,7],
                'Geschnitten':[10,0],
                'Ganz':[0,7]
            },
            'Semmel':{
                'product_name':["Doppelweck", "Kaisersemmel"],
                'total':[20,5],
                'Geschnitten':[20,0],
                'Ganz':[0,5]
            }}

    testCategories = {
            'category_name':["Brot", "Semmel"],
            'quantity':[17,25],
            'cost':[74.50, 12.50]
        }

    response = print_cover(testCategories, testProducts, path = str(cwd/"vorlagen/print_test.xlsx"), tomorrow = True, language = "EN")
    
    print("DONE")

def test_details():
    """Prints order details to 'vorlagne' directory """

    testData = {
        'Entenhausen':{
            'customer_approach':[1,1,3,3,3], 
            'customer_street':["Quickhausen", "Quickhausen", "Elmstreet", "Elmstreet", "Elmstreet"], 
            'customer_nr':[5,5,5,5,5],
            'customer_town':["Entenhausen", "Entenhausen", "Entenhausen", "Entenhausen", "Entenhausen"],
            'customer_name':["Hans", "Hans", "Fritz", "Fritz", "Fritz"],
            'customer_surname':["Peter", "Peter", "Meier", "Meier", "Meier"],
            'customer_id':[2,2,1,1,1],
            'customer_phone':["+83 phone", "+83 phone", "+83 phone", "+83 phone", "+83 phone"],
            'customer_mobile':["+83 mobile", "+83 mobile", "+83 mobile", "+83 mobile", "+83 mobile"],
            'quantity':[10,5,10,5,2], 
            'product_name':["Doppelweck", "Sonnenkernbrot", "Fitnessbrot", "Kaisersemmel", "Sonnenkernbrot"], 
            'product_id':[5, 1, 2, 4, 1],
            'product_selling_price':[0.5, 3.5, 5.0, 0.5, 3.5],
            'subcategory_name':["Geschnitten", "Ganz", "Geschnitten", "Ganz", "Ganz"],
            'category_name':["Semmel", "Brot", "Brot", "Semmel", "Brot"],
            'cost':[5.00, 17.50, 50.0, 2.50,7.0],
            'total_cost':[22.50, 22.50, 59.50, 59.50, 59.50],
            'customer_notes':["First boy", "First boy", "idx 1", "idx 1", "idx 1"],
            'id':[5, 6, 1, 3, 2]
        },
        'Dreamland':{
            'customer_approach':[1], 
            'customer_street':["Castlestreet"], 
            'customer_nr':[5],
            'customer_town':["Dreamland"],
            'customer_name':["Zorg"],
            'customer_surname':["King"],
            'customer_id':[3],
            'customer_phone':["+83 phone"],
            'customer_mobile':["+83 mobile"],
            'quantity':[10], 
            'product_name':["Doppelweck"],
            'product_id':[5],
            'product_selling_price':[.5],
            'subcategory_name':["Geschnitten"],
            'category_name':["Semmel"],
            'cost':[5.00],
            'total_cost':[5.00],
            'customer_notes':["First boy, again"],
            'id':[8]
        }
    }

    cwd = Path().cwd()
    print("CWD:", cwd)

    respones = print_order_list(testData, str(cwd/"vorlagen/test_order_details.xlsx"), True, "EN")

    print("DONE")

#endregion