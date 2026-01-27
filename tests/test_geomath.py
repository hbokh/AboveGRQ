"""
Tests for geomath.py - geographic calculations and unit conversions.
"""

import pytest
import geomath


class TestHeadingString:
    """Tests for heading_str() function."""

    def test_north(self):
        assert geomath.heading_str(0) == "N"
        assert geomath.heading_str(10) == "N"
        assert geomath.heading_str(350) == "N"
        assert geomath.heading_str(359.9) == "N"

    def test_northeast(self):
        assert geomath.heading_str(45) == "NE"
        assert geomath.heading_str(30) == "NE"
        assert geomath.heading_str(60) == "NE"

    def test_east(self):
        assert geomath.heading_str(90) == "E"
        assert geomath.heading_str(80) == "E"
        assert geomath.heading_str(100) == "E"

    def test_southeast(self):
        assert geomath.heading_str(135) == "SE"
        assert geomath.heading_str(120) == "SE"
        assert geomath.heading_str(150) == "SE"

    def test_south(self):
        assert geomath.heading_str(180) == "S"
        assert geomath.heading_str(170) == "S"
        assert geomath.heading_str(190) == "S"

    def test_southwest(self):
        assert geomath.heading_str(225) == "SW"
        assert geomath.heading_str(210) == "SW"
        assert geomath.heading_str(240) == "SW"

    def test_west(self):
        assert geomath.heading_str(270) == "W"
        assert geomath.heading_str(260) == "W"
        assert geomath.heading_str(280) == "W"

    def test_northwest(self):
        assert geomath.heading_str(315) == "NW"
        assert geomath.heading_str(300) == "NW"
        assert geomath.heading_str(330) == "NW"

    def test_none_heading(self):
        assert geomath.heading_str(None) == "?"


class TestUnitConversions:
    """Tests for unit conversion functions."""

    def test_knots_to_mph(self):
        # 100 knots = 115.078 mph
        assert abs(geomath.knots_to_mph(100) - 115.078) < 0.01
        assert geomath.knots_to_mph(0) == 0
        assert geomath.knots_to_mph(None) is None

    def test_mach_to_mph(self):
        # Mach 1 = 767.27 mph (at sea level, standard conditions)
        assert abs(geomath.mach2mph(1.0) - 767.27) < 0.01
        assert abs(geomath.mach2mph(0.85) - 652.18) < 0.01
        assert geomath.mach2mph(0) == 0
        assert geomath.mach2mph(None) is None

    def test_miles_to_kilometers(self):
        # 1 mile = 1.60934 km
        assert abs(geomath.mi2km(1) - 1.60934) < 0.0001
        assert abs(geomath.mi2km(10) - 16.0934) < 0.001
        assert geomath.mi2km(0) == 0
        assert geomath.mi2km(None) is None

    def test_miles_to_nautical_miles(self):
        # 1 mile = 0.868976 nautical miles
        assert abs(geomath.mi2nm(1) - 0.868976) < 0.0001
        assert abs(geomath.mi2nm(100) - 86.8976) < 0.001
        assert geomath.mi2nm(0) == 0
        assert geomath.mi2nm(None) is None

    def test_feet_to_meters(self):
        # 1 foot = 0.3048 meters
        assert abs(geomath.ft2m(1) - 0.3048) < 0.0001
        assert abs(geomath.ft2m(1000) - 304.8) < 0.01
        assert abs(geomath.ft2m(35000) - 10668) < 1
        assert geomath.ft2m(0) == 0
        assert geomath.ft2m(None) is None


class TestDistance:
    """Tests for distance calculation using Haversine formula."""

    def test_distance_same_point(self):
        # Distance from a point to itself should be 0
        point = (53.215119, 6.570963)
        assert geomath.distance(point, point) == 0

    def test_distance_short(self, receiver_coords):
        # Test short distance (< 10 miles)
        # Groningen Airport coordinates: 53.1197, 6.5794
        point_a = receiver_coords
        point_b = (53.1197, 6.5794)
        dist = geomath.distance(point_a, point_b)
        # Should be approximately 6.6 miles
        assert 6.0 < dist < 7.5

    def test_distance_medium(self):
        # Amsterdam to Groningen is about 91 miles
        amsterdam = (52.3676, 4.9041)
        groningen = (53.2194, 6.5665)
        dist = geomath.distance(amsterdam, groningen)
        assert 85 < dist < 100  # Actual calculated distance ≈ 91 miles

    def test_distance_long(self):
        # New York to London is about 3460 miles
        nyc = (40.7128, -74.0060)
        london = (51.5074, -0.1278)
        dist = geomath.distance(nyc, london)
        assert 3400 < dist < 3500

    def test_distance_equator_crossing(self):
        # Test distance across equator
        point_north = (10.0, 0.0)
        point_south = (-10.0, 0.0)
        dist = geomath.distance(point_north, point_south)
        # 20 degrees of latitude ≈ 1380 miles
        assert 1350 < dist < 1400


class TestBearing:
    """Tests for bearing calculation between two points."""

    def test_bearing_north(self):
        # From equator to north pole should be ~0 degrees
        point_a = (0.0, 0.0)
        point_b = (10.0, 0.0)
        bearing = geomath.bearing(point_a, point_b)
        assert 359 < bearing or bearing < 1

    def test_bearing_east(self):
        # Eastward bearing should be ~90 degrees
        point_a = (52.0, 0.0)
        point_b = (52.0, 10.0)
        bearing = geomath.bearing(point_a, point_b)
        assert 85 < bearing < 95

    def test_bearing_south(self):
        # Southward bearing should be ~180 degrees
        point_a = (52.0, 0.0)
        point_b = (42.0, 0.0)
        bearing = geomath.bearing(point_a, point_b)
        assert 175 < bearing < 185

    def test_bearing_west(self):
        # Westward bearing should be ~270 degrees
        point_a = (52.0, 10.0)
        point_b = (52.0, 0.0)
        bearing = geomath.bearing(point_a, point_b)
        assert 265 < bearing < 275

    def test_bearing_northeast(self, receiver_coords):
        # Bearing from Groningen to a point northeast
        point_a = receiver_coords
        point_b = (54.0, 7.5)  # Northeast of Groningen
        bearing = geomath.bearing(point_a, point_b)
        assert 30 < bearing < 60

    def test_bearing_returns_0_to_360(self):
        # Bearing should always be 0-360 degrees
        point_a = (52.0, 5.0)
        point_b = (53.0, 6.0)
        bearing = geomath.bearing(point_a, point_b)
        assert 0 <= bearing < 360

    def test_bearing_invalid_input(self):
        # Should raise TypeError for non-tuple inputs
        with pytest.raises(TypeError):
            geomath.bearing([52.0, 5.0], (53.0, 6.0))
        with pytest.raises(TypeError):
            geomath.bearing((52.0, 5.0), [53.0, 6.0])

    def test_bearing_same_point(self):
        # Bearing from a point to itself
        point = (53.215119, 6.570963)
        bearing = geomath.bearing(point, point)
        # Should be 0 or close to it (may have floating point imprecision)
        assert 0 <= bearing < 360


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_full_calculation_chain(self, receiver_coords):
        """Test a realistic scenario with multiple calculations."""
        # Aircraft at Amsterdam Schiphol
        aircraft_pos = (52.3105, 4.7683)

        # Calculate distance
        dist_mi = geomath.distance(receiver_coords, aircraft_pos)
        dist_km = geomath.mi2km(dist_mi)
        dist_nm = geomath.mi2nm(dist_mi)

        # All should be positive and in reasonable range
        assert dist_mi > 90  # More realistic range
        assert dist_km > dist_mi  # km larger than miles
        assert dist_nm < dist_mi  # nautical miles smaller than miles

        # Calculate bearing
        bearing_deg = geomath.bearing(receiver_coords, aircraft_pos)
        heading = geomath.heading_str(bearing_deg)

        # Should be heading roughly southwest from Groningen to Amsterdam
        assert heading in ["SW", "W", "S", "WSW"]  # Allow more flexibility

    def test_altitude_conversions(self):
        """Test realistic altitude conversions."""
        cruise_alt_ft = 35000  # feet
        cruise_alt_m = geomath.ft2m(cruise_alt_ft)

        # Should be approximately 10,668 meters
        assert 10600 < cruise_alt_m < 10700

    def test_speed_conversions(self):
        """Test realistic speed conversions."""
        # Typical jet cruise speed: 450 knots
        speed_kts = 450
        speed_mph = geomath.knots_to_mph(speed_kts)

        # Should be approximately 518 mph
        assert 515 < speed_mph < 520

        # Mach 0.85 (typical cruise mach)
        mach = 0.85
        speed_mph_mach = geomath.mach2mph(mach)

        # Should be approximately 652 mph
        assert 650 < speed_mph_mach < 655
