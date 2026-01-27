"""
Pytest configuration and shared fixtures for AboveGRQ tests.
"""

import pytest
from datetime import datetime
from configparser import ConfigParser
import shutil
import os


def pytest_configure(config):
    """
    Pytest hook that runs before test collection.
    Creates config.ini from test-config.ini for modules that load config at import time.
    """
    test_config_path = "tests/test-config.ini"
    config_path = "config.ini"

    # Only create config.ini if it doesn't exist
    if not os.path.exists(config_path):
        shutil.copy2(test_config_path, config_path)
        # Mark that we created it so we can clean up later
        config._test_config_created = True
    else:
        config._test_config_created = False


def pytest_unconfigure(config):
    """
    Pytest hook that runs after all tests complete.
    Removes the test config.ini if we created it.
    """
    if getattr(config, "_test_config_created", False):
        config_path = "config.ini"
        if os.path.exists(config_path):
            os.remove(config_path)


@pytest.fixture
def receiver_coords():
    """
    Fixture providing receiver coordinates from test-config.ini.
    Returns tuple of (latitude, longitude).
    """
    parser = ConfigParser()
    parser.read("tests/test-config.ini")
    lat = float(parser.get("receiver", "latitude"))
    lon = float(parser.get("receiver", "longitude"))
    return (lat, lon)


@pytest.fixture
def mock_aircraft_data():
    """
    Fixture providing bogus aircraft data for testing.
    Returns a dictionary mimicking dump1090 aircraft.json format.
    """
    return {
        "now": 1706360400.0,  # Unix timestamp
        "messages": 12345678,
        "aircraft": [
            {
                "hex": "abc123",
                "squawk": "7000",
                "flight": "KLM1234 ",
                "lat": 53.3,
                "lon": 6.6,
                "altitude": 15000,
                "vert_rate": -1024,
                "track": 270,
                "speed": 350,
                "messages": 150,
                "seen": 0.5,
                "rssi": -25.5,
            },
            {
                "hex": "def456",
                "squawk": "1200",
                "flight": "TRA567  ",
                "lat": 53.25,
                "lon": 6.55,
                "altitude": 3500,
                "vert_rate": 0,
                "track": 45,
                "speed": 180,
                "messages": 89,
                "seen": 1.2,
                "rssi": -18.3,
            },
            {
                "hex": "789xyz",
                "squawk": "2000",
                "flight": "BAW888  ",
                "lat": 53.4,
                "lon": 6.7,
                "altitude": 35000,
                "vert_rate": 128,
                "track": 135,
                "speed": 520,
                "messages": 234,
                "seen": 2.1,
                "rssi": -30.2,
            },
            {
                # Aircraft without position data (should be skipped)
                "hex": "nopos1",
                "squawk": "7700",
                "flight": "EMG999  ",
                "messages": 45,
                "seen": 0.8,
                "rssi": -22.0,
            },
        ],
    }


@pytest.fixture
def mock_vrs_data():
    """
    Fixture providing bogus VRS (Virtual Radar Server) data for testing.
    """
    return {
        "acList": [
            {
                "Icao": "abc123",
                "Sqk": "7000",
                "Call": "KLM1234",
                "Lat": 53.3,
                "Long": 6.6,
                "Alt": 15000,
                "Vsi": -1024,
                "Trak": 270,
                "Spd": 350,
                "Sig": 150,
            },
            {
                "Icao": "def456",
                "Sqk": "1200",
                "Call": "TRA567",
                "Lat": 53.25,
                "Long": 6.55,
                "Alt": 3500,
                "Vsi": 0,
                "Trak": 45,
                "Spd": 180,
                "Sig": 89,
            },
        ],
        "stm": 1706360400000,  # Milliseconds
    }


@pytest.fixture
def mock_http_responses():
    """
    Fixture providing mock HTTP responses for hexdb.io API calls.
    """
    return {
        "hex-reg": {
            "abc123": "PH-BXA",
            "def456": "PH-HZD",
            "789xyz": "G-EUUU",
            "unknown": "n/a",
        },
        "hex-type": {
            "abc123": "Boeing 737-800",
            "def456": "Boeing 737-700",
            "789xyz": "Airbus A320",
            "unknown": "n/a",
        },
        "hex-airline": {
            "abc123": "KLM Royal Dutch Airlines",
            "def456": "Transavia",
            "789xyz": "British Airways",
            "unknown": "n/a",
        },
        "callsign-origin_icao": {
            "KLM1234": "EHAM",
            "TRA567": "EHAM",
            "BAW888": "EGLL",
        },
        "callsign-des_icao": {
            "KLM1234": "KJFK",
            "TRA567": "LEPA",
            "BAW888": "EGCC",
        },
        "icao-iata": {
            "EHAM": "AMS",
            "KJFK": "JFK",
            "LEPA": "PMI",
            "EGLL": "LHR",
            "EGCC": "MAN",
        },
        "icao-airport": {
            "EHAM": "Amsterdam Schiphol",
            "KJFK": "John F. Kennedy Intl",
            "LEPA": "Palma de Mallorca",
            "EGLL": "London Heathrow",
            "EGCC": "Manchester",
        },
    }


@pytest.fixture
def sample_datetime():
    """
    Fixture providing a consistent datetime for testing.
    """
    return datetime(2024, 1, 27, 14, 30, 0)


@pytest.fixture
def mock_config():
    """
    Fixture providing a mock configuration parser for testing.
    """
    config = ConfigParser()
    config.add_section("receiver")
    config.set("receiver", "latitude", "53.215119")
    config.set("receiver", "longitude", "6.570963")

    config.add_section("aboveme")
    config.set("aboveme", "distance_alarm", "2")
    config.set("aboveme", "elevation_alarm", "75")
    config.set("aboveme", "wait_x_updates", "3")
    config.set("aboveme", "sleep_time", "1")
    config.set("aboveme", "image_width", "1280")
    config.set("aboveme", "image_height", "1024")
    config.set("aboveme", "wait_time", "2")
    config.set("aboveme", "request_timeout", "60")
    config.set("aboveme", "driver", "dump1090")
    config.set("aboveme", "data_url", "http://localhost/aircraft.json")
    config.set("aboveme", "map_url", "http://localhost/tar1090/")
    config.set("aboveme", "map_params_screenshot", "&iconscale=1S")

    config.add_section("tweet")
    config.set(
        "tweet",
        "tweet_template",
        "${flight}: ${dist_km} km away @ ${alt_m} m, heading ${heading}",
    )
    config.set("tweet", "default_hashtags", "#TestHashtag #ADSB")

    config.add_section("bsky")
    config.set("bsky", "handle", "test.bsky.social")
    config.set("bsky", "password", "testpassword")

    config.add_section("crop")
    config.set("crop", "do_crop", "True")
    config.set("crop", "crop_x", "0")
    config.set("crop", "crop_y", "0")
    config.set("crop", "crop_width", "780")
    config.set("crop", "crop_height", "800")

    config.add_section("apps")
    config.set("apps", "driver_path", "/usr/local/bin/geckodriver")
    config.set("apps", "browser_path", "/usr/bin/firefox")

    return config
