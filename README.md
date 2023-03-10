# ✈️ Above GRQ

*An ADS-B Mastodon Bot, derived from [AboveTustin](https://github.com/kevinabrandon/AboveTustin) (a Twitter bot).*

The original Twitter dependencies have been replaced with basic [posting via the Mastodon API using Python](https://roytang.net/2021/11/mastodon-api-python/).

Uses [dump1090-fa](https://github.com/flightaware/dump1090) to track airplanes and toots whenever an airplane flies nearby Groningen Airport Eelde (IATA: **[GRQ](https://www.wikiwand.com/en/Groningen_Airport_Eelde)**, ICAO: **EHGG**).

**WARNING**: this is [Frankencode](https://www.urbandictionary.com/define.php?term=Frankencode)!!\
Currently it runs on my MacBook Pro (macOS 11.7 with Homebrew packages).\
Look for `CHANGE THIS!!` entries in the code for personal changes that might need to be made.

## Screenshot

Obligatory screenshot, taken from [Ivory](https://tapbots.com/ivory/) for iOS:

![IMG_0189](https://user-images.githubusercontent.com/519955/217902537-7371c254-55d5-4ccc-a179-db6b1c48c952.jpg)

## Dependencies

- Use Python 3.x and [venv](https://docs.python.org/3/library/venv.html).
- Uses [tar1090](https://github.com/wiedehopf/tar1090) for ADSB message decoding, airplane tracking, and webserving.
- Uses Mastodon API for tooting.
- Uses [selenium](https://pypi.python.org/pypi/selenium) for screenshots with Chromedriver and Google Chromium.
- Uses [pillow](https://python-pillow.org/) for image processing.
- Uses [requests](https://pypi.org/project/requests/) for API calls.
- Uses [Chromedriver](https://chromedriver.chromium.org/) for headless web browsing.
- Builds on a running [PiAware](https://flightaware.com/adsb/piaware/build) Raspberry Pi-based ADS-B receiver and decoder with MLAT support, with web server and local databases.

## Code borrowed from

- kevinabrandon/[AboveTustin](https://github.com/kevinabrandon/AboveTustin)
- shbisson/[OverPutney](https://github.com/shbisson/OverPutney)
- ladewig/[OverPutney](https://github.com/ladewig/OverPutney)

## Todo

- [x] Replace Twitter with Mastodon.
- [x] Fix "Loading image..." in screenshots when in headless mode.
- [x] Replace Google Chrome / Chromedriver.
- [X] Use latest Python 3.x version.
- [ ] Remove FlightAware API / FlightXML3 code.
