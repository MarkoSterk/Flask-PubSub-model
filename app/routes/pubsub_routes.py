from flask import Blueprint, request
from app.controllers.pubsub_controllers import (subscribe_controller,
                                                unsubscribe_controller,
                                                publish_controller)


pubsub_routes = Blueprint('pubsub_routes', __name__)

@pubsub_routes.route('/subscribe/<path:channel>', methods=['POST'])
def subscribe(channel):
    """
    Route for user subscriptions to a specified channel
    Channel name is provided as a url argument
    Calls subscribe_controller function 
    """
    return subscribe_controller(channel)


@pubsub_routes.route('/unsubscribe/<path:channel>', methods=['POST'])
def unsubscribe(channel):
    """
    Route for user unsubscriptions from a specified channel
    Channel name is provided as a url argument
    Calls unsubscribe_controller function 
    """
    return unsubscribe_controller(channel)


@pubsub_routes.route('/publish/<path:channel>', methods=['POST'])
def publish(channel):
    """
    Route for publishing messages to to specified channel
    Channel name is provided as a url argument
    Calls publish_controller function
    """
    return publish_controller(channel)