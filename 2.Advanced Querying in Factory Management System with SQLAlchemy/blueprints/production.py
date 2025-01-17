# Modified

from flask import request, jsonify
from . import production_bp
from ..models import db, Production, Product
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import func

limiter = Limiter(key_func=get_remote_address)

@production_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_production():
    data = request.get_json()
    if not data or 'product_id' not in data or 'quantity_produced' not in data or 'date_produced' not in data:
        return jsonify({'message': 'Invalid request'}), 400
    
    date_produced = datetime.strptime(data['date_produced'], '%Y-%m-%d').date()
    
    new_production = Production(
        product_id=data['product_id'],
        quantity_produced=data['quantity_produced'],
        date_produced=date_produced
    )
    db.session.add(new_production)
    db.session.commit()
    return jsonify({'message': 'Production record created successfully', 'id': new_production.id}), 201

@production_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_productions():
    productions = Production.query.all()
    production_list = [{
        'id': prod.id,
        'product_id': prod.product_id,
        'quantity_produced': prod.quantity_produced,
        'date_produced': prod.date_produced.isoformat()
    } for prod in productions]
    return jsonify(production_list), 200

@production_bp.route('/efficiency', methods=['GET'])
@limiter.limit("10 per minute")
def get_production_efficiency():
    date_str = request.args.get('date', None)

    if not date_str:
        return jsonify({'message': 'Date parameter is required'}), 400

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    production_data = (
        db.session.query(Product.name, func.sum(Production.quantity_produced).label('total_produced'))
        .join(Production, Product.id == Production.product_id)
        .filter(Production.date_produced == date_obj)
        .group_by(Product.name)
        .all()
    )

    result = [{'product': name, 'total_produced': total} for name, total in production_data]
    return jsonify(result), 200
