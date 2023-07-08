from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Apartment(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10))
    tenants = db.relationship('Tenant', backref='apartment', cascade='all, delete-orphan')
    lease = db.relationship('Lease', backref='apartment', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'tenants': [tenant.to_dict() for tenant in self.tenants],
            'lease': self.lease.to_dict() if self.lease else None
        }
    
class Tenant(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'apartment_id': self.apartment_id
        }
    
    @validates('age')
    def validate_age(self, key, age):
        if age < 18:
            raise ValueError("Age must be over 18.")
        return age

class Lease(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Float)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'rent': self.rent,
            'apartment_id': self.apartment_id
        }