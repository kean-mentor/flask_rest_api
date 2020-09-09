from flask import Blueprint, current_app, jsonify, request

from utils import storage


simple_api = Blueprint('simple_api', __name__)


@simple_api.route('/values', methods=['GET'])
def get_all():
    if 'prefix' in request.args:
        prefix = request.args['prefix']
        result = []

        for k, v in storage.items():
            if v.startswith(prefix):
                result.append(k)
        return jsonify(result), 200

    return jsonify(storage.get_all()), 200

@simple_api.route('/values', methods=['POST'])
def add():
    if request.json:
        if 'key' not in request.json:
            return jsonify({'message': "ERR: 'key' is a required parameter"}), 400
        if 'value' not in request.json:
            return jsonify({'message': "ERR: 'value' is a required parameter"}), 400

        key = request.json['key']
        value = request.json['value']

        if key in storage:
            message, status_code = 'Item successfully updated', 200
        else:
            message, status_code = 'Item successfully created', 201
        storage[key] = value
        return jsonify({'message': message}), status_code

    else:
        return jsonify({'message': 'ERR: Missing data'}), 400


@simple_api.route('/values/<string:key>', methods=['GET'])
def get_by_key(key):
    if key in storage:
        return jsonify(storage[key]), 200

    return jsonify({'message': 'Key not found!'}), 404

@simple_api.route('/values/<string:key>', methods=['DELETE'])
def delete_by_key(key):
    if key in storage:
        del storage[key]
        return jsonify({'message': 'Item successfully deleted'}), 200

    return jsonify({'message': 'Key not found!'}), 404
