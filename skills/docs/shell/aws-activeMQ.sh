#!/bin/zsh

ssh -i "/Users/tommy/Documents/work.nosync/yudady/g-work/dayooint.com/dtg-stage-key/DTG-TEST-IT.pem" -f -N -L \
8163:b-27971fd9-1dfc-4a09-aef3-96c00509b5e8-1.mq.ap-southeast-1.amazonaws.com:8162 \
ubuntu@13.228.187.227 -v