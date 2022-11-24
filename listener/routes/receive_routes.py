from flask import Blueprint
from listener.controllers.receive_controller import receive_controller

receive_routes = Blueprint('receive_routes', __name__)

@receive_routes.route('/receive/<string:channel>', methods = ['POST'])
def receive(channel):
    return receive_controller(channel)