import pytest
from flask import Flask

from blueprints.devices import devices_bp, db 

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(devices_bp)
    app.config["TESTING"] = True
    
    db['rooms'] = [{'id': 'room_1', 'name': 'Classroom'}]
    db['devices'] = [{'id': 'dev_1', 'name': 'Smart Plug', 'status': 'off', 'room_id': 'room_1'}]
    
    with app.test_client() as client:
        yield client

def test_get_devices(client):
    response = client.get('/')
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_get_device_success(client):
    response = client.get('/dev_1')
    assert response.status_code == 200
    assert response.json['name'] == 'Smart Plug'

def test_get_device_not_found(client):
    response = client.get('/does_not_exist')
    assert response.status_code == 404

def test_create_device_success(client):
    payload = {'name': 'Smart Bulb', 'status': 'on', 'room_id': 'room_1'}
    response = client.post('/', json=payload)
    
    assert response.status_code == 201
    assert response.json['name'] == 'Smart Bulb'

def test_create_device_missing_fields(client):
    response = client.post('/', json={'name': 'Smart Bulb'})
    assert response.status_code == 400

def test_create_device_invalid_room(client):
    payload = {'name': 'Smart Bulb', 'status': 'on', 'room_id': 'invalid_room'}
    response = client.post('/', json=payload)
    assert response.status_code == 400

def test_update_device_success(client):
    response = client.patch