from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)

    tenants = db.relationship('Tenant', secondary='lease')
    leases = db.relationship('Lease', backref='apartment')

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    apartments = db.relationship('Apartment', secondary='lease')
    leases = db.relationship('Lease', backref='tenant')

    @validates('age')
    def validate_age(self, key, age):
        if age < 18:
            raise ValueError("Tenant must be at least 18 years old.")
        return age

class Lease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Float, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)

    tenant = db.relationship('Tenant', backref=db.backref('lease_associations', cascade='all, delete-orphan'))
    apartment = db.relationship('Apartment', backref=db.backref('lease_associations', cascade='all, delete-orphan'))
