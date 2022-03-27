"""
Contains the table schemes for the database

"""

# imports
from miniMoi import base, engine

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float

from datetime import datetime


#region 'models' ----------------------------
class Customers(base):
    """Contains customer related data
    
    attributes:
    -----------
    id : int
        The customer id.
    date : datetime
        Date of creation.
    name : str
        Name of customer.
    surname : str
        Surname of customer.
    street : str
        Name of the street.
    nr : int
        House number.
    postal : str
        Zip code of the town
    town : str
        Town name
    phone : str
        Customers phone number.
    mobile : str
        Customers mobile number.
    birthdate : DateTime
        Date of birth.
            Format: %Y.%m.%d
    approach : int
        This value is needed to indicate
        the order of approach for multipe
        customers within one town.
    notes : str
        Additional notes.
    
    relational:
    -----------
    orders
        Link to Orders -> id
    abo
        Link to Abo -> id

    """

    __tablename__ = "customers"

    id = Column(Integer, primary_key = True)
    date = Column(DateTime, default = datetime.utcnow)

    name = Column(String(20), nullable = False)
    surname = Column(String(20), nullable = False)
    street = Column(String(20), nullable = False)
    nr = Column(Integer, nullable = False)
    postal = Column(String(8), nullable = False)
    town = Column(String(20), nullable = False)
    phone = Column(String(20), default = "")
    mobile = Column(String(20), default = "")
    birthdate = Column(DateTime)
    approach = Column(Integer)
    
    notes = Column(String(100), default = "")

    orders = relationship("Orders", backref="customer_orders", cascade=False)
    abo = relationship("Abo", backref="customer_abo", cascade="all, delete-orphan")

class Orders(base):
    """Contains all orders ever done 
    
    attributes:
    -----------
    id : int
        The row id.
    customer_id : int
        Customer id
            ForeignKey: Customers -> id
    date : datetime
        The date of the order in utc.
    product : int
        product id.
            ForeignKey: Product -> id
    name : str
        The product name at the time of
        order.
    quantity : int
        The amount of the ordered product.
    price : float
        The price of the product at the moment.
    total : float
        The total cost for the amount of
        products ordered.
    
    """
    
    __tablename__ = "orders"

    id = Column(Integer, primary_key = True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    product = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String(100), nullable = False)
    category = Column(String(100), default="unknown")
    subcategory = Column(String(100), default="unknown")
    quantity = Column(Integer, nullable = False)
    price = Column(Float, nullable = False)
    total = Column(Float, nullable = False)

class Abo(base):
    """Timeframe & next orders
    
    This table keeps all orders which should be
    delivered in a specific time interval.

    Each row shows one abo of one product for
    one customer.
    If a customer orders multiple products he
    has multiple rows.
    
    attributes:
    -----------
    id : int
        primary key
    customer_id : int
        The customers id
            ForeignKey: Customers -> id
    update_date : datetime
        Date of the update of the consumer
        abo.
    cycle_type : str
        The inteval type of the abo.
            Options: { None, 'day', 'inteval' }
                None: The abo is currently not active.
                'day': The product should be deliverd always
                       at the same day in the week.
                            Example: if the 'interval' column is
                                     "Monday", then this means
                                     every Monday.
                'inteval': The product should be delivered
                           again after a certain amount of time.
                            Example: if the 'interval' column is
                                     2, this means, every second day.
    interval : int
        The interval of the delivery.
            Options: {
                'None', str(Integer)
                }
            Caution: The days Monday to Sunday
                     are mapped to ints starting at
                     zero (0 = Monday)
    next_delivery : datetime
        The datetime of the next delivery (in UTCnow!).
            Caution: This is the actual delivery date!
    product : int
        Product id.
            ForeignKey: Products -> id
    subcategory: int
        subcategory id.
            ForeignKey: Subcategory -> id
    quantity : int
        The quantity of the product in the abo.
    
    """

    __tablename__ = "abo"

    id = Column(Integer, primary_key = True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable = False)
    update_date = Column(DateTime, default = datetime.utcnow)

    cycle_type = Column(String(10))
    interval = Column(Integer)
    next_delivery = Column(DateTime)

    product = Column(Integer, ForeignKey("products.id"), nullable=False)
    subcategory = Column(Integer, ForeignKey("subcategory.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

class Category(base):
    """Contains all product categories 
    
    attributes:
    -----------
    id : int
        primary key
    name : str
        Category name
    
    relational:
    -----------
    products
        Link to Products -> category
    
    """

    __tablename__ = "category"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False, unique = True)

    products = relationship("Products", backref="category_products", cascade="all, delete-orphan")

class Subcategory(base):
    """Keeps types of subcategories
    
    A subcategory could be 'cut' or
    'whole'

    attributes:
    -----------
    id : int
        the primary key.
    name : str
        The name of the category.

    """

    __tablename__ = "subcategory"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    abo = relationship("Abo", backref="subcategory_abo", cascade=False)

class Products(base):
    """Contains all available products to order 
    
    attributes:
    -----------
    id : int
        primary key
    name : str
        Product name.
    category : int
        The product category id
            ForeignKey: Category -> id
    purchase_price : float
        Cost to purchase this item from the
        distributor
    selling_price : float
        Price upon selling the item.
    margin : float
        Margin in % (--> as decimal)
            Example: .3 = 30%
    store : str
        Name of the item vendor.
    phone : str
        Number of the item vendor.

    relational:
    -----------
    ordered
        Linked to the Orders table
    abos
        Linked to the Abo table

    """

    __tablename__ = "products"

    id = Column(Integer, primary_key = True)

    name = Column(String(100), nullable=False, unique=True)
    category = Column(Integer, ForeignKey("category.id"), nullable = False)
    
    purchase_price = Column(Float, nullable = False)
    selling_price = Column(Float, nullable=False)

    margin = Column(Float)

    store = Column(String(100))
    phone = Column(String(20))

    ordered = relationship("Orders", backref="product_ordered", cascade=False)
    abos = relationship("Abo", backref="product_abos", cascade="all, delete-orphan")

class Log(base):
    """Table tracks all made changes 
    
    This table saves all made changes
    to any of the databases.

    attributes:
    -----------
    id : int
        primary key
    date : datetime
        utcnow of the change
    ressource : str
        Name of the used ressource
        (= endpoint).
    action : str
        Stringified dict. Contains
        the passed parameters.
    
    """

    __tablename__ = "log"

    id = Column(Integer, primary_key = True)
    date = Column(DateTime, default = datetime.utcnow)

    ressource = Column(String(500), nullable = False)
    action = Column(String(500), nullable = False)

#endregion
