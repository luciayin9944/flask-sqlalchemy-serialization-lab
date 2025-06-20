from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item') ##[item.item for item in customer.reviews]

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()

    reviews = fields.List(fields.Nested(lambda:ReviewSchema(exclude=("customer",))))
    # reviews = fields.Nested(lambda:ReviewSchema(exclude=("customer",)))


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item')
    customers = association_proxy("reviews", "customer") 

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    price = fields.Float()
    
    reviews = fields.List(fields.Nested(lambda:ReviewSchema(exclude=("item",))))
    # review = fields.Nested(lambda:ReviewSchema)

#step 1
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>'

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    comment = fields.String()

    customer = fields.Nested(lambda:CustomerSchema(exclude=("reviews",)))
    item = fields.Nested(lambda:ItemSchema(exclude=("reviews",)))

