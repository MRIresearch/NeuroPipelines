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
	more /opt/bin/readme*
	exit
fi

# stable version of freesurfer sourced by default
export FREESURFER_HOME=/opt/freesurfer
export PATH=${FREESURFER_HOME}/bin:$PATH

# if --dev parameter passed then prepare to source development version
if [ $params = "--dev" -o $params = "-D"  ]
	then
	export FREESURFER_HOME=/opt/freesurfer-dev
	export PATH=${FREESURFER_HOME}/bin:$PATH
	shift
fi

# HCP version of freesurfer 5.3.0
if [ $params = "--hcp" -o $params = "-H"  ]
	then
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
