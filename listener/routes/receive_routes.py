from flask import Blueprint
from listener.controllers.receive_controller import receive_controller

receive_routes = Blueprint('receive_routes', __name__)

@receive_routes.route('/receive/<path:channel>', methods = ['POST'])
def receive(channel):
    """
    Route for receiving messages from the specified channel
    """
    return receive_controller(channel)