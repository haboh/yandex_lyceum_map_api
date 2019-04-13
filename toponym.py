import requests


class NotFoundError(Exception):
    pass


# ----------------- Toponym search ----------------------------------


def find_toponym_coordinates(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "geocode": toponym_to_find,
        "format": "json",
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        raise Exception()

    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except IndexError:
        raise NotFoundError()
    toponym_coodrinates = toponym["Point"]["pos"]
    return list(map(float, toponym_coodrinates.split()))


# -------------------------------------------------------------------


# -------------- Find the district by coordinates -------------------
def find_district_by_coordinates(coordinates):
    geocode_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {
        'geocode': ','.join(map(str, coordinates)),
        'kind': 'district',
        'format': 'json',
    }
    response = requests.get(geocode_url, params=params)
    if not response:
        raise Exception()
    return response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['text']
# -------------------------------------------------------------------
