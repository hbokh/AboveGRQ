# CHANGELOG

## 20230214

- Minor updates.

## 20230213

- File `aircraftdata.py`: fixed attribute errors. Now also toot when hexdb.io gives a "n/a" (error 404).
- File `screenshot.py`: personal tweak for `#ProbablyLanding` tag when plane approaches GRQ / EHGG for landing.

## 20230212

- All Python files are now `flake8` valid.
- Added GitHub Action for `flake8` linting.
- File `config.sample.ini`: update FlightAware API information.
- File `aircraftdata.py`: another try to fix attribute errors when `regis.text =` etc. is empty.

## 20230211

- More nitpicking on text.
- File `aircraftdata.py`: try to fix attribute errors when `regis.text =` etc. is empty.

```python
Time to toot!
Exception in Toot():
Traceback (most recent call last):
  File "/Users/username/.virtualenvs/AboveGRQ/tracker.py", line 274, in <module>
    Tweet(a[0], havescreenshot)
  File "/Users/username/.virtualenvs/AboveGRQ/tracker.py", line 61, in Tweet
    templateArgs["regis"] = aircraftdata.regis(a.hex)
  File "/Users/username/.virtualenvs/AboveGRQ/aircraftdata.py", line 15, in regis
    regis.text = ""
AttributeError: can't set attribute
```

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
