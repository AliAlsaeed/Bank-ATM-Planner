#!/bin/bash
if [ "$#" -lt 1 ]; then
    echo "Wrong Arguments"
else
    python2.7 ./location_generator.py
    python3.5 ./dbscan_cluster.py
    ServerID=$(pgrep -f SimpleHTTPServer)
    kill $ServerID
    python -m SimpleHTTPServer &
    sleep 1
    if [ "$1" -eq 1 ]; then
        python -m webbrowser "localhost:8000/googleMapsCluster.html"
    elif [ "$1" -eq 2 ]; then
        python -m webbrowser "localhost:8000/googleMapsHeatMap.html"
    else
        python -m webbrowser "localhost:8000/googleMapsDBSCAN.html"
    fi
fi
