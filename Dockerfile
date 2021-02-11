FROM ubuntu
RUN mkdir /data
# tz data will prompt for interactive Q&A which we dont want
ARG DEBIAN_FRONTEND=noninteractive
# INSTALL PYTHON AND DEPENDENCIES
RUN apt-get -y update && apt-get install -y build-essential python3.6 python3-pip python3-dev cython3 checkinstall cmake default-jdk git libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev liblcms2-dev libtiff-dev libpng-dev libvips libvips-dev libz-dev libbz2-dev libjpeg-dev openslide-tools unzip python3-openslide wget xutils-dev zlib1g-dev libopenjp2-7-dev  python3-gdcm
RUN pip3 install git+https://github.com/Who8MyLunch/CharPyLS

RUN git clone https://github.com/Steven-N-Hart/dicom_wsi.git
RUN cd dicom_wsi && pip3 install -r requirements.txt && cd /
ENV PYTHONPATH=$PYTHONPATH:/dicom_wsi/dicom_wsi/mods/
#
## Add other tools
## Google
#RUN wget https://github.com/GoogleCloudPlatform/wsi-to-dicom-converter/releases/download/v1.0.3/wsi2dcm_1.0.3.deb
#RUN apt install ./wsi2dcm_1.0.3.deb
#
## Orthanc
#RUN wget -O Orthanc.tar.gz https://www.orthanc-server.com/downloads/get.php?path=/whole-slide-imaging/OrthancWSI-0.7.tar.gz
#RUN tar xvzf Orthanc.tar.gz
#RUN cd OrthancWSI-0.7/
#RUN mkdir /OrthancWSI-0.7/Applications/Build
#RUN cd /OrthancWSI-0.7/Applications/Build
#RUN cmake /OrthancWSI-0.7/Applications -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
#RUN make
#RUN mkdir /OrthancWSI-0.7/ViewerPlugin/Build
#RUN cd /OrthancWSI-0.7/ViewerPlugin/Build
#RUN cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
#RUN make
#
#ENV ORTHANC=/OrthancWSI-0.7/Applications/Build
#RUN cd /
#
## Clunie's Tools
#RUN wget -O D3TOOLS.tar.bz https://www.dclunie.com/dicom3tools/workinprogress/dicom3tools_1.00.snapshot.20201208085311.tar.bz2
#RUN tar xjvf D3TOOLS.tar.bz
#RUN cd dicom3tools_1.00.snapshot.20201208085311/ && ./Configure
#RUN cd dicom3tools_1.00.snapshot.20201208085311/ && imake -I./config -DInstallInTopDir -DUseXXXXID
#RUN cd dicom3tools_1.00.snapshot.20201208085311/ && make World
#RUN cd dicom3tools_1.00.snapshot.20201208085311/ && make install
#ENV PATH=$PATH:$PWD/bin/1.4.9.184.x8664/
#RUN cd /
#
#ENV alias python=python3
