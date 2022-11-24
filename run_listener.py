from listener import create_app
import sys
import random

DEBUG = False
receive_url = 'http://localhost'
receive_port = random.randint(3001, 9000)
url = 'http://localhost:3000/subscribe'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please provide a channel to subscribe to.')
    elif len(sys.argv) > 2:
        print('Please provide only one channel to subscribe to.')
    else:
        channel = sys.argv[1]
        listener = create_app(receive_url, receive_port, url, channel)
        listener.run('0.0.0.0', port = receive_port, debug = DEBUG)