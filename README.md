# NeuroPipelines

Umbrella repository for managing and deploying neuroimaging pipelines and containers

## containers

[nklab-fsl](containers/nklab-fsl/README.md) This Singularity container provides FSL v6.0.1 (FSLeyes, BASIL). It is Cuda compatible and so should be able to run eddy_cuda8.0 or eddy_cuda9.1. It also includes FSL v5.0.6 for reproducing HCP pipelines.

[nklab-mrtrix](containers/nklab-mrtrix/README.md ) This Singularity container provides MRTrix 3.0 RC3

[nklab-freesurfer](containers/nklab-freesurfer/README.md ) This Singularity container provides 3 versions of freesurfer - the stable v6.0.0 version, the current development version (this will vary depending on the build date) and the HCP version 5.3.0 used in HCP pipelines.

[nklab-fsltrixsurf](containers/nklab-fsltrixsurf/README.md) This Singularity container is an amalgamation of the three containers (nklab-fsl, nklab-mrtrix and nklab-freesurfer)

[nklab-neuro-tools](containers/nklab-neuro-tools/README.md) This Singularity container provides a comprehensive package of neuroimaging tools like FSL, MRtrix, AFNI, The HCP Pipelines, CIFTIFY, ANTS in one container.  

[nklab-simnibs](containers/nklab-simnibs/README.md) A Singularity Container for SIMNIBS 2.1 for the Simulation of electric fields induced by TMS and tDCS   

[nklab-neuro-utils](containers/nklab-neuro-utils/README.md) A Singularity/Docker container for converting MRI files into BIDS format 

## Data utilities

[dicomutils](dicomutils/README.md) working python code to transfer/route dicoms to XNAT.  
 

