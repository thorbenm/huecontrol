#!/bin/bash

if [ $(date +%H) -lt 12 ]
then
    wakeup -t2 1m
else
    wakeup -s -t2 1m
fi
