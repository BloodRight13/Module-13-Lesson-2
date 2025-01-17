# Modified
from flask import request, jsonify
from . import products_bp
from ..models import db, Product
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)


@products_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'message': 'Invalid request'}), 400
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully', 'id': new_product.id}), 201


@products_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    products_pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    products = products_pagination.items

    product_list = [{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]

    return jsonify({
        'products': product_list,
        'page': products_pagination.page,
        'per_page': products_pagination.per_page,
        'total_pages': products_pagination.pages,
        'total_items': products_pagination.total
    }), 200