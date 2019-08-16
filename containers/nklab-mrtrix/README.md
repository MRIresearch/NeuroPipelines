#  Singularity 3.2.1 recipe for MRtrix 3.0 RC3 Neuroimaging software

The image can be built using Singularity build in singularity (version >= 2.4, preferably 3.0 or greater)

---

## Build Singularity Image

* You will need to have singularity (version >= 2.4 installed, preferably version 3.0 or greater). Simply clone this repository to a convenient directory.
* Navigate into the `nklab-mrtrix`directory and check that you have a Singularity definition file `nklab-mrtrix-def` and the directory `src`
* Confirm that `src` folder and all the files in `src` have full read and write privileges. if not then `sudo chmod -R 777 src` should accomplish this.
* Now simply build the image as  `sudo singularity build nklab-mrtrix.sif nklab-mrtrix-def` - note that the image name is assumed to be `nklab-mrtrix.sif` but this can be changed to a more convenient label. 

## Run Singularity Image
You can now run commands by simply appending them to the end of  `singularity run nklab-mrtrix.sif` So for example to run a mrtrix command like mrinfo directly the following would be entered: `singularity run nklab-mrtrix.sif mrinfo ....`


## Setting up custom environmental variables
You can add additional environmental variables to the container at startup.

When you pass the `--sourcepre` parameter the container looks for a bash file called `/opt/input/nklab-config-pre.sh`. You can achieve this by providing a file `nklab-config-pre.sh` in your current directory and running the container as 

`singularity run -B $PWD:/opt/input nklab-freesurfer-v##.sif --sourcepre recon-all`
