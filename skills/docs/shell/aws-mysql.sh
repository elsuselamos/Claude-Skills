#!/bin/zsh

ssh -i "/Users/tommy/Documents/work.nosync/yudady/g-work/dayooint.com/dtg-stage-key/DTG-TEST-IT.pem" -f -N -L \
3307:dtg-mysql-test-2.cn8o8wwuc4lb.ap-southeast-1.rds.amazonaws.com:3306 \
ubuntu@13.228.187.227 -v