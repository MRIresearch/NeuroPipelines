#  Singularity 3.2.1 recipe for Freesurfer 

Singularity container with: 
    latest Freesurfer development version (/opt/freesurfer-dev)
    Stable freesurver 6.0 with applied patch (/opt/freesurfer) see notes: https://surfer.nmr.mgh.harvard.edu/fswiki/BrainVolStatsFixed
    The freesurfer version 5.3.0 used for HCP processing (/opt/freesurfer-HCP)

Please refer to https://github.com/MRIresearch/NeuroPipelines/blob/master/containers/nklab-fsl/README.md for more information about this container.

---

## Build Singularity Image

* You will need to have singularity (version >= 2.4 installed, preferably version 3.0 or greater). Simply clone this repository to a convenient directory.
* Navigate into the `nklab-freesurfer`directory and check that you have a Singularity definition file `nklab-freesurfer-def` and the directory `src`
* Confirm that `src` folder and all the files in `src` have full read and write privileges. if not then `sudo chmod -R 777 src` should accomplish this.
* Now simply build the image as  `sudo singularity build nklab-freesurfer.sif nklab-freesurfer-def` - note that the image name is assumed to be `nklab-freesurfer.sif` but this can be changed to a more convenient label.
* Using the build script `build.sh` will do above but will also append a version number from the version file to the name of the image as for example `nklab-freesurfer-v0.2` 

## Run Singularity Image
You can now run commands by simply appending them to the end of  `singularity run nklab-freesurfer.sif` So for example to run a freesurfer command like recon-all directly the following would be entered: `singularity run nklab-freesurfer.sif recon-all ....`

---

## Accessing different versions of freesurfer within the container
This container uses an enclosed startup script (see `startup.sh` in directory `src`) - this script allows the environment variables of the container to be managed.

* Freesurfer v6.0.0 runs as the default when you use `singularity run nklab-freesurfer-v##.sif`. So for example to run recon-all version v6.0.0 then just do `singularity run nklab-freesurfer-v##.sif recon-all`
* to run the development version of freesurfer use`--dev` as follows `singularity run nklab-freesurfer-v##.sif --dev recon-all`
* to run the HCP version of freesurfer use`--hcp as follows `singularity run nklab-freesurfer-v##.sif --hcp recon-all`

## Setting up custom environmental variables
The freesurfer environment is sourced within the startup script. To tweak the environment you can source scripts nefore (`--sourcepre`), after (`--sourcepost`) or both after and before (`--sourceboth`) the freesurfer scripts are run.

When you pass the `--sourcepre` parameter the container looks for a bash file called `/opt/input/nklab-config-pre.sh`. You can achieve this by providing a file `nklab-config-pre.sh` in your current directory and running the container as 

`singularity run -B $PWD:/opt/input nklab-freesurfer-v##.sif --sourcepre recon-all`

The container parameters like `--dev`, `--sourcepre`, `--hcp` etc. are mutually exclusive. Only one parameter can be used at a time. The parameter `--sourceboth` gives you the most flexibility. It will source from `/opt/input/nklab-config-pre.sh` and `/opt/input/nklab-config-post.sh` just before and after the freesurfer scripts are sourced.


