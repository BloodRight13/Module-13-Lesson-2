# Modified
from flask import request, jsonify
from . import employees_bp
from ..models import db, Employee, Production, Product
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import func
limiter = Limiter(key_func=get_remote_address)

@employees_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_employee():
    data = request.get_json()
    if not data or 'name' not in data or 'position' not in data:
        return jsonify({'message': 'Invalid request'}), 400
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully', 'id':new_employee.id}), 201

@employees_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_employees():
    employees = Employee.query.all()
    employee_list = [{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees]
    return jsonify(employee_list), 200

@employees_bp.route('/performance', methods=['GET'])
@limiter.limit("10 per minute")
def get_employee_performance():
    performance_data = (
        db.session.query(Employee.name, func.sum(Production.quantity_produced).label('total_quantity'))
        .join(Product, Production.product_id == Product.id)
        .join(Employee, Product.id == Production.product_id)
        .group_by(Employee.name)
        .all()
    )

    result = [{'employee': name, 'total_quantity': total} for name, total in performance_data]
    return jsonify(result), 200