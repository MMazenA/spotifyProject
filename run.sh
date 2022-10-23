#!/bin/bash
echo "Terminating any active sessions"
sh ./terminate.sh

screen -L -Logfile /logs/api.log -dmS api python3 ./t/api.py  
sleep 5
screen -L -Logfile /logs/tracker.log -dmS sptfy python3 ./spotifyTracker/__main__.py 
echo "API and Tracker active"
screen -list
sh ./announce.sh




