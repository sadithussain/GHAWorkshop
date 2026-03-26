import uuid
from flask import Blueprint, request, jsonify
from db import db, save_db

devices_bp = Blueprint('devices_bp', __name__)

@devices_bp.get('/')
def get_devices():
    # get all devices stored in db
    return jsonify(db['devices']), 200

@devices_bp.get('/<string:device_id>')
def get_device(device_id):
    # check if device with id exists in database
    device = None
    for curr_device in db['devices']:
        if curr_device['id'] == device_id:
            device = curr_device
            break

    if not device:
        return jsonify({'error': 'device not found'}), 404

    return jsonify(device), 200

@devices_bp.post('/')
def create_device():
    # verify that the request gave us a name, status, and room_id
    req = request.get_json()

    if not req or 'name' not in req or 'status' not in req or 'room_id' not in req:
        return jsonify({'error': 'request missing "name", "status", and/or "room_id" fields'}), 400

    # verify that the room_id exists in our database
    found = False
    for room in db['rooms']:
        if room['id'] == req['room_id']:
            found = True
            break

    if not found:
        return jsonify({'error': f'room with id {req["room_id"]} not found'}), 400

    # create a dictionary of the new device, with a unique id
    new_device = {
        'id': uuid.uuid4().hex,
        'name': req['name'],
        'status': req['status'],
        'room_id': req['room_id']
    }

    # add the device to the list of devices
    db['devices'].append(new_device)
    save_db()

    # return the new device in our request
    return jsonify(new_device), 201

@devices_bp.patch('/<string:device_id>')
def update_device_status(device_id):
    # verify that the request gave us a status
    req = request.get_json()

    if not req or 'status' not in req:
        return jsonify({'error': 'request missing "status" field'}), 400

    # verify that the device with device_id exists in our dictionary
    device = None
    for curr_device in db['devices']:
        if curr_device['id'] == device_id:
            device = curr_device
            break
    
    if not device:
        return jsonify({'error': f'device with id {device_id} not found'}), 400

    # update the device status with the given status
    device['status'] = req['status']

    # return the entire updated device
    return jsonify(device), 200

@devices_bp.delete('/<string:device_id>')
def delete_device(device_id):
    # verify that the device with device_id exists
    device = None
    for curr_device in db['devices']:
        if curr_device['id'] == device_id:
            device = curr_device
            break

    if not device:
        return jsonify({'error': f'device with id {device_id} not found'}), 404

    # remove the device from the db, can be done by:
    # - .remove on the devices list (with the entire dictionary object)
    # - rebuilding the list without the excluded device
    db['devices'].remove(device)

    # return that we have deleted the device
    return jsonify(), 204
