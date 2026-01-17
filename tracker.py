#
# tracker.py
#
# kevinabrandon@gmail.com
#

import sys
import traceback
import time
from time import sleep
from configparser import ConfigParser
from string import Template
from atproto import Client, models

import datasource
import fa_api
import geomath
import aircraftdata

# Read the configuration file for this application.
parser = ConfigParser()
parser.read("config.ini")

# Assign AboveTustin variables.
abovetustin_distance_alarm = float(
    parser.get("abovetustin", "distance_alarm")
)  # The alarm distance in miles.
abovetustin_elevation_alarm = float(
    parser.get("abovetustin", "elevation_alarm")
)  # The angle in degrees that indicates if the airplane is overhead or not.
abovetustin_wait_x_updates = int(
    parser.get("abovetustin", "wait_x_updates")
)  # Number of updates to wait after the airplane has left the alarm zone before posting.
abovetustin_sleep_time = float(
    parser.get("abovetustin", "sleep_time")
)  # Time between each loop.

# Assign FlightAware variables.
fa_enable = parser.getboolean("flightaware", "fa_enable")
fa_username = parser.get("flightaware", "fa_username")
fa_api_key = parser.get("flightaware", "fa_api_key")

# Bluesky
bsky_handle = parser.get("bsky", "handle")
bsky_password = parser.get("bsky", "password")

crop_width = parser.getint("crop", "crop_width")
crop_height = parser.getint("crop", "crop_height")


# Given an aircraft 'a' post / skeet.
# If we have a screenshot, upload it with the post.
def Post(a, havescreenshot):
    # compile the template arguments
    templateArgs = dict()
    flight = a.flight or a.hex
    flight = flight.replace(" ", "")
    templateArgs["flight"] = flight
    templateArgs["icao"] = a.hex
    templateArgs["icao"] = templateArgs["icao"].replace(" ", "")
    templateArgs["regis"] = aircraftdata.regis(a.hex)
    templateArgs["plane"] = aircraftdata.plane(a.hex)
    templateArgs["oper"] = aircraftdata.oper(a.hex)
    templateArgs["route"] = aircraftdata.route(flight)
    templateArgs["dist_mi"] = "%.1f" % a.distance
    templateArgs["dist_km"] = "%.1f" % geomath.mi2km(a.distance)
    templateArgs["dist_nm"] = "%.1f" % geomath.mi2nm(a.distance)
    templateArgs["alt_ft"] = a.altitude
    templateArgs["alt_m"] = "%.1f" % geomath.ft2m(a.altitude)
    templateArgs["el"] = "%.1f" % a.el
    templateArgs["az"] = "%.1f" % a.az
    templateArgs["heading"] = geomath.HeadingStr(a.track)
    templateArgs["speed_mph"] = "%.1f" % a.speed
    templateArgs["speed_kmph"] = "%.1f" % geomath.mi2km(a.speed)
    templateArgs["speed_kts"] = "%.1f" % geomath.mi2nm(a.speed)
    templateArgs["time"] = a.time.strftime("%H:%M:%S")
    templateArgs["squawk"] = a.squawk
    templateArgs["vert_rate_ftpm"] = a.vert_rate
    templateArgs["vert_rate_mpm"] = "%.1f" % geomath.ft2m(a.vert_rate)
    templateArgs["rssi"] = a.rssi
    if fa_enable and faInfo:
        templateArgs["orig_name"] = faInfo["orig_name"]
        templateArgs["dest_name"] = faInfo["dest_name"]
        if faInfo["orig_alt"]:
            templateArgs["orig_alt"] = faInfo["orig_alt"]
        else:
            templateArgs["orig_alt"] = faInfo["orig_code"]
        if faInfo["dest_alt"]:
            templateArgs["dest_alt"] = faInfo["dest_alt"]
        else:
            templateArgs["dest_alt"] = faInfo["dest_code"]
        if faInfo["dest_city"]:
            templateArgs["dest_city"] = faInfo["dest_city"]
        if faInfo["orig_city"]:
            templateArgs["orig_city"] = faInfo["orig_city"]
        if templateArgs["orig_alt"] and templateArgs["dest_alt"]:
            tweet = Template(parser.get("tweet", "fa_tweet_template")).substitute(
                templateArgs
            )
        else:
            tweet = Template(parser.get("tweet", "tweet_template")).substitute(
                templateArgs
            )
    else:
        tweet = Template(parser.get("tweet", "tweet_template")).substitute(templateArgs)
    # conditional hashtags:
    hashtags = []
    if (
        a.time.hour < 6
        or a.time.hour >= 22
        or (a.time.weekday() == 6 and a.time.hour < 8)
    ):
        hashtags.append(" #AfterHours")
    if a.altitude < 1000:
        hashtags.append(" #LowFlier")
    # This one depends on the relative location of a possible nearby airport.
    # a.altitude >= 1000 and a.altitude < 2500 and (templateArgs["heading"] == "S" or templateArgs["heading"] == "SW")
    if 3800 <= a.altitude < 8500 and templateArgs.get("heading") == "NE":
        hashtags.append(" #ProbablyLanding")
    if a.altitude > 20000 and a.altitude < 35000:
        hashtags.append(" #UpInTheClouds")
    if a.altitude >= 35000:
        hashtags.append(" #WayTheHeckUpThere")
    if a.speed > 300 and a.speed < 500:
        hashtags.append(" #MovingQuickly")
    if a.speed >= 500 and a.speed < 770:
        hashtags.append(" #FlyingFast")
    if a.speed >= 700:
        hashtags.append(" #SpeedDemon")
    if a.speed >= 1:
        hashtags.append(" #AboveGRQ")  # Change me!

    # add the conditional hashtags as long as there is room in 300 chars
    for hash in hashtags:
        if len(tweet) + len(hash) <= 300:
            tweet += hash

    # add the default hashtags as long as there is room
    # for hash in parser.get("tweet", "default_hashtags").split(" "):
    #    if len(tweet) + len(hash) <= 300:
    #        tweet += " " + hash

    print(tweet)

    # Send to Bluesky
    # Reference: https://github.com/MarshalX/atproto/blob/main/examples/send_image.py
    if havescreenshot:
        pass
    client = Client()
    client.login(bsky_handle, bsky_password)

    # Define your post text with multiple hashtags
    post_text = tweet

    # Encode the text to UTF-8 to calculate byte positions
    utf8_text = post_text.encode("utf-8")

    # List of hashtags to include
    hashtags = hashtags

    # Initialize an empty list to hold facets
    facets = []

    # Calculate byte positions and create a facet for each hashtag
    for hashtag in hashtags:
        hashtag_bytes = hashtag.encode("utf-8")
        start = utf8_text.find(hashtag_bytes)
        end = start + len(hashtag_bytes)
        facet = {
            "index": {
                "byteStart": start,
                "byteEnd": end,
            },
            "features": [
                {
                    "$type": "app.bsky.richtext.facet#tag",
                    "tag": hashtag[2:],  # Exclude the '#' symbol
                }
            ],
        }
        facets.append(facet)

    # replace the path to your image file
    with open("screenshot.png", "rb") as f:
        img_data = f.read()

    # Add image aspect ratio to prevent default 1:1 aspect ratio
    # Replace with your desired aspect ratio
    aspect_ratio = models.AppBskyEmbedDefs.AspectRatio(
        height=crop_height, width=crop_width
    )

    client.send_image(
        text=tweet,
        facets=facets,
        image=img_data,
        image_alt="No ALT text available...",
        image_aspect_ratio=aspect_ratio,
    )


if __name__ == "__main__":
    lastReloadTime = time.time()
    display = datasource.get_map_source()
    alarms = dict()  # dictonary of all aircraft that have triggered the alarm
    # Indexed by it's hex code, each entry contains a tuple of
    # the aircraft data at the closest position so far, and a
    # counter.  Once the airplane is out of the alarm zone,
    # the counter is incremented until we hit [abovetustin_wait_x_updates]
    # (defined above), at which point we then Tweet

    fd = datasource.get_data_source()
    lastTime = fd.time

    while True:
        if time.time() > lastReloadTime + 3600 and len(alarms) == 0:
            print("One hour since last browser reload... reloading now")
            display.reload()
            lastReloadTime = time.time()

        sleep(abovetustin_sleep_time)
        fd.refresh()
        if fd.time == lastTime:
            continue
        lastTime = fd.time

        print("Now: {}".format(fd.time))

        current = dict()  # current aircraft inside alarm zone

        # loop on all the aircarft in the receiver
        for a in fd.aircraft:
            # if they don't have lat/lon or a heading skip them
            if a.lat is None or a.lon is None or a.track is None:
                continue
            # check to see if it's in the alarm zone:
            if (
                a.distance < abovetustin_distance_alarm
                or a.el > abovetustin_elevation_alarm
            ):
                # add it to the current dictionary
                current[a.hex] = a
                print(
                    "{}: {}mi, {}az, {}el, {}alt, {}dB, {}seen".format(
                        a.ident_desc(),
                        "%.1f" % a.distance,
                        "%.1f" % a.az,
                        "%.1f" % a.el,
                        a.altitude,
                        "%0.1f" % a.rssi,
                        "%.1f" % (a.seen or 0),
                    )
                )
                if a.hex in alarms:
                    # if it's already in the alarms dict, check to see if we're closer
                    if a.distance < alarms[a.hex][0].distance:
                        # if we're closer than the one already there, then overwrite it
                        alarms[a.hex] = (a, 0)
                else:
                    # add it to the alarms
                    alarms[a.hex] = (a, 0)

        finishedalarms = []
        # loop on all the aircraft in the alarms dict
        for h, a in alarms.items():
            found = False
            # check to see if it's in the current set of aircraft
            for h2, a2 in current.items():
                if h2 == h:
                    print(
                        "{} not yet, dist, elv: {}, {}".format(
                            h, "%.1f" % a[0].distance, "%.1f" % a[0].el
                        )
                    )
                    found = True
                    break
            # if it wasn't in the current set of aircraft, that means it's time to post!
            if not found:
                if a[1] < abovetustin_wait_x_updates:
                    alarms[h] = (a[0], a[1] + 1)
                else:
                    havescreenshot = False
                    if display is not None:
                        print("Time to create screenshot of {}:".format(a[0]))
                        hexcode = a[0].hex
                        hexcode = hexcode.replace(" ", "")
                        hexcode = hexcode.replace("~", "")
                        havescreenshot = display.clickOnAirplane(hexcode)
                    if fa_enable:
                        print("Getting FlightAware flight details")
                        faInfo = fa_api.FlightInfo(a[0].flight, fa_username, fa_api_key)
                    else:
                        faInfo = False

                    print("Time to post!")

                    try:
                        Post(a[0], havescreenshot)
                    except Exception:
                        print("Exception in Post():")
                        traceback.print_exc()
                    finishedalarms.append(a[0].hex)

        # for each alarm that is finished, delete it from the dictionary
        for h in finishedalarms:
            del alarms[h]

        # flush output for following in log file
        sys.stdout.flush()
