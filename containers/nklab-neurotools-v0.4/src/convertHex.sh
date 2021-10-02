#!/bin/bash
# Copyright Paul McCarthy
# (see www.jiscmail.ac.uk/cgi-bin/webadmin?A2=fsl;8e169ec1507)
infile=$1

while read line; do

for number in $line; do
printf "%f " "$number"
done
echo
done < $infile


