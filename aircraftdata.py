# Using the hexdb.io calls to get data from ICAO hex
# Reference: https://hexdb.io/

import requests


def regis(hex):
    """
    Gets registration from hex
    """
    if hex == None:
        return None
    regis = requests.get(f"https://hexdb.io/hex-reg?hex={hex}")
    if regis.text == "n/a":
        regis.text = "AADEAD"
    return regis.text


def plane(hex):
    """
    Gets plane type from hex
    """
    if hex == None:
        return None
    plane = requests.get(f"https://hexdb.io/hex-type?hex={hex}")
    if plane.text == "n/a":
        plane.text = "AADEAD"
    return plane.text


def oper(hex):
    """
    Gets airline from hex
    """
    if hex == None:
        return None
    oper = requests.get(f"https://hexdb.io/hex-airline?hex={hex}")
    if oper.text == "n/a":
        oper.text = "AADEAD"
    return oper.text


def route(flight):
    """
    Gets route from callsign
    """
    if flight == None:
        return None
    # ICAOroute = requests.get(f"https://hexdb.io/callsign-route?callsign={flight}")
    origin = requests.get(f"https://hexdb.io/callsign-origin_icao?callsign={flight}")
    destination = requests.get(f"https://hexdb.io/callsign-des_icao?callsign={flight}")
    origin_IATA = requests.get(f"https://hexdb.io/icao-iata?icao={origin.text}")
    destination_IATA = requests.get(f"https://hexdb.io/icao-iata?icao={destination.text}")
    origin_name = requests.get(f"https://hexdb.io/icao-airport?icao={origin.text}")
    destination_name = requests.get(f"https://hexdb.io/icao-airport?icao={destination.text}")

    route = origin_IATA.text + "-" + destination_IATA.text + " " + origin_name.text + " to " + destination_name.text
    # route = destination.text + "-" + origin.text
    # print (route)
    if route == "n/a-n/a n/a to n/a":
        route = ""
    return route
