"""
Generates test data if called

"""

# imports
import datetime

from miniMoi import Session
from miniMoi.models.Models import Category, Subcategory, Products, Customers, Abo


#region 'run'
def generate():
    """ generates test data """

    # create session
    session = Session()


    toAdd = []

    #region 'category'
    # 1
    toAdd.append(Category(
        name = "Brot"
    ))

    # 2
    toAdd.append(Category(
        name = "Semmel"
    ))

    # 3
    toAdd.append(Category(
        name = "Mischware"
    ))

    #endregion

    #region 'subcategory'
    # 1
    toAdd.append(Subcategory(
        name = "Ganz"
    ))

    # 2
    toAdd.append(Subcategory(
        name = "Geschnitten"
    ))

    #endregion

    #region 'products'
    # 1
    toAdd.append(Products(
        name = "Sonnenkernbrot",
        category = 1,
        purchase_price = 2.00,
        selling_price = 3.50,
        margin = .01,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 2
    toAdd.append(Products(
        name = "Fitnessbrot",
        category = 1,
        purchase_price = 2.50,
        selling_price = 5.00,
        margin = .01,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 3
    toAdd.append(Products(
        name = "Baguette",
        category = 3,
        purchase_price = 1.00,
        selling_price = 2.50,
        margin = .01,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 4
    toAdd.append(Products(
        name = "Kaisersemmel",
        category = 2,
        purchase_price = .20,
        selling_price = .50,
        margin = .01,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 5
    toAdd.append(Products(
        name = "Doppelweck",
        category = 2,
        purchase_price = .15,
        selling_price = .50,
        margin = .01,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    #endregion

    #region 'customers'
    # 1
    toAdd.append(Customers(
        name = "Fritz",
        surname = "Meier",
        street = "Elmstreet",
        nr = 5,
        postal = "0000",
        town = "Entenhausen",
        phone = "+83 phone",
        mobile = "+83 mobile",
        birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
        approach = 3,
        notes = "idx 1"
    ))

    # 2
    toAdd.append(Customers(
        name = "Hans",
        surname = "Peter",
        street = "Quickhausen",
        nr = 5,
        postal = "0000",
        town = "Entenhausen",
        phone = "+83 phone",
        mobile = "+83 mobile",
        birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
        approach = 1,
        notes = "First boy"
    ))

    #3
    toAdd.append(Customers(
        name = "Zorg",
        surname = "King",
        street = "Castlestreet",
        nr = 5,
        postal = "0001",
        town = "Dreamland",
        phone = "+83 phone",
        mobile = "+83 mobile",
        birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
        approach = 1,
        notes = "First boy, again"
    ))

    #4
    toAdd.append(Customers(
        name = "Dagobert",
        surname = "Duck",
        street = "Gansstr.",
        nr = 5,
        postal = "0000",
        town = "Entenhausen",
        phone = "+83 phone",
        mobile = "+83 mobile",
        birthdate = datetime.datetime.strptime("2022.03.16", "%Y.%m.%d"),
        approach = 2,
        notes = "Not relevant"
    ))

    #endregion

    #region 'abos'
    #region customer 1
    toAdd.append(Abo(
        customer_id = 1,
        cycle_type = "day",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
        product = 2,
        subcategory = 2,
        quantity = 10
    ))

    toAdd.append(Abo(
        customer_id = 1,
        cycle_type = "interval",
        interval = 2,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
        product = 1,
        subcategory = 1,
        quantity = 2
    ))

    toAdd.append(Abo(
        customer_id = 1,
        cycle_type = "interval",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
        product = 4,
        subcategory = 1,
        quantity = 5
    ))

    # not relevant for tomorrow!
    toAdd.append(Abo(
        customer_id = 1,
        cycle_type = "interval",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date(),
        product = 3,
        subcategory = 1,
        quantity = 5
    ))

    #endregion

    #region customer 2
    toAdd.append(Abo(
        customer_id = 2,
        cycle_type = "day",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
        product = 5,
        subcategory = 2,
        quantity = 10
    ))

    toAdd.append(Abo(
        customer_id = 2,
        cycle_type = "interval",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
        product = 1,
        subcategory = 1,
        quantity = 5
    ))

    # not relevant for tomorrow!
    toAdd.append(Abo(
        customer_id = 2,
        cycle_type = "interval",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=2),
        product = 5,
        subcategory = 1,
        quantity = 5
    ))

    #endregion

    #region customer 3
    toAdd.append(Abo(
        customer_id = 3,
        cycle_type = "day",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=1),
        product = 5,
        subcategory = 2,
        quantity = 10
    ))

    #endregion

    #region customer 4
    # not relevant for today!
    toAdd.append(Abo(
        customer_id = 4,
        cycle_type = "interval",
        interval = 5,
        next_delivery = datetime.datetime.utcnow().date() + datetime.timedelta(days=-1),
        product = 5,
        subcategory = 1,
        quantity = 5
    ))

    #endregion

    # add & commit
    session.add_all(toAdd)
    session.commit()

    #endregion
