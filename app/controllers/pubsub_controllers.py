from flask import request, jsonify
from app import pub_sub
from app.controllers.error_controller import app_error, catch_error


@catch_error()
def subscribe_controller(channel: str):
    """
    Controller for user subscriptions to a specified channel
    Channel name is provided as a url argument from the router
    Calls pub_sub subscribe method
    """
    data = request.json
    if 'subscriber_url' not in data:
        return app_error('subscriber_url is a mendatory field', 422)
    return pub_sub.subscribe(channel, data['subscriber_url'])


@catch_error()
def unsubscribe_controller(channel: str):
    """
    Controller for user unsubscriptions from a specified channel
    Channel name is provided as a url argument from the router
    Calls pub_sub unsubscribe method
    """
    data = request.json
    if 'subscriber_url' not in data:
        return app_error('subscriber_url is a mendatory field', 422)
    return pub_sub.unsubscribe(channel, data['subscriber_url'])
    

@catch_error()
def publish_controller(channel: str):
    """
    Controller for publishing messages to a specified channel
    Channel name is provided as a url argument from the router
    Message is provided as a json payload
    Calls pub_sub publish_message method
    """
    data = request.json

    pub_sub.publish_message(channel, data)
    return jsonify({
        'status': 'success',
        'message': f'Message published successfully to channel {channel}',
        'data': data,
        'code': 200
    }), 200
