FROM python:3.7
COPY sources.list /etc/apt/
COPY * /home/plugin/
RUN apt-get update \ 
 && mkdir /home/plugin/data \ 
 && mkdir /home/plugin/result 
RUN apt install vim -y \ 