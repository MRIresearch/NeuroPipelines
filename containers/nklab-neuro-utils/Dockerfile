FROM ubuntu:xenial
MAINTAINER Chidi Ugonna<chidiugonna@email.arizona.edu>

# install pre-reqs
RUN apt-get update && apt-get install -y \	
	nano \
	wget \
	curl \
        dc \
	lsb-core \
	python-pip \
        libx11-6 \
        libgl1 \
        libgtk-3-0 \
        libgtk-3-dev \
        libsm6 \
        libxext6 \
        libxt6 \
        mesa-common-dev \
        freeglut3-dev \
        zlib1g-dev \
        libpng-dev \
        expat \
        unzip \
        libeigen3-dev \
        zlib1g-dev \
        libqt4-opengl-dev \
        libgl1-mesa-dev \
        software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
        tcsh \
        xfonts-base \
        python-qt4 \
        gsl-bin \
        gnome-tweak-tool \
        libjpeg62 \
        xvfb \
        vim \
        libglu1-mesa-dev \
        libglw1-mesa   \
        libxm4 \
        netpbm
RUN apt-get update && apt-get install -y \
        hdf5-tools \
        openmpi-bin \
        openmpi-doc \
        libopenmpi-dev \
        gfortran

RUN pip install numpy
RUN pip install scipy
RUN pip install nibabel
RUN pip install dicom
RUN pip install pydicom
RUN pip install sklearn

RUN apt-get install -y python3-pip

RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install nibabel
RUN pip3 install dicom
RUN pip3 install pydicom
RUN pip3 install sklearn

ENV LD_LIBRARY_PATH /.singularity.d/libs:/usr/lib:$LD_LIBRARY_PATH
ENV PATH /opt/bin:$PATH
ENV PATH /opt/bin/dcm2niix/bin:$PATH
ENV PATH /opt/bin/bidskit:$PATH


WORKDIR /tmp
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN echo "LANG=en_US.UTF-8" > /etc/locale.conf
RUN locale-gen en_US.UTF-8

RUN wget https://cmake.org/files/v3.10/cmake-3.10.0-rc1.tar.gz
RUN tar xz -f cmake-3.10.0-rc1.tar.gz
RUN rm cmake-3.10.0-rc1.tar.gz
RUN chmod +x /tmp/cmake-3.10.0-rc1
WORKDIR /tmp/cmake-3.10.0-rc1
RUN ./configure
RUN make
RUN make install
RUN ./bootstrap --prefix=/usr
RUN make
RUN make install


RUN mkdir /opt/bin
WORKDIR /opt/bin 

RUN apt-get install -y git

RUN git clone https://github.com/rordenlab/dcm2niix.git
WORKDIR dcm2niix
RUN mkdir build
WORKDIR build
RUN cmake .. && \
    make install 

COPY ./src/changePython2.sh /opt/bin
COPY ./src/changePython3.sh /opt/bin
COPY ./src/startup.sh /opt/bin
COPY ./src/readme /opt/bin
COPY ./src/version /opt/bin
COPY ./src/bidskit-adapted /opt/bin/bidskit
COPY ./src/nklab-bids-convert.py /opt/bin/


RUN mkdir /opt/output
RUN mkdir /opt/input
RUN mkdir /opt/work
WORKDIR /opt/data

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    mkdir -p /etc/sudoers.d && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

ENV USER developer
ENV HOME /home/developer

RUN chmod -R 777 /opt

ENTRYPOINT ["/opt/bin/startup.sh"]
