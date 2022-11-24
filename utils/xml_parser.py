import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs

def parseRSS(xml_object):
    """
    Parses the incomming rss data and extracts all desired values
    Output is a dictionary with keys matching the guid ('guid' tag) of the weather data
    Each key contains another dictionary with the weather data of the place
    (temperature, wind_speed, humidity)
    """

    data = xml_object.decode('utf-8')
    bs_content = bs(data, features="xml")
    items = bs_content.find_all('item')

    items_data = {}
    for item in items:
        item_guid = item.guid.text
        items_data[item_guid] = {}

        items_data[item_guid]['title'] = item.title.text
        items_data[item_guid]['description'] = item.description.text

        items_data[item_guid]['geo:lat'] = float(item.find_all('geo:lat')[0].text)
        items_data[item_guid]['geo:long'] = float(item.find_all('geo:long')[0].text)
        items_data[item_guid]['geo:alt'] = float(item.find_all('geo:alt')[0].text)
    
    return items_data


