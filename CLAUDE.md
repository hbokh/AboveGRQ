# AboveGRQ Project

## Project Overview

AboveGRQ is an ADS-B aircraft tracking bot that monitors airplanes flying near Groningen Airport Eelde (IATA: GRQ, ICAO: EHGG). It automatically posts screenshots and flight information to Bluesky when aircraft enter a defined alarm zone.

Derived from AboveTustin (originally a Twitter bot), this project uses dump1090-fa for aircraft tracking and tar1090 for web-based visualization and screenshots.

**WARNING**: This is self-described "Frankencode" - it works but may not follow best practices consistently.

## Critical Development Practices

### UV Package Manager (CRITICAL)

**CRITICAL**: This project uses **UV** for all Python operations. Never use `python -m`, `pip install`, or `python script.py` directly.

***ALWAYS USE:**

- `uv run <script.py>` - to run Python scripts
- `uv add <package>` - to add dependencies
- `uv sync` - to sync dependencies
- `uv pip` - if pip commands are needed

Use ruff for linting and formatting.

Write valid Markdown and adhere to the GitHub Flavored Markdown Spec.

## Project Structure

```text
AboveGRQ/
├── tracker.py           # Main tracking loop and Bluesky posting
├── flightdata.py        # Flight data handling (10K+ lines)
├── screenshot.py        # Browser automation for screenshots
├── aircraftdata.py      # Aircraft metadata lookups
├── datasource.py        # Data source abstraction layer
├── geomath.py           # Geographic calculations
├── util.py              # Utility functions
├── config.ini           # Configuration file (not in repo, copy from sample)
├── config.example.ini    # Sample configuration
├── tar1090config.js     # tar1090 web interface config
├── run_tracker.sh       # Restart wrapper script
├── pyproject.toml       # UV/Python project config
└── uv.lock              # UV dependency lock file
```

## Technology Stack

### Core Dependencies

- **Python 3.13+** (currently targets 3.14)
- **UV** - Package and project manager
- **atproto** (>=0.0.65) - Bluesky/AT Protocol client
- **selenium** (==4.9.1) - Browser automation
- **pillow** (>=12.1.0) - Image processing
- **requests** (>=2.32.5) - HTTP requests
- **webdriver-manager** (>=4.0.2) - WebDriver management

### External Dependencies

- **Firefox** browser (required for Selenium)
- **geckodriver** - WebDriver for Firefox
- **tar1090** - ADS-B web interface (running on local or remote host)
- **dump1090-fa** - ADS-B message decoder
- **PiAware** - Raspberry Pi ADS-B receiver (optional, can run on Mac)

## Configuration

### Initial Setup

1. Copy `config.example.ini` to `config.ini`
2. Configure the following sections:
   - `[receiver]` - Your GPS coordinates (latitude/longitude)
   - `[aboveme]` - data_url and map_url for tar1090 instance
   - `[bsky]` - Bluesky handle and password
   - `[apps]` - Paths to geckodriver and Firefox browser
   - `[crop]` - Screenshot cropping dimensions

### Key Configuration Parameters

**Alarm Zone Settings** (`[aboveme]`):

- `distance_alarm` - Distance in miles to trigger tracking (default: 2)
- `elevation_alarm` - Elevation angle in degrees (default: 75)
- `wait_x_updates` - Wait cycles before posting (default: 3)
- `sleep_time` - Seconds between updates (default: 1)

**Screenshot Settings**:

- `image_width` / `image_height` - Browser viewport size
- `crop_x`, `crop_y`, `crop_width`, `crop_height` - Crop rectangle

## Running the Project

### Standard Run

```bash
uv run tracker.py
```

### Production Run (with auto-restart)

```bash
./run_tracker.sh
```

The shell script runs in a loop, automatically restarting the tracker if it exits. It waits 60 seconds between restarts to allow for manual intervention.

## Code Patterns and Architecture

### Main Loop (tracker.py)

1. Connects to tar1090 data source (aircraft.json)
2. Opens browser for screenshot capture
3. Continuously monitors aircraft positions
4. Maintains alarm dictionary of tracked aircraft
5. When aircraft exits alarm zone after wait period:
   - Captures screenshot by clicking aircraft in tar1090
   - Composes post with flight data and hashtags
   - Posts to Bluesky with image and facets (for hashtag linking)

### Data Flow

```text
dump1090-fa → tar1090 → aircraft.json
                ↓
         datasource.py → flightdata.py
                ↓
           tracker.py (main loop)
                ↓
         screenshot.py (browser automation)
                ↓
           Bluesky API (via atproto)
```

### Key Classes and Functions

**tracker.py:**

- `post_aircraft_update(a, havescreenshot)` - Posts to Bluesky with image and facets

**datasource.py:**

- `get_data_source()` - Returns FlightData instance
- `get_map_source()` - Returns ScreenShot instance

**screenshot.py:**

- `ScreenShot` class - Selenium-based browser automation
- `clickOnAirplane(hexcode)` - Clicks aircraft and captures screenshot

**flightdata.py:**

- Aircraft data structures and JSON parsing

**geomath.py:**

- Distance calculations (Haversine)
- Unit conversions (mi/km/nm, ft/m)
- Heading calculations and formatting

**aircraftdata.py:**

- Lookups for registration, aircraft type, operator, route

## Bluesky Integration

The bot uses the AT Protocol (atproto) library to post to Bluesky:

1. Text posts limited to 300 characters
2. Hashtags implemented using "facets" for proper linking
3. Images uploaded with custom aspect ratios
4. Byte-position-based text formatting (UTF-8)

## Testing

The project includes a comprehensive pytest test suite with 72 tests covering:

- **test_geomath.py** - Geographic calculations and unit conversions (24 tests)
- **test_util.py** - Utility functions (6 tests)
- **test_aircraftdata.py** - Aircraft metadata API (mocked) (15 tests)
- **test_flightdata.py** - Flight data parsing (17 tests)
- **test_tracker.py** - Main tracker and Bluesky posting (mocked) (4 tests)

Run tests with:

```bash
uv run pytest tests/ -v
```

All tests use mock/bogus data and test configuration from `tests/test-config.ini`. No actual API calls or browser automation during testing.

See [tests/README.md](tests/README.md) for detailed test documentation.

## tar1090 Configuration

To enable screenshots, edit `config.js` in tar1090 installation:

```javascript
// In HideCols section, comment out the ICAO line:
// "icao",  // ← Add // to show ICAO in interface
```

## Development Notes

- Code quality warning: Project is functional but not polished
- Error handling present but basic
- Browser reloads every hour when no alarms active (prevents memory leaks)
- Screenshot capture requires aircraft to be clickable in tar1090 interface
- Uses Selenium in headless mode (configurable)

## Git Workflow

Current branch: `main`

- Uses pre-commit hooks (ruff for linting)
- Recent focus on UV migration and code cleanup

## Reference Links

- [UV Documentation](https://docs.astral.sh/uv/)
- [atproto Python SDK](https://github.com/MarshalX/atproto)
- [tar1090](https://github.com/wiedehopf/tar1090)
- [dump1090-fa](https://github.com/flightaware/dump1090)
- [AboveTustin (original)](https://github.com/kevinabrandon/AboveTustin)
