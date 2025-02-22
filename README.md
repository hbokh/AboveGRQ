# ✈️ Above GRQ

*An ADS-B Bot, derived from [AboveTustin](https://github.com/kevinabrandon/AboveTustin) (a Twitter bot).*

Posts to Bluesky from wiedehopf/[tar1090](https://github.com/wiedehopf/tar1090).

Uses [dump1090-fa](https://github.com/flightaware/dump1090) to track airplanes and toots whenever an airplane flies nearby Groningen Airport Eelde (IATA: **[GRQ](https://www.wikiwand.com/en/Groningen_Airport_Eelde)**, ICAO: **EHGG**).

**WARNING**: this is [Frankencode](https://www.urbandictionary.com/define.php?term=Frankencode)!!\
Currently it runs on my MacBook Pro M2 (macOS 15.3.1, with Homebrew packages).

## Install

Install "AboveGRQ" in a Python virtualenv.\
Copy the file `config.sample.ini` to `config.ini` and make all the necessary changes in that file.\
Run with `python3 tracker.py`:

```console
(AboveGRQ) hbokh@rpi4:~/.virtualenvs/AboveGRQ$ python3 tracker.py
Will crop
Map URL: http://rpi3.internal/tar1090/?enablelabels
Getting web page http://rpi3.internal/tar1090/?enablelabels
Waiting for page to load...
Reset map
Zoom in
Now: 2024-02-10 16:27:50.600000
Now: 2024-02-10 16:27:51.600000
Now: 2024-02-10 16:27:52.700000
--- cut --- 8< ---
```

## Screenshot

Obligatory screenshot, taken from [Ivory](https://tapbots.com/ivory/) for iOS:

![IMG_0189](https://user-images.githubusercontent.com/519955/217902537-7371c254-55d5-4ccc-a179-db6b1c48c952.jpg)

## Dependencies

- Use Python 3.1x and [venv](https://docs.python.org/3/library/venv.html).
- Use a Firefox based browser.
- Uses [tar1090](https://github.com/wiedehopf/tar1090) for ADSB message decoding, airplane tracking, and webserving.
- Uses [selenium](https://pypi.python.org/pypi/selenium) for screenshots with geckodriver.
- Uses [pillow](https://python-pillow.org/) for image processing.
- Uses [requests](https://pypi.org/project/requests/) for API calls.
- Uses [geckodriver](https://github.com/mozilla/geckodriver) for headless web browsing.
- Builds on a running [PiAware](https://flightaware.com/adsb/piaware/build) Raspberry Pi-based ADS-B receiver and decoder with MLAT support, with web server and local databases.

## Code borrowed from

- kevinabrandon/[AboveTustin](https://github.com/kevinabrandon/AboveTustin)
- shbisson/[OverPutney](https://github.com/shbisson/OverPutney)
- ladewig/[OverPutney](https://github.com/ladewig/OverPutney)
- ggoodloff/[AnyFlightTracker](https://github.com/ggoodloff/AnyFlightTracker/)

## Todo

- [ ] Make hashtags work with "facets".
- [ ] Remove FlightAware API / FlightXML3 code.
- [x] Replace Mastodon with Bluesky.
- [x] Replace Twitter with Mastodon.
- [x] Fix "Loading image..." in screenshots when in headless mode.
- [x] Replace Google Chrome / Chromedriver.
- [X] Use latest Python 3.x version.

## Notes

To enable tar1090 web screenshots, the tar1090 `config.js` on the rpi needs to be edited.
Edit file `/<dir>/tar1090/html/config.js` and remark out (`//`) the ICAO line in the `HideCols` section.
