#  Introduction
This is a recipe file for installing specific versions of neuroimaging software in the singularity container nklab-neurotools-v0.4.sif. Please note that it is highly likely that the steps in the recipe file will need changes as links to dependencies become inaccessible or fundamental changes. 

# Changes 
There are a fewer changes from the original image which was initially built on 9/18/2019. These are minor changes and should not affect the reproducibility of the functionality of this image. You can view the original definition file at `nklab-neurotools-def-original`
* HCP Workbench (wbview and wbcommand) v1.3.2 replaced by v1.5.0 (v1.3.2 no longer accessible)
* Pip url changed from https://bootstrap.pypa.io/pip/get-pip.py to https://bootstrap.pypa.io/pip/3.5/get-pip.py (URL location changed)

# Contents
* FSL 6.0.1. The CUDA 8.0 toolkit libraries have also been installed allowing gpu compatible versions of eddy, bedpostx and probtraxck to be run.
* FSL 5.0.6 for HCP Processing
* The Duke Resting State fMRI pipeline is also included.
* MRtrix 3.0.0 RC 3
* latest Freesurfer development version will be included(/opt/freesurfer-dev)
* Stable freesurver 6.0 with applied patch (/opt/freesurfer) see notes: https://surfer.nmr.mgh.harvard.edu/fswiki/BrainVolStatsFixed
* The freesurfer version 5.3.0 used for HCP processing (/opt/freesurfer-HCP)
* HCP Workbench (wbview and wbcommand) v1.3.2
* HCP Pipelines v4.0.1
* ANTS v2.3.1
* Ciftify v2.1.0
* AFNI v19,2_14 'Claudius'
* ITK-SNAP v3.6.0 (This will need to be sourced separately before building the image)
 

The image can be built using Singularity build in singularity (version >= 2.4, preferably 3.0 or greater)

---

## Build Singularity Image

* You will need to have singularity (version >= 2.4 installed, preferably version 3.0 or greater). Simply clone this repository to a convenient directory.
* Navigate into the `nklab-neurotools-v0.4` directory and check that you have a Singularity definition file `nklab-neurotools-def` and the directory `src` 
* Download ITK-SNAP 3.6.0 (STABLE VERSION) as a **Linux Binary (64 bit)** called  `itksnap-3.6.0-20170401-Linux-x86_64.tar.gz` from [ITK-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php?n=Downloads.SNAP3) into the `src` directory.
* Now simply build the image as  `sudo singularity build nklab-neurotools-v0.4.sif nklab-neurotoolsf-def` - note that the image name is assumed to be `nklab-neurotools-v0.4.sif` but this can be changed to a more convenient label.

## Run Singularity Image
You can now run commands by simply appending them to the end of  `singularity run nklab-neurotools-v0.4.sif` So for example to run an FSL command like flirt directly the following would be entered: `singularity run nklab-neurotools-v0.4.sif flirt ....`

### Cuda Compatibility
* You can run Cuda-8.0 compatible executables by using the `--nv` parameter. The example provided next shows how to accomplish this with `eddy-cuda8.0`:
`singularity run --nv nklab-neurotools-v0.4.sif/opt/fsl/bin/eddy_cuda8.0 --imain=G1_1_OFF_28271_cgm --mask=G1_1_OFF_28271_cgm0_brain_mask --acqp=acqparams.txt --index=index.txt --bvecs=bvecs --bvals=bvals --out=G1_1_OFF_28271_cgm_eddy`

### Shell into Singularity Image
* You can also shell into the singularity image using: `singularity shell nklab-neurotools-v0.4.sif` and then run commands at the command line within the container.

Provided below are notes on specific aspects of the container that may be useful.

---

## Accessing different versions of FSL within the container
This container uses an enclosed startup script (see `startup.sh` in directory `src`) - this script allows the environment variables of the container to be managed.

* FSL v6.0.1 and Freesurfer v6.0.0 run as the default when you use `singularity run nklab-neurotools-v0.4.sif`. So for example to run `recon-all` in Freesurfer version v6.0.0 then just do `singularity run nklab-neurotools-v0.4.sif recon-all`
* to run the HCP version of FSL (v5.0.6) or Freesurfer (v5.3.0) then use `--hcp` as follows `singularity run nklab-neurotools-v0.4.sif --hcp flirt`
* When using FSL 5.0.6 some commands like `flirt` may write out an output matrix in hexadecimal format. You can convert these to decimal format using the script `/opt/bin/convertHex.sh`
* for freesurfer, a matlab source file is also available at `/opt/bin/startup.m` to be used with matlab scripts.
* to run the development version of Freesurfer  then use `--dev as follows `singularity run nklab-neurotools-v0.4.sif --dev recon-all`
* use `--ciftify` to source the correct version of `msm` for use in the ciftify pipeline

## Setting up custom environmental variables
The fsl and freesurfer environments are sourced within the startup script. To tweak the environment you can source scripts nefore (`--sourcepre`), after (`--sourcepost`) or both after and before (`--sourceboth`) the fsl scripts are run.

When you pass the `--sourcepre` parameter the container looks for a bash file called `/opt/input/nklab-config-pre.sh`. You can achieve this by providing a file `nklab-config-pre.sh` in your current directory and running the container as 

`singularity run -B $PWD:/opt/input nklab-fsltrixsurf-v##.sif --sourcepre recon-all`

The container parameters like `--dev`, `--sourcepre`, `--hcp` etc. are mutually exclusive. Only one parameter can be used at a time. The parameter `--sourceboth` gives you the most flexibility. It will source from `/opt/input/nklab-config-pre.sh` and `/opt/input/nklab-config-post.sh` just before the and after the fsl and freesurfer scripts are sourced.

---

## Resting State FMRI pipeline (Nan-kuei Chen/Duke University) 
Please refer to [https://wiki.biac.duke.edu/biac:analysis:resting_pipeline](https://wiki.biac.duke.edu/biac:analysis:resting_pipeline) for details of use.

### Introduction
The original python source  `resting_pipeline.py` available at at [https://wiki.biac.duke.edu/biac:analysis:resting_pipeline] has been slightly amended and is included in this repository in the folder `src`. These changes are:

* `data1` has been selectively converted to dtype `numpy.float64`
* slice indices have been cast as longs in certain instances.
* BXH functionality is ignored. To explicitly use BXH info pass the flag --ignorebxh=N

### Sliding window functionality
A new step has been added `-7sw` to enable sliding window functionality. In order to use this step you will need to use the `--slidewin` parameter which takes 2 numbers seperated by a comma. The 1st number is the window size in seconds and the second number is the shift in seconds between sequential windows. So for example `--slidewin=60,3` will use a window size of `60` seconds shifted by `3` seconds for each subsequent window. Keep in mind that the `--tr` (in milliseconds) parameter is required to calculate the number of volumes to use for each sliding window correlation. If you do not specify the --slidwin parameter and run step `7sw` then default values of `30,3` will be used. Sliding window files are exported to a new directory `SlidingWindow_W_S` and image files are consolidated into 4D volumes for viewing in FSL as a movie 

### Extensions to Slice Correction functionality
The pipeline has been extended to accept custom slice correction timing files. A python script make_fsl_stc.py has been bundled in this container which can take .json files created by dcm2niix. This python program will create a slice correction file with timing values and one with slices in order of acquisition. It can be called as follows:

`/opt/rsfmri_python/bin/make_fsl_stc.py fmri.json` where fmri.json is the json output from dcm2niix. custom names for the slice order and slice time files can be provided as parameters as follows:

`make_fsl_stc.py fmri.json  --slicenum=/path/num.txt --slicetime=/path/time.txt` otherwise these files default to `sliceorder.txt` and `slicetimes.txt` in the current directory.

Once these custom files have been created then they can be provided to the resting state pipeline using the full path as input to the `--sliceorder` parameter 
`--sliceorder=/path/num.txt`

please note that the default custom slice file expected uses slice order. If you pass a text file with slice times then you will need to use another parameter `--slicetimings=time` 


### Example Commands
#### Create Slice Timing files from json
`singularity run  -B $PWD:/opt/data nklab-neurotools-v0.4.sif /opt/rsfmri_python/bin/make_fsl_stc.py /opt/data/fmri.json`

#### Run pipeline (also runs sliding window with window-30s, shift=3s) using custom slice timing file
`singularity run  --rm  -B $PWD:/opt/data  nklab-neurotools-v0.4.sif  /opt/rsfmri_python/bin/resting_pipeline.py --func /opt/data/fmri-std-pre.nii.gz -o restoutput --steps=1,2,3,4,5,6,7,8 --slidewin=30,3 --sliceorder=/opt/data/slicetimes.txt --slicetiming=time --tr=3000`
