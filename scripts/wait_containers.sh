#!/bin/bash
running="false"
while [ "$running" != "true" ]
do 
    running="$(sudo docker inspect -f {{.State.Running}} backend-aitenea)"
    sleep 1;
done

sleep 15
