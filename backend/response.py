from flask import make_response, jsonify

def make_json_response(body, status):
    return jsonify({'data': body, 'status': status })

def unsupported_method():
    return make_json_response("Request type not supported", 400)