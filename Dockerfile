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

WORKDIR /quackers_tools
RUN wget https://github.com/voutcn/megahit/releases/download/v1.2.9/MEGAHIT-1.2.9-Linux-x86_64-static.tar.gz \
&& tar zvxf MEGAHIT-1.2.9-Linux-x86_64-static.tar.gz


RUN chmod -R 777 /quackers_tools


WORKDIR /
CMD ["bash"]
