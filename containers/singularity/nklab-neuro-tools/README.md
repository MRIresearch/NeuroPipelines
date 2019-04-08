#  Singularity image containing Neuroimaging software
This Singularity image will be about 20GB when built using Singularity 2.4+. It comes with FSL 5.10 including eddy_cuda8.0, Mrtrix 3RC2, Freesurfer 6.0.0, Afni 18.0.21, ANTS 2.2.0, MRIQC v0.1, Julia v0.6.1 and The Duke Resting State fMRI pipeline. It also has CUDA 8.0 toolkit libraries installed.

The image can be built using Singularity build in singularity2.5+

---

## Build Singularity Image

* You will need to have singularity 2.4+ installed. Simply clone this repository to a convenient directory.
* Navigate into the `nklab-neuro-tools`directory and check that you have a Singularity definiton file `Singularity` and the directory `src`
* Confirm that `src` folder and all the files in `src` have full read and write privileges. if not then `sudo chmod -R 777 src` should accomplish this.
* Now simply build the image as  `sudo singularity build nklab-neuro-tools.simg Singularity` - note that the image name is assumed to be `nklab-neuro-tools.simg` but this can be changed to a more convenient label. 

## Run Singularity Image
You can now run commands by simply appending them to the end of  `singularity run nklab-neuro-tools.simg` So for example to run an FSL command like flirt directly the following would be entered: `singularity run nklab-neuro-tools.simg flirt ....`

### Cuda Compatibility
* You can run Cuda-8.0 compatible executables by using the `--nv` parameter. The example provided next shows how to accomplish this with `eddy-cuda8.0`:
`singularity run --nv rsfmri.img /opt/fsl/bin/eddy_cuda8.0 --imain=G1_1_OFF_28271_cgm --mask=G1_1_OFF_28271_cgm0_brain_mask --acqp=acqparams.txt --index=index.txt --bvecs=bvecs --bvals=bvals --out=G1_1_OFF_28271_cgm_eddy`

### Shell into Singularity Image
* You can also shell into the singularity image using: `singularity shell nklab-neuro-tools.simg` and then run commands at the command line within the container.

Provided below are notes on specific aspects of the container that may be useful.

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
`singularity run  -B $PWD:/opt/data nklab-neuro-tools.simg /opt/rsfmri_python/bin/make_fsl_stc.py /opt/data/fmri.json`

#### Run pipeline (also runs sliding window with window-30s, shift=3s) using custom slice timing file
`singularity run  --rm  -B $PWD:/opt/data  nklab-neuro-tools.simg  /opt/rsfmri_python/bin/resting_pipeline.py --func /opt/data/fmri-std-pre.nii.gz -o restoutput --steps=1,2,3,4,5,6,7,8 --slidewin=30,3 --sliceorder=/opt/data/slicetimes.txt --slicetiming=time --tr=3000`