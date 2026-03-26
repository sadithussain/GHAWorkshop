import pytest
from flask import Flask

from blueprints.rooms import rooms_bp, db 

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(rooms_bp)
    app.config["TESTING"] = True
    
    db['rooms'] = [{'id': 'room_1', 'name': 'Classroom'}]
    db['devices'] = [{'id': 'dev_1', 'name': 'Projector', 'room_id': 'room_1'}]
    
    with app.test_client() as client:
        yield client

def test_get_rooms(client):
    response = client.get('/')
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_get_room_success(client):
    response = client.get('/room_1')
    assert response.status_code == 200
    assert response.json['room']['name'] == 'Classroom'

def test_get_room_not_found(client):
    response = client.get('/does_not_exist')
    assert response.status_code == 404

def test_create_room_success(client):
    response = client.post('/', json={'name': 'Kitchen'})
    assert response.status_code == 201
    assert response.json['name'] == 'Kitchen'

def test_create_room_bad_request(client):
    response = client.post('/', json={'wrong_key': 'Kitchen'})
    assert response.status_code == 400