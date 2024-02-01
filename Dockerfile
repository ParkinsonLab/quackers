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
&& apt-get install -y libgsl-dev 

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

RUN pip install numpy \
&& pip install matplotlib \
&& pip install pysam \
&& pip install checkm-genome

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

RUN rm *.tar.gz \
&& rm *.zip \
&& rm *.bz2

RUN mv CONCOCT-1.1.0 concoct \
&& mv hmmer-3.4 hmmer \
&& mv Prodigal-2.6.3 prodigal \
&& mv MEGAHIT-1.2.9-Linux-x86_64-static megahit \
&& mv samtools-1.19.2 samtools \
&& mv GTDBTk-2.3.2 gtdbtk 

RUN chmod -R 777 /quackers_tools


WORKDIR /quackers_tools

#/CONCOCT-1.1.0
CMD ["bash"]
