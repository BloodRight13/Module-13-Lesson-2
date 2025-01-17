from flask import request, jsonify
from . import employees_bp
from ..models import db, Employee
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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
