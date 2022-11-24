from flask import jsonify
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import random
from app.controllers.error_controller import app_error

class PubSub(object):
    """
    Publisher/Subscriber module which handles all functionality for
    subscribing users and publishing messages by users.
    """
    def __init__(self, app = None):
        if app:
            self.init_app(app)


    def init_app(self, app):
        """
        Configures pubsub module with application configurations
        """
        for key, value in app.config.items():
            if key.startswith('PUBSUB_'):
                setattr(self, key, value)
        if 'PUBSUB_MESSAGE_TIMEOUT' not in dir(self):
            raise Exception('Missing PubSub configuration values')
        self.channel_subscribers = {}
    

    @staticmethod
    def success_response(msg, data, code = 200, status = 'success'):
        return jsonify({
            'status': status,
            'message': msg,
            'data': data,
            'code': code
        }), code


    def add_channel(self, channel):
        self.channel_subscribers[channel] = []


    def delete_channel(self, channel):
        del self.channel_subscribers[channel]


    def subscribe(self, channel, subscriber_url):
        if channel not in self.channel_subscribers:
            self.add_channel(channel)
        
        if subscriber_url in self.channel_subscribers[channel]:
            return app_error('You are already subscribed to this channel', 303, 'error')
        
        self.channel_subscribers[channel].append(subscriber_url)
        return self.success_response(f'Successfully subscribed to channel {channel}', subscriber_url)

    
    def unsubscribe(self, channel, subscriber_url):
        if channel not in self.channel_subscribers:
            return app_error('This channel does not exist', 400, 'error')
        if subscriber_url not in self.channel_subscribers[channel]:
            return app_error('You are not subscribed to this channel', 303, 'error')

        self.channel_subscribers[channel].remove(subscriber_url)
        if len(self.channel_subscribers[channel]) == 0:
            self.delete_channel(channel)

        return self.success_response(f'Successfully unsubscribed from channel {channel}', subscriber_url)

    
    def unsubscribe_all(self, subscriber_url):
        subscriber_in = []
        for channel in self.channel_subscribers:
            if subscriber_url in self.channel_subscribers[channel]:
                subscriber_in.append(channel)

        for channel in subscriber_in:
            self.channel_subscribers[channel].remove(subscriber_url)

            if len(self.channel_subscribers[channel]) == 0:
                self.delete_channel(channel)
        
        return self.success_response(f'Successfully unsubscribed from: {subscriber_in}', subscriber_url)
    

    def publish_message(self, channel, msg):

        def publish(subscriber, msg, timeout):
            time.sleep(random.uniform(0.5, 1.0))
            requests.post(subscriber, json = msg, timeout=timeout)

        if channel not in self.channel_subscribers:
            self.add_channel(channel)

        with ThreadPoolExecutor(max_workers=5) as executor:
            for existing_channel in self.channel_subscribers:
                if str(existing_channel) in str(channel): 
                    for subscriber in self.channel_subscribers[existing_channel]:
                        executor.submit(publish, subscriber, msg, self.PUBSUB_MESSAGE_TIMEOUT)