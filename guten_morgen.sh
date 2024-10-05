#!/bin/bash

if [ $(date +%H) -lt 12 ]
then
    wakeup -t2 3m
else
    wakeup -s -t2 3m
fi
