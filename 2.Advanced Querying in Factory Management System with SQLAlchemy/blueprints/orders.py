from flask import request, jsonify
from . import orders_bp
from ..models import db, Order
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)


@orders_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_order():
    data = request.get_json()
    if not data or 'customer_id' not in data or 'product_id' not in data or 'quantity' not in data or 'total_price' not in data:
        return jsonify({'message': 'Invalid request'}), 400
    new_order = Order(
        customer_id=data['customer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully', 'id': new_order.id}), 201

@orders_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_orders():
    orders = Order.query.all()
    order_list = [{
        'id': ord.id,
        'customer_id': ord.customer_id,
        'product_id': ord.product_id,
        'quantity': ord.quantity,
        'total_price': ord.total_price
    } for ord in orders]
    return jsonify(order_list), 200
