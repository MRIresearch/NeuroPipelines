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
$*
