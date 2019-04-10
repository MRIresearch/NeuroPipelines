#  nklab-neuro-utils
A number of utilities for data management. Will be updated as time goes by.

* `./src/nklab-bids-convert.py` utility to stage dicoms for conversion by `bidskit` (https://github.com/jmtyszka/bidskit) into BIDS format.

## nklab-bids-convert.py
This utility will walk down the hierarchy of dicom data (`dicomdir`) and will copy it to a new directory (`stagedir`) in the required format for Bidskit to convert into BIDS format. It is important that the dicom data is contained within one folder for each subject. If the data has been collected in multiple sessions then the parameter `--sessions` can be used to prompt the tool to cluster (K-means) the dicoms based on the acquired datetime. For example `--sessions pre post` would copy the dicom data into 2 sessions pre and post for bidskit. In some situations the acquired datetime may be incorrect and thus lead to incorrect clustering. An exceptions file `--exceptionlist` may then be provided to associate a misclassified dicom with one that has the correct datetime. See `./example/exception.json` for an example that associates the misclassified `3SHELL_TENSOR` with `3SHELL_RPE` . Note that the string values in the exception file are substrings of the actual dicom folder names that allow for unique identification. A frozen version of bidskit is also included with this repository which has been slightly adapted for our lab's needs. Please run the tool with the flag `--stageonly` to avoid running this version of bidskit and to just run the dicom preparation steps described above.

## Build Singularity Image

* You will need to have singularity 2.4 or greater installed. Simply clone this repository to a convenient directory.
* Navigate into the `nklab-neuro-utils`directory and check that you have a Singularity definition file `Singularity` and the directory `src`
* Confirm that `src` folder and all the files in `src` have full read and write privileges. if not then `sudo chmod -R 777 src` should accomplish this.
* Now simply build the image as  `sudo singularity build nklab-neuro-utils.simg Singularity` - note that the image name is assumed to be `nklab-neuro-utils.simg` but this can be changed to a more convenient label. 

## Build local Docker Image
* At the moment the docker image is retrievable from docker hub using `docker pull orbisys/nklab-neuro-utils`

## Build local Docker Image

* Simply clone this repository to a convenient directory.
* Navigate into the `nklab-neuro-utils`directory and check that you have the Docker definition file `Docker` and the directory `src`
* Confirm that `src` folder and all the files in `src` have full read and write privileges. if not then `sudo chmod -R 777 src` should accomplish this.
* Now simply build the image as  `sudo docker build -t mylocaldockerimage Docker`  

