# Publisher/Subscriber model implementation with Flask
Developed with python 3.11.

## Installation
Requires Python version 3.11.

Create and run a virtual environment with (example)
```
python3.11 -m venv venv
source venv/bin/activate
```
and install all requirements with
```
pip install -r requirements.txt
```

## Main PubSub server app
The main Publisher/Subscriber app is located in the 'app' folder.
It contains basic functionality for a publisher-subscriber service
(subscribe, unsubscribe, publish) for listening or publishing to
specified channels.
It is a Flask instance which is configured with the Config class in the
'app/config.py' file. The config class calls the SECRET_KEY for the app
as an environmental variable. So make sure to set the variable in the
virtual environment 'venv/bin/activate' file with
```
export SECRET_KEY="my-super-secret-key"
```

Don't forget to unset the SECRET_KEY variable in the 'deactivate' part of the
'venv/bin/activate' file with:
```
unset SECRET_KEY
```

#### Endpoints
[POST] '/subscribe/<path:channel>' : Accepts a post request with a json payload
                                    with a 'subscriber_url' field which specifies on which
                                    url the subscriber is available for messages to the specified
                                    channel. The channel is specified as a url argument of any type.
                                    It uses the pub_sub instance of the PubSub class for functionality.

[POST] '/unsubscribe/<path:channel>' : Accepts a post request with a json payload with a 'subscriber_url'
                                        field which specified which url should no longer be used to send messages to.
                                        The exact channel is specified as a url argument of any type.
                                        It uses the pub_sub instance of the PubSub class for functionality.

[POST] '/publish/<path:channel>' : Accepts a post request with a json payload of any structure. The provided 
                                    payload is send to the specified channel. The channel is spcified as a url
                                    argument of any type.
                                    It uses the pub_sub instance of the PubSub class for functionality.
                                    It sends the provided message to subscribers which subscription channel
                                    matches the channel of the publisher

#### PubSub Module
The PubSub module ('app/pubsub/__init__.py' PubSub class object) contains all functionality for the publisher/subscriber model.
The module is registered/initiated with the Flask app and requires the "PUBSUB_MESSAGE_TIMEOUT" config value in the config.py
Config class.

#### Running the main server app
The main application is run with the 'run_server.py' file in the root directory. Make sure you have all requirements installed.
Run the server with:
```
python run_server.py
```
By default it starts on localhost with port 3000 with Debug = False mode


## Publisher
The publisher is a simple script which gets data from the meteo.arso.gov.si rss feed. After parsing the data
it sends [POST] requests to the main app server 'publish/<path:channel>' endpoint for each location in the rss feed data
with the corresponding data as a json payload. There is an arbitrary delay in the post request between 500 ms and 1000 ms.
The data itself is parsed with the 'utils/xml_parser.py' parseRSS function. The returned data from the function is structured
as a nested dictionary. Each key of the dictionary is the parsed data from the 'guid' tag in the rss field (for each item).
This field(s) in turn contain dictionaries with (weather) data for individual items (locations).

After posting data for all locations to the main server app the publisher "sleeps" for 30 seconds. After that it repeats the
process.

The Publisher can be run with:
```
python run_publisher.py
```
Make sure to have all requirements installed.

## Listener
The listener is a seperate Flask server instance which has one purpose: subscribe to a single channel
and then listen for published messages.

The listener server subscribes to the PubSub network (main app server) at startup and then waits for received messages.
The received messages are printed to the console each time they are received. After that they are lost permanently.

The Listener can be run with:
```
python run_listener.py <channel_name>
```

The <channel_name> is an arbitrary string which specifies the desired channel for subscription.
The channel_name is case sensitive.
Don't forget to install all requirements.
#### Example for Listener
Run the following command to get data only for the location CELJE
```
python run_listener.py CELJE
```
Output: only location CELJE

Run the following command to get data for all locations for the date current date
```
python run_listener.py DD.MM
```
Output: all locations for this specific date

Run the following command to get data for all places which contain the letter CE
```
python run_listener.py CE
```
Output: CELJE and CERKLJE
