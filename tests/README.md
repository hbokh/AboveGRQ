# AboveGRQ Test Suite

This directory contains comprehensive pytest tests for the AboveGRQ aircraft tracking bot.

## Running the Tests

Run all tests:
```bash
uv run pytest tests/
```

Run with verbose output:
```bash
uv run pytest tests/ -v
```

Run specific test file:
```bash
uv run pytest tests/test_geomath.py -v
```

Run specific test class or function:
```bash
uv run pytest tests/test_geomath.py::TestDistance::test_distance_medium -v
```

Run with coverage report:
```bash
uv run pytest tests/ --cov=. --cov-report=html
```

## Test Structure

### `conftest.py`
Shared fixtures used across all tests:
- `receiver_coords` - GPS coordinates from config.ini
- `mock_aircraft_data` - Bogus aircraft data in dump1090 format
- `mock_vrs_data` - Bogus VRS format data
- `mock_http_responses` - Mock responses for hexdb.io API
- `sample_datetime` - Consistent datetime for testing
- `mock_config` - Mock configuration parser

### Test Files

#### `test_geomath.py` (24 tests)
Tests for geographic calculations and unit conversions:
- Heading string conversions (N, NE, E, SE, S, SW, W, NW)
- Unit conversions (knots↔mph, mach↔mph, mi↔km, mi↔nm, ft↔m)
- Haversine distance calculations
- Bearing calculations between two points
- Integration tests combining multiple calculations

#### `test_util.py` (6 tests)
Tests for utility functions:
- Error message formatting and output
- stderr output testing
- Format string argument handling

#### `test_aircraftdata.py` (15 tests)
Tests for aircraft metadata lookups via hexdb.io:
- Registration lookup by hex code
- Aircraft type lookup
- Airline operator lookup
- Flight route lookup (origin/destination)
- Integration tests for complete aircraft info

**Note:** All HTTP requests are mocked to avoid actual API calls.

#### `test_flightdata.py` (17 tests)
Tests for flight data parsing and aircraft data structures:
- `AircraftData` class creation and methods
- dump1090 JSON parsing
- Virtual Radar Server (VRS) data parsing
- Speed and altitude handling
- Network error handling
- Invalid JSON handling
- Integration tests for complete parsing workflow

**Note:** Uses bogus aircraft data from fixtures.

#### `test_tracker.py` (4 tests)
Tests for main tracking loop and Bluesky posting:
- Post creation with screenshots
- Bluesky API client initialization and login
- 300 character limit enforcement
- Template variable substitution
- Image aspect ratio configuration

**Note:** All Bluesky API calls and browser automation are mocked.

## Test Summary

**Total: 72 tests** covering:
- ✅ Geographic calculations (geomath.py) - 24 tests
- ✅ Utility functions (util.py) - 6 tests
- ✅ Aircraft metadata API (aircraftdata.py) - 15 tests
- ✅ Flight data parsing (flightdata.py) - 17 tests
- ✅ Main tracker and posting (tracker.py) - 4 tests
- ⚠️  Browser automation (screenshot.py) - Not tested due to Selenium complexity
- ⚠️  Data source abstraction (datasource.py) - Not tested

## Mock Data

All tests use mock/bogus data:
- **Aircraft positions**: Near Groningen (53.215119, 6.570963)
- **ICAO hex codes**: abc123, def456, 789xyz
- **Registrations**: PH-BXA, PH-HZD, G-EUUU
- **Altitudes**: 800 ft (low), 5000 ft (approach), 15000 ft (cruise), 38000 ft (high)
- **Speeds**: 150 mph (slow), 350 mph (cruise), 720 mph (fast)

## Dependencies

Tests require:
- `pytest` (>=9.0.2)
- `pytest-mock` (>=3.15.1)

These are automatically installed as dev dependencies via `uv add --dev`.

## Notes

- Tests use the coordinates from `tests/test-config.ini` for realistic distance calculations
- All network requests are mocked to avoid external dependencies
- Browser automation (Selenium) is mocked to avoid requiring Firefox/geckodriver
- Tests run quickly (~2 seconds for all 72 tests)
- No actual Bluesky posts are created during testing
- The `test-config.ini` file contains test-specific configuration separate from the production `config.ini`
