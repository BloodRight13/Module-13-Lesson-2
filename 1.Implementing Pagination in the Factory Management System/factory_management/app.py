from flask import Flask
from .config import Config
from .models import db
from .blueprints import employees_bp, products_bp, orders_bp, customers_bp, production_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(employees_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(production_bp)
    
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day, 50 per hour"]
    )
    

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)