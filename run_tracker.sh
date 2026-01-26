#!/usr/bin/env bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.

cd $HOME/.virtualenvs/AboveGRQ || exit
source .venv/bin/activate

while :
do
	echo
	echo '***** Restarting AboveGRQ ' `date -u`
	echo

	uv run tracker.py

	echo
	echo '***** AboveGRQ exited ' `date -u`
	echo

	sleep 60  # Don't restart too quick so there is time to kill
done
