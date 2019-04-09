#!/bin/bash

#cortical references
#https://www.lead-dbs.org/helpsupport/knowledge-base/atlasesresources/cortical-atlas-parcellations-mni-space/

#subcortical references
#https://www.lead-dbs.org/helpsupport/knowledge-base/atlasesresources/atlases/



#download HCP cortical parcellation from schaeffer
cd atlasSource/schaeffer2018
wget https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI/Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz
wget https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI/Schaefer2018_100Parcels_7Networks_order.txt
wget https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI/Schaefer2018_100Parcels_7Networks_order.lut

#manually download DISTAL atlas from https://www.lead-dbs.org/helpsupport/knowledge-base/atlasesresources/atlases
#manually download FSL Harvard SubCORT
cd atlasSource/HarvardSC
cp /home/chidi/share/fsl-6/data/atlases/HarvardOxford/HarvardOxford-sub-maxprob-thr0-1mm.nii.gz .
cp /home/chidi/share/fsl-6/data/atlases/HarvardOxford-Subcortical.xml .
