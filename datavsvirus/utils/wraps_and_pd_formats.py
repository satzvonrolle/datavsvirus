from datavsvirus.utils.lookup_geolocation import get_region_latitude_longitude


__all__ = ['clean_up_german_province_name',
           'try_get_region_latitude_longitude',
           'get_lat_from_dict', 'get_lon_from_dict', 
           'state_mapping', 'switzerland_abbrev_mapping']


state_mapping = {
    'Baden-Württemberg': 'BW',
    'Bayern': 'BY',
    'Berlin': 'BE',
    'Brandenburg': 'BB',
    'Bremen': 'HB',
    'Hamburg': 'HH',
    'Hessen': 'HE',
    'Mecklenburg-Vorpommern': 'MV',
    'Niedersachsen': 'NI',
    'Nordrhein-Westfalen': 'NW',
    'Rheinland-Pfalz': 'RP',
    'Saarland': 'SL',
    'Sachsen': 'SN',
    'Sachsen-Anhalt': 'ST',
    'Schleswig-Holstein': 'SH',
    'Thüringen': 'TH'}

state_ending = state_mapping.values()


switzerland_abbrev_mapping = {
    "ZH": "Zürich",
    "BE": "Bern",
    "LU": "Luzern",
    "UR": "Uri",
    "SZ": "Schwyz",
    "OW": "Obwalden",
    "NW": "Nidwalden",
    "GL": "Glarus",
    "ZG": "Zug",
    "FR": "Fribourg",
    "SO": "Solothurn",
    "BS": "Basel-Stadt",
    "BL": "Basel-Landschaft",
    "SH": "Schaffhausen",
    "AR": "Appenzell Ausserrhoden",
    "AI": "Appenzell Innerrhoden",
    "SG": "Sankt Gallen",
    "GR": "Graubünden",
    "AG": "Aargau",
    "TG": "Thurgau",
    "TI": "Tessin",
    "VD": "Waadt",
    "VS": "Wallis",
    "NE": "Neuenburg",
    "GE": "Genf",
    "JU": "Jura"}


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
