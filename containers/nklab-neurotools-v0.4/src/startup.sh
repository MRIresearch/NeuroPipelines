#!/bin/bash
if [ -z $1 ]
then
  params="-h"
else
  params=$1
fi

if [ $params = "--version" -o $params = "-V" ]
	then
	more /opt/bin/version*
	exit
fi

if [ $params = "--help" -o $params = "-h"  ]
	then
	more /opt/bin/readme*
	exit
fi

# stable version of freesurfer sourced by default
export FREESURFER_HOME=/opt/freesurfer
export PATH=${FREESURFER_HOME}/bin:$PATH

# latest version of FSL sourced by default
export FSLDIR=/opt/fsl     
export FSL_DIR=/opt/fsl   
export PATH=${FSLDIR}/bin:$PATH

# if --dev parameter passed then prepare to source development version
if [ $params = "--dev" -o $params = "-D"  ]
	then
        export LD_LIBRARY_PATH=/opt/freesurfer-dev/lib/qt/lib/:${LD_LIBRARY_PATH}
	export FREESURFER_HOME=/opt/freesurfer-dev
	export PATH=${FREESURFER_HOME}/bin:$PATH
	shift
fi


if [ $params = "--hcp" -o $params = "-H"  ]
	then
        export FSLDIR=/opt/fsl-5.0.6
        export PATH=${FSLDIR}/bin:$PATH
	export FSL_DIR=/opt/fsl-5.0.6

	export FREESURFER_HOME=/opt/freesurfer-HCP
	export PATH=${FREESURFER_HOME}/bin:$PATH
	shift

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

. $FREESURFER_HOME/SetUpFreeSurfer.sh
. $FSLDIR/etc/fslconf/fsl.sh

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
