from .lookup_geolocation import get_region_latitude_longitude


__all__ = ['clean_up_german_province_name_for_geoloc_lookup',
           'try_get_region_latitude_longitude',
           'get_lat_from_dict', 'get_lon_from_dict']


def clean_up_german_province_name_for_geoloc_lookup(province_string):
    if province_string.startswith('LK ') or province_string.startswith('SK '): 
        province_string = province_string[3:]

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

