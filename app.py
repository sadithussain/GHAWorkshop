from flask import Flask, jsonify
from blueprints.rooms import rooms_bp
from blueprints.devices import devices_bp
from db import load_db

def create_app():
    app = Flask(__name__)

    app.register_blueprint(rooms_bp, url_prefix='/rooms')
    app.register_blueprint(devices_bp, url_prefix='/devices')

    @app.get('/')
    def index():
        return jsonify({'message': 'Welcome to your smart home! Use /rooms or /devices to explore.'})
    
    return app

if __name__ == '__main__':
    load_db()
    app = create_app()
    app.run(debug=True, port=5000)