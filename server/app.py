from flask import Flask, make_response, request
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

# Apartment resource
class ApartmentResource(Resource):
    def get(self, apartment_id=None):
        if apartment_id:
            apartment = Apartment.query.get(apartment_id)
            if apartment:
                return apartment.serialize()
            else:
                return {'message': 'Apartment not found'}, 404
        else:
            apartments = Apartment.query.all()
            return [apartment.serialize() for apartment in apartments]

    def post(self):
        data = request.get_json()
        number = data.get('number')

        if not number:
            return {'message': 'Apartment number is required'}, 400

        apartment = Apartment(number=number)
        db.session.add(apartment)
        db.session.commit()

        return apartment.serialize(), 201
    def patch(self, apartment_id):
        apartment = Apartment.query.get(apartment_id)
        if apartment:
            data = request.get_json()
            number = data.get('number')

            if number:
                apartment.number = number

            db.session.commit()
            return apartment.serialize()
        else:
            return {'message': 'Apartment not found'}, 404


    def delete(self, apartment_id):
        apartment = Apartment.query.get(apartment_id)
        if apartment:
            db.session.delete(apartment)
            db.session.commit()
            return {'message': 'Apartment deleted'}
        else:
            return {'message': 'Apartment not found'}, 404

api.add_resource(ApartmentResource, '/apartments', '/apartments/<int:apartment_id>')

# Tenant resource
class TenantResource(Resource):
    def get(self, tenant_id=None):
        if tenant_id:
            tenant = Tenant.query.get(tenant_id)
            if tenant:
                return tenant.serialize()
            else:
                return {'message': 'Tenant not found'}, 404
        else:
            tenants = Tenant.query.all()
            return [tenant.serialize() for tenant in tenants]

    def post(self):
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')

        if not name:
            return {'message': 'Tenant name is required'}, 400

        if age is None:
            return {'message': 'Tenant age is required'}, 400

        try:
            tenant = Tenant(name=name, age=age)
            db.session.add(tenant)
            db.session.commit()
            return tenant.serialize(), 201
        except ValueError as e:
            return {'message': str(e)}, 400

    def patch(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            data = request.get_json()
            name = data.get('name')
            age = data.get('age')

            if name:
                tenant.name = name

            if age is not None:
                try:
                    tenant.age = age
                except ValueError as e:
                    return {'message': str(e)}, 400

            db.session.commit()
            return tenant.serialize()
        else:
            return {'message': 'Tenant not found'}, 404

    def delete(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            db.session.delete(tenant)
            db.session.commit()
            return {'message': 'Tenant deleted'}
        else:
            return {'message': 'Tenant not found'}, 404

api.add_resource(TenantResource, '/tenants', '/tenants/<int:tenant_id>')

# Lease resource
class LeaseResource(Resource):
    def post(self):
        data = request.get_json()
        tenant_id = data.get('tenant_id')
        apartment_id = data.get('apartment_id')
        rent = data.get('rent')

        if not tenant_id:
            return {'message': 'Tenant ID is required'}, 400

        if not apartment_id:
            return {'message': 'Apartment ID is required'}, 400

        if not rent:
            return {'message': 'Rent amount is required'}, 400

        tenant = Tenant.query.get(tenant_id)
        apartment = Apartment.query.get(apartment_id)

        if not tenant:
            return {'message': 'Tenant not found'}, 404

        if not apartment:
            return {'message': 'Apartment not found'}, 404

        lease = Lease(tenant=tenant, apartment=apartment, rent=rent)
        db.session.add(lease)
        db.session.commit()

        return lease.serialize(), 201

    def delete(self, lease_id):
        lease = Lease.query.get(lease_id)
        if lease:
            db.session.delete(lease)
            db.session.commit()
            return {'message': 'Lease deleted'}
        else:
            return {'message': 'Lease not found'}, 404

api.add_resource(LeaseResource, '/leases', '/leases/<int:lease_id>')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
