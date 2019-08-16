#!/bin/bash
if [ -z $1 ]
then
  params="-h"
else
  params=$1
fi

if [ $params = "--version" -o $params = "-V" ]
	then
	more /opt/bin/version
	exit
fi

if [ $params = "--help" -o $params = "-h"  ]
	then
	more /opt/bin/readme
	exit
fi

if [ $params = "--hcp" -o $params = "-H"  ]
	then
	export FREESURFER_HOME=/opt/freesurfer-HCP
	export PATH=${FREESURFER_HOME}/bin:$PATH

        export FSLDIR=/opt/fsl-5.0.6
	export FSL_DIR=/opt/fsl-5.0.6 
        export PATH=${FSL_DIR}/bin:$PATH

	shift
else
        export FREESURFER_HOME=/opt/freesurfer-dev
        export PATH=${FREESURFER_HOME}/bin:$PATH

        export FSLDIR=/opt/fsl     
        export FSL_DIR=/opt/fsl
        export PATH=${FSL_DIR}/bin:$PATH
fi

if [ $params = "--sourcepre" -o $params = "-r"  ]
	then
	. /opt/config/nklab-config-pre.sh
	shift 
fi

if [ $params = "--sourceboth" -o $params = "-b"  ]
	then
	. /opt/config/nklab-config-pre.sh
fi

. $FSLDIR/etc/fslconf/fsl.sh
. $FREESURFER_HOME/SetUpFreeSurfer.sh

if [ $params = "--ciftify" -o $params = "-C" ]
	then
	export PATH=/opt/msm_hocr_v2:$PATH
	shift
fi

if [ $params = "--sourcepost" -o $params = "-p"  ]
	then
	. /opt/config/nklab-config-post.sh
	shift 
fi
if [ $params = "--sourceboth" -o $params = "-b"  ]
	then
	. /opt/config/nklab-config-post.sh
	shift 
fi

$*
