FROM ubuntu:19.10
COPY sources.list /etc/apt/
COPY * /home/plugin/
RUN apt-get update \ 
 && mkdir /home/plugin/data \ 
 && mkdir /home/plugin/result 