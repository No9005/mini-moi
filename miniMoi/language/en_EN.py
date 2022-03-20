"""
The english language files

"""

mapping = {
    'error_codes':{
        'noCommit':"Not able to commit.: {e}: {m}.",
        'unableOperation':"Not able to run the operation '{operation}' the {element}.: {c}: {e}: {m}.",
        'wrongCategory':"Selected category for product not available. (prior '{prior}', now '{p}', category '{c}').",
        'wrongProduct':"Selected product not available.",
        'noEntry':"You did not enter/change anything.",
        'notFound':"The {element} was not found.",
        'wrongFilter':"The applied filter needs to be one of the following: {f}",
        'uknownFilter':"The applied filter is not known.",
        'wrongType':"'{var}' needs to be a(n) {dtype}.",
        'notAllowed':"'{var}' needs to be one of the following '{available}'.",
        'weekdays':"Monday, Tuesday, Wendsday, Thursday, Friday, Saturday, Sunday",
        'cycleMismatch':"The 'interval' is not allowed to be None if the 'cycle_type' indicates a 'day' or 'interval'.",
        '500':"An error occured: {c}: {m}",
        '404':"Endpoint '{ressource}' not found.",


    }
}