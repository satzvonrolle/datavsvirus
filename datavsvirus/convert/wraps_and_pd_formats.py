from lookup_geolocation import get_region_latitude_longitude
from convert_germany import bundesländer_mapping as state_mapping


__all__ = ['clean_up_german_province_name',
           'try_get_region_latitude_longitude',
           'get_lat_from_dict', 'get_lon_from_dict']


state_ending = state_mapping.values()


def clean_up_german_province_name(province_string):
    if province_string.startswith('LK ') or province_string.startswith('SK '): 
        province_string = province_string[3:]

    for st in state_ending:
        if province_string.endswith(st):
            province_string = province_string[:-4]

    return province_string


def try_get_region_latitude_longitude(search_string):
    try:
        return get_region_latitude_longitude(search_string)
    except ValueError:
        return None, None


def get_lat_from_dict(prov_string, lookup_dict):
    return lookup_dict[prov_string][0]

    
def get_lon_from_dict(prov_string, lookup_dict):
    return lookup_dict[prov_string][1]
