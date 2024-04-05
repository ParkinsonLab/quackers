#FROM continuumio/anaconda3
#version 1.0.0: 

FROM ubuntu:22.04
MAINTAINER Billy Law

ENV TZ=America/Canada
ENV DEBIAN_FRONTEND=noninteractive



RUN apt-get update \
&& apt-get -y install wget \
&& apt-get -y install unzip \
&& apt-get -y install g++ \
&& apt-get -y install gcc \
&& apt-get -y install make \
&& apt-get install -y valgrind \
&& apt-get install -y heaptrack \
&& apt-get install -y nano \
&& apt-get install -y libgsl-dev \
&& apt-get install -y libncurses5-dev \
&& apt-get install -y libbz2-dev \
&& apt-get install -y liblzma-dev

RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN echo 'alias python="python3"' >> ~/.bashrc
#this line is necessary for concoct due to some annoying artifact.
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip install numpy 
RUN pip install Cython



WORKDIR /quackers_tools
RUN wget https://github.com/voutcn/megahit/releases/download/v1.2.9/MEGAHIT-1.2.9-Linux-x86_64-static.tar.gz \
&& tar zvxf MEGAHIT-1.2.9-Linux-x86_64-static.tar.gz

RUN wget https://github.com/BinPro/CONCOCT/archive/refs/tags/1.1.0.tar.gz -O concoct.tar.gz\
&& tar xzvf concoct.tar.gz 
WORKDIR /quackers_tools/CONCOCT-1.1.0
RUN python3 setup.py install

WORKDIR /quackers_tools
RUN wget http://eddylab.org/software/hmmer/hmmer.tar.gz \
&& tar -xzvf hmmer.tar.gz 
WORKDIR hmmer-3.4
RUN sh configure && make 

WORKDIR /quackers_tools
RUN wget https://github.com/hyattpd/Prodigal/archive/refs/tags/v2.6.3.zip -O prodigal.zip \
&& unzip prodigal.zip
WORKDIR Prodigal-2.6.3
RUN make 

WORKDIR /quackers_tools
RUN wget https://compsysbio.org/metawrap_mod/metawrap_modules.tar.gz \
&& tar -xzvf metawrap_modules.tar.gz

RUN wget https://compsysbio.org/metawrap_mod/metawrap_scripts.tar.gz \
&& tar -xzvf metawrap_scripts.tar.gz

WORKDIR /quackers_tools
RUN wget https://github.com/Ecogenomics/GTDBTk/archive/refs/tags/2.3.2.zip -O gtdbtk.zip \
&& unzip gtdbtk.zip 

RUN wget https://github.com/BenLangmead/bowtie2/releases/download/v2.5.3/bowtie2-2.5.3-linux-x86_64.zip -O bowtie2.zip \
&& unzip bowtie2.zip \
&& mv bowtie2-2.5.3-linux-x86_64 bowtie2

RUN wget https://github.com/samtools/samtools/releases/download/1.19.2/samtools-1.19.2.tar.bz2 -O samtools.tar.bz2 \
&& tar -xvf samtools.tar.bz2 


WORKDIR samtools-1.19.2
RUN sh configure \
&& make \
&& make install


# Install AdapaterRemoval
WORKDIR /quackers_tools
RUN wget https://github.com/MikkelSchubert/adapterremoval/archive/v2.1.7.tar.gz -O adapterremoval.tar.gz \
&& tar -xzvf adapterremoval.tar.gz \ 
&& mv adapterremoval-2.1.7 adapterremoval \
&& cd adapterremoval \
&& make && mv build/AdapterRemoval /quackers_tools/adapterremoval/ 


# Install CD-HIT-DUP (from auxtools)
RUN wget https://github.com/weizhongli/cdhit/releases/download/V4.6.8/cd-hit-v4.6.8-2017-1208-source.tar.gz -O cdhit.tar.gz \
&& tar --remove-files -xzvf cdhit.tar.gz \
&& rm cdhit.tar.gz \
&& mkdir cdhit_dup \ 
&& cd cd-hit-v4.6.8-2017-1208/ \ 
&& make \
&& mv cd-hit-auxtools/cd-hit-dup /quackers_tools/cdhit_dup/ \
&& cd /quackers_tools \
&& rm -r cd-hit-v4.6.8-2017-1208

WORKDIR /quackers_tools
RUN mv CONCOCT-1.1.0 concoct \
&& mv hmmer-3.4 hmmer \
&& mv Prodigal-2.6.3 prodigal \
&& mv MEGAHIT-1.2.9-Linux-x86_64-static megahit \
&& mv samtools-1.19.2 samtools \
&& mv GTDBTk-2.3.2 gtdbtk 

WORKDIR /quackers_tools
RUN wget http://compsysbio.org/quackers_deps/BBMap_39.06.tar.gz -O bbmap.tar.gz \
&& tar --remove-files -xzvf bbmap.tar.gz

RUN pip install psutil
RUN apt install -y default-jre


WORKDIR /quackers_tools
RUN rm *.tar.gz \
&& rm *.zip \
&& rm *.bz2

RUN chmod -R 777 /quackers_tools

RUN apt-get install -y python-profiler

WORKDIR /quackers

RUN wget https://raw.githubusercontent.com/billytaj/quackers/develop/MetaPro_utilities.py 
RUN wget https://raw.githubusercontent.com/billytaj/quackers/develop/quackers_commands.py
RUN wget https://raw.githubusercontent.com/billytaj/quackers/develop/quackers_paths.py
RUN wget https://raw.githubusercontent.com/billytaj/quackers/develop/quackers_pipe.py
RUN wget https://raw.githubusercontent.com/billytaj/quackers/develop/quackers_stages.py

#WORKDIR /quackers/scripts
#RUN wget https://raw.githubusercontent.com/billytaj/quackers/develop/scripts/0a_Run_bbduk_trimming_filtering.sh

RUN pip install --force-reinstall -v "scikit-learn==1.1.0"

RUN pip install numpy \
&& pip install matplotlib \
&& pip install pysam \
&& pip install checkm-genome

WORKDIR /quackers_tools
RUN wget https://github.com/matsen/pplacer/releases/download/v1.1.alpha17/pplacer-Linux-v1.1.alpha17.zip -O pplacer.zip \
&& unzip pplacer.zip \
&& mv pplacer-Linux-v1.1.alpha17 pplacer \
&& rm *.zip



#for linux-only
WORKDIR /quackers_tools/checkm_data
RUN wget https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz \
&& tar -xzvf checkm_data_2015_01_16.tar.gz \
&& rm *.tar.gz

ENV CHECKM_DATA_PATH=/quackers_tools/checkm_data
ENV PATH="${PATH}:/quackers_tools/hmmer/src"
ENV PATH="${PATH}:/quackers_tools/prodigal"
ENV PATH="${PATH}:/quackers_tools/pplacer"

WORKDIR /quackers_tools
RUN apt-get install dos2unix




#/CONCOCT-1.1.0
CMD ["bash"]
