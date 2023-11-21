from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime 

db = SQLAlchemy()


class Producer(db.Model, SerializerMixin):
    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    founding_year = db.Column(db.Integer)
    region = db.Column(db.String(255))
    operation_size = db.Column(db.String(20))
    image = db.Column(db.String(255))

    cheeses = db.relationship('Cheese', backref='producer', lazy=True)
    
    @validates(name)
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Producer contain name')
        return name
    
    @validates(founding_year)
    def validate_founding_year(self, key, founding_year):
        if founding_year < 1900 or founding_year > datetime.utcnow().year:
            raise ValueError("Founding year must be between 1900 and the current year.")
        return founding_year
    
    @validates(operation_size)
    def validate_operation_size(self, key, operation_size):
        valid_sizes = ["small", "medium", "large", "family", "corporate"]
        if operation_size not in valid_sizes:
            raise ValueError("Operation size must be one of: small, medium, large, family, corporate")
        return operation_size
    
    def __repr__(self):
        return f"<Producer {self.id}>"
    
class Cheese(db.Model, SerializerMixin):
    __tablename__ = "cheeses"

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(255))
    producer_id = db.Column(db.Integer, db.ForeignKey('producers.id'))
    is_raw_milk = db.Column(db.Boolean)
    production_date = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(255))
    price = db.Column(db.Float)
    
    producer_name = association_proxy('producer', 'name')
    
    @validates(production_date)
    def validate_production_date(self, key, production_date):
        if production_date > datetime.utcnow():
            raise ValueError("Production date must be before today")
        return production_date
 
    @validates(price)
    def validate_price(self, key, price):
     if not (1.00 <= price <= 45.00):
         raise ValueError("Price must be between 1.00 and 45.00")
     return price
        

    def __repr__(self):
        return f"<Cheese {self.id}>"
