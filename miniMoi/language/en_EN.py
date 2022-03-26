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
        'notFoundWithId':"The {element} was not found (id = '{id}').",
        'noElementInDB':"There was no {element} in the database. Please add some first.",
        'noDelivery':"There is no marked delivery for tomorrow.",
        'wrongFilter':"The applied filter needs to be one of the following: {f}",
        'uknownFilter':"The applied filter is not known.",
        'wrongType':"'{var}' needs to be a(n) {dtype}.",
        'wrongFormat':"'{var}' needs to be in the format '{format}'.",
        'notAllowed':"'{var}' needs to be one of the following '{available}'.",
        'weekdays':"Monday, Tuesday, Wendsday, Thursday, Friday, Saturday, Sunday",
        'cycleMismatch':"The 'interval' is not allowed to be None if the 'cycle_type' indicates a 'day' or 'interval'.",
        'missingData':"There is data missing: {column}",
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
        'quantity':"#",
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
        'quantity':"Qnt.",
        'product_name':"Product",
        'subcategory_name':"Type",
        'cost':'Cost',
        'total_cost':"Total",
        'customer_phone':"Phone",
        'customer_mobile':"Mobile",
        'customer_notes':"Notes",
        'checkbox':"Check",
        'customer_approach':"Approach",
        'customer_town':"City",
        'product_selling_price':"selling price",
        'product_id':"Product id",
        'customer_id':"Customer id",
        'id':"Abo"
    },
    'html_text':{
        'base_html':{
            'site_content':"mini-moi app",
            'base_app_name':"Mini Moi",
            'base_delivery':"Delivery",
            'base_tables':"Management",
            'base_settings':"Settings",
            'base_shutdown':"Shutdown",
            'base_documentation':"Documentation",
            'base_update':"Updates",
            'base_releases':"Newest Release",
            'base_version':"Version"
        },
        '/settings':{
            'settings_title':"Settings",
            'settings_lead':"Adjust your app by changing your settings.",
            'settings_language':"Language",
            'settings_language_description':"Set the app language.",
            'settings_logging':"Logging",
            'settings_logging_description':(
                "This enables the logging of actions made by "
                "the user. <br> "
                "<span class='text-danger'>Disabling is not recommended!</span>"
                ),
            'settings_logging_on':"Activated",
            'settings_logging_off':"Deactivated",
            'settings_apply_button':"Apply settings"
        },
        '/':{
            'index_title':"Home",
            'index_hello':"Welcome, Mini Moi user!",
            'index_lead':(
                "A little assistent to get an overview of "
                "the next days orders."
            ),
            'index_getting_started':"Getting started",
            'index_steps':"Only 3 steps needed.",
            'index_setup':"Setup your app ",
            'index_setup_link':"click me!",
            'index_enter_data':(
                "Enter your customer data and add some products. <br>"
                "You need set up the following data:"
                ),
            'index_data_customer':(
                "Your consumers in the <span class='text-info'>Consumer Table</span>."
                ),
            'index_data_categories':(
                "Supply your product categories and subcategories (e.g. 'cut', 'whole') in the "
                "<span class='text-info'>Category Table</span> & <span class='text-info'>Subcategory Table</span>."
                ),
            'index_data_products':(
                "Describe your products in the <span class='text-info'>Products Table</span>"
                ),
            'index_data_abos':(
                "Last, but not least: Add the regular orders to the (consumer) abo's "
                "(<span class='text-info'>Abo Table</span>)"
                ),
            'index_create_report':"Create the report for the next day deliveries!"
        },
        '/shutdown/app':{
            'shutdown_title':"Ended app",
            'shutdown_bye':"Goodby, User!",
            'shutdown_lead':"See you soon for the next deliveries &#128513"
        },
        '/delivery':{
            'delivery_title':"Delivery",
            'delivery_lead':"Create the order report for the next day delivery.",
            'delivery_create_report':"Create",
            'delivery_download':"Redownload report",
            'delivery_book':"Book",
            'delivery_create_tooltip':(
                "Creates the report for the next day. The results are shown below. "
                "You can edit this report to customize your next delivery."
                ),
            'delivery_book_tooltip':(
                "Book locks your current report and moves the products "
                "to the 'Orders' table. Additionally the dates for the "
                "next deliveries are calculated for "
                "your customers (based on the set abos). CAUTION: "
                "You can not undo or re-create the report once you have "
                "'booked' your deliveries!!!"
                ),
            'delivery_download_tooltip':(
                "Download the current (shown) report as excel."
                ),

            'delivery_category_table_name':"Product summary",
            'delivery_orders_table_name':"Orders",

            'delivery_product_overview':"Products",
            'delivery_product_overview_description':(
                "The quantity of products needed for the next delivery."
                ),

            'delivery_category_overview':"Categories",
            'delivery_category_overview_description':(
                "Total amount of needed products based on category."
                ),
            'delivery_category_table_section_name':"All",
            
            'delivery_total_earnings':"Earnings",
            'delivery_total_earnings_description':"Your earnings after your tour tomorrow.",

            'delivery_total_spendings':"Spendings",
            'delivery_total_spendings_description':"Purchase price for all products.",
        },
        '/management':{
            'management_title':"Management",
            'management_lead':"Organize your data.",
            'management_customers_btn':"Customers",
            'management_category_btn':"Categories",
            'management_subcategory_btn':"Subcategories",
            'management_products_btn':"Products",
            'management_abo_btn':"Abos",
            'managment_abo_btn_label':"abo",
            'management_tbl_col_remover':"Remove",
            'management_tbl_col_updater':"Update",
            'management_tbl_col_special':"Special",
            'management_auto_text':"Auto.",
            'management_no_data':"No data available!",
        },

    },
    'notification':{
        'save_path':"Your file was saved at: {path}",
        'added_to_db':"'{element}' was successfully added! Please refresh the data.",
        'deleted_from_db':"'{element}' was successfully deleted!",
        'update_to_db':"'{element}' was successfully updated!"
    },
    'column_mapping':{
        'customers':{
            'id':"id",
            'date':"Date",
            'name':"Name",
            'surname':"Surname",
            'street':"Street",
            'nr':"Nr",
            'postal':"Postal",
            'town':"City",
            'phone':"Phone",
            'mobile':"Mobile",
            'birthdate':"Birthdate",
            'approach':"Approach",
            'notes':"Notes"
            },
        'categories':{
            'id':"id",
            'name':"Name"
            },
        'products':{
            'id':"id",
            'name':"Name",
            'category':"Category",
            'purchase_price':"Purchase price",
            'selling_price':"Selling price",
            'margin':"Margin",
            'store':"Store",
            'phone':"Phone",
            },
        'abo':{
            'id':"id",
            'customer_id':"Customer id",
            'update_date':"Update date",
            'cycle_type':"Cycle type",
            'interval':"Interval",
            'next_delivery':"Next delivery",
            'product':"Product",
            'subcategory':"Subcategory",
            'quantity':"Qnt."
        }
    },
    'table_mapping': {
        'customers':"Customers",
        'customer':"Customer",
        'categories':"Categories",
        'category':"Category",
        'subcategories':"Subcategories",
        'subcategory':"Subcategory",
        'products':"Products",
        'product':"Product",
        'abos':"Abos",
        'abo':"Abo"
    },
    'cycle_type_mapping':{
        'None':"None",
        'day':"Weekday",
        'interval':"Interval"
    },
    'weekday_mapping':{
        0:"Monday",
        1:"Tuesday",
        2:"Wendsday",
        3:"Thursday",
        4:"Friday",
        5:"Saturday",
        6:"Sunday",

    }
    
}