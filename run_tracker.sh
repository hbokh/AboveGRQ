#!/usr/bin/env bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.

cd $HOME/.virtualenvs/AboveGRQ || exit
source bin/activate

while :
do
	echo
	echo '***** Restarting AboveGRQ ' `date --utc --rfc-3339=ns`
	echo

	python3 tracker.py

	echo
	echo '***** AboveGRQ exited ' `date --utc --rfc-3339=ns`
	echo

	sleep 60  # Don't restart too quick so there is time to kill
done
