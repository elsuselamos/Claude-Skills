#!/bin/zsh

ssh -i "/Users/tommy/Documents/work.nosync/yudady/g-work/dayooint.com/dtg-stage-key/DTG-TEST-IT.pem" -f -N -L \
6380:dtg-redis-test-notls.qebi7j.clustercfg.memorydb.ap-southeast-1.amazonaws.com:6379 \
ubuntu@13.228.187.227 -v