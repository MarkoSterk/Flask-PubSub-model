from flask import Flask
from werkzeug.exceptions import default_exceptions

from app.config import Config
from app.pubsub import PubSub
from app.controllers.error_controller import error_response

pub_sub = PubSub()

def create_app(config_class: object = Config):
    """
    Instatiates and configures the Flask app with the config_class object
    Adds all extansions and blueprints
    """
    app = Flask(__name__) #instatiates the main app class
    app.config.from_object(config_class) #configures app from config object

    #initiates app extensions
    pub_sub.init_app(app)

    #registers blueprint to the application
    from app.routes.pubsub_routes import pubsub_routes
    app.register_blueprint(pubsub_routes)

    for ex in default_exceptions:
        #Registers the error_response function for all default exceptions.
        app.register_error_handler(ex, error_response)

    return app