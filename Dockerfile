FROM ubuntu
RUN mkdir /data
# tz data will prompt for interactive Q&A which we dont want
ARG DEBIAN_FRONTEND=noninteractive
# INSTALL PYTHON AND DEPENDENCIES
RUN apt-get -y update && apt-get install -y build-essential \
										checkinstall \
										git \
										libreadline-gplv2-dev \
										libncursesw5-dev \
										libssl-dev \
										libsqlite3-dev \
										tk-dev \
										libgdbm-dev \
										libc6-dev \
										liblcms2-dev  \
										libtiff-dev \
										libpng-dev \
										libvips \
										libvips-dev \
										libz-dev \
										libbz2-dev \
										libjpeg-dev \
										openslide-tools \
										python3-openslide \
										wget \
										zlib1g-dev

RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz
RUN tar -xvf Python-3.6.8.tar.xz && cd Python-3.6.8 && ./configure && make && make install && cd /
RUN python3 -m pip install --upgrade pip
RUN pip3 install numpy Pillow pydicom datetime openslide-python pyvips pyaml

RUN git clone https://github.com/Steven-N-Hart/dicom_wsi.git
RUN cd dicom_wsi/dicom_wsi
ENV PYTHONPATH=dicom_wsi/dicom_wsi/mods/
