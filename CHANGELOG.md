# CHANGELOG

## 20230210

- File `datasource.py`: disabled `map_parameters` since they don't work at all
- Nitpicking on missing capital letters at start of `print()`.

## 20230209

- File `screenshot.py`: fix "Loading image..." by explicitly setting `lang=en_US` and `user_agent=`.
- File `screenshot.py`: add `--hide-scrollbars`.
- File `tar1090config.js`: updated to reflect configfile `html/config.js` on the RPi.
- Use Chromium instead of Chrome (incl. `chromedriver`, version 103.0.5046.0).
- Replace Twitter with Mastodon: changed `tweet.png` to `toot.png`.
- Using `black` and `flake8` on some `*.py` files.
- Added `CHANGELOG.md`.
- Update `README.md`.

## 20230208

- File `aircraftdata.py`: replace `api.joshdouch.me` with `hexdb.io`.
- File `aircraftdata.py`: some other small updates.

## 20230207

- Update `config.sample.ini` with longer `tweet_template`.
- Fix spelling in file `aircraftdata.py`.

## Pre commit

- Add the most basic toot / Mastodon functionality to file `tracker.py`.\
  KISS principle: no additional Python modules needed.
