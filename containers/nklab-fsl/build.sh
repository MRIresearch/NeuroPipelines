#!/bin/bash
VER=`cat ./src/version | grep version | awk {'print $2'}`
sudo singularity build nklab-fsl-v${VER}.sif nklab-fsl-def 2>&1 | tee output.txt

