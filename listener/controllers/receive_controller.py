from flask import request, jsonify


def receive_controller(channel):
    """
    Receive controller function for receiving messages on the specified channel
    Received the data as json and prints it to the conole.
    Returns a message with status 200
    """
    data = request.get_json()
    print(f'\n-- channel {channel}: {data}')
    return jsonify({
        'status': 'success',
        'message': f'data received successfully from channel {channel}',
        'data': data,
        'code': 200
    }), 200