"""
Tests for aircraftdata.py - aircraft metadata lookups via hexdb.io API.

These tests mock HTTP requests to avoid actual API calls.
"""

from unittest.mock import Mock, patch
import aircraftdata


class TestRegis:
    """Tests for regis() function - aircraft registration lookup."""

    def test_regis_valid_hex(self, mock_http_responses):
        """Test registration lookup with valid hex code."""
        with patch("aircraftdata.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = mock_http_responses["hex-reg"]["abc123"]
            mock_get.return_value = mock_response

            result = aircraftdata.regis("abc123")

            assert result == "PH-BXA"
            mock_get.assert_called_once_with("https://hexdb.io/hex-reg?hex=abc123")

    def test_regis_unknown_hex(self):
        """Test registration lookup with unknown hex code."""
        with patch("aircraftdata.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = "n/a"
            mock_get.return_value = mock_response

            result = aircraftdata.regis("unknown")

            assert result == "n/a"

    def test_regis_none_input(self):
        """Test registration lookup with None input."""
        result = aircraftdata.regis(None)
        assert result is None


class TestPlane:
    """Tests for plane() function - aircraft type lookup."""

    def test_plane_valid_hex(self, mock_http_responses):
        """Test aircraft type lookup with valid hex code."""
        with patch("aircraftdata.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = mock_http_responses["hex-type"]["abc123"]
            mock_get.return_value = mock_response

            result = aircraftdata.plane("abc123")

            assert result == "Boeing 737-800"
            mock_get.assert_called_once_with("https://hexdb.io/hex-type?hex=abc123")

    def test_plane_unknown_hex(self):
        """Test aircraft type lookup with unknown hex code."""
        with patch("aircraftdata.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = "n/a"
            mock_get.return_value = mock_response

            result = aircraftdata.plane("unknown")

            assert result == "n/a"

    def test_plane_none_input(self):
        """Test aircraft type lookup with None input."""
        result = aircraftdata.plane(None)
        assert result is None


class TestOper:
    """Tests for oper() function - airline operator lookup."""

    def test_oper_valid_hex(self, mock_http_responses):
        """Test airline lookup with valid hex code."""
        with patch("aircraftdata.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = mock_http_responses["hex-airline"]["abc123"]
            mock_get.return_value = mock_response

            result = aircraftdata.oper("abc123")

            assert result == "KLM Royal Dutch Airlines"
            mock_get.assert_called_once_with("https://hexdb.io/hex-airline?hex=abc123")

    def test_oper_unknown_hex(self):
        """Test airline lookup with unknown hex code."""
        with patch("aircraftdata.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = "n/a"
            mock_get.return_value = mock_response

            result = aircraftdata.oper("unknown")

            assert result == "n/a"

    def test_oper_none_input(self):
        """Test airline lookup with None input."""
        result = aircraftdata.oper(None)
        assert result is None


class TestRoute:
    """Tests for route() function - flight route lookup."""

    def test_route_valid_flight(self, mock_http_responses):
        """Test route lookup with valid flight callsign."""
        with patch("aircraftdata.requests.get") as mock_get:
            # Create a side effect function to return different responses
            def get_response(url):
                mock_resp = Mock()
                if "callsign-origin_icao" in url:
                    mock_resp.text = "EHAM"
                elif "callsign-des_icao" in url:
                    mock_resp.text = "KJFK"
                elif "icao-iata?icao=EHAM" in url:
                    mock_resp.text = "AMS"
                elif "icao-iata?icao=KJFK" in url:
                    mock_resp.text = "JFK"
                elif "icao-airport?icao=EHAM" in url:
                    mock_resp.text = "Amsterdam Schiphol"
                elif "icao-airport?icao=KJFK" in url:
                    mock_resp.text = "John F. Kennedy Intl"
                return mock_resp

            mock_get.side_effect = get_response

            result = aircraftdata.route("KLM1234")

            assert result == "AMS-JFK Amsterdam Schiphol to John F. Kennedy Intl"
            assert mock_get.call_count == 6

    def test_route_unknown_flight(self):
        """Test route lookup with unknown flight."""
        with patch("aircraftdata.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.text = "n/a"
            mock_get.return_value = mock_response

            result = aircraftdata.route("UNKNOWN")

            assert result == "n/a"

    def test_route_none_input(self):
        """Test route lookup with None input."""
        result = aircraftdata.route(None)
        assert result is None

    def test_route_domestic_flight(self):
        """Test route lookup for a domestic flight."""
        with patch("aircraftdata.requests.get") as mock_get:

            def get_response(url):
                mock_resp = Mock()
                if "callsign-origin_icao" in url:
                    mock_resp.text = "EGLL"
                elif "callsign-des_icao" in url:
                    mock_resp.text = "EGCC"
                elif "icao-iata?icao=EGLL" in url:
                    mock_resp.text = "LHR"
                elif "icao-iata?icao=EGCC" in url:
                    mock_resp.text = "MAN"
                elif "icao-airport?icao=EGLL" in url:
                    mock_resp.text = "London Heathrow"
                elif "icao-airport?icao=EGCC" in url:
                    mock_resp.text = "Manchester"
                return mock_resp

            mock_get.side_effect = get_response

            result = aircraftdata.route("BAW888")

            assert result == "LHR-MAN London Heathrow to Manchester"


class TestIntegration:
    """Integration tests for aircraft data lookups."""

    def test_full_aircraft_lookup(self, mock_http_responses):
        """Test complete aircraft information lookup."""
        hex_code = "abc123"

        with patch("aircraftdata.requests.get") as mock_get:

            def get_response(url):
                mock_resp = Mock()
                if "hex-reg" in url:
                    mock_resp.text = "PH-BXA"
                elif "hex-type" in url:
                    mock_resp.text = "Boeing 737-800"
                elif "hex-airline" in url:
                    mock_resp.text = "KLM Royal Dutch Airlines"
                return mock_resp

            mock_get.side_effect = get_response

            registration = aircraftdata.regis(hex_code)
            aircraft_type = aircraftdata.plane(hex_code)
            operator = aircraftdata.oper(hex_code)

            assert registration == "PH-BXA"
            assert aircraft_type == "Boeing 737-800"
            assert operator == "KLM Royal Dutch Airlines"

    def test_multiple_aircraft_lookups(self):
        """Test looking up multiple aircraft in sequence."""
        aircraft = [
            ("abc123", "PH-BXA", "Boeing 737-800"),
            ("def456", "PH-HZD", "Boeing 737-700"),
            ("789xyz", "G-EUUU", "Airbus A320"),
        ]

        with patch("aircraftdata.requests.get") as mock_get:

            def get_response(url):
                mock_resp = Mock()
                if "abc123" in url:
                    if "hex-reg" in url:
                        mock_resp.text = "PH-BXA"
                    elif "hex-type" in url:
                        mock_resp.text = "Boeing 737-800"
                elif "def456" in url:
                    if "hex-reg" in url:
                        mock_resp.text = "PH-HZD"
                    elif "hex-type" in url:
                        mock_resp.text = "Boeing 737-700"
                elif "789xyz" in url:
                    if "hex-reg" in url:
                        mock_resp.text = "G-EUUU"
                    elif "hex-type" in url:
                        mock_resp.text = "Airbus A320"
                return mock_resp

            mock_get.side_effect = get_response

            for hex_code, expected_reg, expected_type in aircraft:
                reg = aircraftdata.regis(hex_code)
                plane_type = aircraftdata.plane(hex_code)
                assert reg == expected_reg
                assert plane_type == expected_type
