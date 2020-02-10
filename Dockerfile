FROM ubuntu:19.10
#USER daemon
#COPY sources.list /etc/apt/
# COPY * /home/plugin/
#RUN apt-get update
RUN mkdir -p /home/plugin/data
RUN mkdir -p /home/plugin/result 
RUN mkdir -p /home/test1 \
&& mkdir -p /home/test2 \
&& mkdir -p /home/test3 \
&& mkdir -p /home/test4 \
&& mkdir -p /home/test5 \
&& mkdir -p /home/test6 

