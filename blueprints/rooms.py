import uuid
from flask import Blueprint, request, jsonify
from db import db, save_db

rooms_bp = Blueprint('rooms_bp', __name__)

@rooms_bp.get('/')
def get_rooms():
    # get all rooms stored in db
    return jsonify(db['rooms']), 200

@rooms_bp.get('/<string:room_id>')
def get_room(room_id):
    # check if room exists
    room = None
    for curr_room in db['rooms']:
        if curr_room['id'] == room_id:
            room = curr_room
            break

    if not room:
        return jsonify({'error': 'room not found'}), 404

    # get devices belonging to room
    devices = []
    for device in db['devices']:
        if device['room_id'] == room['id']:
            devices.append(device)

    return jsonify({
        'room': room,
        'devices': devices
    }), 200

@rooms_bp.post('/')
def create_room():
    # verify name header is in request
    req = request.get_json()

    if not req or 'name' not in req:
        return jsonify({'error': 'request missing "name" field'}), 400

    # create new room dictionary
    new_room = {
        'id': uuid.uuid4().hex,
        'name': req['name']
    }

    # add it to db
    db['rooms'].append(new_room)
    save_db()
    
    return jsonify(new_room), 201