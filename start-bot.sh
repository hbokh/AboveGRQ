#!/usr/bin/env bash

rm -f nohup.out
nohup ./run_tracker.sh </dev/null >/dev/null 2>&1 &
