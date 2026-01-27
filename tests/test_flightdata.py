"""
Tests for flightdata.py - flight data parsing and aircraft data structures.

Uses mock aircraft data to avoid network dependencies.
"""

from unittest.mock import patch, MagicMock
from datetime import datetime
import json
import flightdata


class TestAircraftData:
    """Tests for AircraftData class."""

    def test_aircraft_data_creation(self, sample_datetime):
        """Test creating an AircraftData object."""
        aircraft = flightdata.AircraftData(
            dhex="abc123",
            squawk="7000",
            flight="KLM1234",
            registration="PH-BXA",
            lat=53.3,
            lon=6.6,
            altitude=15000,
            vert_rate=-1024,
            track=270,
            speed=350,
            messages=150,
            seen=0.5,
            mlat=False,
            nucp=7,
            seen_pos=1.0,
            rssi=-25.5,
            dist=10.5,
            az=180,
            el=45,
            time=sample_datetime,
        )

        assert aircraft.hex == "abc123"
        assert aircraft.squawk == "7000"
        assert aircraft.flight == "KLM1234"
        assert aircraft.registration == "PH-BXA"
        assert aircraft.lat == 53.3
        assert aircraft.lon == 6.6
        assert aircraft.altitude == 15000
        assert aircraft.vert_rate == -1024
        assert aircraft.track == 270
        assert aircraft.speed == 350
        assert aircraft.distance == 10.5
        assert aircraft.az == 180
        assert aircraft.el == 45

    def test_aircraft_str_representation(self, sample_datetime):
        """Test string representation of aircraft."""
        aircraft = flightdata.AircraftData(
            dhex="abc123",
            squawk="7000",
            flight="KLM1234",
            registration="PH-BXA",
            lat=53.3,
            lon=6.6,
            altitude=15000,
            vert_rate=-1024,
            track=270,
            speed=350,
            messages=150,
            seen=0.5,
            mlat=False,
            nucp=7,
            seen_pos=1.0,
            rssi=-25.5,
            dist=10.5,
            az=180,
            el=45,
            time=sample_datetime,
        )

        str_repr = str(aircraft)
        assert "AircraftData" in str_repr
        assert "10.5" in str_repr  # distance
        assert "45" in str_repr  # elevation

    def test_ident_desc_full(self, sample_datetime):
        """Test ident_desc() with all identifiers."""
        aircraft = flightdata.AircraftData(
            dhex="abc123",
            squawk="7000",
            flight="KLM1234",
            registration="PH-BXA",
            lat=53.3,
            lon=6.6,
            altitude=15000,
            vert_rate=0,
            track=270,
            speed=350,
            messages=150,
            seen=0.5,
            mlat=False,
            nucp=7,
            seen_pos=1.0,
            rssi=-25.5,
            dist=10.5,
            az=180,
            el=45,
            time=sample_datetime,
        )

        ident = aircraft.ident_desc()
        assert "abc123" in ident
        assert "PH-BXA" in ident
        assert "KLM1234" in ident

    def test_ident_desc_flight_same_as_registration(self, sample_datetime):
        """Test ident_desc() when flight equals registration."""
        aircraft = flightdata.AircraftData(
            dhex="abc123",
            squawk="7000",
            flight="PH-BXA",
            registration="PH-BXA",
            lat=53.3,
            lon=6.6,
            altitude=15000,
            vert_rate=0,
            track=270,
            speed=350,
            messages=150,
            seen=0.5,
            mlat=False,
            nucp=7,
            seen_pos=1.0,
            rssi=-25.5,
            dist=10.5,
            az=180,
            el=45,
            time=sample_datetime,
        )

        ident = aircraft.ident_desc()
        # Should only include hex and registration once
        parts = ident.split("/")
        assert len(parts) == 2  # hex and registration only


class TestDump1090DataParser:
    """Tests for Dump1090DataParser."""

    def test_parse_aircraft_data(self, mock_aircraft_data, sample_datetime):
        """Test parsing dump1090 aircraft.json data."""
        parser = flightdata.Dump1090DataParser()

        # Mock the receiver coordinates
        with (
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            aircraft_list = parser.aircraft_data(mock_aircraft_data, sample_datetime)

            # Should parse 3 aircraft (4th has no position)
            assert len(aircraft_list) == 4

            # Check first aircraft
            ac1 = aircraft_list[0]
            assert ac1.hex == "ABC123"
            assert ac1.squawk == "7000"
            assert ac1.flight == "KLM1234 "
            assert ac1.lat == 53.3
            assert ac1.lon == 6.6
            assert ac1.altitude == 15000
            assert ac1.track == 270

    def test_parse_aircraft_ground_altitude(self, sample_datetime):
        """Test parsing aircraft with 'ground' altitude."""
        data = {
            "now": 1706360400.0,
            "aircraft": [
                {
                    "hex": "abc123",
                    "lat": 53.2,
                    "lon": 6.5,
                    "alt_baro": "ground",
                    "track": 90,
                    "speed": 10,
                }
            ],
        }

        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            aircraft_list = parser.aircraft_data(data, sample_datetime)

            assert len(aircraft_list) == 1
            assert aircraft_list[0].altitude == 0.0

    def test_parse_speed_from_different_fields(self, sample_datetime):
        """Test parsing speed from speed, gs, or mach fields."""
        # Test with 'speed' field
        data_speed = {
            "now": 1706360400.0,
            "aircraft": [{"hex": "abc123", "lat": 53.2, "lon": 6.5, "speed": 300}],
        }

        # Test with 'gs' field (ground speed)
        data_gs = {
            "now": 1706360400.0,
            "aircraft": [{"hex": "def456", "lat": 53.2, "lon": 6.5, "gs": 450}],
        }

        # Test with 'mach' field
        data_mach = {
            "now": 1706360400.0,
            "aircraft": [{"hex": "789xyz", "lat": 53.2, "lon": 6.5, "mach": 0.85}],
        }

        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            # Parse speed field
            ac_speed = parser.aircraft_data(data_speed, sample_datetime)
            assert ac_speed[0].speed > 300  # Should be converted from knots to mph

            # Parse gs field
            ac_gs = parser.aircraft_data(data_gs, sample_datetime)
            assert ac_gs[0].speed > 450

            # Parse mach field
            ac_mach = parser.aircraft_data(data_mach, sample_datetime)
            assert 650 < ac_mach[0].speed < 660  # Mach 0.85 ≈ 652 mph

    def test_time_extraction(self, mock_aircraft_data):
        """Test extracting timestamp from dump1090 data."""
        parser = flightdata.Dump1090DataParser()
        timestamp = parser.time(mock_aircraft_data)
        assert timestamp == 1706360400.0

    def test_parse_aircraft_without_position(self, sample_datetime):
        """Test parsing aircraft without lat/lon."""
        data = {
            "now": 1706360400.0,
            "aircraft": [
                {"hex": "abc123", "squawk": "7700", "altitude": 5000}
                # No lat/lon
            ],
        }

        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            aircraft_list = parser.aircraft_data(data, sample_datetime)

            assert len(aircraft_list) == 1
            assert aircraft_list[0].lat is None
            assert aircraft_list[0].lon is None
            assert aircraft_list[0].distance == -1


class TestVRSDataParser:
    """Tests for VRSDataParser (Virtual Radar Server)."""

    def test_parse_vrs_data(self, mock_vrs_data, sample_datetime):
        """Test parsing VRS data."""
        parser = flightdata.VRSDataParser()

        with (
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            aircraft_list = parser.aircraft_data(mock_vrs_data, sample_datetime)

            assert len(aircraft_list) == 2

            # Check first aircraft
            ac1 = aircraft_list[0]
            assert ac1.hex == "ABC123"
            assert ac1.squawk == "7000"
            assert ac1.lat == 53.3
            assert ac1.lon == 6.6
            assert ac1.altitude == 15000

    def test_vrs_time_extraction(self, mock_vrs_data):
        """Test extracting timestamp from VRS data."""
        parser = flightdata.VRSDataParser()
        timestamp = parser.time(mock_vrs_data)
        assert timestamp == 1706360400.0  # Converted from milliseconds

    def test_vrs_speed_conversion(self, sample_datetime):
        """Test VRS speed conversion from knots to mph."""
        data = {
            "acList": [
                {
                    "Icao": "abc123",
                    "Lat": 53.2,
                    "Long": 6.5,
                    "Alt": 10000,
                    "Spd": 400,  # knots
                    "Trak": 90,
                }
            ],
            "stm": 1706360400000,
        }

        parser = flightdata.VRSDataParser()

        with (
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            aircraft_list = parser.aircraft_data(data, sample_datetime)

            # 400 knots ≈ 460 mph
            assert 450 < aircraft_list[0].speed < 470


class TestFlightData:
    """Tests for FlightData class."""

    def test_flightdata_creation(self, mock_aircraft_data):
        """Test creating FlightData object with mocked HTTP."""
        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.urlopen") as mock_urlopen,
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            # Mock the HTTP response
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(mock_aircraft_data).encode(
                "utf-8"
            )
            mock_urlopen.return_value = mock_response

            # Create FlightData
            fd = flightdata.FlightData(
                data_url="http://localhost/aircraft.json", parser=parser
            )

            # Check that aircraft were parsed
            assert fd.aircraft is not None
            assert len(fd.aircraft) == 4
            assert isinstance(fd.time, datetime)

    def test_flightdata_refresh(self, mock_aircraft_data):
        """Test refreshing flight data."""
        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.urlopen") as mock_urlopen,
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(mock_aircraft_data).encode(
                "utf-8"
            )
            mock_urlopen.return_value = mock_response

            fd = flightdata.FlightData(
                data_url="http://localhost/aircraft.json", parser=parser
            )

            # Refresh with updated data
            updated_data = mock_aircraft_data.copy()
            updated_data["now"] = 1706360500.0  # 100 seconds later

            mock_response.read.return_value = json.dumps(updated_data).encode("utf-8")

            fd.refresh()

            # Should have updated aircraft data
            assert fd.aircraft is not None

    def test_flightdata_network_error(self):
        """Test FlightData handling network errors."""
        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.urlopen") as mock_urlopen,
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            # Simulate network error
            from urllib.error import URLError

            mock_urlopen.side_effect = URLError("Connection refused")

            fd = flightdata.FlightData(
                data_url="http://localhost/aircraft.json", parser=parser
            )

            # Should return empty list on error
            assert fd.aircraft == []

    def test_flightdata_invalid_json(self):
        """Test FlightData handling invalid JSON."""
        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.urlopen") as mock_urlopen,
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            mock_response = MagicMock()
            mock_response.read.return_value = b"invalid json {"
            mock_urlopen.return_value = mock_response

            fd = flightdata.FlightData(
                data_url="http://localhost/aircraft.json", parser=parser
            )

            # Should return empty list on JSON decode error
            assert fd.aircraft == []


class TestIntegration:
    """Integration tests for flight data parsing."""

    def test_full_parsing_workflow(self, mock_aircraft_data):
        """Test complete workflow from JSON to AircraftData objects."""
        parser = flightdata.Dump1090DataParser()

        with (
            patch("flightdata.urlopen") as mock_urlopen,
            patch("flightdata.receiver_latitude", 53.215119),
            patch("flightdata.receiver_longitude", 6.570963),
        ):
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps(mock_aircraft_data).encode(
                "utf-8"
            )
            mock_urlopen.return_value = mock_response

            fd = flightdata.FlightData(
                data_url="http://localhost/aircraft.json", parser=parser
            )

            # Verify all aircraft were parsed correctly
            assert len(fd.aircraft) == 4

            # Find aircraft with position data
            positioned_aircraft = [a for a in fd.aircraft if a.lat is not None]
            assert len(positioned_aircraft) == 3

            # Verify distance and elevation calculations
            for aircraft in positioned_aircraft:
                assert aircraft.distance >= 0  # Distance should be calculated
                assert -90 <= aircraft.el <= 90  # Elevation should be valid
                assert 0 <= aircraft.az < 360  # Azimuth should be valid
