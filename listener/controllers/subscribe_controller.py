from flask import request
import requests
import sys

def subscribe_controller(receive_url, receive_port, url, channel):
    """
    subscribe_controller function which subscribes the Listener to the specified channel
    """

    full_url = f'{url}/{channel}'
    full_receive_url = f'{receive_url}:{receive_port}/receive/{channel}'
    data = {
        'subscriber_url': full_receive_url
    }
    try:
        res = requests.post(full_url, json = data, timeout=4.0)
        res = res.json()
        print(f'\n-- {res["message"]} [{res["code"]}]')
    except Exception as e:
        print(f"""
        Failed to subscribe to channel {channel}.
        PubSub network appears to be down.
        Shutdown listener with 'ctrl + C' and restart.
        """)

