#!/bin/zsh

ssh -i "/Users/tommy/Documents/work.nosync/yudady/g-work/dayooint.com/dtg-stage-key/DTG-TEST-IT.pem" -f -N -L \
27018:dtg-dcdb-test.cluster-cn8o8wwuc4lb.ap-southeast-1.docdb.amazonaws.com:27017 \
ubuntu@13.228.187.227 -v