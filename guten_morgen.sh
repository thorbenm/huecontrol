#!/bin/bash

if [ $(date +%H) -lt 12 ]
then
    wakeup -t2 1m
else
    wakeup -s -k -t2 1m
fi
