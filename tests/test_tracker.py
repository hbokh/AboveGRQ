"""
Tests for tracker.py - main tracking loop and Bluesky posting.

Uses mocked dependencies to avoid actual API calls and browser automation.
"""

from unittest.mock import patch, MagicMock, mock_open
import tracker
import flightdata


class TestPostAircraftUpdate:
    """Tests for post_aircraft_update() function."""

    def test_post_with_screenshot(self, sample_datetime, mock_config):
        """Test posting aircraft update with screenshot."""
        # Create mock aircraft
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

        # Mock the config parser
        with (
            patch("tracker.parser", mock_config),
            patch("tracker.aircraftdata.regis", return_value="PH-BXA"),
            patch("tracker.aircraftdata.plane", return_value="Boeing 737-800"),
            patch("tracker.aircraftdata.oper", return_value="KLM"),
            patch("tracker.aircraftdata.route", return_value="AMS-JFK"),
            patch("tracker.Client") as mock_client_class,
            patch("builtins.open", mock_open(read_data=b"fake_image_data")),
        ):
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Call the function
            tracker.post_aircraft_update(aircraft, havescreenshot=True)

            # Verify client was created and logged in
            mock_client_class.assert_called_once()
            mock_client.login.assert_called_once()

            # Verify send_image was called
            mock_client.send_image.assert_called_once()

            # Check the arguments
            call_args = mock_client.send_image.call_args
            assert "text" in call_args.kwargs
            assert "facets" in call_args.kwargs
            assert "image" in call_args.kwargs

    def test_post_respects_300_char_limit(self, sample_datetime, mock_config):
        """Test that posts don't exceed 300 character limit."""
        aircraft = flightdata.AircraftData(
            dhex="abc123",
            squawk="7000",
            flight="KLM1234VERYLONGFLIGHTNUMBER",
            registration="PH-BXA",
            lat=53.3,
            lon=6.6,
            altitude=35000,
            vert_rate=-1024,
            track=270,
            speed=520,
            messages=150,
            seen=0.5,
            mlat=False,
            nucp=7,
            seen_pos=1.0,
            rssi=-25.5,
            dist=100.5,
            az=180,
            el=45,
            time=sample_datetime,
        )

        with (
            patch("tracker.parser", mock_config),
            patch("tracker.aircraftdata.regis", return_value="PH-BXA"),
            patch(
                "tracker.aircraftdata.plane",
                return_value="Boeing 737-800 with very long type name",
            ),
            patch("tracker.aircraftdata.oper", return_value="KLM Royal Dutch Airlines"),
            patch(
                "tracker.aircraftdata.route",
                return_value="AMS-JFK Amsterdam Schiphol to John F. Kennedy International",
            ),
            patch("tracker.Client") as mock_client_class,
            patch("builtins.open", mock_open(read_data=b"fake_image_data")),
        ):
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            tracker.post_aircraft_update(aircraft, havescreenshot=True)

            call_args = mock_client.send_image.call_args
            text = call_args.kwargs["text"]

            # Check that text doesn't exceed 300 characters
            assert len(text) <= 300


class TestTemplateSubstitution:
    """Tests for template variable substitution."""

    def test_all_template_variables(self, sample_datetime, mock_config):
        """Test that template variables are properly substituted."""
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

        with (
            patch("tracker.parser", mock_config),
            patch("tracker.aircraftdata.regis", return_value="PH-BXA"),
            patch("tracker.aircraftdata.plane", return_value="Boeing 737-800"),
            patch("tracker.aircraftdata.oper", return_value="KLM"),
            patch("tracker.aircraftdata.route", return_value="AMS-JFK"),
            patch("tracker.Client") as mock_client_class,
            patch("builtins.open", mock_open(read_data=b"fake_image_data")),
        ):
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            tracker.post_aircraft_update(aircraft, havescreenshot=True)

            call_args = mock_client.send_image.call_args
            text = call_args.kwargs["text"]

            # Check that key information is in the text
            # The exact format depends on the template, but flight should be there
            assert "KLM1234" in text or "abc123" in text


class TestImageAspectRatio:
    """Tests for image aspect ratio configuration."""

    def test_aspect_ratio_from_config(self, sample_datetime, mock_config):
        """Test that aspect ratio is set from config values."""
        aircraft = flightdata.AircraftData(
            dhex="abc123",
            squawk="7000",
            flight="KLM1234",
            registration=None,
            lat=53.3,
            lon=6.6,
            altitude=5000,
            vert_rate=0,
            track=270,
            speed=250,
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

        with (
            patch("tracker.parser", mock_config),
            patch("tracker.crop_width", 780),
            patch("tracker.crop_height", 800),
            patch("tracker.aircraftdata.regis", return_value="n/a"),
            patch("tracker.aircraftdata.plane", return_value="n/a"),
            patch("tracker.aircraftdata.oper", return_value="n/a"),
            patch("tracker.aircraftdata.route", return_value="n/a"),
            patch("tracker.Client") as mock_client_class,
            patch("builtins.open", mock_open(read_data=b"fake_image_data")),
            patch("tracker.models.AppBskyEmbedDefs.AspectRatio") as mock_aspect,
        ):
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            tracker.post_aircraft_update(aircraft, havescreenshot=True)

            # Verify AspectRatio was called with patched values
            mock_aspect.assert_called_once_with(height=800, width=780)
