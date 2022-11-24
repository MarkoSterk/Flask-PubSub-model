import os


class Config:
    '''
    Contains all configurations for Flask app.
    '''
    SECRET_KEY = os.environ["SECRET_KEY"] ###secret key of application
    PUBSUB_MESSAGE_TIMEOUT = 5.0 #5.0 seconds for timeout after sent message. Can be changed