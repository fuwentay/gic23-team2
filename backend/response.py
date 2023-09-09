from flask import make_response, jsonify

def make_json_response(body, status):
    return jsonify({'data': body, 'status': status })