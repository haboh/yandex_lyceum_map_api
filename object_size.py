import requests


def get_dlan_dlat(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "geocode": toponym_to_find,
        "format": "json",
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        raise Exception()

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

    lower_corner = toponym['boundedBy']['Envelope']['lowerCorner']
    upper_corner = toponym['boundedBy']['Envelope']['upperCorner']
    lan1, lat1 = map(float, lower_corner.split())
    lan2, lat2 = map(float, upper_corner.split())
    return abs(lan1 - lan2), abs(lat1 - lat2)
