#!/bin/bash
awk '{if(FNR==1)print $0;if(FNR==2)print "id" "," $0;if(FNR>2 && $0)print FNR-2 "," $0}END{print ""}' $1 > $1"_indexed"
