# ✈️ Above GRQ

*An ADS-B Mastodon Bot, derived from [AboveTustin](https://github.com/kevinabrandon/AboveTustin) (a Twitter bot).*

The original Twitter dependencies have been replaced with basic [posting via the Mastodon API using Python](https://roytang.net/2021/11/mastodon-api-python/).

Uses [dump1090-fa](https://github.com/flightaware/dump1090) to track airplanes and toots whenever an airplane flies nearby Groningen Airport Eelde (IATA: **[GRQ](https://www.wikiwand.com/en/Groningen_Airport_Eelde)**), ICAO: **EHGG**).

**WARNING**: this is [Frankencode](https://www.urbandictionary.com/define.php?term=Frankencode)!!

## Dependencies

- Use Python 3.9 (to bypass some weird incompatabilities with 3.10)
- Uses [tar1090](https://github.com/wiedehopf/tar1090) for ADSB message decoding, airplane tracking, and webserving.
- Uses Mastodon API for tooting.
- Uses [selenium](https://pypi.python.org/pypi/selenium) for screenshots with Chromedriver and Google Chrome / Chromium.
- Uses [pillow](https://python-pillow.org/) for image processing.
- Uses [requests](https://pypi.org/project/requests/) for API calls.
- Uses [Chromedriver](https://chromedriver.chromium.org/) for headless web browsing.
- Builds on a running [Piaware](https://flightaware.com/adsb/piaware/build) Raspberry Pi-based ADS-B receiver and decoder with MLAT support, with web server and local databases.

## Code borrowed from

- kevinabrandon/[AboveTustin](https://github.com/kevinabrandon/AboveTustin)
- shbisson/[OverPutney](https://github.com/shbisson/OverPutney)
- ladewig/[OverPutney](https://github.com/ladewig/OverPutney)

## Todo

- [x] Replace Twitter with Mastodon.
- [ ] Fix "Loading image..." in screenshots.
- [ ] Replace Google Chrome / Chromedriver.
- [ ] Use latest Python 3.x version.
