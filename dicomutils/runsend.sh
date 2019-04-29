#!/bin/bash
DICOMDIR=/media/chidi/Pluto/0_PROJECTS/CORT/BIDS-conversion/Debug_20190420/imacpsych-bidsconvert/xnat-test/teststagedbids
CONFIG=/media/chidi/UBUNTU-SHARE/Dropbox/repos/MRIresearch/NeuroPipelines/dicomutils/config.json
python -m pdb dicomSend.py $DICOMDIR --config  $CONFIG
