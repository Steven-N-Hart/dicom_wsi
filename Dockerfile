FROM ubuntu
RUN mkdir /data
# tz data will prompt for interactive Q&A which we dont want
ARG DEBIAN_FRONTEND=noninteractive
# INSTALL PYTHON AND DEPENDENCIES
RUN apt-get -y update && apt-get install -y build-essential checkinstall cmake default-jdk git libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev liblcms2-dev libtiff-dev libpng-dev libvips libvips-dev libz-dev libbz2-dev libjpeg-dev openslide-tools unzip python3-openslide wget xutils-dev zlib1g-dev

RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz
RUN tar -xvf Python-3.6.8.tar.xz && cd Python-3.6.8 && ./configure && make && make install && cd /
RUN python3 -m pip install --upgrade pip
RUN pip3 install numpy Pillow pydicom datetime openslide-python pyvips pyaml

RUN git clone https://github.com/Steven-N-Hart/dicom_wsi.git
RUN cd dicom_wsi && pip install -r requirements.txt
ENV PYTHONPATH=/dicom_wsi/dicom_wsi/mods/

# Add other tools
#Google
RUN wget https://github.com/GoogleCloudPlatform/wsi-to-dicom-converter/releases/download/v1.0.3/wsi2dcm_1.0.3.deb
RUN apt install ./wsi2dcm_1.0.3.deb

# Orthanc
RUN wget -O Orthanc.tar.gz https://www.orthanc-server.com/downloads/get.php?path=/whole-slide-imaging/OrthancWSI-0.7.tar.gz
RUN tar xvzf Orthanc.tar.gz
RUN cd OrthancWSI-0.7/
RUN mkdir /OrthancWSI-0.7/Applications/Build
RUN cd /OrthancWSI-0.7/Applications/Build
RUN cmake /OrthancWSI-0.7/Applications -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
RUN make
RUN mkdir /OrthancWSI-0.7/ViewerPlugin/Build
RUN cd /OrthancWSI-0.7/ViewerPlugin/Build
RUN cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
RUN make

ENV ORTHANC=/OrthancWSI-0.7/Applications/Build
RUN cd /

# Clunie's Tools
RUN wget -O D3TOOLS.tar.bz https://www.dclunie.com/dicom3tools/workinprogress/dicom3tools_1.00.snapshot.20200716155940.tar.bz2
RUN tar xjvf D3TOOLS.tar.bz
RUN cd dicom3tools_1.00.snapshot.20200716155940/ && ./Configure
RUN cd dicom3tools_1.00.snapshot.20200716155940/ && imake -I./config -DInstallInTopDir -DUseXXXXID
RUN cd dicom3tools_1.00.snapshot.20200716155940/ && make World
RUN cd dicom3tools_1.00.snapshot.20200716155940/ && make install
ENV PATH=$PATH:$PWD/bin/1.4.9.184.x8664/
RUN cd /

ENV alias python=python3
