from flask import Flask
from threading import Thread

def create_app(receive_url, receive_port, url, channel):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret-listener-app-key'

    from listener.routes.receive_routes import receive_routes
    app.register_blueprint(receive_routes)

    from listener.controllers.subscribe_controller import subscribe_controller
    # subscribe_controller(receive_url, receive_port, url, channel)
    Thread(target = subscribe_controller, args=[receive_url, receive_port, url, channel]).start()

    return app
