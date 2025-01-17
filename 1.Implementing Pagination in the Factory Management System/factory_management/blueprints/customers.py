from flask import request, jsonify
from . import customers_bp
from ..models import db, Customer
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

@customers_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_customer():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data or 'phone' not in data:
        return jsonify({'message': 'Invalid request'}), 400
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully', 'id': new_customer.id}), 201

@customers_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_customers():
    customers = Customer.query.all()
    customer_list = [{
        'id': cust.id,
        'name': cust.name,
        'email': cust.email,
        'phone': cust.phone
    } for cust in customers]
    return jsonify(customer_list), 200