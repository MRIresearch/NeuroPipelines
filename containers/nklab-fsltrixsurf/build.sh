#!/bin/bash
VER=`cat ./src/version | grep version | awk {'print $2'}`
sudo singularity build nklab-fsltrixsurf-v${VER}.sif nklab-fsltrixsurf-def 2>&1 | tee output.txt

