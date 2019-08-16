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

if [ $params = "--sourcepre" -o $params = "-r"  ]
	then
	. /opt/config/nklab-config-pre.sh
	shift 
fi

if [ $params = "--sourceboth" -o $params = "-b"  ]
	then
	. /opt/config/nklab-config-pre.sh
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
