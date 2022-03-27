"""
Generates test data if called

"""

# imports
import datetime

import numpy as np
import random

from miniMoi import Session
from miniMoi.models.Models import Category, Subcategory, Products, Customers, Abo, Orders


#region 'run'
def generate():
    """ generates test data """

    # create session
    session = Session()


    toAdd = []

    #region 'step 1 - generate basic data'
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
        purchase_price = 1.20,
        selling_price = 3.50,
        margin = .65,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 2
    toAdd.append(Products(
        name = "Fitnessbrot",
        category = 1,
        purchase_price = 1.80,
        selling_price = 5.00,
        margin = .64,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 3
    toAdd.append(Products(
        name = "Baguette",
        category = 3,
        purchase_price = 1.00,
        selling_price = 2.00,
        margin = .5,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 4
    toAdd.append(Products(
        name = "Kaisersemmel",
        category = 2,
        purchase_price = .20,
        selling_price = .50,
        margin = .6,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    # 5
    toAdd.append(Products(
        name = "Doppelweck",
        category = 2,
        purchase_price = .15,
        selling_price = .50,
        margin = .6,
        store = "MeinLaden",
        phone = "+50 phone"
    ))

    #endregion

    #region 'customers'
    # 1
    toAdd.append(Customers(
        name = "Freddy",
        surname = "Krueger",
        street = "Elmstreet",
        nr = 1428,
        postal = "0000",
        town = "Springwood",
        phone = "+83 nightmare-dreams",
        mobile = "+83 nightmare-dreams",
        birthdate = datetime.datetime.strptime("1984.10.31", "%Y.%m.%d"),
        approach = 1,
        notes = "Sweet dreams"
    ))

    # 2
    toAdd.append(Customers(
        name = "Hans",
        surname = "Peter",
        street = "Quickhausen",
        nr = 17,
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
        nr = 1,
        postal = "0001",
        town = "Dreamland",
        phone = "+83 phone-Zorg",
        mobile = "+83 mobile-Zorg",
        birthdate = datetime.datetime.strptime("2018.03.16", "%Y.%m.%d"),
        approach = 1,
        notes = "First boy, again"
    ))

    #4
    toAdd.append(Customers(
        name = "Dagobert",
        surname = "Duck",
        street = "Gansstr.",
        nr = 80,
        postal = "0000",
        town = "Entenhausen",
        phone = "+83 phone-dagobert",
        mobile = "+83 mobile-dagobert",
        birthdate = datetime.datetime.strptime("1934.01.01", "%Y.%m.%d"),
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

    #endregion

    # add & commit
    session.add_all(toAdd)
    session.commit()

    #endregion

    #region 'step 2 - create orders'
    # reset toAdd
    toAdd = []

    #region 'orders'
    """
    CAUTION:
    We are going to create random orders.
    
    """
    customers_choice = [i for i in range(1,5)]
    # (p_id, p_name, price, cat)
    product_choice = [
        (1, "Sonnenkernbrot", 3.50, "Brot"),
        (2, "Fitnessbrot", 5.00, "Brot"),
        (3, "Baguette", 2.00, "Mischware"),
        (4, "Kaisersemmel", .50, "Semmel"),
        (5, "Doppelweck", .50, "Semmel"),
    ]
    subcat_choice = ["Ganz", "Geschnitten"]
    qnt_choice = [i for i in range(11)]
    date_choice = [
        datetime.datetime.utcnow().date() + datetime.timedelta(weeks=-4),
        datetime.datetime.utcnow().date() + datetime.timedelta(weeks=-1),
        datetime.datetime.utcnow().date() + datetime.timedelta(days=-3, weeks=-1),
        datetime.datetime.utcnow().date() + datetime.timedelta(days=-2),
        datetime.datetime.utcnow().date() + datetime.timedelta(days=-1),
    ]

    # generate orders
    for i in range(50):

        # calculate the product elements
        tmpProd = random.choice(product_choice)
        tmpQnt = random.choice(qnt_choice)
        tmpTotal = tmpProd[2] * tmpQnt

        cstm = random.choice(customers_choice)

        toAdd.append(
            Orders(
                customer_id = cstm,
                date = random.choice(date_choice),
                product = tmpProd[0],
                product_name = tmpProd[1],
                category = tmpProd[-1],
                subcategory = random.choice(subcat_choice),
                quantity = tmpQnt,
                price = tmpProd[2],
                total = tmpTotal,
            )
        )

    #endregion

    # add & commit
    session.add_all(toAdd)
    session.commit()

    #endregion

    #endregion

