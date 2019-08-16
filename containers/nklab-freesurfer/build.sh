#!/bin//bash
VER=`cat ./src/version | grep version | awk {'print $2'}`
sudo singularity build nklab-freesurfer-v${VER}.sif nklab-freesurfer-def 2>&1 | tee output.txt
