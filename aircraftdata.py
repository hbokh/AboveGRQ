# Using the adsbdb.com calls to get data from ICAO hex
# Reference: https://adsbdb.com

import json
import requests


def regis(hex):
    """
    Gets registration from hex
    """
    if hex is None:
        return None
    regis = requests.get(f"https://api.adsbdb.com/v0/aircraft/{hex}")
    data = json.loads(regis.text)
    regis = data['response']['aircraft']['registration']
    print(regis)
    if regis == "unknown aircraft":
        return "n/a"
    return regis


def plane(hex):
    """
    Gets plane type from hex
    """
    if hex is None:
        return None
    plane = requests.get(f"https://api.adsbdb.com/v0/aircraft/{hex}")
    data = json.loads(plane.text)
    type = data['response']['aircraft']['type']
    print(type)
    if type == "unknown aircraft":
        return "n/a"
    return type


def oper(hex):
    """
    Gets airline from hex
    """
    if hex is None:
        return None
    oper = requests.get(f"https://api.adsbdb.com/v0/aircraft/{hex}")
    data = json.loads(oper.text)
    registered_owner = data['response']['aircraft']['registered_owner']
    print(registered_owner)
    if registered_owner == "unknown aircraft":
        return "n/a"
    return registered_owner


def route(flight):
    """
    Gets route from callsign
    """
    if flight is None:
        return None
    route = requests.get(f"https://api.adsbdb.com/v0/callsign/{flight}")
    data = json.loads(route.text)
    origin = data['response']['flightroute']['origin']['name']
    destination = data['response']['flightroute']['destination']['name']
    route = origin + " to " + destination
    print(route)
    if route == "n/a-n/a n/a to n/a":
        return "n/a"
    return route
