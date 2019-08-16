#!/bin/bash
VER=`cat ./src/version91 | grep version | awk {'print $2'}`
sudo singularity build nklab-fsl91-v${VER}.sif nklab-fsl91-def 2>&1 | tee output91.txt

