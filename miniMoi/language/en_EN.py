"""
The english language files

"""

mapping = {
    'error_codes':{
        'noCommit':"Not able to commit.: {e}: {m}.",
        'unableOperation':"Not able to run the operation '{operation}' the {element}.: {c}: {e}: {m}.",
        'wrongCategory':"Selected category for product not available. (prior '{prior}', now '{p}', category '{c}').",
        'wrongProduct':"Selected product not available.",
        'wrongSubcategory':"Selected subcategory not available.",
        'noEntry':"You did not enter/change anything.",
        'notFound':"The {element} was not found.",
        'noDelivery':"There is no marked delivery for tomorrow.",
        'wrongFilter':"The applied filter needs to be one of the following: {f}",
        'uknownFilter':"The applied filter is not known.",
        'wrongType':"'{var}' needs to be a(n) {dtype}.",
        'notAllowed':"'{var}' needs to be one of the following '{available}'.",
        'weekdays':"Monday, Tuesday, Wendsday, Thursday, Friday, Saturday, Sunday",
        'cycleMismatch':"The 'interval' is not allowed to be None if the 'cycle_type' indicates a 'day' or 'interval'.",
        '500':"An error occured: {c}: {m}",
        '404':"Endpoint '{ressource}' not found.",
    },
    'xlsx':{
        'title_overview':"Orders for {date} - {day}",
        'title_details':"Order details for {date} - {day}",
        'notes':"Notes:",
        'km':"Kilometers",
        'time':"Time",
        'total':"Total",
        'start':"Start",
        'end':"End",
        'product_name':"name",
        'total':"total",
        'quantity':"Quant.",
        'category_name':"Category",
        'days':{
            0:"Monday",
            1:"Tuesday",
            2:"Wendsday",
            3:"Thursday",
            4:"Friday",
            5:"Saturday",
            6:"Sunday"
        },
        'customer_street':"Street",
        'customer_nr':"Nr.",
        'customer_name':"Name",
        'customer_surname':"Surname",
        'quantity':"Quantity",
        'product_name':"Product",
        'subcategory_name':"Type",
        'total_cost':"Cost",
        'customer_phone':"Phone",
        'customer_mobile':"Mobile",
        'customer_notes':"Notes",
        'checkbox':"Check"
    }
}