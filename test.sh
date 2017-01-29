#!/bin/bash
# python -m SimpleHTTPServer &
# sleep 1
export PYTHONPATH='.'
RESULT='pgrep -f SimpleHTTPServer'
python2.7 ./location_generator.py
echo '!!!!'
