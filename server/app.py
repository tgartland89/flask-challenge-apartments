from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apartments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class IndexResource(Resource):
    def get(self):
        return {'message': 'Welcome to the Apartment API'}

api.add_resource(IndexResource, '/')


class ApartmentResource(Resource):
    def get(self, apartment_id=None):
        if apartment_id:
            apartment = Apartment.query.get(apartment_id)
            if not apartment:
                return {'message': 'Apartment not found'}, 404
            return apartment.to_dict(), 200
        else:
            apartments = Apartment.query.all()
            return [apartment.to_dict() for apartment in apartments], 200

    def post(self):
        number = request.json.get('number')
        apartment = Apartment(number=number)
        db.session.add(apartment)
        db.session.commit()
        return apartment.to_dict(), 201

    def patch(self, apartment_id):
        apartment = Apartment.query.get(apartment_id)
        if not apartment:
            return {'message': 'Apartment not found'}, 404
        number = request.json.get('number')
        if number:
            apartment.number = number
        db.session.commit()
        return apartment.to_dict(), 200

    def delete(self, apartment_id):
        apartment = Apartment.query.get(apartment_id)
        if not apartment:
            return {'message': 'Apartment not found'}, 404
        db.session.delete(apartment)
        db.session.commit()
        return {'message': 'Apartment deleted'}, 200


class TenantResource(Resource):
    def get(self, tenant_id=None):
        if tenant_id:
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                return {'message': 'Tenant not found'}, 404
            return tenant.to_dict(), 200
        else:
            tenants = Tenant.query.all()
            return [tenant.to_dict() for tenant in tenants], 200

    def post(self):
        name = request.json.get('name')
        age = request.json.get('age')
        apartment_id = request.json.get('apartment_id')
        tenant = Tenant(name=name, age=age, apartment_id=apartment_id)
        db.session.add(tenant)
        db.session.commit()
        return tenant.to_dict(), 201

    def patch(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return {'message': 'Tenant not found'}, 404
        name = request.json.get('name')
        age = request.json.get('age')
        apartment_id = request.json.get('apartment_id')
        if name:
            tenant.name = name
        if age:
            tenant.age = age
        if apartment_id:
            tenant.apartment_id = apartment_id
        db.session.commit()
        return tenant.to_dict(), 200

    def delete(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return {'message': 'Tenant not found'}, 404
        db.session.delete(tenant)
        db.session.commit()
        return {'message': 'Tenant deleted'}, 200


class LeaseResource(Resource):
    def post(self, apartment_id):
        rent = request.json.get('rent')
        lease = Lease(rent=rent, apartment_id=apartment_id)
        db.session.add(lease)
        db.session.commit()
        return lease.to_dict(), 201

    def delete(self, apartment_id):
        lease = Lease.query.filter_by(apartment_id=apartment_id).first()
        if not lease:
            return {'message': 'Lease not found'}, 404
        db.session.delete(lease)
        db.session.commit()
        return {'message': 'Lease deleted'}, 200


api.add_resource(ApartmentResource, '/apartments', '/apartments/<int:apartment_id>')
api.add_resource(TenantResource, '/tenants', '/tenants/<int:tenant_id>')
api.add_resource(LeaseResource, '/apartments/<int:apartment_id>/lease')


if __name__ == '__main__':
    app.run(port=3000, debug=True)