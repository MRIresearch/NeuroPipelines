#!/bin/bash
dockerimg=orbisys/nklab-neuro-utils
workdir=$PWD
mountworkdir=/opt/data

dicomdir=${mountworkdir}/unencrypted
stagedir=${mountworkdir}/stagedbids
bidsdir=${mountworkdir}/origdata

sessions="--sessions pre post"
logname="--logname bidconvert-CORT-log"
translator="--bidstranslator ${mountworkdir}/Protocol_Translator.json"
exception="--exceptionlist ${mountworkdir}/exception.json"

docker run --rm -v ${workdir}:${mountworkdir} $dockerimg python3 -u /opt/bin/nklab-bids-convert.py $dicomdir $stagedir $bidsdir $sessions --workdir $mountworkdir $logname --noprompt --bypass --incremental $translator $exception


