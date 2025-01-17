from flask import Blueprint

employees_bp = Blueprint('employees', __name__, url_prefix='/employees')
products_bp = Blueprint('products', __name__, url_prefix='/products')
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')
customers_bp = Blueprint('customers', __name__, url_prefix='/customers')
production_bp = Blueprint('production', __name__, url_prefix='/production')
