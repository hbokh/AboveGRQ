# ✈️ Above GRQ

*An ADS-B Bot, derived from [AboveTustin](https://github.com/kevinabrandon/AboveTustin) (a Twitter bot).*

Uses [dump1090-fa](https://github.com/flightaware/dump1090) to track airplanes and posts whenever an airplane flies nearby Groningen Airport Eelde (IATA: **[GRQ](https://www.wikiwand.com/en/Groningen_Airport_Eelde)**, ICAO: **EHGG**).

Posts screenshots to Bluesky, taken from a local [tar1090](https://github.com/wiedehopf/tar1090) installation.

**WARNING**: this is [Frankencode](https://www.urbandictionary.com/define.php?term=Frankencode)!!\
Currently it runs on a RPi4 and on my MacBook Pro M2 (most recent macOS with Homebrew packages).

## Install

Checkout this repo as "AboveGRQ" and use [uv](https://docs.astral.sh/uv/) to setup a project env.

Copy the file `config.sample.ini` to `config.ini` and make all the necessary changes in that file.

Run with `uv run tracker.py`:

```console
$ uv run tracker.py
Will crop
Map URL: http://rpi.lan/tar1090/
Getting web page http://rpi.lan/tar1090/
Waiting for page to load...
Reset map
Zoom in
Now: 2026-01-26 18:52:41.600000
Now: 2026-01-26 18:52:42.700000
Now: 2026-01-26 18:52:43.700000
--- cut --- 8< ---
```

## Screenshot

Obligatory screenshot, taken from [Ivory](https://tapbots.com/ivory/) for iOS:

![IMG_0189](https://user-images.githubusercontent.com/519955/217902537-7371c254-55d5-4ccc-a179-db6b1c48c952.jpg)

## Dependencies

- Use Python 3.1x and [uv](https://docs.astral.sh/uv/).
- Use a Firefox based browser.
- Uses [tar1090](https://github.com/wiedehopf/tar1090) for ADSB message decoding, airplane tracking, and webserving.
- Uses [selenium](https://pypi.python.org/pypi/selenium) for screenshots with geckodriver.
- Uses [pillow](https://python-pillow.org/) for image processing.
- Uses [requests](https://pypi.org/project/requests/) for API calls.
- Uses [geckodriver](https://github.com/mozilla/geckodriver) for headless web browsing.
- A [PiAware](https://flightaware.com/adsb/piaware/build) Raspberry Pi-based ADS-B receiver & decoder with MLAT support, with web server and local databases.

## Code borrowed from

- kevinabrandon/[AboveTustin](https://github.com/kevinabrandon/AboveTustin)
- shbisson/[OverPutney](https://github.com/shbisson/OverPutney)
- ladewig/[OverPutney](https://github.com/ladewig/OverPutney)
- ggoodloff/[AnyFlightTracker](https://github.com/ggoodloff/AnyFlightTracker/)

## Todo

- [X] Use latest Python 3.x version.
- [x] Replace Twitter with Mastodon.
- [x] Make hashtags work with "facets".
- [x] Replace Mastodon with Bluesky.
- [x] Fix "Loading image..." in screenshots when in headless mode.
- [x] Replace Google Chrome & Chromedriver.
- [x] Remove FlightAware API / FlightXML3 code.
- [X] Fix additional hashtags.

## Notes

To enable tar1090 web screenshots, the tar1090 `config.js` on the rpi needs to be edited.
Edit file `/<dir>/tar1090/html/config.js` and remark out (`//`) the ICAO line in the `HideCols` section.
