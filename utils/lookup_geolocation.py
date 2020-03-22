import numpy as np

import urllib.request
import json


__all__ = ['get_region_latitude_longitude']


# Use nominatim of openstreetmaps to access location data
search_url = "https://nominatim.openstreetmap.org/search.php?q={0}&format=json"


def get_region_latitude_longitude(search_string):
    """
    Get the geolocation of given region via nominatim.openstreetmaps.org .
    """
    #TODO: Implement sanity check if region is inside a given country (boundbox)

    # Whitespace and german Umlaute are not allowed
    search_string = search_string.replace(" ", "%20")
    search_string = search_string.replace("ä", "ae")
    search_string = search_string.replace("ö", "oe")
    search_string = search_string.replace("ü", "ue")
    search_string = search_string.replace("ß", "ss")

    # Get most relevant location dataset from the corresponding search_string
    with urllib.request.urlopen(search_url.format(search_string)) as url:
        data = json.loads(url.read().decode())

    # We are looking for administrative region because the case data comes from
    #  administrations. Therefore we look for region boundaries
    locations = [d for d in data \
                 if (d['class'] == 'boundary' or \
                     d['class'] == "place") \
                     and \
                    (d['type'] == 'administrative' or \
                     d['type'] == 'political' or \
                     d['type'] == 'county')]

    # Sort remaining location elements by relevance, use most relevant location
    importances = [l['importance'] for l in locations]
    highest_importance = np.argmax(importances)
    location = locations[highest_importance]

    # Return latitude and longitude
    return eval(location['lat']), eval(location['lon'])
