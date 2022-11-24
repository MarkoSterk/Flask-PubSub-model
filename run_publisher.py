import time
import requests
from utils.xml_parser import parseRSS
from concurrent.futures import ThreadPoolExecutor

##url for latest weather observations on meteo.arso.gov.si for all available places
#url = 'https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/en/observation_si_latest.xml'
url = 'https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/en/observation_si_latest.rss'
pubsub_base_url = 'http://localhost:3000/publish'


def publisher():
    """
    To run execute the command "python publisher.py" in your cli
    
    Fetches latest weather observation data from meteo.arso.gov.si (url) for all available places every 30 seconds.
    After parsing the data it publishes the data for each place to its own channel (channel_name = place_name)

    Uses the ThreadPoolExecutor for concurrent publishing of messages on different channels (multithreading)

    Loop runs continously until interrupted with "Ctrl + C"
    """
    def publish_message(pubsub_base_url, channel, data):
        publish_url = f'{pubsub_base_url}/{channel}'
        try:
            requests.post(publish_url, json = data, timeout = 10.0)
        except requests.Timeout:
            print('PubSub network is not responding')
        except requests.ConnectionError:
            print('PubSub network appears to be down')

    while True:
        response = requests.get(url)
        items_data = parseRSS(response.content)
        with ThreadPoolExecutor(max_workers=5) as executor:
            for item in items_data:
                executor.submit(publish_message, pubsub_base_url, item, items_data[item])
        time.sleep(30)

if __name__ == '__main__':
    publisher()