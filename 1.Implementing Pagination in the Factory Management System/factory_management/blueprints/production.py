from flask import request, jsonify
from . import production_bp
from ..models import db, Production
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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