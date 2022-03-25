/*
Collection of functions to help in the creation process

*/

function create_table(data, editable, relevant_columns, not_editable_columns=[]) {
    /* creates a table and returns it

    params:
    -------
    data : json-object
        The data to use for the population.
            Format: {
                'data':{
                    col:[values],
                    col:[values],
                    col:[values],
                    ....
                },
                'order':[],
                'mapping':[]
            }
    editable : bool
        if true, the rows are editable.
    relevant_columns : array | null
        If not null, the array is used as
        selector and order indicator for the
        columns.
    not_editable_columns : array, optional
        Contains colums which should never be
        editable.
        (default is [ ])

    
    returns:
    --------
    html object
        The generated table.

    */

    // get col names
    var cols = data.order;
    var n_cols = cols.length;
    var cols_names = data.mapping;
    var values = data.data;

    // check if we have a relevant_columns array
    if (relevant_columns != null) {

        var new_col_names = [];

        // get corresponding display names
        relevant_columns.forEach(function(col, c) {
            
            // get idx of the col in 'cols'
            var idx = cols.indexOf(col);

            if (idx != -1) { new_col_names.push(cols_names[idx]) }
        });

        // overwrite cols, n_cols & col_names
        cols = relevant_columns;
        cols_names = new_col_names;
        n_cols = cols.length;
        
    };

    // get the length of the table
    var n_entries = values[cols[0]].length;

    // create table element
    var tbl = document.createElement('table');
    tbl.classList.add("table", "table-hover", "table-sm");

    // add head
    var tblh = document.createElement('thead');
    var tblh_tr = document.createElement('tr');
    // only for the 'head' columns: to identify during book!
    tblh_tr.classList.add("head");
    
    // populate thead
    for (i = 0; i < n_cols; i++) {
        
        // create element
        var th = document.createElement('th');
        th.scope = "col";
        th.headers = cols[i];

        // set inner html
        th.innerHTML = cols_names[i];

        // check if col contains underscores -> indicatdes to hide
        if (cols_names[i].includes("_") || cols_names[i] == "id") {
            th.classList.add("hidden");
        };

        // add to table-head-row
        tblh_tr.appendChild(th);

    };

    // add col for remover
    if (editable) {

        var th = document.createElement('th');
        th.scope = "col";
        th.setAttribute('style', "width:5%");

        // append
        tblh_tr.appendChild(th);
    }

    // add the table-head-row to table-head
    tblh.appendChild(tblh_tr);
    tbl.appendChild(tblh);

    // create table body
    var tbody = document.createElement('tbody');

    // populate body
    for (var r = 0; r < n_entries; r++) {

        // create table row
        var tr = document.createElement('tr');

        for (c = 0; c < n_cols; c++) {

            // create table cell
            if (c == 0) { var th = document.createElement('th'); }
            else { var th = document.createElement('td'); };

            // should be invisible?
            if (cols_names[c].includes("_") || cols_names[c] == "id") { th.classList.add("hidden"); };

            // editable?
            if (editable & !not_editable_columns.includes(cols[c])) { th.setAttribute('contenteditable', "true"); };

            // add col name
            th.innerHTML = values[cols[c]][r];

            // add coordinates
            th.classList.add("col_" + c.toString(), "row_" + r.toString());

            // append to table-row
            tr.appendChild(th);
        };

        // add remover cell
        if (editable) {
            
            // create cell
            var th = document.createElement('td');
            th.innerHTML = "<i class='fa-solid fa-circle-minus fa-lg table-remove'></i>";
            th.classList.add("col_remover", "row_remover");

            // add to row
            tr.appendChild(th);
        };

        // append table row to table body
        tbody.appendChild(tr);
    };

    // append table body
    tbl.appendChild(tbody)

    return tbl

};

function empty_tr(n_cols, editable) {
    /* creates a empty table row
    
    params:
    -------
    n_columns : int
        Number of columns for the row
    element : html element
        The element to append to
    editable : bool
        If true, the element is editable
        
    returns:
    --------
    html
        The empty row

    */

    // create table row tag
    var tr = document.createElement('tr');

    // append cells to it
    for (var i = 0; i < n_cols; i++) {

        var td = document.createElement('td');
        td.innerHTML="";

        // create cell
        if (editable) {
            td.contentEditable = "true";
        };

        // append as child
        tr.appendChild(td);

    };

    // add remove icon
    var td = document.createElement('td');
    var icon = document.createElement('i');
    icon.classList.add("fa-solid", "fa-circle-minus", "fa-lg", "table-remove")
    td.appendChild(icon);
    tr.append(td);

    return tr
};

function get_table_values(table) {
    /* Grabs all table values 
    
    Grabs all values from a table and returns
    an array containing json-objects for each row.

    params:
    -------
    table : html element
        the table to parse

    returns:
    --------
    array
    
    */
    
    // grab table
    var TABLE = table

    // grab headers
    var cols = [];

    TABLE.find('thead').children('tr').children().each(function() {
        
        // get headers value
        var headers = $(this).attr('headers');

        if (headers != null) {
            cols.push(headers);
        };
    });

    // create data array
    var data = [];

    // create flat data & iterate
    // see: https://stackoverflow.com/questions/2448051/how-can-i-select-all-elements-without-a-given-class-in-jquery
    TABLE.find('tr:not(.head').each(function () {

        // find all 'td's for row
        var tmp_td = $(this).children();
        var h = {};

        // cycle through headers and apply to h
        // CAUTION: automatically kills the last col (-> no idx for it!)
        cols.forEach(function (col, c) {

            // add key:text at idx[c]
            h[col] = tmp_td.eq(c).text();
        });

        // add to data
        data.push(h);

    });

    return data
};