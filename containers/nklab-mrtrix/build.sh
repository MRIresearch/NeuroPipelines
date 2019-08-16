#!/bin//bash
VER=`cat ./src/version | grep version | awk {'print $2'}`
sudo singularity build nklab-mrtrix-v${VER}.sif nklab-mrtrix-def 2>&1 | tee output.txt
