from flask import request, jsonify


def receive_controller(channel):
    data = request.get_json()
    print(f'\n-- channel {channel}: {data}')
    return jsonify({
        'status': 'success',
        'message': f'data received successfully from channel {channel}',
        'data': data,
        'code': 200
    }), 200